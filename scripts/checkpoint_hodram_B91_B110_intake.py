"""Keep the next211 clean meanings, native-name leads andreusable proofs without credit."""
from pathlib import Path
from scripts.audit_story_glyph_consistency import load,save
from scripts.registered_editorial_runtime import RegisteredRuntime
from dk4tool.patch.owned_name_glyph_v1 import plan_arm9_name_glyph
from dk4tool.patch.grand_race_menu_release import sha

ROOT=Path('work/analysis/Hodram_B91_B110_clean_20261101')
LEDGER=Path('translations/editorial_review_current_v1.json')
NEW=Path('work/analysis/Hodram_B81_B89_release_verified_20261101')
OLD=Path('work/analysis/Hodram_B71_B80_release_verified_20261101')

if __name__=='__main__':
    target=ROOT/'intake_checkpoint.json';assert not target.exists()
    packet,meanings,choice,names,roles=[load(p) for p in [ROOT/'clean_source_packet.json',ROOT/'all209_clean_meanings_before_English.json',
        ROOT/'B91_two_clean_choice_meanings_before_English.json',Path('work/analysis/Hodram_B91_B110_new_names_20261101/names.json'),ROOT/'current_CF_role0_binding.json']]
    assert packet['records']==meanings['meanings']==len(meanings['records'])==209 and choice['labels']==2
    assert all(r['earlier_English_unconsulted'] for r in meanings['records']+choice['records'])
    current=RegisteredRuntime(NEW/'registered_release_verification.json',NEW/'own_registered_startup_verification.json')
    previous=RegisteredRuntime(OLD/'registered_release_verification.json',OLD/'own_registered_startup_verification.json')
    assert current.actor_root==previous.actor_root and current.actor_bytes==previous.actor_bytes
    assert current.common==previous.common
    assert current.image.read_file('/GRP/KANJI.FNT')==previous.image.read_file('/GRP/KANJI.FNT')
    expected,proof=plan_arm9_name_glyph(previous.arm,load('work/analysis/Emilio_name_glyph_20261101/owned_field_proposal.json'))
    assert current.arm==expected
    reuse=dict(current_runtime=current.receipt(),previous_runtime=previous.receipt(),six_known_unchanged_actor_IDs=[1,4,6,12,16,18],
        whole_actual_actor_model_bytes_andCOMMON_andfont_exact=True,
        ARM9_exact_except_source_qualified_exclusive_actor14_name_slot=proof,
        known_getters_reused_without_reexecution=True,
        previous_source_native_bindings=['work/analysis/Hodram_B71_B80_identity_20261101/native_names.json','work/analysis/Hodram_B81_B90_new_names_20261101/names.json'],
        actor14_separate_corrected_getter_andseven_actual_header_proof='work/analysis/Emilio_name_glyph_native_20261101/native_name_glyph_verification_reviewed.json',
        no_historical_RAM_overlay_ornew_global_name_approval=True,new_credit=0)
    reusepath=ROOT/'known_name_proof_reuse.json';save(reusepath,reuse)
    current_names=names['current_names']['rows']
    assert [r['text'] for r in current_names if r['actor_ID']==20]==['Ｆernando Dias']*2
    assert [r['text'] for r in current_names if r['actor_ID']==22]==['Samwell Khan','Samwell ダ Khan']
    assert roles['native_roles']['rows'][0]['resolved_actor_ID']==1
    checkpoint=dict(source_packet=str(ROOT/'clean_source_packet.json'),meanings=str(ROOT/'all209_clean_meanings_before_English.json'),
        choices=str(ROOT/'B91_two_clean_choice_meanings_before_English.json'),clean_name_metadata=str(ROOT/'clean_name_fields.json'),
        item_terms=str(ROOT/'source_bound_item_terminology.json'),new_names='work/analysis/Hodram_B91_B110_new_names_20261101/names.json',
        role0=str(ROOT/'current_CF_role0_binding.json'),known_names=str(reusepath),
        speech_meanings=209,typed_choice_meanings=2,total_prose_objects=211,spoken_blocks=14,control_only_blocks=[94,96,98,99,106,107],
        earlier_English_dialogue_andchoice_labels_unconsulted=True,
        new_native_actor_bindings=8,new_clean_name_getters=16,new_current_name_getters=16,new_voice_bindings=8,
        dynamic_CF_role0_bound_to_actual_startup_captain1_not_actor207=True,
        dynamic_binding_not_actual_future_scene_role_assignment=True,
        findings=[
            'Fernando retains the correct name butboth current native getters have an unintended full-width F. Owned-field proposal,normal-font checks andrepresentative gameplay are pending.',
            'Samwell Khan progressive caption is ASCII;full catalogue stillcontains the Japanese middle componentダ. Verify approved Latin particle andshared ownership before any change;full catalogue UI remains unvisited.',
            'Sailor152 andRetainer152 are distinct source consumer outputs,not inconsistent translations of one field. Trader/Priest/Port Worker role labels preserve source jobs without father/brother relationships orregion surnames.',
            'B95 names a generic Katzbalger sword type,not the full named Sweeping Katzbalger. Other item clues are bound to exact clean catalogue entries andexisting titles.',
            'B91 has a24-byte belief menu andfour conditional stat notices;preserve both source indices,one-point values anddistinct Luck/Spirit terminology. Native branch/notice context qualification remains.',
            'Seven new FE bodies include two FI macros andthree anonymous monkey screeches. Retain sourceFE controls;qualify macro-bearing FE behavior before formatting approval.'],
        current_English_contextual_editorial_native_formatting_stored_gameplay_andrelease_pending=True,
        no_new_ROM_orcompletion_credit=True,new_credit=0,full_goal_complete=False)
    save(target,checkpoint)
    before=LEDGER.read_bytes();ledger=load(LEDGER);assert ledger['records_editorially_completed']==7993
    backup=ROOT/'ledger_before_intake_checkpoint.json';assert not backup.exists();backup.write_bytes(before)
    ledger['Hodram_B91_B110_clean_next_20261101'].update(checkpoint)
    assert LEDGER.read_bytes()==before;save(LEDGER,ledger)
    print('Next211 clean meanings retained;8 new actor bindings,6 exact known-name reuses,CF role0/current captain1 andtwo concrete name-glyph leads. Earlier English still unconsulted;no credit.')
