"""Select complete tutorial exchanges and focused story/style risks without conditional-state overrides."""
from pathlib import Path
from scripts.audit_story_glyph_consistency import load,save
from dk4tool.patch.grand_race_menu_release import sha

DOC=Path('translations/rafael_B121_B140_consumer_manuscript_v5.json')
OUT=Path('translations/rafael351_focused_actual_selection_v1.json')
if __name__=='__main__':
    assert not OUT.exists();doc=load(DOC);rows=doc['records']
    def speech(block,index):
        r=next(r for r in rows if r['block']==block and r['kind']!='typed-choice-label' and r.get('native_object_kind')!='4100-style-alternative' and r['source_reference']['record_index']==index)
        return dict(speech=r['id'])
    def exchange(block,low=None,high=None,menus=True,styles=True):
        chosen=[r for r in rows if r['block']==block and r['kind']!='typed-choice-label' and r.get('native_object_kind')!='4100-style-alternative'
            and (low is None or r['source_reference']['record_index']>=low) and (high is None or r['source_reference']['record_index']<=high)]
        actions={r['source_reference']['header_offset']:dict(speech=r['id']) for r in chosen}
        left=min(actions);right=max(actions)
        for r in rows:
            if r['block']!=block:continue
            at=r.get('source_command_offset')
            if at is None or low is not None and at<left or high is not None and at>right:continue
            if menus and r['kind']=='typed-choice-label':actions[at]=dict(menu=dict(block=block,source_command_offset=at))
            elif styles and r.get('native_object_kind')=='4100-style-alternative':actions[at]=dict(style=dict(block=block,source_command_offset=at))
        return [v for _,v in sorted(actions.items())]
    tutorial=exchange(127)+exchange(128,high=107)+exchange(139)
    tutorial += [speech(129,5),dict(menu=dict(block=129,source_command_offset=80)),speech(129,24),
        speech(137,60),speech(138,18),speech(138,21),speech(140,12)]
    story=exchange(121)+exchange(133)+exchange(136,low=95,high=168)
    for block in [122,123,125]:
        offsets=sorted({r['source_command_offset'] for r in rows if r['block']==block and r.get('native_object_kind')=='4100-style-alternative'})
        story += [dict(style=dict(block=block,source_command_offset=o)) for o in offsets]
    story += [speech(135,43),speech(137,44),dict(menu=dict(block=137,source_command_offset=704))]
    fixtures=[dict(name='early_tutorials_and_controls',purpose='Complete heading/control exchange,full sail/anchor/trim explanation androute/surveyor tutorial;the fixed FE guard line,full-width I corrections,FO expansion,two-page comparison andexact Finish/Recruit Crew/Flagship labels. Selected native commands after ordinary New Game;original sailing state andquest activation are not simulated.',sequence=tutorial),
        dict(name='rescue_names_styles_andlegend',purpose='Complete rescue andCristina exchanges,the legend/remorse turn,all six original eight-slot objects under unchanged default roles,item-name continuity andremaining two-choice widths. Flat disclosed display QA sequence;not original conditional branches,locations,earned scenes orstats.',sequence=story)]
    assert len({str(a['style']) for f in fixtures for a in f['sequence'] if 'style' in a})==6
    assert len([a for f in fixtures for a in f['sequence'] if 'menu' in a])==5
    save(OUT,dict(format='dk4-disclosed-native-dialogue-fixture-selection-v2',fixtures=fixtures,
        complete_exchanges_reviewed_offline_not_a_natural_route_playthrough=True,
        no_roster_role_RNG_orcondition_override=True,all_unselected_conditional_content_offline_only=True,
        guide_photos=False,new_credit=0,evidence={str(p):sha(p.read_bytes()) for p in [DOC,Path(__file__)]}))
    print([(f['name'],len(f['sequence'])) for f in fixtures])
