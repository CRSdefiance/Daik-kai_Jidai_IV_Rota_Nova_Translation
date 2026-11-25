"""Record complete-exchange comparisons with individual source findings and retentions."""
from collections import Counter
from copy import deepcopy
from pathlib import Path
from scripts.audit_story_glyph_consistency import load,save
from scripts.draft_hodram_B281_B300_clean_v2 import OUT as DRAFTS
from scripts.gloss_hodram_B281_B300_clean_v1 import ROOT,OUT as MEANINGS
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.review_hodram_B231_B250_contextual_v1 import mark_macros

CURRENT=ROOT/'current_v1/current_effective.json';OBJECTS=ROOT/'current_objects_v1/current_objects.json'
OUT=Path('translations/hodram_B281_B300_contextual_review_v1.json')

RETAIN={
282:{6:'The respectful guard’s complete summons is natural and preserves the surname address and king’s request.'},
283:{9:'The king’s emphatic praise clearly celebrates defeat of the formidable foe.',12:'The clipped royal command naturally calls for the reward in the ceremony.',28:'The king’s formal mission question is natural and leaves the status unspecified.',35:'The reflective royal question preserves the unresolved essential point in a suitably formal voice.',42:'The puzzled clarification naturally addresses the king as sire without inventing a knightly rank.',45:'The formal recognition argument is fluent and preserves the difference between self-proclamation and universal acknowledgment.',48:'The short echo refers directly to universal recognition in the preceding turn.',56:'The tentative named-Proof question naturally identifies the king’s indirect reference.',60:'The king’s brief acknowledgment of prior knowledge needs no expansion.',80:'The emphatic assent naturally accepts the king’s charge.',97:'The dry observation naturally preserves the counterargument about people chasing empty fantasies.',111:'The formal conclusion preserves the conditional argument just established about demonstrating fleet supremacy.',115:'Gerhard’s complete conclusion identifies collecting the Proofs as the mission.',119:'The concise confirmation naturally closes Gerhard’s reasoning.'},
284:{6:'The complete retainer’s summons keeps the urgent Stockholm return.',13:'Gerhard’s polite speculative question preserves uncertainty about the summons.'},
286:{9:'The natural job/target question responds to the guildmaster without inventing the opponent’s identity.',19:'The complete introduction names William and conveys his vicious character.',27:'The idiomatic comparison is explicitly relative and does not endorse Maldonado outright.',39:'The direct appeal naturally makes Hodram the guild’s last available hope.',43:'The restrained judgment and acceptance fit Hodram’s dry voice.',46:'The excited question naturally confirms acceptance.',65:'Gerhard’s complete practical question follows acceptance of the hidden-target job.',71:'The short clarification naturally prompts Hodram to explain the plan.'},
287:{5:'The inarticulate screech and angry roar fit William’s captured outburst without adding speech or species.',61:'The reserved greeting is natural for the introduced villager.',73:'The brief ruins echo naturally asks for clarification.',84:'The natural skeptical question challenges the villager’s lavish strongest-warrior praise.',92:'The complete statement preserves the explicitly combined strength, righteousness and wisdom.',100:'The natural faint-hope wording conveys the source’s cloud-grasping uncertainty without forcing a literal metaphor.',104:'The candid admission naturally deflates the earlier praise by explaining their broad solicitation.',108:'The formal apology and lack of miraculous expectations preserve the deliberately deflating joke.',115:'The fluent advance offer explicitly preserves nonrepayment if the search fails.'},
289:{23:'The concise appearance question remains distinct from the later capture reminder.',28:'The complete capture question preserves the separate post-appearance objective.'},
290:{62:'The curt movement order is natural for Hodram leading the tense expedition.',96:'The urgent warning is idiomatic and adds no identity to the dynamic role.',118:'The direct firing command preserves the armed response.',214:'The name question correctly sets up Emilio’s actual-sleep reveal.',218:'The conventional sleep sound preserves the joke without extra dialogue.',233:'The complete time notice preserves exactly one elapsed day.',313:'The emphatic escape order is already natural.'},
291:{37:'The complete eerie-jungle observation is natural and preserves the hesitant trailing pause.',66:'The restrained thinking sound fits Hodram’s uncertainty.',70:'The concise warning naturally identifies slick moss as the footing hazard and keeps FI without Lord.',73:'The short acknowledgment needs no elaboration.',77:'The low growl preserves the animal sound without naming a species.',100:'The sudden beast warning naturally conveys the source’s alarm in the established animal encounter.',115:'The direct firing command preserves the chosen armed response.',119:'The sharp growl preserves a distinct emphatic animal cry.',127:'The clipped curse and speed complaint are natural under attack.',152:'The complete gunfire/injury judgment and close-combat order preserve the tactical change.',221:'The brief light discovery naturally signals a possible way out, without inventing a lamp.',225:'The complete escape observation correctly identifies leaving the cave.'},
292:{8:'The complete skeptical monster report naturally keeps the recurring nearby-water appearances.',12:'The terse skeptical echo is a natural response to the monster claim.',19:'The complete statement preserves several ships and the current-year period.',22:'The conversational job request naturally asks Hodram to stop/hunt the monster.',25:'The complete dry response correctly makes encountering it luck-dependent.',28:'The patient response and good wishes naturally accept that the encounter may take time.'},
293:{9:'The hope/prayer idiom preserves the unsettling possibility of additional monsters without specifying a deity.',12:'The short suspicious question gives the preceding qualification its comic payoff.',16:'The brisk dismissal and reward offer naturally dodge Hodram’s question.',60:'The casual recollection is natural guild speech and explicitly introduces a rumor.',67:'The terse formal question fits Hodram asking whether the rumor is true.',71:'The complete clarification preserves that no one found the ruins and the lead remains only rumor.'},
294:{47:'Gerhard’s complete inference naturally explains the ruins’ concealment by the forest.',78:'The concise question naturally proposes a precautionary search.',93:'The formal acknowledgment preserves the caution rationale.',103:'The clipped roll-call question is natural during an escape.',111:'The pause and sudden name call naturally shift from group safety to concern for the admiral.',115:'The stammered reassurance and question preserve Hodram’s weak deflection.',135:'The complete system notice preserves apparent sailor confusion.',155:'Charles’s regret and speculation preserve his morbid curiosity about the skeletons without adding a new objective.',167:'The short realization naturally marks reaching the destination.'},
295:{6:'The warm greeting is natural and keeps the source’s welcoming tone.',14:'The complete question preserves the hidden Christian village and nearby location.',17:'The concise negative answer naturally fits Hodram’s direct voice.',21:'The complete description preserves rock-hewn houses and explicitly qualifies the story as rumor.'},
296:{5:'The unfinished observation naturally hands the blockage explanation to Gerhard.',9:'The complete rockfall speculation and impassable-path statement preserve uncertainty and the obstacle.',12:'The restrained retreat decision is natural for Hodram.',40:'The enthusiastic blasting proposal is idiomatic and preserves Charles’s impulsive solution.',54:'The complete supply objection preserves the nearly impossible single procurement.',60:'The natural pronoun question refers clearly to making gunpowder in the preceding turn.',67:'The complete uncertain availability statement preserves sulfur and this town.',73:'The concise affirmative plan naturally commits to buying sulfur.'},
297:{33:'The first-person plural reminder naturally restates the sulfur objective.',213:'The emphatic insufficiency reply is natural and adds no threshold.',232:'The concise delivery reply keeps the need for more without inventing quantity.',243:'The complete affirmative response correctly marks sufficient supply.',247:'The natural next-step question links the delivery to the next material.',251:'The conversational material-list phrase explicitly preserves timber for charcoal.',254:'The short material echo naturally requests confirmation.',258:'The complete availability statement preserves that timber must be obtained elsewhere.'},
298:{33:'The natural reminder preserves the timber objective.',128:'The emphatic delivery reply preserves major insufficiency without a number.',147:'The concise need-more reply preserves the remaining shortage.',158:'The complete affirmative response correctly marks sufficient timber.',165:'The short exasperated question naturally punctures Charles’s continuing list.',172:'The ingredient echo preserves saltpeter exactly.',179:'The dry distance complaint is natural after the Indian Ocean lead.'},
299:{33:'The natural reminder preserves the saltpeter objective.',229:'The emphatic reply preserves major insufficiency without inventing thresholds.',247:'The concise need-more reply preserves the remaining shortage.',258:'The two-sentence affirmative reply naturally confirms sufficient supply.',265:'The excited completion announcement is natural in the manufacturing exchange.'},
300:{43:'The complete speculative warning preserves uncertainty and the need for care.',46:'The urgent name-and-look warning is natural without forced stammering.',50:'The startled giant-snake identification is natural and supplies no unspoken species.',54:'The complete tactical question and difficulty assessment fit Gerhard’s formal voice.',72:'The coordinated attack order is natural nautical crew speech and preserves attacking together.',75:'The familiar acknowledgment fits the retainer’s colloquial source response.',94:'The exhausted victory statement naturally confirms defeating the creature.',98:'The breathless assent needs no elaboration.',110:'The complete difficulty observation and gunpowder remark preserve Charles’s practical comment.',124:'The complete tactical judgment is natural and preserves avoiding battle here.',128:'The complete withdrawal/cohesion orders naturally keep the group from being left behind.',132:'The familiar nautical assent preserves the retainer’s acknowledgment.',137:'The clipped roll-call question is natural after withdrawal.',141:'The conventional roll-call answer preserves everyone being present.',148:'The sudden emphatic grunt fits Hodram’s alarm without inventing a spoken question.',152:'The complete anxious question preserves the given-name substitution and Gerhard’s concern.',159:'The shocked question naturally responds to the bog trap.',170:'The short reassurance naturally promises immediate help.',178:'The familiar assent naturally answers the request for assistance.',186:'The complete acknowledgment of Gerhard’s rescue preserves the captain’s gratitude.',194:'The reassurance and strained cry naturally preserve the alternative solo rescue.',201:'The natural thanks and surprise convey the source’s apologetic gratitude and unexpected swamp.',208:'The complete system notice preserves apparent sailor fatigue.'},
}

