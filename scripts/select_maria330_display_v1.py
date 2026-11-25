"""Select distinct display risks for representative initialized emulator QA; no chronology or effects claim."""
from scripts.meaning_maria330_clean_v1 import ROOT
from scripts.audit_story_glyph_consistency import load,save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest

def main():
    out=ROOT/'display_selection_v1.json';assert not out.exists()
    rebuiltpath=ROOT/'reconstruction_v2/reconstruction.json';storedpath=ROOT/'stored_v1/stored_native_verification.json'
    rebuilt,stored=map(load,[rebuiltpath,storedpath]);native=load(rebuilt['native']);doc=load(rebuilt['manuscript']);styles=load(rebuilt['styles'])
    rolespath=ROOT/'formatting_v1/role_bindings.json';roles=load(rolespath)
    assert stored['reconstruction_sha256']==digest(rebuiltpath) and stored['complete_stored_pages']==338
    byid={r['id']:r for r in native['records']};voices={r['source_selector']:r['source_voice_class'] for r in roles['native_roles']['rows']}
    def s(b,i):return dict(speech=f'DK4_MES_B{b}_R{i:04d}')
    def style(b,c):return dict(style=dict(block=b,source_command_offset=c))
    def menu():return dict(menu=dict(block=102,source_command_offset=210))
    mainseq=[s(105,16),s(105,23),style(96,16),style(99,58),style(99,446),s(99,52),
        s(121,10),s(121,13),s(121,19),*[s(116,i) for i in [7,11,15,24,36]],
        dict(speech='DK4_MES_B116_R0041_FE_PAGE_1'),dict(speech='DK4_MES_B116_R0041_FE_PAGE_2'),s(116,44),s(116,48),
        dict(speech='DK4_MES_B116_R0051_FE_PAGE_1'),dict(speech='DK4_MES_B116_R0051_FE_PAGE_2'),
        *[s(116,i) for i in [54,58,61,68,72,82,110]],s(110,11),style(122,12),style(122,158),s(122,49),s(122,53),s(122,60),
        *[s(102,i) for i in [4,8,12,32,35]],menu(),*[s(102,i) for i in [50,58,65,73,83,87,110,118]],s(98,13),s(115,4),s(118,8)]
    second=[menu(),*[s(102,i) for i in [147,151,155,159,163,167]]]
    fixtures=[];union=[]
    for name,sequence,extra,selection in [('Maria330_FE_glyphs_styles_menu0',mainseq,[],0),
        ('Maria330_menu1_return',second,[dict(start=4140,duration=4,buttons=['DOWN'])],1)]:
        selected=[];pages=0
        for action in sequence:
            if 'menu' in action:continue
            if 'speech' in action:ident=action['speech']
            else:
                request=action['style'];obj=next(p for p in styles['objects'] if p['block']==request['block'] and p['source_command_offset']==request['source_command_offset'])
                selector=bytes.fromhex(obj['target_object_hex'])[19];request['expected_style']=voices[selector];ident=obj['native_slots'][voices[selector]]['record_id']
            assert ident in byid;selected.append(ident);display=byid[ident]['complete_native_English_display']
            pages+=1 if byid[ident]['kind']=='system-FE' else len(display['pages'])
        assert len(selected)==len(set(selected));union.extend(selected)
        fixtures.append(dict(name=name,sequence=sequence,selection_source_utterances=len(selected),selection_expected_pages=pages,
            frames=4001+(pages+1)*240+6000,capture_extra=[4100,4200,4260,4320] if selection==1 else [],extra_inputs=extra,
            expected_menu_selection=selection,purpose='Focused initialized Maria display QA. Exact reviewed commands sample source-owned FE continuations, complete page clauses, full style tables, three repaired Latin I lines, runtime name/company tokens and native two-choice selection/return. The original host setup/effects/cleanup remain; original story conditions, chronology, locations, branch effects, rewards and stats are not simulated.'))
    save(out,dict(fixtures=fixtures,selected_speech_ids=sorted(set(union)),selected_physical_body_candidates=len(set(union)),
        all_other_conditional_lines_remain_offline_qualified=True,default_menu_then_second_menu_selection_requested=True,
        original_story_choice_branch_orstat_outcomes_not_claimed=True,natural_activation=False,earned_chronology=False,
        actual_gameplay_pending=True,new_credit=0,guide_photos=False,
        evidence={str(p):digest(p) for p in [rebuiltpath,storedpath,rolespath,__file__]}))
    print([(f['name'],f['selection_source_utterances'],f['selection_expected_pages'],f['frames']) for f in fixtures])

if __name__=='__main__':main()
