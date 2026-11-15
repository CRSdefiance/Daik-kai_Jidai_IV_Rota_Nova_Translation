"""Bind B175 identities and admiral terminology without naming its woman or sword."""
from pathlib import Path
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/lil_B175_terms_v4510')
SOURCE=Path('work/analysis/lil_B175_source_v4503/all32_clean_current_complete_context.json')
NAMES=Path('work/analysis/lil_B175_names_v4508/ten_original_name_consumers_owned_and_readonly_paths.json')
CONTROL=Path('work/analysis/lil_B175_controls_v4509/one_resource_three_presentations_C200_two_ends_and7_source_leaves.json')
ROLE=Path('translations/lil_B165_contextual_final_review_v1.json')
POLICY=Path('translations/character_name_localization_policy_v1.json')
GLOSSARY=Path('docs/glossary.md')

if __name__=='__main__':
    assert not ROOT.exists()
    source,names,control,role=map(read,[SOURCE,NAMES,CONTROL,ROLE])
    assert names['source_context_sha256']==control['source_context_sha256']==sha(SOURCE.read_bytes())
    current,clean=NdsImage.open(source['current_ROM']),NdsImage.open('work/clean.nds')
    now,jp=[IlnkContainer.parse(im.read_file('/data/SC2.DK4')).blocks for im in [current,clean]]
    bindings=[]
    for index in [86,104]:
        row=next(r for r in role['records'] if r['block']==165 and r['source_record_index']==index)
        sr,ref=row['source_reference'],row['integrated_reference'];raw,value=bytes.fromhex(row['source_hex']),bytes.fromhex(row['integrated_hex'])
        assert '提督' in row['source_Japanese'] and 'admiral' in row['english'].casefold() and all(row['review'].values())
        assert jp[165][sr['offset']:sr['offset']+len(raw)]==raw and jp[165][sr['offset']+len(raw)]==0
        assert now[165][ref['offset']:ref['offset']+len(value)]==value and now[165][ref['offset']+len(value)]==0
        bindings.append(dict(id=row['id'],source_reference=sr,source_hex=raw.hex(),source_Japanese=row['source_Japanese'],
            integrated_reference=ref,current_hex=value.hex(),reviewed_English=row['english'],final_review=str(ROLE),final_review_sha256=sha(ROLE.read_bytes())))
    assert names['approved_prose_names']=={'2':'Lil','9':'Camille','183':'Angel','184':'Snake','185':'Dandy'}
    assert names['progressive_nameplate_values']=={'2':'Lil Argot','9':'Camille Overijssel','183':'Angel','184':'Snake','185':'Dandy'}
    assert names['full_catalogue_values']['9']=='Camille Marinus Overijssel'
    by={r['source_record_index']:r for r in source['records']}
    for index,phrases in {18:['女海賊'],24:['お嬢ちゃんたち','２人きり','無傷'],28:['囲まれてる','FI'],
        32:['卑怯'],55:['チンピラ','海賊としての誇り'],63:['殺すつもり','海の上','逃げる'],
        69:['度胸','名前'],73:['FI','FA'],77:['かわいい提督','ん！？'],84:['いい剣','釣り合わない','そのうち'],
        92:['分からなきゃ','引き上げ'],105:['FI','怖い'],109:['一言多く','カッコイイ'],113:['追い回される'],120:['負けん気']}.items():
        assert all(p in by[index]['source_Japanese'] for p in phrases),index
    assert by[77]['kind']==by[84]['kind']=='system-FE' and by[73]['source_selector']==2
    assert source['source_macro_counts']=={'FI':4,'FA':1,'FO':0}
    policy=read(POLICY);assert any(r.get('localized_first_name')=='Camille' for r in policy['confirmed_decisions'])
    ROOT.mkdir(parents=True)
    save(ROOT/'current_five_names_anonymous_woman_unidentified_sword_and_admiral_reconciliation.json',dict(
        candidate=source['current_ROM'],candidate_sha256=source['current_ROM_sha256'],source_context=str(SOURCE),source_context_sha256=sha(SOURCE.read_bytes()),
        approved_B175_prose_names=names['approved_prose_names'],native_nameplates_preserved=names['progressive_nameplate_values'],
        original_full_Camille_name_not_added_to_familiar_source_addresses=True,
        exact_completed_Lil_admiral_role_bindings=bindings,chosen_source_提督_English='admiral',
        source_role_is_explicit_and_previously_used_for_Lil_no_new_commission_navy_or_rank_added=True,
        FE_woman_identified_only_as_woman_pirate_from_prior_encounter_not_named_from_later_story=True,
        sword_remains_unnamed_unappraised_no_power_size_price_or_completed_theft_invented=True,
        source_threat_to_kill_here_is_denied_intention_and_sea_challenge_is_future=True,
        woman_pride_rebuke_and_Lil_reassessment_not_alliance_or_recruitment=True,
        source_diminutive_group_address_can_address_Lil_and_associate_without_calling_Camille_female=True,
        no_boss_or_Captain_address_added_to_crew_responses=True,
        source_FI4_FA1_runtime_name_order_and_null_actor_FE_controls_preserved=True,
        companion_future_pursuit_warning_not_earned_game_flag_or_already_observed_attack=True,
        source_4696_CA80_and4635_7D80_presentation_operands_not_guessed_as_actor_identity=True,
        broad_SourceItems_LocalProduct_graphics_and_later_older_record_reaudit_stay_open=True,
        evidence={str(p):sha(p.read_bytes()) for p in [SOURCE,NAMES,CONTROL,ROLE,POLICY,GLOSSARY,Path(__file__)]},
        new_emulator_runs=0,source_prose_or_completion_credit_added=0,no_ROM_registry_ledger_change=True,full_goal_complete=False))
    print('Bound Lil/Camille/Angel/Snake/Dandy and exact earlier Lil admiral references. Woman and sword stay unnamed;FI4/FA1 preserved. No credit.')