SPECIAL={
(281,12):'Restore the captain’s remembered Mediterranean pirate task rather than a bare external command.',
(281,24):'The target is Hernan himself; do not invent a gang as the requested target. Preserve the guildmaster’s anger.',
(282,9):'Restore the admiral address and direct personal request; a request does not literally await him.',
(282,12):'Restore operating beyond the Indian Ocean, not the broader and incorrect southern seas.',
(282,16):'Keep the maritime Arab-region threat, heavy merchant losses and personal request in a speakable royal turn.',
(282,19):'Restore the Arab identification and complete Iscal Yasar name, with the king’s last-hope appeal.',
(283,6):'Use welcome back rather than asserting that the court is the admiral’s home.',
(283,16):'The king asks him to accept the physical reward, not merely an abstract expression of thanks.',
(283,31):'Keep a respectful royal acknowledgment without inventing a status report.',
(283,39):'Preserve the prospective fleet goal rather than presupposing it is already the strongest.',
(283,52):'Restore the indirect symbol-of-supremacy question so Hodram’s next turn identifies the Proofs naturally.',
(283,64):'The Proofs are scattered around the world; do not narrow their locations to the seas when they may lie inland.',
(283,68):'Keep eligibility to rule a sea region without the awkward implication that a neuter owner rules its own sea.',
(283,72):'Restore demonstrating strength at home as well as abroad.',
(283,76):'Use a natural royal charge to raise Sweden to the great-power ranks.',
(283,85):'The treasures are ill-understood; the hunt itself is not an unknown event. Preserve Hodram’s dry response to the royal command.',
(283,89):'Make Gerhard’s courteous doubt a spoken question about significance rather than abstract carrying of meaning.',
(283,93):'Restore Hodram’s uncertainty and qualified judgment; do not turn unlikely worthlessness into certainty.',
(283,104):'Restore regional rivals and the shared quest without requiring the destruction of every mighty rival everywhere.',
(283,107):'Express comprehensive, sophisticated fleet strength beyond local battles in natural speech.',
(284,9):'The king is absent; Hodram reacts to news about His Majesty rather than addressing him directly as Sire.',
(285,6):'Restore the Indian Ocean and the given-name Iscal reminder, not a southern-seas Yasar task.',
(286,12):'Make the group’s prior tribute relationship explicit rather than merely saying some thugs paid Maldonado.',
(286,16):'Restore Escante in Mexico and Clifford in England while preserving the opportunistic breakaway.',
(286,23):'Retain both merchant and immigrant ships and every captive/village; do not narrow group atrocities to William acting alone.',
(286,31):'The band is not an openly established faction; that does not mean it lacks an organization.',
(286,35):'No source death toll is stated. Replace barely returned alive with the source’s broader failure to return in good condition.',
(286,50):'Replace the telegraphic Must act with Hodram’s personal refusal to leave the situation unchecked.',
(286,54):'Restore the guildmaster’s confidence in the reassuring acceptance, not only a generic do-your-best wish.',
(286,68):'Restore the no-lead/force-his-hand setup so Gerhard’s question and later brute-force reply form an exchange.',
(286,75):'Defeat subordinate pirates to provoke William’s impatience; do not imply killing every individual pirate.',
(286,79):'Restore Gerhard’s dry brute-force label rather than the isolated adjective Blunt.',
(287,9):'Restore recognition by the captive’s distinctive voice, preserving the outburst’s payoff.',
(287,12):'Hodram is relieved to be rid of handling the captive, not newly released from an invented imprisonment.',
(287,16):'Make the generous guild reward sound like an impressed, conversational guildmaster.',
(287,57):'The guildmaster wants to introduce someone; do not shift the stated initiative to the visitor.',
(287,69):'Turn the abstract skill-inspires-a-request construction into a courteous personal appeal for particular ruins.',
(287,77):'Restore the traditional/reported status of the ancestral warrior memorial.',
(287,80):'Preserve qualification as the strongest warrior, not a narrator’s claim that only one literal greatest person can succeed.',
(287,88):'Keep the villager’s own conviction and the specific recent pirate defeat; do not invent unanimous community confidence.',
(287,96):'Make Hodram personally hesitant to accept the overpraised request rather than stating an impersonal rule that the task cannot be accepted.',
(287,112):'Make Hodram’s candid appreciation and relief a natural personal observation.',
(287,125):'The villager personally offers to accompany the search after the named map is obtained; do not invent additional companions.',
(287,128):'Keep the singular speaker waiting at the city gate, linked to his own offer to accompany the expedition.',
(288,6):'Use the port worker’s casual surname address and Havana referral without stiff seeking language.',
(289,12):'Keep the remembered New World pirate task in the captain’s voice.',
(290,148):'Preserve apparent minor sailor injuries rather than an unqualified injury fact.',
(290,175):'Keep the quiet play-dead instruction and patience, rather than a possibly physical hold-on command.',
(290,222):'Emilio is actually asleep now; do not turn the joke into a report that he slept in the past.',
(290,278):'The bear may eat people and careless intervention is risky; do not make every possible attack categorically unsafe.',
(290,305):'Preserve considerable fatigue and apparent injuries without adding a precise amount or certainty.',
(291,41):'Make Gerhard’s uneasy hope natural rather than a stiff optative formula.',
(291,45):'Restore the indefinite cave observation and pause instead of a bare UI-like noun.',
(291,49):'The cave looks deep and there is no other way forward; restore both inference and necessity.',
(291,60):'Charles believes this must be a shortcut; do not turn his confidence into an objective guarantee.',
(291,123):'Preserve the retainer’s pained/alarmed cry rather than a mild surprise interjection.',
(291,186):'Keep apparent substantial injuries without assuming every expedition member is male.',
(291,211):'Use an idiomatic relieved escape reaction rather than the unnatural Whew, saved.',
(292,5):'Make the guildmaster’s timely favor request a direct conversational opening.',
(292,16):'Restore fishermen calling it a monster fish and its ship-biting behavior; the source does not identify a demon.',
(293,5):'Preserve defeat and excited admiration without asserting an unspoken killing.',
(293,63):'Restore the entire ancient kingdom’s intact ruins, distance from this town and reported status, not merely royal ruins as a fact.',
(294,43):'Use a natural dense-forest observation that supports Gerhard’s explanation of concealment.',
(294,58):'Preserve Charles’s personal wish to get through the forest quickly, not an apparent order to abandon the expedition.',
(294,64):'Keep the explicit Byzantine Empire and regional Christian/Islamic context as Gerhard’s question, not a historical assertion.',
(294,67):'Refer to a time centuries ago without inventing a tale or established legend.',
(294,71):'Hodram reacts to the bones in front of him; What bones asks for a different clarification.',
(294,75):'Preserve Gerhard’s inference about a previous explorer instead of presenting the death’s circumstances as known.',
(294,96):'Restore the concrete throat trouble as well as difficulty breathing, without adding a diagnosis.',
(294,99):'Warn about this smoke and breathing it before the later explanation; do not insert a premature poison identification.',
(294,107):'Keep the report that everyone is safe, setting up the subsequent discovery that the admiral is not well.',
(294,118):'Restore harmful smoke, prior hearsay and surprise at finding it here in a natural explanation.',
(294,122):'Use Hodram’s weak acknowledgment rather than the incomplete and unclear So... that.',
(294,126):'Make the urgent danger report and order to hurry through speakable English.',
(294,143):'Preserve the lesson about not lingering in suspicious places, then pressing on.',
(295,10):'Keep closer inspection and a useful tip without asserting physical proximity or confidential knowledge.',
(296,37):'Restore Gerhard asking Charles what is wrong and saying they are heading back.',
(296,44):'React naturally to the proposed act of blasting rather than asking about an unexplained noun blast.',
(296,47):'Use natural English for the rocks blocking the path.',
(296,50):'Restore Hodram’s disbelief and the hypothetical large powder requirement in natural speech.',
(296,57):'Use a natural reassurance instead of No concern.',
(296,63):'Restore Charles’s personal research, the large sulfur requirement and his offer to manufacture the powder.',
(296,70):'The named destination is the trade house, not a generic market.',
(297,11):'This is an absence branch: Hodram wishes Charles were present, not asserts that Charles must already be here.',
(298,11):'Preserve the Charles-absence wish consistently with the linked sulfur and saltpeter branches.',
(298,161):'Use a natural final-list introduction that sets up Hodram’s exasperated question.',
(298,169):'State that the essential ingredient is still missing, not ambiguously that it remains intact.',
(298,176):'Restore some town on the Indian Ocean, not an unspecified southern-seas city.',
(299,11):'Preserve the Charles-absence wish, not a statement that he is already here.',
(299,269):'Charles will set the explosive himself; the others must take shelter in town. Restore actor and destination.',
(299,278):'Preserve the exact three-two-one-zero countdown; go must not replace zero.',
(300,40):'Preserve the report that locals apparently avoid this area rather than asserting a confirmed fact.',
(300,68):'This is Hodram’s spoken decision to fight, not a bare menu-like Attack caption.',
(300,119):'Preserve apparent sailor injuries rather than an unqualified result.',
(300,155):'Make the captain’s apparent immobilization in a bog explicit and personal; do not add quicksand.',
(300,174):'Use a natural strained admission that Gerhard cannot do it alone and asks everyone for help.',
(300,182):'Gerhard checks the rescued captain’s welfare; a natural are-you-all-right question fits better than location-like safety wording.',
(300,197):'Render the breath sound as vocalized panting and ask about the rescued captain’s welfare, not the word Pant.',
}

