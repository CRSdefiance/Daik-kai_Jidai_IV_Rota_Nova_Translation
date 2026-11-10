"""Bind B188's complete clean exchange and current native commands without old prose."""
from copy import deepcopy
from pathlib import Path
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.inventory_lil_after_crew_items_complete_v3152 import scoped_inventory
from scripts.reconcile_contextual_mood_retentions_v2482 import historical_key
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/lil_B188_source_v5232')
PRIOR=Path('work/analysis/editorial_handoff_verification_v5225/verified_handoff.json')
GLOSS=Path('work/analysis/lil_B188_clean_context_v5231/all11_clean_exchange_and_fresh_glosses.json')

if __name__=='__main__':
    assert not ROOT.exists();prior,gloss=read(PRIOR),read(GLOSS)
    lp=Path('translations/editorial_review_current_v1.json');assert sha(lp.read_bytes())==prior['ledger_sha256']
    ledger=read(lp);candidate=ledger['current_integrated_candidate'];known={historical_key(r) for r in ledger['contextual_story_natural_dialogue_pass_v1871']['record_keys']}
    assert len(known)==6043 and sha(Path(candidate['path']).read_bytes())==candidate['sha256']==prior['candidate_sha256']
    current,clean=NdsImage.open(candidate['path']),NdsImage.open('work/clean.nds')
    arm,original=current.read_file('/__arm9__.bin'),clean.read_file('/__arm9__.bin')
    spans=[(0x2425C,0x242C8),(0x242CC,0x24310),(0x24314,0x24330),(0x24334,0x243A0),(0x2A1D8,0x2A600)]
    assert all(arm[a:b]==original[a:b] for a,b in spans)
    source,target=[IlnkContainer.parse(im.read_file('/data/SC2.DK4')).blocks[188] for im in [clean,current]]
    inventory,walker,invsource=scoped_inventory();old,spoken=inventory(original,source);now,translated=inventory(arm,target)
    shape=lambda commands:[(c['offset'],c['word'],c['native_extent'],c['ancestor_0100_offsets']) for c in commands]
    assert shape(old)==shape(now) and len(old)==14 and len(spoken)==11
    packet_path=Path(gloss['source']);raw_packet=read(packet_path)
    assert sha(packet_path.read_bytes())==gloss['source_sha256'] and sha(source)==raw_packet['clean_block_sha256']
    assert old==raw_packet['commands'] and gloss['read_no_predecessor_English']
    glosses={r['source_record_index']:r for r in gloss['records']};rows=[]
    for sequence,(a,b) in enumerate(zip(spoken,translated,strict=True)):
        sa,ca=a['offset']+5,b['offset']+5;raw=source[sa:source.index(b'\0',sa+1)];value=target[ca:target.index(b'\0',ca+1)]
        index=source[:sa].count(b'\0');r=deepcopy(glosses[index]);assert r['source_hex']==raw.hex()
        assert raw[0]==value[0] in [130,150,254] and source[sa-5:sa+1]==target[ca-5:ca+1]
        kind='system-FE' if raw[0]==254 else 'progressive'
        r.update(id=f'DK4_MES_B188_R{index:04d}',file_path='/data/SC2.DK4',block=188,source_record_index=index,
            source_reference=dict(block=188,offset=sa,bytes=len(raw),header_offset=sa-5,record_index=index),
            source_Japanese=r['Japanese'],fresh_source_gloss=r['fresh_source_gloss'],source_complete_preamble_hex=source[sa-5:sa+1].hex(),
            current_record_index=target[:ca].count(b'\0'),current_reference=dict(offset=ca,bytes=len(value),header_offset=ca-5),
            current_hex=value.hex(),source_presentation_prefix_hex=format(raw[0],'02x'),kind=kind,source_kind=kind,
            current_native_extent=b['native_extent'],native_command_extent=a['native_extent'],spoken_sequence_index=sequence,
            current_native_voice_macro_entry_and_context_pending=True,source_prose_or_completion_credit_added=0)
        rows.append(r)
    assert not known&{historical_key(r) for r in rows}
    assert [c['word'] for c in old if c['word'] not in [0x4000,0x100,0x200,0x300,0x400]]==[0xA000,0xC200,0]
    macros={k:sum(bytes.fromhex(r['source_hex']).count(k.encode()) for r in rows) for k in ['FI','FA','FO']};assert macros==dict(FI=0,FA=0,FO=0)
    assert current.read_file('/data/EV2.DK4')==clean.read_file('/data/EV2.DK4')
    terminal_path=Path('work/analysis/lil_B187_runs_v5221/newgame_terminal.json');terminal=read(terminal_path)
    report_path=Path(terminal['report']);report=read(report_path)
    assert terminal['terminal'] and report['ROM_sha256']==candidate['sha256'] and report['cold_boot'] and not report['savestate_loaded']
    assert sha(report_path.read_bytes())==terminal['report_sha256'] and not report['callback_errors'] and not report.get('battery_save_preloaded')
    snapshot=next(r for r in report['read_only_capture_RAM_snapshots'] if r['frame']==4000)
    assert snapshot['read_only_export'] and sha(Path(snapshot['path']).read_bytes())==snapshot['sha256']
    group=dict(block=188,clean_block_sha256=sha(source),current_block_sha256=sha(target),source_bytes=len(source),current_bytes=len(target),
        source_header_hex=source[:4].hex(),current_header_hex=target[:4].hex(),all_clean_native_commands=old,all_current_native_commands=now,
        source_native_commands=old,current_native_commands=now,source_current_native_command_shape_exact=True,records=rows,choices=[],
        physical_speeches=11,source_selectors=[130,150,254],source_macro_counts=macros,FE_panels=1,relative_sites=0,
        all_complete_preambles_and_native_command_shapes_equal=True)
    ROOT.mkdir(parents=True)
    save(ROOT/'all11_clean_current_complete_context.json',dict(format='dk4-editorial-source-context-packet-v1',file_path='/data/SC2.DK4',
        source_ROM='work/clean.nds',source_ROM_sha256=sha(Path('work/clean.nds').read_bytes()),current_ROM=candidate['path'],current_ROM_sha256=candidate['sha256'],
        current_ARM9_sha256=sha(arm),current_COMMON_sha256=sha(current.read_file('/COMMON/MESFILE.DK4')),
        source_SC2_sha256=sha(clean.read_file('/data/SC2.DK4')),current_SC2_sha256=sha(current.read_file('/data/SC2.DK4')),
        original_EV2_sha256=sha(current.read_file('/data/EV2.DK4')),
        actual_historical_snapshot=snapshot['path'],actual_historical_snapshot_sha256=snapshot['sha256'],historical_snapshot_ROM=candidate['path'],
        legacy_historical_fields_refer_to_actual_current_opening_not_an_overlay=True,
        current_actual_context_capture_report=str(report_path),current_actual_context_report_sha256=sha(report_path.read_bytes()),current_actual_context_snapshot=snapshot,
        context_is_current_Lil_opening_not_B188_activation=True,blocks=[group],records=rows,typed_choice_records=[],typed_actor_style_records=[],
        source_macro_counts=macros,total_editorial_objects=11,speech_objects=11,ordinary_source_speeches=10,system_FE_panels=1,
        source_selectors=[130,150,254],source_static_actor_selectors=[130,150],source_native_commands=14,
        source_A000=1,source_C200=1,source_relative_sites=0,source_predicates=0,
        source_exact_spans=[dict(start=a,end=b,sha256=sha(arm[a:b])) for a,b in spans],
        source_transcript=str(packet_path),source_transcript_sha256=sha(packet_path.read_bytes()),
        whole_exchange_context_notes=str(GLOSS),whole_exchange_context_notes_sha256=sha(GLOSS.read_bytes()),
        all11_clean_first_glosses_already_recorded_before_current_comparison=True,
        no_ROM_registry_ledger_orcredit_change=True,new_emulator_runs=0,
        evidence={str(p):sha(p.read_bytes()) for p in [PRIOR,GLOSS,packet_path,terminal_path,report_path,Path(__file__)]},full_goal_complete=False))
    print('B188 bound:11 complete speeches,14 linear commands,A000/C200/end;two source actors and current V5219 opening snapshot. No credit.')
