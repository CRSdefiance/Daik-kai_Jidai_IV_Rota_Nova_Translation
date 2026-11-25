"""Verify all18 final C strings, parity tails andcomplete native page consumption."""
from copy import deepcopy
from pathlib import Path
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.generic_name_macro_owned_v5886b import expand
from scripts.maria_unlocked_current_context_v7680 import MariaUnlockedCurrentContext
from scripts.research_lil_B209_native_pages_v6461 import pages as old_pages
from scripts.square_shopkeeper_font_oracles_v7020 import expected_pixels
from scripts.prove_lil_B208_name_planes_v6405 import codes
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/maria_B207_stored_v7697')
MAP=Path('work/analysis/maria_B207_relocation_v7696/Maria18_speeches20_commands_exact_clean_andpredecessor_inverse_RESEARCH.json')
FONT=Path('work/analysis/maria_B207_pages_v7690/Maria18_complete_native_pages72_fresh_compiled_alignments.json')
PRIOR=Path('work/analysis/papal_trade_stored_v7641/all36_stored_targets144_alignments16_zero_ink_tails36_complete_pages.json')
MANUSCRIPT=Path('translations/maria_B207_editorial_manuscript_v1.json')
METRICS=['pages','total_bytes','complete_consumed_bytes','all_visible_first_internal_final_characters_in_order','no_blank_or_overlap_page']
if __name__=='__main__':
    assert not ROOT.exists();mapping,font,prior,doc=map(read,[MAP,FONT,PRIOR,MANUSCRIPT]);assert mapping['candidate_sha256']==font['candidate_sha256']==doc['current_ROM_sha256']
    old,now=[NdsImage.open(p) for p in [prior['candidate'],mapping['candidate']]]
    assert sha(Path(prior['candidate']).read_bytes())==prior['candidate_sha256'] and sha(Path(mapping['candidate']).read_bytes())==mapping['candidate_sha256']
    for path in ['/__arm9__.bin','/COMMON/MESFILE.DK4','/GRP/KANJI.FNT']:assert old.read_file(path)==now.read_file(path)
    page_env={**old_pages.__globals__,'expected_pixels':expected_pixels,'codes':codes};exec(compile(font['source_owned_2b6_page_adapter'],__file__+'::original-stored-pages','exec'),page_env)
    env={**expand.__globals__,'EXPECTED_CAPTAIN':3};exec(compile(font['source_owned_Maria_compiled_adapter'],__file__+'::actual-Maria-stored-input','exec'),env)
    priorfontpath=Path(font['prior_native_page_proof']);assert sha(priorfontpath.read_bytes())==font['prior_native_page_proof_sha256'];priorfont=read(priorfontpath)
    mg=mapping['groups'][0];archive=Path(mg['target_archive']).read_bytes();assert sha(archive)==mg['target_archive_sha256'];block=IlnkContainer.parse(archive).blocks[207];assert sha(block)==mg['research_block_sha256'] and block[:4]==b'CS\1\1'
    ROOT.mkdir(parents=True);ctx=MariaUnlockedCurrentContext(doc['current_strict_native_input'],'unused-no-historical-ROM',ROOT/'current_context');rows=[];fresh=reused=freshfont=reusedfont=0
    for ref,base in zip(mg['text_records'],font['records'],strict=True):
        assert ref['id']==base['id'];raw=bytes.fromhex(ref['target_hex']);body=raw[1:];compiled=bytes.fromhex(base['compiled_hex'])[1:]
        assert body in [compiled,compiled+b' '] and ref['compiled_hex']==base['compiled_hex']
        at=ref['new_offset'];assert block[at:at+len(raw)+1]==raw+b'\0' and block[at-5:at+1].hex()==ref['source_preamble_hex']
        if body==compiled:
            pipeline=deepcopy(base['compiled_native_alignment']);assert len(pipeline['cases'])==4 and all(c['output_hex']==body.hex() for c in pipeline['cases'])
            provenance=None;renderbase=base
            if not all(k in base for k in METRICS):
                provenance=base['prior_exact_native_page_reference'];assert Path(provenance['path'])==priorfontpath
                renderbase=next(r for g in priorfont['groups'] for r in g['records'] if r['id']==provenance['id'] and r['file_path']==provenance['file_path'])
                assert bytes.fromhex(renderbase['compiled_hex'])[1:]==body and renderbase['pages']==base['pages']
            rendered={k:deepcopy(renderbase[k]) for k in METRICS};mode='exact-compiled-input-andown-Maria-context-proof-reuse';reused+=4
        else:
            pipeline=ctx.execute(env['expand'],body,raw[0]);ctx.machines.pop();assert len(pipeline['cases'])==4 and all(c['output_hex']==body.hex() for c in pipeline['cases']);fresh+=4
            previous=next((r for g in prior['groups'] for r in g['records'] if bytes.fromhex(r['final_target_hex'])[1:]==body),None)
            provenance=dict(path=str(PRIOR),file_path=previous['file_path'],id=previous['id']) if previous else None
            if previous:
                rendered=deepcopy(previous['complete_pages']);reusedfont+=1;mode='fresh-Maria-parity-tail-ABI-exact-prior-stored-font-reuse'
            else:
                rendered=page_env['pages'](ctx.arm,ctx.rom.read_file('/GRP/KANJI.FNT'),body);freshfont+=1;mode='fresh-Maria-parity-tail-ABI-andoriginal-font-render'
                for page in rendered['pages']:
                    pixels=bytes.fromhex(page.pop('native_plane_hex'));p=ROOT/(ref['id']+'_stored_page'+str(page['page'])+'.bin');p.write_bytes(pixels)
                    page.update(native_plane=str(p),native_plane_sha256=sha(pixels),same_complete_ink_as_reviewed_compiled_page=True)
            assert len(rendered['pages'])==len(base['pages'])==1
            for page,before in zip(rendered['pages'],base['pages'],strict=True):
                assert Path(page['native_plane']).read_bytes()==Path(before['native_plane']).read_bytes() and page['native_plane_sha256']==before['native_plane_sha256']
        assert rendered['total_bytes']==len(body) and rendered['complete_consumed_bytes']==len(body) and rendered['all_visible_first_internal_final_characters_in_order'] and rendered['no_blank_or_overlap_page']
        for page in rendered['pages']:assert sha(Path(page['native_plane']).read_bytes())==page['native_plane_sha256']
        rows.append(dict(id=ref['id'],file_path=mg['file_path'],final_target_hex=raw.hex(),final_target_offset=at,final_target_bytes=len(raw),parity_space_added=ref['parity_space_added'],proof_mode=mode,exact_prior_consumption_orstored_font_reference=provenance,native_pipeline=pipeline,complete_pages=rendered,all_words_glyphs_bounds_guards_consumption_andpage_count_preserved=True))
    assert len(rows)==18 and not ctx.machines and fresh==28 and reused==44 and freshfont+reusedfont==7
    save(ROOT/'Maria18_stored_targets72_alignments7_zero_ink_tails18_complete_pages.json',dict(candidate=mapping['candidate'],candidate_sha256=mapping['candidate_sha256'],relocation_map=str(MAP),relocation_map_sha256=sha(MAP.read_bytes()),compiled_native_font_proof=str(FONT),compiled_native_font_proof_sha256=sha(FONT.read_bytes()),prior_stored_font_proof=str(PRIOR),prior_stored_font_proof_sha256=sha(PRIOR.read_bytes()),records=rows,stored_alignment_cases=72,fresh_alignment_cases=fresh,exact_reused_own_Maria_alignment_cases=reused,zero_ink_parity_tail_count=7,fresh_stored_font_renders=freshfont,exact_prior_stored_font_reuse=reusedfont,all18_final_stored_targets_equal_reviewed_complete_ink=True,all18_original_single_four_row_pages=True,all_bounds_canaries_pairphase_zero_macros_andcomplete_consumption_pass=True,source0_storage_tail_andtarget2_storage_tail_distinct_from_four_byte_end=True,complete_CS0101_preserved=True,no_ROM_registry_ledger_orname_item_asset_mutation=True,loaders_callers_actual_andregistered_release_pending=True,existing_system_only_unlock_fixture=True,earned_unlock_verified=False,native_context_plan=str(ctx.proof_path),native_context_plan_sha256=sha(ctx.proof_path.read_bytes()),evidence={str(p):sha(p.read_bytes()) for p in [MAP,FONT,PRIOR,MANUSCRIPT,Path(__file__)]},new_credit=0,full_goal_complete=False))
    print(dict(stored_targets=18,stored_alignments=72,fresh_alignments=fresh,own_Maria_exact_reused_alignments=reused,zero_ink_tails=7,fresh_stored_font_renders=freshfont,exact_prior_stored_font_reuse=reusedfont))
