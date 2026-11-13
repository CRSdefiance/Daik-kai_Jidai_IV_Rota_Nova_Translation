"""Record individual contextual and scoped name decisions for the town exchanges."""
from copy import deepcopy
from pathlib import Path
from types import FunctionType

from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.patch.grand_race_menu_release import sha
from scripts import write_rafael_B177_B180_contextual_v1 as workflow
from scripts.audit_story_glyph_consistency import load, save
from scripts.bind_rafael_B181_B200_names_v1 import CURRENT, OUT as IDENTITY
from scripts.seal_rafael_B181_B200_clean_v1 import OUT as SOURCE


DRAFTS = SOURCE / 'sealed_drafts.json'
DECISIONS = Path('translations/rafael_B188_B200_contextual_decisions_v1.txt')
OUT = Path('translations/rafael_B188_B200_contextual_review_v1.json')
LABELS = Path('translations/rafael_B188_B200_scoped_names_review_v1.json')
BLOCKS = list(range(188, 201))
NAMES = {
    85: ('Shopkeeper', 'The Basra dealer runs the shop and thanks his customers. Keep the occupation concise.'),
    87: ('Shopkeeper', 'The Malacca speaker retains the shopkeeper role even in informal conversation about the remedy.'),
    92: ('Barkeep', 'The man takes a drink order and answers the customary form of address. Barkeep fits the tavern.'),
    96: ('Patron', 'The source identifies the man by his place in the tavern. Keep the short role label.'),
    110: ('Shipwright', 'Keep the occupational label while he voices his personal taste in paintings.'),
    130: ('Daimyo', 'Keep the source rank and cultural setting. His collecting order matches his authority.'),
    132: ('Priest', 'Keep the source role for the third collector. His hobby adds no rank or affiliation.'),
    148: ('Guildmaster', 'Keep the source title for the first collector. His personal purchase requires no added title in speech.'),
    150: ('Guildmaster', 'Keep the established source role. His deference in Osaka does not make him a retitled servant.'),
    152: ('Sailor', 'Keep the source-qualified progressive form and distinct Retainer catalogue label for the wine enthusiast.'),
    153: ('Sailor', 'Keep the source-qualified progressive form and distinct Retainer catalogue label for the bystander in Basra.'),
    155: ('Sailor', 'Keep the source-qualified progressive form and distinct Retainer catalogue label for the coughing speaker.'),
    164: ('Man', 'Keep the simple role label in both the tea and the cold-weather exchange. His familiarity needs no invented kinship.'),
    165: ('Woman', 'Keep the simple role label in both exchanges. The shared tea and errand request carry the pair’s familiarity.'),
    166: ('Lady', 'Her baking pride, admiring gossip and direct questions fit the broad polite role. Keep her distinct selector.'),
    167: ('Lady', 'Her offers and responses fit the polite role. Keep her distinct selector even where she shares the nameplate wording.'),
    168: ('Lady', 'Her curiosity in the baking and ruby scenes fits the polite role. Keep her distinct selector.'),
    174: ('Owner', 'Her orders to buy produce, sell dishes and adjust the flavor support the established role.'),
    175: ('Cook', 'He answers food orders and asks how to adjust the flavor. Keep the job title and his dry replies.'),
}
UNTRANSLATED = {
    f'DK4_MES_B191_R{i:04}' for i in (6, 13, 20, 28, 43, 50)
}


def digest(path):
    return sha(Path(path).read_bytes())


