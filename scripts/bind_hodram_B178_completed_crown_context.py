"""Reuse completed B89 clean context for the new B176–B178 conversation review."""
from pathlib import Path
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.audit_story_glyph_consistency import load, save

ROOT = Path('work/analysis/Hodram_B171_B190_clean_20261102')

if __name__ == '__main__':
    target = ROOT / 'linked_B89_crown_context_v1.json'
    assert not target.exists()
    packet_path = Path('work/analysis/Hodram_B81_B90_clean_20261101/clean_source_packet.json')
    packet = load(packet_path)
    group = next(g for g in packet['groups'] if g['block'] == 89)
    clean_path = Path('work/clean.nds')
    assert sha(clean_path.read_bytes()) == packet['source_ROM_sha256']
    block = IlnkContainer.parse(NdsImage.open(clean_path).read_file('/data/SC1.DK4')).blocks[89]
    assert block.hex() == group['clean_block_hex']
    ledger = load('translations/editorial_review_current_v1.json')
    completed = {(r['file_path'], r['id']) for r in ledger['contextual_story_natural_dialogue_pass_v1871']['record_keys']}
    assert len(group['records']) == 18 and all(('/data/SC1.DK4', r['id']) in completed for r in group['records'])
    previous_review = Path('translations/hodram_B81_B89_contextual_final_review_v1.json')
    save(target, dict(clean_source_packet=str(packet_path), clean_source_packet_sha256=sha(packet_path.read_bytes()),
        clean_ROM_sha256=sha(clean_path.read_bytes()), source_block=89, source_records=group['records'],
        already_completed_final_review=str(previous_review), already_completed_final_review_sha256=sha(previous_review.read_bytes()),
        all18_previously_completed_source_keys_reused=True,
        findings=[
            'Hodram finds the crown first, despite Julian setting out earlier.',
            'Julian asks him to relinquish it because he promised it to 美華; exact approved English name remains to be bound.',
            'Hodram agrees and explicitly permits Julian to claim that he found it himself.',
            'B178 gratitude and acknowledgment follow this generosity; Hodram did not require public credit.'],
        linked_new_blocks=[176, 177, 178], prior_English_not_consulted_for_linked_context=True,
        source_context_question_resolved_without_restarting_B89=True, no_new_editorial_credit=True,
        producer_sha256=sha(Path(__file__).read_bytes()), new_credit=0))
    print('Reused exact completed B89 clean context:18 source records;no repeated review orcredit.')
