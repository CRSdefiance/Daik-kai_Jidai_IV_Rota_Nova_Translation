"""Qualify the dialogue and fixed surname stages over the exact registered ROM."""
import inspect
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha as digest_arm
from dk4tool.patch.owned_name_fields_v2 import plan_arm9_name_fields
from dk4tool.patch.rafael_story_b281_b300_release_v1 import plan_release
from dk4tool.rom.nds import NdsImage
from scripts import finalize_rafael_B281_B300_research_v1 as reviewed
from scripts import prepare_rafael_B261_B280_registered_v1 as previous
from scripts.audit_story_glyph_consistency import load, save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.qualify_rafael_zaganos_name_v1 import CLEAN, OUT as REFERENCE, ROOT
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.write_rafael_B281_B300_contextual_v1 import RELEASE


REGISTRY, ARCHIVE, ARM = previous.REGISTRY, previous.ARCHIVE, previous.ARM
OUT = ROOT / 'registered_preparation_v1'
CONFIG = Path('translations/rafael_B281_B300_editorial_release_v1.json')


source = checked_text(inspect.getsource(previous.main), {
    "release['all_preceding_eight_stages_and_exclusive_field_preserved']":
        "release['all_nine_registered_final_stages_preserved'] and release['owned_Plett_Jacob_surnames_verified']",
    '(692, 27)': '(694, 29)',
    "assert 'owned_Francisca_name_field' in profile and 'ascii_glyph_right_bounds' in profile":
        "assert {'owned_Plett_Jacob_surnames', 'owned_Francisca_name_field', 'ascii_glyph_right_bounds'} <= profile.keys()",
    'record_count=135, speech_count=130, typed_choice_count=5, menu_count=2, style_count=16':
        'record_count=245, speech_count=240, typed_choice_count=5, menu_count=2, style_count=76',
    'scoped_name_count=18, native_pages=131, relative_cases=390, FE_count=17, actual_frames=15761':
        'scoped_name_count=17, native_pages=248, relative_cases=800, FE_count=17, actual_frames=12881',
    'actual_runs=1, actual_speeches=42, actual_body_pages=43, actual_choice_labels=5, offline_speeches=88':
        'actual_runs=1, actual_speeches=27, actual_body_pages=31, actual_choice_labels=5, offline_speeches=213',
    "name_proof_path = REFERENCE/'proof.json'": "name_proof_path = REFERENCE/'qualification.json'",
    "    assert name_proof['all_other_raw_ROM_file_and_component_reserve_pointer_censuses_empty']":
        "    assert name_proof['complete_parent_inverse_exact'] and name_proof['changed_bytes'] == 1",
    'names, name_plan = plan_surnames(': 'names, name_plan = plan_arm9_name_fields(',
    "(REFERENCE/'corrected_ARM9_RESEARCH_ONLY.bin').read_bytes()":
        "Path(load(reviewed.NAME_PROOF)['proposed_ARM9']).read_bytes()",
    "Path('dk4tool/patch/rafael_story_b261_b280_release_v1.py')":
        "Path('dk4tool/patch/rafael_story_b281_b300_release_v1.py')",
    "Path('scripts/qualify_rafael_plett_relocation_v1.py')": "Path('scripts/qualify_rafael_zaganos_name_v1.py')",
    "len(proof['changed_records']) == 135": "len(proof['changed_records']) == 245",
    'dialogue_rebuilt_and_exact_135_stored_bindings_verified': 'dialogue_rebuilt_and_exact_245_stored_bindings_verified',
    'all_nine_prior_stage_dependencies_preserved=True': 'all_predecessor_stage_dependencies_preserved=True',
    'Qualified the exact 135-record and two-surname cumulative successor.':
        'Qualified the exact 245-record and Zaganos surname cumulative successor.',
})


if __name__ == '__main__':
    exec(compile(source, __file__ + '::verified-Rafael3649-dialogue-and-owned-name-fields', 'exec'), globals())
    main()
