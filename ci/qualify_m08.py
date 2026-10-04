"""Offline M08 source qualification; no adoption or deployment."""
import hashlib,json,pathlib,subprocess,sys,tempfile
root=pathlib.Path(__file__).resolve().parents[1]/'development-review/m08-v8'
pin='a44def170668cf17d25c51f50fcbf4556f491dfc69d4bc5e4cea0d2ff0102f79'
raw=(root/'package-manifest.json').read_bytes()
if hashlib.sha256(raw).hexdigest()!=pin:raise SystemExit('M08_PACKAGE_MANIFEST_DRIFT')
manifest=json.loads(raw)
for name,identity in manifest['files'].items():
    path=root/name
    if not path.resolve().is_relative_to(root.resolve()):raise SystemExit('M08_PATH_ESCAPE')
    data=path.read_bytes()
    if len(data)!=identity['bytes'] or hashlib.sha256(data).hexdigest()!=identity['sha256']:raise SystemExit('M08_SOURCE_DRIFT:'+name)
for optimized in (False,True):
    command=[sys.executable,'-I','-B']+(['-O'] if optimized else [])
    result=subprocess.run(command+[str(root/'run_qualification.py'),'--child'],capture_output=True,text=True,check=True,timeout=120)
    receipt=json.loads(result.stdout)
    if len(receipt['semantic_mutations'])!=161 or receipt['m08_joint_routes_checked']!=720 or receipt['production_ready'] or receipt['runtime_machine_transitions']!=0:raise SystemExit('M08_QUALIFICATION_SCOPE_DRIFT')
    with tempfile.TemporaryDirectory(prefix='brain-m08-oracle-') as directory:
        output=pathlib.Path(directory)/'oracle.json'
        subprocess.run(command+[str(root/'reproduce_m08_oracle.py'),'--output',str(output)],capture_output=True,text=True,check=True,timeout=30)
        if output.read_bytes()!=(root/'successor/m08-denial-routing-table.json').read_bytes():raise SystemExit('M08_ORACLE_REPRODUCTION_DRIFT')
    print(json.dumps(dict(mode='optimized' if optimized else 'normal',semantic_mutants=161,joint_routes=720,production_ready=False,scope='STATIC_PURE_MODEL_ONLY')))
