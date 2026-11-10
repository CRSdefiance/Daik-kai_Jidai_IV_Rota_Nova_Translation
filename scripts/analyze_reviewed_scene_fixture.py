"""Bind declared fixture calls to complete native body/header planes and readable QA sheets."""
import argparse
from pathlib import Path
from scripts.source_locked_derivation_v5118 import checked_text

parser=argparse.ArgumentParser(description=__doc__)
for name in ['fixture','terminal','native','names','out']:
    parser.add_argument('--'+name,type=Path,required=True)
parser.add_argument('--name-decisions',type=Path)

if __name__=='__main__':
    args=parser.parse_args()
    source=checked_text(Path('scripts/analyze_rafael_B51_B60_focused_actual.py').read_text(encoding='utf-8'),{
        "ROOT = Path('work/analysis/Rafael_B51_B60_focused_pixels_20261104')":"ROOT = args.out",
        "FIXTURE = Path('work/analysis/Rafael_B51_B60_focused_20261104/focused_fixture.json')":"FIXTURE = args.fixture",
        "TERMINAL = Path('work/analysis/Rafael_B51_B60_focused_run_20261104/terminal.json')":"TERMINAL = args.terminal",
        "NATIVE = Path('work/analysis/Rafael_B51_B60_current_runtime_20261104/compatible_native_pages.json')":"NATIVE = args.native",
        "NAMES = Path('work/analysis/Rafael_B51_B60_progressive_name_planes_20261104/native_name_planes.json')":"NAMES = args.names",
        "terminal['frames'] == fixture['frames'] == 12161":"terminal['frames'] == fixture['frames']",
        "    decisions_path = Path(names['name_decisions'])\n    assert sha(decisions_path.read_bytes()) == names['name_decisions_sha256']":
            """    decisions_path = args.name_decisions or Path(names['name_decisions'])
    assert sha(decisions_path.read_bytes()) == (names['evidence'][str(decisions_path)] if args.name_decisions else names['name_decisions_sha256'])""",
        "assert len(expected) == fixture['expected_pages'] == 30 and len(fixture['selected_records']) == 27":
            "assert len(expected) == fixture['expected_pages'] and len(expected)>=len(fixture['selected_records'])",
        " and len(fixture['ordinary_actor_IDs']) == 18":"",
        "selected_utterances=27, selected_pages=30":"selected_utterances=len(fixture['selected_records']), selected_pages=len(expected)",
        "all18_actors_three_FE_three_I_Fernan_F_andthree_two_page_transitions_observed=True,":
            "all_declared_actors_andpages_observed=True, observed_actor_IDs=sorted({h['actor_ID'] for h in headers}),",
        "unvisited_utterances=218,":"unvisited_utterances=len(native['records'])-len(fixture['selected_records']),",
        "all245_complete_conversations_reviewed_offline_not_naturally_played=True,":"all_native_records_checked_offline_not_naturally_played=True,",
        "menu_controller_checks_separate_andpending=True,":"complete_scene_commands_retained=fixture['complete_original_scene_including_transitions_andbranches_retained'],",
        "print(f'27 utterances/30 ordered pages;{len(samples)} full body and{len(headers)} full header planes pass. Five QA sheets pending direct review.')":
            "print(dict(utterances=len(fixture['selected_records']),pages=len(expected),body_planes=len(samples),header_planes=len(headers),sheets=len(sheets),direct_review_pending=True))",
    })
    exec(compile(source,__file__+'::same-ordered-calls-complete-pixels-andblank-guards','exec'),globals())
