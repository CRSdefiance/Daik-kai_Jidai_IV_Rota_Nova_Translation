"""Bind one improved compiled page and15 exact already verified native pages."""
from copy import deepcopy
from pathlib import Path
from PIL import Image
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.maria_unlocked_current_context_v7680 import MariaUnlockedCurrentContext
from scripts.generic_name_macro_owned_v5886b import expand
from scripts.research_lil_B209_native_pages_v6461 import pages as old_pages
from scripts.square_shopkeeper_font_oracles_v7020 import expected_pixels
from scripts.prove_lil_B208_name_planes_v6405 import codes
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/maria_confrontation_final_pages_v7800')
MANUSCRIPT=Path('translations/maria_B36_editorial_manuscript_v2.json')
PLAN=Path('work/analysis/maria_confrontation_wrap_v7799/16_plans_one_sentence_coherence_refinement_no_prose_change.json')
PRIOR=Path('work/analysis/maria_confrontation_pages_v7798/16_compiled64_alignments_complete_native_pages.json')
NAMES=Path('work/analysis/maria_confrontation_names_v7788/three_static_speakers_six_getters_clean_fields_source_macros.json')
LOGICAL=Path('work/analysis/maria_confrontation_refined_logical_v7797/16_final_logical_paragraphs4_fresh60_exact_reused_alignments.json')
if __name__=='__main__':
    assert not ROOT.exists();doc,plan,prior,names,logical=map(read,[MANUSCRIPT,PLAN,PRIOR,NAMES,LOGICAL])
    assert plan['manuscript_sha256']==prior['manuscript_sha256']==logical['manuscript_sha256']==sha(MANUSCRIPT.read_bytes())
    assert len(plan['changed_records'])==1 and plan['changed_records'][0]['id']=='DK4_MES_B36_R0037'
    assert logical['final_native_alignment_coverage']==64
    ROOT.mkdir(parents=True);ctx=MariaUnlockedCurrentContext(names['current_native_input'],'unused-no-historical-ROM',ROOT/'current_context')
    ns=dict(expand.__globals__);exec(compile(prior['source_owned_compiled_macro_adapter'],__file__+'::same-compiled-adapter','exec'),ns)
    pe={**old_pages.__globals__,'expected_pixels':expected_pixels,'codes':codes}
    exec(compile(prior['source_owned_native_page_adapter'],__file__+'::same-guarded-page-adapter','exec'),pe)
    image=NdsImage.open(doc['current_ROM']);arm,font=image.read_file('/__arm9__.bin'),image.read_file('/GRP/KANJI.FNT')
    rows=[];previews=[];fresh=reused=0
    for row,p in zip(doc['records'],plan['records'],strict=True):
        before=next(r for r in prior['records'] if r['id']==row['id']);assert row['id']==p['id']
        if before['compiled_hex']==p['encoded_hex']:
            assert before['source_selector']==row['source_selector'] and before['logical_English']==row['english']
            result=deepcopy(before);result.update(final_proof_mode='exact-own-current-compiled-body-andnative-page-reuse',prior_native_proof=str(PRIOR),prior_native_proof_sha256=sha(PRIOR.read_bytes()));reused+=4
        else:
            assert row['source_record_index']==37
            raw=bytes.fromhex(p['encoded_hex']);expected=raw[1:].replace(b'FI',b'Maria').replace(b'FA',b'Li').replace(b'FO',b'Li Clan')
            result=ctx.execute(ns['expand'],raw[1:],raw[0]);ctx.machines.pop();fresh+=4
            assert len(result['cases'])==4 and all(c['output_hex']==expected.hex() for c in result['cases'])
            rendered=pe['pages'](arm,font,expected);assert len(rendered['pages'])==1
            for page in rendered['pages']:
                pixels=bytes.fromhex(page.pop('native_plane_hex'));path=ROOT/(row['id']+'_page1.bin');path.write_bytes(pixels)
                assert page['first_visible_origin']==[0,0]
                picture=Image.new('RGB',(216,64));colors={0:(239,232,201),1:(0,8,0),15:(98,97,98)}
                picture.putdata([colors[v] for v in pixels]);preview=path.with_suffix('.png');picture.resize((864,256),Image.Resampling.NEAREST).save(preview)
                page.update(native_plane=str(path),native_plane_sha256=sha(pixels),preview=str(preview),preview_sha256=sha(preview.read_bytes()),
                    compiler_owned_continuation_guard_bytes=0,first_visible_origin_matches_original_return_andguard=True)
                previews.append(dict(path=str(preview),sha256=sha(preview.read_bytes())))
            result=dict(id=row['id'],file_path=row['file_path'],block=row['block'],source_record_index=row['source_record_index'],
                source_selector=row['source_selector'],compiled_hex=p['encoded_hex'],expanded_native_hex=expected.hex(),
                logical_English=row['english'],formatted_markup=p['formatted_markup'],native_alignment=result,**rendered,
                final_proof_mode='fresh-native-page-for-scoped-complete-sentence-wrap')
        assert len(result['pages'])==1
        for page in result['pages']:assert sha(Path(page['native_plane']).read_bytes())==page['native_plane_sha256']
        rows.append(result)
    assert len(rows)==16 and fresh==4 and reused==60 and not ctx.machines
    save(ROOT/'16_final_compiled_pages4_fresh60_exact_reused_alignments.json',dict(
        candidate=doc['current_ROM'],candidate_sha256=doc['current_ROM_sha256'],ARM9_sha256=sha(arm),font_sha256=sha(font),
        manuscript=str(MANUSCRIPT),manuscript_sha256=sha(MANUSCRIPT.read_bytes()),plan=str(PLAN),plan_sha256=sha(PLAN.read_bytes()),
        records=rows,fresh_compiled_alignment_cases=4,exact_own_current_compiled_alignment_cases_reused=60,
        fresh_complete_native_page_renders=1,exact_own_current_native_pages_reused=15,final_complete_pages=16,
        final_logical_proof=str(LOGICAL),final_logical_proof_sha256=sha(LOGICAL.read_bytes()),
        all16_single_native_pages_complete_glyph_bounds_canaries_andconsumption=True,
        all_original_words_punctuation_macro_order_source_selectors_andEnglish216_geometry_preserved=True,
        source_owned_compiled_macro_adapter=prior['source_owned_compiled_macro_adapter'],source_owned_native_page_adapter=prior['source_owned_native_page_adapter'],
        review_previews=previews,previous_sheets=prior['review_sheets'],visual_review_pending=True,
        stored_source_controls_actual_reference_policy_production_andregistered_integration_pending=True,
        all16_formatting_gates_false=True,existing_system_only_unlock_fixture=True,earned_unlock_verified=False,
        evidence={str(p):sha(p.read_bytes()) for p in [MANUSCRIPT,PLAN,PRIOR,NAMES,LOGICAL,Path(__file__)]},new_credit=0,new_emulator_runs=0,full_goal_complete=False))
    print('16final native singlepages;4fresh compiled alignments/one fresh page,60alignments/15pages exact reused.Words andmacro order unchanged;visual/stored/control/actual/release pending.')
