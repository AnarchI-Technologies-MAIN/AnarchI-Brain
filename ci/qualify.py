"""Qualify committed HEAD in disposable Git checkouts; reference scope only."""
import hashlib
import io
import json
from pathlib import Path, PurePosixPath
import stat
import subprocess
import sys
import tarfile
import tempfile

ROOT = Path(__file__).resolve().parents[1]
PIN = "f2d48cdd98bd17f74bd826c1af96668110d98cf1205ba1dbd3ef7a758b57868c"
MANIFEST = "evidence/stonewall-0/m01-r3/repair-manifest.json"
PREIMAGES = {".gitignore": "ci/r3-original.gitignore",
             "README.md": "ci/r3-original.README.md"}
# Check and compile the very same buffer before any launcher code runs.
VERIFIED_STUB = (
    "import hashlib,sys; p=sys.argv[1]; expected=sys.argv[2]; b=open(p,'rb').read(); "
    "hashlib.sha256(b).hexdigest()==expected or sys.exit('LAUNCHER_IDENTITY_MISMATCH'); "
    "sys.argv=[p]+sys.argv[3:]; "
    "exec(compile(b,p,'exec',dont_inherit=True),{'__name__':'__main__','__file__':p})"
)


def git(repo, *args):
    return subprocess.run(["git", "-C", str(repo), *args], check=True,
                          capture_output=True).stdout


def plain_bytes(root, name):
    path = PurePosixPath(name)
    if (not name or path.is_absolute() or path.as_posix() != name or
            "\\" in name or ":" in name or
            any(p in (".", "..", ".git") for p in path.parts)):
        raise ValueError("INVALID_BOUND_PATH")
    current = root
    for part in path.parts:
        current = current / part
        info = current.lstat()
        if (stat.S_ISLNK(info.st_mode) or
                getattr(info, "st_file_attributes", 0) & 0x400):
            raise ValueError("BOUND_LINK_OR_REPARSE_POINT")
    return current.read_bytes()


def read_manifest(root):
    raw = plain_bytes(root, MANIFEST)
    if hashlib.sha256(raw).hexdigest() != PIN:
        raise ValueError("Historical R3 manifest changed")
    return json.loads(raw)


def verify_checkout(root, manifest):
    read_manifest(root)
    for name, expected in manifest["bound_files"].items():
        if hashlib.sha256(plain_bytes(root, name)).hexdigest() != expected:
            raise ValueError("SOURCE_DIGEST_MISMATCH:" + name)


def prepare_candidate(repo, destination):
    """Export committed candidate; never stage the caller's index."""
    destination.mkdir()
    with tarfile.open(fileobj=io.BytesIO(git(repo, "archive", "HEAD"))) as archive:
        archive.extractall(destination, filter="data")
    manifest = read_manifest(destination)
    for name, preserved in PREIMAGES.items():
        data = plain_bytes(destination, preserved)
        if hashlib.sha256(data).hexdigest() != manifest["bound_files"][name]:
            raise ValueError("Historical preimage mismatch:" + name)
        (destination / name).write_bytes(data)
    verify_checkout(destination, manifest)
    for path in destination.rglob("*.json"):
        json.loads(path.read_text(encoding="utf-8-sig"))
    git(destination, "init", "--quiet")
    git(destination, "-c", "core.autocrlf=false", "add", "--all", "--force", ".")
    git(destination, "-c", "user.name=Disposable qualification", "-c",
        "user.email=qualification@example.invalid", "-c", "commit.gpgsign=false",
        "commit", "--quiet", "-m", "Disposable reference candidate")
    return manifest


def checkout_candidate(candidate, target, autocrlf, manifest):
    subprocess.run(["git", "-c", "core.autocrlf=" + autocrlf, "clone",
                    "--quiet", "--no-local", str(candidate), str(target)], check=True)
    verify_checkout(target, manifest)


def child_command(snapshot, manifest, optimized, task):
    return [sys.executable, "-I", "-B", *(["-O"] if optimized else []),
            "-c", VERIFIED_STUB, str(snapshot / "qualify_m01_r3.py"),
            manifest["bound_files"]["qualify_m01_r3.py"], "--repo", str(snapshot),
            "--manifest-sha256", PIN, "--task", task]


def main():
    with tempfile.TemporaryDirectory(prefix="brain-reference-") as directory:
        temporary = Path(directory)
        candidate = temporary / "candidate"
        manifest = prepare_candidate(ROOT, candidate)
        for autocrlf in ("false", "true"):
            snapshot = temporary / ("checkout-" + autocrlf)
            checkout_candidate(candidate, snapshot, autocrlf, manifest)
            for optimized in (False, True):
                for task in ("suite", "legacy-schema", "probe-code"):
                    subprocess.run(child_command(snapshot, manifest, optimized, task),
                                   check=True)
                    verify_checkout(snapshot, manifest)
            print("FULL MANIFEST CHECKOUT PASS; core.autocrlf=" + autocrlf, flush=True)
    print("REFERENCE QUALIFICATION PASS; production authority remains unresolved")


if __name__ == "__main__":
    main()
