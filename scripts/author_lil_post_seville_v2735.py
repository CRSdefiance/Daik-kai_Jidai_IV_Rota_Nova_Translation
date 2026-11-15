"""Fresh full-exchange review of B30/B31 and the earlier B132 warning."""
from copy import deepcopy
from pathlib import Path
from collections import Counter
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/lil_post_Seville_author_v2735')
SOURCE=Path('work/analysis/lil_post_Seville_source_v2732/complete34_clean_current_native_context.json')
CONTROL=Path('work/analysis/lil_post_Seville_controls_v2734c/source_bound_34_preambles_and_B132_warning_predicate.json')
BRANCH=Path('work/analysis/lil_post_Seville_branches_v2733/original_relative_skip_operand_proof.json')
DOC=Path('translations/lil_post_seville_and_egypt_warning_editorial_manuscript_v1.json')

# Glosses were written from clean Japanese and full exchanges before localization.
REVIEWS={
'DK4_MES_B30_R0006':('V',"Our fleet... the strongest in Spain... How could this happen? I can't face my sovereign...",
    'Valdes laments that their fleet,the strongest in Spain,has suffered this disaster,and says he cannot face the sovereign.',
    'Restore the collective fleet,the explicit Spanish superlative,the shocked reaction,andthe personal shame. My sovereign preserves the original Majesty reference without inventing the monarchs gender. The source ellipses are hesitant speech,not authored line breaks;do not add a sinking orcasualty claim.'),
'DK4_MES_B30_R0010':('V',"Don't tell me Clifford...",
    'Valdes incredulously begins to say that Clifford has done something;the following alternative speech supplies the alliance description.',
    'Keep the deliberately unfinished disbelief so either native alternative can complete it. No act oroutcome is invented before the branch. Clifford is named without an invented new rank;the disparaging reference is carried by his incredulous tone.'),
'DK4_MES_B30_R0020':('V',"...joined forces with that little girl...",
    'Valdes says,in disbelief,that Clifford joined forces with that little girl.',
    'Restore the actual act ofalliance,which the older With that little girl omitted. Keep the contemptuous little girl andthe incomplete continuation ofhis previous speech. This is one conditional alternative,not a reply to the Amsterdam alternative.'),
'DK4_MES_B30_R0026':('V',"...allied himself with a merchant from Amsterdam...",
    'Valdes disbelieves that Clifford allied himself with a merchant from Amsterdam.',
    'Restore the explicit alliance andorigin rather than the old bare With an Amsterdam trader. This completes his preceding disbelief onthe other original branch;it is not additional proof that two separate alliances occurred.'),
'DK4_MES_B30_R0033':('R',"Hey!",
    'Clifford greets Lil with an energetic familiar Hey!',
    'Retain the brief,natural current greeting. It carries his easy familiarity without adding an address,rank orrelationship.'),
'DK4_MES_B30_R0037':('R',"Clifford!",
    'Lil recognizes andcalls out to Clifford,using his name with san.',
    'Retain the natural name exclamation. In this established acquaintance exchange,an English honorific is unnecessary andwould add stiffness;the recognition andtone remain clear.'),
'DK4_MES_B30_R0041':('V',"Our alliance threw Valdes off and made him divide his forces. That's why he lost...",
    'Clifford explains that their alliance confused Valdes into splitting his forces,and that this caused his defeat.',
    'Restore both the disorientation andthe resulting divided strength in the causal explanation. Keep the assessment in Cliffords own voice;do not invent a tactical maneuver,casualty total orwho personally won the battle.'),
'DK4_MES_B30_R0045':('V',"We've done what we set out to do, then. What are you going to do now?",
    'Lil confirms that they have now achieved their objective and asks what Clifford intends to do next.',
    'Use an easy spoken acknowledgment anddirect personal question. The older What now? omitted that she is specifically asking his plans;the full question sets up his dependence onroyal orders andher worry.'),
'DK4_MES_B30_R0048':('V',"Well... I'll have to see what orders I get from the Crown...",
    'Clifford considers the question andsays that he will have to seek orfollow the sovereigns instructions.',
    'Keep the thoughtful pause,his first-person dependence onroyal direction,andthe unfinished qualification. The Crown is idiomatic institutional English for the source Majesty reference anddoes not invent a male king,which the old English did. No particular order orfuture war is asserted.'),
'DK4_MES_B30_R0051':('R',"Not against me...",
    'Lil uneasily starts to ask whether that could mean opposing her.',
    'Retain the natural frightened fragment andellipsis. With Cliffords royal-orders speech before it andhis hope afterward,the implication is clear. Completing it as a guaranteed future attack would overstate the source.'),
'DK4_MES_B30_R0055':('R',"Let's hope not.",
    'Clifford says he hopes it will not come to that.',
    'Retain the idiomatic response. It directly answers her fear,expresses hope rather than a promise,andpreserves uncertainty about what the Crown may order.'),
'DK4_MES_B30_R0059':('V',"Yeah...",
    'Lil quietly agrees,with a hesitant trailing pause.',
    'Use the familiar Yeah for un,consistent with her ordinary voice andthe subdued mood. The older Yes was stiffer than this uneasy personal exchange. Keep the uncertainty rather than turning it into enthusiasm.'),
'DK4_MES_B30_R0063':('R',"Take care, then.",
    'Clifford says farewell andtells Lil to do well orstay well.',
    'Retain the natural current farewell. Take care carries the familiar goodwill andgenki wish without inventing a vow ornew relationship.'),
'DK4_MES_B30_R0067':('R',"You too.",
    'Lil returns the same good wishes to Clifford.',
    'Retain the concise,idiomatic reciprocal farewell. It works with the immediately preceding Take care,then,andadds no detail.'),
'DK4_MES_B31_R0006':('V',"Hey, you planning to trade in the southern Mediterranean? You've heard the rumors around here, haven't you?",
    'A port worker asks whether the group will trade in the southern Mediterranean,and rhetorically expects that they know the local rumors.',
    'Restore his attention-getting Hey,the plural group address through English you,andthe specifically local rumors. Use a conversational tag question to carry the rough rhetorical ending without inventing a threat ornew rank.'),
'DK4_MES_B31_R0010':('V',"...Huh? Rumors?",
    'Lil reacts with surprise andasks about the rumors.',
    'Restore the audible eh reaction as Huh? while retaining the source pause andquestion. The old Rumors alone flattened her surprise. The ellipsis is spoken hesitation,not a blank leading row.'),
'DK4_MES_B31_R0027':('R',"Rumors? About what?",
    'Camille asks what rumors the port worker means.',
    'Retain the natural two-question reply. It expresses the polite Japanese question in unforced spoken English andworks as the optional Camille response before the port workers explanation.'),
'DK4_MES_B31_R0034':('V',"You haven't heard of the Pirate King of the Mediterranean?",
    'The port worker asks whether they have not heard of the Pirate King of the Mediterranean.',
    'Restore the complete regional title,which the old English reduced to Pirate King. The negative question carries his surprise naturally. The title remains a local appellation,not a newly asserted legal rank.'),
'DK4_MES_B31_R0037':('V',"Who's this Pirate King?",
    'Lil asks what this Pirate King is orwho is meant by that name.',
    'Use the natural English Who question for a person identified bya title. The old What is this Pirate King sounded as ifshe were asking about an object. Do not identify the person before the source does.'),
'DK4_MES_B31_R0048':('R',"...(Could it be that man?)",
    'Gerhard privately wonders,in disbelief,whether the speaker means a particular man.',
    'Retain the cautious current inner thought andits parenthetical presentation. The man remains unnamed andthe possibility remains uncertain. This optional thought belongs to the no-earlier-warning branch,not a spoken reply that everyone hears.'),
'DK4_MES_B31_R0055':('V',"Take my advice. Once you leave this port, head somewhere else! You hear me? Get away from Egypt!",
    'The port worker urges them to take his advice,leave this port for somewhere else,andget out ofthe area around Egypt.',
    'Restore the once-you-leave sequence andthe forceful attention check. Keep the rough protective urgency andexplicit Egypt location without inventing an ambush,death threat orspecific destination. Get away from Egypt naturally includes its vicinity.'),
'DK4_MES_B31_R0059':('V',"Is this what that 'warning' was about...?",
    'Lil wonders whether this is what the earlier warning meant.',
    'Remove the unsupported Clifford name. Native8100at132queries event132,andthe positive branch reaches this speech;complete B132is the barkeeps southern-Mediterranean warning. Keep the recalled warning anduneasy question without inventing who the Pirate King is.'),
'DK4_MES_B31_R0063':('V',"Sounds like you do know a little... Then get out of the southern Mediterranean, and fast!",
    'The port worker infers that Lil knows something,and urges her to leave the southern Mediterranean quickly.',
    'Preserve the qualified inference,a little,andthe explicit region andurgency. Sounds like fits his rough conversation better than formal exposition. This follows Lil recognition onthe earlier-warning branch;it does not prove that she already knows the Pirate Kings identity.'),
'DK4_MES_B31_R0066':('V',"Don't mess with the Pirate King!",
    'The port worker warns them not to interfere with orchallenge the Pirate King.',
    'Use the natural American warning Dont mess with for te o dasu. It preserves the strong hands-off meaning andrough voice;the old Do not challenge was accurate butstiff for this speaker. No battle orattack is promised.'),
'DK4_MES_B31_R0078':('V',"The Pirate King...? Th-that's scary, {MACRO:FI}. Let's just do as we were warned.",
    'Janus stammers fearfully about the Pirate King,addressing Lil politely,and suggests quietly following the warning.',
    'Restore a complete naturally stammered reaction andthe cautious,compliant proposal. Keep the exact original FI runtime name andomit an invented English title for san. The warning remains the known advice;do not change his frightened suggestion into a selected player action.'),
'DK4_MES_B31_R0093':('R',"...(Could it be that man?)",
    'Gerhard privately wonders,in disbelief,whether the Pirate King is a certain man.',
    'Retain the already natural,uncertain inner thought. Although the source wording matches R48,this is a separate conditional object onthe earlier-warning branch andreceives its own review. Do not name the man ormerge the two records.'),
'DK4_MES_B132_R0006':('R',"You're not headed to the southern Mediterranean to trade, are you?",
    'The barkeep asks the young woman andher companions whether they are planning to trade in the southern Mediterranean.',
    'Retain the natural rhetorical negative question. Headed there to trade conveys their intended business travel. English you covers the group;there is no need to turn the familiar ojou-chan address into a new rank orclaim that every companion is female.'),
'DK4_MES_B132_R0010':('R',"Why? What's down there?",
    'Lil asks why,andwhether there is something in the southern Mediterranean.',
    'Retain the idiomatic current questions. Down there clearly refers to the region just named bythe barkeep,andthe line asks for an explanation without assuming danger yet.'),
'DK4_MES_B132_R0021':('V',"There's good money to be made in the southern Mediterranean! We can't pass that up!",
    'Fernando says that the southern Mediterranean offers good earnings,andthat they cannot let this opportunity pass.',
    'Restore the full region andthe forceful cannot-pass-up-opportunity reasoning. The older Lets go substituted a direct travel proposal. Keep his blunt commercial enthusiasm without guaranteeing an actual profit orforcing the players next action.'),
'DK4_MES_B132_R0027':('V',"Don't do it... Don't trade in the southern Mediterranean.",
    'The barkeep tells them to abandon the idea,andnot to trade in the southern Mediterranean.',
    'Restore the initial discouragement andominous spoken pause before the explicit repeated prohibition. Keep the clear region andthe advisory imperative;do not invent a reason before he gives one.'),
'DK4_MES_B132_R0030':('V',"Wait, what do you mean?!",
    'Lil interrupts anddemands to know what he means.',
    'Restore chotto as Wait to carry her abrupt challenge,then keep the natural current question andits force. No new accusation is added.'),
'DK4_MES_B132_R0034':('V',"You hear me? I've warned you. Don't forget it.",
    'The barkeep insists that he has warned them andtells them not to forget it.',
    'Restore the attention check andthe completed warning. Ojisan is the barkeeps familiar self-reference as an older man,not proof that he is anyones uncle;English I conveys it without invented kinship. Keep the emphatic concern rather than adding a specific danger.'),
'DK4_MES_B132_R0045':('R',"What was that about? What now, {MACRO:FI}?",
    'Camille wonders what the warning means,andasks Lil what she will do.',
    'Retain the natural compact questions. What now directly invites Lil next decision in this exchange,anddoes not select an action. Preserve the one original FI runtime name exactly;do not add a title orrelationship.'),
'DK4_MES_B132_R0051':('V',"Don't go to the southern Mediterranean... What does he mean...?",
    'Lil repeats the injunction not to go to the southern Mediterranean,andwonders what the barkeep means.',
    'Restore the exact region andher puzzled question about the warnings meaning. Keep the trailing uncertainty andspoken repetition;do not turn it into a known Pirate King threat before the later port-worker exchange.')
}

