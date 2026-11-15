"""Seal the complete contextual comparison and scoped identities; display gates stay open."""
from copy import deepcopy
from pathlib import Path
from collections import Counter
import re

from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load, save
from scripts.save_hodram_B171_B190_drafts import ROOT

MANUSCRIPT = Path('translations/hodram_B171_B190_contextual_editorial_manuscript_v1.json')
NAMES = Path('translations/hodram_B171_B190_scoped_names_andterms_v1.json')
PARTS = [ROOT / (name + '_whole_exchange_comparison_v1.json') for name in (
    'B171_B173_131', 'B174_B175_74', 'B176_B179_98', 'B180_B190_130')]
CURRENT = Path('work/analysis/Hodram_B171_B190_current_20261102/current_effective.json')
OBJECTS = Path('work/analysis/Hodram_B171_B190_current_objects_20261102/current_objects.json')
DRAFTS = ROOT / 'all435_clean_English_drafts_v2.json'
IDENTITIES = ROOT / 'native_identity_and_term_checkpoint_v1.json'
CITIES = ROOT / 'town_forecast_city_terms_v1.json'

ACTOR_REASONS = {
    1: 'Retain approved Hodram and Joakim with established Bergstrom. The full catalogue preserves the middle component; commanding a fleet does not supply an invented Fleet Admiral rank.',
    4: 'Retain Janus Pasar for the source name. His caution and sarcastic rejoinders do not authorize a new title or relationship.',
    6: 'Retain Julio Erneco and the registered normal-letter repair. Familiar older-man address is not kinship, and the sail lesson supplies no new military rank.',
    7: 'Retain Cristina Erneco in both bound consumers and this dialogue. Preserve her comic protests without inferring a family relationship from a shared surname.',
    13: 'Retain Cesare Tony, consistent with the source-reviewed name and current consumers; his opinions do not create a new office or rank.',
    16: 'Retain Gerhard Adernkatz, preserving the source-reviewed sound and established spelling rather than reverting to a legacy variant.',
    23: 'Retain Manuel Almeida. A knowledgeable contribution to the sail discussion does not establish a new title or relationship.',
    24: 'Retain Sera Shahrbaraz and full Sera Altos Shahrbaraz. The language misunderstanding is a scene fact, not a reason to change her identity or invent incapacity to speak.',
    25: 'Retain Yifa Sol for the source name. Her senior fellow student is not her biological brother; the reveal of his name belongs at the original point in the exchange.',
    26: 'Retain Julian Lopes, including the linked crown context. His voluntary gratitude does not imply that Hodram demanded discovery credit or gave the crown directly to Mihwa.',
    76: 'Retain Mikhail Letzel and full Mikhail Volk Letzel, preserving all source name components without assigning a nationality from their sounds.',
    81: 'Retain Sanghyeon Kan for サンヒョン・カン. Senior fellow student describes the source relationship; it is neither a sibling label nor a formal military rank.',
    85: 'Retain Shopkeeper for the square proprietor. Regional metadata does not supply a personal name, religion or nationality.',
    87: 'Retain Shopkeeper for this second source proprietor. The regional table field is not an extra player-facing title or biography.',
    92: 'Retain Barkeep, a natural occupational label for the tavern proprietor. The familiar source address does not make him anyone\'s father.',
    96: 'Retain Patron for the tavern customer. The drink-order exchange gives no personal name or rank.',
    109: 'Retain Shipwright for the shipyard proprietor in the sail lesson. The familiar older-man address does not establish kinship.',
    110: 'Retain Shipwright for the second regional source actor. Do not append regional metadata to the shared occupational label.',
    132: 'Retain Priest for the source religious officiant. The metadata alone does not establish a denomination or a more specific religious title.',
    148: 'Retain Guildmaster for the guild head. It conveys the explicit occupation without a noble title.',
    152: 'Retain the native progressive Sailor and distinct catalogue Retainer. The source uses different consumer labels; preserve both without a global table substitution.',
    153: 'Retain the native progressive Sailor and distinct catalogue Retainer for this actor too. The regional metadata creates no personal name or religious rank.',
    164: 'Retain the previously reviewed Man label. The paired tea-shopping conversation supports a couple but does not establish marriage or age.',
    165: 'Retain the previously reviewed Woman label. A request to buy tea is natural between this pair; it does not authorize Wife or Young Woman.',
    166: 'Retain Lady for 貴婦人. The refined social voice is preserved without inventing a personal name or a specific noble rank.',
    167: 'Retain Lady for the second source actor. Her home-baking conversation uses an explicit husband where the source does, without making that relationship part of a global label.',
    168: 'Retain Lady for the third source actor. The bakery and collecting exchanges supply social manner, not a named title or age.',
    174: 'Retain Owner for オーナー. Her extravagant business predictions establish the comic employer voice; they do not make her the Cook\'s wife.',
    175: 'Retain Cook for コック. His weary repeated assent fits an employee responding to the Owner, without an invented marriage or servant rank.',
    183: 'Retain Angel for エンジェル. The separate unnamed FE-panel woman is not identified by a header or personal-name utterance; do not assign her this identity or invent a romance.',
    201: 'Retain established Mihwa for 美華 and both bound consumers. The written name and Hangzhou metadata do not independently prove a nationality or a different phonetic reading.',
    202: 'Retain established Reika for 麗姫 and both bound consumers. Preserve the spoken identity in the crown exchange without turning the character 姫 into an invented Princess title.',
}

