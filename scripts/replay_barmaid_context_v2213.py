"""Original city/actor/name providers on current genuine preinteraction RAM."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import save

original=Path('scripts/context_barmaid_dialogue_v779.py')
source=original.read_text()
for old,new in (
    ('work/analysis/barmaid_editorial_v779','work/analysis/barmaid_context_v2213'),
    ('out/all_routes_combined_v778_candidate.nds','out/all_routes_combined_v2171_candidate.nds'),
    ('followup_v778_bribe_live/capture_report.json','recruitment_actual_v2202_V2171/capture_report.json'),
):
    assert source.count(old)==1,old
    source=source.replace(old,new)
root=Path('work/analysis/barmaid_context_v2213')
assert not root.exists()
env={'__name__':'__main__','__file__':__file__}
exec(compile(source,__file__,'exec'),env)
save(root/'replay_provenance.json',dict(source=str(original),source_sha256=sha(original.read_bytes()),effective_source_sha256=sha(source.encode()),producer_sha256=sha(Path(__file__).read_bytes()),original_branches_and_native_getters_unchanged=True,no_fixture_or_earned_gameplay_credit=True,latent996_normal_reachability_requires_separate_bound_closure=True))
