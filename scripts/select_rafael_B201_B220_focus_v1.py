"""Select representative town, staged-panel, pagination, and menu cases for emulator display QA."""
from pathlib import Path

from scripts.audit_story_glyph_consistency import load, save
from scripts.plan_rafael_B201_B220_v1 import ROOT, digest


SOURCE=ROOT/'offline_display_package_v2'
OUT=ROOT/'focused_selection_v1.json'


def main():
    assert not OUT.exists()
    manifest=SOURCE/'formatting_manuscript.json'
    plan=SOURCE/'automatic_plans.json'
    rows=load(manifest)['records']
    planned={r['id']:r for r in load(plan)['records']}
    byid={r['id']:r for r in rows}
    def exchange(block, low=0, high=9999):
        speeches=[r for r in rows if r['block']==block and r['kind']!='typed-choice-label'
            and low<=r['source_record_index']<=high]
        assert speeches
        ordered={r['source_reference']['header_offset']:dict(speech=r['id']) for r in speeches}
        left,right=min(ordered),max(ordered)
        for r in rows:
            if r['block']==block and r['kind']=='typed-choice-label' and left<=r['source_command_offset']<=right:
                offset=r['source_command_offset']
                ordered[offset]=dict(menu=dict(block=block,source_command_offset=offset))
        return [entry for _,entry in sorted(ordered.items())]

    town=[]
    town_ranges={
        201:((22,30),(49,65)), 202:((48,59),(67,85)), 203:((53,72),(84,100)),
        204:((6,30),), 205:((17,33),(44,59)), 206:((46,60),), 207:((58,77),),
    }
    for block,ranges in town_ranges.items():
        for low,high in ranges:
            town.extend(exchange(block,low,high))
    story=exchange(210,10,42)+exchange(211,33,76)+exchange(212,25,58)+exchange(216)+exchange(217)+exchange(220,25,51)
    mixed=exchange(208,5,46)+exchange(208,264,294)+exchange(209,5,49)+exchange(213,22,84)+exchange(218,37,93)
    specs=[
        dict(name='rafael_town_forecasts',sequence=town,
            purpose='Check all seven forecasts and representative china, medicine, dye, tobacco, chili, sake and cheese exchanges.'),
        dict(name='rafael_letter_and_parrot',sequence=story,
            purpose='Check namahage calls, the portrait discovery, the rescue, the castle letter with its signature, all parrot echoes and the sword conversation.'),
        dict(name='rafael_merchants_and_choices',sequence=mixed,
            purpose='Check two separate offers with identical captions, the three-option book choice, rope prices, both earring menus and the two-page pitch.'),
    ]
    all_actions=town+story+mixed
    selected=[a['speech'] for a in all_actions if 'speech' in a]
    assert len(selected)==len(set(selected))
    assert {'DK4_MES_B204_R0030','DK4_MES_B206_R0052','DK4_MES_B213_R0031',
        'DK4_MES_B216_R0074','DK4_MES_B217_R0052','DK4_MES_B218_R0048'}<=set(selected)
    assert planned['DK4_MES_B218_R0048']['expected_native_pages']==2
    selected_menus=[a['menu'] for a in all_actions if 'menu' in a]
    assert {(m['block'],m['source_command_offset']) for m in selected_menus}=={
        (208,218),(208,1588),(209,230),(213,860),(218,836),(218,1006)}
    save(OUT,dict(format='dk4-disclosed-native-dialogue-fixture-selection-v2',fixtures=specs,
        selected_source_variants=len(selected),selected_pages=sum(planned[i]['expected_native_pages'] for i in selected),
        source_variant_IDs=selected,source_FE_IDs=[i for i in selected if byid[i]['source_selector']==254],
        ordinary_actor_IDs=sorted({byid[i]['source_selector'] for i in selected if byid[i]['source_selector']!=254}),
        menus=selected_menus,unselected_speeches_offline_only=True,original_conditions_and_effects_not_activated=True,
        complete_exchanges_reviewed_offline_not_a_natural_route_playthrough=True,guide_photos=False,new_credit=0,
        evidence={str(p):digest(p) for p in (manifest,plan,Path(__file__))}))
    print([(s['name'],len(s['sequence'])) for s in specs],len(selected),'speeches,',len(selected_menus),'menus')


if __name__=='__main__':
    main()

