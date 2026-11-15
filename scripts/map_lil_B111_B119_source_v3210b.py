"""Fresh clean/current source mapping for every remaining B111-B119 object."""
from copy import deepcopy
from pathlib import Path
import struct
from unicorn.arm_const import UC_ARM_REG_R0
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from scripts.inventory_lil_after_crew_items_complete_v3152 import scoped_inventory
from scripts.native_machine_scoped_v764 import machine
from scripts.native_call_abi_v764 import call
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/lil_B111_B119_source_v3210b')
PRIOR=Path('work/analysis/editorial_handoff_verification_v3209/verified_handoff.json')
VOICE=Path('work/analysis/lil_4100_alternatives_v3156/all14_clean_current_eight_style_alternatives.json')
HISTORY=Path('work/analysis/lil_after_London_inventory_v1913/all336_states_and_original_London_town_eligibility.json')

if __name__=='__main__':
    assert not ROOT.exists()
    lp=Path('translations/editorial_review_current_v1.json');ledger=read(lp)
    assert sha(lp.read_bytes())==read(PRIOR)['ledger_sha256']
    candidate=ledger['current_integrated_candidate']
    current,clean=[NdsImage.open(p) for p in [candidate['path'],'work/clean.nds']]
    assert sha(Path(candidate['path']).read_bytes())==candidate['sha256']
    arm,original=current.read_file('/__arm9__.bin'),clean.read_file('/__arm9__.bin')
    spans=[(0x2434C,0x243A0),(0x29BD0,0x29D34),(0x2A154,0x2A1D8),(0x2A414,0x2A5BC),(0x7E988,0x7E9A0)]
    for a,b in spans:assert arm[a:b]==original[a:b]
    historical=read(HISTORY);history=NdsImage.open(historical['candidate'])
    assert sha(Path(historical['candidate']).read_bytes())==historical['candidate_sha256']
    assert sha(Path(historical['snapshot']).read_bytes())==historical['snapshot_sha256']
    ev=clean.read_file('/data/EV2.DK4')
    assert current.read_file('/data/EV2.DK4')==history.read_file('/data/EV2.DK4')==ev
    jp,en=[IlnkContainer.parse(i.read_file('/data/SC2.DK4')).blocks for i in [clean,current]]
    oldvoice=read(VOICE);inventory,walker,inventory_source=scoped_inventory()
    packets=[];records=[];alternatives=[];getter_cases=[]
    for n in range(111,120):
        source,target=jp[n],en[n]
        commands,speeches=inventory(original,source);now,spoken=inventory(arm,target)
        shape=lambda rs:[(r['offset'],r['word'],r['native_extent'],r['ancestor_0100_offsets']) for r in rs]
        assert shape(commands)==shape(now)
        assert not any(0x2000<=c['word']<0x4000 for c in commands)
        raw_headers=[at for at in range(len(source)-4) if source[at:at+5]==bytes.fromhex('0040ffff00')]
        assert raw_headers==sorted(c['offset'] for c in speeches)
        rows=[]
        for sequence,(a,b) in enumerate(zip(speeches,spoken,strict=True)):
            ja,at=a['offset']+5,b['offset']+5
            raw,value=source[ja:source.index(b'\0',ja)],target[at:target.index(b'\0',at)]
            prefix=raw[0]
            assert value[0]==prefix and source[ja-5:ja+1]==target[at-5:at+1]==bytes.fromhex('0040ffff00')+bytes([prefix])
            row=dict(id=f'DK4_MES_B{n}_R{source[:ja].count(bytes([0])):04d}',file_path='/data/SC2.DK4',block=n,
                source_record_index=source[:ja].count(b'\0'),current_record_index=target[:at].count(b'\0'),
                source_reference=dict(offset=ja,bytes=len(raw),header_offset=ja-5),
                current_reference=dict(offset=at,bytes=len(value),header_offset=at-5),
                source_hex=raw.hex(),current_hex=value.hex(),source_Japanese=raw[1:].decode('cp932'),
                current_English=value[1:].decode('cp932'),source_complete_preamble_hex=source[ja-5:ja+1].hex(),
                source_presentation_prefix_hex=f'{prefix:02x}',kind='system-FE' if prefix==254 else 'source-speech-4000',
                source_selector=prefix,original_actor_ID=prefix if prefix<207 else None,
                dynamic_selector_requires_source_binding=207<=prefix<224,
                speaker={2:'Lil Argot',9:'Camille',16:'Gerhard',20:'Fernando',254:'Original FE modal presenter;not actor254'}.get(prefix,f'Source selector{prefix};native identity/source role pending'),
                native_command_extent=a['native_extent'],ancestor_0100_offsets=a['ancestor_0100_offsets'],
                spoken_sequence_index=sequence,current_macro_dispatch_consumer_and_complete_native_display_pending=True,
                source_prose_or_completion_credit_added=0)
            rows.append(row);records.append(row)
        objects=deepcopy([o for o in oldvoice['objects'] if o['block']==n])
        for obj in objects:
            for label,data,runtime,key in [('clean',source,original,'source_command'),('current',target,arm,'current_command')]:
                c=obj[key];at=c['offset'];value=data[at:at+c['native_extent']]
                assert value.hex()==c['whole_command_hex'] and value[:2]==b'\0\x41' and value[18]==0 and all(r['source_selector']==value[19] for r in obj['records'])
                cpu=machine(runtime);stream,owner=0x02660000,0x02662000
                cpu.mem_write(stream-16,b'\xa5'*(len(value)+32));cpu.mem_write(stream,value)
                cpu.mem_write(owner-16,b'\xa5'*64);cpu.mem_write(owner,struct.pack('<4I',0,stream,0,0))
                before_owner=bytes(cpu.mem_read(owner-16,64));before=bytes(cpu.mem_read(0x02000000,0x400000))
                version=next(v for v in obj['versions'] if v['version']==label)
                for i in range(8):
                    relative=20+struct.unpack_from('<H',value,2+2*i)[0]
                    call(cpu,0x2A154,(owner,i));pointer=cpu.reg_read(UC_ARM_REG_R0)
                    assert pointer==stream+relative
                    text=value[relative:value.index(b'\0',relative)]
                    slot=next(s for s in version['style_slots'] if s['style_index']==i)
                    assert slot['hex']==text.hex() and slot['relative_offset']==relative
                    assert bytes(cpu.mem_read(pointer,len(text)+1))==text+b'\0'
                    getter_cases.append(dict(block=n,command_offset=at,version=label,style_index=i,source_selector=value[19],
                        relative_offset=relative,hex=text.hex(),original_inline_getter_ABI_all4MiB_and_guards_exact=True))
                assert bytes(cpu.mem_read(0x02000000,0x400000))==before
                assert bytes(cpu.mem_read(owner-16,64))==before_owner and bytes(cpu.mem_read(stream,len(value)))==value
                assert bytes(cpu.mem_read(stream-16,16))==bytes(cpu.mem_read(stream+len(value),16))==b'\xa5'*16
            alternatives.extend(obj['records'])
        packets.append(dict(block=n,clean_block_sha256=sha(source),current_block_sha256=sha(target),
            source_bytes=len(source),current_bytes=len(target),all_clean_native_commands=commands,
            all_current_native_commands=now,source_current_native_command_shape_exact=True,records=rows,
            actor_style_objects=objects,choices=[],original_event_source=historical['all336_original_events'][n],
            historical_completion_or_dependency_state_not_current_eligibility=True,
            all_source_speech_headers_and_actor_style_slots_bound=True))
    assert len(records)==148 and sum(r['kind']=='system-FE' for r in records)==2
    assert len(alternatives)==34 and sum(len(p['actor_style_objects']) for p in packets)==6 and len(getter_cases)==96
    assert sum(len(p['all_clean_native_commands']) for p in packets)==305
    known={(r['file_path'],r['id']) for r in ledger['contextual_story_natural_dialogue_pass_v1871']['record_keys']}
    assert not known&{(r['file_path'],r['id']) for r in records+alternatives}
    ROOT.mkdir(parents=True)
    save(ROOT/'complete182_clean_current_native_context.json',dict(format='dk4-editorial-source-context-packet-v1',
        source_ROM='work/clean.nds',source_ROM_sha256=sha(Path('work/clean.nds').read_bytes()),
        current_ROM=candidate['path'],current_ROM_sha256=candidate['sha256'],current_ARM9_sha256=sha(arm),
        source_SC2_sha256=sha(clean.read_file('/data/SC2.DK4')),current_SC2_sha256=sha(current.read_file('/data/SC2.DK4')),
        original_EV2_sha256=sha(ev),actual_historical_snapshot=historical['snapshot'],
        actual_historical_snapshot_sha256=historical['snapshot_sha256'],historical_snapshot_ROM=historical['candidate'],
        historical_snapshot_is_London_not_selected_B111_B119_scenes=True,
        source_exact_spans=[dict(start=a,end=b,sha256=sha(arm[a:b])) for a,b in spans],
        blocks=packets,records=records,typed_actor_style_records=alternatives,typed_choice_records=[],
        total_editorial_objects=182,speech_objects=148,ordinary_source_speeches=146,system_FE_panels=2,
        actor_style_objects=6,actor_style_slots=48,unique_stored_actor_style_alternatives=34,
        typed_choice_objects=0,typed_choice_labels=0,all_2000_group_text_commands_absent=True,
        original_clean_current_inline_getter_cases=getter_cases,
        all96_style_getters_freshly_execute_current_and_clean_runtime=True,
        distinct_actor_style_presentation_selectors=sorted({r['source_selector'] for r in alternatives}),
        source_4100_is_actor_style_alternatives_not_player_choices=True,
        source_dynamic_selectors_context_and_native_voice_mapping_pending=True,
        current_macro_dispatch_consumer_native_font_and_pagination_pending=True,
        whole_clean_exchange_context_and_older_English_comparison_pending=True,
        explicit_unmatched_native_walk=walker,unchanged_inventory_function=inventory_source,
        scope='Nine complete B111-B119 exchanges:148speech(146ordinary/2FE),34storedactor-style alternatives/48slots/6objects,no playerchoice menus,305commands. All headers/aliases bind clean/current exactbytes;96fresh inlinegettercalls pass. Whole clean context mustbe readbefore olderEnglish comparison. Bind current roles/voices/macros/consumers andall branch/display/reference/representative/release gates. HistoricalLondon EV2/model state isnot selectedscene eligibility or earnedprogress. B120 and235B101-B110 objects alreadycompleted andexcluded. No neweditorial credit.',
        evidence={str(p):sha(p.read_bytes()) for p in [PRIOR,VOICE,HISTORY,Path(__file__)]},
        source_prose_credit_added=0,completion_credit_added=0,new_emulator_runs=0,full_goal_complete=False))
    print('B111-B119:182source/current objects(148speech/34actor-style alternatives),305commands,96fresh nativegetters;no choices. Fullcleancontext/currentbindings/prose/native/release gates pending;zero credit.')
