"""Seal all 190 contextual decisions and the scoped speaker names for B170–B176."""
from copy import deepcopy
import inspect
from pathlib import Path
from types import FunctionType

from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load, save
from scripts.registered_editorial_runtime_v2 import RegisteredRuntime
from scripts.seal_rafael_B170_B176_current_inputs_v1 import OUT as SOURCE
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.write_rafael_B169_contextual_v1 import fields, getter, NdsImage
from scripts import write_rafael_B177_B180_contextual_v1 as workflow


A = Path('work/analysis')
ROOT = A / 'Rafael_B170_B176_current1975_20261105'
CURRENT = ROOT / 'current_effective.json'
DRAFTS = SOURCE / 'sealed_drafts.json'
PRIOR = A / 'Rafael_B168_B169_current1860_20261105/names_and_terms.json'
DECISIONS = Path('translations/rafael_B170_B176_contextual_decisions_v1.txt')
OUT = Path('translations/rafael_B170_B176_contextual_review_v1.json')
LABELS = Path('translations/rafael_B170_B176_scoped_names_review_v1.json')
IDENTITY = ROOT / 'names_and_terms_v1.json'
NAMES = {
    0: ('Rafael Castor', 'Keep the approved public name and the exact FI substitution Claudio uses.'),
    5: ('Claudio Manaus', 'Keep the approved nameplate. Rafael’s familiar Clau is spoken dialogue.'),
    6: ('Julio Erneco', 'Keep the established name. His proposal to Carlo refers to a new family.'),
    7: ('Cristina Erneco', 'Keep the established Cristina spelling. Her nameplate identifies the dancer and agrees with the corrected spoken lines.'),
    8: ('Arcadius Eudoxios', 'Keep the source-bound public name in the dock sequence. The full-catalogue middle name remains separate.'),
    11: ('Jam Ludwyan', 'Keep the short nameplate distinct from Jam’s full spoken Jam Jack Ludwyan.'),
    19: ('Carlo Sinat', 'Keep the established Carlo Sinat nameplate and use it in his spoken introduction.'),
    20: ('Fernando Dias', 'Keep the approved full name for his two comments.'),
    22: ('Samwell Khan', 'Keep the short nameplate. The spoken introduction and full catalogue include da.'),
    105: ('Trader', 'Keep the occupation label. Carlo addresses this trader as Adil in speech.'),
    116: ('Port Worker', 'Keep the departure office role. The source does not confer rank.'),
    142: ('Innkeeper', 'Keep the native role and let her spoken familiarity with Adil stand without assigning a family tie.'),
    151: ('Sailor', 'Keep the progressive sailor label and the distinct Retainer catalogue form.'),
}
STAGED = {
    'DK4_MES_B171_R0044': ('<Patron 1>',),
    'DK4_MES_B171_R0047': ('<Patron 2>',),
    'DK4_MES_B171_R0061': ('<Patron 1>', '<Patron 2>'),
}


def digest(path):
    return sha(Path(path).read_bytes())


