"""Natural source-faithful revisions prompted by exact native line endings."""
from copy import deepcopy
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from scripts.battle_aftermath_native_plan_v1255 import compiled
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/battle_aftermath_refinement_v1258')
OLD = Path('translations/battle_aftermath_editorial_manuscript_v1.json')
NEW = Path('translations/battle_aftermath_editorial_manuscript_v2.json')
REVISIONS = {
    1995: ('%s surrendered, Admiral!',
        'Preserve the excited surrender report and direct address. Moving Admiral to the end is natural English and keeps all114 actual town names together with a complete report in one native row; no source fact or tone is lost.'),
    2000: ('The enemy flagship is destroyed!',
        'Preserve the formal completed-action report about the enemy flagship. The present result is faithful to 撃破しました and reads naturally without stranding destroyed on a second row.'),
    2024: ("There's no point fighting! Give up!",
        'Preserve the youthful, direct warning that further fighting is pointless and the demand to surrender. Give up is natural spoken English for 降参して in this voice; both complete clauses remain together.'),
    2029: ('You cannot win! Surrender at once!',
        'Preserve the composed declaration that victory is impossible and the urgent surrender demand. At once conveys 一刻も早く naturally while keeping the complete imperative together.'),
}


def main():
    assert not ROOT.exists() and not NEW.exists()
    old = read(OLD)
    font_path = Path('work/analysis/battle_aftermath_fonts_v1256b/native_font_proof.json')
    font = read(font_path)
    assert font['manuscript_sha256'] == sha(OLD.read_bytes()) and len(font['cases']) == 783
    doc,changes = deepcopy(old),[]
    for row in doc['records']:
        n = row['message_id']
        if n in REVISIONS:
            english,note = REVISIONS[n]
            assert row['source_Japanese'] and row['source_meaning']
            changes.append({'message_ID':n,'Japanese':row['source_Japanese'],'before':row['english'],
                'after':english,'source_meaning':row['source_meaning'],'reason':note})
            row['english'] = english
            row['editorial_decision'] = 'revise'
            row['localization_note'] = note+' Native formatting must be retested; no authored line breaks or alignment.'
            row['unwrapped_paragraph_hex'] = english.encode('ascii').hex()
        assert not row['review']['formatting']
        compiled(row)
    assert sum(r['editorial_decision']=='revise' for r in doc['records']) == 58
    assert sum(r['editorial_decision']=='retain' for r in doc['records']) == 17
    doc.update(reviewed_predecessor=str(OLD),reviewed_predecessor_sha256=sha(OLD.read_bytes()),
        native_line_boundary_research=str(font_path),native_line_boundary_research_sha256=sha(font_path.read_bytes()),
        status='75-source-prose-reviewed-with4-native-boundary-refinements;formatting-retest-pending')
    ROOT.mkdir(parents=True)
    save(NEW,doc)
    save(ROOT/'source_prose_refinement.json',{'previous_manuscript':str(OLD),'previous_sha256':sha(OLD.read_bytes()),
        'new_manuscript':str(NEW),'new_sha256':sha(NEW.read_bytes()),'changes':changes,
        'source_prose_records':75,'revised':58,'retained':17,'all_formatting_gates_still_false':True,
        'no_source_credit_duplicated_or_ROM_completion_change':True,
        'producer_sha256':sha(Path(__file__).read_bytes()),'full_goal_complete':False})
    ledger_path = Path('translations/editorial_review_current_v1.json')
    ledger = read(ledger_path)
    assert ledger['records_editorially_completed'] == 1260 and ledger['records_with_source_and_prose_pass'] == 1373
    drafts = ledger['active_source_prose_drafts']
    assert drafts['manuscripts'].count(str(OLD).replace('\\','/'))+drafts['manuscripts'].count(str(OLD)) >= 1
    drafts['manuscripts'] = [str(NEW) if p.replace('\\','/') == OLD.as_posix() else p for p in drafts['manuscripts']]
    ledger['battle_aftermath_v1258_refinement'] = {'proof':str(ROOT/'source_prose_refinement.json'),
        'manuscript':str(NEW),'source_prose_records':75,'revised':58,'retained':17,
        'formatting_native_copy_integration_actual_scenes_pending':True,'completed_entries_added':0}
    save(ledger_path,ledger)
    print('Four faithful prose refinements;75 drafts now58 revised17 retained. All formatting approvals pending.',flush=True)


if __name__ == '__main__':
    main()
