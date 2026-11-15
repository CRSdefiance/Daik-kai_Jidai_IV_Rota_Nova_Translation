"""Sample complete random exchanges and concrete menu/style/FE/page risks in three runs."""
from pathlib import Path
from scripts.audit_story_glyph_consistency import load,save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest

ROOT=Path('work/Maria_B176_B195_clean_20261110')


def main():
    out=ROOT/'display_selection_v1.json';assert not out.exists()
    rebuiltpath=ROOT/'reconstruction_v1/reconstruction.json';storedpath=ROOT/'stored_v1/stored_native_verification.json'
    rebuilt,stored=map(load,[rebuiltpath,storedpath]);doc=load(rebuilt['manuscript']);native=load(rebuilt['native']);styles=load(rebuilt['styles'])
    rolespath=ROOT/'dynamic_roles_current_v1.json';roles=load(rolespath)
    assert stored['reconstruction_sha256']==digest(rebuiltpath) and stored['complete_stored_pages']==302
    assert stored['every_byte_consumed_andall_first_internal_final_glyphs_bounds_canaries_andpagination_pass']
    assert stored['runtime']==roles['runtime']==doc['runtime']
    byid={r['id']:r for r in native['records']};voice={r['source_selector']:r['source_voice_class'] for r in roles['native_roles']['rows']}
    def speech(b,n):return dict(speech=f'DK4_MES_B{b}_R{n:04d}')
    def menu(b,at):return dict(menu=dict(block=b,source_command_offset=at))
    def style(b,at):return dict(style=dict(block=b,source_command_offset=at,expected_style=voice[208]))
    def whole(b):return [dict(speech=r['id']) for r in doc['records'] if r['block']==b and r.get('native_object_kind') is None and r['kind']!='typed-choice-label']
    mainseq=whole(178)+whole(177)+whole(180)
    mainseq += [speech(185,31),menu(185,242),*[speech(185,n) for n in [50,53,57,61]]]
    mainseq += [*[speech(179,n) for n in [4,8,12,16,19,23,27,31,35,38,41,45,48,52]],menu(179,818),
        *[speech(179,n) for n in [67,70,74]],menu(179,990),speech(179,89)]
    second=[style(182,8),*[speech(182,n) for n in [26,29,32]],style(182,702),speech(182,70),
        style(187,8),*[speech(187,n) for n in [33,37,40,43,47,50,61,67,74,86]],
        speech(179,74),menu(179,990),*[speech(179,n) for n in [96,99,102,105]],
        speech(185,31),menu(185,242),speech(185,71)]
    third=[speech(185,31),menu(185,242),speech(185,77),*[speech(188,n) for n in [36,40,44,47,50,53]],
        *whole(195),*[speech(176,n) for n in [53,56,59,62,66,69,73,76,79]]]
    fixtures=[];union=set();selected_style_objects=set();selected_menu_objects=set()
    for name,sequence,choice in [('Maria305_random_trade_menu0',mainseq,0),('Maria305_letters_refusal_menu1',second,1),('Maria305_armor_glyphs_menu2',third,2)]:
        ids=[];units=0;controls=[];captures=[];menus=[];command_bytes=0
        for action in sequence:
            if 'speech' in action:
                ident=action['speech'];row=byid[ident];assert not row.get('native_object_kind')
                group=next(g for g in rebuilt['groups'] if g['block']==row['block'])
                text=next(t for t in group['text_records'] if t['id']==ident)
                command=next(c for c in group['all_target_commands'] if c['offset']==text['new_offset']-5)
                command_bytes+=len(bytes.fromhex(command['whole_command_hex']))
                pages=1 if row['kind']=='system-FE' else len(row['complete_native_English_display']['pages'])
                ids.append(ident);units+=pages
            elif 'style' in action:
                req=action['style'];obj=next(o for o in styles['objects'] if o['block']==req['block'] and o['source_command_offset']==req['source_command_offset'])
                assert req['expected_style']==4 and voice[208]==4
                ident=obj['native_slots'][4]['record_id'];ids.append(ident)
                units+=len(byid[ident]['complete_native_English_display']['pages']);command_bytes+=len(bytes.fromhex(obj['target_object_hex']))
                selected_style_objects.add((req['block'],req['source_command_offset']))
            else:
                req=action['menu'];obj=next(o for o in load(rebuilt['menu'])['menus'] if o['block']==req['block'] and o['source_command_offset']==req['source_command_offset'])
                count=len(obj['record_ids']);assert choice<count
                frame=4140+units*240;captures.extend([frame-40,frame+20,frame+80,frame+120])
                for step in range(choice):controls.append(dict(start=frame+60*step,duration=4,buttons=['DOWN']))
                menus.append(dict(**req,expected_index=choice,caption_count=count));selected_menu_objects.add((req['block'],req['source_command_offset']))
                command_bytes+=len(bytes.fromhex(obj['target_object_hex']));units+=1
        assert len(ids)==len(set(ids)) and set(ids)<=set(byid);union.update(ids)
        pages=units-len(menus);assert command_bytes+512<=9216,(name,command_bytes)
        fixtures.append(dict(name=name,sequence=sequence,selection_source_utterances=len(ids),selection_expected_pages=pages,
            frames=4001+units*240+6000,extra_inputs=controls,capture_extra=sorted(set(captures)),expected_menu_selection=choice,
            expected_menu_instances=menus,selected_complete_command_bytes=command_bytes,
            purpose='Representative initialized display QA with complete stored commands and the full original Maria host. Random parrot/castle/weapon exchanges, native FE letter return, complete dynamic style tables, menu indices0/1/2, Japanese Guan Yu repair, full signatures, two-page letters/armor, FI Charm,1000/100 pricing andcorrected I/F glyphs. Original event conditions, earned locations, item/stat/money rewards, original branch execution andfull route/hardware are not claimed.'))
    assert len(fixtures)==3 and len(union)==127 and len(selected_style_objects)==3 and len(selected_menu_objects)==3
    assert [(f['selection_source_utterances'],f['selection_expected_pages']) for f in fixtures]==[(73,74),(24,26),(33,35)]
    save(out,dict(fixtures=fixtures,selected_speech_ids=sorted(union),selected_source_bodies=len(union),
        planned_original_style_objects=sorted(selected_style_objects),planned_original_menu_objects=sorted(selected_menu_objects),
        complete_parrot_castle_Emilio_random_exchanges_selected=True,unvisited_source_bodies=294-len(union),
        all_other_content_offline_qualified_not_claimed_gameplay=True,natural_activation=False,earned_chronology=False,
        item_stat_money_branch_outcomes_not_simulated=True,actual_gameplay_pending=True,new_credit=0,guide_photos=False,
        evidence={str(p):digest(p) for p in [rebuiltpath,storedpath,rolespath,ROOT/'offline_display_approval_v1.json',Path(__file__)]}))
    print([(f['name'],f['selection_source_utterances'],f['selection_expected_pages'],f['frames'],f['selected_complete_command_bytes']) for f in fixtures])


if __name__=='__main__':main()
