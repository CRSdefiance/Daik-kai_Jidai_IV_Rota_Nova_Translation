"""Bind every source/current object in ten complete shrine/temple exchanges."""
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from scripts.inventory_lil_after_crew_items_complete_v3152 import scoped_inventory
from scripts.verify_village_wrap_v608 import read,save

ROOT = Path('work/analysis/lil_Shrines_Temples_source_v3159')
PRIOR = Path('work/analysis/editorial_handoff_verification_v3158/verified_handoff.json')
VOICE = Path('work/analysis/lil_4100_alternatives_v3156/all14_clean_current_eight_style_alternatives.json')
HISTORY = Path('work/analysis/lil_after_London_inventory_v1913/all336_states_and_original_London_town_eligibility.json')

if __name__ == '__main__':
    assert not ROOT.exists()
    ledgerpath = Path('translations/editorial_review_current_v1.json')
    ledger = read(ledgerpath)
    assert sha(ledgerpath.read_bytes()) == read(PRIOR)['ledger_sha256']
    candidate = ledger['current_integrated_candidate']
    current,clean = [NdsImage.open(p) for p in [candidate['path'],'work/clean.nds']]
    assert sha(Path(candidate['path']).read_bytes()) == candidate['sha256']
    arm,original = current.read_file('/__arm9__.bin'),clean.read_file('/__arm9__.bin')
    spans = [(0x2434C,0x243A0),(0x29BD0,0x29D34),(0x2A154,0x2A1D8),(0x2A414,0x2A5BC),(0x7E988,0x7E9A0)]
    for a,b in spans:
        assert arm[a:b] == original[a:b]
    historical = read(HISTORY)
    history = NdsImage.open(historical['candidate'])
    assert sha(Path(historical['candidate']).read_bytes()) == historical['candidate_sha256']
    assert sha(Path(historical['snapshot']).read_bytes()) == historical['snapshot_sha256']
    ev = clean.read_file('/data/EV2.DK4')
    assert current.read_file('/data/EV2.DK4') == history.read_file('/data/EV2.DK4') == ev
    jp,en = [IlnkContainer.parse(i.read_file('/data/SC2.DK4')).blocks for i in [clean,current]]
    voice = read(VOICE)
    assert voice['candidate_sha256'] == candidate['sha256']
    inventory,_,_ = scoped_inventory()
    packets,records,alternatives = [],[],[]
    for n in range(101,111):
        source,target = jp[n],en[n]
        commands,speeches = inventory(original,source)
        now,spoken = inventory(arm,target)
        shape = lambda rs:[(r['offset'],r['word'],r['native_extent'],r['ancestor_0100_offsets']) for r in rs]
        assert shape(commands) == shape(now)
        rows = []
        for sequence,(a,b) in enumerate(zip(speeches,spoken,strict=True)):
            ja,at = a['offset']+5,b['offset']+5
            raw,value = source[ja:source.index(bytes([0]),ja)],target[at:target.index(bytes([0]),at)]
            prefix = raw[0]
            assert value[0] == prefix and source[ja-5:ja+1] == target[at-5:at+1] == bytes.fromhex('0040ffff00')+bytes([prefix])
            row = dict(id=f'DK4_MES_B{n}_R{source[:ja].count(bytes([0])):04d}',file_path='/data/SC2.DK4',block=n,
                source_record_index=source[:ja].count(bytes([0])),current_record_index=target[:at].count(bytes([0])),
                source_reference=dict(offset=ja,bytes=len(raw),header_offset=ja-5),current_reference=dict(offset=at,bytes=len(value),header_offset=at-5),
                source_hex=raw.hex(),current_hex=value.hex(),source_Japanese=raw[1:].decode('cp932'),current_English=value[1:].decode('cp932'),
                source_complete_preamble_hex=source[ja-5:ja+1].hex(),source_presentation_prefix_hex=f'{prefix:02x}',
                kind='system-FE' if prefix==254 else 'source-speech-4000',source_selector=prefix,
                original_actor_ID=prefix if prefix<207 else None,dynamic_selector_requires_source_binding=207<=prefix<224,
                speaker={2:'Lil Argot',9:'Camille',16:'Gerhard',20:'Fernando',254:'Original FE modal presenter;not actor254'}.get(prefix,f'Source selector{prefix};native identity andsource role pending'),
                native_command_extent=a['native_extent'],ancestor_0100_offsets=a['ancestor_0100_offsets'],spoken_sequence_index=sequence,
                current_macro_dispatch_consumer_and_complete_native_display_pending=True,source_prose_or_completion_credit_added=0)
            rows.append(row)
            records.append(row)
        objects = [o for o in voice['objects'] if o['block']==n]
        for obj in objects:
            assert source[obj['command_offset']:obj['command_offset']+obj['source_command']['native_extent']].hex() == obj['source_command']['whole_command_hex']
            assert target[obj['command_offset']:obj['command_offset']+obj['current_command']['native_extent']].hex() == obj['current_command']['whole_command_hex']
            alternatives.extend(obj['records'])
        packets.append(dict(block=n,clean_block_sha256=sha(source),current_block_sha256=sha(target),source_bytes=len(source),current_bytes=len(target),
            all_clean_native_commands=commands,all_current_native_commands=now,source_current_native_command_shape_exact=True,records=rows,
            actor_style_objects=objects,original_event_source=historical['all336_original_events'][n],
            historical_completion_or_dependency_state_not_current_eligibility=True,all_source_speech_headers_and_actor_style_slots_bound=True))
    assert len(records)==164 and sum(r['kind']=='system-FE' for r in records)==30
    assert len(alternatives)==56 and sum(len(p['actor_style_objects']) for p in packets)==8
    assert sum(len(p['all_clean_native_commands']) for p in packets)==421
    keys={(r['file_path'],r['id']) for r in ledger['contextual_story_natural_dialogue_pass_v1871']['record_keys']}
    assert not keys & {(r['file_path'],r['id']) for r in records+alternatives}
    ROOT.mkdir(parents=True)
    save(ROOT/'complete220_clean_current_native_context.json',dict(format='dk4-editorial-source-context-packet-v1',source_ROM='work/clean.nds',source_ROM_sha256=sha(Path('work/clean.nds').read_bytes()),
        current_ROM=candidate['path'],current_ROM_sha256=candidate['sha256'],current_ARM9_sha256=sha(arm),source_SC2_sha256=sha(clean.read_file('/data/SC2.DK4')),current_SC2_sha256=sha(current.read_file('/data/SC2.DK4')),original_EV2_sha256=sha(ev),
        actual_historical_snapshot=historical['snapshot'],actual_historical_snapshot_sha256=historical['snapshot_sha256'],historical_snapshot_ROM=historical['candidate'],historical_snapshot_is_London_not_selected_Shrines_Temples_scenes=True,
        source_exact_spans=[dict(start=a,end=b,sha256=sha(arm[a:b])) for a,b in spans],blocks=packets,records=records,typed_actor_style_records=alternatives,
        total_editorial_objects=220,speech_objects=164,ordinary_source_speeches=134,system_FE_panels=30,actor_style_objects=8,actor_style_slots=64,unique_stored_actor_style_alternatives=56,
        source_4100_is_eight_actor_style_alternatives_not_player_choices=True,source_dynamic_CF_D0_context_and_native_voice_mapping_pending=True,
        current_macro_dispatch_consumer_native_font_and_pagination_pending=True,whole_clean_exchange_context_and_older_English_comparison_pending=True,
        scope='Ten complete LilSC2B101-B110 source/current exchanges:164speech/56unique stored actor-style alternatives. All421commands andall64slots/eight4100objects bind exact source/current references andaliases. No full clean context reading,glosses,prose,consumer/display approval,relocation,representative sampling orrelease isclaimed. HistoricalEV2 state isnot current eligibility or earnedprogress. Preserve allsourcebranches,CF/D0dynamic selectors,source speaker preambles,FI/FA/FO andstyle aliases. Staticgeneric selector identities mustbereconciled beforeprose;do notinvent ranks/relationships. All220objects remainuncredited.',
        evidence={str(p):sha(p.read_bytes()) for p in [PRIOR,VOICE,HISTORY,Path(__file__)]},source_prose_credit_added=0,completion_credit_added=0,new_emulator_runs=0,full_goal_complete=False))
    print('B101-B110:220source/current objects(164speech/56storedactor-style alternatives),421commands. Currentconsumers/voices/fullcontext/prose/display/reference/release pending;zero credit.')
