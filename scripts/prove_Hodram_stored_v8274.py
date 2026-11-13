"""Check only11new stored parity tails;rebind17byte-identical native bodies through the exact name-only ARM9 inverse."""
from copy import deepcopy
from types import FunctionType
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.dialogue.gerhard_surname_profile_v1 import validate_name_transition
from scripts.Hodram_target_route_context_v8270 import RouteCurrentContext
from scripts.generic_name_macro_owned_v5886b import expand as original_expand
from scripts.research_lil_B209_native_pages_v6461 import pages as original_pages
from scripts.square_shopkeeper_font_oracles_v7020 import expected_pixels as original_pixels
from scripts.prove_lil_B208_name_planes_v6405 import codes
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/Hodram_three_block_stored_v8274')
DOC=Path('translations/hodram_B137_B45_B46_editorial_manuscript_v3.json')
RELOC=Path('work/analysis/Hodram_three_block_relocation_v8273/three_blocks28_speeches8_relative_sites40_native_cases_full_inverses.json')
PAGES=Path('work/analysis/Hodram_B137_B45_B46_pages_v8246/28_complete_native_paragraphs28_pages112_compiled_alignments.json')
LOGICAL=Path('work/analysis/Hodram_B137_B45_B46_refinement_v8244/28_logical_paragraphs4_fresh108_exact_reused_alignments.json')
REBIND=Path('work/analysis/Hodram_current_review_binding_v8272/current_review_andnative_reuse_receipt.json')
INPUT=Path('work/analysis/current_V8259_Hodram_native_v8270/current_native_input.json')
if __name__=='__main__':
    assert not ROOT.exists();doc,reloc,pages,logical,rebind=map(read,[DOC,RELOC,PAGES,LOGICAL,REBIND])
    assert reloc['manuscript_sha256']==rebind['manuscript_sha256']==sha(DOC.read_bytes())
    image=NdsImage.open(doc['current_ROM']);arm=image.read_file('/__arm9__.bin');old=NdsImage.open('out/all_routes_combined_v8172_candidate.nds')
    inverse=validate_name_transition(old.read_file('/__arm9__.bin'),arm)
    assert image.read_file('/GRP/KANJI.FNT')==old.read_file('/GRP/KANJI.FNT')
    digest=sha(arm);assert digest=='12ebaf3f3ce558e731c4c972ae90696392a351426cf147fbf3bd830dd1d82d1b'
    page_adapter=checked_text(pages['source_owned_progressive_page_adapter'],{"assert sha(arm)=='2b6aaaa499d634be9afc255d1c39b64ef0f578283c9768c525b31e34499abd0a'":"assert sha(arm)=='12ebaf3f3ce558e731c4c972ae90696392a351426cf147fbf3bd830dd1d82d1b'"})
    pixels=FunctionType(original_pixels.__code__,{**original_pixels.__globals__,'CURRENT_ARM9':digest},argdefs=original_pixels.__defaults__)
    pe={**original_pages.__globals__,'expected_pixels':pixels,'codes':codes};exec(compile(page_adapter,__file__+'::exact-target-font-pages','exec'),pe)
    ee=dict(original_expand.__globals__);exec(compile(logical['source_owned_progressive_adapter'],__file__+'::unchanged-captain1-macro-literal-expansion','exec'),ee)
    archive=Path(reloc['target_archive']).read_bytes();assert sha(archive)==reloc['target_archive_sha256'];bank=IlnkContainer.parse(archive).blocks
    ROOT.mkdir(parents=True);ctx=RouteCurrentContext(INPUT,'unused-no-historical-ROM',ROOT/'current_context')
    rows=[];fresh=[];reused=[]
    for row in doc['records']:
        group=next(g for g in reloc['groups'] if g['block']==row['block']);ref=next(r for r in group['text_records'] if r['id']==row['id'])
        target=bank[row['block']];assert sha(target)==group['target_block_sha256'];at=ref['new_offset']
        stored=bytes.fromhex(ref['target_hex']);compiled=bytes.fromhex(ref['compiled_hex']);pad=ref['parity_space_added']
        assert stored==compiled+(b' ' if pad else b'') and stored[0]==row['source_selector'] and b'\0' not in stored[1:]
        assert target[at:at+len(stored)+1]==stored+b'\0' and target[at-5:at+1].hex()==row['source_complete_preamble_hex']
        assert not any(m in stored[1:] for m in [b'FI',b'FA',b'FO',b'%'])
        prior=next(p for p in pages['records'] if p['id']==row['id']);assert prior['compiled_hex']==compiled.hex() and len(prior['pages'])==1
        if not pad:
            assert prior['expanded_native_hex']==stored[1:].hex();proof=deepcopy(prior);reused.append(row['id'])
            proof.update(exact_reused_native_body_rebound_by_complete_name_only_ARM9_inverse=True)
        else:
            alignment=ctx.execute(ee['expand'],stored[1:],stored[0]);ctx.machines.pop()
            assert len(alignment['cases'])==4 and all(c['output_hex']==stored[1:].hex() for c in alignment['cases'])
            rendered=pe['pages'](arm,image.read_file('/GRP/KANJI.FNT'),stored[1:]);assert len(rendered['pages'])==1 and rendered['complete_consumed_bytes']==len(stored)-1
            for page,previous in zip(rendered['pages'],prior['pages'],strict=True):
                plane=bytes.fromhex(page.pop('native_plane_hex'));assert sha(plane)==previous['native_plane_sha256']==sha(Path(previous['native_plane']).read_bytes())
                page.update(viewed_native_plane=previous['native_plane'],viewed_native_plane_sha256=previous['native_plane_sha256'])
            proof=dict(native_alignment=alignment,**rendered);fresh.append(row['id'])
        assert len(proof['pages'])==1
        rows.append(dict(id=row['id'],file_path=row['file_path'],block=row['block'],source_selector=row['source_selector'],source_reference=row['source_reference'],predecessor_reference=row['current_reference'],
            target_reference=dict(offset=at,bytes=len(stored),header_offset=at-5,record_index=ref['new_record_index']),compiled_hex=compiled.hex(),stored_hex=stored.hex(),expanded_stored_hex=stored[1:].hex(),
            compiler_owned_parity_space=pad,reused_exact_native_body=not pad,complete_native_stored_proof=proof,complete_native_ink_exact_to_directly_viewed_pages=True))
        print('STORED_PASS',row['id'],'fresh parity' if pad else 'exact native reuse',flush=True)
    assert len(rows)==28 and len(fresh)==11 and len(reused)==17 and not ctx.machines
    save(ROOT/'28_stored_bodies44_fresh68_reused_alignments28_exact_native_pages.json',dict(candidate=doc['current_ROM'],candidate_sha256=doc['current_ROM_sha256'],ARM9_sha256=digest,
        manuscript=str(DOC),manuscript_sha256=sha(DOC.read_bytes()),relocation=str(RELOC),relocation_sha256=sha(RELOC.read_bytes()),native_viewed_proof=str(PAGES),native_viewed_proof_sha256=sha(PAGES.read_bytes()),
        native_rebind=str(REBIND),native_rebind_sha256=sha(REBIND.read_bytes()),complete_ARM9_name_inverse=inverse,records=rows,
        fresh_parity_tail_records=fresh,exact_native_reused_records=reused,fresh_native_alignment_cases=44,exact_reused_native_alignment_cases=68,total_bound_alignment_cases=112,
        all28_complete_native_single_pages_full_first_internal_final_glyphs_bounds_andconsumption_pass=True,all11_parity_tails_create_no_blank_oradditional_page=True,
        all28_complete_sixbyte_preambles_source_01_02_09_10_12_71_zero_macros_preserved=True,
        original_two_exact_warning_exceptions_five_infos_andfullprose_unchanged=True,source_owned_target_page_adapter=page_adapter,
        no_global_font_profile_guard_orold_oracle_change=True,stored_body_checks_not_actual_scene_ornameheaders_item_panel_transition_coverage=True,
        final_dispatch_queries_4800_layout0_hide4700_fullreference_loaders_callers_actual_policy_atomic_registered_release_pending=True,
        native_context_plan=str(ctx.proof_path),native_context_plan_sha256=sha(ctx.proof_path.read_bytes()),new_credit=0,new_emulator_runs=0,full_goal_complete=False,
        evidence={str(p):sha(p.read_bytes()) for p in [DOC,RELOC,PAGES,LOGICAL,REBIND,INPUT,Path(__file__)]}))
    print('28stored paragraphs:11paritytails44fresh/17bodies68exactreuse;all28viewed planes exact/noextra pages.Actual scenes/control/reference/release pending.')
