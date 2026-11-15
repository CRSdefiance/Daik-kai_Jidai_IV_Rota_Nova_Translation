"""Fresh clean-first meanings for the complete32-object confrontation and recruitment."""
from pathlib import Path
from scripts.verify_village_wrap_v608 import read,save
from dk4tool.patch.grand_race_menu_release import sha

ROOT=Path('work/analysis/maria_B97_clean_glosses_v4996')
SOURCE=Path('work/analysis/maria_B97_clean_inventory_v4995/all_clean_B97_speeches_before_predecessor_comparison.json')
GLOSS={
    5:('Whispering/murmuring quietly...','An impersonal FE sound cue opens the scene;do not assign these whispers to an invented named speaker.'),
    9:('A questioning reaction: ?','A brief reaction to the whispering;bind the03 selector before assigning a current native name.'),
    13:('This has become a problem. With things like that,we cannot possibly make a move.','The rough speaker voices a practical obstacle before the accusation;do not yet invent what forces or numbers are present.'),
    16:('...Are you the bandits who were attacking the town of サン＝ジョルジェ?','A direct question identifies the town and past attacks. Bind the approved current town alias;do not invent a recent battle or specific casualties.'),
    19:('W-what!? Who the hell are you?','The rough response is startled and hostile;the stammer and abrupt demand are intentional.'),
    22:('I am with {MACRO:FO}.','The source faction substitution supplies the affiliation. Preserve FO rather than guessing a company name or rank.'),
    26:('What!? You went and helped with that town\'s security! That has caused us a huge problem!','The bandits resent assistance to town security. Do not turn assistance into a formal military appointment or ownership of the town.'),
    30:('Because of you,we cannot raid it! You are taking away our livelihood!','The speaker treats raiding as a livelihood. Keep the self-interested complaint without endorsing it as narration or inventing starvation.'),
    33:('How dare mere thieves talk so arrogantly! We cannot simply abandon the townspeople in distress!','A companion rebukes the bandits and insists on helping the residents. Bind0A and its voice/name before writing character-specific diction.'),
    37:('Shut up! Those Europeans left our village a wreck!','The grievance is serious and source-explicit. Do not soften the devastation or invent burning,killings,enslavement of particular villagers or a named perpetrator.'),
    40:('Whatever anyone says,we will have our revenge!','An emphatic vow of revenge;preserve anger and determination without adding targets not specified here.'),
    43:('Wait. The ones you should resent are the unscrupulous merchants who trade in slaves here in Africa and the brutal soldiers who plunder,isn\'t that so?','The speaker names slave trading and military plunder,then argues for blame directed at those perpetrators. This is the character\'s argument;do not turn it into a broad historical absolution or omit the atrocities.'),
    46:('If you hate every European and attack indiscriminately,you are no different from those brutal people. You bear the same guilt.','An explicit moral challenge to indiscriminate attacks. Preserve its force and connection to the preceding grievance;do not expand into an invented political doctrine.'),
    49:('You talk as if you know all about it!','A hostile rejection of the speaker\'s apparent understanding. Do not misread this as agreement or a literal claim to have heard the advice before.'),
    53:('Stop seeking revenge. It is pointless. It will not restore your happiness,will it?','The challenge moves from guilt to consequences and recovery. Preserve the rhetorical question without inventing a promise of compensation.'),
    57:('Doing that will only make the fighting repeat. More of your companions will suffer.','The warning concerns a cycle of conflict and further harm to the bandits\' own people;do not invent a specific future casualty.'),
    61:('...Th-then what are we supposed to do!?','Anger gives way to an uncertain demand for an alternative. The hesitation is part of that emotional turn.'),
    64:('First of all,we must end the European nations\' struggle for power that causes so many conflicts across the world\'s seas.','The proposed alternative targets competing European powers. Preserve the worldwide maritime scope and goal,without claiming that the goal has already been achieved.'),
    68:('!?','A surprised reaction to the scale of the proposal.'),
    72:('The great powers are on the verge of dividing up the whole world. We are gathering the objects called 覇者の証 to prevent that;those powers seek them as a pretext for their aims.','Bind the approved 覇者の証 terminology before final English. Preserve impending partition,the group\'s stated preventive purpose,and the powers\' use of the objects as a pretext;do not invent the objects\' powers or ownership rules.'),
    75:('You mean to stop the great powers!? A-are you serious/sane?','A startled,incredulous challenge;it is not a claim that the group has already defeated them.'),
    78:('This is not something we could say as a bluff. Having extended our influence as far as Africa,we are confident we can deal with them on at least equal terms.','The speaker asserts confidence based on reaching Africa. Keep this as the character\'s claim;do not invent a fleet size,victory,alliance or formal rank.'),
    81:('...','A silent response allows the challenge to sink in;retain its source pause/control behavior.'),
    85:('Well? Would you try entrusting that revenge of yours to us?','An invitation to place the grievance in the group\'s hands follows the earlier rejection of indiscriminate revenge. Preserve this rhetorical pivot without promising a specific retaliatory act or removing the bandits\' agency.'),
    88:('What!?','A surprised response to the invitation.'),
    92:('Come out to sea with us. With that much spirit,you should be able to do it.','An invitation to join the maritime venture and an expression of confidence in their grit. Do not invent a position,salary,oath or family relationship.'),
    96:('...','A second silence conveys consideration rather than an invented spoken acceptance.'),
    100:('...There is nothing we can do by staying here any longer.','A resigned assessment of remaining in the current place. Do not invent a destroyed port or an order to abandon companions.'),
    103:('All right. We will take a chance on you!','The rough speaker makes a voluntary,hopeful decision to trust the offer.'),
    107:('Welcome.','A brief welcome concludes the acceptance;no rank or kinship is granted in this line.'),
    114:('I do not know whether it has anything to do with that 証 you are looking for,but something like this was hidden inside the ruins.','The later handover is tentative about a connection to the sought object. Do not identify a completed Proof or invent the artifact\'s provenance beyond its being hidden in ruins.'),
    117:('A stone tablet...?','A questioning identification of the object. Preserve uncertainty and the source item/presentation controls;do not translate the question as a confirmed complete Proof.'),
}
if __name__=='__main__':
    assert not ROOT.exists();d=read(SOURCE);assert d['read_no_predecessor_English'] and len(d['records'])==32
    assert {r['source_record_index'] for r in d['records']}==set(GLOSS)
    rows=[{**r,'fresh_source_gloss':GLOSS[r['source_record_index']][0],'whole_exchange_note':GLOSS[r['source_record_index']][1]} for r in d['records']]
    ROOT.mkdir(parents=True);save(ROOT/'all32_clean_exchange_and_fresh_glosses.json',dict(source=str(SOURCE),source_sha256=sha(SOURCE.read_bytes()),file_path='/data/SC3.DK4',block=97,
        records=rows,physical_speech_objects=32,source_commands=len(d['commands']),
        complete_exchange_progression='Whispers -> recognition of the raiders -> hostile livelihood complaint -> village devastation and revenge -> rejection of indiscriminate violence -> alternative political aim and confidence -> invitation -> consideration and voluntary trust -> welcome -> tentative ruins/tablet handover.',
        source_fact_boundaries=['Preserve the village devastation,slave trading,military plunder and the distinction between perpetrators and indiscriminate targets.','Treat judgments,confidence and political aims as character statements.','Bind03/0A/B4 native roles and voices,FO faction,approved town name and 覇者の証 terminology before final prose.','Preserve all40 commands,32 complete preambles,FE sound,pauses,presentations and the final artifact handover without guessing effects.'],
        read_no_predecessor_English=True,all_native_bindings_predecessor_comparison_localization_formatting_actual_and_release_gates_pending=True,
        new_source_prose_or_completion_credit=0,new_review_credit=0,new_emulator_runs=0,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print('Maria B97:32 clean-only fresh glosses/40 commands. Full exchange and slavery/plunder/revenge/recruitment boundaries recorded;zero credit.')
