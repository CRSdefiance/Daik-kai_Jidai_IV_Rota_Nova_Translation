"""Seal every clean meaning before native-name binding or prior-dialogue exposure."""
from copy import deepcopy
from pathlib import Path
from scripts.audit_story_glyph_consistency import load, save
from dk4tool.patch.grand_race_menu_release import sha

ROOT = Path('work/analysis/Hodram_B151_B170_clean_20261102')
PARTS = [ROOT / name for name in [
    'B151_B155_42_clean_meanings_before_English.json', 'B156_86_clean_meanings_before_English.json',
    'B157_29_clean_meanings_before_English.json', 'B158_B160_174_clean_meanings_before_English.json',
    'B161_B166_101_clean_meanings_before_English.json', 'B167_B168_115_clean_meanings_before_English.json',
    'B169_B170_87_clean_meanings_before_English.json']]


def main():
    output = ROOT / 'all634_clean_meanings_before_English_v1.json'
    checkpoint = ROOT / 'complete_clean_meanings_checkpoint.json'
    assert not output.exists() and not checkpoint.exists()
    packet_path = ROOT / 'clean_source_packet.json'
    packet = load(packet_path)
    source = {r['id']: r for g in packet['groups'] for r in g['records']}
    meanings = {}
    for path in PARTS:
        part = load(path)
        assert part['earlier_English_unconsulted'] and part['source_packet_sha256'] == sha(packet_path.read_bytes())
        for row in part['records']:
            assert row['id'] not in meanings
            original = source[row['id']]
            for key in ['source_reference', 'source_hex', 'source_Japanese', 'source_selector', 'source_complete_preamble_hex', 'source_macros']:
                assert row[key] == original[key], (row['id'], key)
            assert row['source_meaning'].strip()
            meanings[row['id']] = deepcopy(row)
    assert set(meanings) == set(source) and len(meanings) == 634
    amendments = {
        'DK4_MES_B153_R0016': (
            'Identifies himself only as someone who has long resisted Ottoman rule.',
            'States that the speaker has long resisted Ottoman rule.',
            'Avoid an unbound gender inference in the source gloss; the original line identifies resistance, not gender.'),
        'DK4_MES_B153_R0045': (
            'Says others have also escaped Ottoman rule, as his group has; tells the addressee to search the ruins in Turkey.',
            'Says others have also escaped Ottoman rule, as the speaker’s group has; tells the addressee to search the ruins in Turkey.',
            'Preserve the explicit collective identity without inferring the speaker’s gender.'),
        'DK4_MES_B169_R0011': (
            'In a returning-visitor variant, he insists that coming here means accepting the challenge.',
            'In one opening variant, he insists that coming here means accepting the challenge.',
            'The line alone does not prove a repeat-visit condition; retain the structural variant without inventing chronology.')
    }
    amended = []
    for record_id, (old, new, reason) in amendments.items():
        row = meanings[record_id]
        assert row['source_meaning'] == old
        row['source_meaning'] = new
        row['source_gloss_amendment'] = dict(previous_meaning=old, reason=reason, prior_artifacts_preserved=True)
        amended.append(dict(id=record_id, previous_meaning=old, amended_meaning=new, reason=reason))
    ordered = [meanings[r['id']] for g in packet['groups'] for r in g['records']]
    save(output, dict(records=ordered, source_meanings=634, source_packet=str(packet_path), source_packet_sha256=sha(packet_path.read_bytes()),
        source_parts={str(p): sha(p.read_bytes()) for p in PARTS}, source_gloss_amendments=amended,
        all_complete_exchanges_read_before_prior_English=True, earlier_English_unconsulted=True,
        native_identity_terms_drafts_andall_five_review_gates_pending=True, new_credit=0, producer_sha256=sha(Path(__file__).read_bytes())))
    caption_path = ROOT / 'eight_clean_caption_meanings_before_English.json'
    captions = load(caption_path)
    source_choice_path = ROOT / 'clean_choice_objects.json'
    source_choices = load(source_choice_path)
    assert len(captions['records']) == 8 and captions['earlier_English_unconsulted']
    assert captions['source_choice_objects_sha256'] == sha(source_choice_path.read_bytes())
    assert {r['id'] for r in captions['records']} == {r['id'] for r in source_choices['records']}
    keys = {(r['file_path'], r['id']) for r in ordered + captions['records']}
    ledger_path = Path('translations/editorial_review_current_v1.json')
    ledger = load(ledger_path)
    completed = {(r['file_path'], r['id']) for r in ledger['contextual_story_natural_dialogue_pass_v1871']['record_keys']}
    assert len(keys) == 642 and not keys & completed and ledger['records_editorially_completed'] == 8856
    save(checkpoint, dict(source_packet=str(packet_path), source_packet_sha256=sha(packet_path.read_bytes()),
        ordinary_meanings=str(output), ordinary_meanings_sha256=sha(output.read_bytes()),
        caption_meanings=str(caption_path), caption_meanings_sha256=sha(caption_path.read_bytes()),
        ordinary_speeches=634, typed_caption_records=8, typed_choice_objects=4, style_objects=0, total_editorial_objects=642,
        source_meanings_saved=642, remaining_source_meanings=0, whole_exchanges=packet['groups'].__len__(),
        source_2000_label_free_controls=14, zero_source_decode_errors=True, exact_source_current_references_preserved=True,
        no_prior_English_dialogue_exposure=True, no_localized_English_drafts=True,
        native_names_roles_mentioned_people_item_terms_andlinked_context_pending=True,
        specific_fidelity_leads=[
            'B156: source-supported supreme naval command andprincess status;preserve retirement/farewell emotional progression andGerhard’s warm joke.',
            'B156: cinematic FE leading rows/spatial staging/Sera-FI headings require actual consumer qualification, not automatic reuse ofordinary FE geometry.',
            'B159: intentional harassment andIan’s resistance;do not invent injuries oridentity facts.',
            'B160: Carlo’s wife/daughter are explicit;the inn woman’s relationship to Adil is not. 主計長 needs the approved ship-role term.',
            'B161: bind ミヴォール andthe swordswoman’s name;admiration is not proof ofan unspoken romantic relationship.',
            'B166: preserve J-A-M, invented proverb andtwo-second joke;the abandonment claim is Jam’s excuse.',
            'B167: exact ship-purchase thresholds,one-percent/one-to-five limit andfive-hold maximum;do not fill unstated price gaps.',
            'B168: Rafael chooses generosity after Cesare declines to reclaim the ship;Good Luck is proof,not the ship’s name.',
            'B169: drink wager,last-coin loser andhead/tail recruitment paths;the couple is not identified as married.',
            'B170: no kinship fromolder-man address,no unbound drink subtype,andthe two question choices distinguish genuine inquiry fromtesting knowledge.'],
        completed_records_unchanged=8856, current_registered_candidate_unchanged=True, new_credit=0,
        full_goal_complete=False, evidence={str(p): sha(p.read_bytes()) for p in [packet_path, output, caption_path, source_choice_path, Path(__file__)]}))
    print('Sealed642 clean-first meanings across20 whole blocks;zero missing orduplicate objects,no prior English,no new completion credit.')


if __name__ == '__main__':
    main()
