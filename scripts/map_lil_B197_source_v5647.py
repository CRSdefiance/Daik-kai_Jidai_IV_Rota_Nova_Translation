"""Bind B197 clean/current objects only after the complete clean exchange and menu gloss."""
import struct
from copy import deepcopy
from collections import Counter
from pathlib import Path
from unicorn.arm_const import UC_ARM_REG_R0
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.native_machine_scoped_v764 import machine
from scripts.native_call_abi_v764 import call
from scripts.inventory_lil_after_crew_items_complete_v3152 import scoped_inventory
from scripts.reconcile_contextual_mood_retentions_v2482 import historical_key
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/lil_B197_source_v5647')
PRIOR=Path('work/analysis/editorial_handoff_verification_v5643/verified_handoff.json')
GLOSS=Path('work/analysis/lil_B197_clean_context_v5646/all21_clean_exchange_three_labels_and_fresh_glosses.json')
SELECTORS=[21,169,254]

def choice_getters3(arm,command):
    value=bytes.fromhex(command['whole_command_hex']);assert command['word']==0x2200;versions=[]
    for phase in [0,2]:
        cpu=machine(arm);stream,owner=0x02660000+phase,0x02662000
        cpu.mem_write(stream-16,b'\xa5'*(len(value)+32));cpu.mem_write(stream,value)
        cpu.mem_write(owner-16,b'\xa5'*64);cpu.mem_write(owner,struct.pack('<3I',0,0,stream));guard=bytes(cpu.mem_read(owner-16,64));before=bytes(cpu.mem_read(0x02000000,0x400000))
        call(cpu,0x2A3B8,(owner,));assert cpu.reg_read(UC_ARM_REG_R0)==3;labels=[]
        for option in range(3):
            relative=8+struct.unpack_from('<H',value,2+2*option)[0];assert 8<=relative<len(value)
            call(cpu,0x2A30C,(owner,option));assert cpu.reg_read(UC_ARM_REG_R0)==stream+relative
            body=value[relative:value.index(0,relative)];assert body
            labels.append(dict(option_index=option,relative_offset=relative,offset=command['offset']+relative,hex=body.hex(),text=body.decode('cp932')))
        assert bytes(cpu.mem_read(0x02000000,0x400000))==before and bytes(cpu.mem_read(owner-16,64))==guard and bytes(cpu.mem_read(stream,len(value)))==value
        assert bytes(cpu.mem_read(stream-16,16))==bytes(cpu.mem_read(stream+len(value),16))==b'\xa5'*16
        versions.append(dict(input_alignment=phase,count=3,labels=labels,original_count_pointer_ABI_all4MiB_owner_stream_and_boundary_guards_exact=True))
    return versions

