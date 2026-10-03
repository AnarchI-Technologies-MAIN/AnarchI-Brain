"""Fresh structural rescan of the exact R2 candidate bundle."""
import sys
sys.dont_write_bytecode = True
import ast
import hashlib
import json
from pathlib import Path
import re
import subprocess
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from qualification.m01_r2.qualify import verify_bundle, require, snapshot
def main():
    repo = Path(__file__).resolve().parents[2]
    before, digest = verify_bundle(repo)
    root = repo / 'evidence/stonewall-0/m01-r2'
    preservation = json.loads((root / 'preservation.json').read_text())
    manifest = json.loads((root / 'repair-manifest.json').read_text())
    changed = set(manifest['authorized_modified_files'])
    checked = 0
    for name, item in preservation['original_sources'].items():
        path = Path(name)
        if path.is_relative_to(repo) and path.relative_to(repo).as_posix() not in changed:
            require(hashlib.sha256(path.read_bytes()).hexdigest() == item['sha256'], 'BASELINE_BYTES_CHANGED:' + name)
            checked += 1
    matrix = 'contracts/organs/AUTHORITY-MATRIX.md'
    original = subprocess.check_output(['git','-C',str(repo),'show','HEAD:' + matrix]).decode()
    current = (repo / matrix).read_text()
    cells = lambda text: [line.strip() for line in text.splitlines() if line.startswith('|') and not ('Candidate' in line or 'candidate' in line)]
    require(cells(original) == cells(current), 'AUTHORITY_CELLS_CHANGED')
    names = re.findall(r'^\d+\. (.+)$', (repo / 'constitution/state-machines/REGISTRY.md').read_text(), re.M)
    obligations = json.loads((root / 'obligations.json').read_text())
    require(len(names) == 19 and [m['registry_name'] for m in obligations['machines']] == names, 'LIFECYCLE_DRIFT')
    ledger = json.loads((root / 'findings-ledger.json').read_text())
    require([f['id'] for f in ledger['findings']] == ['A%02d' % i for i in range(1,21)], 'FINDING_LOSS')
    require(ledger['all_findings_closed'] is False and ledger['m01_freeze_ready'] is False and ledger['freeze_blockers'], 'UNSUPPORTED_CLOSURE')
    active = ['schemas/conformance/boundary_r2.py'] + sorted(n for n in manifest['bound_files'] if n.startswith('qualification/m01_r2/') and n.endswith('.py') and '/history/' not in n) + ['tests/conformance/test_m01_r2.py']
    for name in active:
        require(not any(isinstance(node, ast.Assert) for node in ast.walk(ast.parse((repo / name).read_text()))), 'OPTIMIZABLE_GUARD:' + name)
    require(snapshot(repo) == before, 'RESCAN_SOURCE_DRIFT')
    print(json.dumps({'result':'PASS','scope':'candidate structural rescan; runtime proof remains unavailable',
        'manifest_sha256':digest,'unchanged_original_repository_files':checked,
        'authority_cells_unchanged':True,'registry_machine_count':len(names),'active_python_files_scanned':len(active),
        'findings':ledger['findings'],'freeze_blockers':ledger['freeze_blockers'],
        'all_findings_closed':False,'m01_freeze_ready':False},indent=2))
if __name__ == '__main__':
    main()

