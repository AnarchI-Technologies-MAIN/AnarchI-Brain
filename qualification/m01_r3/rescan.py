"""Complete, location-independent historical byte checks for the R3 reference candidate."""
from __future__ import annotations
import hashlib
import json
from pathlib import Path, PurePosixPath, PureWindowsPath
import re
import stat

OLD_ROOT = PureWindowsPath('C:/AnarchI-Brain')
EXPECTED_ORIGINALS = 56
EXPECTED_UNCHANGED = 49

class Rejected(ValueError):
    pass

def require(value, reason):
    if not value:
        raise Rejected(reason)

def relative_name(value):
    require(type(value) is str and value and '\\' not in value and ':' not in value,
            'RELATIVE_PATH_REQUIRED')
    path = PurePosixPath(value)
    require(not path.is_absolute() and str(path) == value and
            all(part not in ('', '.', '..') for part in path.parts) and
            '.git' not in path.parts and not any(ord(c) < 32 for c in value), 'UNSAFE_RELATIVE_PATH')
    return value

def plain_file(root, relative):
    root = Path(root).resolve()
    name = relative_name(relative)
    current = root
    for part in PurePosixPath(name).parts:
        current = current / part
        info = current.lstat()
        require(not stat.S_ISLNK(info.st_mode) and not
                getattr(info, 'st_file_attributes', 0) & getattr(stat, 'FILE_ATTRIBUTE_REPARSE_POINT', 0x400),
                'LINK_OR_REPARSE_POINT')
    require(current.is_file(), 'HISTORICAL_FILE_MISSING')
    return current

def expected_mapping(preservation, r2_manifest):
    """Original absolute paths are evidence only; never compare them to today's root."""
    found = {}
    sources = preservation['original_sources']
    require(type(sources) is dict, 'ORIGINAL_SOURCE_MAP_REQUIRED')
    for original, metadata in sources.items():
        require(type(original) is str, 'ORIGINAL_PATH_TYPE')
        old = PureWindowsPath(original)
        if not old.is_relative_to(OLD_ROOT):
            continue  # External originals are separately covered by preserved_copies.
        relative = relative_name(old.relative_to(OLD_ROOT).as_posix())
        require(relative.casefold() not in {x.casefold() for x in found}, 'DUPLICATE_ORIGINAL_PATH')
        require(re.fullmatch('[0-9a-f]{64}', metadata.get('sha256', '')) is not None,
                'ORIGINAL_DIGEST_REQUIRED')
        found[relative] = {'original_location': original, 'sha256': metadata['sha256']}
    require(len(found) == EXPECTED_ORIGINALS, 'ORIGINAL_COVERAGE_INCOMPLETE')
    changed = r2_manifest['authorized_modified_files']
    require(type(changed) is list and len(changed) == 7 and len(set(changed)) == 7,
            'AMENDMENT_SET_INCOMPLETE')
    require(set(changed).issubset(found), 'AMENDMENT_OUTSIDE_ORIGINALS')
    unchanged = set(found) - set(changed)
    require(len(unchanged) == EXPECTED_UNCHANGED, 'UNCHANGED_COVERAGE_INCOMPLETE')
    return found, unchanged

def verify_history(repo, preservation, r2_manifest, mapping):
    expected, unchanged = expected_mapping(preservation, r2_manifest)
    require(type(mapping) is dict and mapping.get('version') == 'M01-R3-HISTORICAL-MAP-v1', 'MAP_VERSION')
    rows = mapping.get('originals')
    require(type(rows) is list and len(rows) == EXPECTED_ORIGINALS, 'MAP_COVERAGE_INCOMPLETE')
    actual = {}
    for row in rows:
        require(type(row) is dict and set(row) == {'path','original_location','sha256','comparison'},
                'MAP_ROW_SHAPE')
        name = relative_name(row['path'])
        require(name.casefold() not in {x.casefold() for x in actual}, 'DUPLICATE_MAP_PATH')
        require(name in expected, 'UNMAPPED_HISTORICAL_PATH')
        comparison = 'R2_AMENDED_RETAINED_AS_CANDIDATE'
        if name in unchanged:
            comparison = 'UNCHANGED_ORIGINAL'
        require(row == dict(path=name, **expected[name], comparison=comparison), 'MAP_IDENTITY_MISMATCH')
        actual[name] = row
    require(set(actual) == set(expected), 'MAP_IDENTITY_SET_INCOMPLETE')
    for name in sorted(unchanged):
        require(hashlib.sha256(plain_file(repo, name).read_bytes()).hexdigest() == expected[name]['sha256'],
                'HISTORICAL_BYTES_CHANGED:' + name)
    copies = preservation['preserved_copies']
    require(type(copies) is list and len(copies) == 9 and len({x['path'] for x in copies}) == 9,
            'PRESERVED_COPY_COVERAGE')
    for item in copies:
        require(hashlib.sha256(plain_file(repo, item['path']).read_bytes()).hexdigest() == item['sha256'],
                'PRESERVED_COPY_CHANGED')
    return {'original_identity_set':56, 'unchanged_originals_checked':49,
            'original_candidate_amendments':7, 'preserved_copies_checked':9,
            'repository_location_used_for_selection':False}

def run(repo):
    repo = Path(repo)
    def read(name):
        return json.loads(plain_file(repo, name).read_bytes())
    return verify_history(repo,
        read('evidence/stonewall-0/m01-r2/preservation.json'),
        read('evidence/stonewall-0/m01-r2/repair-manifest.json'),
        read('evidence/stonewall-0/m01-r3/historical-map.json'))
