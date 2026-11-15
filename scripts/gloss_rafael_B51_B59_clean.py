"""Record source-only meanings for nine whole exchanges before consulting old English."""
from copy import deepcopy
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from scripts.audit_story_glyph_consistency import load, save

ROOT = Path('work/analysis/Rafael_early_story_B36_B41_B51_B60_clean_20261104')
MEANINGS = {
51: '''
6|Rafael finds the place quiet and restful and decides to do something he has not done in a while;the thought trails off.
18|Rafael notices something,internally asking what it is.
24|The woman smiles;this is a written gesture rather than a spoken greeting.
28|Rafael is puzzled and privately wonders who she is.
32|A silent interval indicated by an ellipsis in a system-style panel.
37|Hodram calls Sera by name.
41|Rafael reacts to the voice.
46|Sera recognizes and addresses Hodram.
50|Hodram asks who Rafael is,starts asking whether she knows him,then dismisses that possibility.
54|Rafael remains silent.
59|Hodram gives a thoughtful noncommittal response.
63|Sera questions Hodram's reaction by addressing him.
67|Hodram tells Sera they are leaving.
71|Sera agrees.
75|Rafael reflects that she was beautiful and wonders which country's princess she might be;this is his speculation,not an established rank.
86|Rafael thinks he recognizes the military man beside her as someone from the Swedish navy;the recollection trails off.
''',
52: '''
5|A local asks whether Rafael belongs to FO.
9|Rafael confirms,with some puzzlement.
14|The local says that is what they thought.
18|Admiral Albuquerque of Portugal's regular armed forces asked the local to tell Rafael to return home to Lisbon if they saw him.
21|Rafael wonders what the regular armed forces want with them.
31|The rough-spoken companion says there is no helping it and asks whether they should return for now.
36|The more formal companion gives the same practical suggestion to return for now.
''',
53: '''
6|The rough-spoken companion reminds the admiral that Portugal's regular armed forces have summoned them and asks what he intends to do.
10|Rafael decides they should go and confirms that they need to visit the palace.
14|The companion confirms.
''',
54: '''
5|A local calls for Rafael's attention and asks whether he has heard the news.
9|Rafael asks what they mean.
14|The local reports that Fernan Silveira has defeated the notorious Espinosa.
18|Rafael ruefully notes that this is how the story is being told.
23|The local finds his response confusing,then says Silveira is at least preferable to Espinosa,who did nothing but harm.
26|Rafael hesitantly concedes that may be true.
31|The local says the governor's office is apparently being moved to Sofala.
35|Rafael is startled that the African governor's office is moving to Sofala,says he must go,and thanks the older local;the address does not establish kinship.
40|The local calls after him,then wonders what that was all about.
''',
55: '''
5|Silveira greets FI warmly and commends his efforts.
8|Rafael recognizes Admiral Fernan and privately marvels that he has already arrived.
12|Silveira praises their accomplishments,claims he has already reported to His Excellency Albuquerque,and tells them not to worry.
15|Rafael gives an uncertain acknowledgment.
20|Silveira claims he refused,but His Excellency insisted.
24|Silveira announces that he has been appointed governor of Africa and laughs grandly.
28|Rafael is shocked.
36|System notice:Silveira's company has taken all their market share in Sofala.
40|Silveira calls it luck,tells Rafael not to hold it against him,and laughs.
44|Silveira says this is their reward from Albuquerque,and says a gift to celebrate his appointment is unnecessary because he has already deducted it from their reward.
47|Silveira adds that if they insist,he would gladly accept a separate additional gift,and laughs.
54|System notice:they received 3000 gold coins,with a rueful trailing ellipsis.
58|Rafael realizes they have been outmaneuvered and reacts with frustration.
63|Rafael wonders whether Commander Albuquerque really decided this.
67|The blunt companion says Silveira must have pressed for it and probably gave a false report to take all the credit for defeating Espinosa;this is the companion's inference.
78|The formal companion is astonished by Silveira's scheming and tells Admiral FI that surely this cannot be tolerated.
90|The rough-spoken companion tells the admiral that their next target is settled.
95|Another,more measured companion remarks that their next target is now decided.
102|Rafael responds in surprise.
115|A fiery companion says Silveira has made him take this seriously.
121|The rough-spoken companion says they cannot simply stay quiet about this.
132|A boisterous companion declares that even if God forgives Silveira,he will not,and cheers.
138|The blunt companion proposes that they go after him.
142|Rafael agrees hesitantly;he dislikes fighting fellow Portuguese,but dislikes backing down now even more.
154|A woman in the crew declares she will never forgive Silveira.
168|An older companion grumbles about having to push his aging body,then urges FI that they should give this their best;the familiar address does not establish kinship.
174|The rough-spoken companion urges them to beat Silveira and put him in his place.
178|Rafael thanks everyone and resolves to conquer Africa.
182|The blunt companion calls for them to get going.
186|The rough-spoken companion shouts agreement.
''',
56: '''
5|A local recognizes Rafael as the head of FO.
9|Another local says his arrival is timely and calls for his attention.
12|Rafael checks whether they mean him and asks what they need.
17|The second local says life has improved considerably since Espinosa and Silveira ruled the area unchecked.
21|The first local agrees and credits Rafael's organization.
24|Rafael is modest and embarrassed by the praise.
28|The second local says corrupt merchants had held sway for so long that people almost forgot how to trust others.
32|The first local agrees,then recalls the real reason for stopping him.
36|Rafael gives a tentative acknowledgment.
41|The first local urges him to pay attention and hands him something.
46|Rafael asks what it is.
58|The thoughtful companion suspects a connection to a Proof of Conquest;the sentence is left unfinished.
62|Rafael stammers and asks where they obtained it.
66|The first local says an adventurer had been trying to sell it to Espinosa for a high price.
69|The second local condemns the idea of making money by telling a devil like Espinosa where the Proof of Conquest is.
72|Rafael uncertainly asks whether he may really have it.
77|The first local explains that the townspeople pooled their money and pressed the adventurer to sell it,so that they could give it to Rafael.
81|Rafael thanks them earnestly.
89|The first local confirms it is now in his hands and urges him to keep working for everyone's sake.
92|Rafael agrees enthusiastically.
97|The second local says they are counting on him.
''',
57: '''
5|Emilio cries out as he falls or is hurt;the cause is explained in the following exchange.
10|Rafael is alarmed and asks Emilio whether he is all right.
14|The blunt companion notices the pier was rotten.
17|Emilio cries that it hurts.
22|Arcadius asks to examine the injury.
26|Emilio says it hurts again.
30|Arcadius advises against moving the injured part much and says Emilio should rest at the inn.
33|The blunt companion reluctantly helps Emilio,telling him to hold on,then exclaims at how heavy he is.
40|Rafael is relieved that Emilio's injury was not serious,then notices Arcadius.
45|The blunt companion wonders why Arcadius is buying flowers.
48|Rafael notes that Arcadius also has fruit.
53|The blunt companion wonders whether it is someone's birthday today.
57|The blunt companion greets Arcadius and asks whether a party is planned.
60|Arcadius is puzzled.
64|The blunt companion mentions seeing the flowers and appetizing food and eagerly asks to eat some.
68|Arcadius explains that those are gifts for visiting the injured Emilio,not a party.
71|Rafael asks why Emilio would need that.
76|Arcadius reacts with mild exasperation at the question.
80|Arcadius thinks Emilio must be bored,unable to go out even though they are in town,and says that is why a visit is in order.
83|The blunt companion gives a noncommittal response.
87|Arcadius knows Emilio likes sweets,and does not know whether he likes fresh flowers,but notes that flowers cannot be obtained at sea.
91|The blunt companion absorbs this and tentatively asks whether Arcadius would visit him too if something happened to him.
95|Arcadius says of course,as they are companions.
99|The blunt companion agrees awkwardly and repeats himself.
103|The blunt companion denies there is anything more to it and tells Arcadius to go on in to Emilio.
106|Arcadius invites Claudio to come in too,teasing gently that he may get to eat some delicious fruit.
109|Claudio declines and says to give it all to Emilio,who will surely be happy.
113|Arcadius accepts his decision,slightly hesitantly,and takes leave to go inside.
116|Arcadius asks whether Emilio's leg still hurts and offers the gifts.
119|Emilio is delighted by the food,thanks Arcadius,and asks whether Arcadius knew he loves flowers.
122|Arcadius did not know,but is glad Emilio likes them,and encourages him to eat plenty.
126|Emilio cheers.
132|Arcadius begins calling Claudio by name,then asks whether he waited.
135|Claudio admits it awkwardly and suggests that they rejoin everyone else and get moving.
139|Arcadius agrees after a pause.
143|Claudio is silent;the source does not state a confession,romantic relationship orinner thought.
''',
58: '''
5|Woodin checks that he is speaking to Admiral FA.
14|Rafael is startled and asks who he is.
25|Conditional version:Woodin introduces himself as the former head of the Woodin company.
30|Alternative conditional version:Woodin introduces himself as its current head.
38|Rafael recognizes Admiral Woodin.
45|Woodin praises Admiral FA for sweeping across the Indian Ocean so quickly.
50|Rafael protests modestly that it was a fluke.
54|Woodin tells him there is no need for such modesty and reflects that perhaps this too is fate.
57|Woodin brought something for Rafael and asks him to accept it as Woodin's final duty as steward of the Indian Ocean.
63|Rafael reacts with surprise.
68|Woodin identifies it as the never-wilting lotus leaf and says it apparently reveals where the Indian Ocean's Proof of Conquest lies.
72|Rafael realizes the large leaf is a map.
76|Woodin says the Indian Ocean's Proof of Conquest should be a book called the Rig Veda.
79|Rafael repeats Rig Veda thoughtfully.
84|Woodin hopes the object will be worthy of Rafael and bids farewell;do not reverse who is worthy of what.
95|The blunt companion concludes that Woodin is a decent older man;no kinship is established.
99|Rafael addresses the departing Admiral Woodin,thoughtfully.
106|Rafael addresses Admiral Woodin,thanks him for everything,and says goodbye.
''',
59: '''
5|A rough local tells the admiral passing by to stop.
8|Rafael asks whether they mean him.
13|The local confirms and asks whether Rafael knows that this whole area is the turf of the Portuguese governor of Indochina,Duarte Pereira.
17|Rafael asks,with a pause,what follows from that.
22|The local warns him to avoid attracting Pereira's attention.
26|Rafael pauses and thanks the local for the warning.
'''
}