def main():
    assert not OUT.exists() and not LABELS.exists()
    drafts, current, identity = map(load, (DRAFTS, CURRENT, IDENTITY))
    assert identity['runtime'] == current['runtime']
    rows = [r for group in current['groups'] if group['block'] in BLOCKS for r in group['records']]
    selected = [r for r in drafts['records'] if r['block'] in BLOCKS]
    assert len(rows) == len(selected) == 157
    assert {r['source_selector'] for r in rows} == set(NAMES) | {254}
    evidence = {str(path): digest(path) for path in (DRAFTS, CURRENT, IDENTITY, DECISIONS, Path(workflow.__file__), Path(__file__))}
    labels = []
    for binding in identity['name_bindings']:
        actor = binding['actor_ID']
        if actor not in NAMES:
            continue
        label, reason = NAMES[actor]
        forms = {f['consumer']: f for f in binding['current_consumers']}
        assert forms['progressive-nameplate']['text'] == label
        assert forms['full-catalogue']['text'] == ('Retainer' if actor in (152, 153, 155) else label)
        exact = binding['source_andcurrent_fields']
        labels.append(dict(id=f'ACTOR{actor}_RAFAEL188_200_NAME', actor_ID=actor, kind='progressive-nameplate',
            english=label, speaker=label, source_meaning=exact[0]['source']['text'],
            context='Rafael SC0 B188–B200 commodity-fashion exchanges.', decision='retention',
            retention_reason=reason, finding=reason, localization_note=reason,
            source_reference=dict(actor_ID=actor, fields=[f['source'] for f in exact]),
            current_reference=dict(actor_ID=actor, consumer='progressive-nameplate',
                text_hex=forms['progressive-nameplate']['text_hex']),
            current_consumers=binding['current_consumers'],
            review={g: g != 'formatting' for g in workflow.GATES}, new_credit=0))
    contexts = {int(k): v for k, v in drafts['source_contexts'].items() if int(k) in BLOCKS}
    env = {**workflow.review_record.__globals__, 'DECISIONS': DECISIONS, 'CONTEXTS': contexts}
    decisions = FunctionType(workflow.read_decisions.__code__, env)()
    compare = FunctionType(workflow.review_record.__code__, env)
    records = [compare(draft, before, {a: v[0] for a, v in NAMES.items()}, decisions)
               for draft, before in zip(selected, rows, strict=True)]
    assert not decisions and sum(r['kind'] == 'system-FE' for r in records) == 14
    assert not any(r['native_literal_tokens'] for r in records)
    assert {r['id'] for r in records if r.get('current_unintended_glyphs')} == UNTRANSLATED
    for row in records:
        if row['id'] in UNTRANSLATED:
            assert row['current_effective_text'].strip() == row['source_Japanese'].strip()
            row.pop('current_unintended_glyphs')
            row.pop('glyph_only_revision_with_wording_retained')
            row['current_untranslated_Japanese'] = True
    doc = dict(format='dk4-contextual-dialogue-review-v2', translation_policy='natural-dialogue-v2',
        target_locale='en-US', encoder='dialogue-relocatable-v1', review_gates=workflow.GATES,
        file_path='/data/SC0.DK4', blocks=BLOCKS, records=records, source_objects=len(records),
        **{k: current[k] for k in ('current_ROM', 'current_ROM_sha256', 'current_archive_sha256', 'runtime')},
        proposed_revisions=sum(r['decision'] == 'revision' for r in records),
        justified_retentions=sum(r['decision'] == 'retention' for r in records),
        current_glyph_defect_records=[], current_untranslated_records=sorted(UNTRANSLATED),
        all_individual_four_prose_gates_pass=True, all_fifth_formatting_gates_pending=True, new_credit=0, evidence=evidence)
    projected = deepcopy(doc)
    projected['translation_policy'] = 'natural-dialogue-v1'
    validate_natural_dialogue_batch(projected)
    save(LABELS, dict(format='dk4-scoped-name-contextual-review-v2', translation_policy='natural-dialogue-v2',
        target_locale='en-US', encoder='dialogue-relocatable-v1', records=labels, review_gates=workflow.GATES,
        all_name_formatting_gates_pending=True, runtime=current['runtime'], new_credit=0,
        no_global_name_table_changes=True, evidence=evidence))
    doc['evidence'][str(LABELS)] = digest(LABELS)
    save(OUT, doc)
    print(f"{len(records)} complete-exchange decisions: {doc['proposed_revisions']} revisions, "
          f"{doc['justified_retentions']} justified retentions, {len(labels)} role retentions and six untranslated lines corrected.")


if __name__ == '__main__':
    main()
