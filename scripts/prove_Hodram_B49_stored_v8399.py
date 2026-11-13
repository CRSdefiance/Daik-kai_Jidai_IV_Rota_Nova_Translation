"""Verify compiler parity tails against the already viewed B49 complete native pages."""
from copy import deepcopy
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from scripts.Hodram_outcomes_registered_route_context_v8380 import RouteCurrentContext
from scripts.Hodram_FE_font_oracles_v8315 import bind
from scripts.generic_name_macro_owned_v5886b import expand as progressive_expand
from scripts.verify_lil_clifford_north_new_world_FE_v2980 import expand as FE_expand
from scripts.research_lil_B209_native_pages_v6461 import pages as original_pages
from scripts.prove_lil_B208_name_planes_v6405 import codes
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/Hodram_B49_stored_v8399')
RELOCATION=Path('work/analysis/Hodram_B49_relocation_v8398/reconstruction.json')
NATIVE=Path('work/analysis/Hodram_B49_pages_v8395/compiled_native_pages.json')
VIEW=Path('work/analysis/Hodram_B49_native_review_v8397/native_body_review.json')
DOC=Path('translations/hodram_B49_editorial_manuscript_v2.json')
INPUT=Path('work/analysis/current_V8377_Hodram_native_v8380/current_native_input.json')

