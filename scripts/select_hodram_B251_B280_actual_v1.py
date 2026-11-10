"""Select representative exchanges and distinct display risks for one disclosed cold boot."""
from scripts.audit_story_glyph_consistency import load, save
from scripts.approve_hodram_B251_B280_display_v5 import ROOT, OUT


def main():
    target = ROOT / 'focused_selection_v1.json'
    assert not target.exists()
    doc = load(OUT / 'storage_manuscript.json')
    rows = [r for r in doc['records'] if r['kind'] != 'typed-choice-label'
            and r.get('native_object_kind') != '4100-style-alternative']
    sequence = []
    def speech(block, index):
        sequence.append(dict(speech=f'DK4_MES_B{block}_R{index:04d}'))
    def menu(block, offset):
        sequence.append(dict(menu=dict(block=block, source_command_offset=offset)))
    # Taking the compassionate figurehead: the source question and full response chain.
    for index in [5,9,15,18,22,26,33,37]:
        speech(251,index)
    menu(251,432)
    for index in [53,56,60,64,67,70,73,76,80,85,89,92]:
        speech(251,index)
    # Both puzzle/entity outcomes are deliberately ordered display samples. They are
    # not claims that original conditions, rewards or branch routing were activated.
    objects = [(r['source_reference']['offset']-5,dict(speech=r['id'])) for r in rows if r['block']==252]
    for offset in [270,1606]:
        objects.append((offset,dict(menu=dict(block=252,source_command_offset=offset))))
    for offset in [340,822]:
        objects.append((offset,dict(style=dict(block=252,source_command_offset=offset,expected_style=4))))
    sequence.extend(action for _,action in sorted(objects,key=lambda item:item[0]))
    for block in [253,265,274,280]:
        sequence.extend(dict(speech=r['id']) for r in rows if r['block']==block)
    selected = [item['speech'] for item in sequence if 'speech' in item]
    assert len(selected)==len(set(selected)) and set(selected)<={r['id'] for r in rows}
    assert {'DK4_MES_B252_R0116','DK4_MES_B252_R0184','DK4_MES_B274_R0015'}<=set(selected)
    save(target,dict(format='dk4-disclosed-native-dialogue-fixture-selection-v2',
        fixtures=[dict(name='hodram_figureheads_riddle_and_guild_returns',sequence=sequence,
            purpose='Complete figurehead response chain and guild returns; both puzzle/entity branch samples; three native menus; both voice objects; FI/FA and roles207/208; FE inscriptions, sound, entity warning, stat/reward/share notices; glyphs ?! and I; pagination and transition checks.')],
        chosen_fixture_path_is_a_display_sequence_not_original_branch_routing=True,
        original_conditions_locations_effects_andfull_route_unvisited=True,
        original_conditional_outcomes_in_B252_concatenated_for_display_testing=True,
        new_credit=0,guide_photos=False))
    print('Selected',len(selected),'ordinary speeches, two style objects and three menus.')


if __name__=='__main__':
    main()
