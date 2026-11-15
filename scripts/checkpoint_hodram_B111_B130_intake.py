"""Reuse six qualified name bindings across the exact exclusive-name-fields inverse."""
from pathlib import Path
from scripts.registered_editorial_runtime import RegisteredRuntime
from scripts.audit_story_glyph_consistency import load,save
from dk4tool.patch.owned_name_fields_v2 import plan_arm9_name_fields
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage

ROOT=Path('work/analysis/Hodram_B111_B130_clean_20261101')
NEW=Path('work/analysis/Hodram_B91_B110_release_verified_20261101')
OLD=Path('work/analysis/Hodram_B81_B89_release_verified_20261101')
if __name__=='__main__':
    target=ROOT/'native_intake_checkpoint.json';assert not target.exists()
    new=RegisteredRuntime(NEW/'registered_release_verification.json',NEW/'own_registered_startup_verification.json')
    old=RegisteredRuntime(OLD/'registered_release_verification.json',OLD/'own_registered_startup_verification.json')
    assert new.actor_root==old.actor_root and new.actor_bytes==old.actor_bytes and new.common==old.common
    assert new.image.read_file('/GRP/KANJI.FNT')==old.image.read_file('/GRP/KANJI.FNT')
    expected,proof=plan_arm9_name_fields(old.arm,load('work/analysis/Hodram_B91_B110_name_fields_20261101/owned_fields_proposal.json'),NdsImage.open('work/clean.nds').read_file('/__arm9__.bin'))
    assert new.arm==expected
    reuse=ROOT/'known_six_name_proof_reuse.json'
    save(reuse,dict(current_runtime=new.receipt(),previous_runtime=old.receipt(),six_unchanged_actor_IDs=[1,6,14,16,18,139],whole_actual_actor_model_bytes_COMMON_font_exact=True,
        ARM9_except_exclusive_actor20_given_andactor22_middle_fields_exact=proof,known_getters_not_reexecuted=True,
        earlier_four_known_binding_chain='work/analysis/Hodram_B91_B110_clean_20261101/known_name_proof_reuse.json',
        actor139_native='work/analysis/Hodram_B91_B110_new_names_20261101/names.json',
        actor14_qualified_corrected_getters='work/analysis/Emilio_name_glyph_native_20261101/native_name_glyph_verification_reviewed.json',
        no_historical_RAM_overlay_ornew_global_207_name_approval=True,new_credit=0))
    names_path=Path('work/analysis/Hodram_B111_B130_new_names_20261101/names.json');names=load(names_path)
    assert names['runtime']==new.receipt() and len(names['actors'])==18
    current=names['current_names']['rows'];assert [r['text'] for r in current if r['actor_ID']==178]==['Ｆollower']*2
    assert [r['text'] for r in current if r['actor_ID']==43]==['Diogo Escante','Diogo デ Escante']
    checkpoint={**load(ROOT/'intake_scope_checkpoint.json'),'new_names':str(names_path),'known_names':str(reuse),
        'native_roles':str(ROOT/'current_all_six_dynamic_roles.json'),'new_native_actors':18,'clean_getters':36,'current_getters':36,'voice_bindings':18,
        'scoped_name_findings':['Actor178 Follower has a full-width F inboth native consumers;trace its specific storage/provider before a glyph correction.','Actor43 full-catalogue Diogo デ Escante retains a Japanese middle component;sourceディオゴ・デ・エスカンテ supports de without a new rank orbiography.','Sailor151/Retainer151 remain distinct consumers;do not normalize them.','Donna andBenazir are source personal names;Seville/Calicut metadata are not surnames.'],
        'native_static_name_bindings_complete_not_all_preambles_orprose_approved':True,'earlier_English_unconsulted':True,'new_credit':0}
    roles=load(ROOT/'current_all_six_dynamic_roles.json');assert roles['runtime']==new.receipt()
    assert [r['source_selector'] for r in roles['native_roles']['rows']]==[207,208,209,214,215,220]
    save(target,checkpoint)
    ledger_path=Path('translations/editorial_review_current_v1.json');before=ledger_path.read_bytes();ledger=load(ledger_path)
    assert ledger['records_editorially_completed']==8204;(ROOT/'ledger_before_native_intake.json').write_bytes(before)
    ledger['Hodram_B111_B130_clean_next_20261101'].update(checkpoint,native_intake_checkpoint=str(target))
    assert ledger_path.read_bytes()==before;save(ledger_path,ledger)
    print('Next323 source-only meanings retained;18 new native actors,6 exact known-name reuses,six native dynamic roles andtwo scoped glyph/name leads. Earlier English unconsulted;no credit.')