if __name__=='__main__':
    assert not ROOT.exists() and not DOC.exists();source,control,branch=map(read,[SOURCE,CONTROL,BRANCH])
    assert len(source['records'])==34 and set(REVIEWS)=={r['id'] for r in source['records']}
    assert control['warning_reference_is_B132_Barkeep_not_Clifford'] and len(control['current_original_predicate_cases'])==8
    assert len(branch['cases'])==320 and len(branch['operands_requiring_adjustment_when_resizing'])==32
    records=[]
    for original in source['records']:
        row=deepcopy(original);decision,english,gloss,note=REVIEWS[row['id']]
        prefix=row['source_presentation_prefix_hex'].upper();row.update(english='{SPEAKER:'+prefix+'}'+english,
            source_meaning=gloss,localization_note=note,editorial_decision='revise' if decision=='V' else 'retain-wording',
            context=source['scope']+' This record is reviewed as part ofits complete native exchange andconditional path;the recorded storage neighbors do not imply consecutive reachability.',
            review=dict(source=True,context=True,localization=True,naturalness=True,formatting=False),
            status='source-context-prose-approved;native-formatting-reference-representative-release-pending')
        if decision=='R':
            assert english==' '.join(row['current_English'].split()).replace('FI','{MACRO:FI}').replace('FA','{MACRO:FA}').replace('FO','{MACRO:FO}'),row['id']
            row['fresh_retained_wording_justification']=note
        assert '{LB' not in row['english'] and '{PAD}' not in row['english'] and not english.startswith(' ')
        for macro in ['FI','FA','FO']:assert bytes.fromhex(row['source_hex'])[1:].count(macro.encode())==english.count('{MACRO:'+macro+'}')
        records.append(row)
    assert Counter(r['editorial_decision'] for r in records)=={'revise':22,'retain-wording':12}
    ROOT.mkdir(parents=True)
    doc=dict(format='dk4-ilnk-editorial-source-prose-draft-v1',translation_policy='natural-dialogue-v2',target_locale='en-US',
        file_path='/data/SC2.DK4',review_gates=['source','context','localization','naturalness','formatting'],
        source_ROM_sha256=source['source_ROM_sha256'],current_ROM=source['current_ROM'],current_ROM_sha256=source['current_ROM_sha256'],
        required_runtime_ARM9_sha256=source['current_ARM9_sha256'],source_context=str(SOURCE),source_context_sha256=sha(SOURCE.read_bytes()),
        control_contract=str(CONTROL),control_contract_sha256=sha(CONTROL.read_bytes()),branch_proof=str(BRANCH),branch_proof_sha256=sha(BRANCH.read_bytes()),
        records=records,revised=22,retained=12,formatting_review_pending=True,source_prose_credit_added=0,completion_credit_added=0,
        no_authored_line_breaks_or_padding=True,actual_B30_B31_B132_IDs=[],new_emulator_runs=0,full_goal_complete=False)
    save(DOC,doc)
    save(ROOT/'source_prose_review_receipt.json',dict(manuscript=str(DOC),manuscript_sha256=sha(DOC.read_bytes()),revised=22,retained=12,
        all34_clean_Japanese_and_complete_exchanges_reviewed=True,warning_attribution_correction_source_bound=True,
        formatting_reference_representative_and_release_pending=True,actual_B30_B31_B132_IDs=[],source_prose_credit_added=0,completion_credit_added=0,
        producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print('34fresh source/prose reviews authored:22revisions/12justified retentions;B132warning context correct. Full native formatting/reference/release pending;no credit yet.')
