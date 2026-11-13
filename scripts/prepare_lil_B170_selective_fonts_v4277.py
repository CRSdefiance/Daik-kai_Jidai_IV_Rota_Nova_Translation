"""Reuse31 byte-identical native records and freshly verify the two changed complete plans."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import save

ROOT=Path('work/analysis/lil_B170_selective_font_tools_v4277')
OLD=Path('scripts/verify_lil_B170_fonts_v4274.py')
NEW=Path('scripts/verify_lil_B170_fonts_v4277.py')
if __name__=='__main__':
    assert not ROOT.exists() and not NEW.exists()
    text=OLD.read_text(encoding='utf-8').replace('lil_B170_layout_v1','lil_B170_layout_v2').replace('lil_B170_fonts_v4274','lil_B170_fonts_v4277').replace('lil_B170_editorial_manuscript_v2.json','lil_B170_editorial_manuscript_v4.json')
    needle='    cases=[];qa_reports=[];pictures=[];macro_calls=0\n'
    assert text.count(needle)==1
    text=text.replace(needle,needle+"""    previous_path=Path('work/analysis/lil_B170_fonts_v4274/current_macro_QA_and_progressive_font_proof.json')
    previous=read(previous_path);previous_doc_path=Path(previous['manuscript']);previous_doc=read(previous_doc_path)
    assert sha(previous_doc_path.read_bytes())==previous['manuscript_sha256']
    assert previous['candidate_sha256']==doc['current_ROM_sha256'] and previous['ARM9_sha256']==sha(ctx.arm) and previous['COMMON_sha256']==sha(ctx.common)
    assert previous['scoped_profile_sha256']==sha(Path('dk4tool/dialogue/lil_B170_profile.py').read_bytes())
    cached={r['id']:r for r in previous['cases']};previous_rows={r['id']:r for r in previous_doc['records']};reused_calls=0;fresh_records=[]
""")
    needle="        if row['kind']=='system-FE':continue\n"
    assert text.count(needle)==1
    text=text.replace(needle,"""        old=previous_rows[row['id']];prior=cached[row['id']]
        if old['english']==row['english'] and old['source_hex']==row['source_hex'] and old['source_selector']==row['source_selector'] and prior['encoded_hex']==result.encoded.hex() and prior['formatted_markup']==result.formatted_markup:
            assert prior['complete_native_independent216x64_plane_equal'] and prior['all_first_final_internal_glyphs_in_order_and_unique_cells'] and prior['all_visible_origins_zero_and16px_rows_within4rows']
            assert sha(Path(prior['preview']).read_bytes())==prior['preview_sha256']
            assert sum(len(p['cases']) for p in prior['current_native_macro_pipelines'])==8
            cases.append(dict(prior,exact_byte_identical_native_reuse_proof=str(previous_path),exact_byte_identical_native_reuse_proof_sha256=sha(previous_path.read_bytes())))
            pictures.append((row['id'],'selector'+row['source_presentation_prefix_hex'],Image.open(prior['preview']).convert('RGB')))
            macro_calls+=8;reused_calls+=8
            continue
        fresh_records.append(row['id'])
"""+needle)
    needle='    negatives=[]\n'
    assert text.count(needle)==1
    text=text.replace(needle,"    assert set(fresh_records)=={'DK4_MES_B170_R0037','DK4_MES_B170_R0104'} and reused_calls==248 and macro_calls-reused_calls==16\n"+needle)
    needle='current_original_macro_alignment_calls=264,'
    assert text.count(needle)==1
    text=text.replace(needle,needle+"new_current_original_macro_alignment_calls=macro_calls-reused_calls,reused_original_macro_alignment_calls=reused_calls,fresh_record_IDs=fresh_records,previous_native_proof=str(previous_path),previous_native_proof_sha256=sha(previous_path.read_bytes()),")
    text=text.replace('33 complete progressive planes,264 macro cases,33 QA plans and13 source-consumer negatives pass;five sheets need visual review.',
        '33 complete progressive planes:16 fresh/248 exact reused macro cases,33 fresh QA plans and13 source-consumer negatives pass;five final sheets need visual review.')
    compile(text,str(NEW),'exec')
    NEW.write_text(text,encoding='utf-8',newline='\n')
    ROOT.mkdir(parents=True)
    save(ROOT/'source_derivation.json',dict(previous=str(OLD),previous_sha256=sha(OLD.read_bytes()),successor=str(NEW),successor_sha256=sha(NEW.read_bytes()),
        expected_total_macro_cases=264,expected_fresh_cases=16,expected_exact_reused_cases=248,
        fresh_native_record_IDs=['DK4_MES_B170_R0037','DK4_MES_B170_R0104'],no_actual_gameplay_orcredit_change=True,full_goal_complete=False))
    print('Selective native verifier prepared:two fresh complete records,31 exact native-case reuses,all33 QA plans refreshed.')
