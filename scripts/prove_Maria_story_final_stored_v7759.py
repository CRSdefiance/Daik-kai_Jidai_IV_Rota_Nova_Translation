"""Finalv3 stored strings:reuse65 exact proofs andcheck onlytwo changed native dispatches."""
from copy import deepcopy
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from scripts.maria_unlocked_current_context_v7680 import MariaUnlockedCurrentContext
from scripts.generic_name_macro_owned_v5886b import expand
from scripts.research_lil_B209_native_pages_v6461 import pages as old_pages
from scripts.square_shopkeeper_font_oracles_v7020 import expected_pixels
from scripts.prove_lil_B208_name_planes_v6405 import codes
from scripts import prove_lil_shrines_temples_controls_v3168c as inherited
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/maria_story_final_stored_v7759')
MAP=Path('work/analysis/maria_story_final_relocation_v7758/three_blocks67_speeches20_fixups100_native_target_cases_exact_inverse.json')
FONT=Path('work/analysis/maria_story_final_native_v7757b/67_final_v3_native_pages_andfully_bound_logical_lineage.json')
PRIOR=Path('work/analysis/maria_story_stored_v7743/67_final_stored_targets268_alignments33_zero_ink_tails68_pages.json')
CONTROLS=Path('work/analysis/maria_story_final_controls_v7745/67_final_dispatches_numeric_leaves_opaque_controls_resources_pause_C200_ends.json')
CONSUMERS=Path('work/analysis/maria_story_effective_v7729/all67_effective_English_templates134_original_dispatches.json')
CURRENT=Path('work/analysis/maria_story_current_v7728/all67_complete_source_current_refs_before_new_English_manuscript.json')
INPUT=Path('work/analysis/current_V7717_native_v7720/route3/current_native_input.json')
METRICS=['pages','total_bytes','complete_consumed_bytes','all_visible_first_internal_final_characters_in_order','no_blank_or_overlap_page']
if __name__=='__main__':
    assert not ROOT.exists();mapping,font,prior,controls,consumers=map(read,[MAP,FONT,PRIOR,CONTROLS,CONSUMERS])
    assert mapping['candidate_sha256']==font['candidate_sha256']==prior['candidate_sha256']==controls['candidate_sha256']
    data=Path(mapping['target_archive']).read_bytes();assert sha(data)==mapping['target_archive_sha256'];bank=IlnkContainer.parse(data).blocks
    ns=dict(expand.__globals__);exec(compile(font['source_owned_compiled_macro_adapter'],__file__+'::same-own-Maria-ABI','exec'),ns)
    pe={**old_pages.__globals__,'expected_pixels':expected_pixels,'codes':codes};exec(compile(font['source_owned_native_page_adapter'],__file__+'::same-native216-page-renderer','exec'),pe)
    de={**inherited.__dict__,'SOURCE':CURRENT,'route':3,'route_mask':8,'CATALOG_LOOKUP':{}}
    for name,text in consumers['source_owned_dispatch_adapters'].items():exec(compile(text,__file__+'::'+name,'exec'),de)
    exec(compile(consumers['source_owned_measured_macro_body_adapter'],__file__+'::actual-Maria-macros','exec'),de)
    de['CATALOG_LOOKUP'],catalogue=de['bind_current_catalog'](NdsImage.open(mapping['candidate']))
    ROOT.mkdir(parents=True);ctx=MariaUnlockedCurrentContext(INPUT,'unused-no-historical-ROM',ROOT/'current_context')
    rows=[];dispatches=[];fresh=compiledreuse=oldreuse=freshpages=0
    for group in mapping['groups']:
        block=bank[group['block']];assert sha(block)==group['target_block_sha256']
        for ref in group['text_records']:
            before=next(r for r in prior['records'] if r['id']==ref['id']);base=next(r for r in font['records'] if r['id']==ref['id'])
            raw=bytes.fromhex(ref['target_hex']);body=raw[1:];at=ref['new_offset'];compiled=bytes.fromhex(base['compiled_hex'])[1:]
            assert block[at:at+len(raw)+1]==raw+b'\0' and block[at-5:at+1].hex()==ref['source_complete_preamble_hex']
            assert body in [compiled,compiled+b' ']
            expected=body.replace(b'FI',b'Maria').replace(b'FA',b'Li').replace(b'FO',b'Li Clan')
            if raw.hex()==before['final_target_hex']:
                assert ref['id'] not in font['changed_record_IDs']
                pipeline=deepcopy(before['native_pipeline']);rendered=deepcopy(before['complete_pages']);oldreuse+=4
                mode='exact-original-own-current-final-stored-body-selector-andall-four-alignments-reuse'
                oldcase=next(r for r in controls['final_dispatches'] if r['id']==ref['id'])
                assert oldcase['final_stored_hex']==raw.hex() and oldcase['source_selector']==raw[0]
                dispatched=deepcopy(oldcase);dispatched.update(previous_stored_control_proof=str(CONTROLS),previous_stored_control_proof_sha256=sha(CONTROLS.read_bytes()),
                    historical_final_offset=oldcase['final_offset'],final_offset=at,exact_stored_body_reuse_not_old_offset_reuse=True)
            else:
                assert ref['id'] in font['changed_record_IDs']
                if body==compiled:
                    pipeline=deepcopy(base['native_alignment']);rendered={k:deepcopy(base[k]) for k in METRICS};compiledreuse+=4
                    mode='exact-new-final-compiled-body-native-alignment-andpage-reuse'
                else:
                    pipeline=ctx.execute(ns['expand'],body,raw[0]);ctx.machines.pop();fresh+=4
                    assert all(c['output_hex']==expected.hex() for c in pipeline['cases'])
                    rendered=pe['pages'](ctx.arm,ctx.rom.read_file('/GRP/KANJI.FNT'),expected);freshpages+=len(rendered['pages'])
                    assert len(rendered['pages'])==len(base['pages'])==1
                    for page,original in zip(rendered['pages'],base['pages'],strict=True):
                        pixels=bytes.fromhex(page.pop('native_plane_hex'));assert pixels==Path(original['native_plane']).read_bytes()
                        path=ROOT/(ref['id']+'_final_stored_page1.bin');path.write_bytes(pixels)
                        page.update(native_plane=str(path),native_plane_sha256=sha(pixels),same_complete_ink_as_final_v3_compiled_page=True)
                    mode='fresh-final-parity-tail-native-ABI-andpage'
                dispatched=ctx.execute(de['dispatch'],raw[0],body);ctx.machines.pop()
                assert dispatched['registered_catalog_match'] is None and dispatched['resolved_actor_ID']==raw[0]
                assert next(b for b in dispatched['boundaries'] if b['kind']=='unexecuted-progressive-body')['text_hex']==expected.hex()
                dispatched.update(id=ref['id'],file_path=group['file_path'],final_offset=at,final_stored_hex=raw.hex(),fresh_final_v3_dispatch=True)
            assert len(pipeline['cases'])==4 and all(c['output_hex']==expected.hex() for c in pipeline['cases'])
            assert rendered['total_bytes']==rendered['complete_consumed_bytes']==len(expected) and len(rendered['pages'])==1
            for page in rendered['pages']:assert sha(Path(page['native_plane']).read_bytes())==page['native_plane_sha256']
            dispatches.append(dispatched);rows.append(dict(id=ref['id'],file_path=group['file_path'],block=group['block'],final_stored_reference=dict(offset=at,bytes=len(raw),record_index=ref['new_record_index']),
                final_target_hex=raw.hex(),final_expanded_hex=expected.hex(),parity_space_added=ref['parity_space_added'],proof_mode=mode,native_pipeline=pipeline,complete_pages=rendered))
    assert len(rows)==len(dispatches)==67 and oldreuse==260 and fresh+compiledreuse+oldreuse==268 and not ctx.machines
    assert sum(r['parity_space_added'] for r in rows)==33
    save(ROOT/'67_final_v3_stored_pages33_tails_two_new_dispatches65_exact_reuse.json',dict(
        candidate=mapping['candidate'],candidate_sha256=mapping['candidate_sha256'],relocation_map=str(MAP),relocation_map_sha256=sha(MAP.read_bytes()),
        font_proof=str(FONT),font_proof_sha256=sha(FONT.read_bytes()),records=rows,final_dispatches=dispatches,current_registered_catalogue_binding=catalogue,
        fresh_stored_alignment_cases=fresh,new_compiled_alignment_cases_exact_reused=compiledreuse,previous_unchanged_stored_alignment_cases_reused=oldreuse,
        stored_alignment_coverage=268,zero_ink_parity_tails=33,final_complete_native_pages=67,fresh_stored_page_renders=freshpages,
        fresh_final_native_dispatches=2,exact_previous_dispatches_reused=65,
        all67_final_stored_targets_equal_reviewed_complete_native_ink=True,all67_final_dispatches_no_catalogue_override=True,
        source_codes_macros_preambles_glyphs_bounds_canaries_consumption_andall_single_pages_preserved=True,
        previous_v2_native_actual_two_page_andall_three_source_captures_preserved=True,
        final_v3_affected_English_B34_B108_actual_captures_andnew_reference_loaders_still_pending=True,
        no_new_ROM_ledger_registry_orcredit_change=True,all67_formatting_gates_false=True,
        existing_system_only_unlock_fixture=True,earned_unlock_verified=False,
        native_context_plan=str(ctx.proof_path),native_context_plan_sha256=sha(ctx.proof_path.read_bytes()),
        evidence={str(p):sha(p.read_bytes()) for p in [MAP,FONT,PRIOR,CONTROLS,CONSUMERS,CURRENT,INPUT,Path(__file__)]},new_credit=0,new_emulator_runs=0,full_goal_complete=False))
    print('v3stored67 single pages/33zero-ink tails;alignment cases',fresh,'fresh',compiledreuse,'newcompiled exact',oldreuse,'unchanged stored exact;2fresh dispatches65exact reuse.Affected English actual/release pending.')
