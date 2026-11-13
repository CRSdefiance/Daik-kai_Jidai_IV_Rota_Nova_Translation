"""Stage and register the dialogue-only successor over the verified Rafael3894 ROM."""
from copy import deepcopy
import os
from pathlib import Path
import sys

from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha as digest_bytes
from dk4tool.patch.rafael_story_b301_b320_release_v1 import plan_release
from dk4tool.patch.xdelta import apply_xdelta, make_xdelta
from dk4tool.rom.nds import NdsImage
from dk4tool.script.format_safety_relocated_v1 import bind_registered_story_percent_guard
from scripts import build_registered_rafael3894_v1 as previous
from scripts.audit_story_glyph_consistency import load, save
from scripts.finalize_rafael_B301_B320_research_v1 import FINAL, STORED
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.prepare_rafael_B301_B320_registered_v1 import ARCHIVE, ARM, CLEAN, CONFIG, PARENT, QUALIFICATION, REGISTRY
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.verify_release_baseline import REQUIRED_MENU_TEXT, REQUIRED_OPTIONS_TEXT


OUT = Path('work/rafael4347_release_v1')
PROFILE = 'all-routes-rafael4347-dialogue-v1-20261106'
CANDIDATE = OUT / 'all_routes_rafael4347_candidate.nds'
MANIFEST = CANDIDATE.with_suffix('.manifest.json')
PATCH = CANDIDATE.with_suffix('.xdelta')
INVERSE_PATCH = OUT / 'clean_input_reconstruction_RESEARCH_ONLY.nds'
STAGED = OUT / 'staged_successor.json'
RELEASE = OUT / 'registered_release_verification.json'
STARTUP = OUT / 'own_registered_startup_verification.json'
GETTERS = OUT / 'own_registered_name_getters_v1.json'
PARENT_REGISTRY = OUT / 'release_stack_before_Rafael4347.json'
CHECK_SC0 = 'registered_B301_B320_dialogue_and_complete_parent_target_inverse'


def between(source, start, end):
    left = source.index(start)
    return source[left:source.index(end, left)]


stage_source = checked_text(previous.stage_source, {
    "release['all_nine_registered_final_stages_preserved'] and release['owned_Plett_Jacob_surnames_verified']":
        "release['all_predecessor_stage_dependencies_preserved'] and release['owned_Zaganos_surname_verified']",
    between(previous.stage_source, "    assert digest(qualification['name_proposal'])", "    old_manifest ="):
        "    assert qualification['only_SC0_changes'] and qualification['complete_parent_inverse_exact']\n",
    between(previous.stage_source, "    stages = ", "    assert all(layer"):
        """    assert [Path(path) for path in old_manifest['batches'][-2:]] == [
        previous.FINAL, Path(old_profile['owned_Zaganos_surname'])]
    assert old_manifest['checks'][previous.CHECK_SC0] and old_manifest['checks'][previous.CHECK_NAMES]
    assert old_manifest['checks']['registered_runtime_bounds_and_complete_parent_target_inverse']
    assert old_profile['ascii_glyph_right_bounds'] == config['right_bound_configuration']
""",
    "len(old_manifest['batches']) == 694 and len(old_manifest['checks']) == 29":
        "len(old_manifest['batches']) == 696 and len(old_manifest['checks']) == 31",
    "len(dialogue_proof['changed_records']) == 245": "len(dialogue_proof['changed_records']) == 453",
    between(previous.stage_source, '    names, name_proof = ', '    final_archive = '):
        """    assert [path for _, path, data in parent.iter_files() if proposed.read_file(path) != data] == [ARCHIVE]
    assert all(proposed.read_file(path) == data for path, data in parent.iter_components())
    assert digest_bytes(original_arm) == qualification['target_ARM9_sha256'] == release['target_ARM9_sha256']
    assert all(text in original_arm for text in REQUIRED_MENU_TEXT) and any(text in original_arm for text in REQUIRED_OPTIONS_TEXT)
""",
    '    proposed.replace_file(ARM, original_arm)\n': '',
    'reopened.read_file(ARM) == names': 'reopened.read_file(ARM) == original_arm',
    'both_components_whole_parent_inverse_exact=True, all_predecessor_stage_dependencies_preserved=True,':
        'whole_parent_inverse_exact=True, all_predecessor_stage_dependencies_preserved=True,\n'
        '        all_other_files_components_graphics_names_andruntime_exact_to_parent=True,',
    'dialogue_proof=dialogue_proof, surname_proof=name_proof, new_credit=0':
        'dialogue_proof=dialogue_proof, new_credit=0',
    'Staged Rafael3894.': 'Staged Rafael4347.',
})


register_source = checked_text(previous.register_source, {
    ' and not SURNAME_CONFIG.exists()': '',
    'verified_Rafael3649_output_reused=True': 'verified_Rafael3894_output_reused=True',
    "r['id']) for r in bindings}) == 245": "r['id']) for r in bindings}) == 453",
    between(previous.register_source, '    save(SURNAME_CONFIG,', "    registry['profiles'][PROFILE]"):
        """    profile.update(verified_rafael3894_predecessor=predecessor, rafael_B301_B320_late_dialogue=str(CONFIG),
                   note='Experimental cumulative successor with the full reviewed Rafael B301–B320 dialogue.')
    assert profile['ascii_glyph_right_bounds'] == registry['profiles'][parent['profile']]['ascii_glyph_right_bounds']
""",
    'release_stack.Rafael3894.pending.json': 'release_stack.Rafael4347.pending.json',
    "result['batches'].extend([str(FINAL), str(SURNAME_CONFIG)])": "result['batches'].append(str(FINAL))",
    """    result['changed_records'].setdefault(ARM, []).extend(load(SURNAME_CONFIG)['changed_records'])
    result['checks'].update({CHECK_SC0: True, CHECK_NAMES: True})""":
        """    result['checks'][CHECK_SC0] = True""",
    "'late_editorial:rafael-b281-b300'": "'late_editorial:rafael-b301-b320'",
    """    result['relocations'].setdefault(ARM, {})['owned_Zaganos_surname'] = staged['surname_proof']
""": "",
    'Rafael3894_registered_successor_pipeline': 'Rafael4347_registered_successor_pipeline',
    "result['batches'][:694] == old_manifest['batches'] and len(result['batches']) == 696":
        "result['batches'][:696] == old_manifest['batches'] and len(result['batches']) == 697",
    "len(result['checks']) == 31": "len(result['checks']) == 32",
    "'complete_stack_entries': 696, 'registered_manifest_entries': 696, 'passing_release_checks': 31":
        "'complete_stack_entries': 697, 'registered_manifest_entries': 697, 'passing_release_checks': 32",
    "'changed_components': [ARM], 'new_contextual_records': 245, 'prose_revisions': 202":
        "'changed_components': [], 'new_contextual_records': 453, 'prose_revisions': 397",
    "'justified_retentions': 43": "'justified_retentions': 56",
    'Registered Rafael3894 with 696 entries and 31 release checks.':
        'Registered Rafael4347 with 697 entries and 32 release checks.',
})


if __name__ == '__main__':
    exec(compile(stage_source + '\n' + register_source, __file__ + '::registered-dialogue-successor', 'exec'), globals())
    if sys.argv[1:] == ['--register']:
        register()
    else:
        assert not sys.argv[1:]
        stage()
