"""Select complete source-command samples and concrete FE/menu/role/page risks for gameplay QA."""
from pathlib import Path
from scripts.audit_story_glyph_consistency import load,save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest

ROOT=Path('work/Maria_B216_B252_clean_20261110')


def main():
    out=ROOT/'display_selection_v1.json';assert not out.exists()
    rebuiltpath=ROOT/'reconstruction_v1/reconstruction.json';storedpath=ROOT/'stored_v1/stored_native_verification.json'
    rebuilt,stored=map(load,[rebuiltpath,storedpath]);doc,native,styles,menus=map(load,[rebuilt['manuscript'],rebuilt['native'],rebuilt['styles'],rebuilt['menu']])
    rolespath=ROOT/'dynamic_roles_current_v1.json';roles=load(rolespath)
    assert stored['reconstruction_sha256']==digest(rebuiltpath) and stored['complete_stored_pages']==353
    assert stored['every_byte_consumed_andall_first_internal_final_glyphs_bounds_canaries_andpagination_pass']
    assert stored['runtime']==roles['runtime']==doc['runtime']
    byid={r['id']:r for r in native['records']};assert len(byid)==351
    voices={r['source_selector']:r['source_voice_class'] for r in roles['native_roles']['rows']}
    assert all(voices[v]==4 for v in [208,211,215,216])
    def speech(b,n):return dict(speech=f'DK4_MES_B{b}_R{n:04d}')
    def words(b,ns):return [speech(b,n) for n in ns]
    def menu(b,at,index=None):return dict(menu=dict(block=b,source_command_offset=at,**({} if index is None else dict(expected_index=index))))
    def style(b,at):return dict(style=dict(block=b,source_command_offset=at,expected_style=4))
    def whole(b):return [dict(speech=r['id']) for r in doc['records'] if r['block']==b and not r.get('native_object_kind') and r['kind']!='typed-choice-label']
    figure_prefix=[4,8,14,17,21,25,32,36]
    town_take=[a for b in [216,217,218,219,222,223,224] for a in whole(b)]
    town_take += words(220,figure_prefix)+[menu(220,404)]+words(220,[51,54,58,62,65,68,71,74,78,83,87,90])
    town_take += [a for b in [225,226,227,228] for a in whole(b)]
    town_take += [menu(252,1876),style(252,1924),speech(252,277),style(252,2398),speech(252,304),speech(252,312),style(252,3046)]
    refusal=words(220,figure_prefix)+[menu(220,404)]+words(220,[97,101,107,110,114])
    refusal += words(221,[5,8,11])+[menu(221,270),speech(221,67),style(221,846),speech(221,89)]
    refusal += words(221,[110,114,118,121,125,128,132,136,140,143])+[menu(221,1622)]+words(221,[183,194,206,211,222,225])
    refusal += [a for b in [237,238,239,249,250,251] for a in whole(b)]
    refusal += [menu(252,882),style(252,1172),speech(252,174),speech(252,178),style(252,1640)]+words(252,[213,217,221,232])+[style(252,3306)]
    correct=[a for b in [229,230,231,232,233,234,235,236,240,241,242] for a in whole(b)]
    correct += words(221,[5,8,11])+[menu(221,270)]+words(221,[104,110,114,118,121,125])
    correct += [style(252,24),style(252,328),speech(252,61),style(252,676),speech(252,91),speech(252,95),menu(252,882),menu(252,1876,1),speech(252,312),style(252,3046),style(252,3306)]
    selected_styles=set();selected_menus=set();union=set();fixtures=[]
    for name,sequence,default in [('Maria363_towns_take_Plett_scare_menu0',town_take,0),
        ('Maria363_refusal_riddle_left_sleep_menu1',refusal,1),('Maria363_guilds_riddle_right_forest_other_menu2',correct,2)]:
        ids=[];units=command_bytes=0;controls=[];captures=[];declared=[]
        for action in sequence:
            if 'speech' in action:
                key=action['speech'];row=byid[key];assert not row.get('native_object_kind')
                group=next(g for g in rebuilt['groups'] if g['block']==row['block'])
                record=next(t for t in group['text_records'] if t['id']==key)
                command=next(c for c in group['all_target_commands'] if c['offset']==record['new_offset']-5)
                command_bytes+=len(bytes.fromhex(command['whole_command_hex']));ids.append(key)
                units+=1 if row['kind']=='system-FE' else len(row['complete_native_English_display']['pages'])
            elif 'style' in action:
                request=action['style'];obj=next(o for o in styles['objects'] if o['block']==request['block'] and o['source_command_offset']==request['source_command_offset'])
                selector=bytes.fromhex(obj['source_object_hex'])[19];assert voices[selector]==request['expected_style']==4
                key=obj['native_slots'][4]['record_id'];ids.append(key);units+=len(byid[key]['complete_native_English_display']['pages'])
                command_bytes+=len(bytes.fromhex(obj['target_object_hex']));selected_styles.add((request['block'],request['source_command_offset']))
            else:
                request=action['menu'];obj=next(o for o in menus['menus'] if o['block']==request['block'] and o['source_command_offset']==request['source_command_offset'])
                count=len(obj['record_ids']);choice=request.get('expected_index',default);assert count in [2,3] and choice in range(count)
                frame=4140+units*240;captures.extend([frame-40,frame+20,frame+80,frame+120])
                controls.extend(dict(start=frame+60*step,duration=4,buttons=['DOWN']) for step in range(choice))
                declared.append(dict(**{k:v for k,v in request.items() if k!='expected_index'},expected_index=choice,caption_count=count))
                command_bytes+=len(bytes.fromhex(obj['target_object_hex']));units+=1;selected_menus.add((request['block'],request['source_command_offset']))
        assert len(ids)==len(set(ids)) and set(ids)<=set(byid)
        assert command_bytes+512<=9216,(name,command_bytes)
        union.update(ids)
        fixtures.append(dict(name=name,sequence=sequence,selection_source_utterances=len(ids),selection_expected_pages=units-len(declared),
            frames=4001+units*240+6000,extra_inputs=controls,capture_extra=sorted(set(captures)),expected_menu_selection=default,
            expected_menu_instances=declared,selected_complete_command_bytes=command_bytes,
            purpose='Representative initialized native-command QA: town ruins leads and gold-river wrapping; figurehead take/refusal; all five source menus and puzzle directions; repaired FE riddle/instruction/angry-voice rows and A returns; Plett/Jean/Peralonso/Jacob/Yuris/Hernan exchanges, names, roles and macros; both two-page reports; forest selectors208/211/215/216, bear responses, conditional Emilio sleep and ordinary host exit. Separate conditional samples are concatenated in a disclosed QA host using complete original commands. Original branch outcomes, stats, rewards, natural activation, earned geography/chronology, future crew assignments, full-route and hardware coverage are not claimed.'))
    assert len(fixtures)==3 and selected_menus=={(220,404),(221,270),(221,1622),(252,882),(252,1876)}
    save(out,dict(fixtures=fixtures,selected_speech_ids=sorted(union),selected_source_bodies=len(union),
        planned_original_style_objects=sorted(selected_styles),planned_original_menu_objects=sorted(selected_menus),
        unvisited_source_bodies=351-len(union),all_other_content_offline_qualified_not_claimed_gameplay=True,
        natural_activation=False,earned_chronology=False,item_stat_money_branch_outcomes_not_simulated=True,
        actual_gameplay_pending=True,new_credit=0,guide_photos=False,
        evidence={str(p):digest(p) for p in [rebuiltpath,storedpath,rolespath,ROOT/'offline_display_approval_v1.json',Path(__file__)]}))
    print([(f['name'],f['selection_source_utterances'],f['selection_expected_pages'],f['frames'],f['selected_complete_command_bytes']) for f in fixtures])


if __name__=='__main__':main()
