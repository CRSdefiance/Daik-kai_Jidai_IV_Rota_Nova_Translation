"""Rereview natural clauses for name-bearing reports across the captured cap."""
from copy import deepcopy
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save

OLD = Path('translations/ship_sinking_editorial_manuscript_v2.json')
OUT = Path('translations/ship_sinking_editorial_manuscript_v3.json')


def main():
    assert not OUT.exists()
    doc = deepcopy(read(OLD))
    bound = Path('work/analysis/ship_name_bound_v1335b/original_ship_rename_capacity.json')
    assert read(bound)['max_name_bytes_excluding_NUL']==18
    changes = {
        2059:('Admiral, %s is going under...',
              'Going under is idiomatic nautical English for the source ongoing sinking. Preserve the address,progressive action and trailing distressed pause. No completed sinking or crew fate is added.'),
        2066:('The enemy ship %s has been sunk!',
              'Use a complete natural report identifying the enemy ship before the result. The passive suits the polite source;the original firing-ship context supplies our agency without adding an attacker name or fleet victory.'),
        2069:('The enemy ship %s has been sunk!',
              'Use the natural complete sinking announcement,keeping the named enemy vessel and emphasis. The passive changes English sentence order without changing the source event or inventing gendered speech.'),
        2070:('We did it! The enemy ship %s has gone down!',
              'Preserve the rough triumphant We did it followed by the specific enemy sinking. Has gone down is idiomatic nautical English;do not claim defeat of the whole fleet or deaths.'),
        2071:('The enemy ship %s has been sunk!',
              'Use a clear complete report for the older voice without an artificial dialect. The named enemy vessel and completed sinking are preserved;our shot remains established by the original caller.'),
        2072:('Enemy ship %s has gone down!',
              'Use a short excited report with the original enemy identification. Has gone down expresses sinking naturally rather than a status-label fragment;no additional damage or outcome is invented.')}
    for row in doc['records']:
        if row['message_id'] in changes:
            row['english'],row['localization_note'] = changes[row['message_id']]
            row['editorial_decision'] = 'revise'
            row['review']['formatting'] = False
    doc.update(revised=8,retained=8,supersedes_manuscript=str(OLD),supersedes_manuscript_sha256=sha(OLD.read_bytes()),
        supported_ship_name_capacity_proof=str(bound),supported_ship_name_capacity_proof_sha256=sha(bound.read_bytes()),
        source_context_localization_and_naturalness_rereviewed=True,
        formatting_review_pending=True,producer_sha256=sha(Path(__file__).read_bytes()))
    assert sum(r['editorial_decision']=='revise' for r in doc['records'])==8
    save(OUT,doc)
    print('V3:all16 Japanese meanings and voices rereviewed;eight natural revisions,eight retentions. No native-formatting approval yet.',flush=True)


if __name__=='__main__':
    main()
