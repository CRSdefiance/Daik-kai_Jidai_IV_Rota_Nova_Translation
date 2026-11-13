"""Refine two faithful complete clauses after native orphan-word review."""
from copy import deepcopy
from pathlib import Path
from scripts.verify_village_wrap_v608 import read, save
from scripts.declaration_responses_native_plan_v1535 import compiled
from dk4tool.patch.grand_race_menu_release import sha

OLD = Path('translations/declaration_responses_editorial_manuscript_v1.json')
NEW = Path('translations/declaration_responses_editorial_manuscript_v2.json')

if __name__ == '__main__':
    assert not NEW.exists()
    doc = deepcopy(read(OLD))
    changes = {
        2201: ("They're declaring war?! Then we'll have to accept their challenge!",
               'Use the idiomatic have to accept their challenge to preserve surprise,resignation and willingness to respond. This keeps all source intent and avoids the separated Very/well and orphan challenge in the first native preview;no manual break or alignment is authored.'),
        2208: ("Hmph! You've declared war?! I'll see to it that you regret that reckless decision!",
               'Use the natural emphatic promise see to it that you regret to express the original causative threat and retain the explicit reckless decision. This is a longer full source-faithful clause,not a fit-only abbreviation;native wrapping keeps reckless decision together without authored layout.'),
    }
    for row in doc['records']:
        if row['message_id'] in changes:
            row['english'], note = changes[row['message_id']]
            row['localization_note'] += ' ' + note
        assert not row['review']['formatting']
        compiled(row)
    doc.update(supersedes=str(OLD), supersedes_sha256=sha(OLD.read_bytes()),
        status='eight-source-context-prose-refined;native-font-visual-release-original-event-pending',
        producer_sha256=sha(Path(__file__).read_bytes()))
    save(NEW, doc)
    print('Two source-faithful refinements preserve all facts and resolve the first-pass orphan phrases;formatting still pending.')
