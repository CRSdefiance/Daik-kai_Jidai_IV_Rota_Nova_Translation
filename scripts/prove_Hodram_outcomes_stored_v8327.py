"""Check two new parity tails; exactly reuse four native bodies with identical code/font/input."""
from copy import deepcopy
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from scripts.Hodram_registered_route_context_v8303 import RouteCurrentContext
from scripts.Hodram_FE_font_oracles_v8315 import bind
from scripts.generic_name_macro_owned_v5886b import expand as progressive_expand
from scripts.research_lil_B209_native_pages_v6461 import pages as original_pages
from scripts.prove_lil_B208_name_planes_v6405 import codes
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/Hodram_outcome_stored_v8327')
DOC=Path('translations/hodram_B47_B48_editorial_manuscript_v2.json')
MAP=Path('work/analysis/Hodram_outcome_relocation_v8326/two_blocks6_speeches15_commands_full_source_parent_inverses.json')
PAGES=Path('work/analysis/Hodram_B47_B48_pages_v8324/six_complete_native_pages24_compiled_alignments_distinct_FE.json')
LOGICAL=Path('work/analysis/Hodram_B47_B48_logical_v8320/six_logical_paragraphs24_guarded_alignments_distinct_FE_one_FI.json')
INPUT=Path('work/analysis/current_V8300_Hodram_native_v8303/current_native_input.json')
if __name__=='__main__':
    assert not ROOT.exists();doc,mapping,pages,logical=map(read,[DOC,MAP,PAGES,LOGICAL]);assert mapping['manuscript_sha256']==sha(DOC.read_bytes()) and pages['candidate_sha256']==doc['current_ROM_sha256']
    image=NdsImage.open(doc['current_ROM']);arm,font=image.read_file('/__arm9__.bin'),image.read_file('/GRP/KANJI.FNT');pixels,_,oracle=bind(image)
    assert pages['ARM9_sha256']==sha(arm) and pages['font_sha256']==sha(font)
    pe={**original_pages.__globals__,'expected_pixels':pixels,'codes':codes};exec(compile(pages['source_owned_target_page_adapter'],__file__+'::unchanged-current-complete-page','exec'),pe)
    env=dict(progressive_expand.__globals__);exec(compile(logical['source_owned_progressive_adapter'],__file__+'::unchanged-captain1-wrapper','exec'),env)
    archive=Path(mapping['target_archive']).read_bytes();assert sha(archive)==mapping['target_archive_sha256'];bank=IlnkContainer.parse(archive).blocks
    ROOT.mkdir(parents=True);ctx=RouteCurrentContext(INPUT,'unused-no-historical-ROM',ROOT/'current_context');rows=[];fresh=[];reused=[]
    for row in doc['records']:
        group=next(g for g in mapping['groups'] if g['block']==row['block']);ref=next(t for t in group['text_records'] if t['id']==row['id']);stored=bytes.fromhex(ref['target_hex']);compiled=bytes.fromhex(row['compiled_hex']);at=ref['new_offset'];block=bank[row['block']]
        assert sha(block)==group['target_block_sha256'] and block[at:at+len(stored)+1]==stored+b'\0' and stored==compiled+(b' ' if ref['parity_space_added'] else b'')
        prior=next(p for p in pages['records'] if p['id']==row['id']);assert prior['compiled_hex']==compiled.hex() and len(prior['pages'])==1
        expected=stored[1:].replace(b'FI',b'Hodram');proof=deepcopy(prior)
        if ref['parity_space_added']:
            assert row['source_selector']==2
            alignment=ctx.execute(env['expand'],stored[1:],2);ctx.machines.pop();assert all(c['output_hex']==expected.hex() for c in alignment['cases']) and len(alignment['cases'])==4
            rendered=pe['pages'](arm,font,expected);assert rendered['complete_consumed_bytes']==len(expected) and len(rendered['pages'])==1
            for page,oldpage in zip(rendered['pages'],prior['pages'],strict=True):
                plane=bytes.fromhex(page.pop('native_plane_hex'));assert sha(plane)==oldpage['native_plane_sha256']==sha(Path(oldpage['native_plane']).read_bytes())
                page.update(native_plane=oldpage['native_plane'],native_plane_sha256=oldpage['native_plane_sha256'],viewed_native_plane=oldpage['native_plane'],viewed_native_plane_sha256=oldpage['native_plane_sha256'])
            proof=dict(native_alignment=alignment,**rendered);fresh.append(row['id'])
        else:
            assert expected.hex()==prior['expanded_native_hex'];reused.append(row['id'])
        for page in proof['pages']:assert sha(Path(page['native_plane']).read_bytes())==page['native_plane_sha256']
        rows.append(dict(id=row['id'],file_path=row['file_path'],block=row['block'],source_selector=row['source_selector'],source_reference=row['source_reference'],predecessor_reference=row['current_reference'],
            target_reference=dict(file_path=row['file_path'],block=row['block'],offset=at,bytes=len(stored),header_offset=at-5,record_index=ref['new_record_index'],target_block_sha256=sha(block)),compiled_hex=compiled.hex(),stored_hex=stored.hex(),expanded_stored_hex=expected.hex(),
            compiler_owned_parity_space=ref['parity_space_added'],reused_exact_native_body=not ref['parity_space_added'],complete_native_stored_proof=proof,complete_native_ink_exact_to_directly_viewed_pages=True))
    assert len(fresh)==2 and len(reused)==4 and len(rows)==6 and not ctx.machines
    save(ROOT/'six_stored_bodies8_fresh16_reused_alignments_six_exact_native_pages.json',dict(candidate=doc['current_ROM'],candidate_sha256=doc['current_ROM_sha256'],ARM9_sha256=sha(arm),font_sha256=sha(font),manuscript=str(DOC),manuscript_sha256=sha(DOC.read_bytes()),relocation=str(MAP),relocation_sha256=sha(MAP.read_bytes()),records=rows,
        fresh_parity_body_IDs=fresh,reused_byte_exact_body_IDs=reused,fresh_stored_alignments=8,exact_reused_compiled_alignments=16,complete_stored_native_pages=6,one_real_FI_anddistinct_FE_consumer_preserved=True,
        both_added_trailing_spaces_fully_consumed_without_extra_page_orink=True,target_oracle_binding=oracle,source_owned_target_page_adapter=pages['source_owned_target_page_adapter'],
        actual_control_effects_FE_geometry_headers_transitions_policy_atomic_andregistered_release_pending=True,new_credit=0,new_emulator_runs=0,full_goal_complete=False,
        native_context_plan=str(ctx.proof_path),native_context_plan_sha256=sha(ctx.proof_path.read_bytes()),evidence={str(p):sha(p.read_bytes()) for p in [DOC,MAP,PAGES,LOGICAL,INPUT,Path(__file__)]}))
    print('Stored6:two parity tails/8fresh alignments,four exactbody reuses/16alignments;six same native pages/one FI/originalFE.No extra ink orpage.')
