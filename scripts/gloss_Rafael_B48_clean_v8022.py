"""Freeze91 fresh clean-Japanese intent glosses and complete-exchange risks before English comparison."""
from copy import deepcopy
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/Rafael_B48_clean_gloss_v8022')
SOURCE=Path('work/analysis/Rafael_next_clean_v8020/complete_clean_SC0_B48_EV0_andcoverage_before_current_English.json')
NAMES=Path('work/analysis/Rafael_B48_clean_names_v8021/nine_clean_static_identity_fields_before_current_English.json')
# These are source meanings, not the release wording or approved English terminology.
GLOSSES={
5:"Rafael remembers that Athens is a city of learning and philosophy, with eager interest.",
17:"Janus feels the whole city has an atmosphere that makes him think he ought to study.",
32:"Cesare declares emphatically that there should be things for them to learn too.",
38:"Claudio complains about Cesare's stiff, overly formal manner and asks whether he can do something about it.",
49:"Cristina tells Claudio not to be so quick to complain.",
56:"Rafael chides Clau for always complaining.",
61:"Claudio puts on exaggerated compliance: all right, all right, he gets it; he will keep quiet.",
71:"Julio calls this a good opportunity and says he will go investigate the object called 覇者の証.",
75:"Claudio repeats the unfamiliar term hesitantly, puzzled rather than informed about its meaning.",
81:"In an alternative introduction Rafael remembers Julio had something to do and asks what it is.",
86:"Julio answers that he is going to investigate 覇者の証.",
92:"Rafael asks what 覇者の証 is.",
97:"Julio says finding that out is precisely what he is going to investigate. Preserve the mildly evasive/comic reply.",
101:"Rafael is visibly confused: two question marks, a brief reaction rather than an invented spoken explanation.",
106:"Julio tells him to wait a little; he will be back soon.",
109:"Rafael gives a hesitant, not fully comprehending acknowledgment.",
116:"Rafael notices something: a quiet pause, then surprise and curiosity about what he sees.",
121:"The departure-office man reacts impatiently and says there is no ship that conveniently meets the request; try somewhere else.",
125:"The older man says a place on deck or in the hold, anywhere, will do. He wants passage to some faraway country.",
129:"The departure-office man objects that at his age he probably could not even scrub the deck. This is the man's dismissive judgment, not an established inability mechanic.",
132:"The older man appeals again and asks him not to say that.",
136:"Rafael politely interrupts to ask whether something is wrong.",
140:"The older man identifies Rafael as a sailor from a ship that has just entered port and asks apologetically whether he can take him aboard.",
144:"The departure-office man advises the captain against it: this old man is asking for free passage. 艦長 is the addressed captain; じいさん is not evidence of kinship.",
148:"Rafael confirms that the man wants to go on a voyage and considers what to do.",
152:"Claudio protests at taking aboard so many old men, an exaggerated complaint in the exchange, not an invented family relationship.",
155:"The older man falters and asks if it is no after all.",
159:"Rafael asks to hear the reason first and says they will decide afterward, showing considerate judgment rather than immediately refusing.",
164:"The older man introduces himself as ハンス・レッツェル, a researcher in natural history.",
167:"Hans says the entire world is the subject of his research and urgently begs them to show him the world.",
171:"Claudio is briefly silent. Preserve the pause before his reversal.",
175:"Rafael acknowledges that he understands the reason.",
180:"Claudio suddenly exclaims that this is admirable, reversing his earlier complaint.",
184:"Rafael asks Clau's name in surprise at this reaction.",
189:"Claudio admires Hans for driving his aged body to brave dangerous seas in order to complete his own research. He praises the determination and says he respects him; the whip idiom is figurative.",
192:"Rafael agrees somewhat taken aback, then warmly invites Hans aboard.",
197:"Hans asks if this is really all right and expresses gratitude.",
200:"Hans addresses the admiral politely and asks one more favor on top of the imposition. The source explicitly uses 提督殿 here; do not infer a rank from unrelated honorifics.",
204:"Rafael asks what the request is.",
209:"Hans hesitates, then asks for one companion to come aboard too.",
212:"Rafael is puzzled again, with a short question-mark reaction.",
217:"Hans says this is his assistant, a promising... young man, with hesitation and a throat-clearing beat, and asks アルカディウス to introduce themself. Preserve the presented identity and awkward delivery without explaining a concealed identity.",
221:"The assistant politely introduces the name アルカディウス・エウドシオス and asks to be treated well/looks forward to working with them.",
232:"In a private aside Janus reacts that the newcomer has a delicate/slight build. Do not turn it into a factual health diagnosis, contemptuous slur or revealed identity.",
236:"In a matching aside Claudio says Janus is one to talk, but agrees that even Janus starts to look sturdy by comparison.",
239:"Rafael clears his throat to interrupt the private exchange; do not invent a spoken reprimand.",
247:"Hans resumes praising the assistant as a promising... young man in more than an academic attitude. Preserve the hesitant wording and suggestion without supplying an unsupported explanation.",
250:"The assistant says they have studied a little about navigation but still expects to need everyone to teach them many things.",
254:"Rafael asks the newcomer not to worry or think too hard about it: they are only getting started themselves. Reassuring welcome, not a claim of veteran expertise.",
258:"The assistant says that hearing this is reassuring.",
262:"Hans exults that everything is going well and this is the start of a splendid voyage.",
273:"Janus thinks it looks as though this will be an enjoyable voyage.",
280:"Rafael tells Clau it is reassuring to have such a learned scholar with them.",
284:"Claudio agrees, urges the doctor to do his research properly, then pointedly adds the assistant. Preserve the extra beat without inventing romance or hostility.",
288:"Hans responds enthusiastically that they can leave it to him.",
292:"The assistant gives another restrained, polite acknowledgment and looks forward to working with them.",
296:"Julio calls out from a distance.",
300:"Rafael recognizes Julio on his return.",
305:"Julio is surprised to find the person he sought here.",
308:"Hans recognizes Julio with delighted surprise.",
312:"Julio recognizes Hans and says he has been looking for him.",
316:"Claudio is confused by the recognition.",
320:"Rafael is very surprised that this was the person Julio had been looking for.",
324:"Julio explains that Hans is an acquaintance who has researched 覇者の証 for many years. 知り合い does not establish relatives, a mentor relation or a lifelong close friendship.",
327:"Hans asks whether they too are interested in 覇者の証.",
331:"Rafael says interest is beside the point: he still does not know what 覇者の証 is and asks for an explanation.",
336:"The assistant explains that they are treasures scattered through the sea regions and are said to come into the hands of those who rule the seas. Preserve hearsay and the plural regional treasures.",
339:"Hans says the details remain mysterious, but it appears that a lead to finding the treasures may be emerging. Do not turn a prospect into a solved location.",
343:"Julio excitedly asks whether Hans has figured it out.",
347:"Hans cites an ancient document: seven treasures in all, with the ancient Seven Sages marking the places where they were to be sealed on maps of various shapes. Preserve source attribution and all seven, not a generic lost-map legend.",
350:"Hans continues that someday those destined to rule each sea are to obtain its map. This is the document's reported destiny, not an established gameplay guarantee for the current crew.",
354:"Rafael realizes what it would mean if they collected them through their own efforts; the thought trails into excitement.",
358:"Julio confirms that they would truly be rulers of the world's seas in both name and substance.",
361:"Rafael quietly repeats the idea of ruling the seas, absorbing the new ambition.",
366:"Rafael resolves enthusiastically that they should do it and win them through their own efforts.",
370:"Claudio says {MACRO:FI} is always the first to get excited. He does not fully understand yet, but says they need to see this proof/sign before anything else. Preserve the source FI substitution and the teasing practical response.",
379:"In one stored alternative Rafael affirms that he will certainly find them. This is personal determination, not a system promise.",
385:"In another alternative Rafael declares that he will find them and someday challenge Hayreddin as well. Keep this future challenge distinct from present hostility or an already completed confrontation.",
389:"The assistant reacts in surprise to the mention of Hayreddin.",
393:"Hans is astonished and wonders whether he has joined quite an extraordinary/formidable ship; preserve the lightly comic question rather than declaring regret or certainty of disaster.",
396:"Julio chuckles that it is too late to realize that now: this admiral/captain fears nothing. The source explicitly uses 提督さん; preserve amused affection, not literal invulnerability.",
403:"Hans reflects approvingly that being young is a good thing.",
406:"Hans says he recently heard a rumor that someone took one of the 覇者の証 maps to the south of Africa. Do not invent that person's identity, a specific city or a precisely located treasure.",
409:"Rafael asks whether this is really true.",
414:"Hans does not know whether the rumor is true, but thinks that if they go to Africa they may pick up some information.",
418:"Rafael accepts the lead and proposes heading to Africa.",
427:"System announcement: natural-history doctor/scholar Hans Retzel has joined the party. The proper name's English spelling is still to be checked against approved names.",
431:"System qualification: Hans is not a navigator, so he cannot be assigned on the deck screen. Preserve this exact limitation rather than claiming he cannot board the ship or perform any useful role.",
435:"System explanation: having Hans now enables detailed item information to be viewed.",
438:"System instruction: try pressing X while item information is displayed. Preserve X and the context; do not substitute Y/another screen.",
441:"Hans says he cannot do the ship's work but asks them to look after him, and invites them to call him if they want to know about items.",
}

