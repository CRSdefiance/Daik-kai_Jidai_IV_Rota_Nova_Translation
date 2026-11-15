"""Complete73-speech fresh contextual manuscript; native/release gates pending."""
from collections import Counter
from pathlib import Path
import re
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/hodram_opening_editorial_v2019')
SOURCE=Path('work/analysis/hodram_opening_source_v2017b/all73_clean_current_opening_and_Lil_encounter_source.json')
DOC=Path('translations/hodram_opening_contextual_editorial_manuscript_v1.json')

# block:ordinal|source gloss|proposed English (=retains normalized current wording)|individual decision reason
TEXT=r"""
42:0|Hodram quietly orders a warning to be issued.|=|The terse command suits his controlled manner before the repeated chain of orders.
42:1|An unnamed subordinate crisply acknowledges the order.|=|Aye is a natural naval acknowledgment; FE remains an unattributed voice rather than a named officer.
42:2|Charles relays the command to issue a warning.|=|Repeating Warn them preserves the command passing down the chain.
42:3|Another unnamed acknowledgment answers the relayed order emphatically.|=|Aye, aye keeps the enthusiastic response distinct from the first acknowledgment.
42:4|The hail declares military surveillance,accuses that ship of violating national territorial waters,and orders it to halt.|Our forces patrol these waters! Your ship is violating our territorial waters! Stop at once!|Restore the direct accusation and command; the old generic border rule loses who is being addressed and the national-water claim.
42:5|Hodram orders his men to move.|=|Move out is a concise command that maintains his decisive voice without specifying an unspoken attack maneuver.
42:6|Hodram thanks his men for their work.|=|Well done naturally conveys the senior officer's acknowledgment after the operation.
42:7|Gerhard politely asks the admiral to address the crew.|Admiral, would you address the crew?|Restore the respectful request; a bare imperative sounded like Gerhard was ordering his commander.
42:8|Hodram hesitates before the speech he dislikes.|=|Hm preserves the reluctant pause that the officers' following silences prolong.
42:9|Charles waits silently for Hodram to begin.|...|Use American ellipsis punctuation while keeping this separate silence and its original Charles preamble.
42:10|Manuel also waits silently.|...|Keep the second officer's separate expectant beat rather than omitting a native speech object.
42:11|Hodram asks the men whether they know the rapidly rising island nation in the North Sea.|Do you know the island nation rising so rapidly in the North Sea?|Restore the rhetorical question whose answer in the next speech is England.
42:12|England openly allows piracy against Spanish merchant ships and uses their wealth to steadily strengthen its navy.|England openly permits piracy against Spanish merchant ships, taking their wealth to steadily strengthen its navy.|Keep ships,public authorization and gradual naval growth explicit; this sets up the example Hodram says Sweden must follow.
42:13|Their country seeks Baltic and North Sea supremacy and must emulate that example to raise its navy to world-class standards.|Sweden seeks to dominate the Baltic and North Seas. We must follow their example and build a world-class navy.|Restore the link to England's example and both seas; Sweden is the already established national context,not a new affiliation.
42:14|They alone have been entrusted with this undertaking,yet little is actually expected of them.|Though we've been entrusted with this undertaking, little is actually expected of us.|Avoid the unsupported universal claim that no one expects anything; preserve his frank contrast between responsibility and low expectations.
42:15|Gerhard falls silent at that assessment.|...|The distinct silent reaction makes Hodram's frankness land; American punctuation replaces the untranslated glyph.
42:16|The fleet is a navy in name only,and its sole current ship is the Vestaros.|As you all know, we're a navy in name only. This ship, the Vestaros, is the only vessel in our fleet.|Restore the named ship and distinguish their small fleet from the whole country's navy. Vestaros is confirmed in the current native ship data and established display evidence.
42:17|The brass see them only as a pirate-like patrol fleet,a stopgap until a regular force is formed.|Our superiors see us as little more than pirates on patrol, a stopgap until a regular navy is formed.|Correct pirate hunters,a factual reversal. Regular navy follows the explicit naval context; no new rank or unit is created.
42:18|As a young nation,the country has budget difficulties,partly because supporting Protestants is national policy.|That's the trouble with being a young nation. Our policy of supporting the Protestants leaves little room in the budget.|Keep the religious and policy context rather than turning the line into a vague complaint about Protestants.
42:19|The task ahead is very hard and Hodram does not expect it to be solved within two or three years.|=|The long road and exact two-or-three-year contrast remain clear in natural speech.
42:20|One day they should sail the world's strongest navy,built by their own efforts,on the Baltic before the king and all their people.|One day, let's show His Majesty and all our people the world's strongest navy, built by our own hands and sailing the Baltic!|Restore building the navy through their own efforts; under our command added a different claim and weakened the rally's central ambition.
42:21|Success or failure depends on the men's tireless efforts.|Success depends on your tireless efforts!|Keep the sustained effort asked of the crew rather than only saying every individual matters.
42:22|The crew roars its approval.|=|Yeah naturally conveys this collective burst of enthusiasm,without assigning the FE response to a particular officer.
42:23|The crew applauds.|=|(Applause) is a clear stage direction for the Japanese clapping sound effect; it is not invented spoken dialogue.
42:24|Manuel says the admiral's speeches give him a thrill as always.|=|Your speeches always give me chills keeps the admiration and establishes the friendly praise that embarrasses Hodram.
42:25|Gerhard says it is no exaggeration that those passionate speeches persuaded them to devote their lives to this country.|=|Devote our lives localizes the burial idiom by intent and keeps their personal commitment without inventing birthplace or family ties.
42:26|Charles first learned what trembling with anticipation for battle felt like during one of Admiral FA's addresses.|It was one of your speeches, Admiral FA, that first made me tremble with excitement for battle.|Restore the personal first experience and the battle-thrill image; you stirred us all erased both and changed the subject to everyone.
42:27|Hodram asks them to stop;pompous addresses are among the duties he finds most painful,and he changes topic.|=|The curt Enough and admission about speeches contrast naturally with the public rally and move to practical business.
42:28|He reports that defeating hostile fleets and pirates will now earn state rewards according to the results.|I hear we'll now receive state rewards for defeating enemy fleets and pirates, based on our results.|Preserve the reported-news stance and performance-based state payment,without changing it into a fixed reward or unrelated subsidy.
42:29|Manuel reacts with enthusiasm at the news.|=|Great is an immediate informal response that fits his lively voice.
42:30|Charles concludes that they now have the conditions needed to expand their fleet budget.|=|The practical budget conclusion clearly follows the new reward policy.
42:31|Gerhard says they can finally take the offensive.|=|At last, we can attack naturally expresses his eagerness to move from defense to action.
42:32|They must promptly check the report of unauthorized Hanseatic incursions;today's quarry was apparently not what they expected.|We must quickly check that report of Hanseatic ships violating our waters. It seems today's quarry wasn't what we expected.|Remove the invented escape outcome and restore the urgency and uncertain appraisal of today's quarry.
42:33|After a short rest for the sailors,departure preparations are to begin immediately.|Once the crew has had a short rest, get us ready to sail at once.|Keep both the brief rest and the immediate preparation afterward,not an open-ended delay.
42:34|Gerhard acknowledges the order crisply.|=|Sir is an established military acknowledgment in this admiral/subordinate exchange,not a new rank.
42:35|Charles acknowledges the order.|=|Aye is concise and appropriately naval.
42:36|Manuel gives an energetic naval acknowledgment.|=|Aye, aye captures the borrowed Japanese Aye sir sound without manufacturing a new address.
43:0|Gerhard proposes defeating Speyer and recovering Baltic coastal trade rights obtained through incursions into their waters.|=|The aggressive crush and reclaim wording suits Gerhard and preserves his stated justification and Baltic trade objective.
43:1|Charles explains that sea-battle victories weaken the enemy's hold on the towns.|Victory at sea weakens the enemy's grip on the towns.|Avoid narrowing the mechanic to ports wholly controlled by the enemy; the discussion concerns competing trade rights.
43:2|A strong fleet can maintain a large trade area,whose profits finance an even stronger fleet.|=|The circular fleet-trade-profit argument remains complete and conversational.
43:3|Manuel says regular trade is the best way to raise the huge sum required to build a fleet.|Exactly. Building a fleet costs a fortune. The best way to raise it is to trade regularly.|Restore the comparison and fleet-building purpose; the earlier compressed statement merely said trade provides money.
43:4|Hodram concludes that the world's largest trading sphere is the shortcut to the world's best fleet.|So building the world's largest trading network is the fastest route to the world's strongest fleet.|Restore the first world-leading objective; good trade did not preserve the scale of the network.
43:5|Gerhard says that,in the long run,a force without funding cannot achieve victory.|Exactly. In the long run, no force can win without the money to support it.|Keep the long-term financial principle without inventing a requirement that the war itself be long.
43:6|Manuel advises contracts in as many towns as possible,even at one percent,to establish routes before increasing market share.|=|The exact one-percent amount,contracts-first route network and later share expansion are all clear; percent remains spelled out for native format safety.
43:7|If a faction they are at war with has a contract in a town,they can then invest to take its market share freely.|If a power we're at war with has a contract in that town, we can then invest to take its share freely.|Restore wartime status and the rival contract condition; after battle and enemy control of the whole port were unsupported additions.
43:8|Hodram first orders contracts with the major North Sea towns to secure an outlet to the open ocean.|Good. First, we'll sign contracts in the main North Sea towns and secure an outlet to the open ocean.|Keep the initial action,the main towns and the outward strategic direction,rather than a generic ocean route.
44:0|A young woman's unseen voice calls out Hey,you.|A young woman's voice: "Hey, you!"|Keep the source's offscreen female-voice cue and direct call. The FE consumer remains unattributed; Lil is identified only when she appears.
44:1|Hodram reacts to the unexpected call with confusion.|?|Preserve the wordless question using American punctuation and the exact Hodram preamble.
44:2|Lil identifies the ship moored in the harbor as his and angrily questions his intentions.|That ship in the harbor's yours, right? What do you think you're doing?|Restore the harbor reference and challenge to his intentions; what are you doing here was a different question.
44:3|Hodram says nothing as Lil accosts him.|...|Keep the deliberate silent beat that fuels Lil's frustration,using American punctuation.
44:4|Lil demands to know if he is listening and says she is speaking to him.|Are you listening? I'm talking to you!|Restore the unanswered demand rather than repeating the ship identification and a generic Listen.
44:5|Hodram asks what she wants to say.|=|What is it is a natural terse response for his restrained manner after the silence.
44:6|Lil calls this her territory and says she will never allow him to begin trading without permission.|=|Barge in and start trading captures her possessive bluster and commercial grievance without adding a legal ownership fact.
44:7|Camille rebukes Lil for speaking rudely to a complete stranger.|=|The direct admonition sounds natural and establishes Camille's discomfort with her behavior.
44:8|Hodram says that signing a contract and trading under it should cause no problem.|If we sign a contract to trade, there should be no problem...|Keep the conditional explanation and measured should; the next line must quote this wording recognizably.
44:9|Lil mockingly repeats his no-problem claim and complains that he is stiff and gloomy.|"There should be no problem..." Ugh! You're so stiff and gloomy.|Keep the spoken quotation synchronized with Hodram's previous line and preserve Lil's mocking tone.
44:10|Camille asks her to stop and warns that this is a bad idea.|Lil, stop. This is a bad idea.|Restore the warning as well as the request,without inventing a specific threat or outcome.
44:11|Lil realizes he is military and sarcastically asks if soldiers,adventurers and pirates are all trading now.|Oh, I see. You're a military man. So now soldiers, adventurers, and pirates are all going into business?|Restore adventurers and the sarcastic question while keeping the three groups parallel.
44:12|She complains that outsider after outsider enters the merchants' territory with an arrogant attitude.|=|The territory and ownership language retain the merchant grievance established by her preceding lines; the casual complaint suits Lil.
44:13|Camille urgently calls Lil's name again.|=|The short repeated name conveys his growing alarm without adding an instruction.
44:14|Gerhard angrily interrupts after listening to her abuse.|=|That is enough,woman preserves his abrupt insult and anger,which Hodram immediately restrains.
44:15|Lil challenges him to a fight.|=|The blunt challenge keeps her aggression and leads directly to Hodram's intervention.
44:16|Hodram tells Gerhard to stop.|=|The terse name and order show his control of his subordinate without a new explanation.
44:17|Gerhard protests to his commander.|=|But,sir preserves the unfinished respectful objection before Lil speaks again.
44:18|Lil grudgingly acknowledges that Hodram seems unexpectedly mature or reasonable.|Huh. You're more reasonable than I thought.|Keep her limited concession to his composure,rather than changing it into a broad judgment of moral decency.
44:19|She insists that this is a separate matter,threatens consequences if he interferes,and tells Camille to leave with her.|=|The existing transition and threat work in the established trading dispute,and Camille already uses the approved spelling.
44:20|Camille stammers an apology and asks them not to be offended,then worries that this is asking too much.|Um, I-I'm sorry... Please don't take offense... though that's probably asking too much.|Restore his hesitant concession instead of asserting that Hodram has already taken offense; Hodram's restrained reaction matters to the joke.
44:21|Camille hesitantly takes his leave.|=|The stammer and brief goodbye preserve his awkward attempt to end the encounter.
44:22|Charles remains speechless after the confrontation.|...|Keep this separate reaction with its Charles preamble; it is not a disposable non-prose fragment.
44:23|Manuel exclaims and stammers at what a girl she is.|Yikes... W-what a girl!|Restore shock and the stammer so the line reads as flustered disbelief rather than admiration.
44:24|Gerhard protests that even generosity has limits and that FI has allowed an extremely rude woman's abuse.|FI, even generosity has its limits! How can you let that rude woman insult you like that?!|Restore the full objection and explicit tolerance of abuse; FI,you're too forgiving erased most of his outraged reasoning.
44:25|Hodram says dealing with people like her is more painful than any torture.|=|The exaggerated comparison explains his restraint as weary avoidance and caps the contrast with Gerhard.
44:26|Manuel invokes the proverb about avoiding trouble and says she is the kind of person one should not anger.|=|Best not to stir up trouble naturally conveys the proverb's intent in this European setting without inventing religious beliefs; the following warning completes the thought.
"""

