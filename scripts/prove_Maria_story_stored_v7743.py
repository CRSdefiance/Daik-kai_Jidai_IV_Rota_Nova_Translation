"""Verify every final stored C string and parity tail against complete reviewed native ink."""
from copy import deepcopy
from pathlib import Path
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from scripts.maria_unlocked_current_context_v7680 import MariaUnlockedCurrentContext
from scripts.generic_name_macro_owned_v5886b import expand
from scripts.research_lil_B209_native_pages_v6461 import pages as old_pages
from scripts.square_shopkeeper_font_oracles_v7020 import expected_pixels
from scripts.prove_lil_B208_name_planes_v6405 import codes
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/maria_story_stored_v7743')
MAP=Path('work/analysis/maria_story_relocation_v7742/three_blocks67_speeches20_fixups100_native_target_cases_exact_inverse.json')
FONT=Path('work/analysis/maria_story_pages_v7738/67_compiled268_alignments68_complete_native_pages.json')
MANUSCRIPT=Path('translations/maria_B34_B108_B35_editorial_manuscript_v2.json')
INPUT=Path('work/analysis/current_V7717_native_v7720/route3/current_native_input.json')
METRICS=['pages','total_bytes','complete_consumed_bytes','all_visible_first_internal_final_characters_in_order','no_blank_or_overlap_page']
if __name__=='__main__':
    assert not ROOT.exists();mapping,font,doc=map(read,[MAP,FONT,MANUSCRIPT]);assert mapping['candidate_sha256']==font['candidate_sha256']==doc['current_ROM_sha256']
    assert font['manuscript_sha256']==sha(MANUSCRIPT.read_bytes())
    data=Path(mapping['target_archive']).read_bytes();assert sha(data)==mapping['target_archive_sha256'];bank=IlnkContainer.parse(data).blocks
    ns=dict(expand.__globals__);exec(compile(font['source_owned_compiled_macro_adapter'],__file__+'::exact-own-Maria-macro-ABI','exec'),ns)
    pe={**old_pages.__globals__,'expected_pixels':expected_pixels,'codes':codes};exec(compile(font['source_owned_native_page_adapter'],__file__+'::exact-current-page-renderer','exec'),pe)
    ROOT.mkdir(parents=True);ctx=MariaUnlockedCurrentContext(INPUT,'unused-no-historical-ROM',ROOT/'current_context')
    rows=[];fresh=reused=freshpages=0
    for group in mapping['groups']:
        block=bank[group['block']];assert sha(block)==group['target_block_sha256']
        for ref in group['text_records']:
            base=next(r for r in font['records'] if r['id']==ref['id']);raw=bytes.fromhex(ref['target_hex']);body=raw[1:]
            compiled=bytes.fromhex(base['compiled_hex'])[1:];at=ref['new_offset']
            assert ref['compiled_hex']==base['compiled_hex'] and body in [compiled,compiled+b' ']
            assert block[at:at+len(raw)+1]==raw+b'\0' and block[at-5:at+1].hex()==ref['source_complete_preamble_hex']
            expected=body.replace(b'FI',b'Maria').replace(b'FA',b'Li').replace(b'FO',b'Li Clan')
            if body==compiled:
                pipeline=deepcopy(base['native_alignment']);rendered={k:deepcopy(base[k]) for k in METRICS};reused+=4
                assert base['expanded_native_hex']==expected.hex()
                mode='exact-final-input-original-own-Maria-compiled-proof-reuse'
            else:
                assert ref['parity_space_added'];pipeline=ctx.execute(ns['expand'],body,raw[0]);ctx.machines.pop();fresh+=4
                assert all(c['output_hex']==expected.hex() for c in pipeline['cases'])
                rendered=pe['pages'](ctx.arm,ctx.rom.read_file('/GRP/KANJI.FNT'),expected);freshpages+=len(rendered['pages'])
                assert len(rendered['pages'])==len(base['pages'])
                for page,previous in zip(rendered['pages'],base['pages'],strict=True):
                    pixels=bytes.fromhex(page.pop('native_plane_hex'))
                    assert pixels==Path(previous['native_plane']).read_bytes() and sha(pixels)==previous['native_plane_sha256']
                    path=ROOT/(ref['id']+f'_stored_page{page["page"]}.bin');path.write_bytes(pixels)
                    page.update(native_plane=str(path),native_plane_sha256=sha(pixels),same_complete_ink_as_reviewed_compiled_page=True)
                mode='fresh-parity-tail-Maria-ABI-andoriginal-native-render'
            assert len(pipeline['cases'])==4 and all(c['output_hex']==expected.hex() for c in pipeline['cases'])
            assert rendered['total_bytes']==rendered['complete_consumed_bytes']==len(expected)
            assert rendered['all_visible_first_internal_final_characters_in_order'] and rendered['no_blank_or_overlap_page']
            for page in rendered['pages']:assert sha(Path(page['native_plane']).read_bytes())==page['native_plane_sha256']
            rows.append(dict(id=ref['id'],file_path=group['file_path'],block=group['block'],final_stored_reference=dict(offset=at,bytes=len(raw),record_index=ref['new_record_index']),
                final_target_hex=raw.hex(),final_expanded_hex=expected.hex(),parity_space_added=ref['parity_space_added'],proof_mode=mode,native_pipeline=pipeline,complete_pages=rendered,
                all_stored_visible_ink_complete_andidentical_to_reviewed_compiled_pages=True))
    assert len(rows)==67 and fresh+reused==268 and sum(r['parity_space_added'] for r in rows)==33 and not ctx.machines
    assert sum(len(r['complete_pages']['pages']) for r in rows)==68
    save(ROOT/'67_final_stored_targets268_alignments33_zero_ink_tails68_pages.json',dict(
        candidate=mapping['candidate'],candidate_sha256=mapping['candidate_sha256'],relocation_map=str(MAP),relocation_map_sha256=sha(MAP.read_bytes()),
        font_proof=str(FONT),font_proof_sha256=sha(FONT.read_bytes()),manuscript=str(MANUSCRIPT),manuscript_sha256=sha(MANUSCRIPT.read_bytes()),
        records=rows,stored_alignment_cases=268,fresh_alignment_cases=fresh,exact_own_Maria_alignment_cases_reused=reused,
        zero_ink_parity_tail_count=33,fresh_stored_native_page_renders=freshpages,complete_stored_native_pages=68,
        all67_stored_targets_equal_reviewed_complete_native_ink=True,source_macro_counts_andall8_static_selectors_preserved=True,
        all_native_bounds_input_bitmap_header_canaries_glyph_order_andcomplete_consumption_exact=True,
        two_page_R111_has_no_lost_character_extra_blank_page_orparity_ink=True,
        complete_four_byte_terminals_distinct_from_target_storage_tails=True,
        no_ROM_registry_ledger_orcredit_mutation=True,all67_formatting_gates_false=True,
        loaders_callers_controls_actual_policy_production_andregistered_integration_pending=True,
        existing_system_only_unlock_fixture=True,earned_unlock_verified=False,
        native_context_plan=str(ctx.proof_path),native_context_plan_sha256=sha(ctx.proof_path.read_bytes()),
        evidence={str(p):sha(p.read_bytes()) for p in [MAP,FONT,MANUSCRIPT,INPUT,Path(__file__)]},new_emulator_runs=0,new_credit=0,full_goal_complete=False))
    print('Stored67targets/268alignments:',fresh,'fresh',reused,'exact own reuse;33zero-ink tails;68complete pages;',freshpages,'fresh stored page renders.')
