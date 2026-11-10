"""Preserve the whole village exchange andits cultural/emotional progression,source first."""
from copy import deepcopy
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load,save
from scripts.gloss_rafael_B61_B63_clean import ROOT

MEANINGS='''
5|Rafael is surprised to discover that there is a village even in this remote place.
9|Claudio finds the village forlorn andlacking any sense of bustle or vitality.
12|Rafael notices,on closer inspection,that ships from other countries are also docked there.
17|Rafael hears a commotion in the distance.
21|Claudio thinks something has happened.
25|Rafael urges them to go andsee.
31|The village woman protests that the buyer previously promised to pay more.
35|The sailor dismisses the earlier promise andsays he will not pay a penny more for today's goods.
39|The woman demands to know what is wrong with the goods,saying she selected the village's best.
43|The sailor contemptuously repeats her claim that these are the village's best.
47|The sailor calls the construction flimsy,says the goods do not deserve a proper price androughly handles/damages them.
51|The woman orders him to stop andthreatens consequences if he breaks anything else;the villagers worked hard to make these goods.
55|The sailor cries out in pain andangrily demands what the woman thinks she is doing.
58|The woman cries out as the encounter turns violent.
62|Rafael orders the sailor to stop,condemning a man for striking a woman;preserve the character's expressed objection without adding a new relationship.
67|Claudio offers to fight the sailor himself.
71|The sailor clicks his tongue in annoyance.
75|Claudio scornfully notes that the sailor has run away.
79|Rafael asks the woman whether she is all right.
84|The woman remains silent.
88|Claudio condemns the treatment of the girl andasks whether the sailor was picking a quarrel ormaking false complaints.
91|Rafael tentatively asks whether the things are for sale andoffers to buy them as a favor;if localized English loses this patronizing shade,the following offended response will no longer follow.
95|The woman sharply echoes the qualifying words in Rafael's offer,offended by his attitude.
98|She asks what a sheltered young gentleman like him could understand andrejects his pity.
102|Claudio angrily complains that,instead of thanking them for helping,she criticized them.
106|Rafael wonders whether their manner really upset her so badly.
111|Claudio insists that their attitude does not justify her complaints,because they did save her.
114|Rafael calms Clau andsuggests a meal andchange of mood,joking that getting angry makes him hungry.
119|Janus considers the account of what happened.
123|Claudio says it makes him furious andcalls the woman outrageous.
126|Rafael takes responsibility:in hindsight,his offer to buy as a favor may have sounded as though he were looking down on her.
130|Rafael admits he did pity her andthinks her anger understandable;he worries that he hurt her anddoes not know what to do.
134|Arcadius gently advises FI not to dwell on what has already happened.
138|Arcadius says that once one recognizes a mistake,one should take care not to repeat it.
141|Janus agrees andpraises FI's usual instinct to reach out to people in trouble.
144|Janus says the approach was clumsy this time buthe is sure the girl understood that Rafael meant no harm.
147|Rafael thanks his companions.
152|Claudio protests that she insulted them without even thanking them,andstarts insisting that FI was not the one at fault.
155|Claudio gives up the argument andgrumbles that everyone aboard is impossibly softhearted;his irritation is affectionate exasperation rather than proof of a betrayal.
158|Claudio sighs contentedly after eating his fill.
162|The woman hesitantly calls for their attention.
166|Rafael is surprised to see her.
171|Claudio recognizes her andcalls her the rude woman from earlier.
174|She hesitantly says she would,in fact,like Rafael to buy the goods.
177|Claudio objects that she is going too far andreminds her that she was the one who so forcefully refused.
181|She quickly says she is not trying to force them.
184|Claudio says that goes without saying andasks FI what he intends to do.
187|Rafael says he will decide after inspecting the goods andasks her to bring them to the port office.
191|She thanks him andeagerly agrees to come if he will look at the goods.
194|Rafael warns that he might not be able to meet her expectations.
198|She says not to worry:trying costs her nothing andshe is prepared for rejection.
202|She falters andhesitates before saying something more personal.
206|She blurts out an apology for earlier.
210|Rafael reacts in surprise.
215|She quickly says she will see them later andleaves.
219|Janus realizes that she is a good-hearted girl underneath.
222|Arcadius chides Clau for calling such a girl a rude woman.
225|Claudio insists that she was the one who behaved badly,insulting them after they saved her.
229|Claudio contrasts her earlier rejection of pity with her request to buy andcalls it shameless.
232|Arcadius says her behavior shows courage,not shamelessness.
235|Janus describes her red face andtrembling body:she set aside her pride to ask for help for her family andfellow villagers;those family ties are explicit in this source.
239|Rafael quietly says she is a good person.
244|Claudio begins to understand.
248|Claudio enthusiastically proposes that they hurry andprepare to unload their cargo.
252|Rafael notes that Claudio is getting ahead of things:they have not even negotiated the sale yet.
256|Claudio says FI does not really care about inspecting the goods either andurges him to buy the whole lot.
260|Rafael stammers Clau's name in surprise at his sudden enthusiasm.
265|Janus calls Claudio forceful butfondly says that this straightforwardness is one of his good qualities.
269|Arcadius warmly agrees.
274|Rafael confirms that the deal is settled.
279|The woman thanks him,saying she can now report back properly tothe village andeveryone will be happy.
283|Rafael realizes they have not exchanged names,introduces himself as FI andasks hers.
287|She repeats FI's name andintroduces herself as Charlotte,sourceシャルロット;final English spelling still needs exact name binding.
290|Rafael asks Charlotte why her people deliberately established a village on such poor land.
295|Charlotte explains that her people were traveling Romani/Gypsy people,sourceジプシー,andused to move throughout Europe;settling does not imply that their ethnicity ceased.
298|She remembers walking as hard as she could while holding her mother's hand.
301|At one point,someone approached them with the idea of emigrating to the New World.
305|They were told the New World held mountains of gold andvast untouched fertile lands;these are the promoter's promises,not narrator-verified facts.
309|The group discussed the proposal,pooled what little money they had anddecided to cross the ocean.
313|Her father,mother andthe others were initially full of hope that they could have land anda village of their own.
316|Their hope soon turned to despair.
319|They learned that digging at random would not reveal gold mines;all they could see was barren wilderness.
322|Rafael condemns the people who took their money byluring them with enticing promises.
326|Despite their despair,the group encouraged one another anddecided to build a village.
330|Because they had never owned land,they struggled to grow crops;conditions had been difficult ever since their arrival.
333|Rafael naively asks whether such hardship made them consider returning to their country.
337|Charlotte questions the word country:her Romani people have no country of their own andnowhere they can return to.
340|She describes the prejudiced accusations they faced:missing possessions were blamed on them andepidemics were blamed on them. These are reported scapegoating claims,not factual generalizations about Romani people.
343|She says that wherever they went in Europe,people looked at them with disgust as though they were something filthy.
347|Rafael falls silent,taking in what she has told him.
352|About two orthree years earlier,their crops finally succeeded andthey became self-sufficient;at last they had a village of their own. Preserve both the approximate date andthe hard-won belonging.
355|About a year earlier,a ship happened to visit andthey began obtaining new goods through barter.
358|She adds that they are often forced to sell for next to nothing,as happened earlier,butfeels they have little choice.
363|Charlotte admits that she was actually very happy when FI came to her aid.
367|She had never expected that anyone would help her.
370|Rafael addresses Charlotte andtries to apologize for hurting her when he first spoke to her.
375|She recognizes that he meant well andsays she should have thanked him for saving her.
379|She asks whether he will come back to the village.
383|Rafael readily promises that he will.
388|She asks whether he truly means it.
392|Rafael explicitly promises.
397|She insists that he keep his promise andsays she will wait for him.
401|Rafael says they will see each other again.
406|She calls after him to remind him of the promise.
410|Rafael watches her leave,then is surprised to notice Clau nearby.
414|Claudio is openly moved andsays the story makes him cry.
418|Arcadius sympathizes with how the villagers suffered both in Europe andthe New World.
422|Rafael is surprised that Arcadius was also listening.
427|Arcadius apologizes,explaining that he did not intend to eavesdrop butbecame concerned/interested.
439|Rafael recalls feeling as though he would lose his own place in the world when Portugal seemed likely to be annexed by Spain;preserve the impending threat in his recollection.
444|He contrasts his experience with their having had no place to belong from birth.
451|Claudio urgently asks FI whether there is anything they can do.
455|Arcadius proposes that they consider ways to help the village develop,something useful someday even if they cannot help immediately.
458|Rafael agrees that they should do so.
462|Rafael pauses silently.
467|Rafael quietly repeats Charlotte's name to himself.
472|Arcadius remarks that she was a very sincere andlovely girl.
476|Claudio agrees.
480|Rafael quietly agrees.
485|Rafael privately wonders what they can accomplish with their own hands;this remains an open question rather than a newly invented mission objective.
'''

