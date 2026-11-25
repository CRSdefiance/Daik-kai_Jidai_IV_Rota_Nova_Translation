"""Bind scoped actors for B181–B200 to the exact registered name consumers."""
import inspect
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.audit_story_glyph_consistency import load, save
from scripts.registered_editorial_runtime_v2 import RegisteredRuntime
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.write_rafael_B169_contextual_v1 import fields, getter


A = Path('work/analysis')
ROOT = A / 'Rafael_B181_B200_current2165_20261106'
CURRENT = ROOT / 'current_effective.json'
OUT = ROOT / 'names_and_terms_v1.json'
PRIOR = [A / p for p in (
    'Rafael_B170_B176_current1975_20261105/names_and_terms_v1.json',
    'Rafael_B168_B169_current1860_20261105/names_and_terms.json',
)]


def digest(path):
    return sha(Path(path).read_bytes())


def runtime(receipt):
    ctx = RegisteredRuntime(receipt['release_proof'], receipt['startup_proof'], captain=0)
    assert ctx.receipt() == receipt
    return ctx


def main():
    assert not OUT.exists()
    current = load(CURRENT)
    ctx = runtime(current['runtime'])
    jp = NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    actors = sorted({r['source_selector'] for g in current['groups'] for r in g['records']} - {254})
    assert len(actors) == 29
    cached = {}
    previous_docs = [load(p) for p in PRIOR]
    for path, previous in zip(PRIOR, previous_docs, strict=True):
        old = runtime(previous['runtime'])
        assert (ctx.arm, ctx.common, ctx.actor_root, ctx.actor_bytes) == (old.arm, old.common, old.actor_root, old.actor_bytes)
        assert ctx.image.read_file('/GRP/KANJI.FNT') == old.image.read_file('/GRP/KANJI.FNT')
        for binding in previous['name_bindings']:
            cached.setdefault(binding['actor_ID'], (binding, path))
    fresh = [actor for actor in actors if actor not in cached]
    code = checked_text(inspect.getsource(getter), {'for ident in [2,4,13,23,109]:': 'for ident in FRESH:'})
    native = {**getter.__globals__, 'FRESH': fresh}
    exec(compile(code, __file__ + '::original-scoped-getters', 'exec'), native)
    result = ctx.execute(native['names'])
    assert len(result['rows']) == 2 * len(fresh)
    bindings = []
    for actor in actors:
        exact = fields(actor, jp, ctx)
        if actor in cached:
            prior, path = cached[actor]
            assert exact == prior['source_andcurrent_fields']
            forms, reference = prior['current_consumers'], str(path)
        else:
            forms = [r for r in result['rows'] if r['actor_ID'] == actor]
            reference = None
        assert {r['consumer'] for r in forms} == {'progressive-nameplate', 'full-catalogue'}
        assert all(bytes.fromhex(r['text_hex']).decode('cp932') == r['text'] for r in forms)
        bindings.append(dict(actor_ID=actor, source_andcurrent_fields=exact, current_consumers=forms,
            fresh=actor in fresh, exact_dependency_reuse_reference=reference))
    save(OUT, dict(runtime=ctx.receipt(), name_bindings=bindings, fresh_actors=fresh,
        exact_reused_actors=[a for a in actors if a not in fresh], exact_prior_ARM9_COMMON_actor_root_and_font=True,
        macro_ascii_lengths=previous_docs[0]['macro_ascii_lengths'],
        name_localization_and_native_display_approval_pending=True,
        evidence={str(p): digest(p) for p in (CURRENT, *PRIOR, Path(__file__))}, new_credit=0))
    for b in bindings:
        print(b['actor_ID'], [f['source']['text'] for f in b['source_andcurrent_fields']],
              [(v['consumer'], v['text']) for v in b['current_consumers']])


if __name__ == '__main__':
    main()
