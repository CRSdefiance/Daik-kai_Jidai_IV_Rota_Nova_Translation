"""Review Ian’s complete scene and bind its public nameplates to the exact actors."""
from copy import deepcopy
from pathlib import Path
from types import FunctionType
import inspect
import struct

from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.main_pool_cache_visibility import BASE
from dk4tool.rom.nds import NdsImage
from scripts import write_rafael_B177_B180_contextual_v1 as workflow
from scripts.audit_story_glyph_consistency import load, save
from scripts.check_rafael_B168_pages_on1860_v1 import IDENTITY as PREVIOUS, RELEASE, STARTUP
from scripts.prove_lil_B167_names_v4124b import names as getter
from scripts.qualify_rafael351_item_and_UI_terms_v1 import string
from scripts.registered_editorial_runtime_v2 import RegisteredRuntime
from scripts.source_locked_derivation_v5118 import checked_text


A = Path('work/analysis')
ROOT = A / 'Rafael_B169_current1860_20261105'
CURRENT = ROOT / 'current_effective.json/current_effective.json'
DRAFTS = A / 'Rafael_B161_B180_clean_20261105/B169_clean_first_v1/sealed_drafts.json'
DECISIONS = Path('translations/rafael_B169_contextual_decisions_v1.txt')
OUT = Path('translations/rafael_B169_contextual_review_v1.json')
IDENTITY = ROOT / 'names_and_terms_v1.json'
LABELS = Path('translations/rafael_B169_scoped_names_review_v1.json')
FRESH = [92, 96, 152, 164, 165]
REASONS = {
    0: ('Rafael Castor', 'Keep the approved full name. His offer to Ian and his admission that he leads a fleet identify the same speaker.'),
    5: ('Claudio Manaus', 'Keep the approved public name and Rafael’s spoken nickname Clau. His jokes remain his own.'),
    6: ('Julio Erneco', 'Keep his established public name. His speculative comment about Ian’s origins belongs to Julio.'),
    21: ('Ian Dukov', 'Keep the full established name, which Ian gives himself. Familiar dialogue uses Ian.'),
    92: ('Barkeep', 'Keep the familiar role of the person who runs the tavern and dismisses Ian. The source address establishes no kinship.'),
    96: ('Patron', 'Keep the source’s generic tavern-customer label. The scene identifies him when he returns through the repeated taunt.'),
    152: ('Sailor', 'Keep Sailor on the nameplate for the clean progressive label 水夫 and Retainer in the separate catalogue for 配下. The subordinate joins the ambush without an added rank.'),
    164: ('Man', 'Keep the concise generic label. The scene does not establish a legal, romantic or family relationship.'),
    165: ('Woman', 'Keep the concise generic label without importing a relationship from the clean role marker.'),
}


def digest(path):
    return sha(path.read_bytes())


def fields(actor, jp, ctx):
    def forms(arm, data):
        base = struct.unpack_from('<I', arm, 0xCDAC0)[0] - BASE
        for column in (0, 4, 8):
            offset = base + 32 * actor + column
            pointer = struct.unpack_from('<I', arm, offset)[0]
            yield {'field_offset': offset, **(string(data, pointer) if pointer else dict(pointer=0, hex='', text=''))}
    return [dict(column=c, source=j, current=t) for c, j, t in zip((0, 4, 8), forms(jp, jp), forms(ctx.arm, ctx.raw), strict=True)]


