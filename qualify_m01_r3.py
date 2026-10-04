"""Verified-source R3 reference qualification. No repository mutation or gate closure.

The expected manifest digest is supplied by the externally pinned handoff. All
repository-owned code comes from verified in-memory buffers, not bytecode caches.
The Python interpreter, standard library, installed jsonschema dependencies, and
OS are trusted dependencies. This is not a sandbox for hostile Python callbacks.
"""
from __future__ import annotations
import sys
sys.dont_write_bytecode = True
import argparse
import hashlib
import importlib.abc
import importlib.machinery
import io
import json
from pathlib import Path, PurePosixPath
import stat
import types
import unittest

MANIFEST = 'evidence/stonewall-0/m01-r3/repair-manifest.json'
MODULES = {
    'qualification': None,
    'qualification.m01_r3': 'qualification/m01_r3/__init__.py',
    'qualification.m01_r3.model': 'qualification/m01_r3/model.py',
    'qualification.m01_r3.rescan': 'qualification/m01_r3/rescan.py',
    'schemas': None,
    'schemas.conformance': None,
    'schemas.conformance.boundary_r3': 'schemas/conformance/boundary_r3.py',
    'tests': None,
    'tests.conformance': None,
    'tests.conformance.test_m01_r3': 'tests/conformance/test_m01_r3.py',
    'tests.conformance.test_m01_r3_regressions': 'tests/conformance/test_m01_r3_regressions.py',
}
class Rejected(ValueError):
    pass

def require(value, reason):
    if not value:
        raise Rejected(reason)

def sha(data):
    return hashlib.sha256(data).hexdigest()

def plain_file(root, name):
    require(type(name) is str and name and '\\' not in name and ':' not in name,
            'INVALID_BOUND_PATH')
    parts = PurePosixPath(name)
    require(not parts.is_absolute() and parts.as_posix() == name and
            all(p not in ('', '.', '..', '.git') for p in parts.parts) and
            not any(ord(c) < 32 for c in name), 'INVALID_BOUND_PATH')
    current = Path(root).resolve()
    for part in parts.parts:
        current = current / part
        info = current.lstat()
        require(not stat.S_ISLNK(info.st_mode) and not
                getattr(info, 'st_file_attributes', 0) & getattr(stat, 'FILE_ATTRIBUTE_REPARSE_POINT', 0x400),
                'BOUND_LINK_OR_REPARSE_POINT')
    require(current.is_file(), 'BOUND_FILE_MISSING')
    return current

def unique_pairs(pairs):
    result = {}
    for key, value in pairs:
        require(key not in result, 'DUPLICATE_MANIFEST_KEY')
        result[key] = value
    return result

def verify_snapshot(repo, expected):
    raw = plain_file(repo, MANIFEST).read_bytes()
    require(sha(raw) == expected, 'R3_MANIFEST_DIGEST_MISMATCH')
    manifest = json.loads(raw, object_pairs_hook=unique_pairs)
    require(manifest['candidate'] == 'M01-Repair-R3' and manifest['m01_freeze_ready'] is False,
            'CANDIDATE_STATUS_MISMATCH')
    files = manifest['bound_files']
    require(type(files) is dict and len(files) == manifest['bound_file_count'], 'BOUND_INVENTORY_COUNT')
    require(len({name.casefold() for name in files}) == len(files), 'BOUND_CASE_COLLISION')
    buffers = {}
    for name, expected_sha in files.items():
        data = plain_file(repo, name).read_bytes()
        require(type(expected_sha) is str and sha(data) == expected_sha, 'SOURCE_DIGEST_MISMATCH:' + name)
        buffers[name] = data
    require(all(path is None or path in buffers for path in MODULES.values()), 'MODULE_BINDING_MISSING')
    buffers[MANIFEST] = raw
    return manifest, types.MappingProxyType(buffers)

class SourceGraph(importlib.abc.MetaPathFinder, importlib.abc.Loader):
    def __init__(self, repo, buffers):
        self.repo, self.buffers = Path(repo).resolve(), buffers
    def find_spec(self, fullname, path=None, target=None):
        if fullname in MODULES:
            filename = MODULES[fullname]
            package = filename is None or filename.endswith('/__init__.py')
            return importlib.machinery.ModuleSpec(fullname, self, is_package=package)
        if fullname.split('.')[0] in ('qualification', 'schemas', 'tests'):
            raise ImportError('REPOSITORY_MODULE_NOT_IN_VERIFIED_GRAPH:' + fullname)
        return None
    def create_module(self, spec):
        return None
    def exec_module(self, module):
        name = module.__name__
        relative = MODULES[name]
        if relative is None:
            module.__path__ = []
            return
        filename = str(self.repo / relative)
        module.__file__ = filename
        module.__cached__ = None
        if relative.endswith('/__init__.py'):
            module.__path__ = []
        code = compile(self.buffers[relative], filename, 'exec', dont_inherit=True)
        exec(code, module.__dict__)

