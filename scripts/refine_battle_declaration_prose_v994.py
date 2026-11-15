"""Keep immutable V992 drafts;refine four dynamic sentences after native-name preview."""
from copy import deepcopy
from pathlib import Path
from shutil import copy2

from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/battle_declaration_v994')
OLD = Path('translations/battle_declaration_editorial_manuscript_v1.json')
NEW = Path('translations/battle_declaration_editorial_manuscript_v2.json')
REVISIONS = {
    1897: ('Is it all right to declare war on %s?', 'Keep the complete polite declaration confirmation in one natural question. A company abbreviation may already end in a period;putting the question after the faction label avoids an added second period.'),
    1899: ("Admiral, you're all right with us declaring war on %s?", 'Keep the explicit Admiral address and reassurance-seeking confirmation as conversational English. Place the complete faction label at the end of the question so a name ending Co. does not acquire a second period.'),
    1901: ('Shall we declare war on %s?', 'Keep the older formal shall and the complete declaration confirmation as a natural question. No extra sentence period is appended to a faction label that may already end in Co.'),
    1903: ('Do I have your approval to declare war on %s?', 'Preserve formal approval-seeking and the declaration of war as a complete idiomatic question. Avoid both inverted You approve,yes and an extra period after a complete abbreviated company name.'),
}


def main():
    assert not ROOT.exists() and not NEW.exists()
    before = OLD.read_bytes()
    doc = read(OLD)
    updated = deepcopy(doc)
    changes = []
    for row in updated['records']:
        n = row['message_id']
        if n in REVISIONS:
            english, note = REVISIONS[n]
            assert english.isascii() and english == ' '.join(english.split()) and english.count('%s') == 1
            assert row['editorial_decision'] == 'revise' and not row['review']['formatting']
            changes.append({'message_ID': n, 'previous_English': row['english'], 'new_English': english,
                            'reason': 'Actual native complete-label preview inserted Centurione Co. and exposed a doubled sentence period. This is prose refinement,not manual line positioning.'})
            row['english'], row['localization_note'] = english, note
    assert len(changes) == 4 and sum(r['editorial_decision'] == 'revise' for r in updated['records']) == 13
    ROOT.mkdir(parents=True)
    followup = ROOT/'native_name_preview_followup.json'
    save(followup, {'previous_manuscript': str(OLD), 'previous_manuscript_sha256': sha(before),
        'source_context_proof': doc['native_context_proof'], 'source_context_proof_sha256': doc['native_context_proof_sha256'],
        'source_label': 'Centurione Co.', 'source_label_catalog_entry': 8,
        'changes': changes, 'same_four_source_context_meaning_and_voice_gates_rereviewed': True,
        'all7_single_percent_s_arguments_preserved': True, 'no_new_review_or_completion_count': True,
        'native_font_dynamic_wrap_registered_release_and_actual_scenes_still_pending': True,
        'producer_sha256': sha(Path(__file__).read_bytes())})
    updated.update(reviewed_research_manuscript=str(OLD), reviewed_research_manuscript_sha256=sha(before),
                   native_name_preview_followup=str(followup), native_name_preview_followup_sha256=sha(followup.read_bytes()))
    save(NEW, updated)
    assert OLD.read_bytes() == before
    ledger_path = Path('translations/editorial_review_current_v1.json')
    ledger = read(ledger_path)
    assert ledger['records_with_source_and_prose_pass'] == 1199 and ledger['records_editorially_completed'] == 1174
    save(ROOT/'editorial_ledger_before_prose_followup.json', ledger)
    assert ledger['active_source_prose_drafts']['manuscripts'][-1] == str(OLD)
    ledger['active_source_prose_drafts']['manuscripts'][-1] = str(NEW)
    ledger['battle_declaration_v992']['current_refined_manuscript'] = str(NEW)
    ledger['battle_declaration_v994'] = {'manuscript': str(NEW), 'preview_followup': str(followup),
        'status': 'same22-source-prose-reviewed-four-dynamic-sentences-refined-native-font-release-actual-pending',
        'completed_entries_added': 0, 'source_prose_reviews_added': 0}
    checkpoint = ('V994 refines four of the same22 battle/declaration drafts after native complete-faction-label preview exposed doubled periods after Co. All seven original arguments,source meanings,voices and thirteen-revision/nine-retention decisions remain intact. Historical V992 manuscript is preserved. No new coverage credit;1174 complete,1199 source/prose reviewed;V987 current. Runtime selector research,native fonts,registered release and actual representative scenes remain pending;goal active.')
    ledger['latest_checkpoint'] = checkpoint
    ledger['research_checkpoints'].append({'id': 'V994-battle-declaration-native-name-preview-refinement',
        'proof': str(followup), 'manuscript': str(NEW), 'source_prose_reviews_added': 0, 'completed_entries_added': 0,
        'this_goal_turn_classification': 'progress:four natural dynamic questions refined from observed native faction substitution punctuation',
        'full_goal_complete': False})
    save(ledger_path, ledger)
    doc_path = Path('docs/battle_declaration_v994_preview_refinement.md')
    assert not doc_path.exists()
    with doc_path.open('x', encoding='utf-8') as f:
        f.write('# V994: complete faction-name punctuation refinement\n\n'+checkpoint+'\n\n')
        for row in changes:
            f.write(f"## COMMON {row['message_ID']}\n\n"+row['new_English']+'\n\n'+row['reason']+'\n\n')
    for p in map(Path, ('docs/translation_progress.md', 'docs/editorial_review_goal.md', 'docs/todo.md')):
        with p.open('a', encoding='utf-8') as f:
            f.write('\n\n## V994: battle/declaration punctuation follow-up\n\n'+checkpoint+' See [V994 follow-up](battle_declaration_v994_preview_refinement.md).\n')
    archive = Path('E:/Rota Nova translations/Editorial review/V994 Battle declaration preview refinement')
    assert not archive.exists()
    files = []
    for source in (NEW, followup, Path(__file__), doc_path, ledger_path):
        target = archive/source.absolute().relative_to(Path.cwd())
        target.parent.mkdir(parents=True, exist_ok=True)
        assert not target.exists()
        copy2(source, target)
        assert source.read_bytes() == target.read_bytes()
        files.append({'source': str(source), 'archive': str(target), 'sha256': sha(target.read_bytes())})
    save(ROOT/'archive_manifest.json', {'files': files, 'all_hashes_verified': True, 'no_additional_coverage_credit': True})
    print('Four dynamic questions refined;all22 source/prose reviews preserved.1174 complete,1199 source/prose;formatting/release/actual pending.')


if __name__ == '__main__':
    main()
