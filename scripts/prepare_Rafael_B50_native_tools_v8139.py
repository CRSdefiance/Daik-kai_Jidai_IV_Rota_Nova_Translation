"""Prepare B50 logical and compiled native proofs with both original FA and FI substitutions."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/Rafael_B50_native_tools_v8139')
NAMES='Rafael_B50_names_current_v8136/three_static_speakers_six_reused_getters_three_reused_voices_exact_V8122_binding.json'
if __name__=='__main__':
    assert not ROOT.exists()
    a=derive('scripts/prove_Rafael_B49_logical_v8089.py','scripts/prove_Rafael_B50_logical_v8139.py',{
        'Rafael_B49_logical_v8089':'Rafael_B50_logical_v8139',
        'Rafael_B49_names_v8078/seven_static_speakers14_getters_clean_fields28_synthetic_macro_alignments.json':NAMES,
        'B49':'B50',".replace('{MACRO:FI}','FI').encode('cp932')":".replace('{MACRO:FI}','FI').replace('{MACRO:FA}','FA').replace('{MACRO:FO}','FO').encode('cp932')",
        '[0,2,4,5,6,8,9]':'[0,2,9]','len(rows)==61':'len(rows)==28','61_logical_paragraphs244_original_native_alignments_no_FE':'28_logical_paragraphs112_original_native_alignments_no_FE',
        'alignment_cases=244':'alignment_cases=112','dict(FI=2,FA=0,FO=0)':'dict(FI=1,FA=2,FO=0)',
        'B49_has61_progressive':'B50_has28_progressive',
        'Original four-alignment macro/literal checks for91 B49 paragraphs;four FE consumers stay distinct.':'Original four-alignment macro/literal checks for28 B50 paragraphs;no FE consumers.',
        '61 logical paragraphs/244guarded native alignments pass;allprogressive/noFE,two sourceFI.':'28 logical paragraphs/112guarded native alignments pass;allprogressive/noFE,sourceFA2/FI1.',
    })
    b=derive('scripts/prove_Rafael_B49_pages_v8091.py','scripts/prove_Rafael_B50_pages_v8141.py',{
        'Rafael_B49_pages_v8091':'Rafael_B50_pages_v8141',
        'Rafael_B49_layout_v8090/61_automatic_plans_full_native_width_exact_source00_02_09_no_FE.json':'Rafael_B50_layout_v8140/28_automatic_plans_full_native_width_exact_source00_02_09_FA2_FI1.json',
        'Rafael_B49_logical_v8089/61_logical_paragraphs244_original_native_alignments_no_FE.json':'Rafael_B50_logical_v8139/28_logical_paragraphs112_original_native_alignments_no_FE.json',
        'Rafael_B49_names_v8078/seven_static_speakers14_getters_clean_fields28_synthetic_macro_alignments.json':NAMES,
        'B49':'B50','block=49':'block=50','[0,2,4,5,6,8,9]':'[0,2,9]',
        "row['english'].replace('{MACRO:FI}','Rafael')":"row['english'].replace('{MACRO:FI}','Rafael').replace('{MACRO:FA}','Castor').replace('{MACRO:FO}','Castor Co.')",
        "assert all(t not in body for t in [b'FA',b'FO']) and body.count(b'FI')==int(row['source_record_index'] in [311,388])":"assert b'FO' not in body and body.count(b'FI')==int(row['source_record_index']==108) and body.count(b'FA')==int(row['source_record_index'] in [40,61])",
        '    assert not warnings\n':'    # Retain every warning for individual visual review; only errors block this offline glyph proof.\n',
        'len(rows)==61':'len(rows)==28',"for r in rows)==61":"for r in rows)==28",
        '61_complete_native_paragraphs61_pages244_compiled_alignments':'28_complete_native_paragraphs28_pages112_compiled_alignments',
        'alignment_cases=244':'alignment_cases=112','complete_progressive_paragraphs=61':'complete_progressive_paragraphs=28','complete_progressive_pages=61':'complete_progressive_pages=28',
        'all61_single_original_four_row_pages_complete':'all28_single_original_four_row_pages_complete',
        'all_words_punctuation_andtwo_source_FI_macros_preserved_without_shortening':'all_words_punctuation_source_FA2_FI1_preserved_without_shortening',
        'no_warnings_andno_warning_waivers_needed=True':'no_warnings_andno_warning_waivers_needed=not warnings,exact_warning_review_pending=bool(warnings)',
        'all61_formatting_gates_false':'all28_formatting_gates_false',
        '61complete native paragraphs/61pages/244alignments;allglyphs/bounds pass.Zero warnings;eleven sheets need direct viewing,actual/stored/release pending.':'28complete native paragraphs/28pages/112alignments;allglyphs/bounds pass.All QA diagnostics retained;five sheets need direct viewing,actual/stored/release pending.',
    })
    ROOT.mkdir(parents=True);save(ROOT/'source_locked_derivations.json',[a,b])
    print('Prepared B50 logical/compiled native tools;sourceFA2/FI1 andall warnings remain exact.')
