"""Select representative complete native commands for disclosed display/controller testing."""
from scripts.audit_story_glyph_consistency import load,save
from scripts.approve_hodram_B281_B300_display_v5 import ROOT,OUT

def main():
    target=ROOT/'focused_selection_v1.json';assert not target.exists()
    doc=load(OUT/'storage_manuscript.json')
    ordinary=[r for r in doc['records'] if r['kind']!='typed-choice-label' and r.get('native_object_kind')!='4100-style-alternative']
    sequence=[]
    def speech(b,i):sequence.append(dict(speech=f'DK4_MES_B{b}_R{i:04d}'))
    def block(b):sequence.extend(dict(speech=r['id']) for r in ordinary if r['block']==b)
    def menu(b,c):sequence.append(dict(menu=dict(block=b,source_command_offset=c)))
    def style(b,c):sequence.append(dict(style=dict(block=b,source_command_offset=c,expected_style=4)))
    block(282) # Complete request, FA expansion and the corrected two-page conclusion.
    for i in [85,89,93,97,100,104,107,111,115,119]:speech(283,i)
    block(287) # Complete captive/reward/villager exchange, ? and one-page map response.
    # Both bear alternatives are intentionally concatenated for display coverage;
    # their original conditions, menu routing and consequences are not simulated.
    objects=[(r['source_reference']['offset']-5,dict(speech=r['id'])) for r in ordinary if r['block']==290]
    objects += [(c,dict(menu=dict(block=290,source_command_offset=c))) for c in [876,1876]]
    objects += [(c,dict(style=dict(block=290,source_command_offset=c,expected_style=4))) for c in [24,328,1166,1924,2398,3300]]
    sequence.extend(action for _,action in sorted(objects,key=lambda p:p[0]))
    for i in [70,73,77,100]:speech(291,i)
    style(291,824);menu(291,1114)
    for i in [115,119,123,127,152,186,211,221,225]:speech(291,i)
    for i in [71,75,78]:speech(294,i)
    menu(294,820)
    for i in [93,96,99,103,107,111,115,118,122,126,135,143]:speech(294,i)
    block(296) # Complete Charles rockfall/sulfur conversation, including silence glyph.
    for i in [258,265,269,278]:speech(299,i)
    for i in [40,43,46,50,54]:speech(300,i)
    menu(300,560)
    for i in [68,72,75,94,98,110,119,148,152,155,159,170,174,178,182,186,194,197,201,208]:speech(300,i)
    selected=[r['speech'] for r in sequence if 'speech' in r]
    assert len(selected)==len(set(selected)) and set(selected)<={r['id'] for r in ordinary}
    assert len([r for r in sequence if 'menu' in r])==5
    assert len([r for r in sequence if 'style' in r])==7
    save(target,dict(format='dk4-disclosed-native-dialogue-fixture-selection-v2',
        fixtures=[dict(name='hodram_royal_ruins_beasts_and_gunpowder',sequence=sequence,
            purpose='Corrected two-page royal conclusion and one-page map response; captive/villager exchange; all five native menus; representative voice objects/fallbacks; five punctuation targets; injury FE blank-row correction, fatigue/confusion/reward/share/sound notices; Charles gunpowder exchange, countdown and bog rescue; pagination and transitions.')],
        chosen_fixture_path_is_a_display_sequence_not_original_branch_routing=True,
        original_conditions_locations_effects_andfull_route_unvisited=True,
        optional_party_andmutually_exclusive_outcomes_concatenated_for_display_testing=True,
        no_roster_state_RNG_event_orresult_override=True,new_credit=0,guide_photos=False))
    print(dict(selected_ordinary_speeches=len(selected),style_commands=7,menus=5))

if __name__=='__main__':main()
