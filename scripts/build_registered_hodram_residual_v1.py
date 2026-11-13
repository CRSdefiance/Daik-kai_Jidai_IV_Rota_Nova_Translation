"""Stage/register the cumulative residual SC1 andthree owned surnames; preserve the full prefix."""
from pathlib import Path
import sys
from scripts import build_registered_hodram_B311_B324_v1 as previous
from scripts.prepare_hodram_residual_registered_v2 import ARCHIVE,ARM,CLEAN,CONFIG,PARENT,QUALIFICATION,REGISTRY,FINAL,ROOT
from scripts.prepare_hodram_residual_surnames_v1 import CONFIG as NAME_CONFIG,QUALIFICATION as NAME_QUALIFICATION
from dk4tool.patch.hodram_residual_release_v2 import plan_release
from dk4tool.patch.registered_owned_name_fields_v2 import plan_release as plan_names
from scripts.source_locked_derivation_v5118 import checked_text

STORED=ROOT/'stored_v2/stored_native_verification.json'
OUT=Path('work/hodram_residual_release_v1')
PROFILE='all-routes-hodram-residual-dialogue-names-v1-20261109'
CANDIDATE=OUT/'all_routes_hodram_residual_candidate.nds'
MANIFEST=CANDIDATE.with_suffix('.manifest.json');PATCH=CANDIDATE.with_suffix('.xdelta')
INVERSE_PATCH=OUT/'clean_input_reconstruction_RESEARCH_ONLY.nds'
STAGED=OUT/'staged_successor.json';RELEASE=OUT/'registered_release_verification.json'
STARTUP=OUT/'own_registered_startup_verification.json';GETTERS=OUT/'own_registered_name_getters_v1.json'
PARENT_REGISTRY=OUT/'release_stack_before_Hodram_residual.json'
CHECK_SC1='registered_Hodram_residual_dialogue_and_complete_parent_target_inverse'
CHECK_NAMES='registered_Hodram_residual_surnames_and_complete_parent_target_inverse'
NEGATIVES=ROOT/'registered_semantic_checks_v1/qualification.json'

