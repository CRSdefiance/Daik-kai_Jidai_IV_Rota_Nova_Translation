"""Bind32 clean-first Maria speeches and all40 exact current commands."""
from copy import deepcopy
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from scripts.inventory_lil_after_crew_items_complete_v3152 import scoped_inventory
from scripts.reconcile_contextual_mood_retentions_v2482 import historical_key
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/maria_B97_source_v4998')
GLOSS=Path('work/analysis/maria_B97_clean_glosses_v4996/all32_clean_exchange_and_fresh_glosses.json')
PRIOR=Path('work/analysis/editorial_handoff_verification_v4993/verified_handoff.json')
if __name__=='__main__':
    assert not ROOT.exists();prior,gloss=read(PRIOR),read(GLOSS);lp=Path('translations/editorial_review_current_v1.json')
    assert sha(lp.read_bytes())==prior['ledger_sha256'];ledger=read(lp);candidate=ledger['current_integrated_candidate']
    assert sha(Path(candidate['path']).read_bytes())==candidate['sha256']==prior['candidate_sha256']
    known={historical_key(r) for r in ledger['contextual_story_natural_dialogue_pass_v1871']['record_keys']};assert len(known)==5966
    current,clean=NdsImage.open(candidate['path']),NdsImage.open('work/clean.nds');arm,ca=current.read_file('/__arm9__.bin'),clean.read_file('/__arm9__.bin')
    spans=[(0x2425C,0x242C8),(0x242CC,0x24310),(0x24314,0x24330),(0x24334,0x243A0),(0x2A1D8,0x2A600)]
    assert all(arm[a:b]==ca[a:b] for a,b in spans)
    jp,en=[IlnkContainer.parse(im.read_file('/data/SC3.DK4')).blocks[97] for im in [clean,current]]
    inv,walker,invsource=scoped_inventory();old,spoken=inv(ca,jp);now,translated=inv(arm,en)
    shape=lambda commands:[(c['offset'],c['word'],c['native_extent'],c['ancestor_0100_offsets']) for c in commands]
    assert shape(old)==shape(now) and len(old)==40 and len(spoken)==len(translated)==32
    rawpath=Path(gloss['source']);raw=read(rawpath);assert sha(rawpath.read_bytes())==gloss['source_sha256'] and sha(jp)==raw['clean_block_sha256'] and old==raw['commands']
    assert gloss['read_no_predecessor_English'];glosses={r['source_record_index']:r for r in gloss['records']};rows=[]
    for index,(a,b) in enumerate(zip(spoken,translated,strict=True)):
        sa,at=a['offset']+5,b['offset']+5;s=jp[sa:jp.index(0,sa+1)];v=en[at:en.index(0,at+1)];record=jp[:sa].count(b'\0')
        assert s[0]==v[0] in [3,10,180,254] and jp[sa-5:sa+1]==en[at-5:at+1]
        row=deepcopy(glosses[record]);assert row['source_hex']==s.hex();kind='system-FE' if s[0]==254 else 'progressive'
        row.update(id=f'DK4_MES_B97_R{record:04d}',file_path='/data/SC3.DK4',block=97,source_record_index=record,
            source_Japanese=row['Japanese'],source_reference=dict(block=97,offset=sa,bytes=len(s),header_offset=sa-5,record_index=record),
            source_complete_preamble_hex=jp[sa-5:sa+1].hex(),current_reference=dict(offset=at,bytes=len(v),header_offset=at-5),
            current_record_index=en[:at].count(b'\0'),current_hex=v.hex(),source_presentation_prefix_hex=format(s[0],'02x'),
            kind=kind,source_kind=kind,native_command_extent=a['native_extent'],current_native_extent=b['native_extent'],spoken_sequence_index=index,
            current_native_voice_macro_entry_controls_and_context_pending=True,source_prose_or_completion_credit_added=0)
        rows.append(row)
    assert not known&{historical_key(r) for r in rows}
    leaves=[c for c in old if c['word']!=0x4000]
    assert [(c['word'],c['offset']) for c in leaves]==[(0x6000,8),(0x4620,10),(0x633E,14),(0xA000,1750),(0x4820,1884),(0xA000,1888),(0x4700,1896),(0,1898)]
    for a,b in zip(old,now,strict=True):
        if a['word']!=0x4000:assert a['whole_command_hex']==b['whole_command_hex']
    macros={m:sum(bytes.fromhex(r['source_hex']).count(m.encode()) for r in rows) for m in ['FI','FA','FO']};assert macros==dict(FI=0,FA=0,FO=1)
    assert current.read_file('/data/EV3.DK4')==clean.read_file('/data/EV3.DK4')
    terminalpath=Path('work/analysis/current_Maria_context_v4997/terminal.json');terminal=read(terminalpath);rp=Path(terminal['report']);report=read(rp)
    assert terminal['terminal'] and terminal['candidate_sha256']==report['ROM_sha256']==candidate['sha256'] and report['cold_boot'] and not report['savestate_loaded'] and not report['callback_errors']
    assert sha(rp.read_bytes())==terminal['report_sha256'];snap=next(s for s in report['read_only_capture_RAM_snapshots'] if s['frame']==31000)
    assert snap['read_only_export'] and sha(Path(snap['path']).read_bytes())==snap['sha256']
    fixturepath=Path('work/analysis/current_Maria_context_v4997/existing_system_unlock_manifest.json')
    group=dict(block=97,clean_block_sha256=sha(jp),current_block_sha256=sha(en),source_bytes=len(jp),current_bytes=len(en),
        source_header_hex=jp[:4].hex(),current_header_hex=en[:4].hex(),all_clean_native_commands=old,all_current_native_commands=now,
        source_native_commands=old,current_native_commands=now,source_current_native_command_shape_exact=True,records=rows,choices=[],
        physical_speeches=32,source_selectors=[3,10,180,254],source_macro_counts=macros,FE_panels=1,relative_sites=0,
        all_complete_preambles_and_native_command_shapes_equal=True)
    ROOT.mkdir(parents=True);save(ROOT/'all32_clean_current_complete_context.json',dict(format='dk4-editorial-source-context-packet-v1',file_path='/data/SC3.DK4',
        source_ROM='work/clean.nds',source_ROM_sha256=sha(Path('work/clean.nds').read_bytes()),current_ROM=candidate['path'],current_ROM_sha256=candidate['sha256'],
        current_ARM9_sha256=sha(arm),current_COMMON_sha256=sha(current.read_file('/COMMON/MESFILE.DK4')),
        source_SC3_sha256=sha(clean.read_file('/data/SC3.DK4')),current_SC3_sha256=sha(current.read_file('/data/SC3.DK4')),original_EV3_sha256=sha(current.read_file('/data/EV3.DK4')),
        actual_historical_snapshot=snap['path'],actual_historical_snapshot_sha256=snap['sha256'],historical_snapshot_ROM=candidate['path'],
        current_actual_context_capture_report=str(rp),current_actual_context_report_sha256=sha(rp.read_bytes()),current_actual_context_snapshot=snap,
        existing_system_unlock_manifest=str(fixturepath),existing_system_unlock_manifest_sha256=sha(fixturepath.read_bytes()),
        context_is_current_Maria_opening_not_B97_activation=True,no_historical_initialized_RAM_overlay=True,
        blocks=[group],records=rows,typed_choice_records=[],typed_actor_style_records=[],source_macro_counts=macros,
        total_editorial_objects=32,speech_objects=32,ordinary_source_speeches=31,system_FE_panels=1,source_selectors=[3,10,180,254],source_static_actor_selectors=[3,10,180],
        source_native_commands=40,source_A000=2,source_C200=0,source_relative_sites=0,source_predicates=0,
        source_exact_spans=[dict(start=a,end=b,sha256=sha(arm[a:b])) for a,b in spans],source_transcript=str(rawpath),source_transcript_sha256=sha(rawpath.read_bytes()),
        whole_exchange_context_notes=str(GLOSS),whole_exchange_context_notes_sha256=sha(GLOSS.read_bytes()),
        all32_clean_first_glosses_recorded_before_predecessor_comparison=True,source_setup_resource_presentation_and_effect_bodies_unresolved=True,
        evidence={str(p):sha(p.read_bytes()) for p in [PRIOR,GLOSS,rawpath,terminalpath,rp,fixturepath,Path(__file__)]},
        source_prose_or_completion_credit_added=0,new_emulator_runs_in_this_mapping=0,full_goal_complete=False))
    print('Maria B97 bound:32 speeches/40 commands,03/0A/B4/FE,FO1 and exact current Maria-opening snapshot. No credit.')
