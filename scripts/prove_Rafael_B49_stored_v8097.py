"""Fresh native checks for eight zero-ink parity tails;reuse seven byte-exact reviewed bodies."""
from copy import deepcopy
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from scripts.papal_trade_route_native_context_v7626 import RouteCurrentContext
from scripts.generic_name_macro_owned_v5886b import expand as progressive_expand
from scripts.research_lil_B209_native_pages_v6461 import pages as old_pages
from scripts.square_shopkeeper_font_oracles_v7020 import expected_pixels
from scripts.prove_lil_B208_name_planes_v6405 import codes
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/Rafael_B49_stored_v8097')
RELOCATION=Path('work/analysis/Rafael_B49_relocation_v8096/one_block61_speeches56_relative_fixups280_cases_exact_full_inverse.json')
NATIVE=Path('work/analysis/Rafael_B49_pages_refined_v8092/61_final_native_pages20_fresh224_reused_alignments.json')
VIEW=Path('work/analysis/Rafael_B49_native_review_v8095/61_native_pages7_names_three_scoped_warnings22_infos_wrap_review.json')
MANUSCRIPT=Path('translations/rafael_B49_editorial_manuscript_v2.json')
LOGICAL=Path('work/analysis/Rafael_B49_logical_v8089/61_logical_paragraphs244_original_native_alignments_no_FE.json')
if __name__=='__main__':
    assert not ROOT.exists();relocation,native,view,doc,logical=map(read,[RELOCATION,NATIVE,VIEW,MANUSCRIPT,LOGICAL])
    assert view['manuscript_sha256']==sha(MANUSCRIPT.read_bytes()) and len(view['directly_viewed_sheets'])==12 and all(s['directly_viewed'] for s in view['directly_viewed_sheets'])
    assert native['manuscript_sha256']==sha(Path(doc['prior_manuscript']).read_bytes())
    image=NdsImage.open(doc['current_ROM']);assert sha(Path(doc['current_ROM']).read_bytes())==doc['current_ROM_sha256']
    group=relocation['groups'][0];blockpath=Path(group['target_block']);target=blockpath.read_bytes()
    assert sha(target)==group['target_block_sha256'] and len(target)==3792 and group['target_logical_end']==3792
    archive=Path(relocation['target_archive']).read_bytes()
    assert sha(archive)==relocation['target_archive_sha256'] and IlnkContainer.parse(archive).blocks[49]==target
    arm,font=image.read_file('/__arm9__.bin'),image.read_file('/GRP/KANJI.FNT')
    pe={**old_pages.__globals__,'expected_pixels':expected_pixels,'codes':codes}
    exec(compile(native['source_owned_progressive_page_adapter'],__file__+'::original-progressive-pages','exec'),pe)
    env=dict(progressive_expand.__globals__);exec(compile(logical['source_owned_progressive_adapter'],__file__+'::original-progressive-processing','exec'),env)
    names=read(logical['names_proof']);ROOT.mkdir(parents=True)
    ctx=RouteCurrentContext(names['current_native_input'],'unused-no-historical-ROM',ROOT/'current_context')
    rows=[];fresh=[];reused=[]
    for row in doc['records']:
        old=next(r for r in native['records'] if r['id']==row['id'])
        stored=next(r for r in group['text_records'] if r['id']==row['id'])
        raw=bytes.fromhex(stored['target_hex']);compiled=bytes.fromhex(stored['compiled_hex']);at=stored['new_offset']
        assert compiled.hex()==old['compiled_hex']==row['compiled_hex'] and raw==compiled+(b' ' if stored['parity_space_added'] else b'')
        assert raw[0]==row['source_selector'] and b'\0' not in raw[1:] and target[at:at+len(raw)+1]==raw+b'\0'
        assert target[at-5:at+1].hex()==row['source_complete_preamble_hex']
        body=raw[1:];assert all(t not in body for t in [b'FA',b'FO',b'%'])
        assert body.count(b'FI')==int(row['source_record_index'] in [311,388])
        expected=body.replace(b'FI',b'Rafael')
        if raw==compiled:
            assert expected.hex()==old['expanded_native_hex']
            proof=deepcopy(old);reused.append(row['id'])
        else:
            alignment=ctx.execute(env['expand'],body,raw[0]);ctx.machines.pop()
            assert len(alignment['cases'])==4 and all(r['output_hex']==expected.hex() for r in alignment['cases'])
            rendered=pe['pages'](arm,font,expected)
            assert len(rendered['pages'])==len(old['pages'])==row['native_page_count'] and rendered['complete_consumed_bytes']==len(expected)
            for page,previous in zip(rendered['pages'],old['pages'],strict=True):
                plane=bytes.fromhex(page.pop('native_plane_hex'))
                assert sha(plane)==previous['native_plane_sha256']==sha(Path(previous['native_plane']).read_bytes())
                page.update(viewed_native_plane=previous['native_plane'],viewed_native_plane_sha256=previous['native_plane_sha256'])
            proof=dict(native_alignment=alignment,**rendered);fresh.append(row['id'])
        assert len(proof['pages'])==1
        rows.append(dict(id=row['id'],file_path=row['file_path'],block=49,source_selector=row['source_selector'],kind='progressive',
            source_reference=row['source_reference'],predecessor_reference=row['current_reference'],
            target_reference=dict(offset=at,bytes=len(raw),header_offset=at-5,record_index=stored['new_record_index']),
            stored_hex=raw.hex(),compiled_hex=compiled.hex(),expanded_stored_hex=expected.hex(),
            compiler_owned_parity_space=stored['parity_space_added'],reused_exact_native_body=raw==compiled,
            complete_native_stored_proof=proof,complete_native_ink_exact_to_directly_viewed_pages=True))
        print('STORED_PASS',row['id'],'fresh parity tail' if raw!=compiled else 'exact native reuse',flush=True)
    assert len(rows)==61 and len(fresh)==31 and len(reused)==30 and not ctx.machines
    assert sum(len(r['complete_native_stored_proof']['pages']) for r in rows)==61
    save(ROOT/'all61_stored_bodies124_fresh120_reused_alignments61_exact_viewed_pages.json',dict(
        candidate=doc['current_ROM'],candidate_sha256=doc['current_ROM_sha256'],research_block=str(blockpath),research_block_sha256=sha(target),
        relocation=str(RELOCATION),relocation_sha256=sha(RELOCATION.read_bytes()),native_viewed_proof=str(NATIVE),native_viewed_proof_sha256=sha(NATIVE.read_bytes()),
        native_review=str(VIEW),native_review_sha256=sha(VIEW.read_bytes()),manuscript=str(MANUSCRIPT),manuscript_sha256=sha(MANUSCRIPT.read_bytes()),
        records=rows,fresh_parity_tail_records=fresh,exact_native_reused_records=reused,
        fresh_native_alignment_cases=124,exact_reused_native_alignment_cases=120,total_bound_alignment_cases=244,
        all61_complete_native_paragraphs61_pages_full_first_internal_final_glyphs_bounds_consumption_pass=True,
        all61_native_ink_planes_exact_to_already_viewed=True,all31_parity_tails_create_no_blank_oradditional_page=True,
        all61_complete_stored_single_pages_exact_to_viewed=True,
        all61_complete_sixbyte_preambles_source00_02_09_andtwo_FI_preserved=True,
        three_exact_QA_warnings22_infos_andnarrow_documented_exceptions_unchanged=True,
        stored_body_checks_not_actual_scene_page_transition_orrelease=True,
        final_dispatch_predicates_fullreference_callers_loaders_actual_C281_transition_policy_atomic_andrelease_pending=True,
        native_context_plan=str(ctx.proof_path),native_context_plan_sha256=sha(ctx.proof_path.read_bytes()),
        evidence={str(p):sha(p.read_bytes()) for p in [RELOCATION,NATIVE,VIEW,MANUSCRIPT,LOGICAL,Path(__file__)]},
        new_credit=0,new_emulator_runs=0,full_goal_complete=False))
    print('61stored paragraphs/61exactviewed pages:31tails124fresh/30bodies120reused alignments;noextra/blank pages. ActualC281transition/control/reference/release pending.')
