"""Record exact contextual and speaker decisions for Rafael B181–B187."""
from copy import deepcopy
from pathlib import Path
from types import FunctionType

from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.patch.grand_race_menu_release import sha
from scripts import write_rafael_B177_B180_contextual_v1 as workflow
from scripts.audit_story_glyph_consistency import load, save
from scripts.bind_rafael_B181_B200_names_v1 import CURRENT, OUT as IDENTITY, PRIOR
from scripts.seal_rafael_B181_B200_clean_v1 import OUT as SOURCE


DRAFTS = SOURCE / 'sealed_drafts.json'
DECISIONS = [Path(f'translations/rafael_{scope}_contextual_decisions_v1.txt') for scope in ('B181_B183', 'B184_B187')]
OUT = Path('translations/rafael_B181_B187_contextual_review_v1.json')
LABELS = Path('translations/rafael_B181_B187_scoped_names_review_v1.json')
BLOCKS = list(range(181, 188))
NAMES = {
    0: ('Rafael Castor', 'Keep the established name. The Aziza introduction gives FI and FA in the source order.'),
    5: ('Claudio Manaus', 'Keep his public name. Rafael addresses him in familiar dialogue as Clau.'),
    6: ('Julio Erneco', 'Keep his established name. Claudio’s irritated address in the Yifa scene assigns no family relationship.'),
    25: ('Yifa Sol', 'Keep the established name. Yifa gives just her first name when joining the crew.'),
    26: ('Julian Lopes', 'Keep the established name. His overtures to Mihwa use his first name in familiar speech.'),
    81: ('Sanghyeon Kan', 'Keep the established name. He gives his own first name and describes training under the same teacher as Yifa.'),
    183: ('Angel', 'Keep the source nickname for the pirate who recalls the earlier fight and answers Aziza.'),
    184: ('Snake', 'Keep the source nickname for the pirate who orders the others to surround Rafael and Claudio.'),
    201: ('Mihwa', 'Keep the shared reviewed name across both crown branches and both original name consumers.'),
    202: ('Reika', 'Keep the source-bound name for the woman who tells them about the tomb and whom Claudio later mentions.'),
}


def digest(path):
    return sha(Path(path).read_bytes())


def main():
    assert not OUT.exists() and not LABELS.exists()
    drafts, current, identity, older = map(load, (DRAFTS, CURRENT, IDENTITY, PRIOR[1]))
    assert identity['runtime'] == current['runtime'] and identity['exact_prior_ARM9_COMMON_actor_root_and_font']
    aziza = next(b for b in older['name_bindings'] if b['actor_ID'] == 27)
    assert all(f['text'] == 'Aziza Nurennahar' for f in aziza['current_consumers'])
    rows = [r for g in current['groups'] if g['block'] in BLOCKS for r in g['records']]
    selected = [r for r in drafts['records'] if r['block'] in BLOCKS]
    assert len(rows) == len(selected) == 227
    assert {r['source_selector'] for r in rows} == set(NAMES) | {254}
    evidence = {str(path): digest(path) for path in (DRAFTS, CURRENT, IDENTITY, PRIOR[1], *DECISIONS,
        Path(workflow.__file__), Path(__file__))}
    labels = []
    for binding in identity['name_bindings']:
        actor = binding['actor_ID']
        if actor not in NAMES:
            continue
        label, reason = NAMES[actor]
        forms = {f['consumer']: f for f in binding['current_consumers']}
        assert forms['progressive-nameplate']['text'] == forms['full-catalogue']['text'] == label
        exact = binding['source_andcurrent_fields']
        labels.append(dict(id=f'ACTOR{actor}_RAFAEL181_187_NAME', actor_ID=actor, kind='progressive-nameplate',
            english=label, speaker=label, source_meaning=exact[0]['source']['text'],
            context='Rafael SC0 B181–B187 recruitment and pirate exchanges.', decision='retention',
            retention_reason=reason, finding=reason, localization_note=reason,
            source_reference=dict(actor_ID=actor, fields=[f['source'] for f in exact]),
            current_reference=dict(actor_ID=actor, consumer='progressive-nameplate',
                text_hex=forms['progressive-nameplate']['text_hex']),
            current_consumers=binding['current_consumers'],
            review={g: g != 'formatting' for g in workflow.GATES}, new_credit=0))
    contexts = {int(k): v for k, v in drafts['source_contexts'].items() if int(k) in BLOCKS}
    decisions = {}
    for path in DECISIONS:
        env = {**workflow.review_record.__globals__, 'DECISIONS': path, 'CONTEXTS': contexts}
        subset = FunctionType(workflow.read_decisions.__code__, env)()
        assert not decisions.keys() & subset.keys()
        decisions.update(subset)
    compare = FunctionType(workflow.review_record.__code__, env)
    records = [compare(draft, before, {a: v[0] for a, v in NAMES.items()}, decisions)
               for draft, before in zip(selected, rows, strict=True)]
    assert not decisions
    panels = [r for r in records if r['kind'] == 'system-FE']
    assert len(panels) == 13 and all(r['block'] == 187 for r in panels)
    for row in panels:
        row.update(speaker='Aziza Nurennahar', semantic_speaker_actor_ID=27,
            native_FE_presentation_binding_pending=True)
    anomalies = [r['id'] for r in records if r.get('current_unintended_glyphs')]
    assert anomalies == ['DK4_MES_B181_R0005', 'DK4_MES_B184_R0085']
    punctuation = ['DK4_MES_B181_R0118', 'DK4_MES_B183_R0088', 'DK4_MES_B187_R0059']
    assert all(r['decision'] == 'revision' for r in records if r['id'] in punctuation)
    doc = dict(format='dk4-contextual-dialogue-review-v2', translation_policy='natural-dialogue-v2',
        target_locale='en-US', encoder='dialogue-relocatable-v1', review_gates=workflow.GATES,
        file_path='/data/SC0.DK4', blocks=BLOCKS, records=records, source_objects=len(records),
        **{k: current[k] for k in ('current_ROM', 'current_ROM_sha256', 'current_archive_sha256', 'runtime')},
        proposed_revisions=sum(r['decision'] == 'revision' for r in records),
        justified_retentions=sum(r['decision'] == 'retention' for r in records),
        current_glyph_defect_records=anomalies, punctuation_consistency_revisions=punctuation,
        source_F_literal_token_counts={t: sum(r['native_literal_tokens'].count(t) for r in records) for t in ('FI', 'FA', 'FO')},
        all_individual_four_prose_gates_pass=True, all_fifth_formatting_gates_pending=True, new_credit=0, evidence=evidence)
    projected = deepcopy(doc)
    projected['translation_policy'] = 'natural-dialogue-v1'
    validate_natural_dialogue_batch(projected)
    save(LABELS, dict(format='dk4-scoped-name-contextual-review-v2', translation_policy='natural-dialogue-v2',
        target_locale='en-US', encoder='dialogue-relocatable-v1', records=labels, review_gates=workflow.GATES,
        semantic_Aziza_native_FE_presentation_pending=True, all_name_formatting_gates_pending=True, runtime=current['runtime'],
        new_credit=0, no_global_name_table_changes=True, evidence=evidence))
    doc['evidence'][str(LABELS)] = digest(LABELS)
    save(OUT, doc)
    print(f"{len(records)} complete-exchange decisions: {doc['proposed_revisions']} revisions, "
          f"{doc['justified_retentions']} justified retentions, {len(labels)} scoped names and 13 Aziza FE panels.")


if __name__ == '__main__':
    main()
