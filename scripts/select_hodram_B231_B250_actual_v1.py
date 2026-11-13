"""Select complete exchanges and concrete glyph, substitution, menu and pagination risks."""
from scripts.audit_story_glyph_consistency import load,save
from scripts.approve_hodram_B231_B250_display_v2 import ROOT,OUT

SELECTION=ROOT/'focused_selection_v1.json'

def main():
    assert not SELECTION.exists()
    doc=load(OUT/'storage_manuscript.json')
    ordinary=[r for r in doc['records'] if r['kind']!='typed-choice-label' and r.get('native_object_kind')!='4100-style-alternative']
    sequence=[]
    def speech(block,index): sequence.append(dict(speech=f'DK4_MES_B{block}_R{index:04d}'))
    def whole(block):
        for row in ordinary:
            if row['block']==block:sequence.append(dict(speech=row['id']))
    def style(block): sequence.append(dict(style=dict(block=block,source_command_offset=8,expected_style=4)))
    speech(236,30)
    style(238)
    for index in [35,44,50]:speech(238,index)
    style(239);whole(239)
    for index in [18,28]:speech(240,index)
    whole(242)
    for index in [6,10,14,17,52,64]:speech(243,index)
    sequence.append(dict(menu=dict(block=243,source_command_offset=674)))
    for index in [79,95,163]:speech(243,index)
    speech(244,14);speech(245,7);speech(247,6)
    for block in [248,249,250]:whole(block)
    ids=[s['speech'] for s in sequence if 'speech' in s]
    assert len(ids)==len(set(ids)) and set(ids)<={r['id'] for r in ordinary}
    assert {r['id'] for r in ordinary if r['source_selector']==254}<=set(ids)
    save(SELECTION,dict(format='dk4-disclosed-native-dialogue-fixture-selection-v2',
        fixtures=[dict(name='hodram_letters_rose_figurehead_and_survey',sequence=sequence,
            purpose='Complete Jam letter/replies, Rose exchange and Rio survey job/replies; both source voice objects; all four FE panel bodies and FI substitutions; Fernando ASCII F, isolated question mark, revised one/two-page transitions and original two-choice consumer.')],
        chosen_fixture_path_is_a_display_sequence_not_original_branch_routing=True,
        original_conditions_locations_effects_andfull_route_unvisited=True,new_credit=0,guide_photos=False))
    print('Selected',len(sequence),'native commands for one representative cold boot.')

if __name__=='__main__':main()
