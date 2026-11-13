"""Bind dialogue identities to clean Japanese inline names;preserve distinct pooled catalog label."""
from pathlib import Path
from ndspy.code import MainCodeFile
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.main_pool_cache_visibility import POOL
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/lil_B179_role_identity_v4715')
SOURCE=Path('work/analysis/lil_B179_source_v4708/all14_clean_current_complete_context.json')
NAMES=Path('work/analysis/lil_B179_names_v4713b/six_original_Barkeep_Patron_Retainer_name_consumers.json')

if __name__=='__main__':
    assert not ROOT.exists()
    source,names=read(SOURCE),read(NAMES)
    assert names['source_context_sha256']==sha(SOURCE.read_bytes())
    clean=NdsImage.open('work/clean.nds').read_file('/__arm9__.bin');arm=NdsImage.open(source['current_ROM']).read_file('/__arm9__.bin')
    assert sha(arm)==source['current_ARM9_sha256']==names['ARM9_sha256']
    assert clean[0x7ED88:0x7EDD4]==arm[0x7ED88:0x7EDD4]
    cases=names['native_six_consumer_cases']['rows'];assert len(cases)==6
    expected={92:(0x15D2A4,'酒場の親父','Barkeep'),96:(0x15C5E4,'酒場の客','Patron'),152:(0x1484D4,'水夫','Sailor')}
    bindings=[]
    for actor,(at,jp,en) in expected.items():
        row=next(r for r in cases if r['actor_ID']==actor and r['consumer']=='progressive-nameplate')
        assert row['pointer']==0x02000000+at and row['text']==en
        a=clean[at:clean.index(0,at)+1];b=arm[at:arm.index(0,at)+1]
        assert a==jp.encode('cp932')+b'\0' and b==en.encode('ascii')+b'\0'
        assert row['ownership_mode']=='original-read-only-name-pointer-without-scratch-ring' and not row['original_getter_writes']
        bindings.append(dict(actor_ID=actor,consumer='progressive-nameplate',native_getter=row['getter'],pointer=row['pointer'],file_offset=at,
            clean_Japanese=jp,current_English=en,source_complete_terminated_hex=a.hex(),current_complete_terminated_hex=b.hex(),
            source_code_exact_and_native_current_pointer_binds_both_inline_spans=True))
    catalog=next(r for r in cases if r['actor_ID']==152 and r['consumer']=='full-catalogue')
    assert catalog['text']=='Retainer' and catalog['pointer']==0x02387E48
    payload=bytes(MainCodeFile(arm,0x02000000).sections[3].data[:-48]);assert len(payload)==123040
    at=catalog['pointer']-POOL;assert 0<=at<len(payload) and payload[at:at+9]==b'Retainer\0'
    assert names['progressive_nameplate_values']=={'92':'Barkeep','96':'Patron','152':'Sailor'}
    ROOT.mkdir(parents=True)
    save(ROOT/'source_current_progressive_roles_and_distinct_Retainer_catalogue_binding.json',dict(
        candidate=source['current_ROM'],candidate_sha256=source['current_ROM_sha256'],source_context=str(SOURCE),source_context_sha256=sha(SOURCE.read_bytes()),
        native_name_proof=str(NAMES),native_name_proof_sha256=sha(NAMES.read_bytes()),progressive_role_source_current_bindings=bindings,
        approved_dialogue_roles={'92':'Barkeep','96':'Patron','152':'Sailor'},full_catalogue_roles=names['full_catalogue_values'],
        separate_catalogue152_pointer=catalog['pointer'],separate_catalogue152_name='Retainer',staged_pool_base=POOL,
        separate_catalogue152_payload_offset=at,staged_payload_bytes=123040,
        exact_progressive_source_Sailor_Japanese_suifu_not_inferred_from_catalogue_Retainer=True,
        catalogue_getter_is_distinct_and_does_not_override_dialogue_identity=True,
        Master_tavern_address_may_use_bound_Barkeep_without_invented_superior_relationship=True,
        no_named_lord_faction_military_rank_kinship_or_spoken_title_invented=True,no_name_asset_or_code_change=True,
        city_wine_terms_complete_prose_comparison_native_display_actual_and_release_still_pending=True,
        not_actual_B179_gameplay_or_nameplate_observation=True,no_ROM_registry_ledger_orcredit_change=True,new_emulator_runs=0,
        evidence={str(p):sha(p.read_bytes()) for p in [SOURCE,NAMES,Path(__file__)]},full_goal_complete=False))
    print('Clean inline identities bind Barkeep/Patron/Sailor;source水夫/currentSailor at1484D4. Separate pooled catalog Retainer152 preserved. No assets or credit changed.')
