"""Read the complete explicit B39 signaling prerequisite for B49; no dialogue credit."""
from pathlib import Path
from scripts.verify_village_wrap_v608 import read,save
from dk4tool.patch.grand_race_menu_release import sha
ROOT=Path('work/analysis/Rafael_B49_prerequisite_gloss_v8077')
SOURCE=Path('work/analysis/Rafael_B49_prerequisite_B39_v8076/complete_clean_SC0_B39_EV0_andcoverage_before_current_English.json')
TARGET=Path('work/analysis/Rafael_next_clean_v8073/complete_clean_SC0_B49_EV0_andcoverage_before_current_English.json')
GLOSSES={
11:'A sailor alerts the admiral to a vessel that appears to be a Dutch merchant ship and seems to be signaling something. The ship identification is tentative.',
15:'Rafael wonders what it is and asks whether the signal can be understood.',
19:'The sailor enthusiastically says the signal will be decoded.',
24:'In an alternative source branch, Janus addresses FI as admiral and tentatively identifies the signaling ship as a Dutch merchantman.',
27:'Rafael asks Janus whether he can understand it.',
31:'Janus hesitates politely and offers to decode the signal.',
37:'Claudio assumes there may be a fight and expresses eager anticipation.',
48:'Arcadius calls him a barbarian under the breath or as a quiet aside.',
52:'Claudio asks whether something was said.',
56:'Arcadius asks whether he heard it, with dry humor.',
63:'Rafael reminds Claudio that their voyage is not a mission to pick fights around the world.',
68:'Claudio answers with exaggerated deference to FI as admiral, saying he understands. This is banter, not a new rank or hierarchy.',
71:'Rafael asks about the result of the signal decoding.',
82:'The sailor reports that the signal says to put into Amsterdam.',
87:'In an alternative branch, Janus says it seems to be an instruction to put into Amsterdam and asks what they should do.',
93:'Rafael hesitates and asks for opinions.',
103:'The sailor asks whether they should stop in Amsterdam for the time being.',
108:'Arcadius finds the situation suspicious but thinks complying is preferable to the possibility of being ambushed at sea. Do not turn this into proof of a planned ambush or guaranteed safety.',
112:'Rafael privately notices that Arcadius also has strategic judgment. Do not add an identity reveal or invented biography.',
119:'Claudio argues that the other fleet is not so large and proposes forcing their way through. This is his argument, not a verified fleet census.',
123:'Rafael says he would rely on Claudio if it came to that, but hesitates to take that course.',
127:'Rafael decides to proceed cautiously and put into port once.',
}
if __name__=='__main__':
    assert not ROOT.exists();source,target=map(read,[SOURCE,TARGET]);g=source['groups'][0]
    assert len(g['records'])==len(GLOSSES)==22 and {r['source_record_index'] for r in g['records']}==set(GLOSSES)
    event=target['groups'][0]['source_event_records'][0];assert event['event_ID']==49 and 39 in event['must_be_completed']
    ROOT.mkdir(parents=True)
    save(ROOT/'complete22_clean_B39_glosses_explicit_B49_prerequisite_context_only.json',dict(
        source_packet=str(SOURCE),source_packet_sha256=sha(SOURCE.read_bytes()),target_source_packet=str(TARGET),target_source_packet_sha256=sha(TARGET.read_bytes()),
        records=[dict(**r,context_source_gloss=GLOSSES[r['source_record_index']]) for r in g['records']],
        explicit_source_B49_requires_event39=True,source_B39_event=g['source_event_records'],
        conversation_progression='A possibly Dutch merchantman signals; Claudio wants a fight; Rafael and Arcadius favor caution; the signal instructs Amsterdam; Rafael decides to put into port.',
        source_branch_alternatives_not_yet_native_verified=[[11,15,19],[24,27,31],[82],[87]],
        source_signal_names_Amsterdam_butdoesnot_prove_native_B49_city_scheduler_eligibility=True,
        no_claim_that_Lil_sent_signal_orformal_pact_already_exists=True,
        whole_B39_clean_context_read_without_current_English_comparison=True,
        context_only_no_new_source_prose_orcompletion_credit=True,new_credit=0,new_emulator_runs=0,full_goal_complete=False,
        evidence={str(p):sha(p.read_bytes()) for p in [SOURCE,TARGET,Path(__file__)]}))
    print('Complete22-speech clean B39 prerequisite read/glossed forB49. Amsterdam signal iscontext,not proved native activation. No credit orcurrent English comparison.')
