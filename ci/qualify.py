"""CI reference qualification; no adoption or deployment."""
import hashlib,json,pathlib,shutil,subprocess,sys,tempfile
root=pathlib.Path(__file__).resolve().parents[1]
pin="f2d48cdd98bd17f74bd826c1af96668110d98cf1205ba1dbd3ef7a758b57868c"
manifest=root/"evidence/stonewall-0/m01-r3/repair-manifest.json"
if hashlib.sha256(manifest.read_bytes()).hexdigest()!=pin: raise SystemExit("Historical R3 manifest changed")
for path in root.rglob("*.json"):
 if ".git" not in path.parts: json.loads(path.read_text(encoding="utf-8-sig"))
with tempfile.TemporaryDirectory(prefix="brain-reference-") as directory:
 snapshot=pathlib.Path(directory)/"repo"
 shutil.copytree(root,snapshot,ignore=shutil.ignore_patterns(".git","__pycache__","ci-results"))
 # The only deliberate change to a historical bound path is the hardened ignore file.
 # Restore its preserved preimage solely in this disposable qualification snapshot.
 shutil.copyfile(root/"ci/r3-original.gitignore",snapshot/".gitignore")
 for optimized in (False,True):
  command=[sys.executable,"-I","-B"]
  if optimized: command.append("-O")
  for task in ("suite","legacy-schema","probe-code"):
   subprocess.run(command+[str(snapshot/"qualify_m01_r3.py"),"--repo",str(snapshot),"--manifest-sha256",pin,"--task",task],check=True)
print("REFERENCE QUALIFICATION PASS; production authority remains unresolved")
