"""R2 candidate qualification; exact source bundle and index observations, no effects."""
from __future__ import annotations
import sys
sys.dont_write_bytecode = True
import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import tempfile

BASE_HEAD = '79fd607b3b8983fdd2d0254f3af59df9a92257b8'
R1_SHA = 'cb8a492c4667ffaaf0ef1ac1b62f2c9883c9e90d09873d470aeb47175a100a6c'
OVERRIDES = ('GIT_DIR','GIT_WORK_TREE','GIT_INDEX_FILE','GIT_OBJECT_DIRECTORY',
             'GIT_ALTERNATE_OBJECT_DIRECTORIES','GIT_COMMON_DIR','GIT_NAMESPACE')
class Rejected(ValueError):
    pass
def require(value, reason):
    if not value:
        raise Rejected(reason)
def git(repo, *args):
    require(not any(os.environ.get(k) for k in OVERRIDES), 'GIT_CONTEXT_OVERRIDE')
    result = subprocess.run(['git','--no-optional-locks','-c','core.fsmonitor=false','-C',str(repo),*args],
                            capture_output=True, check=False, timeout=30)
    require(result.returncode == 0, 'GIT_READ_FAILED')
    return result.stdout
def snapshot(repo):
    head = git(repo,'rev-parse','HEAD').decode().strip()
    require(head == BASE_HEAD, 'HEAD_DRIFT')
    names = (git(repo,'ls-files','-z') + git(repo,'ls-files','--others','--exclude-standard','-z')).decode().split('\0')
    files = {}
    for name in sorted(set(x for x in names if x)):
        path = (repo / name).resolve()
        require(path.is_relative_to(repo), 'SOURCE_PATH_OUTSIDE_REPO')
        require(path.is_file(), 'SOURCE_FILE_MISSING')
        files[name] = hashlib.sha256(path.read_bytes()).hexdigest()
    index = Path(git(repo,'rev-parse','--git-path','index').decode().strip())
    if not index.is_absolute():
        index = repo / index
    return {'head':head,'tree':git(repo,'rev-parse','HEAD^{tree}').decode().strip(),
            'index_sha256':hashlib.sha256(index.read_bytes()).hexdigest(),
            'sources':files,'status':git(repo,'status','--porcelain=v1','--untracked-files=all').decode()}
def verify_bundle(repo):
    path = repo / 'evidence/stonewall-0/m01-r2/repair-manifest.json'
    manifest = json.loads(path.read_text())
    require(manifest['baseline_head'] == BASE_HEAD, 'MANIFEST_HEAD')
    for name, digest in manifest['bound_files'].items():
        target = (repo / name).resolve()
        require(target.is_relative_to(repo), 'BUNDLE_PATH_OUTSIDE_REPO')
        require(hashlib.sha256(target.read_bytes()).hexdigest() == digest, 'BUNDLE_IDENTITY:' + name)
    before = snapshot(repo)
    allowed = set(manifest['authorized_modified_files']) | set(manifest['bound_files']) | {
        'evidence/stonewall-0/m01-r2/repair-manifest.json'}
    changed = set(filter(None, git(repo,'diff','--name-only','-z').decode().split('\0')))
    changed.update(filter(None, git(repo,'ls-files','--others','--exclude-standard','-z').decode().split('\0')))
    require(changed.issubset(allowed), 'UNAUTHORIZED_WORKSPACE_CHANGE')
    require(before['index_sha256'] == manifest['baseline_index_sha256'], 'INDEX_DRIFT')
    return before, hashlib.sha256(path.read_bytes()).hexdigest()
def child(command):
    result = subprocess.run(command, capture_output=True, text=True, timeout=90)
    require(result.returncode == 0, 'QUALIFICATION_CHILD_FAILED:' + result.stderr[-1200:])
    return result
