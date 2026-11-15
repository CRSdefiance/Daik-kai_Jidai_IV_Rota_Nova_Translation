"""Stage and register the reviewed dialogue-only successor over Rafael4347."""
from copy import deepcopy
import os
from pathlib import Path
import sys

from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha as digest_bytes
from dk4tool.patch.rafael_story_b321_b342_release_v1 import plan_release
from dk4tool.patch.xdelta import apply_xdelta, make_xdelta
from dk4tool.rom.nds import NdsImage
from dk4tool.script.format_safety_relocated_v1 import bind_registered_story_percent_guard
from scripts import build_registered_rafael4347_v1 as previous
from scripts.audit_story_glyph_consistency import load, save
from scripts.finalize_rafael_B321_B342_research_v1 import FINAL, STORED
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.prepare_rafael_B321_B342_registered_v1 import ARCHIVE, ARM, CLEAN, CONFIG, PARENT, QUALIFICATION, REGISTRY
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.verify_release_baseline import REQUIRED_MENU_TEXT, REQUIRED_OPTIONS_TEXT


OUT = Path('work/rafael4903_release_v1')
PROFILE = 'all-routes-rafael4903-dialogue-v1-20261106'
CANDIDATE = OUT / 'all_routes_rafael4903_candidate.nds'
MANIFEST = CANDIDATE.with_suffix('.manifest.json')
PATCH = CANDIDATE.with_suffix('.xdelta')
INVERSE_PATCH = OUT / 'clean_input_reconstruction_RESEARCH_ONLY.nds'
STAGED = OUT / 'staged_successor.json'
RELEASE = OUT / 'registered_release_verification.json'
STARTUP = OUT / 'own_registered_startup_verification.json'
GETTERS = OUT / 'own_registered_name_getters_v1.json'
PARENT_REGISTRY = OUT / 'release_stack_before_Rafael4903.json'
CHECK_SC0 = 'registered_B321_B342_dialogue_and_complete_parent_target_inverse'

stage_source = checked_text(previous.stage_source, {
    """    assert [Path(path) for path in old_manifest['batches'][-2:]] == [
        previous.FINAL, Path(old_profile['owned_Zaganos_surname'])]
    assert old_manifest['checks'][previous.CHECK_SC0] and old_manifest['checks'][previous.CHECK_NAMES]""":
        """    assert Path(old_manifest['batches'][-1]) == previous.FINAL
    assert old_manifest['checks'][previous.CHECK_SC0]
    assert release['owned_Plett_Jacob_surnames_verified'] and release['owned_Zaganos_surname_verified']""",
    "len(old_manifest['batches']) == 696 and len(old_manifest['checks']) == 31":
        "len(old_manifest['batches']) == 697 and len(old_manifest['checks']) == 32",
    "len(dialogue_proof['changed_records']) == 453": "len(dialogue_proof['changed_records']) == 556",
    'Staged Rafael4347.': 'Staged Rafael4903.',
})
register_source = checked_text(previous.register_source, {
    'verified_Rafael3894_output_reused=True': 'verified_Rafael4347_output_reused=True',
    "r['id']) for r in bindings}) == 453": "r['id']) for r in bindings}) == 556",
    'verified_rafael3894_predecessor': 'verified_rafael4347_predecessor',
    'rafael_B301_B320_late_dialogue': 'rafael_B321_B342_late_dialogue',
    'Rafael B301–B320 dialogue.': 'Rafael B321–B342 dialogue.',
    'release_stack.Rafael4347.pending.json': 'release_stack.Rafael4903.pending.json',
    'late_editorial:rafael-b301-b320': 'late_editorial:rafael-b321-b342',
    'Rafael4347_registered_successor_pipeline': 'Rafael4903_registered_successor_pipeline',
    "result['batches'][:696] == old_manifest['batches'] and len(result['batches']) == 697":
        "result['batches'][:697] == old_manifest['batches'] and len(result['batches']) == 698",
    "len(result['checks']) == 32": "len(result['checks']) == 33",
    "'complete_stack_entries': 697, 'registered_manifest_entries': 697, 'passing_release_checks': 32":
        "'complete_stack_entries': 698, 'registered_manifest_entries': 698, 'passing_release_checks': 33",
    "'new_contextual_records': 453, 'prose_revisions': 397": "'new_contextual_records': 556, 'prose_revisions': 364",
    "'justified_retentions': 56": "'justified_retentions': 192",
    'Registered Rafael4347 with 697 entries and 32 release checks.':
        'Registered Rafael4903 with 698 entries and 33 release checks.',
})


if __name__ == '__main__':
    exec(compile(stage_source + '\n' + register_source, __file__ + '::registered-dialogue-successor', 'exec'), globals())
    if sys.argv[1:] == ['--register']:
        register()
    else:
        assert not sys.argv[1:]
        stage()
