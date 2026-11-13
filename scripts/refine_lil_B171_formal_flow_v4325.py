"""Rephrase two complete formal speeches without changing facts or wrap guards."""
from copy import deepcopy
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.prepare_lil_B156_layout_v3705 import derive
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/lil_B171_formal_flow_v4325')
INPUT = Path('translations/lil_B171_editorial_manuscript_v1.json')
OUTPUT = Path('translations/lil_B171_editorial_manuscript_v2.json')

if __name__ == '__main__':
    assert not ROOT.exists() and not OUTPUT.exists()
    doc = deepcopy(read(INPUT))
    changes = {
        44: ("Without our teacher's permission, she left the mountain to escape training, and even went abroad. It is inexcusable.",
             'Move the lack of teacher permission to the front while preserving leaving the mountain to escape training,foreign travel and the visitor\'s condemnation. This resolves the stranded our without shortening meaning or adding a new punishment.'),
        55: ("She was expelled from our school for the grave offense of going abroad. I could not bring her back even if I wished to.",
             'State the expulsion and grave offense first,then the inability even if he wished otherwise. The national travel prohibition is explicit in R48. This preserves every source fact and resigned condition while avoiding stranded if/has;school remains the training institution,not an invented name or further legal penalty.'),
    }
    for row in doc['records']:
        index = row['source_record_index']
        if index in changes:
            body, reason = changes[index]
            row['previous_full_meaning_paragraph'] = row['english']
            row['english'] = '{SPEAKER:51}' + body
            row['localization_note'] += ' ' + reason
            assert row['editorial_decision'] == 'revise'
    doc.update(previous_manuscript=str(INPUT), previous_manuscript_sha256=sha(INPUT.read_bytes()),
        phrase_flow_findings_from_first_plan_resolved_without_waiver=True)
    save(OUTPUT, doc)
    tools = [derive('scripts/plan_lil_B171_layout_v4323.py', 'scripts/plan_lil_B171_layout_v4326.py', {
        'lil_B171_layout_v4323': 'lil_B171_layout_v4326',
        'editorial_manuscript_v1': 'editorial_manuscript_v2', 'editorial_manuscript_v2': 'editorial_manuscript_v3',
    })]
    tools.append(derive('scripts/verify_lil_B171_fonts_v4324.py', 'scripts/verify_lil_B171_fonts_v4327.py', {
        'lil_B171_fonts_v4324': 'lil_B171_fonts_v4327', 'editorial_manuscript_v2': 'editorial_manuscript_v3',
    }))
    ROOT.mkdir(parents=True)
    save(ROOT / 'source_reconciliation_and_successors.json', dict(manuscript=str(OUTPUT), manuscript_sha256=sha(OUTPUT.read_bytes()),
        earlier_failed_plan='work/analysis/lil_B171_layout_v4323/all37_paragraph_layout_QA.json',
        revised_records=[44,55], source_facts_and24_revision13_retention_counts_preserved=True,
        no_guard_metrics_profile_or_protected_boundary_changes=True, tools=tools,
        evidence={str(p): sha(p.read_bytes()) for p in [INPUT,Path(__file__)]}, full_goal_complete=False))