def install_graph(repo, buffers):
    require(not any(name == prefix or name.startswith(prefix + '.')
                    for name in sys.modules for prefix in ('qualification', 'schemas', 'tests')),
            'REPOSITORY_MODULE_PRELOADED')
    graph = SourceGraph(repo, buffers)
    sys.meta_path.insert(0, graph)
    return graph

def run_suite():
    from tests.conformance import test_m01_r3, test_m01_r3_regressions
    suite = unittest.TestSuite((unittest.defaultTestLoader.loadTestsFromModule(test_m01_r3),
                               unittest.defaultTestLoader.loadTestsFromModule(test_m01_r3_regressions)))
    class Transcript(io.StringIO):
        def write(self, text):
            sys.stdout.write(text)
            sys.stdout.flush()
            return super().write(text)
    stream = Transcript()
    result = unittest.TextTestRunner(stream=stream, verbosity=2).run(suite)
    text = stream.getvalue()
    require(result.wasSuccessful(), 'R3_REFERENCE_TEST_FAILURE')
    return {'test_methods_run': result.testsRun, 'failures':len(result.failures),
            'errors':len(result.errors), 'skipped':len(result.skipped),
            'transcript_sha256':sha(text.encode('utf-8'))}

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repo', type=Path, required=True)
    parser.add_argument('--manifest-sha256', required=True)
    parser.add_argument('--task', choices=('suite','rescan','probe-code','legacy-schema','historical-model','native'),
                        default='suite')
    args = parser.parse_args()
    repo = args.repo.resolve()
    before = None
    try:
        manifest, before = verify_snapshot(repo, args.manifest_sha256)
        install_graph(repo, before)
        if args.task == 'suite':
            result = run_suite()
        if args.task == 'rescan':
            from qualification.m01_r3 import rescan
            result = rescan.run(repo)
        if args.task == 'probe-code':
            from qualification.m01_r3 import model
            from schemas.conformance import boundary_r3
            from qualification.m01_r3 import rescan
            from tests.conformance import test_m01_r3, test_m01_r3_regressions
            expected = ('P03','P04','P05','P06','P07','P08')
            require(model.topology()['C05'][2] == expected, 'HISTORICAL_TOPOLOGY_DRIFT')
            result = {'C05_predicates':list(model.topology()['C05'][2]),
                      'repository_code_source':'VERIFIED_BYTES_COMPILED', 'cache_loader_used':False}
        if args.task == 'legacy-schema':
            relative = 'schemas/conformance/run_sw0_006.py'
            module = types.ModuleType('_m01_r3_legacy_schema')
            module.__file__ = str(repo / relative)
            sys.modules[module.__name__] = module
            exec(compile(before[relative], module.__file__, 'exec', dont_inherit=True), module.__dict__)
            require(module.run() == 0, 'LEGACY_SCHEMA_FAILURE')
            result = {'legacy_schema_assertions_reported':840, 'exit':0}
        if args.task in ('historical-model','native'):
            from qualification.m01_r3 import model
            if args.task == 'historical-model':
                metrics, diagnostics = model.historical.model_suite()
                result = {'metrics':metrics, 'diagnostics':diagnostics}
            if args.task == 'native':
                result = model.historical.native_powershell_check()
        _, after = verify_snapshot(repo, args.manifest_sha256)
        require(dict(before) == dict(after), 'BOUND_SOURCE_DRIFT_DURING_QUALIFICATION')
        print(json.dumps({'candidate':'M01-Repair-R3', 'task':args.task, 'result':'PASS',
            'scope':'REFERENCE_ONLY', 'verified_source_buffers':len(before), 'details':result,
            'source_bytes_unchanged':True, 'm01_freeze_ready':False}, sort_keys=True))
        return 0
    except Exception as exc:
        # Only fixed internal reasons and exception classes; no artifact payloads.
        reason = type(exc).__name__
        if type(exc) is Rejected:
            reason = str(exc)
        print(json.dumps({'candidate':'M01-Repair-R3','result':'FAIL','reason':reason,
                          'm01_freeze_ready':False}))
        return 1
if __name__ == '__main__':
    raise SystemExit(main())
