"""Select representative story and town displays and bind the stored catalogue check."""
from pathlib import Path
import sys

from scripts.audit_story_glyph_consistency import load, save
from scripts.bind_rafael_B181_B200_names_v1 import CURRENT, ROOT
from scripts.prepare_rafael_B170_B176_focus_v1 import catalogue as earlier, TEMPLATE
from scripts.source_locked_derivation_v5118 import checked_text


SELECTION = ROOT / 'focused_selection_v1.json'
STORY = {
    181: (5,19,118,144,163),
    182: (9,44,82,87,91),
    183: (14,19,31,47,65,75,88,97,117,142,150),
    184: (7,35,59,85),
    185: (14,43,54),
    186: (12,22,33,57,70,79,108,168,171,174,182,195,199,202),
    187: (6,10,15,19,23,26,29,34,47,51,55,59,64,68,72,75,79,83,87,91,96,100,104,109,113,118,121,125,147,155),
}
TOWN = {
    188: (6,9,38), 189: (12,16,37), 190: (7,10,24,32,36,40,47,51),
    191: (6,9,13,16,20,24,28,31,35,39,43,47,50,54), 192: (5,9,28,31,38,73),
    193: (23,27,31,35,39), 194: (11,21,62), 195: (10,28,35,49,53,61,73,83,95),
    196: (6,10,14,18,22,26,30,33,36), 197: (16,19,29), 198: (13,23,63),
    199: (6,10,45,60), 200: (6,10,30,38,41,45),
}


def select():
    assert not SELECTION.exists()
    groups = load(CURRENT)['groups']
    fixtures = []
    actors, fe = set(), set()
    for name, blocks, purpose in (
        ('rafael_yifa_julian_aziza', STORY, 'Check normal glyphs and pauses, name expansion, both crown presentations and every Aziza FE body.'),
        ('rafael_town_forecasts', TOWN, 'Check all thirteen local forecasts, the separate door sound, and representative bread, wine, tea and other exchanges.'),
    ):
        keys = {(b,i) for b, indices in blocks.items() for i in indices}
        selected = [r for g in groups for r in g['records'] if (g['block'],r['source_reference']['record_index']) in keys]
        assert len(selected) == len(keys)
        actors.update(r['source_selector'] for r in selected if r['source_selector'] != 254)
        fe.update(r['id'] for r in selected if r['source_selector'] == 254)
        fixtures.append(dict(name=name, speech_ids=[r['id'] for r in selected], purpose=purpose))
    assert fe == {r['id'] for g in groups for r in g['records'] if r['source_selector'] == 254}
    assert len(fe) == 27 and len(actors) == 29
    save(SELECTION,dict(fixtures=fixtures, expected_FE_bodies=sorted(fe), expected_ordinary_actor_IDs=sorted(actors),
        only_selected_complete_source_commands_after_native_initializers=True,
        natural_activation=False, original_locations=False, event_economic_effects_unobserved=True,
        guide_photos=False, new_credit=0))
    print([(f['name'],len(f['speech_ids'])) for f in fixtures])


catalogue = checked_text(earlier,{
    'Rafael_B170_B176_current1975_20261105': 'Rafael_B181_B200_current2165_20261106',
    'len(rows)==190': 'len(rows)==384',
    'all190_stored_effective_body_bindings.json': 'all384_stored_effective_body_bindings.json',
    '190 stored story bodies pass': '384 stored story and town bodies pass',
})

if __name__ == '__main__':
    if sys.argv[1:] == ['--select']:
        select()
    else:
        exec(compile(catalogue,__file__+'::same-exact-stored-catalogue-check', 'exec'),globals())
