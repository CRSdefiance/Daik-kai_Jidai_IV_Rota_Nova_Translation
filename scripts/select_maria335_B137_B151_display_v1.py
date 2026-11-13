"""Select concrete glyph/wrap/tutorial/transition risks for initialized controller QA."""
from scripts.meaning_maria335_B137_B151_v1 import ROOT
from scripts.audit_story_glyph_consistency import load,save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest


def main():
    out=ROOT/'display_selection_v1.json';assert not out.exists()
    rebuiltpath=ROOT/'reconstruction_v2/reconstruction.json'
    storedpath=ROOT/'stored_v1/stored_native_verification.json'
    rebuilt,stored=map(load,[rebuiltpath,storedpath]);native=load(rebuilt['native'])
    assert stored['reconstruction_sha256']==digest(rebuiltpath) and stored['complete_stored_pages']==333
    assert stored['every_byte_consumed_andall_first_internal_final_glyphs_bounds_canaries_andpagination_pass']
    byid={r['id']:r for r in native['records']}
    def s(b,n):return dict(speech=f'DK4_MES_B{b}_R{n:04d}')
    def menu():return dict(menu=dict(block=138,source_command_offset=1274))
    mainseq=[s(137,46),s(138,70),s(138,78),menu(),
        *[s(138,n) for n in [93,97,101,105,109,113,116,119,125]],
        *[s(139,n) for n in [134,177,195,199,202,205]],s(140,116),
        *[s(141,n) for n in [9,28,43,54,60]],
        *[s(145,n) for n in [51,54,57,60,77,81,97,100]],
        s(146,56),s(148,8),s(148,12),s(149,37),s(150,36),
        *[s(151,n) for n in [6,9,20,23,31,46,50]]]
    second=[menu(),s(138,125),s(139,205)]
    fixtures=[];union=set()
    for name,sequence,choice in [('Maria335_B137_B151_tutorial_glyph_FE_menu0',mainseq,0),('Maria335_B137_B151_menu1_return',second,1)]:
        selected=[a['speech'] for a in sequence if 'speech' in a]
        assert len(selected)==len(set(selected)) and set(selected)<=set(byid)
        pages=sum(1 if byid[i]['kind']=='system-FE' else len(byid[i]['complete_native_English_display']['pages']) for i in selected)
        assert pages==len(selected);union.update(selected)
        fixtures.append(dict(name=name,sequence=sequence,selection_source_utterances=len(selected),selection_expected_pages=pages,
            frames=4001+(pages+1)*240+6000,extra_inputs=[dict(start=4140,duration=4,buttons=['DOWN'])] if choice else [],
            capture_extra=[4100,4200,4260,4320] if choice else [],expected_menu_selection=choice,
            purpose='Focused initialized Maria QA: repaired Latin I and Indeed, all eight tutorial room labels and two scoped phrase refinements, two short name questions, all three reclaimed paragraphs, six scoped FE guard repairs with named returns, both menu options, and source-faithful bread/trend prose. Preserve original host setup/effects/cleanup. Original chronology, optional conditions, historical location, skill/room effects and commodity outcomes are not simulated.'))
    assert len(union)==44
    save(out,dict(fixtures=fixtures,selected_speech_ids=sorted(union),selected_source_bodies=44,
        all_other_conditional_lines_remain_offline_qualified=True,natural_activation=False,earned_chronology=False,
        original_minigame_branch_reward_andstat_outcomes_not_claimed=True,actual_gameplay_pending=True,new_credit=0,guide_photos=False,
        evidence={str(p):digest(p) for p in [rebuiltpath,storedpath,ROOT/'formatting_v1/role_bindings.json',__file__]}))
    print([(f['name'],f['selection_source_utterances'],f['selection_expected_pages'],f['frames']) for f in fixtures])


if __name__=='__main__':main()
