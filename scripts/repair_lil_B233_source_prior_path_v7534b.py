"""Restore the immutable historical adapter filename; retain the failed producer."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive,checked_text
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B233_source_prior_tools_v7534b')
if __name__=='__main__':
    assert not ROOT.exists() and not Path('work/analysis/lil_B233_source_pages_v7534').exists()
    jobs=[('scripts/prove_lil_B233_source_pages_v7534.py','scripts/prove_lil_B233_source_pages_v7534b.py',{'source_pages_v7534':'source_pages_v7534b','lil_B222_native_pages_v7047/all11_paragraphs16_complete_native_pages128_alignments.json':'lil_B222_native_pages_v7047/all16_paragraphs16_complete_native_pages128_alignments.json'}),('scripts/audit_lil_B233_source_v7535.py','scripts/audit_lil_B233_source_v7535b.py',{'source_actual_v7535':'source_actual_v7535b','source_pages_v7534':'source_pages_v7534b'})]
    for a,b,c in jobs:assert not Path(b).exists();checked_text(Path(a).read_text('utf8'),c)
    rows=[derive(*j) for j in jobs];ROOT.mkdir(parents=True);save(ROOT/'source_locked_historical_prior_path_repair.json',dict(tools=rows,first_source_page_reader_failed_before_output_orapproval=True,historical_B222_all16_adapter_filename_restored_only=True,B233_eleven_record_obligations_unchanged=True,no_ROM_input_runtime_font_geometry_prose_orcredit_change=True,failed_producer_preserved_not_negative_rejection=True,new_credit=0,full_goal_complete=False))
