"""First current/effective B31/B53 comparison after clean gloss and full source view."""
import struct
from copy import deepcopy
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from scripts.Hodram_B31_B53_registered_route_context_v8781 import RouteCurrentContext
from scripts.inventory_lil_after_crew_items_complete_v3152 import scoped_inventory
from scripts.prove_Maria_story_branches_v7741 import native_skip
from scripts.prove_lil_B139_B140_conditionals_v3461c import probe
from scripts import prove_lil_shrines_temples_controls_v3168c as inherited
from scripts.reconcile_contextual_mood_retentions_v2482 import historical_key
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/Hodram_B54_B60_current_v8799')
GLOSS=Path('work/analysis/Hodram_next_clean_gloss_v8787/82_qualified_clean_glosses_no_unbound_gender_orFA_type.json')
DISPLAY=Path('work/analysis/Hodram_B54_B60_source_display_v8794/82_complete_source_dispatches_alignments_pages_andmacro_binding.json')
VIEW=Path('work/analysis/Hodram_B54_B60_source_review_v8798b/source_context_names_display_review_before_current_English.json')
CONTROL=Path('work/analysis/Hodram_B54_B60_source_controls_v8791/source_controls.json')
NAMES=Path('work/analysis/Hodram_B54_B60_names_v8792/ten_source_identities_current_getters_voices_andplanes.json')
INPUT=Path('work/analysis/current_V8778_Hodram_native_v8781/current_native_input.json')
HANDOFF=Path('work/analysis/editorial_handoff_verification_v8790/verified_handoff.json')
if __name__=='__main__':
    assert not ROOT.exists();gloss,display,view,control,names,inp,verified=map(read,[GLOSS,DISPLAY,VIEW,CONTROL,NAMES,INPUT,HANDOFF])
    ledgerpath=Path('translations/editorial_review_current_v1.json');assert sha(ledgerpath.read_bytes())==verified['ledger_sha256'] and verified['completed']==7237
    assert view['all82_source_native_pages_and11_sheets_directly_viewed'] and view['existing_B54_B60_English_dialogue_bodies_still_unconsulted']
    assert view['source_ready_for_current_English_comparison_not_final_localization_orformatting_approval']
    assert gloss['all82_clean_utterances_andseven_complete_blocks_read_before_earlier_English'] and control['source_gloss_sha256']==display['evidence'][str(GLOSS)]==sha(GLOSS.read_bytes())
    assert view['evidence'][DISPLAY.as_posix()]==sha(DISPLAY.read_bytes())
    for sheet in view['viewed_sheets']:assert sha(Path(sheet['path']).read_bytes())==sheet['sha256']
    image=NdsImage.open(inp['current_ROM']);assert sha(Path(inp['current_ROM']).read_bytes())==inp['current_ROM_sha256']==verified['candidate_sha256']==display['candidate_sha256']
    arm=image.read_file('/__arm9__.bin');archive=image.read_file('/data/SC1.DK4');bank=IlnkContainer.parse(archive).blocks
    inventory,walker,fn=scoped_inventory();ROOT.mkdir(parents=True);ctx=RouteCurrentContext(INPUT,'unused-no-historical-ROM',ROOT/'current_context')
    ns={**inherited.__dict__,'SOURCE':INPUT,'route':1,'route_mask':2,'CATALOG_LOOKUP':{}}
    for key,text in display['source_owned_dispatch_adapters'].items():exec(compile(text,__file__+'::'+key,'exec'),ns)
    ns['CATALOG_LOOKUP'],catalogue=ns['bind_current_catalog'](image)
    exec(compile(display['source_owned_macro_body_adapter'],__file__+'::measured-captain1-defaults','exec'),ns)
    voices={r['source_selector']:r['original_voice_class'] for r in names['ten_source_selector_voices']['rows']}
    rows=[];groups=[];dispatches=[];relative_cases=[];query_cases=[]
    for source in gloss['groups']:
        number=source['block'];block=bank[number];clean=bytes.fromhex(source['clean_block_hex']);commands,speeches=inventory(arm,block)
        assert len(commands)==len(source['commands']) and len(speeches)==len(source['records'])
        logical=8+int.from_bytes(block[4:6],'little');assert commands[-1]['word']==0 and commands[-1]['offset']+4==logical and not any(block[logical:])
        mapping={a['offset']:b['offset'] for a,b in zip(source['commands'],commands,strict=True)};mapping[source['clean_logical_end']]=logical
        pairs=[];relmaps=[]
        for a,b in zip(source['commands'],commands,strict=True):
            assert a['word']==b['word'] and [mapping[x] for x in a['ancestor_0100_offsets']]==b['ancestor_0100_offsets']
            av,bv=bytes.fromhex(a['whole_command_hex']),bytes.fromhex(b['whole_command_hex']);word=a['word']
            if word==0x4000:assert av[:6]==bv[:6];kind='speech'
            elif word in [0x100,0x200,0x300,0x400]:
                sa,ca=[struct.unpack_from('<H',v,2)[0] for v in [av,bv]];st=a['offset']+4+sa;ct=b['offset']+4+ca
                assert mapping[st]==ct and mapping[a['offset']+4]==b['offset']+4
                relmaps.append(dict(source_offset=a['offset'],current_offset=b['offset'],word=word,source_span=sa,current_span=ca,source_skip_target=st,current_skip_target=ct))
                relative_cases.append(dict(block=number,version='current',**ctx.execute(native_skip,block,b)));ctx.machines.pop();kind='relative'
            else:
                assert av==bv;kind='opaque-query-or-terminal'
                if word==0x8000:query_cases.append(dict(block=number,version='current',**ctx.execute(probe,block,b)));ctx.machines.pop()
            pairs.append(dict(word=word,kind=kind,source_offset=a['offset'],current_offset=b['offset'],source_extent=a['native_extent'],current_extent=b['native_extent'],source_hex=av.hex(),current_hex=bv.hex(),bytes_equal=av==bv))
        grows=[]
        for original,command in zip(source['records'],speeches,strict=True):
            at=command['offset']+5;raw=block[at:block.index(0,at+1)];prefix=raw[0]
            assert prefix==original['source_selector'] and block[at-5:at+1].hex()==original['source_complete_preamble_hex']
            result=ctx.execute(ns['dispatch'],prefix,raw[1:]);ctx.machines.pop();is_FE=prefix==254
            assert result['resolved_actor_ID']==(None if is_FE else prefix) and result['source_voice_class']==(None if is_FE else voices[prefix])
            assert bool(result['FE_original_null_actor_calls'])==is_FE
            selected=ns['CATALOG_LOOKUP'].get(raw[1:]);template=selected['target'] if selected else raw[1:]
            expanded=template.replace(b'FI',b'Hodram').replace(b'FA',b'Bergstrom').replace(b'FO',b'Bergstrom Fleet')
            boundary=next(q for q in result['boundaries'] if q['kind']==('unexecuted-FE-modal-body' if is_FE else 'unexecuted-progressive-body'));assert boundary['text_hex']==expanded.hex()
            previous=next(r for r in display['records'] if r['id']==original['id']);assert previous['source_hex']==original['source_hex']
            row=deepcopy(original);row.update(kind='system-FE' if is_FE else 'progressive',source_kind='system-FE' if is_FE else 'progressive',current_reference=dict(file_path='/data/SC1.DK4',block=number,offset=at,bytes=len(raw),header_offset=at-5,record_index=block[:at].count(b'\0')),
                current_hex=raw.hex(),current_record_index=block[:at].count(b'\0'),current_native_extent=command['native_extent'],current_0100_ancestors=command['ancestor_0100_offsets'],
                current_raw_storage_English=raw[1:].decode('cp932'),raw_storage_comparison_paragraph=' '.join(raw[1:].decode('cp932').split()),
                effective_predecessor_template_hex=template.hex(),effective_predecessor_paragraph=' '.join(template.decode('cp932').split()),current_actual_default_expanded_hex=expanded.hex(),
                registered_catalogue_match=result['registered_catalog_match'],current_English_body_unread=False,current_English_dialogue_still_unconsulted=False,current_English_dialogue_still_unread=False,
                current_English_body_now_exposed=True,source_prose_orcompletion_credit_added=False,current_contextual_prose_formatting_actual_andrelease_pending=True)
            grows.append(row);rows.append(row);dispatches.append(dict(id=row['id'],current_fresh=result,source_reused_exact_same_own_context=previous['original_dispatch']))
        groups.append(dict(block=number,file_path='/data/SC1.DK4',clean_block_hex=clean.hex(),clean_block_sha256=sha(clean),source_header_hex=clean[:8].hex(),current_block_hex=block.hex(),current_block_sha256=sha(block),current_header_hex=block[:8].hex(),
            current_stored_bytes=len(block),current_logical_end=logical,current_tail_bytes=len(block)-logical,all_source_commands=source['commands'],all_current_commands=commands,all_command_reference_pairs=pairs,relative_operand_maps=relmaps,source_event_records=source['source_event_records'],records=grows))
    ledger=read(ledgerpath);completed={historical_key(r) for f in ledger['completed_editorial_families'] for r in f['records']};keys={historical_key(r) for r in rows}
    assert len(rows)==len(keys)==82 and len(completed)==7237 and not completed&keys and len(relative_cases)==24 and len(query_cases)==6 and not ctx.machines
    save(ROOT/'current_effective.json',dict(current_ROM=inp['current_ROM'],current_ROM_sha256=inp['current_ROM_sha256'],current_ARM9_sha256=sha(arm),current_COMMON_sha256=sha(image.read_file('/COMMON/MESFILE.DK4')),current_archive_sha256=sha(archive),
        file_path='/data/SC1.DK4',groups=groups,records=rows,source_current_dispatches=dispatches,current_relative_cases=relative_cases,current_query_cases=query_cases,
        source_first_glosses_andcomplete_native_page_view_precede_current_English=True,all82_source_units_uncredited_in_current_ledger=True,
        complete152commands82preambles24relative_targets6queries33nonprose_controls_and7normal_ends_bound=True,
        source_gloss=str(GLOSS),source_gloss_sha256=sha(GLOSS.read_bytes()),source_native_display=str(DISPLAY),source_native_display_sha256=sha(DISPLAY.read_bytes()),source_native_view=str(VIEW),source_native_view_sha256=sha(VIEW.read_bytes()),
        source_controls=str(CONTROL),source_controls_sha256=sha(CONTROL.read_bytes()),registered_current_catalogue_binding=catalogue,
        source_native_calls_reused_exact_same_own8778_context_not_replayed=True,Geronimo_Alonso_shared_de_middle_field_finding_remains_open=True,
        current_comparison_not_English_editorial_native_display_actual_orrelease_approval=True,
        current_native_input=str(INPUT),native_context_plan=str(ctx.proof_path),native_context_plan_sha256=sha(ctx.proof_path.read_bytes()),inventory_walker=walker,inventory_function=fn,
        no_ROM_write_orledger_credit=True,new_credit=0,new_emulator_runs=0,full_goal_complete=False,
        evidence={str(p):sha(p.read_bytes()) for p in [GLOSS,DISPLAY,VIEW,CONTROL,NAMES,INPUT,HANDOFF,Path(__file__)]}))
    for row in rows:print(row['id'],repr(row['effective_predecessor_paragraph']),'catalogue',row['registered_catalogue_match'])
    print('First current comparison:82fresh dispatches/120relative cases/6unforcedqueries;152commands fully mapped;no editorial approval orcredit.')