if __name__=='__main__':
    assert not ROOT.exists()
    relocation,native,view,doc=map(read,[RELOCATION,NATIVE,VIEW,DOC])
    assert relocation['manuscript_sha256']==view['manuscript_sha256']==sha(DOC.read_bytes())
    assert native['manuscript_sha256']==sha(Path(doc['predecessor_manuscript']).read_bytes())
    assert view['reviewed_body_pages']==14 and view['directly_viewed_native_sheet']==native['review_sheet']
    assert sha(Path(native['review_sheet']['path']).read_bytes())==native['review_sheet']['sha256']
    group=relocation['groups'][0];target=Path(group['target_block']).read_bytes()
    archive=Path(relocation['target_archive']).read_bytes()
    assert sha(target)==group['target_block_sha256'] and sha(archive)==relocation['target_archive_sha256']
    assert IlnkContainer.parse(archive).blocks[49]==target
    image=NdsImage.open(doc['current_ROM']);assert sha(Path(doc['current_ROM']).read_bytes())==doc['current_ROM_sha256']
    arm,font=image.read_file('/__arm9__.bin'),image.read_file('/GRP/KANJI.FNT')
    pixels,factory,oracle=bind(image);paint,calibration=factory(image)
    pe={**original_pages.__globals__,'expected_pixels':pixels,'codes':codes}
    exec(compile(native['source_owned_target_page_adapter'],__file__+'::unchanged-complete-page-oracle','exec'),pe)
    prog=dict(progressive_expand.__globals__);exec(compile(native['source_owned_progressive_adapter'],__file__+'::unchanged-progressive','exec'),prog)
    fe=dict(FE_expand.__globals__);exec(compile(native['source_owned_FE_adapter'],__file__+'::unchanged-null-actor-FE','exec'),fe)
    ROOT.mkdir(parents=True);ctx=RouteCurrentContext(INPUT,'unused-no-historical-ROM',ROOT/'current_context')
    rows=[];fresh=[];reused=[]
    for row in doc['records']:
        ref=next(r for r in group['text_records'] if r['id']==row['id'])
        old=next(r for r in native['records'] if r['id']==row['id'])
        compiled=bytes.fromhex(ref['compiled_hex']);stored=bytes.fromhex(ref['target_hex']);at=ref['new_offset']
        assert compiled.hex()==row['compiled_hex']==old['compiled_hex']
        assert stored==compiled+(b' ' if ref['parity_space_added'] else b'')
        assert stored[0]==row['source_selector'] and b'\0' not in stored[1:]
        assert target[at:at+len(stored)+1]==stored+b'\0' and target[at-5:at+1].hex()==row['source_complete_preamble_hex']
        assert target[:at].count(b'\0')==ref['new_record_index']
        expected=stored[1:];is_FE=row['source_selector']==254
        assert not any(token in expected for token in [b'FI',b'FA',b'FO'])
        if stored==compiled:
            assert expected.hex()==old['expanded_native_hex']
            for p in old['pages']:
                assert sha(Path(p['native_plane']).read_bytes())==p['native_plane_sha256']
                if 'physical_plane' in p:assert sha(Path(p['physical_plane']).read_bytes())==p['physical_plane_sha256']
            proof=deepcopy(old);reused.append(row['id'])
        else:
            result=ctx.execute(fe['expand'] if is_FE else prog['expand'],expected,*(() if is_FE else (row['source_selector'],)));ctx.machines.pop()
            assert len(result['cases'])==4 and all(c['output_hex']==expected.hex() for c in result['cases'])
            if is_FE:
                assert all(c['null_source_actor'] for c in result['cases'])
                rendered=paint(expected);previous=old['pages'][0]
                assert sha(rendered['logical'])==previous['native_plane_sha256']
                assert sha(rendered['physical'])==previous['physical_plane_sha256']
                assert rendered['complete_return_input_object_canaries_and_native_independent_plane_equal']
                rendered.pop('logical');rendered.pop('physical')
                proof=dict(native_alignment=result,original_FE_painter=rendered,complete_consumed_bytes=len(expected),full_logical_andphysical_planes_exact_to_viewed=previous)
            else:
                rendered=pe['pages'](arm,font,expected)
                assert len(rendered['pages'])==len(old['pages'])==1 and rendered['complete_consumed_bytes']==len(expected)
                for p,previous in zip(rendered['pages'],old['pages'],strict=True):
                    plane=bytes.fromhex(p.pop('native_plane_hex'))
                    assert sha(plane)==previous['native_plane_sha256']==sha(Path(previous['native_plane']).read_bytes())
                    p.update(viewed_native_plane=previous['native_plane'],viewed_native_plane_sha256=sha(plane))
                proof=dict(native_alignment=result,**rendered)
            fresh.append(row['id'])
        rows.append(dict(id=row['id'],file_path=row['file_path'],block=49,source_selector=row['source_selector'],source_reference=row['source_reference'],predecessor_reference=row['current_reference'],target_reference=dict(offset=at,bytes=len(stored),header_offset=at-5,record_index=ref['new_record_index']),stored_hex=stored.hex(),compiled_hex=compiled.hex(),expanded_stored_hex=expected.hex(),compiler_owned_parity_space=ref['parity_space_added'],reused_exact_native_body=stored==compiled,complete_native_stored_proof=proof,complete_native_ink_exact_to_directly_viewed_page=True))
    assert len(rows)==14 and len(fresh)==6 and len(reused)==8 and not ctx.machines
    save(ROOT/'stored_bodies.json',dict(candidate=doc['current_ROM'],candidate_sha256=doc['current_ROM_sha256'],manuscript=str(DOC),manuscript_sha256=sha(DOC.read_bytes()),relocation=str(RELOCATION),relocation_sha256=sha(RELOCATION.read_bytes()),view=str(VIEW),view_sha256=sha(VIEW.read_bytes()),research_block=group['target_block'],research_block_sha256=sha(target),records=rows,fresh_parity_tail_records=fresh,exact_native_reused_records=reused,fresh_native_alignment_cases=24,exact_reused_native_alignment_cases=32,all14_full_first_internal_final_glyphs_bounds_consumption_andsingle_page_checks_pass=True,all14_ink_planes_exact_to_already_viewed=True,compiler_tails_create_no_blank_oradditional_page=True,source_bound_ellipsis_andmixed_ellipsis_English_preserved=True,FE_original_null_actor_logical_andphysical_planes_exact=True,target_oracle_binding=oracle,FE_factory_calibration=calibration,native_context_plan=str(ctx.proof_path),native_context_plan_sha256=sha(ctx.proof_path.read_bytes()),menu_UI_full_stored_controls_loaders_actual_policy_andregistered_release_pending=True,new_credit=0,new_emulator_runs=0,full_goal_complete=False,evidence={str(p):sha(p.read_bytes()) for p in [RELOCATION,NATIVE,VIEW,DOC,INPUT,Path(__file__)]}))
    print('All14 stored bodies pass:6 parity tails/24 fresh alignments,8 exact bodies/32 reused alignments. Full viewed ink unchanged;no blank/extra pages.No ROM/credit.')
