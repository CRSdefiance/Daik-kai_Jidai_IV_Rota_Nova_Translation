"""Check the one compiler parity tail freshly; reuse four byte-identical viewed bodies."""
from copy import deepcopy
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from scripts.Lil_current_route_context_v8198 import RouteCurrentContext
from scripts.generic_name_macro_owned_v5886b import expand
from scripts.research_lil_B209_native_pages_v6461 import pages as old_pages
from scripts.square_shopkeeper_font_oracles_v7020 import expected_pixels
from scripts.prove_lil_B208_name_planes_v6405 import codes
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/Gerhard_stored_v8209')
RELOCATION=Path('work/analysis/Gerhard_sparse_relocation_v8208b/two_blocks_five_sparse_revisions_all_commands_native_relative_cases_full_predecessor_inverse.json')
NATIVE=Path('work/analysis/Gerhard_pages_v8206/5_complete_native_paragraphs5_pages20_compiled_alignments.json')
VIEW=Path('work/analysis/Gerhard_native_review_v8207/five_native_pages_directly_viewed_one_info_zero_warnings.json')
MANUSCRIPT=Path('translations/gerhard_surname_consistency_manuscript_v1.json')
LOGICAL=Path('work/analysis/Gerhard_logical_v8204/5_logical_paragraphs20_original_native_alignments.json')
if __name__=='__main__':
    assert not ROOT.exists();relocation,native,view,doc,logical=map(read,[RELOCATION,NATIVE,VIEW,MANUSCRIPT,LOGICAL])
    assert view['pages_sha256']==sha(NATIVE.read_bytes()) and view['all_five_complete_bodies_visually_read']
    assert native['manuscript_sha256']==sha(MANUSCRIPT.read_bytes())
    image=NdsImage.open(doc['current_ROM']);assert sha(Path(doc['current_ROM']).read_bytes())==doc['current_ROM_sha256']
    archive=Path(relocation['target_archive']).read_bytes();assert sha(archive)==relocation['target_archive_sha256']
    container=IlnkContainer.parse(archive);arm,font=image.read_file('/__arm9__.bin'),image.read_file('/GRP/KANJI.FNT')
    pe={**old_pages.__globals__,'expected_pixels':expected_pixels,'codes':codes}
    exec(compile(native['source_owned_progressive_page_adapter'],__file__+'::original-progressive-pages','exec'),pe)
    names=read(logical['names_proof']);ROOT.mkdir(parents=True)
    ctx=RouteCurrentContext(names['current_native_input'],'unused-no-historical-ROM',ROOT/'current_context')
    rows=[];fresh=[];reused=[]
    for row in doc['records']:
        group=next(g for g in relocation['groups'] if g['block']==row['block']);target=Path(group['target_block']).read_bytes()
        assert sha(target)==group['target_block_sha256'] and container.blocks[row['block']]==target
        old=next(r for r in native['records'] if r['id']==row['id']);stored=next(r for r in group['text_records'] if r['id']==row['id'])
        raw=bytes.fromhex(stored['target_hex']);compiled=bytes.fromhex(stored['compiled_hex']);at=stored['new_offset']
        assert compiled.hex()==old['compiled_hex'] and raw==compiled+(b' ' if stored['parity_space_added'] else b'')
        assert raw[0]==row['source_selector'] and b'\0' not in raw[1:] and target[at:at+len(raw)+1]==raw+b'\0'
        assert target[at-5:at+1].hex()==row['source_complete_preamble_hex']
        body=raw[1:];assert b'%' not in body
        for token in [b'FI',b'FA',b'FO']:assert body.count(token)==bytes.fromhex(row['source_hex'])[1:].count(token)
        expected=body.replace(b'FI',b'Lil').replace(b'FA',b'Argot').replace(b'FO',b'Argot Co.')
        if raw==compiled:
            assert expected.hex()==old['expanded_native_hex'];proof=deepcopy(old);reused.append(row['id'])
        else:
            alignment=ctx.execute(expand,body,raw[0]);ctx.machines.pop()
            assert len(alignment['cases'])==4 and all(r['output_hex']==expected.hex() for r in alignment['cases'])
            rendered=pe['pages'](arm,font,expected)
            assert len(rendered['pages'])==len(old['pages'])==1 and rendered['complete_consumed_bytes']==len(expected)
            for page,previous in zip(rendered['pages'],old['pages'],strict=True):
                plane=bytes.fromhex(page.pop('native_plane_hex'))
                assert sha(plane)==previous['native_plane_sha256']==sha(Path(previous['native_plane']).read_bytes())
                page.update(viewed_native_plane=previous['native_plane'],viewed_native_plane_sha256=previous['native_plane_sha256'])
            proof=dict(native_alignment=alignment,**rendered);fresh.append(row['id'])
        assert len(proof['pages'])==1
        rows.append(dict(id=row['id'],file_path=row['file_path'],block=row['block'],source_selector=row['source_selector'],kind='progressive',
            source_reference=row['source_reference'],predecessor_reference=row['current_reference'],
            target_reference=dict(offset=at,bytes=len(raw),header_offset=at-5,record_index=stored['new_record_index']),
            stored_hex=raw.hex(),compiled_hex=compiled.hex(),expanded_stored_hex=expected.hex(),
            compiler_owned_parity_space=stored['parity_space_added'],reused_exact_native_body=raw==compiled,
            complete_native_stored_proof=proof,complete_native_ink_exact_to_directly_viewed_pages=True))
        print('STORED_PASS',row['id'],'fresh parity tail' if raw!=compiled else 'exact native reuse',flush=True)
    assert len(rows)==5 and len(fresh)==1 and len(reused)==4 and not ctx.machines
    save(ROOT/'5_stored_bodies4_fresh16_reused_alignments5_exact_viewed_pages.json',dict(
        candidate=doc['current_ROM'],candidate_sha256=doc['current_ROM_sha256'],relocation=str(RELOCATION),relocation_sha256=sha(RELOCATION.read_bytes()),
        native_viewed_proof=str(NATIVE),native_viewed_proof_sha256=sha(NATIVE.read_bytes()),native_review=str(VIEW),native_review_sha256=sha(VIEW.read_bytes()),
        manuscript=str(MANUSCRIPT),manuscript_sha256=sha(MANUSCRIPT.read_bytes()),records=rows,fresh_parity_tail_records=fresh,exact_native_reused_records=reused,
        fresh_native_alignment_cases=4,exact_reused_native_alignment_cases=16,total_bound_alignment_cases=20,
        all5_complete_native_paragraphs5_pages_full_first_internal_final_glyphs_bounds_consumption_pass=True,
        all5_native_ink_planes_exact_to_already_viewed=True,one_parity_tail_creates_no_blank_oradditional_page=True,
        all5_complete_sixbyte_preambles_01_09_10_FI1_preserved=True,
        one_info_zero_warning_QA_unchanged=True,stored_body_checks_not_actual_scene_page_transition_orrelease=True,
        native_target_name_final_controls_fullreference_callers_loaders_actual_policy_atomic_andregistered_release_pending=True,
        native_context_plan=str(ctx.proof_path),native_context_plan_sha256=sha(ctx.proof_path.read_bytes()),
        evidence={str(p):sha(p.read_bytes()) for p in [RELOCATION,NATIVE,VIEW,MANUSCRIPT,LOGICAL,Path(__file__)]},
        new_credit=0,new_emulator_runs=0,full_goal_complete=False))
    print('5 stored paragraphs/5 exact viewed pages;1 parity tail4fresh/4bodies16reused alignments;no extra page.')