stage_source=checked_text(previous.stage_source,{
    "    assert load(NEGATIVES)['all8_production_scope_mutations_rejected']":
        "    assert load(NEGATIVES)['all8_production_scope_mutations_rejected'] and load(NEGATIVES)['all6_registered_surname_policy_mutations_rejected']\n    name_qualification=load(NAME_QUALIFICATION)",
    "len(old_manifest['batches']) == 705 and len(old_manifest['checks']) == 40":
        "len(old_manifest['batches']) == 706 and len(old_manifest['checks']) == 41",
    "len(dialogue_proof['changed_records']) == 400":"len(dialogue_proof['changed_records']) == 394",
    "    output = bytes(proposed.rom.save())\n    proposed.replace_file(ARCHIVE, original_archive)":
        """    assert digest_bytes(bytes(proposed.rom.save()))==qualification['target_ROM_sha256']
    names,name_proof=plan_names(proposed,NAME_CONFIG)
    assert name_proof['changed_bytes']==28 and name_proof['complete_parent_inverse_exact']
    assert name_proof['all_unowned_ARM9_bytes_sections_pointer_tables_andallocations_exact']
    proposed.replace_file(ARM,names)
    output=bytes(proposed.rom.save())
    assert digest_bytes(output)==name_qualification['target_ROM_sha256']
    mixed=load(ROOT/'mixed_research_v2/research_reference.json')
    assert digest(mixed['research_ROM'])==mixed['research_ROM_sha256']==name_qualification['target_ROM_sha256']
    assert output==Path(mixed['research_ROM']).read_bytes()
    assert all(proposed.read_file(path)==data for _,path,data in parent.iter_files() if path!=ARCHIVE)
    assert all(proposed.read_file(path)==data for path,data in parent.iter_components() if path!=ARM)
    proposed.replace_file(ARM,original_arm)
    proposed.replace_file(ARCHIVE, original_archive)""",
    "assert digest(CANDIDATE) == qualification['target_ROM_sha256']":"assert digest(CANDIDATE) == name_qualification['target_ROM_sha256']",
    "reopened.read_file(ARM) == original_arm":"reopened.read_file(ARM) == names",
    "target_ARM9_sha256=qualification['target_ARM9_sha256']":"target_ARM9_sha256=name_qualification['target_ARM9_sha256']",
    'all_other_files_components_graphics_names_andruntime_exact_to_parent=True,':
        'all_other_files_components_graphics_names_andruntime_exact_to_parent=False,all_except_SC1_andthree_owned_surnames_exact_to_parent=True,both_components_whole_parent_inverse_exact=True,',
    'dialogue_proof=dialogue_proof, new_credit=0':
        'dialogue_proof=dialogue_proof,surname_fields_proof=name_proof,surname_fields_config_sha256=digest(NAME_CONFIG),surname_fields_qualification_sha256=digest(NAME_QUALIFICATION),new_credit=0',
    'Staged Hodram B311-B324.':'Staged Hodram residual dialogue andsurnames.',
})
register_source=checked_text(previous.register_source,{
    "    assert digest(QUALIFICATION) == staged['qualification_sha256']":
        "    assert digest(QUALIFICATION) == staged['qualification_sha256']\n    assert digest(NAME_CONFIG)==staged['surname_fields_config_sha256']\n    assert digest(NAME_QUALIFICATION)==staged['surname_fields_qualification_sha256']",
    "getters['both_name_getters_exact_for_all9_protected_actors']":"getters['both_name_getters_exact_for_all12_protected_actors']",
    'verified_Hodram_B301_B310_output_reused=True':'verified_Hodram_B311_B324_output_reused=True',
    "r['id']) for r in bindings}) == 400":"r['id']) for r in bindings}) == 394",
    'verified_hodram_b301_b310_predecessor':'verified_hodram_b311_b324_predecessor',
    'hodram_B311_B324_late_dialogue':'hodram_residual_late_dialogue',
    "note='Experimental cumulative successor with the full reviewed Hodram B311–B324 dialogue.'":
        "owned_Hodram_residual_surnames=str(NAME_CONFIG),note='Experimental cumulative successor with all residual reviewed SC1 dialogue andthree source-bound surname repairs.'",
    'release_stack.Hodram_B311_B324.pending.json':'release_stack.Hodram_residual.pending.json',
    "result['batches'].append(str(FINAL))":"result['batches'].extend([str(FINAL),str(NAME_CONFIG)])",
    "    result['checks'][CHECK_SC1] = True":
        "    result['checks'][CHECK_SC1] = True\n    result['checks'][CHECK_NAMES]=True\n    result['changed_records'][ARM].extend(staged['surname_fields_proof']['changed_records'])\n    result['relocations'][ARM]['owned_Hodram_residual_surnames']=staged['surname_fields_proof']",
    'late_editorial:hodram-b311-b324':'late_editorial:hodram-residual',
    'Hodram_B311_B324_registered_successor_pipeline':'Hodram_residual_registered_successor_pipeline',
    "result['batches'][:705] == old_manifest['batches'] and len(result['batches']) == 706":
        "result['batches'][:706] == old_manifest['batches'] and len(result['batches']) == 708",
    "len(result['checks']) == 41":"len(result['checks']) == 43",
    "'complete_stack_entries': 706, 'registered_manifest_entries': 706, 'passing_release_checks': 41":
        "'complete_stack_entries': 708, 'registered_manifest_entries': 708, 'passing_release_checks': 43",
    "'changed_components': [], 'owned_Rafael_residual_middle_fields_verified': True, 'new_contextual_records': 400, 'prose_revisions': 175":
        "'changed_components': [ARM], 'owned_Hodram_residual_surnames_verified':True,'owned_Rafael_residual_middle_fields_verified': True, 'new_contextual_records': 394, 'prose_revisions': 221",
    "'justified_retentions': 225":"'justified_retentions': 173",
    'Registered Hodram B311-B324 with706 entries and41 release checks.':
        'Registered Hodram residual dialogue/surnames with708 entries and43 release checks.',
})
env={**previous.env,**vars(previous),**globals(),'previous':previous,'__file__':__file__}
exec(compile(stage_source+'\n'+register_source,__file__+'::same-cumulative-successor-contract-two-qualified-transactions','exec'),env)
if __name__=='__main__':
    if sys.argv[1:]==['--register']:env['register']()
    else:assert not sys.argv[1:];env['stage']()
