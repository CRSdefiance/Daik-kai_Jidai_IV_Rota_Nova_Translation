"""Read three complete clean exchanges before consulting any existing English."""
from copy import deepcopy
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load,save

ROOT=Path('work/analysis/Rafael_B61_B80_clean_20261104')
MEANINGS={
61: '''
12|Kuhn bitterly laments losing the jar/vessel to people he considers beneath him;the object is source壺,not an invented named treasure.
15|Kuhn curses andtells the victors to remember this,threatening that he will not forget the defeat.
22|Kuhn cannot believe that he himself has fallen to such opponents when he was so close to his goal.
27|Pereira enthusiastically praises Admiral FA for a job well done.
31|Rafael modestly says they somehow managed it andthanks Governor Pereira.
42|Pereira casually says it is all right/no trouble;the surrounding conditional commands must distinguish this occurrence from the later identical reply.
64|Pereira again casually says it is all right/no trouble in a separate source occurrence,not an additional chronological reply inferred from numerical order.
75|Pereira says he will stop quibbling over details andurges Rafael to follow his own judgment anddefeat Spain or whatever other opponent stands before him.
78|Rafael emotionally addresses the governor,trailing off.
83|Claudio warmly exclaims that the older man is a good guy;the familiarおっさん does not establish kinship.
94|Pereira laughs uproariously andboasts that Governor Pereira of Indochina is always a good guy;the self-important title is a deliberate part of his joke.
107|In an alternative longer boast,Pereira laughs about being the good Governor of Indochina andhands something to Admiral FA,telling him to take it.
113|A system notice announces the surprisingly large receipt of500000 in military funds from Governor Pereira;preserve the exact amount andpurpose.
122|Rafael reacts with an extended astonished cry.
129|Janus expresses considerable polite surprise at the gift.
136|Claudio roars with delight,praising the governor's extraordinary generosity.
147|Jam gives an extended exuberant cheer.
154|Rafael cannot believe the size of the gift andasks whether it is really all right to take so much.
158|Pereira cheerfully confirms that it is all right,urges them to do their best andsays he is counting on them.
161|Rafael answers with a spirited affirmative.
''',
62: '''
5|Actor179 respectfully addresses FA,says he is worthy to rule the seas of this continent andasks him to accept the offered object;this praise does not establish a new formal royal rank.
10|Rafael wonders whether the object might be connected to the Proof,leaving the phrase excitedly unfinished.
15|Rafael thanks the giver,then notices something unexpected.
19|Claudio remarks that the giver has already left.
23|Rafael observes that the object looks like a sword scabbard butcontains no blade andwonders what that means.
34|Rafael wonders whether this too is a key to deciphering the map to the Proof of Conquest.
40|In the companion alternative,Arcadius confidently identifies this too as a key to deciphering the Proof of Conquest map.
46|Claudio agrees enthusiastically anddeclares that the New World's treasure is theirs for the taking.
''',
63: '''
5|Claudio asks FI for a moment andrequests that he come to the inn.
9|Rafael is mildly puzzled butagrees.
14|Claudio starts by insisting that Rafael show the other person some consideration.
18|Rafael does not understand what Claudio means.
22|Claudio names Eirene andreminds Rafael that he recently made her help with physical labor.
25|Rafael defends himself by saying it was only a little work.
30|Claudio angrily says that is beside the point:Eirene is not as physically robust as the others,so Rafael ought to be considerate.
34|Rafael hesitates andsays there were circumstances behind what happened.
38|Claudio retorts that circumstances do not justify absolutely anything.
41|Rafael protests that Claudio does not need to get so angry.
46|Claudio bristles,tells Rafael to do as he pleases andleaves in anger.
52|Arcadius notices FI andpolitely asks what is wrong.
55|Rafael recognizes Arcadius andevasively says it is just something minor.
60|Arcadius says Claudio seemed to be shouting earlier,leaving room for Rafael to explain.
63|Rafael privately worries,then asks whether Arcadius also heard what the argument was about.
67|Arcadius says no,not that much.
71|Rafael hesitantly asks whether they can talk for a moment.
75|Arcadius agrees tentatively.
79|Rafael privately addresses Eirene andadmits that the argument was about her.
84|Eirene is surprised that they were discussing her.
88|Rafael says Clau is angry about the recent time Eirene helped with heavy work.
92|Eirene recalls that nobody else was available andexplains that,because everyone is supposed to think she is a man,it would have looked strange for her to refuse the work.
95|Rafael says that he gave the same explanation,that there had been no choice,butClaudio was still furious.
100|Eirene pauses silently before responding;do not invent a spoken explanation.
104|Rafael complains that Clau simply shouted his own views andstormed out without listening.
108|Rafael feels hurt because he believes he is trying to think about Eirene too.
113|Eirene apologizes that concealing the fact that she is a woman has put FI in a difficult position;the source explicitly establishes the concealed identity here.
117|Rafael denies that she has caused him trouble,apologizes for venting andasks her not to worry about it.
122|Eirene gently tells FI that she thinks he is working very hard as admiral.
126|Eirene says they can all feel safe aboard the ship because of him.
130|Rafael is embarrassed by the sudden praise andasks Eirene what brought it on.
134|Eirene says nothing is wrong;because she values his efforts,she does not want FI to push himself too hard.
138|Rafael softly addresses Eirene,moved by her concern.
143|Eirene tells him not to worry alone:talking to someone,even just to complain,can ease the burden.
146|Rafael says Eirene is like an older sister;this is an explicit comparison,not a newly established family relationship.
150|Eirene asks whether he thinks so.
154|Rafael agrees that he does feel better than before andthanks her for listening.
159|Eirene says she should be the one apologizing for the trouble she has caused him.
162|Rafael explains that he has never quarreled so badly with Clau before anddoes not know what to do;he returns to asking how to handle it.
166|Eirene says Claudio will probably be fine andwill likely forget the argument after he eats.
170|Rafael asks whether that is really so.
175|Eirene confidently says Claudio is simple in that way andsuggests that they have a meal.
179|Claudio cheerfully greets FI andasks whether he ate enough.
182|Rafael awkwardly answers yes andaddresses Clau,unsure what to say.
186|Claudio asks why Rafael is making such an odd face.
189|Rafael stammers that he was just thinking Claudio seems in a good mood.
193|Claudio is briefly puzzled,then dismisses it andsays he will go ahead.
197|Rafael realizes that Eirene was right:Claudio has completely forgotten the quarrel.
202|Rafael marvels at how well Eirene understands Clau andnaively wonders whether it is because she is a scholar;preserve the comic uncertainty rather than supplying a romantic explanation.
'''}
CONTEXT={
61:'Complete aftermath of the Kuhn struggle andPereira farewell/gift. Conditional occurrences andshort/long donation alternatives remain separate until exact EV0/branch binding. Military funds are500000;the governor self-title is voiced by Pereira himself. The older-man address is familiar,not a family relationship.',
62:'Complete mysterious-giver/scabbard exchange ending with an explicit New World treasure reference. Rafael andArcadius have alternative map-key conclusions. The empty scabbard andits relation to the Proof remain questions as stated;do not invent the missing blade or giver biography.',
63:'Whole inn argument,reassurance andmeal payoff. Source switches from public Arcadius address to private Eirene address andexplicitly states the concealed female identity andcrew assumption of a man. Preserve public speaker controls;do not globally rename Arcadius. Claudio concern,Rafael defensiveness,Eirene reassurance andthe naive scholar joke form one emotional progression. The older-sister phrase is a source simile,not kinship;no romance is supplied.'}

