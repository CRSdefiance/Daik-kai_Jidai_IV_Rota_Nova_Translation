"""Bind seven names, FO, price, alternative item descriptions and original event entry."""
import struct
from pathlib import Path
from ndspy.code import MainCodeFile
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.main_pool_cache_visibility import POOL
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B138_terms_v3429')
SOURCE=Path('work/analysis/lil_remaining_B138_B140_source_v3422/next44_B138_clean_current_context.json')
CONTEXT=Path('work/analysis/lil_B138_clean_context_v3428/all44_complete_clean_context_and_fresh_glosses.json')
VOICE=Path('work/analysis/lil_B138_voices_v3425/current_seven_static_names_voices_and207_catalog_rebind.json')
CONTROL=Path('work/analysis/lil_B138_controls_v3426e/all44_source_current_dispatches10_predicates_and1_query.json')
CATALOG=Path('translations/all_item_names_arm9_v1.json')
if __name__=='__main__':
    assert not ROOT.exists();packet,context,voice,control,catalog=map(read,[SOURCE,CONTEXT,VOICE,CONTROL,CATALOG]);assert context['all44_complete_clean_source_objects_read_before_older_English_comparison']
    item=next(r for r in catalog['records'] if r['id']=='DK4_ITEM_POINTER_177');assert item['english']=='Evergreen Lotus Leaf'
    versions=[]
    for version,path in [('clean','work/clean.nds'),('current',packet['current_ROM'])]:
        image=NdsImage.open(path);arm=image.read_file('/__arm9__.bin');code=MainCodeFile(arm,0x02000000);views=[(s.ramAddress,bytes(s.data),'original-main-code-section') for s in code.sections]
        if version=='current':assert len(code.sections[3].data)-48==123040;views.append((POOL,bytes(code.sections[3].data[:-48]),'registered123040-byte-runtime-pool-copy'))
        pointer=struct.unpack_from('<I',arm,item['offset'])[0];hits=[v for v in views if v[0]<=pointer<v[0]+len(v[1])];assert len(hits)==1
        base,data,owner=hits[0];tail=data[pointer-base:];end=tail.index(b'\0');name=tail[:end].decode('cp932');assert name==('枯れないハスの葉' if version=='clean' else 'Evergreen Lotus Leaf')
        versions.append(dict(version=version,ROM=path,ROM_sha256=sha(Path(path).read_bytes()),ARM9_sha256=sha(arm),item_ID=177,catalog_record_ID=item['id'],pointer_file_offset=item['offset'],pointer=pointer,storage_owner=owner,complete_C_string_hex=tail[:end+1].hex(),text=name))
    names={r['actor_ID']:r['current_catalog_name'] for r in voice['fresh_seven_actor_names']['rows']};assert set(names)=={2,14,20,21,22,23,92} and names[21]=='Ian Dukov'
    rows={r['source_record_index']:r for r in packet['records']};assert '１００' in rows[93]['source_Japanese'] and rows[78]['source_Japanese']==rows[253]['source_Japanese']=='？'
    assert '宝の地図' in rows[82]['source_Japanese'] and '葉っぱ' in rows[261]['source_Japanese']
    commands=packet['blocks'][0]['all_clean_native_commands'];displays=[c for c in commands if c['word'] in [0x4879,0x4841]]
    assert [c['whole_command_hex'] for c in displays]==['7948b1a8','4148b1a8'] and all(bytes.fromhex(c['whole_command_hex'])[2:]==bytes.fromhex('b1a8') for c in displays)
    source_event=packet['blocks'][0]['original_event_source'];assert source_event['event_ID']==138 and source_event['action_index']==139 and source_event['SC2_action_block']==138 and source_event['native_action_word']==0x208A
    ev=NdsImage.open(packet['current_ROM']).read_file('/data/EV2.DK4');assert ev==NdsImage.open('work/clean.nds').read_file('/data/EV2.DK4')
    at=96+source_event['body_offset'];source_bytes=bytes.fromhex(source_event['source_hex']);assert ev[at:at+len(source_bytes)]==source_bytes
    historical=read(packet['prior_state_inventory']);assert historical['all336_original_events'][138]==source_event
    parent=NdsImage.open(historical['candidate']);current=NdsImage.open(packet['current_ROM'])
    for start,end in [(0x220D8,0x22ECC),(0x23840,0x23A28),(0x256A0,0x256D0),(0x2A690,0x2A6C0)]:assert current.read_file('/__arm9__.bin')[start:end]==parent.read_file('/__arm9__.bin')[start:end]
    query=control['original_event_queries'];assert len(query)==1 and query[0]['event']==137
    macros=[c for c in control['speech_dispatch_cases'] if c['version']=='clean-Japanese' and c['id']==rows[23]['id']];assert len(macros)==1
    raw=bytes.fromhex(rows[23]['source_hex'])[1:];expanded=bytes.fromhex(macros[0]['boundaries'][1]['text_hex']);assert raw.count(b'FO')==1 and expanded==raw.replace(b'FO',b'Argot Co.')
    ROOT.mkdir(parents=True);terms=ROOT/'clean_current_names_leaf_price_macro_and_entry_reconciliation.json'
    save(terms,dict(source_context=str(SOURCE),source_context_sha256=sha(SOURCE.read_bytes()),complete_clean_context=str(CONTEXT),complete_clean_context_sha256=sha(CONTEXT.read_bytes()),voice_proof=str(VOICE),voice_proof_sha256=sha(VOICE.read_bytes()),control_proof=str(CONTROL),control_proof_sha256=sha(CONTROL.read_bytes()),registered_item_catalog=str(CATALOG),registered_item_catalog_sha256=sha(CATALOG.read_bytes()),two_complete_item_pointer_versions=versions,approved_item_name='Evergreen Lotus Leaf',exact_current_actor_names=names,approved_dialogue_names=dict(Lil='Lil',Emilio='Emilio',Fernando='Fernando',Ian='Ian',Samwell='Samwell',Manuel='Manuel',Nagarpur='Nagarpur',barkeep='unnamed barkeep;not Uncle'),source_price_gold_coins=100,source_FO_occurrences=1,current_bound_FO_expansion='Argot Co.',FO_runtime_token_must_be_preserved_not_hardcoded=True,source_display_commands=displays,same_original_item177_operand_in_two_display_forms=True,source_reported_treasure_map_and_unidentified_leaf_descriptions_both_preserved=True,no_new_second_item_or_confirmed_treasure_identification_invented=True,ordinary_leaf_reference_not_forced_to_full_catalogue_name=True,source_wordless_question_marks_at_records=[78,253],source_8000_raw_result2_and8100_boolean_query_remain_distinct=True,source_event_record=source_event,source_event_file_offset=at,source_event_bytes_hex=source_bytes.hex(),event138_action139_native208A_selects_SC2_B138=True,source_entry_binding_reused_from_exact_EV2_native_spans_and_historical336_event_inventory=True,historical_event137_completion_query_not_current_eligibility_or_selected_gameplay=True,all44_source_locations_uncredited_in_current_ledger=True,company_status_reports_and_gift_purchase_paths_are_alternatives=True,nested_Emilio_Samwell_replies_and_separate_Ian_Fernando_Manuel_conditions_preserved=True,earlier_money_maxim_callback_and_barkeep_dignity_arc_preserved=True,no_new_rank_family_romance_or_item_facts=True,whole_goal_Proof_consistency_Maria32_COMMON3_and_wider_scope_remain_open=True,no_ROM_registry_or_editorial_credit_change=True,new_emulator_runs=0,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    a=Path('scripts/compare_lil_B137_effective_v3388.py');b=Path('scripts/compare_lil_B138_effective_v3431.py');assert not b.exists();t=a.read_text(encoding='utf-8')
    changes=[('lil_B137_comparison_v3388','lil_B138_comparison_v3431'),('work/analysis/lil_remaining_B137_B140_source_v3380b/next48_B137_clean_current_context.json',SOURCE.as_posix()),('work/analysis/lil_B137_controls_v3384/all48_source_current_dispatches_and12_predicates.json',CONTROL.as_posix()),('work/analysis/lil_B137_clean_context_v3386/all48_complete_clean_context_and_fresh_glosses.json',CONTEXT.as_posix()),('work/analysis/lil_B137_terms_v3387/clean_current_names_addresses_thought_and_fivefold_wages.json',terms.as_posix()),('all48','all44'),('fresh48','fresh44'),('len(rows)==48','len(rows)==44'),('source_current_comparisons=48','source_current_comparisons=44'),('Eleven static names,FI3,twelve predicates,thought/wordless-shock markers andfivefold hypothetical wages bound.','Seven static names,FO1,ten predicates,one event137 query,raw predicate result2,price100,shared leaf item177 and original B138 entry bound.')]
    for x,y in changes:assert x in t,x;t=t.replace(x,y)
    compile(t,str(b),'exec');b.write_text(t,encoding='utf-8');save(ROOT/'comparison_tool_provenance.json',dict(previous=str(a),previous_sha256=sha(a.read_bytes()),successor=str(b),successor_sha256=sha(b.read_bytes()),producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print('Seven names,FO1,price100,leaf item177,two source descriptions and B138 entry bound. Comparison prepared;no source/prose or completion credit.')
