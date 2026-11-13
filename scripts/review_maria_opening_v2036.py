"""Fresh complete Hangzhou opening38 from clean Japanese, with individual reasons."""
from collections import Counter
from pathlib import Path
import re
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/maria_opening_editorial_v2036')
SOURCE=Path('work/analysis/maria_opening_source_v2034/all38_clean_current_Hangzhou_opening_source.json')
DOC=Path('translations/maria_opening_contextual_editorial_manuscript_v1.json')
# ordinal|faithful source gloss first|proposed English (=retains normalized current)|decision reason
TEXT=r"""
0|Jam energetically reports his return to the admiral.|Admiral, we're back!|The contraction and direct report restore his buoyant spoken voice; the old we are sounded unusually stiff for him.
1|Yukihisa formally reports completion of the mission to destroy the wako ships.|The wako ships are destroyed. Our mission is complete.|Restore a complete formal report and the mission's target. Wako is the source's pirate designation,not a new nationality claim about every raider.
2|Maria asks about their own losses.|=|Our losses is a natural concise military question and sets up Jam's boast and Yukihisa's precise report.
3|Jam laughs and says that using the familiar tactic rules out taking damage.|Heh heh! We used that tactic of yours. Losses? Not a scratch!|His boast now sounds spontaneous. The complete following exchange explicitly credits Maria's plan,so yours does not invent its author.
4|They use a formation to trap nimble wako ships that specialize in boarding,then sink them with overwhelming firepower and sustain no losses.|Our formation trapped the nimble wako ships, skilled at boarding. We sank them with overwhelming firepower and suffered no losses.|Restore the contrast between enemy boarding skill and formation/firepower without inventing a failed boarding attempt. Yukihisa's technical delivery contrasts with Jam's boast.
5|Richard gives a thoughtful acknowledgment and thanks them for their work.|=|Hmm. Good work is natural and concise. The following two silences,and Maria's later praise,preserve the joke of his premature acknowledgment.
6|Jam says nothing in response to Richard.|...|Preserve this separate silent reaction with Jam's native preamble,using American ellipsis punctuation.
7|Yukihisa also says nothing in response to Richard.|...|Keep the second distinct silence before the actual admiral speaks; it is part of the conversational timing.
8|Maria praises and thanks both returning officers.|You both did well. Thank you.|Address both officers directly and keep both praise and acknowledgment of their work. Both did well was unnatural in a direct exchange.
9|Jam cheers exuberantly at Maria's praise.|=|Yahoo is an idiomatic exuberant cheer and keeps his response markedly less formal than Yukihisa's.
10|Yukihisa gives a crisp respectful acknowledgment.|=|Yes preserves the short formal acknowledgment without inventing a new title or extra explanation.
11|Jam familiarly greets the older Xien and says they have returned.|Hey, Xien! We're back!|A familiar Hey and contraction convey his casual address. Avoid old man Xien sounding like an official label or a kinship claim.
12|Xien says he has heard they achieved a great victory.|I hear it was quite a victory.|Restore the reported nature of his information and the approving scale of the achievement.
13|Yukihisa says they only maneuvered the fleet as FI planned;victory was assured once they gained the windward position in the narrow bay.|We only maneuvered the fleet as FI planned. Once we took the windward position in that narrow bay, victory was assured.|Restore the narrow bay and explicit fleet maneuvering,while preserving his modest attribution of the victory to Maria.
14|Jam marvels that the enemy fleet appeared exactly as Admiral FI said it would,and says even they were surprised.|The enemy fleet showed up just like Admiral FI said it would! Man, even we were surprised!|Keep his excited colloquial delivery and her explicit admiral address. Do not narrow the prediction to a location that the source does not specify.
15|Yukihisa calls the plan a masterstroke and praises its brilliance.|=|A masterstroke. Brilliant is polished but emphatic praise that suits his restrained formality after Jam's excitement.
16|Xien thoughtfully says FI has done well.|=|The measured Hmm and third-person acknowledgment naturally continue his approving reaction and retain the exact FI substitution.
17|Jam says Maria is very frightening but also impressive or appealing.|She's terrifying, but... she's pretty great, huh?|Restore a spoken,admiring aside rather than a flat adjective list. Great preserves the broad favorable feeling without inventing romance.
18|Yukihisa says their lives are owed to her presence and leadership.|We owe our lives to her.|This idiomatic expression preserves his gratitude and devotion; depend on that commander lost the personal acknowledgment.
19|Xien dislikes Richard,who can do no work aboard a ship yet acts as FI's adviser.|Still, Richard is insufferable. He's useless aboard a ship, yet he acts like he's FI's adviser.|Keep the older man's pointed irritation and the shipboard-work contrast; at sea alone could be mistaken for a narrow navigational criticism.
20|Jam says it cannot be helped:Richard's strong connections back in England let them operate openly and run wild in isolationist Ming waters.|What can you do? His powerful connections back in England let us run wild in Ming's closed waters.|The colloquial rhetorical question and run wild retain Jam's swagger. Preserve the game-stated maritime closure and English connections without adding a legal charge or an outside historical claim.
21|Xien teases Jam that he has no such connection to France.|Yet you have no such ties to France.|Restore the explicit country. Such ties naturally links his teasing reply to Richard's English connections.
22|Jam says he took the blame for an unknown man's crime and cannot show his face at home;he threatens to beat the man if he finds him.|Heh. I took the blame for some stranger's crime, so I can't go home. If I find him, I'll give him a beating!|Restore the first-person colloquial explanation. Took the blame keeps the stated facts without inventing the method by which someone framed him.
23|Xien says Yukihisa's fate is also ironic.|=|The understated observation makes a natural transition from Jam's predicament to Yukihisa's reversed relationship with the pirates.
24|Yukihisa stowed away on a wako ship to reach Ming in search of a legendary sword,but instead ended up suppressing those pirates.|You stowed away on a wako ship to reach Ming in search of a legendary sword, only to end up hunting those very pirates.|Restore the stowaway journey,its destination and its purpose. Only to end up conveys Xien's ironic comparison without introducing a new sword name.
25|Yukihisa asks Xien not to worry;he happened to learn abroad of his compatriots' wrongdoing and cannot leave such disgraceful men alone.|Do not concern yourself. I happened to learn of my countrymen's wrongdoing abroad. I cannot leave such disgraceful men unchecked.|Restore compatriots,the incidental discovery abroad and his duty to act. Formal,complete sentences preserve his principled voice without adding a rank or claiming an outcome.
26|Xien approves the reassuring strength of Yukihisa's words.|=|Reassuring words is a natural reflective acknowledgment from Xien and closes the officers' conversation cleanly.
27|Maria asks whether Ian is present.|Is Ian here?|Restore the named person and her question about his presence; the envoy was an invented replacement for the source name.
28|Ian asks whether she needs him.|=|You called is a natural prompt for Maria's request and preserves his attentive brevity without adding an unspoken form of address.
29|Maria requests a report on contracts with the coastal towns.|=|Report on the coastal contracts is a natural clipped command in this established trade discussion. It keeps the coast and contract subject without burdening her direct voice.
30|Ian reports smooth progress and the remarkable effectiveness of bribes.|=|Going well. Bribes work wonders is natural confident reporting,and the dry second sentence preserves his matter-of-fact attitude toward corruption.
31|They settled on paying three percent of sales;Ian says officials will look away if their ships are disguised as foreign vessels.|We agreed to pay 3 percent of sales. They say the officials will look the other way if we pass our ships off as foreign vessels.|Make the payment direction and the ships being disguised explicit,and preserve the reported assurance. Percent remains spelled out to avoid native printf parsing.
32|Maria says this is as expected and condemns their complete corruption.|=|As expected. Utterly corrupt... naturally preserves her terse disgust and contrasts with Ian's practical approval.
33|Ian calls the admiral harsh,but thinks the magistrate realized overlooking their trade would be advantageous because of its large expected tax revenue.|Harsh words, Admiral... But the magistrate must have seen the benefit of overlooking trade that promises so much tax revenue.|Restore the tax-revenue rationale and Ian's inference. The reply stays diplomatically practical rather than joining Maria's condemnation.
34|Merchants always seek profit;Ian says winning their support beforehand has proved worthwhile.|=|The existing two sentences clearly preserve both the general profit motive and the value of securing their support early. They complete his explanation without changing the referent to officials.
35|Ian says the path is now open and trading can begin at once.|=|The way is open and Trade can begin immediately are idiomatic and preserve both the successful arrangement and its immediate practical consequence.
36|Maria agrees and orders thorough ship maintenance in anticipation of Kurushima's retaliation.|Yes. Make sure the ships are thoroughly serviced in preparation for Kurushima's retaliation.|Restore the explicit thoroughness and anticipatory maintenance order,keeping Maria's disciplined attention on the coming threat.
37|Ian respectfully acknowledges the order.|=|Understood is an idiomatic closing acknowledgment and preserves the clean end of the complete exchange.
"""

