"""Fresh native context against current genuine pre-interaction V2171 RAM."""
from pathlib import Path
import sys
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import save

mode = sys.argv[1]
assert mode in ('recruitment','schemes','followup')
current = 'out/all_routes_combined_v2171_candidate.nds'
report = 'E:/Rota Nova translations/Generated/work/emulation_v193/tavern_direct_actual_v2190_V2171/capture_report.json'
if mode == 'recruitment':
    original = Path('scripts/context_tavern_recruitment_v771.py')
    root = Path('work/analysis/tavern_recruitment_context_v2196')
    substitutions = {
        'work/analysis/tavern_recruitment_editorial_v771': str(root).replace('\\','/'),
        'out/all_routes_combined_v770_candidate.nds': current,
        'E:/Rota Nova translations/Generated/work/emulation_v193/tavern_round_v770_accept_v770/capture_report.json': report,
        'from dk4tool.script.common_message_table import common_message_entries': 'from dk4tool.patch.town_trade_port_contextual_reference_v1 import current_entries as common_message_entries',
        ',arm,clean=False)': ',arm)',
    }
elif mode == 'schemes':
    original = Path('scripts/context_tavern_schemes_v774.py')
    root = Path('work/analysis/tavern_schemes_context_v2197')
    substitutions = {
        'work/analysis/tavern_schemes_editorial_v774': str(root).replace('\\','/'),
        'out/all_routes_combined_v773_candidate.nds': current,
        'E:/Rota Nova translations/Generated/work/emulation_v193/condition_rumor_v774_second_round_live/capture_report.json': report,
    }
else:
    original = Path('scripts/context_scheme_followup_v777.py')
    root = Path('work/analysis/tavern_followup_context_v2198')
    substitutions = {
        'from scripts.review_scheme_followup_v777 import ROOT, CURRENT, TABLES': "from scripts.review_scheme_followup_v777 import TABLES\nROOT=Path('work/analysis/tavern_followup_context_v2198')\nCURRENT=Path('"+current+"')",
        'E:/Rota Nova translations/Generated/work/emulation_v193/schemes_v776_qualified_live/capture_report.json': report,
    }
assert not root.exists()
source = original.read_text()
counts = {}
for before, after in substitutions.items():
    counts[before] = source.count(before)
    assert counts[before] in (1,2), (before,counts[before])
    source = source.replace(before, after)
namespace = {'__name__':'__main__','__file__':__file__}
exec(compile(source,__file__,'exec'),namespace)
save(root/'fresh_replay_provenance.json',dict(mode=mode,original_source=str(original),original_source_sha256=sha(original.read_bytes()),effective_source_sha256=sha(source.encode()),exact_substitution_counts=counts,current_ROM=current,current_report=report,unchanged_original_context_producer=True,no_runtime_functions_or_UI_returns_rewritten=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