CONTEXTS = {
51: 'Quiet encounter with Sera andHodram. Rafael wonders about Sera;his princess idea remains speculation. Silent andgesture records carry the awkward encounter without invented explanations.',
52: 'A local relays Albuquerque’s summons to Lisbon. Two alternate companions suggest returning;do not turn their alternatives into a two-person conversation.',
53: 'A companion reminds Rafael about the summons;Rafael confirms the palace destination.',
54: 'A local unknowingly repeats Silveira’s version of Espinosa’s defeat. Rafael is rueful,then alarmed by the Sofala governor’s-office news andhurries away.',
55: 'Silveira masks self-serving appropriation as jovial reward-giving. His stolen market share anddeducted gift provoke the crew;conditional crew reactions support Rafael’s reluctant then determined decision.',
56: 'Two grateful locals offer a lead to the Proof of Conquest. Their pooled purchase expresses restored trust;Rafael is embarrassed by praise,then surprised andthankful.',
57: 'Emilio’s injury leads to Arcadius’s thoughtful visit. Claudio moves from food jokes to an awkward request for the same care,declines the fruit,andwaits outside. Preserve the understated implication without declaring a relationship.',
58: 'Woodin courteously hands stewardship andthe Indian Ocean clue onward. Current/former leadership introductions are alternatives. Rafael is modest andgrateful;the parting stays respectful.',
59: 'An intimidating local warns Rafael about Pereira’s sphere of control;Rafael responds with restrained skepticism andthanks.'}