if __name__=='__main__':
    assert not ROOT.exists()and not DOC.exists()
    source=read(SOURCE);plans=[line.split('|')for line in TEXT.strip().splitlines()]
    expected=[(p['block'],i)for p in source['packets']for i,_ in enumerate(p['records'])]
    assert len(plans)==len(expected)==73
    assert [tuple(map(int,r[0].split(':')))for r in plans]==expected
    speakers={'01':'Hodram Joakim Bergstrom','10':'Gerhard Ardelknatts','12':'Charles Jean Rochefort','17':'Manuel Almeida','02':'Lil Argot','09':'Camille Marinus Overijssel','fe':'Unattributed crew or offscreen voice'}
    rows=[]
    raw_rows=[r for p in source['packets']for r in p['records']]
    for original,(_,gloss,proposed,note)in zip(raw_rows,plans,strict=True):
        before=original['provisional_current_reference'];prefix=original['source_reference']['leading_byte_hex']
        current=re.sub(r'\s+',' ',before['body_after_first_byte_CP932']).strip()
        english=current if proposed=='='else proposed
        assert re.findall(r'\b(?:FI|FA|FO)\b',english)==re.findall('FI|FA|FO',original['source_reference']['body_after_first_byte_CP932'])
        english=re.sub(r'\b(FI|FA|FO)\b',lambda m:'{MACRO:'+m[1]+'}',english)
        decision='retain-wording'if proposed=='='else'revise'
        rows.append(dict(id=original['id'],file_path='/data/SC1.DK4',block=original['block'],source_ordinal=original['source_ordinal'],
            source_reference=original['source_reference'],current_reference=before,source_hex=original['source_reference']['hex'],current_text_hex=before['hex'],
            source_record_index=original['source_reference']['segment_index'],record_index=before['segment_index'],
            source_complete_preamble_hex=original['source_reference']['complete_preamble_hex'],source_presentation_prefix_hex=prefix,
            source_Japanese=original['source_reference']['body_after_first_byte_CP932'],current_stored_English=before['body_after_first_byte_CP932'],
            speaker=speakers[prefix],source_meaning=gloss,english='{SPEAKER:'+prefix.upper()+'}'+english+'{PAD}',
            editorial_decision=decision,localization_note=note,
            **({'fresh_retained_wording_justification':note}if decision=='retain-wording'else{'finding':note}),
            context='Complete SC1 opening B42 naval warning/public address/private praise and reward policy;B43 fleet-trade-finance explanation and initial North Sea contracts;B44 Lil intrusion,Camille apologies,Gerhard outrage,Hodram restraint andManuel proverb. Read every full exchange and neighboring speech. Preserve military status,religious policy,political ambitions,trade conditions,the ship name and distinct formal/casual voices. No invented kinship,rank,battle outcome or trading condition.',
            review=dict(source=True,context=True,localization=True,naturalness=True,formatting=False)))
    ROOT.mkdir(parents=True)
    (ROOT/'source_packet.json').write_bytes(SOURCE.read_bytes())
    save(DOC,dict(format='dk4-ilnk-translation-batch-v1',file_path='/data/SC1.DK4',source_file_sha256=source['current_SC1_sha256'],
        editorial_clean_source_file_sha256=source['clean_SC1_sha256'],source_ROM=source['clean_ROM'],source_ROM_sha256=source['clean_ROM_sha256'],
        current_ROM=source['candidate'],current_ROM_sha256=source['candidate_sha256'],required_runtime_ARM9_sha256=source['ARM9_sha256'],
        encoder='dialogue-fixed-v1',dialogue_profile='hodram-story-probe',translation_policy='natural-dialogue-v2',target_locale='en-US',
        review_gates=['source','context','localization','naturalness','formatting'],records=rows,
        source_packet=str(SOURCE),source_packet_sha256=sha(SOURCE.read_bytes()),draft_only_not_formatting_or_release_authorized=True,
        current_live_control_context='work/analysis/hodram_opening_context_v2018',
        native_catalog_names_queried_on_isolated_copies_not_claimed_pure=True,
        measured_default_native_substitutions={'FI':'Hodram','FA':'Bergstrom','FO':'Bergstrom Fleet'},
        separate_FE_objects=6,progressive_objects=67,source_choice_objects=0,
        next_gates=['Close andbind the live original control/FE context.','Native source-bound macro/format/font/pagination checks.',
            'Typed reference map for93/31/47commands;practical original/revised scene transitions.','Guarded registered cumulative integration andexact clean-input patch.'],full_goal_complete=False))
    decisions=Counter(r['editorial_decision']for r in rows)
    save(ROOT/'source_prose_review_receipt.json',dict(manuscript=str(DOC),manuscript_sha256=sha(DOC.read_bytes()),records=73,decisions=dict(decisions),
        full_three_exchange_source_and_current_context_reviewed=True,each_row_has_gloss_and_revision_or_retention_reason=True,
        formatting_approved=False,registered_or_completed=False,ROM_registry_or_ledger_not_changed_by_this_producer=True,
        producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print(dict(source_prose_records=73,decisions=dict(decisions),native_formatting_and_release_pending=True))