if __name__=='__main__':
    output=ROOT/'B64_120_clean_meanings_v1.json';assert not output.exists()
    packet_path=ROOT/'clean_source_packet.json';packet=load(packet_path)
    group=next(g for g in packet['groups'] if g['block']==64)
    meanings={int(k):v for k,v in (line.split('|',1) for line in MEANINGS.strip().splitlines())}
    assert len(meanings)==len(group['records'])==120 and set(meanings)=={r['source_reference']['record_index'] for r in group['records']}
    rows=[]
    context=('Complete120-speech village incident andreturn:violent low-price buyer,patronizing rescue offer,offended dignity,companions correcting Claudio,her difficult apology,Claudio changing his mind,an ordinary trade,andthe settlement/migration account. '
        'Preserve the Romani identity inジプシー rather than erasing it to generic nomads;represent theft/disease accusations as prejudice she reports,not endorsed facts. '
        'Source explicitly includes her parents,family andvillagers,butno romantic relationship with Rafael. Promises of gold/fertile land are reported deceptive recruitment. '
        'Dates remain approximate:two orthree years to self-sufficiency,aboutone year since ship/barter contact. Rafael connects their lack of a homeland with the threatened annexation of Portugal. '
        'Final proper-name/header/event bindings andall localized English remain pending;no older English was consulted.')
    for original in group['records']:
        row=deepcopy(original);assert row['source_decode_error'] is None and row['earlier_English_unconsulted']
        row.update(source_meaning=meanings[row['source_reference']['record_index']],whole_exchange_context=context,
            source_read_with_all_previous_andfollowing_speeches_in_block=True,
            clean_name_event_membership_current_comparison_drafts_andall_five_gates_pending=True)
        rows.append(row)
    save(output,dict(source_packet=str(packet_path),source_packet_sha256=sha(packet_path.read_bytes()),records=rows,
        complete_exchanges=[64],all120_source_meanings_read_as_complete_exchange_before_existing_English=True,
        cultural_context_preserved_with_reported_prejudice_attributed_to_its_speakers=True,
        all_five_editorial_gates_still_pending=True,source_gloss_not_final_English=True,new_credit=0,
        guide_photos=False,producer_sha256=sha(Path(__file__).read_bytes())))
    print('120 source-only meanings/full village exchange sealed;Romani context,reported prejudice,trade dignity anddates preserved;no credit.',flush=True)