def main():
    assert not any(p.exists() for p in (OUT, IDENTITY, LABELS))
    drafts, current, prior = map(load, (DRAFTS, CURRENT, PREVIOUS))
    ctx = RegisteredRuntime(RELEASE, STARTUP, captain=0)
    assert ctx.receipt() == current['runtime'] == prior['runtime']
    assert prior['exact_unchanged_actor0_macro_dependencies']
    source = current['groups'][0]['records']
    assert drafts['complete_blocks'] == [169] and len(source) == len(drafts['records']) == 68
    assert {r['source_selector'] for r in source} == set(REASONS)
    code = checked_text(inspect.getsource(getter), {'for ident in [2,4,13,23,109]:': 'for ident in FRESH:'})
    native = {**getter.__globals__, 'FRESH': FRESH}
    exec(compile(code, __file__ + '::original-getters-for-five-scoped-roles', 'exec'), native)
    result = ctx.execute(native['names'])
    assert len(result['rows']) == 2 * len(FRESH)
    jp = NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    prior_actors = {b['actor_ID']: b for b in prior['name_bindings']}
    bindings, labels, names = [], [], {}
    for actor, (expected, reason) in REASONS.items():
        exact_fields = fields(actor, jp, ctx)
        if actor in FRESH:
            forms = [r for r in result['rows'] if r['actor_ID'] == actor]
        else:
            assert exact_fields == prior_actors[actor]['source_andcurrent_fields']
            forms = prior_actors[actor]['current_consumers']
        assert {r['consumer'] for r in forms} == {'progressive-nameplate', 'full-catalogue'}
        assert all(bytes.fromhex(r['text_hex']).decode('ascii') == r['text'] for r in forms)
        public = next(r for r in forms if r['consumer'] == 'progressive-nameplate')
        assert public['text'] == expected, (actor, public['text'])
        names[actor] = expected
        bindings.append(dict(actor_ID=actor, source_andcurrent_fields=exact_fields, current_consumers=forms, fresh=actor in FRESH))
        labels.append(dict(id=f'ACTOR{actor}_RAFAEL169_NAME', actor_ID=actor, kind='progressive-nameplate',
            english=expected, speaker=expected, source_meaning='Public character name or role in the clean actor fields.',
            context='Public speaker labels and separate catalogue fields for Rafael SC0 B169.',
            decision='retention', retention_reason=reason, finding=reason, localization_note=reason,
            source_reference=dict(actor_ID=actor, fields=[f['source'] for f in exact_fields]),
            current_reference=dict(actor_ID=actor, consumer='progressive-nameplate', text_hex=public['text_hex']),
            review={gate: gate != 'formatting' for gate in workflow.GATES}, new_credit=0))
    env = {**workflow.review_record.__globals__, 'DECISIONS': DECISIONS, 'CONTEXTS': {169: drafts['source_contexts']['169']}}
    read = FunctionType(workflow.read_decisions.__code__, env)
    compare = FunctionType(workflow.review_record.__code__, env)
    decisions = read()
    rows = [compare(draft, existing, names, decisions) for draft, existing in zip(drafts['records'], source, strict=True)]
    assert not decisions and all(row['kind'] == 'progressive' and not row['native_literal_tokens'] for row in rows)
    prior_role_review = Path('translations/hodram_B151_B170_scoped_names_final_v1.json')
    old_role = next(r for r in load(prior_role_review)['records'] if r['actor_ID'] == 152)
    assert old_role['english'] == 'Sailor' and 'distinct Retainer consumers' in old_role['retention_reason']
    role_forms = next(r for r in bindings if r['actor_ID'] == 152)['current_consumers']
    assert {r['consumer']: r['text'] for r in role_forms} == {'progressive-nameplate': 'Sailor', 'full-catalogue': 'Retainer'}
    evidence = {str(p): digest(p) for p in (DRAFTS, CURRENT, PREVIOUS, DECISIONS, prior_role_review, Path(workflow.__file__), Path(__file__))}
    save(LABELS, dict(format='dk4-scoped-name-contextual-review-v2', translation_policy='natural-dialogue-v2',
        target_locale='en-US', encoder='dialogue-relocatable-v1', records=labels, review_gates=workflow.GATES,
        all_name_formatting_gates_pending=True, runtime=ctx.receipt(), new_credit=0, no_global_name_table_changes=True, evidence=evidence))
    save(IDENTITY, dict(runtime=ctx.receipt(), actors=sorted(REASONS), name_bindings=bindings, fresh_actors=FRESH,
        exact_reused_actors=sorted(REASONS.keys() - set(FRESH)), scoped_names=str(LABELS), scoped_names_sha256=digest(LABELS),
        exact_unchanged_actor0_macro_dependencies=True, macro_ascii_lengths=prior['macro_ascii_lengths'],
        new_credit=0, evidence={**evidence, **prior['evidence']}))
    doc = dict(format='dk4-contextual-dialogue-review-v2', translation_policy='natural-dialogue-v2', target_locale='en-US',
        encoder='dialogue-relocatable-v1', review_gates=workflow.GATES, file_path='/data/SC0.DK4', blocks=[169],
        records=rows, source_objects=68, **{k: current[k] for k in ('current_ROM', 'current_ROM_sha256', 'current_archive_sha256', 'runtime')},
        proposed_revisions=sum(r['decision'] == 'revision' for r in rows), justified_retentions=sum(r['decision'] == 'retention' for r in rows),
        current_glyph_defect_records=[r['id'] for r in rows if r.get('current_unintended_glyphs')],
        all_individual_four_prose_gates_pass=True, all_fifth_formatting_gates_pending=True, new_credit=0,
        evidence={**evidence, str(IDENTITY): digest(IDENTITY), str(LABELS): digest(LABELS)})
    check = deepcopy(doc)
    check['translation_policy'] = 'natural-dialogue-v1'
    validate_natural_dialogue_batch(check)
    save(OUT, doc)
    print(f"68 comparisons, {doc['proposed_revisions']} revisions, {doc['justified_retentions']} retentions and nine scoped name decisions.")


if __name__ == '__main__':
    main()