STYLE_RETAIN={
(290,24):{4:'The rough shorthand no-map-means-getting-lost warning is natural and complete in context.',6:'The emphatic complete map warning fits the simple frightened voice without forced baby talk.'},
(290,328):{0:'The measured forest observation and caution are natural in an expedition report.',3:'The casual hope not to get lost preserves the source’s specific concern.',4:'The concise uneasy woods observation is idiomatic and fits the rough voice.',5:'The caution and alertness instruction naturally preserve the older speaker’s practical advice.',7:'The formal optative forest concern preserves hope of avoiding an encounter without naming a pursuer.'},
(290,670):{0:'The hesitant behind-you warning naturally conveys alarm; the addressee is clear.',1:'The complete urgent instruction not to move and rearward warning match the source.',2:'The broken rearward warning naturally conveys panic.',3:'The cry and stammered warning preserve the expressive register.',5:'The short emphatic rearward warning fits the older voice.',6:'The startled cry and warning naturally preserve the simple alarm.'},
(290,970):{2:'The informal complete bear-ran-off announcement preserves escape.',5:'The older speaker’s concise bear-fled exclamation is natural.',6:'The celebratory yes/gone reaction naturally preserves the simple excited voice.'},
(290,1166):{0:'The stammered complete report exactly preserves no sign of departure.',1:'The natural refuses-to-leave idiom conveys the bear’s continuing presence.',2:'The frustrated no-good/will-not-move report is natural.',3:'The stammered failed-result report naturally preserves worry.',4:'The rough stammered will-not-run warning preserves continued danger.',5:'The older speaker’s complete worried observation is natural.',6:'The go-home phrasing keeps the source’s simple anthropomorphic voice; it is not a mapped-home claim.',7:'The reflective short movement observation fits the formal older register.'},
(290,1632):{0:'The relieved sigh and giving-up report preserve the waiting outcome.',3:'The relieved giving-up report remains natural without grammatical gender marking.',4:'The at-last phrasing preserves emphatic relief in the rough voice.',5:'The conventional sleep sound preserves the nonspoken gag.'},
(290,1924):{3:'The expressive what-nerve complaint naturally conveys the bear’s brazen refusal.',4:'The rough has-guts/will-not-run reaction matches the source tone.',5:'The incredulous rhetorical complaint is natural and preserves failed intimidation.',7:'The disappointed formal observation and stubborn-beast phrase preserve the bear’s refusal.'},
(290,2398):{7:'The complete alarm and suggestion to flee preserve danger without invented injuries.'},
(290,3040):{0:'The complete somehow-escaped statement naturally preserves relief.',1:'The relieved sigh and complete escape report are natural.',6:'The breathless terror recollection preserves the simple frightened register.',7:'The breathless observation preserves apparent group safety and relief.'},
(290,3300):{0:'The urgent through/ruins discovery is natural with the forest context already established.',1:'The restrained through/ruins observation naturally marks arrival.',2:'The complete forest-exit relief and excited ruins identification are natural.',3:'The woods exit and paused ruins identification preserve the expressive discovery.',6:'The complete exit/strange-stones question preserves uncertainty about the ruins.',7:'The formal short through/ruins observation naturally marks discovery without extra names.'},
(291,24):{3:'The complete lost-without-map warning naturally preserves this variant’s specific concern.',4:'The colloquial suicidal idiom preserves the source’s reckless-with-life warning; it is figurative danger language.'},
(291,824):{6:'The simple complete bad-feeling observation naturally conveys unease without additional creatures.'},
(291,1246):{3:'The complete cramped-cave warning naturally preserves the risk to allies without assuming gender.',7:'The formal complete friendly-fire warning preserves the reason shooting is unsafe.'},
(291,1890):{1:'The restrained complete victory report is natural.',6:'The excited victory and explicit strong tiger are natural and preserve this variant’s specific remark.'},
(291,2194):{2:'The informal complete hunger conclusion and no-chase explanation match this source voice’s confident deduction.',5:'The complete older-speaker inference explicitly derives lack of hunger from no pursuit.'},
(294,28):{2:'The clear map requirement naturally conveys the immediate gate in the simple voice.',4:'The colloquial come-on and complete map prerequisite are natural.',5:'The concise map requirement conveys the gate without extra facts.',6:'The simple emphatic map plea fits this voice without forced baby talk.'},
(300,24):{2:'The colloquial no-map question and inability to proceed naturally convey the complaint.',6:'The simple emphatic inability to continue preserves the map gate.'},
(300,1610):{0:'The urgent ahead call naturally directs the admiral’s attention without naming the discovery.',1:'The short ahead call naturally functions as an instruction to look.',4:'The direct look command is natural and preserves the unnamed discovery.',5:'The direct look-there command preserves the pointing cue.',6:'The simple name/there call preserves the excited pointing reaction.',7:'The awed exclamation is natural and needs no explanation.'},
}

