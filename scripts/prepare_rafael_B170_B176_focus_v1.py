"""Select representative whole commands for the six modal pages and named scenes."""
from scripts.audit_story_glyph_consistency import load, save
from scripts.plan_rafael_B170_B176_display_v1 import ROOT, CURRENT
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.check_rafael_B168_B169_stored_catalogue_v1 import source as old_catalogue, TEMPLATE


SELECTION = ROOT / 'focused_selection_v1.json'
BLOCKS = {
    170: (5,25,44,50,59,84,112,139,149,201,232,241,244,248,253,266,297,305,312),
    171: (10,13,31,39,44,47,52,61,64,68,76,80,88,92,99,103),
    172: (11,19,25,48,51,69,73,99,114,118,129,133,141),
    173: (5,29,48,58,62,66,70,95),
    174: (6,),
    176: (5,18,40,44,52,68,86,91,98,106,119,131,135,140,148),
}
catalogue = checked_text(old_catalogue, {
    'Rafael_B168_B169_current1860_20261105': 'Rafael_B170_B176_current1975_20261105',
    'len(rows)==115': 'len(rows)==190',
    'all115_stored_effective_body_bindings.json': 'all190_stored_effective_body_bindings.json',
    '115 stored story bodies pass': '190 stored story bodies pass',
})


def select():
    assert not SELECTION.exists()
    groups = load(CURRENT)['groups']
    selection = {(block,n) for block, rows in BLOCKS.items() for n in rows}
    records = [r for g in groups for r in g['records']
               if (r['block'],r['source_reference']['record_index']) in selection]
    assert len(records) == len(selection) == 72
    assert sum(r['source_selector']==254 for r in records) == 6
    assert {r['source_selector'] for r in records} - {254} == {0,5,6,7,8,11,19,20,22,105,116,142,151}
    save(SELECTION, dict(fixtures=[dict(name='carlo_cristina_samwell_and_jam',
        speech_ids=[r['id'] for r in records],
        purpose='Verify the six modal presentations, ordinary A transitions and all scoped names, including both FI substitutions.')],
        only_selected_complete_source_commands_after_native_initializers=True,
        B175_duplicate_update_checked_in_storage_only=True,
        natural_activation=False, original_locations=False, guide_photos=False, new_credit=0))


if __name__ == '__main__':
    import sys
    if sys.argv[1:] == ['--select']:
        select()
    else:
        exec(compile(catalogue, __file__+'::unchanged-source-bound-catalogue-read', 'exec'), globals())
