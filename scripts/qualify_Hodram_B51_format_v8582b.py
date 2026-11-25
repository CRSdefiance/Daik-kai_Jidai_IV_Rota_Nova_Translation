"""Correct one alignment-count sentence; preserve approval results and old evidence."""
from copy import deepcopy
from pathlib import Path
from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/Hodram_B51_format_v8582b')
OLD = Path('translations/hodram_B51_editorial_manuscript_v4.json')
DOC = Path('translations/hodram_B51_editorial_manuscript_v5.json')
APPROVAL = Path('work/analysis/Hodram_B51_format_v8582/formatting_approval.json')

if __name__ == '__main__':
    assert not ROOT.exists() and not DOC.exists()
    old, approval = map(read, [OLD, APPROVAL])
    assert approval['manuscript_sha256'] == sha(OLD.read_bytes())
    doc = deepcopy(old)
    row = next(r for r in doc['records'] if r['id'] == 'DK4_MES_B51_R0032')
    before = row['formatting_approval_reason']
    phrase = 'twenty relevant guarded alignments across stages'
    assert before.count(phrase) == 1
    row['formatting_approval_reason'] = before.replace(phrase, 'four guarded alignments per logical or compiled body, with byte-identical stored-body evidence explicitly reused')
    doc.update(predecessor_manuscript=str(OLD), predecessor_manuscript_sha256=sha(OLD.read_bytes()))
    for a, b in zip(old['records'], doc['records'], strict=True):
        assert {k for k in a if a[k] != b[k]} == ({'formatting_approval_reason'} if a['id'] == row['id'] else set())
    assert all(doc[k] == old[k] for k in old if k not in ['records', 'predecessor_manuscript', 'predecessor_manuscript_sha256'])
    validate_natural_dialogue_batch(doc)
    ROOT.mkdir(parents=True)
    save(DOC, doc)
    result = deepcopy(approval)
    result.update(manuscript=str(DOC), manuscript_sha256=sha(DOC.read_bytes()), predecessor=str(OLD), predecessor_sha256=sha(OLD.read_bytes()),
        predecessor_approval=str(APPROVAL), predecessor_approval_sha256=sha(APPROVAL.read_bytes()),
        technical_note_correction=dict(id=row['id'], field='formatting_approval_reason', before=before, after=row['formatting_approval_reason']),
        all_words_bytes_source_current_final_refs_names_review_gates_andactual_scope_unchanged=True,
        original_approval_andcount_note_preserved_as_history=True, producer_sha256=sha(Path(__file__).read_bytes()))
    save(ROOT / 'formatting_approval.json', result)
    print('B51 formatting note corrected to four alignments per body with explicit stored reuse. All five gates, words, bytes, references, names and actual scope unchanged; original approval preserved.')