GOLD={(283,19):250000,(286,59):25000,(287,20):180000,(287,119):5000,(293,20):70000}
MARKET={(287,46):'Havana',(293,43):'Malacca'}


def main():
    assert not OUT.exists();draft,current,objects=map(load,(DRAFTS,CURRENT,OBJECTS))
    assert current['runtime']==objects['runtime'] and current['records']==242 and objects['native_style_getter_cases']==144
    bound={r['id']:r for g in current['groups'] for r in g['records']}
    bound.update({r['id']:r for r in objects['style_records']+objects['choice_records']})
    assert len(bound)==len(draft['records'])==384
    rows=[];glyphs=[]
    for original in draft['records']:
        row=deepcopy(original);old=bound[row['id']]
        assert all(row[k]==old[k] for k in ('source_reference','source_hex','source_Japanese'))
        for key,value in old.items():
            if key.startswith('current_') or key=='selected_native_pointer':row[key]=deepcopy(value)
        prior=mark_macros(old['current_comparison_paragraph'],row);english=row['english'];reason=None
        if row.get('kind')=='typed-choice-label':
            key=(row['block'],row['source_command_offset'],row['source_index'])
            if key==(290,876,0):reason='The action is fighting bravely, not merely being brave; make the combat choice explicit.'
            elif key==(290,1876,0):reason='Specify scaring it away so the intimidation branch is distinct from attacking.'
            elif key==(300,560,0):reason='The source action is fighting the giant snake, not the narrower Hit action.'
            else:english=prior;reason='The existing concise caption naturally preserves this specific source choice: '+row['source_meaning']
        elif row.get('kind')=='actor-style-alternative':
            key=(row['block'],row['source_command_offset']);index=row['source_style_indices'][0]
            retained=STYLE_RETAIN.get(key,{}).get(index)
            if retained:english=prior;reason=retained
            else:
                reason='Restore the variant’s complete meaning and spoken register: '+row['source_meaning']
                if key==(290,328) and index==6:reason='The source hopes for something good, not specifically treasure; preserve the broad excited anticipation.'
                if key==(290,970):reason='Make running away explicit and restore this variant’s distinct reaction rather than merely reporting that the bear ran.'
                if key==(290,2398) and index<4:reason='The source says an expedition member was attacked, not specifically mauled; preserve the personal danger/escape warning without assuming gender.'
                if key==(290,2398) and index==4:reason='Preserve the rough speaker’s uncertainty about several possible injuries, not a confirmed male-only injury report.'
                if key==(291,1246):reason='Use a natural warning about hitting allies in cramped quarters, without assuming a male-only party or personal friendships.'
                if key==(291,1890) and index==4:reason='The source says defeated, not explicitly dead; preserve the rough victory exclamation without inventing death.'
                if key==(291,1890) and index in [0,2,3,5,7]:
                    reason='Vocalize the breath sound naturally rather than speaking the stage-direction word Pant; preserve this variant’s confidence/uncertainty.'
                    if index==5:english='Hah... hah... We finally brought it down!'
                if key==(290,3040) and index in [2,3]:reason='The source expresses having survived, not an assessment that a location looks safe; preserve breathless relief.'
                if key==(290,3040) and index==4:reason='Preserve the rough speaker’s relieved question about getting away rather than an unqualified report.'
                if key==(290,3300) and index==4:reason='Restore the excited forest exit and affirmative ruins recognition in the rough voice.'
                if key==(290,3300) and index==5:reason='Preserve the older speaker’s tentative identification of the ruins rather than asserting it outright.'
                if key==(300,1610):reason='Preserve the source’s stammered, hesitant pointing reaction without naming the discovery.'
        else:
            key=(row['block'],row['source_reference']['record_index']);retained=RETAIN.get(key[0],{}).get(key[1])
            if retained:english=prior;reason=retained
            elif key in GOLD:reason=f'Restore the explicit gold-coin denomination while retaining exactly {GOLD[key]:,}.'
            elif key in MARKET:reason=f'Identify market share explicitly in {MARKET[key]}, retaining a slight increase without inventing an amount.'
            elif any(ord(c)>127 for c in prior):
                reason='Preserve the exact silence/reaction in scoped ASCII dialogue punctuation; fresh glyph and layout checks are required.'
                glyphs.append(dict(id=row['id'],current_text=prior,target_text=english,kind='scoped-non-ASCII-punctuation-consistency'))
            else:reason=SPECIAL.get(key,'Restore the complete speakable source turn: '+row['source_meaning'])
        if english==prior and row.get('kind')=='actor-style-alternative' and not STYLE_RETAIN.get((row['block'],row['source_command_offset']),{}).get(row['source_style_indices'][0]):
            reason='The current wording already matches the independent clean-source draft and preserves this specific variant: '+row['source_meaning']
        if english==prior and reason is None:raise AssertionError(row['id'])
        english.encode('ascii');assert not any(t in english for t in ['{LB','{ALIGN','{PAD}','\n','%'])
        assert {m:english.count('{MACRO:'+m+'}') for m in ['FI','FA','FO']}=={m:row.get('source_macros',{}).get(m,0) for m in ['FI','FA','FO']}
        decision='retention' if english==prior else 'revision'
        assert reason
        row.update(english=english,logical_English=english,decision=decision,finding=reason,
            retention_reason=reason if decision=='retention' else None,localization_note=reason,
            current_comparison_paragraph=old['current_comparison_paragraph'],
            independent_clean_draft_reference=dict(path=str(DRAFTS),id=row['id'],sha256=digest(DRAFTS)),
            current_English_conversation_comparison_pending=False,current_ROM_English_unconsulted=False,current_English_now_exposed=True,
            clean_first_draft_not_final_comparison_approval=False,source_only_not_final_English=False,
            source_current_complete_exchange_comparison_complete=True,new_credit=0)
        assert row['review']==dict(source=True,context=True,localization=True,naturalness=True,formatting=False)
        rows.append(row)
    counts=dict(Counter(r['decision'] for r in rows));assert sum(counts.values())==384
    assert len(glyphs)==5
    save(OUT,{**draft,'records':rows,'counts':counts,'remaining_contextual_comparisons':0,
        'all_four_individual_prose_gates_pass':True,'all_formatting_gates_pending':True,
        'scoped_native_names_terms_anddisplay_still_pending':True,'current_English_comparisons':384,
        'current_binding':str(CURRENT),'current_binding_sha256':digest(CURRENT),
        'current_objects':str(OBJECTS),'current_objects_sha256':digest(OBJECTS),
        'current_ROM':current['current_ROM'],'current_ROM_sha256':current['current_ROM_sha256'],'native_runtime':current['runtime'],
        'findings_requiring_fresh_display_checks':glyphs,'native_substitutions_require_fresh_changed_body_checks':True,
        'no_new_font_artwork_orengine_changes':True,'prose_only_no_new_ROM_orregistered_credit':True,
        'full_goal_complete':False,'new_credit':0,'evidence':{str(p):digest(p) for p in (DRAFTS,MEANINGS,CURRENT,OBJECTS,Path(__file__))}})
    print('Saved 384 complete contextual comparisons:',counts,'; names, terms and fresh display gates remain.')


if __name__=='__main__':main()
