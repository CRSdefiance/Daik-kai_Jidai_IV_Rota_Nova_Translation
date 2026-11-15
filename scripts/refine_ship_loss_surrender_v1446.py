"""Natural direct-address order for complete predicates,no fit-only shortening."""
from copy import deepcopy
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save

OLD = Path('translations/ship_loss_surrender_editorial_manuscript_v1.json')
NEW = Path('translations/ship_loss_surrender_editorial_manuscript_v2.json')
PROOF = Path('work/analysis/ship_loss_surrender_fonts_v1445/native_font_research.json')

if __name__=='__main__':
    assert not NEW.exists()
    doc,proof = deepcopy(read(OLD)),read(PROOF)
    assert proof['manuscript_sha256']==sha(OLD.read_bytes()) and len(proof['cases'])==624 and len(proof['findings'])==233
    affected = {r['message_ID'] for r in proof['findings']}
    assert len(affected)==20
    for row in doc['records']:
        n = row['message_id'];old = row['english']
        if n in affected:
            assert old.startswith('Admiral, ') and old.endswith('!')
            body = old[len('Admiral, '):-1]
            row['english'] = body[0].upper()+body[1:]+', Admiral!'
            assert len(row['english'])==len(old)
            assert row['english'].count('%s')==old.count('%s')==1
            row['previous_reviewed_english'] = old
            row['localization_note'] += (' English naturally allows the direct address at the end. '
                'Keep the entire reported event and any appearance/hearsay qualifier;move Admiral without '
                'shortening the sentence or authoring a break. The revised paragraph has exactly the same '
                'ASCII byte length as the earlier draft and removes no source fact. Native layout must be reverified.')
        row['editorial_decision'] = 'retain' if row['english']==row['current_English'] else 'revise'
        row['review']['formatting'] = False
    assert all(r['editorial_decision']=='revise' for r in doc['records'])
    doc.update(revised=24,retained=0,previous_manuscript=str(OLD),previous_manuscript_sha256=sha(OLD.read_bytes()),
        source_voice_and_direct_address_refinement='20 idiomatic end-position Admiral addresses;all20 preserve paragraph byte length. Four already-natural layouts retained from the first review. All24 differ from the original candidate;no source review credit is duplicated.',
        earlier_native_layout_findings=str(PROOF),earlier_native_layout_findings_sha256=sha(PROOF.read_bytes()),
        producer_sha256=sha(Path(__file__).read_bytes()))
    save(NEW,doc)
    print('20 natural address-order refinements with identical byte lengths;24 source-faithful revisions,all native gates still pending.',flush=True)
