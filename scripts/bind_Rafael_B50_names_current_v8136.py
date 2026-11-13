"""Bind three known B50 identities/getters/voices to own V8122 without replaying exact B49 cases."""
from copy import deepcopy
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/Rafael_B50_names_current_v8136')
OLD=Path('work/analysis/Rafael_B49_names_v8078/seven_static_speakers14_getters_clean_fields28_synthetic_macro_alignments.json')
MACRO=Path('work/analysis/Rafael_B50_macros_names_v8133/three_clean_FA_FI_paragraphs12_fresh_alignments_six_exact_reused_name_getters.json')
GLOSS=Path('work/analysis/Rafael_B50_clean_gloss_v8131/28_first_clean_glosses_three_source_identities_before_current_English.json')
INPUT=Path('work/analysis/current_V8122_Rafael_native_v8125/current_native_input.json')
START=Path('work/analysis/Rafael_B49_context_binding_v8125/own_Rafael_startup_andstrict_captain0_context.json')
if __name__=='__main__':
    assert not ROOT.exists();old,macro,gloss,inp,start=map(read,[OLD,MACRO,GLOSS,INPUT,START])
    assert macro['current_B50_English_dialogue_body_still_unread'] and gloss['source_only_no_current_B50_English_exposed_no_localized_manuscript']
    current,prior=[NdsImage.open(p) for p in [inp['current_ROM'],old['candidate']]]
    assert sha(Path(inp['current_ROM']).read_bytes())==inp['current_ROM_sha256']==start['candidate_sha256']
    assert sha(Path(old['candidate']).read_bytes())==old['candidate_sha256']==macro['candidate_sha256']
    for path in ['/__arm9__.bin','/COMMON/MESFILE.DK4','/GRP/KANJI.FNT','/data/EV0.DK4']:assert current.read_file(path)==prior.read_file(path)
    assert start['all_whole_RGB_actor_andcaptain_controls_equal'] and start['actual_original_captain_ID']==0
    assert start['actor_captain_controls'][0]==start['actor_captain_controls'][1]
    chosen=[0,2,9];fields=[deepcopy(r) for r in old['complete_clean_andcurrent_name_fields'] if r['actor_ID'] in chosen]
    assert fields==macro['exact_reused_clean_current_fields_andgetters']
    voices=deepcopy(old['native_static_selector_andvoice_resolution']);voices['rows']=[r for r in voices['rows'] if r['source_selector'] in chosen]
    assert len(voices['rows'])==3
    ROOT.mkdir(parents=True);save(ROOT/'three_static_speakers_six_reused_getters_three_reused_voices_exact_V8122_binding.json',dict(
        candidate=inp['current_ROM'],candidate_sha256=inp['current_ROM_sha256'],current_native_input=str(INPUT),current_native_input_sha256=sha(INPUT.read_bytes()),
        source_gloss=str(GLOSS),source_gloss_sha256=sha(GLOSS.read_bytes()),selected_source_static_actors=chosen,
        complete_clean_andcurrent_name_fields=fields,native_static_selector_andvoice_resolution=voices,measured_default_macro_lengths=dict(FI=6,FA=6,FO=10),
        source_name_andmacro_proof=str(MACRO),source_name_andmacro_proof_sha256=sha(MACRO.read_bytes()),
        original_name_andvoice_proof=str(OLD),original_name_andvoice_proof_sha256=sha(OLD.read_bytes()),
        exact_reused_name_getters=6,exact_reused_voice_cases=3,fresh_name_getters=0,fresh_voice_cases=0,
        unchanged_ARM9_COMMON_font_EV0_andwhole_actor_captain_startup_controls_bind_reuse=True,
        source_FA2_FI1_fresh12_alignments_are_in_prior_V8066_not_new_V8122_execution=True,
        not_full_RAM_equivalence_actual_B50_headers_orcatalogue_UI_approval=True,current_English_B50_bodies_still_unread=True,
        startup_binding=str(START),startup_binding_sha256=sha(START.read_bytes()),new_credit=0,new_emulator_runs=0,full_goal_complete=False,
        evidence={str(p):sha(p.read_bytes()) for p in [OLD,MACRO,GLOSS,INPUT,START,Path(__file__)]}))
    print('B50 three identities/six getters/three voices reused under exact V8122 code/font/fields/whole-actor/captain controls;body comparison still pending.')
