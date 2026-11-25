"""Compare exact current/effective English only after six complete clean-first glosses/source view."""
from copy import deepcopy
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from scripts.Hodram_registered_route_context_v8303 import RouteCurrentContext
from scripts.inventory_lil_after_crew_items_complete_v3152 import scoped_inventory
from scripts import prove_lil_shrines_temples_controls_v3168c as inherited
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/Hodram_B47_B48_current_v8317c')
GLOSS=Path('work/analysis/Hodram_B47_B48_clean_gloss_v8312/six_first_clean_glosses_both_race_outcomes_FE_FI_andAmsterdam_wait_direction.json')
DISPLAY=Path('work/analysis/Hodram_B47_B48_source_display_v8316b/six_source_dispatches24_macro_alignments_five_progressive_one_FE_pages_Lil_identity_reuse.json')
CONTROLS=Path('work/analysis/Hodram_B47_B48_source_controls_v8314/two_EV1_entries15_commands6_preambles7_opaque_effect_pairs50_complete_seeded_ends.json')
INPUT=Path('work/analysis/current_V8300_Hodram_native_v8303/current_native_input.json')

if __name__=='__main__':
    assert not ROOT.exists();gloss,display,controls,inp=map(read,[GLOSS,DISPLAY,CONTROLS,INPUT])
    assert display['current_English_dialogue_bodies_unconsulted'] and controls['current_English_dialogue_bodies_still_unconsulted']
    assert display['source_gloss_sha256']==controls['source_gloss_sha256']==sha(GLOSS.read_bytes())
    sheet=display['review_sheet'];assert sha(Path(sheet['path']).read_bytes())==sheet['sha256']
    ledger=read('translations/editorial_review_current_v1.json');assert ledger['records_editorially_completed']==7199 and not ledger['full_goal_complete']
    image=NdsImage.open(inp['current_ROM']);assert sha(Path(inp['current_ROM']).read_bytes())==inp['current_ROM_sha256']==display['candidate_sha256']
    arm=image.read_file('/__arm9__.bin');archive=image.read_file('/data/SC1.DK4');bank=IlnkContainer.parse(archive).blocks
    inventory,walker,fn=scoped_inventory();ROOT.mkdir(parents=True);ctx=RouteCurrentContext(INPUT,'unused-no-historical-ROM',ROOT/'current_context')
    ns={**inherited.__dict__,'SOURCE':INPUT,'route':1,'route_mask':2,'CATALOG_LOOKUP':{}}
    for key,text in display['source_owned_dispatch_adapters'].items():exec(compile(text,__file__+'::'+key,'exec'),ns)
    ns['CATALOG_LOOKUP'],catalogue=ns['bind_current_catalog'](image)
    exec(compile(display['source_owned_macro_body_adapter'],__file__+'::measured-current-Hodram-defaults','exec'),ns)
    rows=[];groups=[];cases=[]
    for source in gloss['groups']:
        number=source['block'];block=bank[number];clean=bytes.fromhex(source['clean_block_hex']);commands,speeches=inventory(arm,block)
        assert [c['word'] for c in commands]==[c['word'] for c in source['commands']] and len(speeches)==3
        logical=8+int.from_bytes(block[4:6],'little');assert commands[-1]['offset']+4==logical and block[logical:]==bytes(len(block)-logical)
        pairs=[]
        for a,b in zip(source['commands'],commands,strict=True):
            av=clean[a['offset']:a['offset']+a['native_extent']];bv=block[b['offset']:b['offset']+b['native_extent']]
            if a['word']!=0x4000:assert av==bv
            pairs.append(dict(word=a['word'],source_offset=a['offset'],current_offset=b['offset'],source_extent=a['native_extent'],current_extent=b['native_extent'],source_hex=av.hex(),current_hex=bv.hex(),bytes_equal=av==bv))
        for original,command in zip(source['records'],speeches,strict=True):
            at=command['offset']+5;raw=block[at:block.index(0,at+1)];is_FE=raw[0]==254
            assert raw[0]==original['source_selector'] and block[at-5:at+1].hex()==original['source_complete_preamble_hex']
            result=ctx.execute(ns['dispatch'],raw[0],raw[1:]);ctx.machines.pop()
            assert result['resolved_actor_ID']==(None if is_FE else 2) and result['source_voice_class']==(None if is_FE else 3)
            boundary=next(b for b in result['boundaries'] if b['kind']==('unexecuted-FE-modal-body' if is_FE else 'unexecuted-progressive-body'))
            selected=ns['CATALOG_LOOKUP'].get(raw[1:]);template=selected['target'] if selected else raw[1:];expanded=template.replace(b'FI',b'Hodram').replace(b'FA',b'Bergstrom').replace(b'FO',b'Bergstrom Fleet')
            assert boundary['text_hex']==expanded.hex()
            if is_FE:assert len(result['FE_original_null_actor_calls'])==1 and result['FE_original_null_actor_calls'][0]['args'][2]==0
            row=deepcopy(original);row.update(kind='system-FE' if is_FE else 'progressive',source_kind='system-FE' if is_FE else 'progressive',
                current_reference=dict(file_path='/data/SC1.DK4',block=number,offset=at,bytes=len(raw),header_offset=at-5,record_index=block[:at].count(b'\0')),current_hex=raw.hex(),current_record_index=block[:at].count(b'\0'),current_native_extent=command['native_extent'],current_0100_ancestors=command['ancestor_0100_offsets'],
                current_raw_storage_English=raw[1:].decode('cp932'),raw_storage_comparison_paragraph=' '.join(raw[1:].decode('cp932').split()),
                effective_predecessor_template_hex=template.hex(),effective_predecessor_paragraph=' '.join(template.decode('cp932').split()),current_actual_default_expanded_hex=expanded.hex(),registered_catalogue_match=result['registered_catalog_match'],
                current_English_body_unread=False,current_English_dialogue_body_not_yet_consulted=False,current_English_dialogue_body_now_exposed=True,
                current_effective_body_dispatch_andcatalogue_pending=False,source_presentation_consumer_not_yet_approved=False,source_native_dispatch_andcomplete_original_page_bound_offline=True,
                source_prose_orcompletion_credit_added=False,prose_formatting_actual_effects_andregistered_release_pending=True)
            rows.append(row);cases.append(dict(id=row['id'],file_path=row['file_path'],version='current-English',**result))
        groups.append(dict(block=number,file_path='/data/SC1.DK4',clean_block_hex=clean.hex(),clean_block_sha256=sha(clean),current_block_hex=block.hex(),current_block_sha256=sha(block),
            current_stored_bytes=len(block),current_logical_end=logical,current_tail_bytes=len(block)-logical,all_source_commands=source['commands'],all_current_commands=commands,all_command_reference_pairs=pairs,source_event_records=source['source_event_records']))
    assert len(rows)==6 and len(cases)==6 and not ctx.machines
    save(ROOT/'six_exact_source_current_effective_refs_after_whole_clean_gloss_andnative_source_view.json',dict(current_ROM=inp['current_ROM'],current_ROM_sha256=inp['current_ROM_sha256'],current_ARM9_sha256=sha(arm),current_COMMON_sha256=sha(image.read_file('/COMMON/MESFILE.DK4')),current_archive_sha256=sha(archive),file_path='/data/SC1.DK4',records=rows,groups=groups,
        all_six_clean_first_whole_exchange_glosses_precede_current_English_exposure=True,source_six_page_sheet_directly_viewed=sheet,
        source_gloss=str(GLOSS),source_gloss_sha256=sha(GLOSS.read_bytes()),source_display_proof=str(DISPLAY),source_display_proof_sha256=sha(DISPLAY.read_bytes()),source_controls_proof=str(CONTROLS),source_controls_proof_sha256=sha(CONTROLS.read_bytes()),
        source_dispatches=display['records'],current_dispatches=cases,registered_current_catalogue_binding=catalogue,all_original_nonspeech_effect_bytes_andcomplete_terminals_exact=True,
        raw_andruntime_comparison_not_English_editorial_approval=True,source_FE_actual_geometry_palette_name_transition_effects_andsource_prose_formatting_release_pending=True,
        current_native_input=str(INPUT),native_context_plan=str(ctx.proof_path),native_context_plan_sha256=sha(ctx.proof_path.read_bytes()),
        no_ROM_write_orledger_credit=True,new_credit=0,new_emulator_runs=0,full_goal_complete=False,evidence={str(p):sha(p.read_bytes()) for p in [GLOSS,DISPLAY,CONTROLS,INPUT,Path(__file__)]}))
    for row in rows:print(row['id'],repr(row['effective_predecessor_paragraph']), 'catalogue',row['registered_catalogue_match'])
