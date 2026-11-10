"""Hash-exact historical inputs for tests, isolated from release construction.

Retention may remove old .nds outputs, including deliberately retired releases.
These recipes recover their original bytes from the accepted canonical source;
they do not change release status or invoke/relax the playable release gate.
Only allowlisted whole-ROM identities are accepted. Artifacts use .romfixture,
never a release filename, and must not be launched or used as release parents.
"""

from collections import defaultdict
import hashlib
import json
import os
from pathlib import Path
import tempfile

from dk4tool.rom.nds import NdsImage
from scripts import build_integrated_release as batch_api

ROOT = Path(__file__).resolve().parents[1]
RECIPES = ROOT/'tests/fixtures/historical_roms_v1.json'
CACHE = ROOT/'out/test-fixtures/historical'


def digest(data):
    return hashlib.sha256(data).hexdigest()


def cache_location(cache):
    path = Path(cache).resolve()
    if os.name == 'nt' and not str(path).startswith('\\\\?\\'):
        path = Path('\\\\?\\'+str(path))
    return path


def load_recipe(name):
    document = json.loads(RECIPES.read_text(encoding='utf-8'))
    if document.get('format') != 'dk4-historical-test-fixtures-v1':
        raise ValueError('Unknown historical fixture schema')
    if name not in document['recipes']:
        raise ValueError('Historical fixture must have an explicit original identity')
    return document, document['recipes'][name]


def _archived_image(document, recipe):
    base = ROOT/document['base']
    if digest(base.read_bytes()) != recipe['base_sha256']:
        raise ValueError('Historical fixture canonical source hash differs')
    grouped = defaultdict(list)
    for name in recipe['batches']:
        path = ROOT/name
        if digest(path.read_bytes()) != document['input_sha256'][name]:
            raise ValueError(f'Historical fixture batch hash differs: {name}')
        header = batch_api.load_batch_header(path)
        grouped[header['file_path']].append(path)
    image = NdsImage.open(base)
    for file_path, paths in batch_api.order_graphics_sync_groups(grouped):
        source = image.read_file(file_path)
        formats = {batch_api.load_batch_header(p)['format'] for p in paths}
        for path in paths:
            header = batch_api.load_batch_header(path)
            batch_api.validate_ascii_guard_policy(path,header)
            batch_api.validate_fixed_text_layout_policy(path,header)
            batch_api.validate_fixed_allocation_policy(path,header)
        if formats == {'dk4-arm9-fixed-text-batch-v1'}:
            rebuilt, _ = batch_api.apply_arm9_fixed_batches(paths,source)
        elif formats == {'dk4-pxl-native-label-batch-v1'}:
            if len(paths) != 1:
                raise ValueError('Historical native artwork needs one complete source-locked batch')
            header = batch_api.load_batch_header(paths[0])
            rebuilt, _ = batch_api.apply_pxl_native_label_batch(paths[0],source,image.read_file(header['font_file_path']))
        elif formats == {'dk4-ilnk-translation-batch-v1'}:
            rows, unchanged = [], set()
            for path in paths:
                header = batch_api.load_batch_header(path)
                batch_api.validate_natural_dialogue_qa(path,header,source)
                rows.extend(batch_api.read_translation_batch(path,source))
                unchanged.update(header.get('unchanged_records',[]))
            ids = [r['id'] for r in rows]
            if len(ids) != len(set(ids)):
                raise ValueError('Duplicate historical fixture record')
            expected = {batch_api.parse_pointer_group(r) for r in rows}
            declared = {batch_api.parse_pointer_group(r) for r in rows if r['id'] in unchanged}
            rebuilt = batch_api.rebuild_mesfile(source,rows)
            actual = batch_api.changed_segments(source,rebuilt)
            if actual-expected:
                raise ValueError('Unowned historical fixture segment changed')
            batch_api.validate_unchanged_segments(file_path,expected,actual,declared)
        else:
            raise ValueError(f'Unsupported historical fixture transformation: {formats}')
        image.replace_file(file_path,rebuilt)
    config = recipe['common_native_reblocking']
    if config:
        if digest((ROOT/config).read_bytes()) != document['input_sha256'][config]:
            raise ValueError('Historical native mapper config hash differs')
        common,arm,_ = batch_api.apply_common_reblocking(image.read_file('/COMMON/MESFILE.DK4'),
            image.read_file('/__arm9__.bin'),ROOT/config)
        image.replace_file('/COMMON/MESFILE.DK4',common)
        image.replace_file('/__arm9__.bin',arm)
    return image


def reconstruct(document,recipe):
    raw = bytes(_archived_image(document,recipe).rom.save())
    if digest(raw) != recipe['expected_ROM_sha256']:
        raise ValueError(f"Historical fixture reconstruction does not match its original whole-ROM identity: {digest(raw)} != {recipe['expected_ROM_sha256']}")
    return raw


def materialize(name, cache=CACHE):
    document,recipe = load_recipe(name)
    cache = cache_location(cache)
    path = cache/(recipe['expected_ROM_sha256']+'.romfixture')
    if path.exists():
        if digest(path.read_bytes()) != recipe['expected_ROM_sha256']:
            raise ValueError('Historical fixture cache hash differs; refusing altered bytes')
        return path
    raw = reconstruct(document,recipe)
    cache.mkdir(parents=True,exist_ok=True)
    # Publish complete bytes atomically; another pytest process must never see a
    # partially written fixture or overwrite an existing hash-locked input.
    with tempfile.NamedTemporaryFile(dir=cache,prefix='.historical-fixture-',suffix='.partial',delete=False) as output:
        temporary = Path(output.name)
        output.write(raw)
    try:
        os.link(temporary,path)
    except FileExistsError:
        if digest(path.read_bytes()) != recipe['expected_ROM_sha256']:
            raise ValueError('Concurrent historical fixture cache hash differs')
    finally:
        temporary.unlink()
    receipt = dict(artifact_kind='historical-test-fixture-only',name=name,
        expected_ROM_sha256=recipe['expected_ROM_sha256'],original_manifest=recipe['original_manifest'],
        original_manifest_sha256=recipe['original_manifest_sha256'],recipe_sha256=digest(RECIPES.read_bytes()),
        historical_profile_status=recipe['historical_profile_status'],release_approved=False)
    path.with_suffix('.json').write_text(json.dumps(receipt,indent=2)+'\n')
    return path


def historical_rom(name):
    return materialize(name)