def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repo', type=Path, default=Path(__file__).resolve().parents[2])
    parser.add_argument('--historical-runner', type=Path)
    parser.add_argument('--input-check-only', action='store_true')
    args = parser.parse_args()
    repo = args.repo.resolve()
    try:
        runner = args.historical_runner if args.historical_runner is not None else repo / 'qualification/m01_r2/history/repair_r1.py'
        require(hashlib.sha256(runner.read_bytes()).hexdigest() == R1_SHA, 'HISTORICAL_RUNNER_IDENTITY')
        if args.input_check_only:
            print('INPUT_IDENTITY=PASS\nSCOPE=INPUT_CHECK_ONLY')
            return 0
        before, manifest_sha = verify_bundle(repo)
        sys.path.insert(0, str(repo))
        from qualification.m01_r2 import model
        normal = child([sys.executable,'-B',str(repo / 'tests/conformance/test_m01_r2.py')])
        optimized = child([sys.executable,'-O','-B',str(repo / 'tests/conformance/test_m01_r2.py')])
        legacy = child([sys.executable,'-B',str(repo / 'schemas/conformance/run_sw0_006.py')])
        # Deliberately mutated bytes must fail even when Python removes assertions.
        with tempfile.TemporaryDirectory(prefix='anarchi-r2-input-') as temp:
            wrong = Path(temp) / 'UNTRUSTED_CHANGED_RUNNER.py'
            wrong.write_bytes(runner.read_bytes() + b'\n# TEST MUTATION\n')
            rejection = subprocess.run([sys.executable,'-O','-B',str(Path(__file__)),
                          '--historical-runner',str(wrong),'--input-check-only'],
                          capture_output=True, text=True, timeout=30)
            require(rejection.returncode != 0 and 'HISTORICAL_RUNNER_IDENTITY' in rejection.stdout,
                    'OPTIMIZED_IDENTITY_CONTROL_FAILED')
        with tempfile.TemporaryDirectory(prefix='anarchi-r2-checkout-') as temp:
            checkout = Path(temp) / 'repo'
            child(['git','-c','core.autocrlf=true','clone','--quiet','--no-hardlinks','--no-checkout',str(repo),str(checkout)])
            # Prospective source snapshot policy, without committing/staging the source repository.
            (checkout / '.gitattributes').write_bytes((repo / '.gitattributes').read_bytes())
            child(['git','-C',str(checkout),'-c','core.autocrlf=true','checkout','--quiet','HEAD'])
            portable = child([sys.executable,'-B',str(checkout / 'schemas/conformance/run_sw0_006.py')])
            require('FAILURE_COUNT=0' in portable.stdout, 'CHECKOUT_CORPUS_FAILED')
        metrics, diagnostics = model.historical.model_suite()
        native = model.historical.native_powershell_check()
        after = snapshot(repo)
        require(before == after, 'SOURCE_OR_INDEX_CHANGED_DURING_QUALIFICATION')
        summary = {'candidate':'M01-R2','scope':'REFERENCE_QUALIFICATION_ONLY',
                   'manifest_sha256':manifest_sha,'head_tree_index_unchanged':True,
                   'source_bytes_unchanged_during_run':True,
                   'authorized_dirty_worktree':bool(before['status']),
                   'normal_suite_output':normal.stdout + normal.stderr,
                   'optimized_suite_output':optimized.stdout + optimized.stderr,
                   'legacy_schema_output':legacy.stdout,
                   'checkout_scope':'fresh baseline checkout with the prospective .gitattributes overlay',
                   'prospective_checkout_output':portable.stdout,
                   'optimized_mutated_runner_rejected':True,
                   'historical_reference_metrics':metrics,'native_regression':native,
                   'admission_authentication_implemented':False,
                   'durable_or_atomic_effect_runtime_implemented':False,
                   'all_original_findings_closed':False,'m01_freeze_ready':False,'result':'PASS'}
        print(json.dumps(summary, indent=2))
        return 0
    except Exception as exc:
        # Fixed messages contain no artifact payloads or keys.
        print(json.dumps({'candidate':'M01-R2','result':'FAIL','reason':str(exc),
                          'm01_freeze_ready':False}))
        return 1
if __name__ == '__main__':
    raise SystemExit(main())

