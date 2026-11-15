"""Select actual display risks without simulating original optional story outcomes."""
from scripts.meaning_maria337_clean_v1 import ROOT
from scripts.audit_story_glyph_consistency import load,save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest


def main():
    out=ROOT/'display_selection_v1.json';assert not out.exists()
    rebuiltpath=ROOT/'reconstruction_v1/reconstruction.json'
    storedpath=ROOT/'stored_v1/stored_native_verification.json'
    rebuilt,stored=map(load,[rebuiltpath,storedpath]);native=load(rebuilt['native'])
    assert stored['reconstruction_sha256']==digest(rebuiltpath) and stored['complete_stored_pages']==339
    byid={r['id']:r for r in native['records']}
    def s(b,n):return dict(speech=f'DK4_MES_B{b}_R{n:04d}')
    def menu():return dict(menu=dict(block=136,source_command_offset=356))
    mainseq=[s(127,29),s(128,65),s(128,80),
        *[s(130,n) for n in [207,210,213,218,221,225,229,271]],
        *[s(131,n) for n in [13,16,19,24,27,32,36,39,43,46,49,52]],
        s(132,191),s(132,242),s(135,294),
        *[s(135,n) for n in [321,325,328,332,335,338,341,344,348,351,354,357,360,363,366,369]],
        s(136,15),s(136,19),s(136,23),menu(),s(136,211)]
    second=[menu(),s(136,88),s(136,113),s(136,211)]
    fixtures=[];union=[]
    for name,sequence,selection in [('Maria337_glyphs_FE_tutorial_menu0',mainseq,0),('Maria337_menu1_return',second,1)]:
        selected=[a['speech'] for a in sequence if 'speech' in a]
        assert len(selected)==len(set(selected)) and set(selected)<=set(byid)
        pages=sum(1 if byid[i]['kind']=='system-FE' else len(byid[i]['complete_native_English_display']['pages']) for i in selected)
        union.extend(selected)
        fixtures.append(dict(name=name,sequence=sequence,selection_source_utterances=len(selected),selection_expected_pages=pages,
            frames=4001+(pages+1)*240+6000,extra_inputs=[dict(start=4140,duration=4,buttons=['DOWN'])] if selection else [],
            capture_extra=[4100,4200,4260,4320] if selection else [],expected_menu_selection=selection,
            purpose='Focused initialized Maria display QA: full Latin glyphs, names/substitutions, six FE panels and their named returns, all four two-page tutorial paragraphs, thresholds/equipment, both repaired captions and ordinary menu return. Exact source commands retain complete native controls behind all original host setup/effects/cleanup. Original story chronology, conditions, locations, minigame, outcomes, stats and rewards are not simulated.'))
    assert {f'DK4_MES_B135_R{n:04d}' for n in [325,335,351,366]}<=set(union)
    save(out,dict(fixtures=fixtures,selected_speech_ids=sorted(set(union)),selected_source_bodies=len(set(union)),
        all_other_conditional_lines_remain_offline_qualified=True,natural_activation=False,earned_chronology=False,
        original_minigame_branch_reward_andstat_outcomes_not_claimed=True,actual_gameplay_pending=True,new_credit=0,guide_photos=False,
        evidence={str(p):digest(p) for p in [rebuiltpath,storedpath,ROOT/'formatting_v1/role_bindings.json',__file__]}))
    print([(f['name'],f['selection_source_utterances'],f['selection_expected_pages'],f['frames']) for f in fixtures])


if __name__=='__main__':main()