TERM_REASONS = {
    '新羅の金冠': 'Retain Silla Gold Crown consistently with the exact inventory label and linked B89 discovery exchange. Silla remains the named cultural origin; do not replace it with a generic royal crown.',
    '武寧王陵': 'Retain Tomb of King Muryeong, preserving the named king and tomb rather than inventing a temple, treasure identity or political history.',
    '京城': 'Retain established Seoul for the source city identity. Keep its typed city owner separate from the actor metadata field; add no historical or national claim.',
    '杭州': 'Retain Hangzhou consistently with the source city and current typed city label. Its association with a character does not establish that character\'s nationality.',
    'スプリットセイル': 'Retain established Spritsail, the current component name used by the sail lesson. Preserve the described placement and function without inventing a ship class.',
    'ジガースパンカー': 'Retain Jigger Spanker, the bound component name. Treat it as a sail term rather than a character, vessel name or invented rank.',
}


def evidence(paths):
    return {str(p): sha(p.read_bytes()) for p in paths}


def main():
    captions_path = ROOT / 'two_caption_whole_exchange_comparison_v1.json'
    consistency_path = ROOT / 'complete435_prose_consistency_v1.json'
    assert not any(p.exists() for p in [MANUSCRIPT, NAMES, captions_path, consistency_path])
    drafts, objects, current, identities, cities = map(load, [DRAFTS, OBJECTS, CURRENT, IDENTITIES, CITIES])
    parts = [load(p) for p in PARTS]
    for part in parts:
        for path, digest in part['evidence'].items():
            assert sha(Path(path).read_bytes()) == digest, path
    old_choices = {r['id']: r for r in objects['choice_records']}
    captions = []
    for draft in [r for r in drafts['records'] if r.get('kind') == 'typed-choice-label']:
        old = old_choices[draft['id']]
        assert all(old[k] == draft[k] for k in ['source_reference', 'source_hex', 'source_choice_object_hex'])
        row = deepcopy(draft)
        for key, value in old.items():
            if key.startswith('current_') or key == 'native_choice_provider_not_run_as_message_catalogue':
                row[key] = deepcopy(value)
        first = row['source_index'] == 0
        english = 'Listen.' if first else 'No thanks'
        reason = ('Hear is an unnatural isolated command here. Listen. naturally accepts the offered sail lesson and preserves the source volitional response.' if first else
            'No thanks is already a natural menu refusal of the offered lesson. The source does not promise to listen later; menu punctuation is optional.')
        row.update(english=english, logical_English=english, decision='revision' if first else 'retention',
            finding=reason, retention_reason=None if first else reason,
            source_byte_offset=row['source_reference']['offset'], source_word=0x2100,
            source_first_draft_English=draft['english'], source_first_draft_reference=dict(path=str(DRAFTS), sha256=sha(DRAFTS.read_bytes()), id=row['id']),
            current_ROM=current['current_ROM'], current_ROM_sha256=current['current_ROM_sha256'],
            current_ROM_English_conversation_comparison_pending=False, current_reference_pending=False,
            current_English_comparison_pending=False, clean_source_current_anddraft_considered_in_complete_exchange=True,
            review=dict(source=True, context=True, localization=True, naturalness=True, formatting=False),
            prose_comparison_review=dict(source=True, context=True, localization=True, naturalness=True, formatting=False),
            all_fifth_formatting_gates_still_pending=True, new_credit=0)
        captions.append(row)
    assert len(captions) == 2
    save(captions_path, dict(records=captions, compared=2, proposed_revisions=1, justified_retentions=1,
        evidence=evidence([DRAFTS, OBJECTS, Path(__file__)]), all_fifth_gates_pending=True, new_credit=0))
    rows = [r for part in parts for r in part['records']] + captions
    rows.sort(key=lambda r: (r['block'], r['source_reference']['offset']))
    assert len(rows) == len({r['id'] for r in rows}) == 435
    assert Counter(r['decision'] for r in rows) == {'revision': 195, 'retention': 240}
    gates = dict(source=True, context=True, localization=True, naturalness=True, formatting=False)
    for row in rows:
        assert row['review'] == row['prose_comparison_review'] == gates
        row['localization_note'] = row['finding']
        row['current_English_comparison_pending'] = False
        row['formatting_visual_stored_gameplay_andregistered_release_pending'] = True
    name_rows = []
    assert set(ACTOR_REASONS) == {r['actor_ID'] for r in identities['records']}
    for index, bound in enumerate(identities['records']):
        actor = bound['actor_ID']
        consumers = {r['consumer']: r['text'] for r in bound['current_consumers']}
        reason = ACTOR_REASONS[actor]
        name_rows.append(dict(id=f'SC1_B171_B190_ACTOR_{actor}_SCOPED_NAME', actor_ID=actor,
            english=consumers['progressive-nameplate'], speaker=consumers['progressive-nameplate'],
            context='Complete B171–B190 conversations and exact source identity; scoped consumer approval only.',
            source_meaning=' / '.join(f['text'] for f in bound['clean_fields'] if f['text'] is not None),
            localization_note=reason, decision='retention', retention_reason=reason, review=deepcopy(gates),
            current_consumers=bound['current_consumers'], context_record_ids=bound['context_record_ids'],
            exact_binding_reference=dict(path=str(IDENTITIES), sha256=sha(IDENTITIES.read_bytes()), key='records', index=index),
            native_display_proof_reuse_orfresh_plane_binding_pending=True, actual_full_catalogue_UI_unvisited=True, new_credit=0))
    for index, term in enumerate(identities['source_literal_terms']):
        reason = TERM_REASONS[term['source_Japanese']]
        name_rows.append(dict(id=f'SC1_B171_B190_TERM_{index}', english=term['current_label'], speaker='Scoped source term',
            context='B171–B179 complete sail, crown and companion exchanges.', source_meaning=term['source_Japanese'],
            localization_note=reason, decision='retention', retention_reason=reason, review=deepcopy(gates),
            exact_binding_reference=dict(path=str(IDENTITIES), sha256=sha(IDENTITIES.read_bytes()), key='source_literal_terms', index=index),
            typed_field=term, actual_individual_widget_unvisited=True, new_credit=0))
    for index, city in enumerate(cities['records']):
        reason = f"Retain {city['current_label']} for {city['source_Japanese']}, consistently with the exact typed city label. Preserve this forecast's destination without adding geography or changing its tentative market prediction."
        name_rows.append(dict(id=f'SC1_B180_B190_CITY_{city["city_index"]}', english=city['current_label'], speaker='Forecast destination',
            context='Complete B180–B190 town exchange and its concluding market forecast.', source_meaning=city['source_Japanese'],
            localization_note=reason, decision='retention', retention_reason=reason, review=deepcopy(gates),
            exact_binding_reference=dict(path=str(CITIES), sha256=sha(CITIES.read_bytes()), key='records', index=index),
            typed_field=city, actual_individual_city_UI_unvisited=True, new_credit=0))
    assert len(name_rows) == 49
    save(NAMES, dict(format='dk4-scoped-name-andterm-localization-v1', translation_policy='natural-dialogue-v2', target_locale='en-US',
        review_gates=list(gates), records=name_rows, ordinary_actors=32, current_name_consumer_bindings=64,
        typed_story_terms=6, forecast_cities=11, justified_retentions=49, proposed_name_table_edits=0,
        all_four_prose_gates_pass=True, all_fifth_formatting_gates_pending=True, no_new_global207_name_approval=True,
        no_new_dialogue_credit=True, runtime=identities['runtime'], evidence=evidence([IDENTITIES, CITIES, Path(__file__)])))
    doc = dict(format='dk4-editorial-manuscript-v1', encoder='dialogue-relocatable-v1', translation_policy='natural-dialogue-v2',
        target_locale='en-US', review_gates=list(gates), file_path='/data/SC1.DK4',
        current_ROM=current['current_ROM'], current_ROM_sha256=current['current_ROM_sha256'],
        current_archive_sha256=current['current_archive_sha256'], blocks=list(range(171, 191)), records=rows,
        complete_comparison_blocks=list(range(171, 191)), current_comparisons=435, remaining_current_comparisons=0,
        proposed_revisions=195, wording_retentions=240, complete_four_gate_comparisons=435, place_name_questions=0,
        formatting_andvisual_stored_gameplay_integration_still_pending=True, all_individual_fifth_gates_still_pending=True,
        scoped_name_review=str(NAMES), scoped_name_review_sha256=sha(NAMES.read_bytes()),
        source_andcurrent_exact_reference_bindings=True, earlier_user_tea_screenshot_incidental_exposure_disclosed=True,
        no_blanket_before_any_prior_English_claim=True, scoped_Proofs_consistency_does_not_close_wider_terminology_question=True,
        new_credit=0, new_ROMs=0, full_goal_complete=False,
        evidence=evidence(PARTS + [captions_path, NAMES, CURRENT, OBJECTS, DRAFTS, Path(__file__)]))
    save(MANUSCRIPT, doc)
    checks = []
    for row in rows:
        english = row['english']
        assert english == english.strip() == row['logical_English']
        assert not any(s in english for s in ['\n', '\r', '{LB', '{ALIGN', '{PAD}', '  '])
        raw = bytes.fromhex(row['source_hex'])
        assert all(english.count('{MACRO:' + m + '}') == raw.count(m.encode('ascii')) for m in ['FI', 'FA', 'FO'])
        encoded = english.encode('cp932')
        assert all(32 <= b < 127 for b in encoded), (row['id'], english)
        assert not re.search(r'(?:^|[^A-Za-z])(Christina|Serah|Tohni|Mivall)(?:$|[^A-Za-z])', english), row['id']
        assert row['finding'].strip() and row['source_meaning'].strip() and row['context'].strip()
        checks.append(dict(id=row['id'], decision=row['decision'], source_reference=row['source_reference'],
            current_reference=row['current_reference'], planned_logical_English_sha256=sha(encoded),
            CP932_andASCII_only=True, source_MACRO_counts_exact=True, four_prose_gates_pass=True, formatting_gate=False,
            punctuation_glyph_normalization=row.get('punctuation_only_glyph_normalization', False)))
    save(consistency_path, dict(manuscript=str(MANUSCRIPT), manuscript_sha256=sha(MANUSCRIPT.read_bytes()), records=checks,
        compared=435, revisions=195, retentions=240, scoped_name_andterm_retentions=49,
        all_changed_andretained_text_has_fresh_logical_prose_checks=True,
        macro_counts_CP932_ASCII_logical_paragraphs_scoped_spellings_andfour_gates_pass=True,
        formatting_native_glyph_bounds_allocation_pagination_visual_storage_gameplay_andrelease_still_pending=True,
        new_credit=0, new_ROMs=0, evidence=evidence([MANUSCRIPT, NAMES, Path(__file__)])))
    print('PASS 435 contextual comparisons: 195 revisions / 240 retentions; 49 scoped name/term retentions. Four prose gates only; no credit or ROM.')


if __name__ == '__main__':
    main()