def main():
    assert not any(p.exists() for p in (OUT, LABELS, IDENTITY))
    drafts, current, prior = map(load, (DRAFTS, CURRENT, PRIOR))
    assert drafts['complete_blocks'] == [g['block'] for g in current['groups']] == list(range(170, 177))
    rt, old = current['runtime'], prior['runtime']
    ctx, oldctx = [RegisteredRuntime(r['release_proof'], r['startup_proof'], captain=0) for r in (rt, old)]
    assert ctx.receipt() == rt and oldctx.receipt() == old
    assert ctx.release['parent_sha256'] == old['candidate_sha256']
    assert (ctx.arm, ctx.common, ctx.actor_root, ctx.actor_bytes) == (oldctx.arm, oldctx.common, oldctx.actor_root, oldctx.actor_bytes)
    assert ctx.image.read_file('/GRP/KANJI.FNT') == oldctx.image.read_file('/GRP/KANJI.FNT')
    assert prior['exact_unchanged_actor0_macro_dependencies']
    rows = [r for g in current['groups'] for r in g['records']]
    assert len(rows) == len(drafts['records']) == 190
    assert {r['source_selector'] for r in rows} == set(NAMES) | {254}
    cached = {b['actor_ID']: b for b in prior['name_bindings']}
    fresh = sorted(set(NAMES) - cached.keys())
    assert fresh == [105, 116, 142, 151]
    env = {**getter.__globals__, 'FRESH': fresh}
    code = checked_text(inspect.getsource(getter), {'for ident in [2,4,13,23,109]:': 'for ident in FRESH:'})
    exec(compile(code, __file__ + '::original-role-getters', 'exec'), env)
    getters = ctx.execute(env['names'])['rows']
    assert len(getters) == 2 * len(fresh)
    jp = NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    bindings, labels = [], []
    for actor, (expected, reason) in NAMES.items():
        exact = fields(actor, jp, ctx)
        if actor in cached:
            assert exact == cached[actor]['source_andcurrent_fields']
            forms = cached[actor]['current_consumers']
        else:
            forms = [r for r in getters if r['actor_ID'] == actor]
        assert {r['consumer'] for r in forms} == {'progressive-nameplate', 'full-catalogue'}
        public = next(r for r in forms if r['consumer'] == 'progressive-nameplate')
        assert public['text'] == expected and bytes.fromhex(public['text_hex']).decode('ascii') == expected
        bindings.append(dict(actor_ID=actor, source_andcurrent_fields=exact, current_consumers=forms, fresh=actor in fresh))
        labels.append(dict(id=f'ACTOR{actor}_RAFAEL170_176_NAME', actor_ID=actor, kind='progressive-nameplate',
            english=expected, speaker=expected, source_meaning='Public character name or role in the clean actor fields.',
            context='Public speaker labels and separate catalogue fields for Rafael SC0 B170–B176.',
            decision='retention', retention_reason=reason, finding=reason, localization_note=reason,
            source_reference=dict(actor_ID=actor, fields=[f['source'] for f in exact]),
            current_reference=dict(actor_ID=actor, consumer='progressive-nameplate', text_hex=public['text_hex']),
            review={g: g != 'formatting' for g in workflow.GATES}, new_credit=0))
    env = {**workflow.review_record.__globals__, 'DECISIONS': DECISIONS,
           'CONTEXTS': {int(k): v for k, v in drafts['source_contexts'].items()}}
    decisions = FunctionType(workflow.read_decisions.__code__, env)()
    compare = FunctionType(workflow.review_record.__code__, env)
    records = [compare(draft, existing, {a: v[0] for a, v in NAMES.items()}, decisions)
               for draft, existing in zip(drafts['records'], rows, strict=True)]
    assert not decisions and sum(r['kind'] == 'system-FE' for r in records) == 6
    assert sum(len(r['native_literal_tokens']) for r in records) == 2
    for row in records:
        if row['id'] in STAGED:
            headings = STAGED[row['id']]
            prefix = ''.join(headings) + ' '
            assert row['english'].startswith(prefix)
            source_rows = row['source_Japanese'].splitlines()
            expected = ''.join('＜客' + ('１' if '1' in h else '２') + '＞' for h in headings)
            assert source_rows[0] == expected and len(source_rows) >= 2
            row.update(source_staged_FE=True, source_heading_row=source_rows[0], native_heading_tokens=headings,
                       localized_modal_body=row['english'][len(prefix):], FE_source_layout_native_requalification_pending=True)
    evidence = {str(p): digest(p) for p in (DRAFTS, CURRENT, PRIOR, DECISIONS, Path(workflow.__file__), Path(__file__))}
    save(LABELS, dict(format='dk4-scoped-name-contextual-review-v2', translation_policy='natural-dialogue-v2',
        target_locale='en-US', encoder='dialogue-relocatable-v1', records=labels, review_gates=workflow.GATES,
        all_name_formatting_gates_pending=True, runtime=rt, new_credit=0, no_global_name_table_changes=True, evidence=evidence))
    save(IDENTITY, dict(runtime=rt, actors=sorted(NAMES), name_bindings=bindings, fresh_actors=fresh,
        exact_reused_actors=sorted(set(NAMES) - set(fresh)), scoped_names=str(LABELS), scoped_names_sha256=digest(LABELS),
        exact_unchanged_actor0_macro_dependencies=True, exact_prior_ARM9_COMMON_actor_root_and_font=True,
        macro_ascii_lengths=prior['macro_ascii_lengths'], new_credit=0, evidence={**prior['evidence'], **evidence}))
    doc = dict(format='dk4-contextual-dialogue-review-v2', translation_policy='natural-dialogue-v2', target_locale='en-US',
        encoder='dialogue-relocatable-v1', review_gates=workflow.GATES, file_path='/data/SC0.DK4',
        blocks=list(range(170,177)), records=records, source_objects=190,
        **{k: current[k] for k in ('current_ROM','current_ROM_sha256','current_archive_sha256','runtime')},
        proposed_revisions=sum(r['decision']=='revision' for r in records), justified_retentions=sum(r['decision']=='retention' for r in records),
        current_glyph_defect_records=[r['id'] for r in records if r.get('current_unintended_glyphs')],
        all_individual_four_prose_gates_pass=True, all_fifth_formatting_gates_pending=True, new_credit=0,
        evidence={**evidence, str(IDENTITY): digest(IDENTITY), str(LABELS): digest(LABELS)})
    preliminary = deepcopy(doc)
    preliminary['translation_policy'] = 'natural-dialogue-v1'
    validate_natural_dialogue_batch(preliminary)
    save(OUT, doc)
    print(dict(records=len(records), revisions=doc['proposed_revisions'], retentions=doc['justified_retentions'],
               scoped_names=len(labels), FE=6, structurally_staged_FE=len(STAGED)))


if __name__ == '__main__':
    main()
