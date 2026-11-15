"""Bind clean couple roles, household tea and the prospective Sofala notice."""
from pathlib import Path
import inspect,struct
from ndspy.code import MainCodeFile
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.main_pool_cache_visibility import POOL
from dk4tool.patch.grand_race_menu_release import sha
from scripts.current_build_native_context_v4774 import CurrentContext
from scripts.reconcile_lil_B183_terms_v4931 import bindings
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/lil_B184_terms_v5045')
SOURCE=Path('work/analysis/lil_B184_source_v5039/all9_clean_current_complete_context.json')
NAMES=Path('work/analysis/lil_B184_names_v5044/four_original_progressive_and_catalogue_name_consumers.json')
CONTROL=Path('work/analysis/lil_B184_controls_v5043/A000_C200_single_end_and_no_relative_or_predicate_contract.json')
ROLES={'164':'Man in a Couple','165':'Woman in a Couple'}

if __name__=='__main__':
    assert not ROOT.exists()
    packet,names,control=map(read,[SOURCE,NAMES,CONTROL])
    assert names['source_context_sha256']==control['source_context_sha256']==sha(SOURCE.read_bytes())
    assert names['progressive_nameplate_values']==names['full_catalogue_values']==ROLES
    clean=NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    arm=NdsImage.open(packet['current_ROM']).read_file('/__arm9__.bin')
    assert sha(arm)==packet['current_ARM9_sha256']
    assert clean[0x7ED88:0x7EE20]==arm[0x7ED88:0x7EE20]
    payload=bytes(MainCodeFile(arm,0x02000000).sections[3].data[:-48])
    assert len(payload)==123040
    ordinary_path=Path('translations/ordinary_name_fidelity_manuscript_v1.json')
    ordinary=read(ordinary_path)
    roles=[]
    for ident,jp in [(164,'カップル男'),(165,'カップル女')]:
        record=next(r for r in ordinary['records'] if r['index']==ident)
        field=record['table_field']
        source_ptr=struct.unpack_from('<I',clean,field)[0]
        current_ptr=struct.unpack_from('<I',arm,field)[0]
        source_at=source_ptr-0x02000000
        source_bytes=clean[source_at:clean.index(0,source_at)+1]
        assert source_bytes==jp.encode('cp932')+b'\0'
        assert source_ptr==record['clean_pointer'] and record['japanese']==jp
        assert record['english']==ROLES[str(ident)] and current_ptr==record['after_pointer']
        at=current_ptr-POOL
        current_bytes=ROLES[str(ident)].encode('ascii')+b'\0'
        assert payload[at:at+len(current_bytes)]==current_bytes
        cases=[r for r in names['native_four_consumer_cases']['rows'] if r['actor_ID']==ident]
        assert len(cases)==2 and all(r['pointer']==current_ptr and r['text']==ROLES[str(ident)] and
            not r['original_scratch_rings'] and not r['original_getter_writes'] for r in cases)
        roles.append(dict(actor_ID=ident,clean_Japanese=jp,approved_English=ROLES[str(ident)],
            source_pointer=source_ptr,source_storage_offset=source_at,source_terminated_hex=source_bytes.hex(),
            current_pointer=current_ptr,current_pool_offset=at,current_terminated_hex=current_bytes.hex(),
            table_field=field,both_native_name_consumers_bind_exact_live_pointer=True))
    goods=read('translations/commodity_name_manuscript_v343.json')
    good=next(r for r in goods['records'] if r['index']==31)
    fidelity=next(r for r in read('translations/commodity_fidelity_v2.json')['records'] if r['index']==31)
    assert good['Japanese']==fidelity['Japanese']=='茶' and good['English']==fidelity['English']=='Tea'
    cities=[]
    for field,at in [(0x122404,0x15C758),(0x1234C8,0x15C278)]:
        ptr=struct.unpack_from('<I',clean,field)[0]
        assert ptr==0x02000000+at
        value=clean[at:clean.index(0,at)+1]
        assert value=='ソファラ'.encode('cp932')+b'\0'
        cities.append(dict(pointer_field=field,source_pointer=ptr,source_storage_offset=at,
            source_terminated_hex=value.hex(),source_text='ソファラ',approved_English='Sofala'))
    field=good['pointer_field'];ptr=struct.unpack_from('<I',clean,field)[0];at=ptr-0x02000000
    assert clean[at:clean.index(0,at)].decode('cp932')=='茶'
    assert clean[field+4:field+12]==arm[field+4:field+12]==bytes.fromhex(good['metadata_hex'])
    fields=[r['pointer_field'] for r in cities]+[good['pointer_field']]+[r['table_field'] for r in roles]
    ROOT.mkdir(parents=True)
    ctx=CurrentContext('work/analysis/lil_B184_voices_v5040/current_native_input.json',packet['historical_snapshot_ROM'],ROOT/'current_context')
    live=ctx.execute(bindings,fields);ctx.machines.pop();assert not ctx.machines
    assert [r['text'] for r in live['rows']]==['Sofala','Sofala','Tea','Man in a Couple','Woman in a Couple']
    for a,b in zip(cities,live['rows'][:2],strict=True):a.update(b)
    by={r['source_record_index']:r for r in packet['records']}
    assert set(by)=={6,10,14,18,22,26,30,33,36}
    assert all(s in by[22]['source_Japanese'] for s in ['うちのお茶','残り少ない','明日','買ってきて'])
    assert all(s in by[36]['source_Japanese'] for s in ['ソファラ','茶','流行しそう'])
    assert all('ソファラ' not in r['source_Japanese'] for i,r in by.items() if i!=36)
    assert '心が安まる' in by[30]['source_Japanese'] and '生きていけない' in by[33]['source_Japanese']
    paths=[SOURCE,NAMES,CONTROL,ordinary_path,Path('translations/commodity_name_manuscript_v343.json'),
        Path('translations/commodity_fidelity_v2.json'),Path(__file__)]
    save(ROOT/'two_couple_roles_Sofala_Tea_and_household_request_reconciliation.json',dict(
        candidate=packet['current_ROM'],candidate_sha256=packet['current_ROM_sha256'],
        source_context=str(SOURCE),source_context_sha256=sha(SOURCE.read_bytes()),approved_prose_names=ROLES,
        source_progressive_nameplates=names['progressive_nameplate_values'],full_catalogue_names=names['full_catalogue_values'],
        complete_clean_and_current_role_bindings=roles,source_couple_roles_do_not_establish_marriage_age_or_kinship=True,
        two_source_current_city_aliases=cities,city='Sofala',commodity_index=31,source_commodity='茶',commodity='Tea',
        commodity_binding=live['rows'][2],original_commodity_metadata_hex=good['metadata_hex'],
        personal_enjoyment_and_gentle_dependence_hyperbole_preserved=True,household_tea_is_low_not_city_or_trade_cargo_shortage=True,
        request_to_buy_tomorrow_and_willing_future_agreement_not_completed_transaction=True,
        calming_personal_feeling_not_medical_claim_or_gameplay_bonus=True,
        final_notice_prospective_no_earned_boom_price_profit_or_previous_scene_location=True,
        all9_clean_first_glosses_precede_predecessor_English=True,no_predecessor_English_exposed=True,
        source_owned_pointer_adapter=inspect.getsource(bindings),current_native_pointer_binding=live,
        current_native_context_plan=str(ctx.proof_path),current_native_context_plan_sha256=sha(ctx.proof_path.read_bytes()),
        no_new_commodity_city_or_name_widget_fidelity_completion=True,new_emulator_runs=0,new_review_credit=0,
        evidence={str(p):sha(p.read_bytes()) for p in paths},full_goal_complete=False))
    print('Clean couple roles bound without marital inference; both Sofala aliases and Tea31 live pointers pass. Household request remains separate from prospective notice. Zero credit.')