if __name__=='__main__':
    assert not ROOT.exists();prior,gloss=map(read,[PRIOR,GLOSS]);ledgerpath=Path('translations/editorial_review_current_v1.json')
    assert sha(ledgerpath.read_bytes())==prior['ledger_sha256'];ledger=read(ledgerpath);candidate=ledger['current_integrated_candidate']
    known={historical_key(r) for r in ledger['contextual_story_natural_dialogue_pass_v1871']['record_keys']}
    assert len(known)==6191 and sha(Path(candidate['path']).read_bytes())==candidate['sha256']==prior['candidate_sha256']
    current,clean=NdsImage.open(candidate['path']),NdsImage.open('work/clean.nds');arm,original=[im.read_file('/__arm9__.bin') for im in [current,clean]]
    spans=[(0x2425C,0x242C8),(0x242CC,0x24310),(0x24314,0x24330),(0x24334,0x243A0),(0x2A1D8,0x2A600)]
    assert all(arm[a:b]==original[a:b] for a,b in spans)
    source,target=[IlnkContainer.parse(im.read_file('/data/SC2.DK4')).blocks[197] for im in [clean,current]]
    inventory,walker,invsource=scoped_inventory();old,spoken=inventory(original,source);now,translated=inventory(arm,target)
    shape=lambda cs:[(c['offset'],c['word'],c['native_extent'],c['ancestor_0100_offsets']) for c in cs]
    assert shape(old)==shape(now) and len(old)==39 and len(spoken)==21
    packet_path=Path(gloss['source']);raw_packet=read(packet_path)
    assert sha(packet_path.read_bytes())==gloss['source_sha256'] and sha(source)==raw_packet['clean_block_sha256']
    assert old==raw_packet['commands'] and gloss['read_no_predecessor_English']
    glosses={r['source_record_index']:r for r in gloss['records']};rows=[]
    for sequence,(a,b) in enumerate(zip(spoken,translated,strict=True)):
        sa,ca=a['offset']+5,b['offset']+5;raw=source[sa:source.index(0,sa+1)];value=target[ca:target.index(0,ca+1)]
        index=source[:sa].count(b'\0');r=deepcopy(glosses[index]);assert r['source_hex']==raw.hex()
        assert raw[0]==value[0] in SELECTORS and source[sa-5:sa+1]==target[ca-5:ca+1]
        kind='system-FE' if raw[0]==254 else 'progressive'
        r.update(id=f'DK4_MES_B197_R{index:04d}',file_path='/data/SC2.DK4',block=197,
            source_reference=dict(block=197,offset=sa,bytes=len(raw),header_offset=sa-5,record_index=index),source_Japanese=r['Japanese'],source_complete_preamble_hex=source[sa-5:sa+1].hex(),
            current_record_index=target[:ca].count(b'\0'),current_reference=dict(offset=ca,bytes=len(value),header_offset=ca-5),current_hex=value.hex(),
            source_presentation_prefix_hex=format(raw[0],'02x'),kind=kind,source_kind=kind,current_native_extent=b['native_extent'],native_command_extent=a['native_extent'],spoken_sequence_index=sequence,
            current_native_voice_macro_entry_and_context_pending=True,source_prose_or_completion_credit_added=0)
        rows.append(r)
    a=next(c for c in old if c['word']==0x2200);b=next(c for c in now if c['word']==0x2200)
    versions=[dict(version=version,command=cmd,alignment_cases=choice_getters3(code,cmd)) for version,code,cmd in [('clean',original,a),('current',arm,b)]]
    labels,currentlabels=[v['alignment_cases'][0]['labels'] for v in versions];choices=[]
    assert [r['text'] for r in labels]==['買おう','買わない','任せる']
    for s,t in zip(labels,currentlabels,strict=True):
        option=s['option_index'];assert t['option_index']==option
        choices.append(dict(id=f'DK4_CHOICE_B197_C230_O{option}',file_path='/data/SC2.DK4',block=197,command_offset=230,option_index=option,source_command_word=0x2200,
            source_reference=dict(offset=s['offset'],bytes=len(bytes.fromhex(s['hex']))),current_reference=dict(offset=t['offset'],bytes=len(bytes.fromhex(t['hex']))),source_hex=s['hex'],current_hex=t['hex'],source_Japanese=s['text'],
            fresh_source_gloss=gloss['choices'][0]['fresh_literal_glosses'][option],kind='typed-choice-label',speaker='Player decision after the original15 actor asks the Admiral',
            whole_exchange_note='Original options propose buying,decline buying,or leave the decision to the addressed actor. The third is delegation,not another refusal. Preserve order/results and independently bind financial and branch behavior.',
            current_native_typed_choice_font_reference_and_outcome_binding_pending=True,source_prose_or_completion_credit_added=0))
    assert len(rows)==21 and len(choices)==3 and {r['source_selector'] for r in rows}==set(SELECTORS)
    assert not known&{historical_key(r) for r in rows+choices}
    macros={k:sum(bytes.fromhex(r['source_hex']).count(k.encode()) for r in rows) for k in ['FI','FA','FO']};assert macros==dict(FI=0,FA=0,FO=0)
    for a,b in zip(old,now,strict=True):
        if a['word']==0x100:assert a['whole_command_hex'][:8]==b['whole_command_hex'][:8]
        elif a['word'] not in [0x4000,0x2200]:assert a['whole_command_hex']==b['whole_command_hex']
    assert current.read_file('/data/EV2.DK4')==clean.read_file('/data/EV2.DK4')
    terminal_path=Path('work/analysis/lil_B196_runs_v5639/newgame_terminal.json');terminal=read(terminal_path);report_path=Path(terminal['report']);report=read(report_path)
    assert terminal['terminal'] and report['ROM_sha256']==candidate['sha256'] and report['cold_boot'] and not report['savestate_loaded']
    assert sha(report_path.read_bytes())==terminal['report_sha256'] and not report['callback_errors'] and not report.get('battery_save_preloaded')
    snapshot=next(r for r in report['read_only_capture_RAM_snapshots'] if r['frame']==4000);assert snapshot['read_only_export'] and sha(Path(snapshot['path']).read_bytes())==snapshot['sha256']
    counts=Counter(c['word'] for c in old);relative=[c for c in old if c['word'] in [0x100,0x200,0x300,0x400]]
    assert len(relative)==6 and counts[0xA000]==5 and counts[0x4821]==1 and counts[0]==1 and not counts[0x8000] and not counts[0xC200]
    group=dict(block=197,clean_block_sha256=sha(source),current_block_sha256=sha(target),source_bytes=len(source),current_bytes=len(target),source_header_hex=source[:4].hex(),current_header_hex=target[:4].hex(),
        all_clean_native_commands=old,all_current_native_commands=now,source_native_commands=old,current_native_commands=now,source_current_native_command_shape_exact=True,records=rows,
        choices=[dict(command_offset=230,source_command=next(c for c in old if c['word']==0x2200),current_command=next(c for c in now if c['word']==0x2200),original_count_and_pointer_cases=versions,records=choices)],
        physical_speeches=21,source_selectors=SELECTORS,source_macro_counts=macros,FE_panels=1,relative_sites=6,all_complete_preambles_and_native_command_shapes_equal=True)
    ROOT.mkdir(parents=True);save(ROOT/'all24_clean_current_complete_context_with_three_choice_labels.json',dict(format='dk4-editorial-source-context-packet-v1',file_path='/data/SC2.DK4',
        source_ROM='work/clean.nds',source_ROM_sha256=sha(Path('work/clean.nds').read_bytes()),current_ROM=candidate['path'],current_ROM_sha256=candidate['sha256'],current_ARM9_sha256=sha(arm),current_COMMON_sha256=sha(current.read_file('/COMMON/MESFILE.DK4')),
        source_SC2_sha256=sha(clean.read_file('/data/SC2.DK4')),current_SC2_sha256=sha(current.read_file('/data/SC2.DK4')),original_EV2_sha256=sha(current.read_file('/data/EV2.DK4')),
        actual_historical_snapshot=snapshot['path'],actual_historical_snapshot_sha256=snapshot['sha256'],historical_snapshot_ROM=candidate['path'],legacy_historical_fields_refer_to_actual_current_opening_not_an_overlay=True,
        current_actual_context_capture_report=str(report_path),current_actual_context_report_sha256=sha(report_path.read_bytes()),current_actual_context_snapshot=snapshot,context_is_current_Lil_opening_not_B197_activation=True,
        blocks=[group],records=rows,typed_choice_records=choices,typed_actor_style_records=[],source_macro_counts=macros,total_editorial_objects=24,speech_objects=21,ordinary_source_speeches=20,system_FE_panels=1,
        typed_choice_objects=1,typed_choice_labels=3,source_selectors=SELECTORS,source_static_actor_selectors=SELECTORS[:-1],source_native_commands=39,source_A000=5,source_C200=0,source_relative_sites=6,source_predicates=0,source_picture_commands=1,source_end_words=1,
        original_choice_getter_cases=versions,all12_original_label_getters_and4_count_getters_clean_current_even_alignments_pass=True,native_choice_selection_cancel_fonts_geometry_and_pagination_pending=True,
        source_exact_spans=[dict(start=a,end=b,sha256=sha(arm[a:b])) for a,b in spans],source_transcript=str(packet_path),source_transcript_sha256=sha(packet_path.read_bytes()),whole_exchange_context_notes=str(GLOSS),whole_exchange_context_notes_sha256=sha(GLOSS.read_bytes()),
        all21_clean_speech_glosses_and3_label_glosses_recorded_before_predecessor_English_comparison=True,raw_current_command_hex_and_typed_label_getters_are_structural_evidence_not_translation_source=True,
        source_relative_picture_effect_resource_entry_4720_4735_6003_and_name_contracts_pending=True,no_ROM_registry_ledger_orcredit_change=True,new_emulator_runs=0,
        evidence={str(p):sha(p.read_bytes()) for p in [PRIOR,GLOSS,packet_path,terminal_path,report_path,Path(__file__)]},full_goal_complete=False))
    print('B197:24 exact source/current objects(21 speeches/three2200 labels),39 shapes/six relative sites;12 label/four count getter calls pass.No old speech-prose comparison or credit.')
