"""Bind Yifa's reviewed Taoist-arts terminology to exact clean/current COMMON records."""
from pathlib import Path
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/lil_B170_terms_v4268')
SOURCE=Path('work/analysis/lil_B170_source_v4260/all33_clean_current_complete_context.json')
NAMES=Path('work/analysis/lil_B170_names_v4266/four_original_name_consumers_and_owned_scratch_paths.json')
CONTROL=Path('work/analysis/lil_B170_dispatches_v4263/all33_source_current_dispatches_FI1_FO1_and12_control_leaves.json')
if __name__=='__main__':
    assert not ROOT.exists()
    source,names,control=map(read,[SOURCE,NAMES,CONTROL])
    assert names['source_context_sha256']==control['source_context_sha256']==sha(SOURCE.read_bytes())
    image,clean=NdsImage.open(source['current_ROM']),NdsImage.open('work/clean.nds')
    current,jp=[IlnkContainer.parse(im.read_file('/COMMON/MESFILE.DK4')).blocks for im in [image,clean]]
    bindings=[]
    paths=[Path('translations/activity_special_contextual_final_review_v1.json'),Path('translations/duel_special_contextual_final_review_v1.json')]
    for path in paths:
        row=next(r for r in read(path)['records'] if '道術' in r.get('source_Japanese',''))
        sr,ref=row['source_reference'],row['integrated_reference']
        raw,value=bytes.fromhex(row['source_hex']),bytes.fromhex(row['integrated_hex'])
        assert jp[sr['block']][sr['offset']:sr['offset']+len(raw)]==raw
        assert current[ref['block']][ref['offset']:ref['offset']+len(value)]==value
        assert current[ref['block']][ref['offset']+len(value)]==0
        assert row['speaker']=='Yifa' and all(row['review'].values()) and 'Taoist arts' in row['english']
        bindings.append(dict(final_review=str(path),final_review_sha256=sha(path.read_bytes()),id=row['id'],
            clean_reference=sr,clean_hex=raw.hex(),clean_Japanese=row['source_Japanese'],current_reference=ref,current_hex=value.hex(),
            reviewed_English=row['english'],source_meaning=row['source_meaning'],localization_note=row['localization_note']))
    byindex={r['source_record_index']:r for r in source['records']}
    assert '道術' in byindex[90]['source_Japanese'] and '道術' in byindex[100]['source_Japanese']
    assert '提督' in byindex[61]['source_Japanese']
    assert 'イファ' in byindex[121]['source_Japanese'] and 'イファ' in byindex[125]['source_Japanese']
    assert names['progressive_nameplate_values']==names['full_catalogue_values']=={'2':'Lil Argot','25':'Yifa Sol'}
    assert names['approved_prose_names']=={'2':'Lil','25':'Yifa'}
    ROOT.mkdir(parents=True)
    save(ROOT/'current_Taoist_arts_Yifa_names_and_source_address_reconciliation.json',dict(candidate=source['current_ROM'],candidate_sha256=source['current_ROM_sha256'],
        source_context=str(SOURCE),source_context_sha256=sha(SOURCE.read_bytes()),current_COMMON_sha256=sha(image.read_file('/COMMON/MESFILE.DK4')),
        exact_completed_COMMON_Taoist_arts_bindings=bindings,chosen_Daoist_discipline_term='Taoist arts',
        term_preserves_source_cultural_context_without_inventing_spells_or_religious_bans=True,
        approved_B170_prose_names={'2':'Lil','25':'Yifa'},native_full_names_preserved={'2':'Lil Argot','25':'Yifa Sol'},
        no_Sol_added_to_source_spoken_introduction=True,source_Admiral_claim_only_where_61_explicitly_says_teitoku=True,
        teacher_translation='teacher',teacher_gender_name_school_country_rank_and_degree_not_given=True,
        source_onesan_address_is_familiar_stranger_appeal_not_established_kinship=True,
        source_cheeky_brat_is_Lil_opinion_not_numeric_age_or_narrator_fact=True,
        no_other_route_paralysis_technique_scene_or_Claudio_relationship_imported=True,
        names_proof=str(NAMES),names_proof_sha256=sha(NAMES.read_bytes()),source_FI1_FO1_in_introduction_preserved=True,
        source_event_eligibility_and_later_A000_effect_not_inferred=True,later_older_record0D_reaudit_stays_open=True,
        evidence={str(p):sha(p.read_bytes()) for p in [SOURCE,NAMES,CONTROL,*paths,Path(__file__)]},
        new_emulator_runs=0,source_prose_or_completion_credit_added=0,no_ROM_registry_ledger_change=True,full_goal_complete=False))
    print('Taoist arts bound to two exact completed COMMON records;Yifa names/stranger address/unspecified teacher reconciled. No B170 predecessor English exposed orcredit.')
