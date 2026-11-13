"""Sample every town forecast and distinct repaired random-scene/menu behavior."""
from pathlib import Path
from scripts.audit_story_glyph_consistency import load,save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest

ROOT=Path('work/Maria_B152_B175_clean_20261109')


def main():
    out=ROOT/'display_selection_v1.json';assert not out.exists()
    rebuiltpath=ROOT/'reconstruction_v2/reconstruction.json';storedpath=ROOT/'stored_v2/stored_native_verification.json'
    rebuilt,stored=map(load,[rebuiltpath,storedpath]);native=load(rebuilt['native'])
    assert stored['reconstruction_sha256']==digest(rebuiltpath) and stored['complete_stored_pages']==373
    assert stored['every_byte_consumed_andall_first_internal_final_glyphs_bounds_canaries_andpagination_pass']
    byid={r['id']:r for r in native['records']}
    def s(b,n):return dict(speech=f'DK4_MES_B{b}_R{n:04d}')
    def menu(b,n):return dict(menu=dict(block=b,source_command_offset=n))
    town={153:[27,72],154:[5,38],155:[4,61],156:[72,94],157:[13,35],158:[15,28],159:[22,62],160:[44,59],
        161:[29,44],162:[45,64],163:[70,84],164:[87,99],165:[19,29],166:[24,58],167:[45,55],168:[31,76]}
    mainseq=[dict(speech=r['id']) for r in native['records'] if r['block']==152]
    for b,ns in town.items():mainseq.extend(s(b,n) for n in ns)
    mainseq += [s(169,11),menu(169,218),*[s(169,n) for n in [61,73,106,151,267,44]],
        s(170,20),menu(170,230),*[s(170,n) for n in [56,92,100,108]],
        *[s(171,n) for n in [9,13,17,21,25,29,33,37,41,79,83,94]],
        *[s(174,n) for n in [25,28,35,43,78,84,98,95]],s(175,54),s(175,71)]
    second=[menu(170,230),s(170,52),s(170,56),menu(169,218),s(169,301),s(174,84),s(175,71)]
    third=[menu(170,230),s(170,84),s(170,92),s(170,100),s(170,108)]
    fixtures=[];union=set()
    for name,sequence,choice in [('Maria390_town_random_menu0',mainseq,0),('Maria390_two_andthree_menu1',second,1),('Maria390_delegation_menu2',third,2)]:
        ids=[a['speech'] for a in sequence if 'speech' in a]
        assert len(ids)==len(set(ids)) and set(ids)<=set(byid)
        pages=sum(1 if byid[i]['kind']=='system-FE' else len(byid[i]['complete_native_English_display']['pages']) for i in ids)
        assert pages==len(ids);union.update(ids)
        controls=[];captures=[];units=0
        for action in sequence:
            if 'menu' in action:
                frame=4140+units*240
                if choice:
                    controls.append(dict(start=frame,duration=4,buttons=['DOWN']))
                    if choice==2:controls.append(dict(start=frame+60,duration=4,buttons=['DOWN']))
                    captures.extend([frame-40,frame+20,frame+80,frame+120])
                units+=1
            else:units+=1
        fixtures.append(dict(name=name,sequence=sequence,selection_source_utterances=len(ids),selection_expected_pages=pages,
            frames=4001+units*240+6000,extra_inputs=controls,capture_extra=captures,expected_menu_selection=choice,
            purpose='Representative initialized display QA: all17 town forecasts with nearby named speech, full repaired wine exchange, Scents, private bargaining and reclaimed aside, intact prices and50000 glyphs, Wits, three-option delegation, Namahage FE repeats andnamed returns, andGlassmaking Guide. Copy complete commands behind original Maria host setup/effects/cleanup. Original conditions, chronology, item/stat rewards, commerce outcomes and supernatural claims are not simulated.'))
    assert len(fixtures)==3 and {169,170}=={a['menu']['block'] for f in fixtures for a in f['sequence'] if 'menu' in a}
    save(out,dict(fixtures=fixtures,selected_speech_ids=sorted(union),selected_source_bodies=len(union),
        town_forecast_blocks_sampled=list(range(152,169)),two_choice_andall_three_indices_planned=True,
        all_other_conditional_lines_remain_offline_qualified=True,natural_activation=False,earned_chronology=False,
        original_minigame_branch_reward_andstat_outcomes_not_claimed=True,actual_gameplay_pending=True,new_credit=0,guide_photos=False,
        evidence={str(p):digest(p) for p in [rebuiltpath,storedpath,ROOT/'formatting_v1/role_bindings.json',__file__]}))
    print([(f['name'],f['selection_source_utterances'],f['selection_expected_pages'],f['frames']) for f in fixtures])


if __name__=='__main__':main()
