"""Strict post-COMMON transformation for all 164 complete scene captions."""

import json
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.approve_scene_caption_formatting import approve
from scripts.compile_scene_caption_allocation import compile_allocation
from scripts.compile_scene_caption_single_dispatch import compile_scoped_dispatch
from scripts.compile_scene_caption_tracking import compile_tracking
from scripts.probe_scene_caption_wrappers import validate_callers

SOURCE_SHA = '13f89291781011e0835acc025870a0c748299075ea45e713c96bdc9676aae9ab'
TARGET_SHA = '004aef018e9731fc5ab202ac40cfffe70e2cdc2060e44e7d7ea64946128c7b83'
MANUSCRIPT = Path('translations/scene_caption_manuscript_v2.json')
EVIDENCE = Path('translations/scene_caption_native_formatting_evidence_v1.json')
CONFIG = Path('translations/scene_caption_release_v1.json')


def compile_release(source, document, evidence):
    if sha(source) != SOURCE_SHA:
        raise ValueError('Scene captions require the complete V137 post-COMMON ARM9')
    if document.get('translation_policy') != 'natural-dialogue-v2' or document.get('target_locale') != 'en-US':
        raise ValueError('Native caption localization policy is required')
    if any(not all(row['review'][gate] is True for gate in
                   ('source', 'context', 'localization', 'naturalness', 'formatting')) for row in document['records']):
        raise ValueError('All native caption editorial/formatting gates are required')
    raster, wrappers = evidence['raster'], evidence['wrappers']
    if wrappers['proposed_arm9_sha256'] != TARGET_SHA or raster['proposed_arm9_sha256'] != TARGET_SHA:
        raise ValueError('Native caption evidence does not cover the strict target')
    if document['source_reviewed_manuscript_sha256'] != wrappers['manuscript_sha256']:
        raise ValueError('Native caption source manuscript lineage differs')
    approve(document, raster, wrappers)
    clean, canonical = [NdsImage.open(path).read_file('/__arm9__.bin') for path in (
        'work/clean.nds', 'out/raphael_natural_v2_accepted_base.nds')]
    if sha(clean) != document['source_arm9_sha256'] or sha(canonical) != '9a79c25d4a7cf03678a8b5444c3f685a9f675be879109817adb01643141768f5':
        raise ValueError('Caption clean/canonical source ownership differs')
    allocated, allocation = compile_allocation(document, clean, canonical, source)
    tracked, tracking = compile_tracking(allocated, document)
    proposed = compile_scoped_dispatch(tracked)
    callers = validate_callers(proposed)
    if sha(proposed) != TARGET_SHA:
        raise ValueError('Complete native-reviewed caption target is not reproduced')
    report = {'format': 'dk4-scene-caption-release-v1', 'caption_count': 164,
              'source_arm9_sha256': SOURCE_SHA, 'target_arm9_sha256': TARGET_SHA,
              'native_wrapper_callers': callers, 'max_width_pixels': tracking['max_width'],
              'owned_ranges': allocation['owned_ranges'], 'unused_ranges': allocation['unused_ranges'],
              'all_existing_waiting_widget_semantics_preserved': True,
              'native_pixel_cases': 328, 'native_class_compatibility_cases': 88,
              'native_wrapper_compatibility_cases': 20, 'runtime_verified': False,
              'limitations': wrappers['limitations']}
    return proposed, report


def apply_release(source, config_path):
    config = json.loads(Path(config_path).read_text(encoding='utf-8'))
    if config.get('format') != 'dk4-scene-caption-release-v1':
        raise ValueError('Unknown complete caption release format')
    if config['source_arm9_sha256'] != SOURCE_SHA or config['target_arm9_sha256'] != TARGET_SHA:
        raise ValueError('Caption release source/target pin differs')
    for path in (MANUSCRIPT, EVIDENCE):
        if config['dependencies'].get(path.as_posix()) != sha(path.read_bytes()):
            raise ValueError('Caption approved manuscript/native evidence changed')
    return compile_release(source, json.loads(MANUSCRIPT.read_text(encoding='utf-8')),
                           json.loads(EVIDENCE.read_text(encoding='utf-8')))
