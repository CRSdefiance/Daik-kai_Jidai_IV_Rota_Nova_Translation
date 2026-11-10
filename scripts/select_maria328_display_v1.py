"""Select concrete FE/menu/pagination/style risks for one disclosed initialized QA sequence."""
from scripts.meaning_maria328_clean_v1 import ROOT
from scripts.audit_story_glyph_consistency import load,save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest

def main():
    target=ROOT/'display_selection_v1.json';assert not target.exists()
    rebuiltpath=ROOT/'reconstruction_v1/reconstruction.json';storedpath=ROOT/'stored_v1/stored_native_verification.json'
    rebuilt,stored=map(load,[rebuiltpath,storedpath]);native=load(rebuilt['native']);doc=load(rebuilt['manuscript'])
    styles=load(rebuilt['styles']);roles=load(ROOT/'formatting_v1/role_bindings.json')
    assert stored['reconstruction_sha256']==digest(rebuiltpath) and stored['complete_stored_pages']==321
    byid={r['id']:r for r in native['records']};source={r['id']:r for r in doc['records']}
    voices={r['source_selector']:r['source_voice_class'] for r in roles['native_roles']['rows']}
    def speech(block,index):return dict(speech=f'DK4_MES_B{block}_R{index:04d}')
    def style(block,offset):return dict(style=dict(block=block,source_command_offset=offset))
    def menu(block,offset):return dict(menu=dict(block=block,source_command_offset=offset))
    sequence=[style(86,10),*[speech(86,i) for i in [28,32,36]],speech(87,132),speech(87,135),
        dict(speech='DK4_MES_B87_R0139_FE_PAGE_1'),dict(speech='DK4_MES_B87_R0139_FE_PAGE_2'),menu(87,816),
        *[speech(87,i) for i in [194,198,204,208,212,216,220,223,229]],
        *[speech(92,i) for i in [6,9,13,17,21,24]],menu(92,372),*[speech(92,i) for i in [44,48,52,55]],
        speech(76,38),speech(77,12),speech(88,204),speech(94,73),
        speech(95,5),speech(95,11),style(95,138),*[speech(95,i) for i in [38,42,45,49,53]],
        style(95,400),*[speech(95,i) for i in [82,86,89,92]]]
    selected=[];pages=0
    for action in sequence:
        if 'menu' in action:continue
        if 'speech' in action:ident=action['speech']
        else:
            request=action['style']
            proof=next(p for p in styles['objects'] if p['block']==request['block'] and p['source_command_offset']==request['source_command_offset'])
            selector=bytes.fromhex(proof['target_object_hex'])[19]
            request['expected_style']=voices[selector]
            ident=proof['native_slots'][voices[selector]]['record_id']
        assert ident in byid
        selected.append(ident);display=byid[ident]['complete_native_English_display']
        pages+=1 if byid[ident]['kind']=='system-FE' else len(display['pages'])
    assert len(selected)==len(set(selected)) and sum('menu' in a for a in sequence)==2
    assert any('{MACRO:FI}' in source[i]['english'] for i in selected)
    frames=4001+(pages+2)*240+6000
    spec=dict(name='Maria328_FE_menus_styles_pagination',sequence=sequence,
        purpose='Focused actual display QA: source-owned two-panel FE riddle and A-to-three-choice return; repaired bean FE rows and a default wrong answer; normal/FE portrait transitions; four complete progressive continuations; complete dynamic208/214/215 style objects and rescue dialogue. Copied source segments share the initialized Hangzhou host. Original event conditions, locations, chronology, branches, rewards and other effects are not simulated.',
        selection_source_utterances=len(selected),selection_expected_pages=pages,frames=frames,capture_extra=[],extra_inputs=[])
    save(target,dict(fixtures=[spec],selected_speech_ids=selected,selected_physical_body_candidates=len(selected),selected_body_pages=pages,
        unvisited_body_ids=sorted(set(byid)-set(selected)),
        expected_menu_observation='Default selection0 and normal A return for two three-choice menus; other choices/cancel remain offline-only.',
        all_other_conditional_lines_remain_offline_qualified=True,natural_activation=False,earned_chronology=False,
        actual_gameplay_pending=True,new_credit=0,guide_photos=False,
        evidence={str(p):digest(p) for p in [rebuiltpath,storedpath,ROOT/'formatting_v1/role_bindings.json',__file__]}))
    print('Selected',len(selected),'physical bodies',pages,'pages/two menus/three complete style objects;',frames,'frames; actual observation pending.')

if __name__=='__main__':main()
