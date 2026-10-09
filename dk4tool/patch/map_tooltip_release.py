"""Strict complete map tooltip/creature transformation after V139 viewer labels."""

import json
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.approve_map_tooltip_formatting import TARGET_SHA, approve
from scripts.compile_map_creature_allocation import compile_allocation
from scripts.inventory_map_tooltip_classes import inventory
from scripts.prepare_map_entity_tooltips import SOURCE_SHA, prepare

CONFIG = Path('translations/map_tooltip_release_v1.json')
EVIDENCE = Path('translations/map_tooltip_native_evidence_v1.json')
MANUSCRIPTS = (Path('translations/map_entity_tooltip_manuscript_v2.json'),
               Path('translations/map_creature_class_manuscript_v2.json'))


def apply_release(source, config_path):
    config = json.loads(Path(config_path).read_text(encoding='utf-8'))
    if config.get('format') != 'dk4-map-tooltip-release-v1':
        raise ValueError('Unknown complete map tooltip release format')
    if sha(source) != SOURCE_SHA or config['source_arm9_sha256'] != SOURCE_SHA or config['target_arm9_sha256'] != TARGET_SHA:
        raise ValueError('Complete V139 parent/tooltip target differs')
    for path in (*MANUSCRIPTS, EVIDENCE):
        if config['dependencies'].get(path.as_posix()) != sha(path.read_bytes()):
            raise ValueError('Approved tooltip manuscript/evidence changed')
    documents = [json.loads(path.read_text(encoding='utf-8')) for path in MANUSCRIPTS]
    evidence = json.loads(EVIDENCE.read_text(encoding='utf-8'))
    if any(not all(row['review'][gate] is True for gate in ('source', 'context', 'localization', 'naturalness', 'formatting'))
           for document in documents for row in document['records']):
        raise ValueError('All tooltip editorial/formatting gates are required')
    approve(documents, evidence)
    clean, canonical = [NdsImage.open(path).read_file('/__arm9__.bin') for path in (
        'work/clean.nds', 'out/raphael_natural_v2_accepted_base.nds')]
    if sha(clean) != '0d1541022ef95afe02ad7a1a381a1fc3e5e74442a5f0408f436d68a5d306d731' or sha(canonical) != '9a79c25d4a7cf03678a8b5444c3f685a9f675be879109817adb01643141768f5':
        raise ValueError('Clean/canonical tooltip source ownership differs')
    fresh, _, _ = prepare(clean, canonical, source)
    _, creatures = inventory(clean, source)
    keys = ('id', 'source_offset', 'source_capacity', 'pointer_field', 'source_hex', 'japanese', 'english')
    if [{k: r[k] for k in keys} for d in documents for r in d['records']] != [
            {k: r[k] for k in keys} for r in [*fresh['records'], *creatures]]:
        raise ValueError('Fresh-source tooltip prose/consumer review differs')
    proposed, report = compile_allocation(clean, canonical, source)
    if sha(proposed) != TARGET_SHA:
        raise ValueError('Native-reviewed complete tooltip target is not reproduced')
    report.update({'format': config['format'], 'message_count': 9,
                   'status': 'pass-strict-complete-tooltip-release-experimental-runtime-pending',
                   'runtime_verified': False, 'limitations': documents[0]['native_formatting_limits'],
                   'native_pixel_cases': 312 + 1560 + 156 + 66 + 68,
                   'inherited_golden_pixel_cases': 16, 'inherited_caption_count': 164})
    return proposed, report