if __name__=='__main__':
    output=ROOT/'B61_B63_77_clean_meanings_v1.json';assert not output.exists()
    packet_path=ROOT/'clean_source_packet.json';packet=load(packet_path);records=[]
    for group in packet['groups'][:3]:
        number=group['block'];assert number in MEANINGS
        meanings={int(k):v for k,v in (line.split('|',1) for line in MEANINGS[number].strip().splitlines())}
        assert len(meanings)==len(group['records']) and set(meanings)=={r['source_reference']['record_index'] for r in group['records']}
        for original in group['records']:
            row=deepcopy(original);assert row['source_decode_error'] is None and row['earlier_English_unconsulted']
            row.update(source_meaning=meanings[row['source_reference']['record_index']],whole_exchange_context=CONTEXT[number],
                source_read_with_all_previous_andfollowing_speeches_in_block=True,
                clean_name_event_membership_current_comparison_drafts_andall_five_gates_pending=True)
            records.append(row)
    assert len(records)==77
    save(output,dict(source_packet=str(packet_path),source_packet_sha256=sha(packet_path.read_bytes()),records=records,
        complete_exchanges=[61,62,63],all77_source_meanings_read_as_complete_exchanges_before_existing_English=True,
        source_B63_explicit_private_Eirene_identity_not_a_global_header_rename=True,
        all_five_editorial_gates_still_pending=True,source_gloss_not_final_English=True,new_credit=0,
        guide_photos=False,producer_sha256=sha(Path(__file__).read_bytes())))
    print('77 source-only meanings/three complete exchanges sealed;no old English read,no completion credit.',flush=True)
