"""Fresh clean whole-exchange context for a retrospective layout lead, without new credit."""
from copy import deepcopy
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/retrospective_B218_wrap_gloss_v7832')
LEADS=Path('work/analysis/completed_contraction_wrap_leads_v7831/completed_layout_contraction_andquestion_tag_leads_with_live_storage_refs.json')
GLOSSES={
5:"The companion addresses the admiral and says he heard information in town about a splendid weapon.",
8:"Lil questions that description. If he calls it splendid, it must really be impressive. She asks the weapon's name.",
11:"He explains that it is called Ares's Holy Spear because tradition says Ares, one of the twelve Olympian gods, possessed it. Preserve the attribution to a legend.",
14:"Lil does not know who Ares is. She tentatively takes his point that the spear must be impressive and immediately asks where to obtain it.",
17:"According to rumor, armor named after other members of the twelve Olympian gods may also be lying nearby. This is uncertain hearsay, not a guaranteed item reward or a precise location.",
20:"Lil is impatient with the indirect explanation and presses for where it actually is.",
23:"He infers from townspeople's way of talking that it may be somewhere in this vicinity, and says he very much wants to find it. No specific site is identified.",
27:"Lil privately observes that he is interested and finds that somewhat unexpected. The aside conveys mild surprise at this companion's interest, not a discovery, announcement, insult or new relationship.",
30:"The companion notices Lil's odd expression, asks what is wrong, and asks whether his interest in legends is unexpected.",
34:"Lil agrees, explaining that weapons seem unlike him or do not suit him. Keep the personal impression without adding cowardice, incompetence or a new occupation.",
37:"He allows that she may be right, then explains that mysterious stories move him: the gods of myth who once ranged all over this land. His fascination is with the evocative legend.",
40:"Just thinking that weapons those gods may have used remain in the world makes his thoughts fly back to antiquity. Keep may-have-used and the imaginative emotional response; no supernatural effect is demonstrated.",
43:"Lil responds hesitantly that she does not really understand. The exchange ends with their differing interests intact, without her adopting his enthusiasm.",
}
if __name__=='__main__':
    assert not ROOT.exists();leads=read(LEADS)
    group=next(g for g in leads['source_current_native_groups'] if g['file_path']=='/data/SC2.DK4' and g['block']==218)
    records=[]
    for r in group['source_complete_native_speech_boundaries']:
        assert r['record_index'] in GLOSSES
        records.append(dict(id=f"DK4_MES_B218_R{r['record_index']:04d}",file_path='/data/SC2.DK4',block=218,
            source_reference=deepcopy(r),source_hex=r['raw_hex'],source_Japanese=bytes.fromhex(r['raw_hex'])[1:].decode('cp932'),
            fresh_clean_context_gloss=GLOSSES[r['record_index']],
            purpose='Retrospective formatting of an already credited exchange; no new translation or completion credit.'))
    assert len(records)==len(GLOSSES)==13
    ROOT.mkdir(parents=True)
    save(ROOT/'thirteen_fresh_clean_exchange_glosses_before_full_current_layout_review.json',dict(
        file_path='/data/SC2.DK4',block=218,source_block_sha256=group['source_block_sha256'],
        records=records,whole_exchange_read=True,
        emotional_progression='Practical Lil asks for a useful weapon and concrete location; her companion describes an uncertain local legend, then reveals a reflective love of ancient myth. Her private surprise leads to his explanation and her remaining incomprehension.',
        target_R27_complete_parenthetical_short_predicate='The thought is a two-sentence aside. A coherent short final predicate should be considered together under the original width without changing its words or source controls.',
        current_target_historical_plan_seen_as_lead=True,
        full_current_exchange_not_yet_read_this_retrospective_pass=True,
        no_new_complete_translation_pass_orcompletion_credit_claim=True,new_credit=0,new_emulator_runs=0,
        evidence={str(p):sha(p.read_bytes()) for p in [LEADS,Path(__file__)]},full_goal_complete=False))
    print('All13 B218 clean speeches freshly glossed asan exchange;full current-layout comparison next.No duplicate credit.')
