"""Compare nine whole exchanges, retaining good English and recording concrete defects."""
import inspect
from pathlib import Path
from scripts import save_hodram_B171_B190_comparisons as previous
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.audit_story_glyph_consistency import load, save
from scripts.gloss_rafael_B51_B59_clean import ROOT

CURRENT=Path('work/analysis/Rafael_B51_B60_current_20261104/current_effective.json')
DRAFTS=ROOT/'B51_B60_all245_sealed_drafts_v1.json'
OBJECTS=ROOT/'speech_comparison_scope_v1.json'
DECISIONS={
51: '''
R|Restore the quiet/restful setting andthe sense that Rafael has not done this in a while;at last changes the unfinished thought.
K|(Hm?) is a natural brief internal reaction.
K|(Smiles) naturally presents the source gesture without inventing speech.
K|The puzzled question andprivate Who is she? preserve the understated encounter.
K|Retain the silent interval;normalize punctuation only andlet the native FE formatter determine rows.
K|Calling Sera by name already works without adding a relationship.
K|The repeated internal Hm? naturally reacts to the arriving voice.
K|Oh,Hodram naturally conveys recognition.
R|Restore the interrupted question about acquaintance andself-correction;the compressed current line sounds like a narrator summary.
K|Retain Rafael’s silence,with punctuation-only normalization.
K|Hmm naturally preserves Hodram’s thoughtful noncommittal response.
K|Sera’s questioning Hodram? already conveys her reaction.
R|Let's go preserves Hodram leaving with Sera;Go alone can sound like sending her away.
K|Yes is a natural agreement.
R|Restore wondering which country's princess she might be;the source leaves that status speculative.
R|Keep Rafael’s tentative recollection of the military man andthe Swedish navy,without making prior service a settled fact.
''',
52: '''
R|Replace the flat statement-question with a natural check of FO affiliation;keep the substitution.
R|Replace the isolated question-mark lead with Rafael’s natural puzzled confirmation.
K|Thought so is a natural local’s recognition response.
R|Restore the Portuguese military affiliation andthe relayed if-I-see-you message,with Lisbon as the return destination.
R|Use the source’s regular military rather than narrowing it to navy;make Rafael’s puzzled question natural.
R|Replace the clipped No choice with the rough companion’s conversational suggestion andfor-now qualification.
R|Preserve the formal companion’s tentative return suggestion rather than make it a flat order.
''',
53: '''
R|Restore the conversational reminder andmilitary summons;What now sounds like a new crisis rather than asking Rafael’s decision.
K|Let's go.To the palace,right? is natural decision-making anddestination confirmation.
K|Yes clearly answers the palace question.
''',
54: '''
K|Hey,you! Heard the news? naturally opens the local’s excited report.
K|What? naturally asks the local to explain.
K|The current reported Silveira/Espinosa victory is clear;Silveira’s admiral rank is established by adjacent source dialogue.
R|Remove official,which invents a formally sanctioned account;Rafael is reacting to a local rumor.
R|Replace must be better with the source’s qualified personal judgment,andpreserve the local’s puzzlement at Rafael.
K|Well...maybe so naturally expresses Rafael’s hesitant concession.
R|Restore moving the governor’s office,not a claim that the governor has already moved personally.
R|Restore the African governor’s office,Sofala andRafael’s urgent need to go;the older-local address adds no kinship.
K|The call after Rafael andconfused final question close the exchange naturally.
''',
55: '''
K|Ah,FI! Well done is natural patronizing praise andpreserves the name substitution.
R|Use the source’s Admiral Fernan address andnatural private surprise that he isalready here.
R|Remove invented Lord andrestore Silveira’s expansive praise,his claimed report andthe reassurance.
R|Right sounds confident;restore Rafael’s uncertain acknowledgment.
R|Restore Silveira as the speaker who supposedly refused,andHis Excellency’s insistence rather than passive offer wording.
K|The current appointment boast andlaugh preserve the smug self-satisfaction.
K|What?! naturally conveys shock.
K|The system notice clearly preserves all Sofala market shares being taken by the Silveira Company.
K|The luck/no-hard-feelings laugh naturally preserves Silveira’s shameless dismissal.
R|Restore the full reward joke:Albuquerque’s reward,the unnecessary appointment gift,andits prior deduction.Remove invented Lord.
R|Make the offer of a separate additional gift natural;the current isolated more obscures the joke’s referent.
K|Received3,000gold coins... naturally preserves the amount andrueful notice.
K|Damn!He got us! naturally conveys Rafael’s frustrated realization that he has been outmaneuvered.
R|Retain the source’s Commander Albuquerque address while asking whether this really was his decision.
R|Keep Claudio’s accusation as probable conjecture;the current line asserts begging andlying as established facts.
K|The existing cunning/Admiral FI/cannot-let-this-go wording is natural;retain it andcorrect only the full-width I.
R|Target is clear is telegraphic;restore the companion’s excited announcement that their next target is settled.
K|Our next target is clear is a natural measured counterpart to the rougher companion’s reaction.
R|Translate the remaining Japanese え？ as Rafael’s natural Huh? reaction.
R|Replace made me serious with an idiomatic fired-up challenge.
K|We can't stay silent naturally rejects letting the insult pass.
K|God may forgive him.Not me!Yahoo! preserves the boisterous theological joke andcheer.
K|Let's do it! is a natural rallying response.
K|The hesitant agreement,fellow-Portuguese misgiving andstronger aversion to backing down are natural andfaithful.
R|Restore Cristina’s personal refusal to forgive;No mercy shifts it into a threat about battle conduct.
K|Retain Julio’s natural old-bones joke andFI encouragement;correct the two full-width I letters only.
K|The current smirk idiom naturally conveys putting Silveira in his place andmaintains the crew’s excitement.
R|Replace Africa is ours,which declares a completed victory,with Rafael’s resolution to conquer it.
R|Let's go is the natural group rally;Go alone sounds like a command to someone else.
K|Aye naturally answers the crew’s rally.
''',
56: '''
K|The FO leader question naturally recognizes Rafael andpreserves the company substitution.
K|Perfect timing andthe call for attention naturally convey the local’s excitement.
K|Do you mean me?What is it? naturally preserves Rafael’s tentative response.
K|The current comparison with life under Espinosa andSilveira is clear andconversational.
K|We owe it to your company naturally credits Rafael’s people.
K|Really?You're making me blush naturally preserves his embarrassment at praise.
K|The current crooked-merchants/trust sentence is idiomatic andpreserves the long duration andsocial effect.
K|The reminder about why they called him over naturally returns to their purpose.
K|Oh is a natural tentative acknowledgment.
R|Stay sharp can imply danger;use pay attention as the mild admonition before handing over the object.
R|Replace unnatural What's it? with a natural object question.
R|Restore the unfinished,surprised Proof of Conquest connection rather than the compressed unexplained Conquest clue.
K|The hesitant where-question naturally preserves Rafael’s surprise andrequest for the object’s origin.
R|Restore the high asking price,which motivates the following explanation of pooled town funds.
K|The current profit/devil/Proof-location condemnation is complete andnatural.
K|Can this really be mine? naturally asks whether Rafael may accept it.
R|Fix the incomplete just to give you while retaining pooled town money andthe pressured sale.
K|Thank you so much! naturally conveys earnest gratitude.
K|Now it's yours.Do your best for everyone naturally hands over responsibility along with the gift.
K|Yes! is a natural enthusiastic acceptance.
R|Restore We're counting on you;Good luck omits the townspeople’s expressed expectation.
''',
57: '''
K|The scream already conveys Emilio’s alarm andpain.
K|The alarmed name andAre you all right question naturally respond to the accident.
K|The rotten-pier observation is natural Claudio speech andpreserves his immediate inference.
K|The drawn-out pain cry is appropriate to Emilio’s voice.
K|Let me see is a natural request to inspect the injury.
K|The repeated weak pain cry naturally follows the examination request.
R|The source advises against moving the injured part much,not against moving Emilio at all;retain resting at the inn.
K|The reluctant help,hold-on instruction andweight complaint are natural andcomplete.
R|Restore relief that the injury isnot serious andmake the sighting of Arcadius conversational.
R|Why buy flowers sounds like asking an abstract purpose;Claudio is surprised to see Arcadius buying them now.
K|And fruit naturally adds Rafael’s observation to Claudio’s previous line.
K|What's up?Someone's birthday? is natural casual speculation.
K|The existing greeting andparty question naturally carry Claudio’s mistaken assumption.
K|Eh? is a natural puzzled response.
R|Replace the abrupt tasty-food report andHurry andshare with Claudio’s natural eager recollection andrequest.
R|Restore that Arcadius is going to visit Emilio;gift alone omits the action driving the next question.
K|Emilio?Why? naturally voices Rafael’s puzzlement.
R|Make Arcadius’s mild exasperation conversational rather than a literal What are you saying?
R|Restore being unable to go out despite finally being in town;stuck in town reverses what is confining Emilio.
K|Huh is a natural noncommittal response from Claudio.
K|The sweets/uncertain flowers/at-sea explanation is natural andpreserves Arcadius’s thoughtfulness.
K|The existing hesitant request for a visit preserves Claudio’s vulnerability without inventing romance.
R|We're friends,aren't we? conveys the warmth of 仲間 in this reassurance more naturally than the detached We're companions.
K|R-right...of course naturally preserves Claudio’s awkward acceptance.
K|The denial andGo see him naturally deflect his embarrassment without explaining it.
K|The invitation to Claudio andpossible tasty fruit naturally echo his earlier appetite joke.
K|The refusal andgift-for-Emilio request naturally show Claudio’s generosity without a new motive.
R|Retain Arcadius’s slight hesitation in accepting the refusal;the clipped Bye loses that emotional beat.
K|The leg-pain question andgift offer already work as gentle bedside speech.
R|Restore Emilio’s delight at the food before the surprise that flowers are his favorite;both parts shape the joke.
R|Replace detached No,that was new to me with a natural admission andwarm encouragement to eat.
K|Hooray! naturally conveys Emilio’s delight.
K|The interrupted Clau address andwaiting question preserve Arcadius’s surprise naturally.
K|The hesitant admission andsuggestion to rejoin the others preserve Claudio’s awkwardness without invented inner thought.
R|Replace unnatural ...Let's. with a natural agreement to rejoin everyone.
K|Retain Claudio’s final silence without explaining its implication;punctuation-only normalization remains scoped.
''',
58: '''
R|Restore Admiral andmake Uddin’s identity-check question naturally courteous.
K|You are...? is a natural startled request for identification in context.
R|Replace this man with Uddin’s first-person former-leader introduction;keep the condition alternative.
R|Replace this man with Uddin’s first-person current-leader introduction;do not merge alternatives.
K|Admiral Uddin... naturally conveys Rafael’s recognition.
R|Restore explicit Indian Ocean andnatural personal praise rather than the fragment Worthy of Admiral FA.
K|The hesitant luck response naturally preserves Rafael’s modesty.
K|No need for modesty.Maybe it's fate naturally conveys Uddin’s reassuring reflection.
R|Restore the named Indian Ocean andcourteous handover;avoid a terse colon-led gift instruction.
K|The punctuation-only surprised reaction needs only consumer-specific glyph normalization.
R|Use the registered Evergreen Lotus Leaf item name andrestore the reported nature of its clue function.
K|This huge leaf...it's a map naturally preserves Rafael’s realization.
R|Use the registered Rigveda item name andrestore Uddin’s should-be qualification andIndian Ocean reference.
R|Match Rafael’s questioning echo to the registered Rigveda spelling.
K|May it prove worthy of you.Now,farewell is natural andpreserves the correct direction of worthiness.
K|The decent-old-man comment is natural Claudio speech anddoes not invent a family relationship.
K|The quiet Admiral Uddin address naturally preserves Rafael’s parting reaction.
K|The existing thanks-for-everything andgoodbye naturally close the respectful farewell.
''',
59: '''
K|Hold it,Admiral! naturally arrests Rafael’s attention.
K|You mean me? naturally checks the address.
R|Restore Pereira’s Portuguese identity andIndochina governorship;keep the local’s rough warning rather than a neutral territorial statement.
K|...And? naturally conveys Rafael’s restrained skepticism.
K|The notice-me warning naturally preserves avoiding Pereira’s adverse attention without inventing a new threat.
R|Replace formal Much obliged with Rafael’s restrained,explicit thanks for the warning.
''',
}


