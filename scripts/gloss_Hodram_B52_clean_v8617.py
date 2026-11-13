"""Read all three clean speeches and both source choices before existing English."""
from copy import deepcopy
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/Hodram_B52_clean_gloss_v8617')
SOURCE=Path('work/analysis/Hodram_B52_clean_v8616/complete_clean_SC1_B52_EV1_andcoverage_before_current_English.json')
GLOSSES={
    'DK4_MES_B52_R0006':(
        "The colloquial speaker asks whether the addressee intends to make an enemy of the group called ハイレディン一家.",
        "Preserve the question about intention. 一家 refers to the named person's group/outfit here; it does not independently establish blood kinship. Bind its approved faction/person spelling separately. Do not turn the question into confirmed existing hostility, a war declaration, a government order, or a claim about rank, criminality or nationality."),
    'DK4_MES_B52_R0021':(
        "Then withdraw/leave quickly, before you are spotted.",
        "The speaker follows up with brisk advice to leave before being noticed. Preserve the then and the prospective not-yet-spotted condition. Do not invent a specific lookout, pursuer, location, authority, escape outcome or new travel restriction. Its native menu/branch membership remains to be executed."),
    'DK4_MES_B52_R0033':(
        "You are reckless with your life / you do not fear for your life, do you?",
        "命知らず is a colloquial comment on dangerous boldness or recklessness; the drawn-out ねえ gives a commenting reaction. It neither guarantees death nor supplies an explicit threat, insult, admiration, past feat or battle result. Read its emotional effect with the confident source choice, while leaving exact native branch outcomes unapproved."),
}
CHOICES=[
    ('そんな気はない','That is not my intention. / I have no intention of doing that.',
     'Denies the intention posed in the preceding question; do not recast it as surrender, a promise of alliance, cowardice or a relationship.'),
    ('相手になろう','I will take them on. / I will be their opponent.',
     'A willing, confident challenge in response to the preceding question; do not claim that battle has started, that victory is assured, or that a new rank or relationship exists.'),
]
if __name__=='__main__':
    assert not ROOT.exists();packet=read(SOURCE)
    assert packet['source_only_no_current_English_exposed_orused'] and not packet['inventory_failures']
    group=deepcopy(packet['groups'][0]);raw=bytes.fromhex(group['clean_block_hex']);rows=group['records']
    assert group['block']==52 and group['clean_stored_bytes']==group['clean_logical_end']==228 and group['clean_tail_bytes']==0
    assert list(GLOSSES)==[r['id'] for r in rows] and [r['source_selector'] for r in rows]==[113,113,113]
    assert len(group['commands'])==14 and group['completed_coverage_overlap']==0
    for row in rows:
        assert row['current_English_body_unread'] and not row['already_contextually_completed'] and row['source_decode_error'] is None
        assert bytes.fromhex(row['source_hex'])[1:].decode('cp932')==row['source_Japanese']
        gloss,note=GLOSSES[row['id']]
        row.update(first_clean_source_gloss=gloss,source_context_note=note,whole_clean_exchange_andboth_choice_labels_read=True,current_English_dialogue_still_unconsulted=True,source_meaning_only_not_localized_orformatting_approval=True,native_speakers_menu_queries_branches_opaque_controls_terminal_current_actual_release_pending=True)
    menu=next(c for c in group['commands'] if c['word']==0x2100)
    assert menu['offset']==68 and menu['native_extent']==36
    labels=[]
    for japanese,gloss,note in CHOICES:
        value=japanese.encode('cp932');start=raw.index(value,menu['offset']);end=start+len(value)
        assert end<menu['offset']+menu['native_extent'] and raw[end]==0 and raw.count(value)==1
        labels.append(dict(source_Japanese=japanese,source_hex=value.hex(),source_reference=dict(file_path=group['file_path'],block=52,command_offset=68,offset=start,bytes=len(value)),first_clean_source_gloss=gloss,source_context_note=note,native_choice_label_prefix_stride_count_andselection_results_not_yet_approved=True))
    event=group['source_event_records'];assert len(event)==1 and event[0]['event_ID']==52 and event[0]['action_index']==53 and event[0]['must_be_completed']==[30] and event[0]['must_not_be_completed']==[74]
    ends=[c for c in group['commands'] if c['word']==0]
    assert [(c['offset'],c['whole_command_hex']) for c in ends]==[(166,'00000000'),(224,'00000080')]
    opaque=next(c for c in group['commands'] if c['offset']==164);assert opaque['word']==0xC283 and opaque['whole_command_hex']=='83c2'
    context="A colloquial warning asks whether the addressee means to antagonize the explicitly named ハイレディン一家. The two source choices deny that intention or volunteer to oppose the group. Subsequent speech offers a quick withdrawal before discovery, or comments on dangerous boldness. These are linguistic relationships, not yet native selected-path observations. All three source speech selectors are71 with the complete six-byte preambles preserved. Event52 explicitly requires30 and excludes74; original outer conditions, scheduling, location and natural activation remain unexecuted. Numeric adjacency alone does not prove continuity with B51."
    ROOT.mkdir(parents=True)
    save(ROOT/'three_first_clean_glosses_two_choice_labels_anddistinct_terminal_risks.json',dict(source=str(SOURCE),source_sha256=sha(SOURCE.read_bytes()),source_ROM=packet['source_ROM'],source_ROM_sha256=packet['source_ROM_sha256'],groups=[group],whole_exchange_context=context,source_typed_choice=dict(command=menu,labels=labels,complete_native_choice_layout_andselection_control_flow_not_yet_verified=True),source_unresolved_controls=dict(opaque_at164=opaque,distinct_end_commands=ends,final_high_bit_end_not_assumed_normal_zero_return=True,source_2100_count_metadata_andboth_0200_0300_relative_outcomes_unexecuted=True),all3_clean_utterances_andtwo_choices_glossed_before_current_English=True,current_English_dialogue_bodies_andchoice_labels_still_unconsulted=True,approved_named_group_spelling_androle_consumer_binding_pending=True,no_kinship_rank_orconfirmed_hostility_invented=True,no_prose_orformatting_approval_no_ROM_orcounter_credit=True,B51_registered_build_patch_startup_andcredit_remain_separate=True,new_credit=0,new_emulator_runs=0,full_goal_complete=False,producer_sha256=sha(Path(__file__).read_bytes())))
    print('B52 clean-first: three speeches/two choices glossed; intention/withdrawal/recklessness and named-group qualification preserved. Distinct end words and opaque164 require native review. Current English unread; zero credit.')
