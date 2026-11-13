"""Source-first Mediterranean alternatives andPortuguese summons;do not turn loss into victory."""
from pathlib import Path
from scripts.source_only_gloss_v1 import seal

ROOT=Path('work/analysis/Rafael_B61_B80_clean_20261104')
MEANINGS={
76: '''
7|Rafael recognizes andaddresses Admiral Hayreddin.
12|Hayreddin remarks that FI has grown;although the Ottoman Pasha forces are extraordinarily strong,he thinks Rafael's group may be capable of facing them,leaving the thought unfinished.
15|Rafael begins with a nervous polite affirmative,privately catches himself andswitches to a more confident response;do not invent a new rank to explain the change.
20|Hayreddin tells them that if they defeat Pasha's forces,they should go to Alexandria andmeet the priest.
23|Rafael repeats the Alexandria priest reference andsays he will remember it.
27|Hayreddin strongly warns them not to let down their guard.
31|Claudio cheerfully acknowledges the warning andthanks the older man;おっさん is familiar address,not kinship.
34|Hayreddin gives a brief amused response andtakes his leave.
37|Rafael says goodbye to Admiral Hayreddin.
''',
77: '''
5|Rafael celebrates FO finally becoming the foremost power in the Mediterranean.
10|Claudio admits they suffered a painful direct defeat against Valdes,butsays their overall success still counts andthey should hold their heads high;do not reverse the battle result.
13|Rafael agrees that winning naval battles is not everything andurges them on toward the sourceエシュタード objective;the exact earlier clean-term/approved spelling binding remains pending rather than inventing its territorial scope.
''',
78: '''
5|Claudio declares them the strongest Mediterranean power andsays even Spain cannot ignore FO's support for restoring the Portuguese royal house.
9|Rafael hesitantly hopes Claudio is right.
13|Claudio tells him that he is now a ruler/master of the seas in both name andsubstance andshould show more pride;this praise is not a newly invented formal coronation.
17|Rafael accepts the encouragement andthanks Clau.
21|Claudio reminds him that he is their admiral andurges him to keep going because they are nearly there.
24|Rafael rallies them to conquer the world's seas.
29|The sailor gives a loud enthusiastic affirmative cheer.
''',
79: '''
5|Actor139 respectfully congratulates FA on attaining Mediterranean supremacy andasks him to accept an offered object.
10|Rafael sighs with relief at how long it has taken.
22|Arcadius confidently infers that this too is a Proof of Conquest map andrecalls that the Mediterranean treasure should be some kind of crown;preserve the inference anduncertain recollection rather than naming a specific crown.
29|Claudio says that is what they must look for andurges them onward.
32|Rafael is puzzled because the pattern drawn on the cloth does not look like a map at all.
''',
80: '''
13|Actor113 says he has finally found FA,checks his identity andannounces that the king of Portugal is summoning him.
19|In the homecoming alternative,the same speaker announces FA's return andsays the king is calling for him.
'''}
CONTEXT={
76:'Whole Hayreddin warning andfarewell. He praises Rafael growth butframes the Pasha victory andAlexandria priest visit as future conditional steps. Rafael catches his own deferential response;Claudio uses a familiar older-man address without kinship.',
77:'Complete three-speech alternative acknowledging Mediterranean supremacy despite an explicit painful direct loss to Valdes. Retain overall achievement versus particular naval defeat andthe namedエシュタード ambition;no unspoken economic mechanism orterritorial definition is supplied.',
78:'Whole Mediterranean confidence/rally exchange. FO supports restoration of the Portuguese royal house;Claudio encourages the still-insecure Rafael,who rallies the crew to the world seas. Praise of mastery does not confer a newly defined royal rank.',
79:'Complete Mediterranean object handover andmap/crown discussion. The cloth pattern confuses Rafael even though Arcadius thinks it is a map. Sourceactor139 role,exact item binding andevent conditions remain pending;do not add a particular crown name orHighPriest rank.',
80:'Two complete alternative summons delivered by the same sourceactor113:an identity-check encounter andrecognition on homecoming. Portugal king is explicit in the first. Bind these to exact EV0 conditions andthe B74 summons without treating both alternatives as a linear exchange.'}

if __name__=='__main__':
    seal(ROOT/'clean_source_packet.json',ROOT/'B76_B80_26_clean_meanings_v1.json',MEANINGS,CONTEXT,__file__)
