"""Consolidate scoped UI consumer evidence without implying integration/runtime."""

import json
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha

REPORTS = ('grand_race_menu_label_layout', 'grand_race_region_player_layout_v136',
           'grand_race_status_layout', 'grand_race_results_layout',
           'grand_race_wireless_screens', 'grand_race_wireless_roles',
           'grand_race_wireless_return', 'grand_race_final_labels_v136', 'grand_race_result_rows')


def values(document):
    ids, texts = set(), set()
    def visit(value):
        if isinstance(value, dict):
            if isinstance(value.get('id'), str):
                ids.add(value['id'])
            for key in ('english', 'complete_english', 'header'):
                if isinstance(value.get(key), str):
                    texts.add(value[key])
            for child in value.values():
                visit(child)
        elif isinstance(value, list):
            for child in value:
                visit(child)
    visit(document)
    return ids, texts


def main():
    path = Path('translations/grand_race_remaining_ui_manuscript_v2.json')
    manuscript = json.loads(path.read_text(encoding='utf-8'))
    manuscript_sha = sha(path.read_bytes())
    indexed, reports = {}, []
    for name in REPORTS:
        report_path = Path('work/qa') / name / 'report.json'
        document = json.loads(report_path.read_text())
        if document['manuscript_sha256'] != manuscript_sha:
            raise ValueError('Consumer evidence manuscript is stale')
        indexed[name] = values(document)
        reports.append({'path': report_path.as_posix(), 'sha256': sha(report_path.read_bytes())})
    integrated = set()
    for batch_path in ('translations/grand_race_transition_status_arm9_v2.json', 'translations/grand_race_menu_arm9_v2.json'):
        integrated.update(r['id'] for r in json.loads(Path(batch_path).read_text())['records'])
    records = []
    for row in manuscript['records']:
        name = row['id'].removeprefix('GRAND_RACE_UI_')
        conditional = name.startswith(('PLACE_', 'NUMBER_'))
        evidence = [report for report, (ids, texts) in indexed.items() if row['id'] in ids or row['english'] in texts]
        if name == 'ROLES':
            evidence.append('grand_race_wireless_roles')
        if conditional:
            evidence.append('grand_race_result_rows')
        if not evidence:
            raise ValueError(f'Scoped message still lacks consumer evidence: {name}')
        limits = ['Physical screen routing, complete widget/runtime execution and release integration remain separate gates.']
        if conditional:
            limits.append('Result-row name limit/termination and proposed wider frame remain conditional; no unconditional formatting gate.')
        if name == 'HOST_SELECTING':
            limits.append('Original two-line layout fails; reviewed third-widget rewrite/allocation must be integrated.')
        records.append({'id': row['id'], 'english': row['english'], 'source_parts': len(row['source_parts_in_reading_order']),
                        'consumer_evidence': sorted(set(evidence)), 'integrated_in_V136': row['id'] in integrated,
                        'conditional_result_row': conditional, 'limitations': limits})
    output = Path('work/analysis/grand_race_ui_coverage_v136.json')
    report = {'scope': '51-message Grand Race manuscript, not exhaustive ARM9/UI inventory',
              'manuscript_sha256': manuscript_sha, 'evidence_reports': reports, 'records': records,
              'message_count': len(records), 'source_part_count': sum(r['source_parts'] for r in records),
              'messages_with_consumer_evidence': len(records), 'integrated_messages': len(integrated),
              'conditional_result_messages': sum(r['conditional_result_row'] for r in records),
              'runtime_verified': False, 'goal_complete': False}
    output.write_text(json.dumps(report, indent=2) + '\n')
    print('51/51 scoped messages have consumer evidence; eight integrated, eight conditional result labels; runtime/integration still pending.')


if __name__ == '__main__':
    main()
