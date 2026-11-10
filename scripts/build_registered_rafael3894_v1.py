"""Build and register the exact Rafael B281–B300 cumulative successor."""
from copy import deepcopy
import inspect
import os
from pathlib import Path
import sys

from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha as digest_bytes
from dk4tool.patch.owned_name_fields_v2 import plan_arm9_name_fields
from dk4tool.patch.rafael_story_b281_b300_release_v1 import plan_release
from dk4tool.patch.xdelta import apply_xdelta, make_xdelta
from dk4tool.rom.nds import NdsImage
from dk4tool.script.format_safety_relocated_v1 import bind_registered_story_percent_guard
from scripts import build_registered_rafael3649_v1 as previous
from scripts.audit_story_glyph_consistency import load, save
from scripts.finalize_rafael_B281_B300_research_v1 import FINAL, NAME_PROOF, STORED
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.prepare_rafael_B281_B300_registered_v1 import ARCHIVE, ARM, CLEAN, CONFIG, OUT as PREPARATION, REGISTRY
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.verify_rafael_B51_B60_registered_release import KEYS
from scripts.verify_release_baseline import REQUIRED_MENU_TEXT, REQUIRED_OPTIONS_TEXT


PARENT = previous.RELEASE
OUT = Path('work/rafael3894_release_v1')
PROFILE = 'all-routes-rafael3894-dialogue-zaganos-v1-20261106'
CANDIDATE = OUT / 'all_routes_rafael3894_candidate.nds'
MANIFEST = CANDIDATE.with_suffix('.manifest.json')
PATCH = CANDIDATE.with_suffix('.xdelta')
INVERSE_PATCH = OUT / 'clean_input_reconstruction_RESEARCH_ONLY.nds'
STAGED = OUT / 'staged_successor.json'
RELEASE = OUT / 'registered_release_verification.json'
STARTUP = OUT / 'own_registered_startup_verification.json'
GETTERS = OUT / 'own_registered_name_getters_v1.json'
PARENT_REGISTRY = OUT / 'release_stack_before_Rafael3894.json'
SURNAME_CONFIG = Path('translations/rafael_B281_B300_zaganos_release_v1.json')
QUALIFICATION = PREPARATION / 'qualification.json'
CHECK_SC0 = 'registered_B281_B300_dialogue_and_complete_parent_target_inverse'
CHECK_NAMES = 'registered_Zaganos_surname_and_complete_parent_target_inverse'


stage_source = checked_text(inspect.getsource(previous.stage), {
    "release['all_preceding_eight_stages_and_exclusive_field_preserved']":
        "release['all_nine_registered_final_stages_preserved'] and release['owned_Plett_Jacob_surnames_verified']",
    "assert [Path(path) for path in old_manifest['batches'][-9:]] == stages":
        """assert [Path(path) for path in old_manifest['batches'][-11:-2]] == stages
    assert [Path(path) for path in old_manifest['batches'][-2:]] == [
        previous.FINAL, Path(old_profile['owned_Plett_Jacob_surnames'])]
    assert old_manifest['checks'][previous.CHECK_SC0] and old_manifest['checks'][previous.CHECK_NAMES]""",
    "len(old_manifest['batches']) == 692 and len(old_manifest['checks']) == 27":
        "len(old_manifest['batches']) == 694 and len(old_manifest['checks']) == 29",
    "len(dialogue_proof['changed_records']) == 135": "len(dialogue_proof['changed_records']) == 245",
    'names, name_proof = plan_surnames(': 'names, name_proof = plan_arm9_name_fields(',
    "assert json.loads(json.dumps(name_proof)) == native_names['name_data_plan']":
        "assert name_proof == native_names['name_data_plan'] and name_proof['changed_bytes'] == 1",
    'both_components_whole_parent_inverse_exact=True, all_nine_registered_final_stages_preserved=True,':
        'both_components_whole_parent_inverse_exact=True, all_predecessor_stage_dependencies_preserved=True,',
    'Staged Rafael3649.': 'Staged Rafael3894.',
})


register_source = checked_text(inspect.getsource(previous.register), {
    "getters['both_name_getters_exact_for_actors_35_65_68_186_203']":
        "getters['both_name_getters_exact_for_actors_35_65_68_70_186_203']",
    'verified_nine_stage_output_reused=True': 'verified_Rafael3649_output_reused=True',
    "r['id']) for r in bindings}) == 135": "r['id']) for r in bindings}) == 245",
    "format='dk4-registered-Plett-Jacob-surname-stage-v1'": "format='dk4-registered-Zaganos-surname-stage-v1'",
    """changed_records=[dict(id='RAFAEL261_280_NAME_65', actor_ID=65, english='Plett Perrault'),
                         dict(id='RAFAEL261_280_NAME_68', actor_ID=68, english='Jacob Portunto')]""":
        """changed_records=[dict(id='RAFAEL281_300_NAME_70', actor_ID=70, english='Zaganos Bey')]""",
    """profile.update(verified_post_nine_stage_predecessor=predecessor, rafael_B261_B280_late_dialogue=str(CONFIG),
                   owned_Plett_Jacob_surnames=str(SURNAME_CONFIG),
                   note='Experimental registered four-route successor with Rafael B261–B280 and two source-owned surnames.')""":
        """profile.update(verified_rafael3649_predecessor=predecessor, rafael_B281_B300_late_dialogue=str(CONFIG),
                   owned_Zaganos_surname=str(SURNAME_CONFIG),
                   note='Experimental cumulative successor with Rafael B281–B300 and the source-owned Zaganos surname.')""",
    'release_stack.Rafael3649.pending.json': 'release_stack.Rafael3894.pending.json',
    "'late_editorial:rafael-b261-b280'": "'late_editorial:rafael-b281-b300'",
    """result['relocations'].setdefault(ARM, {})['owned_Plett_Jacob_surnames'] = staged['surname_proof']""":
        """result['relocations'].setdefault(ARM, {})['owned_Zaganos_surname'] = staged['surname_proof']""",
    'Rafael3649_post_nine_stage_pipeline': 'Rafael3894_registered_successor_pipeline',
    "result['batches'][:692] == old_manifest['batches'] and len(result['batches']) == 694":
        "result['batches'][:694] == old_manifest['batches'] and len(result['batches']) == 696",
    "len(result['checks']) == 29": "len(result['checks']) == 31",
    "'complete_stack_entries': 694, 'registered_manifest_entries': 694, 'passing_release_checks': 29":
        "'complete_stack_entries': 696, 'registered_manifest_entries': 696, 'passing_release_checks': 31",
    "'owned_Francisca_name_field_verified': True, 'owned_Plett_Jacob_surnames_verified': True,":
        "'owned_Francisca_name_field_verified': True, 'owned_Plett_Jacob_surnames_verified': True, "
        "'owned_Zaganos_surname_verified': True, 'all_nine_registered_final_stages_preserved': True,",
    "'new_contextual_records': 135, 'prose_revisions': 118": "'new_contextual_records': 245, 'prose_revisions': 202",
    "'justified_retentions': 17": "'justified_retentions': 43",
    'Registered Rafael3649 with 694 entries and 29 release checks.':
        'Registered Rafael3894 with 696 entries and 31 release checks.',
})


if __name__ == '__main__':
    exec(compile(stage_source + '\n' + register_source, __file__ + '::registered-Rafael3649-successor', 'exec'), globals())
    if sys.argv[1:] == ['--register']:
        register()
    else:
        assert not sys.argv[1:]
        stage()
