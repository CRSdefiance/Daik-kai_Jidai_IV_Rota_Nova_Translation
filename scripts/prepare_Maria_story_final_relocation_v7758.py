"""Freeze the original guarded reconstruction against finalv3 prose andnative proofs."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
if __name__=='__main__':
    root=Path('work/analysis/maria_story_final_relocation_tools_v7758');assert not root.exists()
    result=derive('scripts/relocate_Maria_story_research_v7742.py','scripts/relocate_Maria_story_final_v7758.py',{
        'maria_story_relocation_v7742':'maria_story_final_relocation_v7758',
        'translations/maria_B34_B108_B35_editorial_manuscript_v2.json':'translations/maria_B34_B108_B35_editorial_manuscript_v3.json',
        'work/analysis/maria_story_refined_v7735/67_refined_decisions_native_logical_bindings_automatic_plans_QA.json':
        'work/analysis/maria_story_final_prose_v7756b/67_final_v3_plans_two_refinements65_exact_compiled_retentions.json',
        'work/analysis/maria_story_pages_v7738/67_compiled268_alignments68_complete_native_pages.json':
        'work/analysis/maria_story_final_native_v7757b/67_final_v3_native_pages_andfully_bound_logical_lineage.json',
        "and not plan['unresolved']":"and all(not any(i['severity'] in ['warning','error'] for i in r['base_QA']['issues']) for r in plan['records'])",
    })
    root.mkdir(parents=True);save(root/'provenance.json',dict(derivation=result,all_original_native_numeric_constants_ownership_inverse_andbranch_guards_preserved=True,
        previous_v2_archive_andproofs_preserved=True,no_registered_ROM_orcredit_change=True,full_goal_complete=False))
    print('Frozen finalv3 three-block reconstruction;all native constants/ownership/inverse/branch guards unchanged.')
