"""Revisit the source voices as natural spoken clauses,without fit-only shortening."""
from copy import deepcopy
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save

SOURCE = Path('translations/enemy_capture_editorial_manuscript_v1.json')
OUT = Path('translations/enemy_capture_editorial_manuscript_v2.json')
REVIEW = {
    2082:("We've captured the enemy ship %s!",'Use a complete natural spoken report for the polite capture announcement. The earlier terse naval caption is intelligible,but a voiced character naturally reports the completed action with we have captured. Preserve the named enemy vessel and add no casualties or admiral address.'),
    2083:('Captured enemy ship %s!','Preserve the intentionally clipped Japanese report as a terse English action report. Put captured first in the idiomatic status-report construction and restore enemy,which the old translation omitted. Do not turn this unusually clipped voice into the same conversational sentence as the other officers.'),
    2084:('We captured the enemy ship %s!','Use a complete lively spoken clause for conversational shita yo. The straightforward past-tense announcement preserves the speaker\'s direct energy without adding a boast,casualties or destruction.'),
    2085:("We've captured the enemy ship %s!",'Use natural conversational English for the feminine announcement. A contraction suits spoken dialogue;do not invent a gendered catchphrase from wa.'),
    2086:('We took the enemy ship %s!','Retain the revised complete confident spoken clause for ubatta ze. Took expresses seizure naturally without inventing sinking,crew deaths or a fleet-wide victory.'),
    2087:("We've captured the enemy ship %s!",'Use a complete natural spoken report for the older officer. Preserve the emphatic announcement through the exclamation and avoid fabricating an archaic or pirate accent from zoi.'),
    2088:('We took over the enemy ship %s!','Retain the source-faithful youthful announcement:take over expresses nottotta and enemy restores an omitted fact. The named vessel is the object of this action,not the entire opposing fleet.'),
    2089:('We have captured the enemy ship %s!','Use an uncontracted complete announcement for the formal emphatic shimashita zo voice. The slightly more formal we have differentiates it naturally without adding a rank or an invented fact.')
}

if __name__=='__main__':
    assert not OUT.exists()
    doc = deepcopy(read(SOURCE))
    assert sha(Path(doc['source_context']).read_bytes())==doc['source_context_sha256']
    assert [r['message_id'] for r in doc['records']]==list(REVIEW)
    for row in doc['records']:
        n = row['message_id'];english,note = REVIEW[n]
        assert english.isascii() and english==' '.join(english.split()) and english.count('%s')==1
        assert '%' not in english.replace('%s','') and not any(c in english for c in '{}\n\r\t')
        row['previous_reviewed_english'] = row['english']
        row['english'],row['localization_note'] = english,note
        row['editorial_decision'] = 'revise' if english!=row['current_English'] else 'retain'
        row['review']['formatting'] = False
    assert all(r['editorial_decision']=='revise' for r in doc['records'])
    doc.update(revised=8,retained=0,previous_manuscript=str(SOURCE),previous_manuscript_sha256=sha(SOURCE.read_bytes()),
        source_voice_spoken_English_reconsideration='Full spoken clauses for the seven conversational/formal reports;intentionally clipped action report for2083. No source facts removed and no authored layout. Five earlier caption retentions are reconsidered,not silently relabeled completed.',
        producer_sha256=sha(Path(__file__).read_bytes()))
    save(OUT,doc)
    print('Eight source-faithful paragraphs refined:seven spoken clauses,one intentionally clipped report;all native gates remain open.',flush=True)