def normalized_current(row):
    text=previous.normalized_current(row)
    if row['id'] in ['DK4_MES_B55_R0078','DK4_MES_B55_R0168']:
        assert 'Ｉ' in text
        text=text.replace('Ｉ','I')
    return text


def save_part(label,decisions,producer):
    source=checked_text(inspect.getsource(previous.save_comparison_part),{
        'current_ROM_English_conversation_comparison_pending=False, current_reference_pending=False,':
            'current_ROM_English_conversation_comparison_pending=False, current_reference_pending=False,current_English_comparison_pending=False,earlier_English_unconsulted=False,current_English_now_exposed=True,',
        '            rows.append(row)':
            """            if row['id'] in ['DK4_MES_B55_R0078','DK4_MES_B55_R0168']:
                assert code=='K'
                row['wording_retention_with_scoped_glyph_fix']=True
                row['glyph_finding']=dict(current='Ｉ',proposed='I',count=old['current_comparison_paragraph'].count('Ｉ'),complete_native_font_andpagination_checks_pending=True)
            rows.append(row)""",
    })
    env={**previous.save_comparison_part.__globals__,'ROOT':ROOT,'CURRENT':CURRENT,'DRAFTS':DRAFTS,'OBJECTS':OBJECTS,'normalized_current':normalized_current}
    exec(compile(source,__file__+'::same-exact-comparison-current-exposure-and-scoped-I-findings','exec'),env)
    env['save_comparison_part'](label,decisions,{},producer)


if __name__=='__main__':
    assert not OBJECTS.exists()
    save(OBJECTS,dict(choice_records=[],speech_only_comparison_scope=True,
        four_B60_choice_captions_separately_pending=True,new_credit=0))
    decisions={b:[line.replace('|',' | ',1) for line in text.strip().splitlines()] for b,text in DECISIONS.items()}
    save_part('B51_B59_146',decisions,__file__)