if __name__ == '__main__':
    output = ROOT / 'B51_B59_146_clean_meanings_v1.json'
    assert not output.exists()
    packet_path = ROOT / 'clean_source_packet.json'; packet = load(packet_path)
    source_path = Path(packet['source_ROM'])
    assert sha(source_path.read_bytes()) == packet['source_ROM_sha256']
    archive = NdsImage.open(source_path).read_file('/data/SC0.DK4')
    blocks = IlnkContainer.parse(archive).blocks
    records = []
    for group in [g for g in packet['groups'] if 51 <= g['block'] <= 59]:
        block = group['block']; meanings = {int(k): v for k, v in (line.split('|', 1) for line in MEANINGS[block].strip().splitlines())}
        assert sha(blocks[block]) == group['clean_block_sha256'] and blocks[block].hex() == group['clean_block_hex']
        assert set(meanings) == {r['source_reference']['record_index'] for r in group['records']}
        for row in group['records']:
            current = deepcopy(row); index = row['source_reference']['record_index']
            current.update(source_meaning=meanings[index], whole_exchange_context=CONTEXTS[block],
                source_read_with_all_previous_andfollowing_speeches_in_block=True,
                review=dict(source=True, context=False, localization=False, naturalness=False, formatting=False),
                event_branch_identity_native_controls_andproper_name_bindings_pending=True)
            records.append(current)
    assert len(records) == 146 and all(r['earlier_English_unconsulted'] for r in records)
    save(output, dict(format='dk4-clean-source-meaning-v1', translation_policy='natural-dialogue-v2', target_locale='en-US',
        source_packet=str(packet_path), source_packet_sha256=sha(packet_path.read_bytes()), records=records,
        all146_clean_meanings_before_current_English=True, no_localized_draft_orROM_orcompletion_credit=True,
        event_membership_not_natural_activation=True, new_credit=0, guide_photos=False,
        producer_sha256=sha(Path(__file__).read_bytes())))
    print('Saved146 source-first meanings across9 complete exchanges;current English unconsulted,zero completion credit.')
