"""Select complete exchanges plus the distinct display and changed-layout risks."""
from scripts.audit_story_glyph_consistency import load,save
from scripts.approve_hodram_B211_B230_display_v1 import OUT
from scripts.review_hodram_B221_B230_contextual_v1 import ROOT

SELECTION=ROOT/'focused_selection_v1.json'

def main():
    assert not SELECTION.exists()
    doc=load(OUT/'storage_manuscript.json')
    ordinary=[r for r in doc['records'] if r['kind']!='typed-choice-label' and r.get('native_object_kind')!='4100-style-alternative']
    sequence=[]
    def speech(block,index):sequence.append(dict(speech=f'DK4_MES_B{block}_R{index:04d}'))
    def whole(block):
        for row in ordinary:
            if row['block']==block:sequence.append(dict(speech=row['id']))
    def style(block,offset):sequence.append(dict(style=dict(block=block,source_command_offset=offset,expected_style=4)))
    def menu(block,offset):sequence.append(dict(menu=dict(block=block,source_command_offset=offset)))
    whole(211)
    for row in ordinary:
        if row['block']==212 and (row['source_selector']==254 or row['source_reference']['record_index'] in [5,9]):sequence.append(dict(speech=row['id']))
    style(213,8);speech(213,30);style(213,702)
    whole(215)
    speech(216,5);menu(216,64);speech(216,22);speech(216,51);menu(216,230);speech(216,72);speech(216,78)
    speech(217,42);speech(217,45);style(218,8)
    whole(223)
    speech(224,47);menu(224,136);speech(224,61)
    style(226,8)
    for b,i in [(226,31),(226,34),(226,48),(228,45),(229,36),(230,16)]:speech(b,i)
    ids=[s['speech'] for s in sequence if 'speech' in s]
    assert len(ids)==len(set(ids)) and set(ids)<={r['id'] for r in ordinary}
    save(SELECTION,dict(format='dk4-disclosed-native-dialogue-fixture-selection-v2',
        fixtures=[dict(name='hodram_letters_swan_town_and_choices',sequence=sequence,
            purpose='Observe complete B211/B215/B223 exchanges, all four FE panels, FI expansion, all four native voice tables and three menus, representative names and revised page turns.')],
        chosen_fixture_path_is_a_display_sequence_not_original_branch_routing=True,
        original_conditions_locations_effects_andfull_route_unvisited=True,new_credit=0,guide_photos=False))
    print('Selected',len(sequence),'complete commands for representative emulator QA.')

if __name__=='__main__':main()
