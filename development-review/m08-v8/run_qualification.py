from pathlib import Path
import hashlib,json,subprocess,sys,types

ROOT=Path(__file__).resolve().parent
def digest(data):return hashlib.sha256(data).hexdigest()
def require(value,reason):
    if not value:raise ValueError(reason)
if '--child' in sys.argv:
    record=json.loads((ROOT/'execution-inputs.json').read_bytes())
    buffers={name:(ROOT/name).read_bytes() for name in record['files']}
    for name,identity in record['files'].items():
        require(digest(buffers[name])==identity['sha256'] and len(buffers[name])==identity['bytes'],'PREEXEC_IDENTITY:'+name)
    for module_name in ('reference_semantics','test_reference'):
        module=types.ModuleType(module_name);module.__file__=str(ROOT/(module_name+'.py'));sys.modules[module_name]=module
        exec(compile(buffers[module_name+'.py'],module.__file__,'exec',dont_inherit=True),module.__dict__)
    result=sys.modules['test_reference'].run(record['expected_reference_sha256'], buffers)
    for name,identity in record['files'].items():require(digest((ROOT/name).read_bytes())==identity['sha256'],'POSTEXEC_DRIFT:'+name)
    result['verified_input_files']=len(buffers);result['source_buffers_compiled']=True
    result['optimized']=sys.flags.optimize;print(json.dumps(result,sort_keys=True))
    sys.exit(0)
files={}
for directory in ('inputs','successor'):
    for path in sorted((ROOT/directory).rglob('*')):
        if path.is_file():files[path.relative_to(ROOT).as_posix()]={'bytes':path.stat().st_size,'sha256':digest(path.read_bytes())}
for name in ('reference_semantics.py','test_reference.py','build_successor.py','run_qualification.py','input-custody.json','evidence/source-before.json'):
    raw=(ROOT/name).read_bytes();files[name]={'bytes':len(raw),'sha256':digest(raw)}
record={'files':files,'expected_reference_sha256':files['successor/expected-classifications.json']['sha256'],'scope':'PREEXEC_BINDING_OBSERVATION_NO_ATOMIC_LOCK'}
with (ROOT/'execution-inputs.json').open('x',encoding='utf-8') as f:json.dump(record,f,indent=2)
for mode in ('normal','optimized'):
    command=[sys.executable,'-I','-B']
    if mode=='optimized':command.append('-O')
    command += [str(Path(__file__).resolve()),'--child']
    result=subprocess.run(command,capture_output=True,text=True)
    (ROOT/'evidence'/f'{mode}.stdout.txt').write_text(result.stdout,encoding='utf-8')
    (ROOT/'evidence'/f'{mode}.stderr.txt').write_text(result.stderr,encoding='utf-8')
    require(result.returncode==0,'QUALIFICATION_FAILED:'+mode)
    output=json.loads(result.stdout)
    with (ROOT/'evidence'/f'{mode}.json').open('x',encoding='utf-8') as f:json.dump({'command':command,'exit_code':result.returncode,'result':output},f,indent=2)
    print(mode,output['baseline'],len(output['semantic_mutations']),output['abort_component_combinations'],output['atlas_component_combinations'])
for name,identity in files.items():require(digest((ROOT/name).read_bytes())==identity['sha256'],'RUNNER_POSTEXEC_DRIFT:'+name)
print('Verified before/after identities; no runtime, publication, host activation, import or authority issuance.')
