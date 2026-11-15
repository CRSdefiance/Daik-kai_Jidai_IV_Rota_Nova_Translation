"""Keep gone missing together through one reviewed ordinary auxiliary boundary."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import checked_text,derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B221_wrap_tools_v6985')
if __name__=='__main__':
    assert not ROOT.exists()
    jobs=[('scripts/plan_lil_B221_layout_v6976b.py','scripts/plan_lil_B221_layout_v6976c.py',{
        'layout_v6976b':'layout_v6976c',
        '            candidate=((cost[0]+tiny':
        "            if row['id']=='DK4_MES_B221_R0067' and pair==('had','gone'):weak=0\n            candidate=((cost[0]+tiny"}),
        ('scripts/verify_lil_B220_native_pages_v6928b.py','scripts/verify_lil_B221_native_pages_v6980c.py',{
            'B220':'B221','layout_v6927b/seventeen_whole_paragraph_plans_no_macros_no_prose_changes':
            'layout_v6976c/fourteen_whole_paragraph_plans_no_macros_no_prose_changes',
            'native_pages_v6928/all17_paragraphs17_complete_native_pages136_alignments':
            'native_pages_v6980b/all14_paragraphs16_complete_native_pages112_alignments',
            'native_pages_v6928b':'native_pages_v6980c',
            'current_V6910_native_v6920':'current_V6956_native_v6966',
            'from scripts import verify_lil_B220_native_pages_v6928 as original':
            'from scripts import verify_lil_B221_native_pages_v6980b as original',
            "len(plan['records'])==17":"len(plan['records'])==14",
            "DK4_MES_B220_R0035":"DK4_MES_B221_R0067",'[28,28,29,13]':'[33,24,35,33]',
            '[26,199]':'[2,17,85]',
            'reused==132 and fresh==4 and len(cases)==len(pictures)==17':
            'reused==108 and fresh==4 and len(cases)==14 and len(pictures)==16',
            'all17_complete_pages_sheet':'all14_complete_pages_sheet',
            'complete_pages_reused=16':'complete_pages_reused=15',
            'all17_paragraphs_and_136_alignment_cases_bound_without_repeating_unchanged_checks':
            'all14_paragraphs_and_112_alignment_cases_bound_without_repeating_unchanged_checks',
            'all17_paragraphs17_complete_native_pages136_alignments':'all14_paragraphs16_complete_native_pages112_alignments',
            '17 complete pages/136 alignments:132 exact cases reused,4 fresh compiled cases;only R35 wrap changes,unchanged prose/native geometry.':
            '14 paragraphs/16 pages/112 alignments:108 exact cases reused,4 fresh compiled cases;only R67 wrap changes,unchanged prose/native geometry.'}),
    ]
    for source,target,changes in jobs:
        assert not Path(target).exists();checked_text(Path(source).read_text('utf-8'),changes)
    rows=[derive(source,target,changes) for source,target,changes in jobs]
    ROOT.mkdir(parents=True)
    save(ROOT/'one_source_bound_auxiliary_boundary_no_prose_or_page_change.json',dict(derivations=rows,
        record_ID='DK4_MES_B221_R0067',exact_boundary=['had','gone'],
        reason='This ordinary complete-word wrap separates the past-perfect auxiliary had from its complement. It keeps gone missing together on the following row, preserves all wording and four rows, and avoids treating every auxiliary boundary as a reason for another short row. The exception is restricted to this exact source-bound paragraph; all native glyph,guard,bounds and page checks remain.',
        original_plans_and_all_native_proofs_preserved=True,no_prose_or_viewport_or_native_instruction_change=True,
        no_global_weak_boundary_or_literal_I_rule_change=True,new_review_credit=0,full_goal_complete=False))
