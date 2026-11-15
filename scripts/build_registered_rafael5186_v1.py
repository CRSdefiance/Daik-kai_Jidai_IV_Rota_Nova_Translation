"""Registered cumulative successor: residual SC0 dialogue and exclusive middle fields."""
from copy import deepcopy
import os
from pathlib import Path
import sys
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha as digest_bytes
from dk4tool.patch.rafael_story_b0_b34_release_v1 import plan_release
from dk4tool.patch.rafael_middle_fields_release_v1 import plan_release as plan_names
from dk4tool.patch.xdelta import apply_xdelta,make_xdelta
from dk4tool.rom.nds import NdsImage
from dk4tool.script.format_safety_relocated_v1 import bind_registered_story_percent_guard
from scripts import build_registered_rafael4903_v1 as previous
from scripts.audit_story_glyph_consistency import load,save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.prepare_rafael_B0_B34_registered_v1 import ARCHIVE,ARM,CLEAN,CONFIG,PARENT,QUALIFICATION,REGISTRY
from scripts.prepare_rafael_B0_B34_middle_stage_v1 import CONFIG as NAME_CONFIG,QUALIFICATION as NAME_QUALIFICATION
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.verify_release_baseline import REQUIRED_MENU_TEXT,REQUIRED_OPTIONS_TEXT

OUT=Path('work/rafael5186_release_v1')
PROFILE='all-routes-rafael5186-dialogue-middle-fields-v1-20261106'
CANDIDATE=OUT/'all_routes_rafael5186_candidate.nds'
MANIFEST=CANDIDATE.with_suffix('.manifest.json')
PATCH=CANDIDATE.with_suffix('.xdelta')
INVERSE_PATCH=OUT/'clean_input_reconstruction_RESEARCH_ONLY.nds'
STAGED=OUT/'staged_successor.json'
RELEASE=OUT/'registered_release_verification.json'
STARTUP=OUT/'own_registered_startup_verification.json'
GETTERS=OUT/'own_registered_name_getters_v1.json'
PARENT_REGISTRY=OUT/'release_stack_before_Rafael5186.json'
FINAL=Path('translations/rafael_B0_B34_final_review_v1.json')
STORED=Path('work/Rafael_B0_B34_clean_20261106/stored_v1/stored_native_verification.json')
CHECK_SC0='registered_B0_B34_dialogue_and_complete_parent_target_inverse'
CHECK_NAMES='registered_Rafael_residual_middle_fields_and_complete_parent_target_inverse'

stage_source=checked_text(previous.stage_source,{
    "    assert not OUT.exists()":"""    assert not OUT.exists()
    name_qualification=load(NAME_QUALIFICATION)
    assert digest(NAME_CONFIG)==name_qualification['config_sha256']
    assert name_qualification['exact_combined_research_target_and_story_only_inverse']""",
    "len(old_manifest['batches']) == 697 and len(old_manifest['checks']) == 32":
        "len(old_manifest['batches']) == 698 and len(old_manifest['checks']) == 33",
    "len(dialogue_proof['changed_records']) == 556":"len(dialogue_proof['changed_records']) == 283",
    "    output = bytes(proposed.rom.save())\n    proposed.replace_file(ARCHIVE, original_archive)":
        """    assert digest_bytes(bytes(proposed.rom.save()))==qualification['target_ROM_sha256']
    names,name_proof=plan_names(proposed,NAME_CONFIG)
    assert name_proof['changed_bytes']==9 and name_proof['complete_parent_inverse_exact']
    assert name_proof['all_unowned_ARM9_bytes_sections_pointer_tables_andallocations_exact']
    proposed.replace_file(ARM,names)
    output=bytes(proposed.rom.save())
    assert digest_bytes(output)==name_qualification['target_ROM_sha256']
    combined=load('work/Rafael_B0_B34_clean_20261106/rebuilt_with_names_v1/research_reference.json')
    assert digest(combined['research_ROM'])==combined['research_ROM_sha256']==name_qualification['target_ROM_sha256']
    assert output==Path(combined['research_ROM']).read_bytes()
    assert all(proposed.read_file(path)==data for _,path,data in parent.iter_files() if path!=ARCHIVE)
    assert all(proposed.read_file(path)==data for path,data in parent.iter_components() if path!=ARM)
    proposed.replace_file(ARM,original_arm)
    proposed.replace_file(ARCHIVE, original_archive)""",
    "assert digest(CANDIDATE) == qualification['target_ROM_sha256']":
        "assert digest(CANDIDATE) == name_qualification['target_ROM_sha256']",
    "reopened.read_file(ARM) == original_arm":"reopened.read_file(ARM) == names",
    "target_ARM9_sha256=qualification['target_ARM9_sha256']":
        "target_ARM9_sha256=name_qualification['target_ARM9_sha256']",
    "all_other_files_components_graphics_names_andruntime_exact_to_parent=True":
        "all_other_files_components_graphics_names_andruntime_exact_to_parent=False, all_except_owned_middle_fields_exact_to_parent=True, both_components_whole_parent_inverse_exact=True",
    "dialogue_proof=dialogue_proof, new_credit=0":
        "dialogue_proof=dialogue_proof, middle_fields_proof=name_proof, middle_fields_config_sha256=digest(NAME_CONFIG), middle_fields_qualification_sha256=digest(NAME_QUALIFICATION), new_credit=0",
    'Staged Rafael4903.':'Staged Rafael5186.',
})

