"""Keep the exact grammatical boundary; the unchanged base audit requires no waiver."""
from copy import deepcopy
from pathlib import Path
from scripts.audit_story_glyph_consistency import load, save
from dk4tool.patch.grand_race_menu_release import sha

ROOT = Path('work/analysis/Hodram_B191_B210_formatting_20261104')

if __name__ == '__main__':
    before = ROOT / 'guard_and_opening_preferences_v3.json'
    output = ROOT / 'guard_and_opening_preferences_v4.json'
    assert not output.exists()
    doc = deepcopy(load(before))
    row = doc['records']['DK4_MES_B201_R0074']
    prior = row.pop('QA_line_ending_retention')
    row.update(grammatical_boundary_reason=prior['reason'], no_QA_waiver_required_or_applied=True,
        diagnostic_two_lines=["I'd like to buy it from you, but", "I don't have that kind of money."],
        unchanged_base_QA_issues_for_exact_two_line_result=[])
    doc.update(previous_preferences=str(before), previous_preferences_sha256=sha(before.read_bytes()),
        no_base_QA_diagnostics_suppressed=True, unused_v19_retention_runner_not_required=True)
    save(output, doc)
