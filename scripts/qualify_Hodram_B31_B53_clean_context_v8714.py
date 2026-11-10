"""Qualify the explicit event chain and gloss both B31 variants before earlier English."""
from copy import deepcopy
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/Hodram_B31_B53_clean_context_v8714')
B53=Path('work/analysis/Hodram_B53_clean_gloss_v8712/one_first_clean_gloss_apparent_Ottoman_wanted_status_before_current_English.json')
B31=Path('work/analysis/Hodram_B53_dependency_context_v8713/complete_clean_SC1_B31_dependency_context_before_B53_English.json')

if __name__=='__main__':
    assert not ROOT.exists();warning,dependency=read(B53),read(B31)
    assert warning['current_English_body_still_unconsulted'] and dependency['source_only_no_current_English_exposed_orused'] and not dependency['inventory_failures']
    parent=deepcopy(dependency['groups'][0]);later=deepcopy(warning['groups'][0])
    assert parent['block']==31 and len(parent['records'])==2 and parent['completed_coverage_overlap']==0
    assert [r['id'] for r in parent['records']]==['DK4_MES_B31_R0013','DK4_MES_B31_R0018']
    assert [r['source_selector'] for r in parent['records']]==[34,34]
    assert parent['records'][0]['source_Japanese']=='まったく、しつこい野郎だ\nならば、この俺が相手になろう'
    assert parent['records'][1]['source_Japanese']=='まったく、しつこい野郎だ\nならば、この俺が相手になろう\n本当に恐ろしい男の怒りに\n触れる前にな'
    selected=parent['source_event_records'][0];later_event=later['source_event_records'][0]
    assert (selected['event_ID'],selected['script_block'],selected['must_be_completed'],selected['must_not_be_completed'])==(31,31,[52],[])
    assert (later_event['event_ID'],later_event['script_block'],later_event['must_be_completed'],later_event['must_not_be_completed'])==(53,53,[31],[74])
    for index,row in enumerate(parent['records']):
        gloss='The colloquial speaker complains with irritation that the person in question is very persistent, then says he himself will take that opponent on.'
        note='まったく conveys exasperation; しつこい野郎 is a rough description of a persistent fellow/opponent, and この俺 emphasizes the speaker himself. Preserve the decision to face the opponent, not a victory, death threat, promised outcome or moral judgment. The omitted addressee/third-person reference and exact scene relationship need their native source context. Do not invent a title, relative, alliance, nationality, reason for persistence or battle result.'
        if index:
            gloss+=' The warning adds that this should happen before incurring the anger of a truly frightening man.'
            note+=' Preserve the added before-clause and the unnamed frightening man. The Japanese does not name that man or independently establish that he is a sultan, commander, father, the speaker himself or a different specific character. Do not identify him by importing lore. The exact grammatical attachment and effect should be reviewed with the source branch/query and displayed context.'
        row.update(first_clean_source_gloss=gloss,source_context_note=note,
            whole_clean_utterance_read_before_current_English=True,current_English_dialogue_still_unconsulted=True,
            native_branch_membership_androle_name_full_preamble_consumer_pending=True,
            not_assumed_two_consecutive_speeches=True,
            source_meaning_only_not_editorial_orformatting_approval=True,
            no_source_prose_counter_orcompletion_credit=True)
    qualification='The explicit original EV1 prerequisite graph is event52 -> event31 -> event53: event31 requires52, and event53 requires31 while excluding74. This supplies an original dependency connection to B52, which the earlier one-line context note did not record. Different immediate prerequisites do not establish absence of a connection. These flags alone do not prove chronological proximity, a continuous conversation, original location, the completion effect of either B52 choice, natural activation or the unnamed man\'s identity. B31 has two distinct source speech objects with repeated opening content and a longer warning variant; read both but do not treat them as consecutive repetitions until original native branch/query behavior is mapped. B53 is one separate complete warning. Current English for both remains unread.'
    ROOT.mkdir(parents=True)
    save(ROOT/'three_clean_glosses_explicit52_31_53_dependency_andunnamed_man_before_current_English.json',dict(
        source_warning=str(B53),source_warning_sha256=sha(B53.read_bytes()),source_dependency=str(B31),source_dependency_sha256=sha(B31.read_bytes()),
        groups=[parent,later],explicit_source_event_chain=[52,31,53],dependency_and_scene_qualification=qualification,
        original_B53_gloss_words_andsource_refs_unchanged=True,
        old_B53_context_note_retained_as_history_corrected_only_for_explicit_dependency_connection=True,
        native_branch_query_dispatch_role_names_opaque_effects_andactual_context_pending=True,
        source_units=3,primary_B53_units=1,B31_dependency_context_units=2,
        all_three_complete_clean_utterances_glossed_before_earlier_English=True,
        current_English_for_B31_andB53_still_unconsulted=True,
        no_bounty_crime_rank_kinship_unnamed_identity_oroutcome_invented=True,
        B52_registered_build_andrelease_checks_remain_separate=True,
        no_editorial_orformatting_approval_source_prose_counter_orcompletion_credit=True,
        new_credit=0,new_emulator_runs=0,full_goal_complete=False,
        evidence={str(p):sha(Path(p).read_bytes()) for p in [B53,B31,__file__]}))
    print('B31/B53 clean-first:3source utterances glossed;explicit52->31->53 prerequisite link recorded,not continuous-scene proof. Two source variants/unnamed frightening man preserved;older English unread. Zero credit.')
