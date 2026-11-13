"""Source-lock the full216px automatic planner without changing old QA or prose."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save

if __name__ == '__main__':
    root = Path('work/analysis/Hodram_B51_layout_tools_v8562')
    assert not root.exists()
    result = derive('scripts/plan_Hodram_B50_v8491b.py', 'scripts/plan_Hodram_B51_v8562.py', {
        'Hodram_B50_layout_v8491b': 'Hodram_B51_layout_v8562',
        'translations/hodram_B50_editorial_manuscript_v1.json': 'translations/hodram_B51_editorial_manuscript_v1.json',
        'work/analysis/Hodram_B50_logical_v8490/logical_paragraphs.json': 'work/analysis/Hodram_B51_logical_v8561/logical_paragraphs.json',
        "assert (row['kind']=='progressive' and row['source_selector']==2) or (row['kind']=='system-FE' and row['source_selector']==254)":
            "assert row['kind']=='progressive' and row['source_selector'] in [1,16,18,113]",
        '"row[\'source_selector\'] in [2]"': '"row[\'source_selector\'] in [1,16,18,113]"',
        'Hodram B50 plan:': 'Hodram B51 plan:',
        'Hodram-B50-RESEARCH-ONLY:': 'Hodram-B51-RESEARCH-ONLY:',
        "|{('here','take'),('take','this')}": "|{('southern','mediterranean'),('my','advice'),('better','off'),('off','leaving'),('bad','news'),('your','own'),('own','good'),('another','sea'),('what','do'),('do','you'),('you','mean')}",
        "logical['fresh_native_alignment_cases']==12 and len(doc['records'])==3": "logical['fresh_native_alignment_cases']==20 and len(doc['records'])==5",
        'assert not failures and len(rows)==3': 'assert not failures and len(rows)==5',
        'FE_usable216_bitmap228_distinction_from_original32_boundary_measurements=True': 'all_progressive216_bitmap_andusable_width_no_FE_panel=True',
    })
    root.mkdir(parents=True)
    save(root / 'derivation.json', dict(derivation=result, all_original_native_constants_andmultiplicity_preserved=True,
        original_full216px_width_font_macro_lengths_pair_phase_andQA_unchanged=True,
        scoped_coherent_phrase_preferences_are_planner_costs_not_authored_breaks=True,
        no_manual_prose_breaks_padding_shortening_waiver_ROM_write_orcredit=True))
