"""Select tutorial exchanges and concrete display risks from the completed 557 review."""
from pathlib import Path
from scripts.audit_story_glyph_consistency import load,save
from dk4tool.patch.grand_race_menu_release import sha

DOC=Path('translations/rafael_B141_B160_formatting_manuscript_v3.json')
PLAN=Path('work/analysis/Rafael557_storage_inputs_v1_20261105/plans.json')
OUT=Path('translations/rafael557_focused_actual_selection_v1.json')

if __name__=='__main__':
    assert not OUT.exists();doc,plan=map(load,[DOC,PLAN]);rows=doc['records']
    def exchange(block,low=None,high=None):
        speeches=[r for r in rows if r['block']==block and r['kind']!='typed-choice-label'
            and (low is None or r['source_reference']['record_index']>=low)
            and (high is None or r['source_reference']['record_index']<=high)]
        actions={r['source_reference']['header_offset']:dict(speech=r['id']) for r in speeches}
        left,right=min(actions),max(actions)
        for r in rows:
            if r['block']==block and r['kind']=='typed-choice-label' and left<=r['source_command_offset']<=right:
                actions[r['source_command_offset']]=dict(menu=dict(block=block,source_command_offset=r['source_command_offset']))
        return [v for _,v in sorted(actions.items())]
    tutorial=exchange(142)+exchange(143,63,110)+exchange(143,233,294)+exchange(143,299)+exchange(146)+exchange(150)
    story=exchange(145)+exchange(148,5,53)+exchange(148,121,182)+exchange(148,224)+exchange(154,84,117)
    story += [dict(menu=dict(block=154,source_command_offset=1562))]+exchange(154,185)+exchange(152,131,144)
    selected=[a['speech'] for a in tutorial+story if 'speech' in a]
    assert len(selected)==len(set(selected))
    byid={r['id']:r for r in rows};layouts={r['id']:r for r in plan['records']}
    assert {'DK4_MES_B143_R0067','DK4_MES_B146_R0006','DK4_MES_B148_R0121'}<=set(selected)
    assert sum(byid[i]['source_selector']==254 for i in selected)==6
    menus=[a['menu'] for a in tutorial+story if 'menu' in a]
    assert len(menus)==4 and len({(m['block'],m['source_command_offset']) for m in menus})==4
    fixtures=[dict(name='tutorials_fullnames_andmaps',purpose='Complete Red Dye map exchange, palace introduction with FU, war-funds notices, combat/investment lesson, merchant invitation with FU and full water/map explanation. Exact selected native commands after ordinary New Game; original quests, locations and branch effects are not activated.',sequence=tutorial),
        dict(name='identity_FE_menus_andpagination',purpose='Reviewed Arcadius/Eirene identity and reassurance exchange, selected alliance discussion and both FE notices, the refusal two-page farewell, Maldonado choice and retained commitment, and the repaired Pereira glyph/world-politics passage. Flat disclosed display QA order, not conditional event activation or original menu narrative branches.',sequence=story)]
    save(OUT,dict(format='dk4-disclosed-native-dialogue-fixture-selection-v2',fixtures=fixtures,
        selected_source_variants=len(selected),selected_pages=sum(layouts[i]['expected_native_pages'] for i in selected),
        source_variant_IDs=selected,source_FE_IDs=[i for i in selected if byid[i]['source_selector']==254],
        ordinary_actor_IDs=sorted({byid[i]['source_selector'] for i in selected if byid[i]['source_selector']!=254}),
        complete_exchanges_reviewed_offline_not_a_natural_route_playthrough=True,
        no_roster_role_RNG_orcondition_override=True,all_unselected_conditional_content_offline_only=True,
        guide_photos=False,new_credit=0,evidence={str(p):sha(p.read_bytes()) for p in [DOC,PLAN,Path(__file__)]}))
    print(dict(fixtures=[(f['name'],len(f['sequence'])) for f in fixtures],speeches=len(selected),pages=sum(layouts[i]['expected_native_pages'] for i in selected),menus=len(menus)))
