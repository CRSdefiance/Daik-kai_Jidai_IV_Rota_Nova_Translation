"""Rebind the actual scheme name-input contract; do not mistake editor stress for eligibility."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import save
original=Path('scripts/verify_scheme_input_contract_v776.py')
root=Path('work/analysis/current_scheme_input_contract_v2199')
assert not root.exists()
source=original.read_text()
changes={
 'work/analysis/tavern_schemes_integration_v776':'work/analysis/current_scheme_input_contract_v2199',
 'out/all_routes_combined_v773_candidate.nds':'out/all_routes_combined_v2171_candidate.nds',
 'work/analysis/tavern_schemes_editorial_v774/native_context.json':'work/analysis/tavern_schemes_context_v2197b/native_context.json',
}
counts={}
for before,after in changes.items():
 counts[before]=source.count(before);assert counts[before]==1
 source=source.replace(before,after)
exec(compile(source,__file__,'exec'),{'__name__':'__main__','__file__':__file__})
save(root/'replay_provenance.json',dict(original=str(original),original_sha256=sha(original.read_bytes()),effective_source_sha256=sha(source.encode()),replacement_counts=counts,current_native_names_and_initializers_verified=True,source_exclusion_cases_inherited_only_under_unchanged_private_call_paths=True,no_general_older_record_technical_reaudit_claim=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
