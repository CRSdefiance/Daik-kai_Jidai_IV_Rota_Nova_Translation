"""Seal final body and name proofs using the established actor-record schema."""
from pathlib import Path

from scripts.source_locked_derivation_v5118 import checked_text


PARENT = Path(__file__).with_name('seal_rafael_B168_B169_offline_v1.py')
text = checked_text(PARENT.read_text(encoding='utf-8'), {
    "OUT = ROOT / 'offline_display_v1'": "OUT = ROOT / 'offline_display_v2'",
    "    save(NAMES, {**names, 'actors': sorted({*names['actors'], 15}), 'scoped_actors': 10,":
        "    angelo_actor = next(r for r in prior_names['actors'] if r['actor_ID'] == 15)\n"
        "    rebound = next(r for r in load(display.IDENTITY)['name_bindings'] if r['actor_ID'] == 15)\n"
        "    assert angelo_actor['native_getter_binding'] == rebound\n"
        "    actors = sorted([*names['actors'], angelo_actor], key=lambda r: r['actor_ID'])\n"
        "    assert len({r['actor_ID'] for r in actors}) == 10\n"
        "    save(NAMES, {**names, 'actors': actors, 'scoped_actors': 10,",
})
if __name__ == '__main__':
    exec(compile(text, __file__+'::source-bound-actor-records', 'exec'), globals())
