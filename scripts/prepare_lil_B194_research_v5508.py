"""Prepare exact-parent one-block research, whole loaders, four-branch census and guarded ends."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save

ROOT = Path('work/analysis/lil_B194_research_tools_v5508')
PARENT = Path('out/all_routes_combined_v5478_candidate.nds')
ROM = Path('out/lil_B194_reference_v5509_RESEARCH_ONLY.nds')
PLAN = Path('work/analysis/lil_B194_relocation_v5506b/nested_source_relocation_research.json')

if __name__ == '__main__':
    assert not ROOT.exists()
    shared = {'B193': 'B194', 'prepare_lil_B193_research_v5463': 'prepare_lil_B194_research_v5508'}
    rows = [derive('scripts/create_lil_B193_reference_v5464.py', 'scripts/create_lil_B194_reference_v5509.py', {
        **shared, 'research_v5464': 'research_v5509', 'stored_v5462': 'stored_v5507',
        'all15': 'all11', 'targets60': 'targets44', 'verification_v5443': 'verification_v5505',
        "stored['current_final_stored_macro_alignment_cases']==60": "stored['current_final_stored_macro_alignment_cases']==44",
        'current_final_stored_macro_alignment_cases=60': 'current_final_stored_macro_alignment_cases=44',
        '==[193]': '==[194]', 'V5437': 'V5478',
    })]
    rows.append(derive('scripts/verify_lil_B193_loader_v5465.py', 'scripts/verify_lil_B194_loader_v5510.py', {
        **shared, 'loader_v5465': 'loader_v5510', 'research_v5464': 'research_v5509',
        'work/analysis/lil_B192_loader_v5424/whole_SC2_and_B192_initial_entry_proof.json':
        'work/analysis/lil_B193_loader_v5465/whole_SC2_and_B193_initial_entry_proof.json', 'V5437': 'V5478',
    }))
    rows.append(derive('scripts/verify_lil_B193_references_v5466.py', 'scripts/verify_lil_B194_references_v5511.py', {
        **shared, 'reference_census_v5466': 'reference_census_v5511', 'loader_v5465': 'loader_v5510',
        '[193]': '[194]', '18-command/no-relative-site': '21-command/four-relative-site',
        "sum(len(r['mapped_commands'])for r in result)==18": "sum(len(r['mapped_commands'])for r in result)==21",
        "sum(r['typed_relative_span_count']for r in result)==0": "sum(r['typed_relative_span_count']for r in result)==4",
        "sum(r['target_native_skip_cases']for r in result)==0": "sum(r['target_native_skip_cases']for r in result)==20",
        'all18_commands_no_relative_sites': 'all21_commands_four_relative_sites',
        'all18_clean_current_target_commands_and_no_relative_sites_reexecuted': 'all21_clean_current_target_commands_and_four_relative_sites_reexecuted',
        'native_commands_each=18,relative_sites=0,target_native_skip_cases=0': 'native_commands_each=21,relative_sites=4,target_native_skip_cases=20',
    }))
    rows.append(derive('scripts/prove_lil_B193_ends_v5467.py', 'scripts/prove_lil_B194_ends_v5512.py', {
        **shared, 'ends_v5467': 'ends_v5512', 'n==193': 'n==194',
        'two_declared_tail_end_decodes_no_relative_sites': 'two_declared_tail_end_decodes_four_relative_sites',
    }))
    ROOT.mkdir(parents=True)
    save(ROOT / 'prepared_tools.json', dict(tools=rows, parent=str(PARENT), research=str(ROM), plan=str(PLAN),
        source_stored_logical=[540, 540], target_stored_logical=[516, 514], source_tailzeros=0, target_tailzeros=2,
        commands=21, speeches=11, progressive=10, FE=1, FI=1, relative_sites=4, predicates=1,
        predicate_source312_target274_alignment_changed=True, resource42_source406_target376=True,
        C200_source494_534_target464_508=True, end_source536_target510=True,
        parent_loader_reuse_requires_exact_whole_ROM_hash=True, new_emulator_runs=0, new_review_credit=0,
        full_goal_complete=False))
