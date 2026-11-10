"""Refine avoidable auxiliary/idiom breaks without altering prose, row counts, width or guards."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/Rafael_B50_phrase_tools_v8143')
if __name__=='__main__':
    assert not ROOT.exists()
    a=derive('scripts/plan_Rafael_B50_layout_v8140.py','scripts/plan_Rafael_B50_layout_v8140b.py',{
        'Rafael_B50_layout_v8140':'Rafael_B50_layout_v8140b',
        'ENV={**previous.ENV':"COHERENT_PAIRS=COHERENT_PAIRS|{(\"it's\",'been'),(\"you're\",'as'),('come','on'),('no','idea'),(\"i'll\",'do')}\nENV={**previous.ENV",
    })
    src=Path('scripts/refine_Rafael_B49_pages_v8092.py').read_text('utf8')
    note=src[src.index("    save(ROOT/'rejected_extra_article"):src.index("    print('FinalB49",src.index("    save(ROOT/'rejected_extra_article"))]
    b=derive('scripts/refine_Rafael_B49_pages_v8092.py','scripts/refine_Rafael_B50_pages_v8143.py',{
        note:'',
        'Rafael_B49_pages_refined_v8092':'Rafael_B50_pages_refined_v8143',
        'Rafael_B49_pages_v8091/61_complete_native_paragraphs61_pages244_compiled_alignments.json':'Rafael_B50_pages_v8141/28_complete_native_paragraphs28_pages112_compiled_alignments.json',
        'Rafael_B49_layout_v8090c/61_automatic_plans_full_native_width_exact_source00_02_09_no_FE.json':'Rafael_B50_layout_v8140b/28_automatic_plans_full_native_width_exact_source00_02_09_FA2_FI1.json',
        'Rafael_B49_logical_v8089/61_logical_paragraphs244_original_native_alignments_no_FE.json':'Rafael_B50_logical_v8139/28_logical_paragraphs112_original_native_alignments_no_FE.json',
        'Rafael_B49_names_v8078/seven_static_speakers14_getters_clean_fields28_synthetic_macro_alignments.json':'Rafael_B50_names_current_v8136/three_static_speakers_six_reused_getters_three_reused_voices_exact_V8122_binding.json',
        'B49':'B50','block=49':'block=50',
        "['DK4_MES_B49_R0043','DK4_MES_B49_R0142','DK4_MES_B49_R0213','DK4_MES_B49_R0244','DK4_MES_B49_R0405']":"['DK4_MES_B50_R0049','DK4_MES_B50_R0069','DK4_MES_B50_R0103','DK4_MES_B50_R0108','DK4_MES_B50_R0114']",
        'prefix in [2,8]':'prefix in [0,2,9]',
        "assert all(m not in body for m in [b'FI',b'FA',b'FO',b'%'])":"assert b'%' not in body\n        for token in [b'FI',b'FA',b'FO']:assert body.count(token)==bytes.fromhex(row['source_hex'])[1:].count(token)\n        expected=body.replace(b'FI',b'Rafael').replace(b'FA',b'Castor').replace(b'FO',b'Castor Co.')",
        "c['output_hex']==body.hex()":"c['output_hex']==expected.hex()",
        "' '.join(body.decode('ascii').split())==row['english']":"' '.join(expected.decode('ascii').split())==row['english'].replace('{MACRO:FI}','Rafael').replace('{MACRO:FA}','Castor').replace('{MACRO:FO}','Castor Co.')",
        "pe['pages'](arm,font,body);assert rendered['complete_consumed_bytes']==len(body)":"pe['pages'](arm,font,expected);assert rendered['complete_consumed_bytes']==len(expected)",
        'expanded_native_hex=body.hex()':'expanded_native_hex=expected.hex()',
        'len(rows)==61 and len(reused)==56':'len(rows)==28 and len(reused)==23','len(groups)==5':'len(groups)==4',
        "['DK4_MES_B49_R0213','DK4_MES_B49_R0244','DK4_MES_B49_R0405']":"['DK4_MES_B50_R0061','DK4_MES_B50_R0114']",
        'reused_compiled_alignment_cases=224,total_bound_compiled_alignment_cases=244':'reused_compiled_alignment_cases=92,total_bound_compiled_alignment_cases=112',
        'reused_progressive_alignment_cases=224':'reused_progressive_alignment_cases=92','progressive_alignment_cases=244':'progressive_alignment_cases=112',
        'no_repeated_native_execution_for56_exact_records':'no_repeated_native_execution_for23_exact_records',
        '61_final_native_pages20_fresh224_reused_alignments':'28_final_native_pages20_fresh92_reused_alignments',
        'Recheck only five changed paragraphs;reuse56 exact native proofs andreplace five sheets.':'Recheck five changed B50 paragraphs;reuse23 exact native proofs andreplace four sheets.',
        'FinalB49:61native pages,20fresh/224exactreused alignments;five updated sheets need direct view. Three original weak-ending diagnostics retained;formatting still pendingactual/release.':'FinalB50:28native pages,20fresh/92exactreused alignments;four updated sheets need direct view.Two original weak-ending diagnostics retained;formatting still pendingactual/release.',
    })
    ROOT.mkdir(parents=True);save(ROOT/'source_locked_derivations.json',[a,b])
    print('Prepared five same-row-count B50 phrase preferences and only-changed-record native rebind.')