register_source=checked_text(previous.register_source,{
    "    assert digest(QUALIFICATION) == staged['qualification_sha256']":
        """    assert digest(QUALIFICATION) == staged['qualification_sha256']
    assert digest(NAME_CONFIG)==staged['middle_fields_config_sha256']
    assert digest(NAME_QUALIFICATION)==staged['middle_fields_qualification_sha256']""",
    "getters['both_name_getters_exact_for_actors_35_65_68_70_186_203']":
        "getters['both_name_getters_exact_for_all9_protected_actors']",
    'verified_Rafael4347_output_reused=True':'verified_Rafael4903_output_reused=True',
    "stored['style_records']":"stored.get('style_records', [])",
    "r['id']) for r in bindings}) == 556":"r['id']) for r in bindings}) == 283",
    'verified_rafael4347_predecessor':'verified_rafael4903_predecessor',
    'rafael_B321_B342_late_dialogue':'rafael_B0_B34_late_dialogue',
    "note='Experimental cumulative successor with the full reviewed Rafael B321–B342 dialogue.'":
        "owned_Rafael_residual_middle_fields=str(NAME_CONFIG), note='Experimental cumulative successor with all residual SC0 dialogue and three owned full-name repairs.'",
    'release_stack.Rafael4903.pending.json':'release_stack.Rafael5186.pending.json',
    "result['batches'].append(str(FINAL))":"result['batches'].extend([str(FINAL),str(NAME_CONFIG)])",
    "result['checks'][CHECK_SC0] = True":"""result['checks'][CHECK_SC0] = True
    result['checks'][CHECK_NAMES] = True
    result['changed_records'][ARM].extend(staged['middle_fields_proof']['changed_records'])
    result['relocations'][ARM]['owned_Rafael_residual_middle_fields']=staged['middle_fields_proof']""",
    'late_editorial:rafael-b321-b342':'late_editorial:rafael-b0-b34',
    'Rafael4903_registered_successor_pipeline':'Rafael5186_registered_successor_pipeline',
    "result['batches'][:697] == old_manifest['batches'] and len(result['batches']) == 698":
        "result['batches'][:698] == old_manifest['batches'] and len(result['batches']) == 700",
    "len(result['checks']) == 33":"len(result['checks']) == 35",
    "'complete_stack_entries': 698, 'registered_manifest_entries': 698, 'passing_release_checks': 33":
        "'complete_stack_entries': 700, 'registered_manifest_entries': 700, 'passing_release_checks': 35",
    "'changed_components': [], 'new_contextual_records': 556, 'prose_revisions': 364":
        "'changed_components': [ARM], 'owned_Rafael_residual_middle_fields_verified': True, 'new_contextual_records': 283, 'prose_revisions': 162",
    "'justified_retentions': 192":"'justified_retentions': 121",
    'Registered Rafael4903 with 698 entries and 33 release checks.':
        'Registered Rafael5186 with 700 entries and 35 release checks.',
})

exec(compile(stage_source+'\n'+register_source,__file__+'::qualified-cumulative-successor','exec'),globals())

if __name__=='__main__':
    if sys.argv[1:]==['--register']:register()
    else:
        assert not sys.argv[1:]
        stage()
