"""Seal all 373 contextual decisions and scoped name/term retentions; formatting remains open."""
from collections import Counter
from copy import deepcopy
from pathlib import Path
import re
from scripts.audit_story_glyph_consistency import load, save
from scripts.save_hodram_B191_B210_comparisons import ROOT, CURRENT, OBJECTS, DRAFTS
from dk4tool.patch.grand_race_menu_release import sha

MANUSCRIPT = Path('translations/hodram_B191_B210_contextual_editorial_manuscript_v1.json')
NAMES = Path('translations/hodram_B191_B210_scoped_names_andterms_v1.json')
IDENTITIES = ROOT / 'native_identity_checkpoint_v1.json'
TERMS = ROOT / 'source_current_term_checkpoint_v1.json'
PARTS = [ROOT / (name + '_whole_exchange_comparison_v1.json') for name in [
    'B191_B197_97', 'B198_B203_107', 'B204_B207_84', 'B208_B210_64']]
ACTOR_REASONS = {
    1: 'Retain approved Hodram/Joakim and established Bergstrom, preserving the full middle component and admiral voice without inventing a higher rank.',
    6: 'Retain Julio Erneco. His excited sake inference and private bargaining advice create no new family or military title.',
    7: 'Retain Cristina Erneco in both consumers and the earrings exchange; correct the spoken legacy Christina separately and infer no kinship from the surname.',
    11: 'Retain Jam Ludwyan and full Jam Jack Ludwyan; bind the letter signature to that full name instead of legacy Ludwayer.',
    12: 'Retain Yukihisa Shiraki and full Yukihisa Genjo Shiraki; the Namahage encounter adds no new title or religious identity.',
    15: 'Retain Angelo Puccini and his source-explicit Mamma mia, without adding invented Italianisms or a new office.',
    16: 'Retain Gerhard Adernkatz and the registered surname correction. Respectful mention of Rocco does not establish knighthood for either man.',
    18: 'Retain Charles Rochefort and full Charles Jean Rochefort; scientific curiosity and book interest characterize him without a new rank.',
    19: 'Retain Carlo Sinat. His care for the stranger and skill at bargaining do not make him a doctor or a merchant\'s son.',
    20: 'Retain Fernando Dias with the registered normal F. His private haggling advice creates no new occupation or relationship.',
    21: 'Retain Ian Dukov with normal ASCII I in both consumers; the separate full-width story-notice I is corrected without changing his identity.',
    24: 'Retain Sera Shahrbaraz and full Sera Altos Shahrbaraz. Her head shake is nonverbal refusal, not evidence of a newly invented condition or motive.',
    25: 'Retain Yifa Sol. Her playful further-discount suggestion adds no familial or formal subordinate relationship.',
    76: 'Retain Mikhail Letzel and full Mikhail Volk Letzel. His interest in medicinal materials does not make the stranger his teacher or relative.',
    82: 'Retain Shopkeeper for the ceramics proprietor without appending regional metadata or inventing a personal name.',
    86: 'Retain Shopkeeper for the dye proprietor. Familiar 親父さん does not justify father in the dialogue or label.',
    87: 'Retain Shopkeeper for the almond-medicine rumor speaker; no named pharmacist or medical credentials follow.',
    92: 'Retain Barkeep for the tavern proprietor. The familiar address in the cheese exchange is occupational, not fatherhood.',
    103: 'Retain Patron for the tavern customer without adding a personal name, rank or relationship to the other diner.',
    104: 'Retain Trader for the ceramics seller; his boast does not authorize a police or criminal-status label.',
    105: 'Retain Trader for the rope seller. Regional metadata is not his surname or a new religious identity.',
    113: 'Retain Port Worker for the ceramics aside. The familiar source role does not establish a brother relationship.',
    115: 'Retain Port Worker for the tobacco exchange, without inferring family or employment relationships from address.',
    117: 'Retain Port Worker for the sake exchange; unused regional metadata remains separate from the natural occupational label.',
    119: 'Retain Port Worker in the medicine and cheese exchanges without adding a name, sibling tie or medical office.',
    124: 'Retain Guard for 衛兵. The castle alarm supports service to the lord but no new military rank or personal name.',
    130: 'Retain Daimyo for 大名, preserving the Japanese lord role rather than inventing a king or a sole ruler of Japan.',
    145: 'Retain Innkeeper for 宿屋のおばさん, preserving the job without inventing an aunt relationship or a precise age.',
    147: 'Retain Guildmaster for the guild head in the ceramics and chase scenes; no police role or confirmed crime follows from pursuit.',
    150: 'Retain Guildmaster for the deferential glass-collection exchange; his manners do not turn him into an invented samurai retainer.',
    153: 'Retain progressive Sailor and distinct catalogue Retainer for this source actor; do not flatten consumer-specific roles.',
    154: 'Retain Sailor/Retainer for the dye adviser. Regional metadata and familiar shopkeeper address add no father or personal name.',
    155: 'Retain Sailor/Retainer for the coughing speaker, with no invented diagnosis, nationality or family tie.',
    156: 'Retain Sailor/Retainer for the sake drinker; keep the explicit difference between source name consumers.',
    157: 'Retain Sailor/Retainer for the abrupt book giver; do not relabel the character Thief from the chase alone.',
    159: 'Retain Sailor/Retainer for the medicine rumor speaker, without inventing an employee relationship or medical expertise.',
    166: 'Retain Lady for 貴婦人. Refined food conversation supports manner without a named noble rank.',
    167: 'Retain Lady for this second actor; the explicitly friendly cooking exchange does not establish marriage or a personal name.',
    168: 'Retain Lady for the host. Her stated friendship and cooking knowledge add neither a formal title nor a family relationship.',
    169: 'Retain Alluring Woman for 妖艶な女, consistent with the flirtatious book offer; do not name her as a confirmed celestial maiden.',
    170: 'Retain Mysterious Old Man for 謎の老人. The medicinal-book offer adds no Grandpa relationship, magical profession or named identity.',
    172: 'Retain Stranger before and after recovery, as previously localized. Source unused regional sailor metadata adds no occupation, nationality or medical diagnosis.',
    173: 'Retain Shady Man for 怪しい人 across both sales encounters; suggestiveness is source-supported without assigning a confirmed crime or ethnicity.',
}