if __name__=='__main__':
    assert not ROOT.exists()and not DOC.exists()
    source=read(SOURCE);plans=[line.split('|')for line in TEXT.strip().splitlines()]
    assert len(plans)==len(source['records'])==38 and[int(p[0])for p in plans]==list(range(38))
    speakers={'03':'Maria Huamei Li','0a':'Xien Yan','0b':'Jam Jack Ludwyan','0c':'Yukihisa Genjo Shiraki','15':'Ian Dukov','4a':'Richard Townsend'}
    rows=[]
    for original,(_,gloss,proposed,note)in zip(source['records'],plans,strict=True):
        before=original['provisional_current_reference'];prefix=original['source_reference']['leading_byte_hex']
        current=re.sub(r'\s+',' ',before['body_after_first_byte_CP932']).strip();english=current if proposed=='='else proposed
        assert re.findall(r'\b(?:FI|FA|FO)\b',english)==re.findall('FI|FA|FO',original['source_reference']['body_after_first_byte_CP932'])
        english=re.sub(r'\b(FI|FA|FO)\b',lambda m:'{MACRO:'+m[1]+'}',english);decision='retain-wording'if proposed=='='else'revise'
        rows.append(dict(id=original['id'],file_path='/data/SC3.DK4',block=33,source_ordinal=original['source_ordinal'],
            source_reference=original['source_reference'],current_reference=before,source_hex=original['source_reference']['hex'],current_text_hex=before['hex'],
            source_record_index=original['source_reference']['segment_index'],record_index=before['segment_index'],
            source_complete_preamble_hex=original['source_reference']['complete_preamble_hex'],source_presentation_prefix_hex=prefix,
            source_Japanese=original['source_reference']['body_after_first_byte_CP932'],current_stored_English=before['body_after_first_byte_CP932'],
            speaker=speakers[prefix],source_meaning=gloss,english='{SPEAKER:'+prefix.upper()+'}'+english+'{PAD}',
            editorial_decision=decision,localization_note=note,
            **({'fresh_retained_wording_justification':note}if decision=='retain-wording'else{'finding':note}),
            context='Complete SC3 B33 Hangzhou opening:Jam andYukihisa report naval success,Richard interjects beforeMaria praises them;the officers discussMaria,English connections,French exile andYukihisa\'s sword-search irony;Maria andIan discuss bribed coastal contracts,three-percent payments,foreign-ship disguise,tax revenues andpreparation forKurushima\'s retaliation. Read every full exchange andneighboring speech. Preserve distinct casual/formal voices,humor,cultural context andexact names withoutinvented kinship,rank,framing method orlegal detail.',
            review=dict(source=True,context=True,localization=True,naturalness=True,formatting=False)))
    ROOT.mkdir(parents=True);(ROOT/'source_packet.json').write_bytes(SOURCE.read_bytes())
    save(DOC,dict(format='dk4-ilnk-translation-batch-v1',file_path='/data/SC3.DK4',source_file_sha256=source['current_SC3_sha256'],
        editorial_clean_source_file_sha256=source['clean_SC3_sha256'],source_ROM=source['clean_ROM'],source_ROM_sha256=source['clean_ROM_sha256'],
        current_ROM=source['candidate'],current_ROM_sha256=source['candidate_sha256'],required_runtime_ARM9_sha256=source['ARM9_sha256'],
        encoder='dialogue-fixed-v1',dialogue_profile='maria-story-live',translation_policy='natural-dialogue-v2',target_locale='en-US',
        review_gates=['source','context','localization','naturalness','formatting'],records=rows,
        source_packet=str(SOURCE),source_packet_sha256=sha(SOURCE.read_bytes()),draft_only_not_formatting_or_release_authorized=True,
        current_live_control_context='work/analysis/maria_opening_context_v2035',native_catalog_names_measured_on_isolated_copies_not_claimed_pure=True,
        measured_default_native_substitutions={'FI':'Maria','FA':'Li','FO':'Li Clan'},
        separate_FE_objects=0,progressive_objects=38,source_choice_objects=0,
        next_gates=['Bind current live six-speaker context andexact macro measurements.','All38 native macro/font/bounds/pagination checks.',
            'Complete85-command map,CS0101 loader andpractical revised scene transition.','Guarded registered cumulative integration andexact clean-input patch.'],full_goal_complete=False))
    decisions=Counter(r['editorial_decision']for r in rows)
    save(ROOT/'source_prose_review_receipt.json',dict(manuscript=str(DOC),manuscript_sha256=sha(DOC.read_bytes()),records=38,decisions=dict(decisions),
        complete_opening_source_current_context_reviewed=True,each_row_has_gloss_and_revision_or_retention_reason=True,
        formatting_approved=False,registered_or_completed=False,ROM_registry_or_ledger_not_changed_by_this_producer=True,
        producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print(dict(source_prose_records=38,decisions=dict(decisions),native_formatting_and_release_pending=True))
