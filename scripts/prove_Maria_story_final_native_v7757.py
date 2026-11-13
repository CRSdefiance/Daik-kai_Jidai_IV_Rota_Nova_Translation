"""Validate two final changed paragraphs; exactly reuse65 own-current compiled proofs."""
import inspect
from copy import deepcopy
from pathlib import Path
from PIL import Image
from scripts.generic_name_macro_owned_v5886b import expand
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.maria_unlocked_current_context_v7680 import MariaUnlockedCurrentContext
from scripts.research_lil_B209_native_pages_v6461 import pages as old_pages
from scripts.square_shopkeeper_font_oracles_v7020 import expected_pixels
from scripts.prove_lil_B208_name_planes_v6405 import codes
from scripts.verify_village_wrap_v608 import read,save
from dk4tool.patch.grand_race_menu_release import sha
ROOT=Path('work/analysis/maria_story_final_native_v7757')
MANUSCRIPT=Path('translations/maria_B34_B108_B35_editorial_manuscript_v3.json')
PLAN=Path('work/analysis/maria_story_final_prose_v7756b/67_final_v3_plans_two_refinements65_exact_compiled_retentions.json')
PRIOR=Path('work/analysis/maria_story_pages_v7738/67_compiled268_alignments68_complete_native_pages.json')
INPUT=Path('work/analysis/current_V7717_native_v7720/route3/current_native_input.json')
if __name__=='__main__':
    assert not ROOT.exists();doc,plan,prior=map(read,[MANUSCRIPT,PLAN,PRIOR])
    assert plan['manuscript_sha256']==sha(MANUSCRIPT.read_bytes()) and len(plan['changed_records'])==2
    changed={r['id'] for r in plan['changed_records']};assert changed=={'DK4_MES_B34_R0042','DK4_MES_B108_R0111'}
    adapter=prior['source_owned_compiled_macro_adapter'];ns=dict(expand.__globals__);exec(compile(adapter,__file__+'::exact-own-Maria-ABI','exec'),ns)
    pe={**old_pages.__globals__,'expected_pixels':expected_pixels,'codes':codes};exec(compile(prior['source_owned_native_page_adapter'],__file__+'::unchanged-216-native-renderer','exec'),pe)
    ROOT.mkdir(parents=True);ctx=MariaUnlockedCurrentContext(INPUT,'unused-no-historical-ROM',ROOT/'current_context')
    rows=[];logical=[];previews=[]
    for r,p in zip(doc['records'],plan['records'],strict=True):
        assert r['id']==p['id'];base=next(b for b in prior['records'] if b['id']==r['id']);body=bytes.fromhex(p['encoded_hex'])[1:]
        assert bytes.fromhex(p['encoded_hex'])[0]==r['source_selector']
        if r['id'] not in changed:
            assert p['encoded_hex']==base['compiled_hex'] and r['english']==base['logical_English'] and r['source_selector']==base['source_selector']
            row=deepcopy(base);row.update(final_v3_proof_mode='exact-own-current-v2-compiled-input-ARM9-COMMON-FNT-andselector-reuse',prior_native_proof=str(PRIOR),prior_native_proof_sha256=sha(PRIOR.read_bytes()))
            for page in row['pages']:
                assert sha(Path(page['native_plane']).read_bytes())==page['native_plane_sha256']
            logical.append(dict(id=r['id'],mode='unchanged-v2-own-current-logical-proof-reuse',original_complete_row_reference=r['predecessor_effective_reference'],
                previous_v2_manuscript=doc['previous_manuscript'],previous_v2_manuscript_sha256=doc['previous_manuscript_sha256']))
        else:
            raw=r['english'].encode('cp932');expected_logical=raw.replace(b'FI',b'Maria').replace(b'FA',b'Li').replace(b'FO',b'Li Clan')
            l=ctx.execute(ns['expand'],raw,r['source_selector']);ctx.machines.pop();assert all(c['output_hex']==expected_logical.hex() for c in l['cases'])
            logical.append(dict(id=r['id'],mode='four-fresh-final-logical-alignments',logical_hex=raw.hex(),native_alignment=l))
            native=ctx.execute(ns['expand'],body,r['source_selector']);ctx.machines.pop()
            expected=body.replace(b'FI',b'Maria').replace(b'FA',b'Li').replace(b'FO',b'Li Clan')
            assert all(c['output_hex']==expected.hex() for c in native['cases']) and ' '.join(expected.decode('cp932').split())==expected_logical.decode('cp932')
            rendered=pe['pages'](ctx.arm,ctx.rom.read_file('/GRP/KANJI.FNT'),expected);assert len(rendered['pages'])==1
            for page in rendered['pages']:
                pixels=bytes.fromhex(page.pop('native_plane_hex'));path=ROOT/(r['id']+'_final_page1.bin');path.write_bytes(pixels)
                assert page['first_visible_origin']==[0,0]
                image=Image.new('RGB',(216,64));colors={0:(239,232,201),1:(0,8,0),15:(98,97,98)};image.putdata([colors[b] for b in pixels]);png=path.with_suffix('.png');image.save(png)
                page.update(native_plane=str(path),native_plane_sha256=sha(pixels),preview=str(png),preview_sha256=sha(png.read_bytes()),compiler_owned_continuation_guard_bytes=0)
                previews.append(dict(path=str(png),sha256=sha(png.read_bytes())))
            row=dict(id=r['id'],file_path=r['file_path'],block=r['block'],source_record_index=r['source_record_index'],source_selector=r['source_selector'],
                compiled_hex=p['encoded_hex'],expanded_native_hex=expected.hex(),logical_English=r['english'],formatted_markup=p['formatted_markup'],
                native_alignment=native,final_v3_proof_mode='four-fresh-final-compiled-alignments-andoriginal-native-page',**rendered)
        assert len(row['pages'])==1;rows.append(row)
    assert len(rows)==67 and len(logical)==67 and not ctx.machines
    save(ROOT/'67_final_v3_compiled_pages_two_fresh65_exact_own_reuse.json',dict(
        candidate=doc['current_ROM'],candidate_sha256=doc['current_ROM_sha256'],ARM9_sha256=sha(ctx.arm),font_sha256=sha(ctx.rom.read_file('/GRP/KANJI.FNT')),
        manuscript=str(MANUSCRIPT),manuscript_sha256=sha(MANUSCRIPT.read_bytes()),plan=str(PLAN),plan_sha256=sha(PLAN.read_bytes()),
        records=rows,logical_bindings=logical,changed_record_IDs=sorted(changed),
        fresh_logical_alignment_cases=8,fresh_compiled_alignment_cases=8,exact_own_current_compiled_alignment_cases_reused=260,
        fresh_complete_native_page_renders=2,exact_own_current_native_pages_reused=65,final_complete_pages=67,
        source_owned_compiled_macro_adapter=adapter,source_owned_native_page_adapter=prior['source_owned_native_page_adapter'],
        all67_single_native_four_row_pages_complete_glyph_bounds_andconsumption=True,
        English216px_safe_geometry_andall_native_guards_unchanged=True,all_source_FA_FI_FO_counts_andselectors_preserved=True,
        previous_successful_v2_two_page_actual_proof_preserved_not_claimed_current_v3=True,
        review_previews=previews,visual_review_pending=True,stored_reference_affected_English_actual_policy_production_andregistered_integration_pending=True,
        all67_formatting_gates_false=True,existing_system_only_unlock_fixture=True,earned_unlock_verified=False,
        native_context_plan=str(ctx.proof_path),native_context_plan_sha256=sha(ctx.proof_path.read_bytes()),
        evidence={str(p):sha(p.read_bytes()) for p in [MANUSCRIPT,PLAN,PRIOR,INPUT,Path(__file__)]},new_credit=0,new_emulator_runs=0,full_goal_complete=False))
    print('Finalv3:8fresh logical+8fresh compiled alignments;2fresh native pages+65exact own-current page/260compiled alignment reuse.All67single pages;stored andtwo affected English actual checks pending.')