def evidence(paths):
    return {str(p): sha(p.read_bytes()) for p in paths}


if __name__ == '__main__':
    caption_path = ROOT / 'all21_caption_whole_exchange_comparison_v1.json'
    consistency_path = ROOT / 'complete373_prose_consistency_v1.json'
    assert not any(p.exists() for p in [MANUSCRIPT, NAMES, caption_path, consistency_path])
    drafts, objects, current, identities, terms = map(load, [DRAFTS, OBJECTS, CURRENT, IDENTITIES, TERMS])
    parts = [load(p) for p in PARTS]
    for part in parts:
        assert all(sha(Path(p).read_bytes()) == digest for p, digest in part['evidence'].items())
    gates = dict(source=True, context=True, localization=True, naturalness=True, formatting=False)
    old = {r['id']: r for r in objects['choice_records']}
    captions = []
    for draft in [r for r in drafts['records'] if r.get('kind') == 'typed-choice-label']:
        prior = old[draft['id']]
        assert all(prior[k] == draft[k] for k in ['source_reference', 'source_hex', 'source_choice_object_hex', 'source_index', 'source_count'])
        row = deepcopy(draft)
        for key, value in prior.items():
            if key.startswith('current_') or key == 'native_choice_provider_not_run_as_message_catalogue':
                row[key] = deepcopy(value)
        revision = False
        if row['block'] in [200, 205]:
            reason = ('Buy is a clear natural acceptance of the currently quoted price; keep the specific source-index branch and exact price in its surrounding exchange.' if row['source_index'] == 0 else
                'Pass is a natural refusal of this quoted offer; preserve whether the original next branch bargains further or ends the transaction rather than relabeling it Haggle.')
        elif row['block'] == 201:
            reason = ['Buy naturally accepts the stated 8500 offer without unnecessary additional wording.',
                'Pass is a clear polite menu refusal of this book offer.',
                'Decide does not specify who decides; Let Ian decide naturally preserves delegation to Ian rather than another request for the player to choose.'][row['source_index']]
            revision = row['source_index'] == 2
        elif row['source_command_offset'] == 956:
            reason = ['Got it. is a natural acknowledgment of the seller\'s explanation, not a premature purchase decision.',
                'So what? naturally preserves the dismissive challenge, distinct from the later price objection.'][row['source_index']]
        else:
            assert row['block'] == 210 and row['source_command_offset'] == 1126
            reason = ['Bought! is unnatural as a buyer\'s acceptance; I\'ll take them! preserves the volitional purchase at the quoted 9000 price.',
                'Pricey is a natural concise price objection, preserving the source 高い rather than flattening it into the earlier So what response.'][row['source_index']]
            revision = row['source_index'] == 0
        english = draft['english'] if revision else prior['current_comparison_paragraph']
        row.update(english=english, logical_English=english, decision='revision' if revision else 'retention',
            finding=reason, retention_reason=None if revision else reason, localization_note=reason,
            source_byte_offset=row['source_reference']['offset'],
            source_first_draft_English=draft['english'], source_first_draft_reference=dict(path=str(DRAFTS), sha256=sha(DRAFTS.read_bytes()), id=row['id']),
            current_ROM=current['current_ROM'], current_ROM_sha256=current['current_ROM_sha256'],
            current_ROM_English_conversation_comparison_pending=False, current_reference_pending=False, current_English_comparison_pending=False,
            clean_source_current_anddraft_considered_in_complete_exchange=True, review=deepcopy(gates), prose_comparison_review=deepcopy(gates),
            all_fifth_formatting_gates_still_pending=True, new_credit=0)
        captions.append(row)
    assert len(captions) == 21 and Counter(r['decision'] for r in captions) == {'revision': 2, 'retention': 19}
    save(caption_path, dict(records=captions, compared=21, proposed_revisions=2, justified_retentions=19,
        evidence=evidence([DRAFTS, OBJECTS, Path(__file__)]), all_fifth_gates_pending=True, new_credit=0))
    rows = [r for p in parts for r in p['records']] + captions
    rows.sort(key=lambda r: (r['block'], r['source_reference']['offset']))
    assert len(rows) == len({r['id'] for r in rows}) == 373
    assert Counter(r['decision'] for r in rows) == {'revision': 154, 'retention': 219}
    for row in rows:
        assert row['review'] == row['prose_comparison_review'] == gates
        row.update(localization_note=row['finding'], current_English_comparison_pending=False,
            formatting_visual_stored_gameplay_andregistered_release_pending=True)
    names = []
    assert set(ACTOR_REASONS) == {r['actor_ID'] for r in identities['records']}
    for index, bound in enumerate(identities['records']):
        label = next(c['text'] for c in bound['current_consumers'] if c['consumer'] == 'progressive-nameplate')
        reason = ACTOR_REASONS[bound['actor_ID']]
        names.append(dict(id=f'SC1_B191_B210_ACTOR_{bound["actor_ID"]}_SCOPED_NAME', actor_ID=bound['actor_ID'],
            english=label, speaker=label, source_meaning=' / '.join(f['text'] for f in bound['clean_fields'] if f['text'] is not None),
            context='Complete B191–B210 exchanges and exact source/current name consumers.', localization_note=reason,
            decision='retention', retention_reason=reason, review=deepcopy(gates), current_consumers=bound['current_consumers'],
            context_record_ids=bound['context_record_ids'],
            exact_binding_reference=dict(path=str(IDENTITIES), sha256=sha(IDENTITIES.read_bytes()), key='records', index=index),
            native_display_reuse_orfresh_plane_binding_pending=True, actual_full_catalogue_UI_unvisited=True, new_credit=0))
    def term(ident, english, meaning, reason, key, index, field):
        names.append(dict(id=ident, english=english, speaker='Scoped source term', source_meaning=meaning,
            context='Complete B191–B210 exchange and source/current term binding; no global UI fidelity closure.',
            localization_note=reason, decision='retention', retention_reason=reason, review=deepcopy(gates),
            exact_binding_reference=dict(path=str(TERMS), sha256=sha(TERMS.read_bytes()), key=key, index=index),
            typed_field=field, actual_individual_widget_unvisited=True, new_credit=0))
    for i, city in enumerate(terms['cities']):
        term(f'SC1_B191_B210_CITY_{i}', city['current_term'], city['source_Japanese'],
            f"Retain {city['current_term']} for this exact source city and its typed aliases. Keep the forecast prospective without asserting prior scene location or geography.", 'cities', i, city)
    for i, good in enumerate(terms['goods']):
        reason = f"Retain the bound {good['current_term']} commodity label for {good['source_Japanese']}; scoped prose may use a grammatical plural or a clear common synonym without renaming the UI. Wider older-label fidelity review stays open."
        term(f'SC1_B191_B210_GOOD_{good["index"]}', good['current_term'], good['source_Japanese'], reason, 'goods', i, good)
    for i, item in enumerate(terms['spoken_item_terms']):
        reason = ('Retain Glassmaking Guide consistently with the explicitly spoken source title and exact current item pointer; do not restore the old literal dictionary draft.' if item['index'] == 14 else
            'Retain registered Shachihoko for source 鯱の像/scene シャチホコ. Jam\'s mistaken figurehead claim remains character dialogue; legacy Orca Figurehead is not restored.')
        term(f'SC1_B191_B210_ITEM_{item["index"]}', item['current_term'], item['source_Japanese'], reason, 'spoken_item_terms', i, item)
    for i, attribute in enumerate(terms['attributes']):
        term(f'SC1_B191_B210_STAT_{i}', attribute['english'], attribute['japanese'],
            f"Retain approved {attribute['english']} for {attribute['japanese']} and the exact one-point notice. Permanent Spirit remains distinct from current Mood; Wits retains its final s.", 'attributes', i, attribute)
    for i, category in enumerate(terms['source_categories']):
        term(f'SC1_B191_B210_CATEGORY_{category["index"]}', category['prose'], category['Japanese'],
            'Retain the broad medicine/dyes source category without inventing a remedy, brand, pigment, recipe or completed purchase.', 'source_categories', i, category)
    rocco = terms['portrait_subject']
    term('SC1_B203_ROCCO_SCOPED_NAME', rocco['project_English'], rocco['source_Japanese'],
        'Retain established Rocco Alemkel, consistent with the clean name and earlier contextual proof; respectful 殿 does not grant knighthood and no external historical identity is asserted.', 'portrait_subject', None, rocco)
    for i, (ja, en, reason) in enumerate([
        ('ギヤマン（ガラス）', 'giyaman / glass', 'Retain giyaman and the explicit glass gloss without adding etymology, cut-glass material or a new commodity name.'),
        ('なまはげ', 'namahage', 'Retain the named cultural figure as a generic creature noun and its complete bad-child chant, without invented ritual, religion, date or resolved dream identity.')]):
        term(f'SC1_B191_B210_CULTURAL_{i}', en, ja, reason, 'cultural_terms', i, dict(source_term=ja, prose=en))
    assert len(names) == 70
    save(NAMES, dict(format='dk4-scoped-name-andterm-localization-v1', translation_policy='natural-dialogue-v2', target_locale='en-US',
        review_gates=list(gates), records=names, ordinary_actors=43, current_name_consumer_bindings=86,
        justified_retentions=70, proposed_name_table_edits=0, all_four_prose_gates_pass=True, all_fifth_formatting_gates_pending=True,
        no_new_global207_name_approval=True, no_new_dialogue_credit=True, runtime=identities['runtime'], evidence=evidence([IDENTITIES, TERMS, Path(__file__)])))
    doc = dict(format='dk4-editorial-manuscript-v1', encoder='dialogue-relocatable-v1', translation_policy='natural-dialogue-v2',
        target_locale='en-US', review_gates=list(gates), file_path='/data/SC1.DK4', blocks=list(range(191, 211)), records=rows,
        current_ROM=current['current_ROM'], current_ROM_sha256=current['current_ROM_sha256'], current_archive_sha256=current['current_archive_sha256'],
        complete_comparison_blocks=list(range(191, 211)), current_comparisons=373, remaining_current_comparisons=0,
        proposed_revisions=154, wording_retentions=219, complete_four_gate_comparisons=373,
        formatting_andvisual_stored_gameplay_integration_still_pending=True, all_individual_fifth_gates_still_pending=True,
        scoped_name_review=str(NAMES), scoped_name_review_sha256=sha(NAMES.read_bytes()), source_andcurrent_exact_reference_bindings=True,
        no_blanket_before_any_historical_English_exposure_claim=True, new_credit=0, new_ROMs=0, full_goal_complete=False,
        evidence=evidence([*PARTS, caption_path, NAMES, CURRENT, OBJECTS, DRAFTS, Path(__file__)]))
    checks = []
    for row in rows:
        english = row['english']
        assert english == english.strip() == row['logical_English'] and not any(s in english for s in ['\n', '\r', '{LB', '{ALIGN', '{PAD}', '  '])
        raw = bytes.fromhex(row['source_hex'])
        assert all(english.count('{MACRO:' + m + '}') == raw.count(m.encode('ascii')) for m in ['FI', 'FA', 'FO'])
        encoded = english.encode('cp932')
        assert all(32 <= b < 127 for b in encoded), (row['id'], english)
        assert not re.search(r'\b(?:Christina|Ludwayer)\b', english)
        assert row['finding'].strip() and row['source_meaning'].strip() and row['context'].strip()
        checks.append(dict(id=row['id'], decision=row['decision'], source_reference=row['source_reference'], current_reference=row['current_reference'],
            logical_English_sha256=sha(encoded), ASCII_CP932_andmacro_counts_exact=True, four_prose_gates_pass=True, formatting_gate=False,
            punctuation_glyph_normalization=row.get('punctuation_only_glyph_normalization', False)))
    by_id = {r['id']: r for r in rows}
    def words(ident):
        return re.findall(r"[A-Za-z']+", by_id[f'DK4_MES_B209_R{ident:04d}']['english'].lower())
    assert words(9)[1:] == words(13) and words(17)[2:] == words(20)
    assert words(28) == words(32) and words(36) == words(40)
    assert words(59)[1:-1] == words(63)
    save(MANUSCRIPT, doc)
    save(consistency_path, dict(manuscript=str(MANUSCRIPT), manuscript_sha256=sha(MANUSCRIPT.read_bytes()), records=checks,
        compared=373, revisions=154, retentions=219, scoped_name_andterm_retentions=70,
        all_logical_paragraphs_ASCII_CP932_macro_counts_scoped_spellings_andparrot_word_echoes_pass=True,
        formatting_native_glyph_bounds_allocation_pagination_visual_storage_gameplay_andrelease_still_pending=True,
        new_credit=0, new_ROMs=0, evidence=evidence([MANUSCRIPT, NAMES, Path(__file__)])))
    print('PASS 373 contextual comparisons: 154 revisions / 219 retentions; 70 scoped name/term retentions. Formatting pending; no credit or ROM.')
