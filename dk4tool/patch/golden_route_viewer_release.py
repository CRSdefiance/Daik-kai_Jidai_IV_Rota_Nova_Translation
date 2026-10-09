"""Strict complete Golden Route viewer transformation after V138 captions."""

import json
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.approve_golden_route_viewer_formatting import TARGET_SHA, approve
from scripts.prepare_golden_route_viewer import (
    MANUSCRIPT,
    SOURCE_SHA,
    compile_allocation,
    compile_manuscript,
)

CONFIG = Path('translations/golden_route_viewer_release_v1.json')
EVIDENCE = Path('translations/golden_route_viewer_native_evidence_v1.json')


def apply_release(source, config_path):
    config = json.loads(Path(config_path).read_text(encoding='utf-8'))
    if config.get('format') != 'dk4-golden-route-viewer-release-v1':
        raise ValueError('Unknown complete Golden Route release format')
    if sha(source) != SOURCE_SHA or config['source_arm9_sha256'] != SOURCE_SHA or config['target_arm9_sha256'] != TARGET_SHA:
        raise ValueError('Complete V138 caption source/Golden Route target differs')
    for path in (MANUSCRIPT, EVIDENCE):
        if config['dependencies'].get(path.as_posix()) != sha(path.read_bytes()):
            raise ValueError('Approved Golden Route manuscript/evidence changed')
    document = json.loads(MANUSCRIPT.read_text(encoding='utf-8'))
    evidence = json.loads(EVIDENCE.read_text(encoding='utf-8'))
    if document.get('translation_policy') != 'natural-dialogue-v2' or document.get('target_locale') != 'en-US':
        raise ValueError('Golden Route localization policy is required')
    if any(not all(row['review'][gate] is True for gate in ('source', 'context', 'localization', 'naturalness', 'formatting'))
           for row in document['records']):
        raise ValueError('Every Golden Route editorial/formatting gate is required')
    approve(document, evidence)
    clean, canonical = [NdsImage.open(path).read_file('/__arm9__.bin') for path in (
        'work/clean.nds', 'out/raphael_natural_v2_accepted_base.nds')]
    if sha(clean) != '0d1541022ef95afe02ad7a1a381a1fc3e5e74442a5f0408f436d68a5d306d731' or sha(canonical) != '9a79c25d4a7cf03678a8b5444c3f685a9f675be879109817adb01643141768f5':
        raise ValueError('Clean/canonical Golden Route source ownership differs')
    reviewed = compile_manuscript(clean, canonical, source)
    keys = ('id', 'source_offset', 'source_capacity', 'pointer_field', 'source_hex', 'japanese', 'english')
    if [{key: row[key] for key in keys} for row in document['records']] != [
            {key: row[key] for key in keys} for row in reviewed['records']]:
        raise ValueError('Fresh-source Golden Route prose/consumer review differs')
    proposed, report = compile_allocation(document, source)
    if sha(proposed) != TARGET_SHA:
        raise ValueError('Complete native-reviewed Golden Route target is not reproduced')
    report.update({'format': config['format'], 'source_arm9_sha256': SOURCE_SHA,
                   'target_arm9_sha256': TARGET_SHA, 'message_count': 6,
                   'native_title_pixel_cases': 8, 'native_footer_pixel_cases': 6,
                   'native_modal_pixel_cases': 2, 'runtime_verified': False,
                   'limitations': document['native_formatting_limits']})
    return proposed, report