def section(index):
    if index<=61:return 'Athens/conditional crew banter before Julio leaves'
    if index<=109:return 'Julio investigation setup and unanswered-term joke;alternative introduction requires branch proof'
    if index<=159:return 'Older traveler refused free passage;Rafael hears the reason before judging'
    if index<=197:return 'Naturalist introduction andpassion;Claudio reverses from complaint to admiration'
    if index<=292:return 'One more favor;assistant introduction,hesitant characterization,private asides,welcome'
    if index<=331:return 'Julio returns;Hans recognition andacquaintance revealed;Rafael still needs explanation'
    if index<=370:return 'Seven regional treasures/maps,source-attributed legend andRafael developing ambition'
    if index<=403:return 'Exclusive determination/Hayreddin variants andlight comic response;branch proof pending'
    if index<=418:return 'Uncertain rumor,possible African information andchosen direction'
    return 'Four distinct system panels andHans item-information role;X instruction'

if __name__=='__main__':
    assert not ROOT.exists()
    source,names=map(read,[SOURCE,NAMES]);g=source['groups'][0]
    assert not source['inventory_failures'] and len(g['records'])==91 and len(g['commands'])==163
    assert all(r['current_English_body_unread'] and not r['already_contextually_completed'] and not r['source_decode_error'] for r in g['records'])
    assert {r['source_record_index'] for r in g['records']}==set(GLOSSES)
    fields={r['source_actor_ID']:[f.get('text') for f in r['fields']] for r in names['records']}
    rows=[]
    for original in g['records']:
        row=deepcopy(original);index=row['source_record_index']
        row.update(source_gloss=GLOSSES[index],speaker_source_identity_fields=fields.get(row['source_selector']),
            full_clean_exchange_context=section(index),
            source_gloss_not_current_English_derived=True,source_gloss_mode='fresh-clean-Japanese-whole-exchange-intent',
            all91_clean_speeches_and163_commands_read_ascomplete_exchange=True,
            literal_proper_name_fields_bound_without_approving_all_current_consumers=True,
            source_native_predicate_branch_caller_controls_anddisplay_review_pending=True,
            source_prose_orcompletion_credit_added=False)
        rows.append(row)
    ROOT.mkdir(parents=True)
    save(ROOT/'91_fresh_clean_glosses_nine_source_identities_before_current_English.json',dict(
        source_packet=str(SOURCE),source_packet_sha256=sha(SOURCE.read_bytes()),
        source_name_packet=str(NAMES),source_name_packet_sha256=sha(NAMES.read_bytes()),records=rows,
        source_event_records=g['source_event_records'],source_event_dependencies=g['source_event_anddependencies'],
        all91_glosses_fresh_before_current_English_exposure=True,
        complete_clean_exchange_read_before_current_English=True,
        no_external_historical_biography_orconcealed_identity_revelation_invented=True,
        source_legend_uncertainty_seven_maps_sages_future_ambition_andAfrican_rumor_preserved=True,
        source_Hans_not_a_navigator_deck_assignment_limit_andX_item_information_instruction_preserved=True,
        exact_source_FI_atR370_preserved_as_runtime_substitution=True,
        source_Julio_setup_andHayreddin_variants_require_native_branch_proof=True,
        current_English_bodies_names_getters_andlocalization_still_pending=True,
        new_credit=0,new_emulator_runs=0,
        evidence={str(p):sha(Path(p).read_bytes()) for p in [SOURCE,NAMES,Path(__file__)]},full_goal_complete=False))
    print('91 clean B48 intent glosses frozen before current English;163commands/nine source identities/fourFE panels. Branch/getter/current/native/actual/release pending;zero credit.')
