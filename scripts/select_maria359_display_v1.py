"""Select bounded representative town, jungle and shipyard QA hosts with all five menus."""
from pathlib import Path
from scripts.audit_story_glyph_consistency import load,save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest

ROOT=Path('work/Maria_B253_B274_clean_20261110')

def main():
    output=ROOT/'display_selection_v1.json';assert not output.exists()
    rebuiltpath=ROOT/'reconstruction_v1/reconstruction.json';storedpath=ROOT/'stored_v1/stored_native_verification.json'
    rebuilt,stored=map(load,[rebuiltpath,storedpath])
    assert stored['reconstruction_sha256']==digest(rebuiltpath) and stored['complete_stored_pages']==350
    assert stored['every_byte_consumed_andall_first_internal_final_glyphs_bounds_canaries_andpagination_pass']
    doc,native,styles,menus=map(load,[rebuilt['manuscript'],rebuilt['native'],rebuilt['styles'],rebuilt['menu']])
    byid={r['id']:r for r in native['records']};rows={r['id']:r for r in doc['records']}
    def block(b,style_offsets=None):
        commands=[]
        for r in doc['records']:
            if r['block']==b and r['kind']!='typed-choice-label' and not r.get('native_object_kind'):
                commands.append((r['source_reference']['offset'],dict(speech=r['id'])))
        for o in styles['objects']:
            if o['block']==b and (style_offsets is None or o['source_command_offset'] in style_offsets):
                commands.append((o['source_command_offset'],dict(style=dict(block=b,source_command_offset=o['source_command_offset'],expected_style=4))))
        for o in menus['menus']:
            if o['block']==b:commands.append((o['source_command_offset'],dict(menu=dict(block=b,source_command_offset=o['source_command_offset']))))
        return [r for _,r in sorted(commands)]
    def speech(b,n):return dict(speech=f'DK4_MES_B{b}_R{n:04d}')
    town=[r for b in [253,254,255,256,257,258,266] for r in block(b,[])]
    town += [speech(267,55),dict(menu=dict(block=267,source_command_offset=486)),speech(267,70),speech(267,74),speech(267,89),speech(267,127)]
    jungle=[r for b in [259,263,264] for r in block(b)]
    shipyard=block(269,[24,392])+[r for b in [271,272,273,274] for r in block(b)]
    specs=[];union=set();selected_menus=set();selected_styles=set()
    for name,sequence,choice in [('Maria359_towns_London_snake_menu0',town,0),('Maria359_jungle_coin_forest_menu1',jungle,1),('Maria359_carronade_desert_compass_menu0',shipyard,0)]:
        ids=[];units=commandbytes=0;extra=[];captures=[];declared=[]
        for action in sequence:
            if 'speech' in action:
                ident=action['speech'];row=byid[ident]
                group=next(g for g in rebuilt['groups'] if g['block']==row['block'])
                text=next(t for t in group['text_records'] if t['id']==ident)
                command=next(c for c in group['all_target_commands'] if c['offset']==text['new_offset']-5)
                commandbytes+=len(bytes.fromhex(command['whole_command_hex']));ids.append(ident)
                units+=1 if row['kind']=='system-FE' else len(row['complete_native_English_display']['pages'])
            elif 'style' in action:
                req=action['style'];obj=next(o for o in styles['objects'] if (o['block'],o['source_command_offset'])==(req['block'],req['source_command_offset']))
                ident=obj['native_slots'][4]['record_id'];ids.append(ident)
                units+=len(byid[ident]['complete_native_English_display']['pages']);commandbytes+=len(bytes.fromhex(obj['target_object_hex']))
                selected_styles.add((obj['block'],obj['source_command_offset']))
            else:
                req=action['menu'];obj=next(o for o in menus['menus'] if (o['block'],o['source_command_offset'])==(req['block'],req['source_command_offset']))
                frame=4140+units*240;captures += [frame-40,frame+20,frame+80,frame+120]
                extra += [dict(start=frame+60*step,duration=4,buttons=['DOWN']) for step in range(choice)]
                declared.append(dict(**req,expected_index=choice,caption_count=2));selected_menus.add((obj['block'],obj['source_command_offset']))
                units+=1;commandbytes+=len(bytes.fromhex(obj['target_object_hex']))
        assert len(ids)==len(set(ids)) and commandbytes+512<=9216,(name,commandbytes)
        union.update(ids)
        specs.append(dict(name=name,sequence=sequence,selection_source_utterances=len(ids),selection_expected_pages=units-len(declared),
            frames=4001+units*240+6000,extra_inputs=extra,capture_extra=sorted(set(captures)),expected_menu_selection=choice,
            expected_menu_instances=declared,selected_complete_command_bytes=commandbytes,
            purpose='Representative initialized native-command display QA: complete scurvy cure on one page, London two-page transition, thirty/forty-day demonstration, jungle/forest options and complete personality commands, coin role214, desert punctuation, carronade research and actor18 header, shipwright gratitude, compass humor and all five menu returns. Concatenated disclosed QA host; original conditional activation, outcomes, rewards, chronology, full route and hardware are unvisited.'))
    assert len(selected_menus)==5
    save(output,dict(fixtures=specs,selected_speech_ids=sorted(union),selected_source_bodies=len(union),planned_original_style_objects=sorted(selected_styles),
        planned_original_menu_objects=sorted(selected_menus),unvisited_source_bodies=349-len(union),all_other_content_offline_qualified_not_claimed_gameplay=True,
        natural_activation=False,earned_chronology=False,item_stat_money_branch_outcomes_not_simulated=True,actual_gameplay_pending=True,new_credit=0,guide_photos=False,
        evidence={str(p):digest(p) for p in [rebuiltpath,storedpath,ROOT/'offline_display_approval_v1.json',Path(__file__)]}))
    print([(s['name'],s['selection_source_utterances'],s['selection_expected_pages'],s['frames'],s['selected_complete_command_bytes']) for s in specs])

if __name__=='__main__':main()
