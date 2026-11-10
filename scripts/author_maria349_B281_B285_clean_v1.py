"""Independent clean-source drafts for complete forest, town-clue and desert alternatives."""
from pathlib import Path
from scripts.audit_story_glyph_consistency import load,save

ROOT=Path('work/Maria_B275_B285_clean_20261110')
CONTEXTS={
281:"A map-dependent forest expedition encounters a wolf. The three choices are driving it away, fighting or fleeing. Distinct alternatives injure Maria, injure another crew member who warns her, or exhaust the sailors and cause some to leave. Maria regrets exposing a crew member to harm; the injured character's replies range from reassurance to a child's explicit denial of being all right. Dynamic selector218 gives prompt-treatment reassurance after the wolf leaves, but its actual role/identity still requires native binding. Preserve the separate injury targets, treatment condition, uncertainty about safety and nearing the forest exit, and final sighting without inventing the destination's identity. Source does not say a pack of wolves or a wolf killed. Physical personality alternatives are conditional voices, not a chorus. Native menu/branch mapping remains pending; adjacent block numbers do not prove original progression.",
282:"A town woman welcomes FI and describes a recent visit to the Forbidden City, an enormous palace, then suggests Maria visit too. Preserve her personal visit and sightseeing suggestion. Do not turn the palace into a temple, invent imperial permission, or infer that nearby forest alternatives occur immediately in this conversation.",
283:"Map-dependent expedition through a dark, densely wooded forest. Some voices stress darkness despite daylight, others compare it to night. A dead end prompts return or searching for a detour. The search finds no usable path, so Maria proposes retracing steps while seeking another route. One day passes before a destination is spotted. Preserve the distinct alternatives, lack of a path, one-day duration and final pointing without naming an unspoken discovery. The source darkness is not a new nighttime event or supernatural danger.",
284:"A town woman remembers an overdue tip. She heard an ancient pictorial map was found, apparently showing an old kingdom's ruins near this town. Maria wants to see the map and asks where it is, but the woman does not know. Preserve reported information, approximate place and her uncertainty; do not identify the kingdom, assert confirmed ruins, or guarantee map ownership or local availability. Native name/role and exact map terminology remain to be bound.",
285:"In a hot desert, the party needs a map and encounters a swarm of scorpions. Three choices offer fighting, driving them away or running. Repeated success alternatives praise Maria after the scorpions flee; a separate failure injures Maria and requires one day's treatment. The quiet-departure branch warns against provoking the scorpions, but a sailor drops baggage, causing a thud and a cry, then Maria orders everyone to run and a sailor-injury notice follows. Preserve every physical alternative, different injury targets, urgency, one-day stay and uncertain sailor-injury report. Do not invent poison, death, a guaranteed successful escape, lost cargo quantities or simultaneous branch activation. Dynamic218's treatment warning needs native identity/voice binding. All ordinary wraps are formatter-owned.",
}
TEXT=r'''SC3_B281_STYLE_24_0|Polite warning that without a map they will get lost.|Admiral, we'll lose our way without a map.
SC3_B281_STYLE_24_32|Measured warning that a map is needed to avoid getting lost.|Admiral, we'll get lost without a map.
SC3_B281_STYLE_24_62|Youth asks whether lacking a map is a problem.|Admiral, isn't it a bad idea to go without a map?
SC3_B281_STYLE_24_98|Conversational worry that they may get lost without a map.|Admiral, I think we'll get lost without a map.
SC3_B281_STYLE_24_130|Rough warning of trouble without a map.|Admiral, we're in trouble without a map.
SC3_B281_STYLE_24_158|Elder warns they will lose the way without a map.|Admiral, we'll lose our way if we have no map.
SC3_B281_STYLE_24_194|Child says they need a map to continue.|Admiral, we need a map if we're going on.
SC3_B281_STYLE_24_224|Formal warning about getting lost without a map.|Admiral, without a map, we shall lose our way.
SC3_B281_STYLE_322_0|Polite invitation to set out.|Come, let's go.
SC3_B281_STYLE_322_20|Bright invitation to set out.|All right, let's go!
SC3_B281_STYLE_322_36|Rough suggestion to get going.|Well, let's get moving.
SC3_B281_STYLE_322_50|Elder's invitation to depart.|Well then, shall we go?
SC3_B281_STYLE_422_0|Polite stammered warning that a wolf is there.|A-Admiral! A wolf!
SC3_B281_STYLE_422_28|Measured startled recognition of a wolf.|Hm! A wolf!
SC3_B281_STYLE_422_48|Youth stammers on seeing a wolf.|A-Admiral! It's a wolf!
SC3_B281_STYLE_422_74|Frightened scream at a wolf.|Aaaah! A wolf!
SC3_B281_STYLE_422_102|Rough startled announcement that a wolf appeared.|Whoa! A wolf!
SC3_B281_STYLE_422_132|Elder stammers in warning about a wolf.|A-Admiral! There is a wolf!
SC3_B281_STYLE_422_160|Child cries at seeing a wolf.|Aaah! It's a wolf!
SC3_B281_STYLE_422_186|Formal stammered warning about the wolf.|A-Admiral! A wolf is here!
DK4_MES_B281_R0088|A sailor cries in fear.|Eek! Aaaah!
DK4_MES_B281_R0093|Maria hushes and calms everyone.|Shh! Everyone, stay calm.
DK4_MES_B281_R0097|A retainer nervously asks what she intends.|W-what do you intend to do?
SC3_B281_CHOICE_758_0|Drive the wolf away.|Drive it away
SC3_B281_CHOICE_758_1|Fight the wolf.|Fight
SC3_B281_CHOICE_758_2|Flee.|Run
DK4_MES_B281_R0116|Maria takes charge and will drive it away.|Leave it to me. I'll drive it away.
SC3_B281_STYLE_838_0|Polite alarm warning the admiral of danger.|Admiral! Look out!
SC3_B281_STYLE_838_22|Youth urgently warns of danger.|Admiral! Watch out!
SC3_B281_STYLE_838_50|Conversational alarm directed at the admiral.|Oh! Admiral, look out!
SC3_B281_STYLE_838_76|Rough sudden warning.|Look out!
SC3_B281_STYLE_838_92|Elder's alarmed warning.|Ah! Admiral, take care!
SC3_B281_STYLE_838_118|Child urgently warns the admiral.|Oh! Admiral! Watch out!
DK4_MES_B281_R0139|Maria admits letting her guard down.|I let my guard down.
SC3_B281_STYLE_1028_0|Polite urgent check on her condition.|Are you all right!?
SC3_B281_STYLE_1028_16|Conversational urgent check.|Are you okay!?
SC3_B281_STYLE_1028_28|Rough urgent check.|You all right!?
SC3_B281_STYLE_1028_40|Child checks on her.|Are you okay?
DK4_MES_B281_R0166|Maria reassures them and thanks them.|I'm all right. Thank you.
DK4_MES_B281_R0175|System reports FI injured.|FI was injured.
DK4_MES_B281_R0179|Maria orders swords drawn and continued advance regardless.|Everyone, draw your swords! Keep moving forward!
SC3_B281_STYLE_1232_0|Urgent warning of danger.|Look out!
SC3_B281_STYLE_1232_12|Rough urgent warning.|Watch out!
SC3_B281_STYLE_1232_24|Youthful urgent warning.|Look out!
SC3_B281_STYLE_1296_0|Cry of pain from the injured crew member.|Aagh!
SC3_B281_STYLE_1296_10|High frightened cry of pain.|Aaaah!
SC3_B281_STYLE_1296_26|Brief cry of pain.|Aah!
SC3_B281_STYLE_1296_34|Rough loud cry.|Waaagh!
DK4_MES_B281_R0227|Maria checks on the injured crew member.|Are you all right!?
SC3_B281_STYLE_1384_0|In pain, but says they are managing.|Ugh! J-just about.
SC3_B281_STYLE_1384_18|Pained response without reassurance.|Ugh! Ow, ow...
SC3_B281_STYLE_1384_36|Youthful pained complaint.|Ooh! That hurts...
SC3_B281_STYLE_1384_56|Rough bravado that the wound is nothing serious.|Ugh! I-it's nothing. Just a scratch.
SC3_B281_STYLE_1384_96|Elder reassures Maria while in pain.|Ugh! I-I'm all right.
SC3_B281_STYLE_1384_120|Child cries and explicitly denies being all right.|Waaah! No, I'm not!
DK4_MES_B281_R0250|Maria blames herself for the wound and apologizes.|This is my fault... I'm sorry...
SC3_B281_STYLE_1600_0|Prompt treatment will be sufficient; the wolf has fled.|With prompt treatment, the wound will heal. The wolf has run off, too.
SC3_B281_STYLE_1600_50|Measured reassurance to the admiral; prompt treatment will heal it and the wolf left.|Admiral... Please don't worry. Prompt treatment will take care of it. The wolf has run off, too.
SC3_B281_STYLE_1600_122|Youthful reassurance that quick treatment is enough and the wolf is gone.|It'll be all right. We just need to treat the wound now. The wolf's gone, too.
SC3_B281_STYLE_1600_182|Conversational advice to treat immediately, relieved the wolf left.|We just need to treat the wound right away. At least the wolf is gone now.
SC3_B281_STYLE_1600_236|Rough reassurance that immediate treatment will heal a wound like this; wolf gone.|Don't worry! A wound like this will heal if we treat it right away. The wolf's gone, too.
SC3_B281_STYLE_1600_306|Elder reassures that immediate treatment prevents serious harm; wolf departure ends danger.|Do not fret. With prompt treatment, this wound will not be serious. The wolf has left, and the danger has passed.
SC3_B281_STYLE_1600_394|Child says quick first aid will make it all right and is glad the wolf fled.|It'll be okay if we treat it right away! The wolf ran off, too. That's good!
SC3_B281_STYLE_1600_456|Formal reassurance that this degree of injury will heal with prompt treatment; wolf left.|It will be all right. A wound like this will heal with prompt treatment. The wolf has fled as well.
DK4_MES_B281_R0274|Maria is relieved.|What a relief...
DK4_MES_B281_R0281|System says sailors appear tired.|Sailors look tired.
DK4_MES_B281_R0286|Maria thinks the wolf is very hungry and urges immediate flight.|That wolf looks terribly hungry. Let's get out of here, quickly!
DK4_MES_B281_R0294|System reports tired sailors and apparent departures by some.|Sailors are tired. Some seem to have left.
SC3_B281_STYLE_2380_0|Polite panting reassurance after running this far.|Hah... hah... hah... We should be safe this far away.
SC3_B281_STYLE_2380_54|Youth pants and wonders whether they are finally safe.|Hah... hah... hah... We should be safe now, shouldn't we?
SC3_B281_STYLE_2380_110|Conversational panting question about safety this far away.|Hah... hah... hah... We're safe this far away, aren't we?
SC3_B281_STYLE_2380_164|Rough panting hope that they are safe this far away.|Hah... hah... hah... We ought to be safe this far away.
SC3_B281_STYLE_2380_220|Elder wheezes and seeks reassurance that danger has passed.|Huff... huff... huff... W-we're safe now, aren't we?
SC3_B281_STYLE_2380_268|Child pants and asks whether they have escaped far enough.|Huff... puff... We've run far enough now, right?
SC3_B281_STYLE_2380_306|Formal panting reassurance after reaching safety.|Hah... hah... hah... We should be safe here.
SC3_B281_STYLE_2774_0|Polite suggestion that they may soon leave the forest.|We should be out of the forest soon.
SC3_B281_STYLE_2774_32|Youth asks if they are nearly through the forest.|Aren't we almost out of the forest?
SC3_B281_STYLE_2774_62|Rough observation that they may soon emerge.|Looks like we're nearly through the forest.
SC3_B281_STYLE_2774_92|Elder thinks the forest's end is near.|We should be through the forest before long.
SC3_B281_STYLE_2774_122|Child hopes they are surely near the forest's end.|We're almost out of the forest, aren't we? We must be.
SC3_B281_STYLE_2954_0|Polite announcement that the destination is coming into view.|Admiral, I can see it now!
SC3_B281_STYLE_2954_26|Youth identifies the sight to the admiral.|That's it, Admiral.
SC3_B281_STYLE_2954_42|Conversational announcement that it is visible.|Admiral, it's coming into view!
SC3_B281_STYLE_2954_64|Rough announcement of the sighting.|Admiral, I can see it!
SC3_B281_STYLE_2954_86|Child delighted to have found it.|There it is, Admiral!
DK4_MES_B282_R0006|The woman welcomes FI.|Welcome, FI.
DK4_MES_B282_R0009|She recently visited the enormous Forbidden City palace and suggests a visit.|I visited the Forbidden City the other day. It's such an enormous palace! Why don't you go and see it?
SC3_B283_STYLE_24_0|Polite statement that they cannot proceed without a map.|Admiral, we cannot go any farther without a map.
SC3_B283_STYLE_24_40|Measured warning that proceeding without a map is reckless.|Admiral, it would be reckless to go on without a map.
SC3_B283_STYLE_24_82|Youth says they cannot know the way without a map.|Admiral, how will we know where to go without a map?
SC3_B283_STYLE_24_132|Conversational admission of not knowing how to proceed without a map.|Admiral, without a map, I don't know how we can go on.
SC3_B283_STYLE_24_182|Rough statement that they cannot continue without a map.|Admiral, we can't go on without a map.
SC3_B283_STYLE_24_220|Elder says they cannot know the way without a map.|Admiral, without a map, we won't know where to go.
SC3_B283_STYLE_24_270|Child does not know the way without a map.|Admiral, we don't know where to go without a map.
SC3_B283_STYLE_24_324|Formal statement that further travel is impossible without a map.|Admiral, proceeding without a map is impossible.
SC3_B283_STYLE_436_0|Polite observation of the forest's great darkness.|It is very dark in this forest.
SC3_B283_STYLE_436_28|Measured observation of dense gloomy forest.|What a dense, gloomy forest...
SC3_B283_STYLE_436_46|Youth notes the forest is dark despite daytime.|It's daytime, but this forest is so dark!
SC3_B283_STYLE_436_74|Conversational surprise at darkness inside the forest.|It's so dark inside the forest.
SC3_B283_STYLE_436_98|Rough observation of darkness.|This forest's awfully dark.
SC3_B283_STYLE_436_118|Elder remarks on dense forest growth.|What a dense forest this is.
SC3_B283_STYLE_436_140|Child compares pitch-dark forest to night.|It's pitch-dark in here. Like nighttime.
SC3_B283_STYLE_436_172|Formal observation of dense gloomy forest.|A most dense and gloomy forest...
DK4_MES_B283_R0064|Maria sees a dead end.|A dead end...
SC3_B283_CHOICE_682_0|Turn back for now.|Turn back
SC3_B283_CHOICE_682_1|Search for a detour.|Find another way
DK4_MES_B283_R0082|Maria proposes returning for now and seeking another route.|Let's turn back for now. We'll look for another route.
DK4_MES_B283_R0088|Maria asks whether they can proceed.|Can we get through?
SC3_B283_STYLE_824_0|Polite report that no usable path can be found.|No. I can't find anything resembling a path.
SC3_B283_STYLE_824_38|Measured report that no path is visible anywhere.|No... I cannot see one anywhere.
SC3_B283_STYLE_824_68|Youth thinks it is impossible; no passable way.|It doesn't look like it. There's no way through.
SC3_B283_STYLE_824_102|Rough report of no usable path.|No good. Can't find anything like a path.
SC3_B283_STYLE_824_136|Elder reports that no path exists.|No good. There is nothing resembling a path.
SC3_B283_STYLE_824_170|Child complains there is no path.|There's no path at all!
SC3_B283_STYLE_824_188|Formal report that a path cannot be found.|No, I'm afraid not. I can find nothing resembling a path.
DK4_MES_B283_R0115|Maria must retrace their steps while looking for another way.|We have no choice. Let's head back and look for another way.
DK4_MES_B283_R0125|System reports one day elapsed.|A day passed.
SC3_B283_STYLE_1202_0|Polite excited pointing to the destination.|Admiral! Look, over there!
SC3_B283_STYLE_1202_24|Conversational excited pointing.|Admiral! There, look!
SC3_B283_STYLE_1202_50|Elder points out the sight.|Admiral! Look there!
SC3_B283_STYLE_1202_74|Child eagerly points.|Admiral! Look! Over there!
DK4_MES_B284_R0005|She greets FI and remembers something she forgot to tell her.|Oh, FI. I meant to tell you something, but it slipped my mind.
DK4_MES_B284_R0009|She heard an ancient pictorial map was found, apparently showing an old kingdom's ruins near town.|I heard someone recently found an ancient illustrated map. It seems to show the ruins of an old kingdom near this town.
DK4_MES_B284_R0012|Maria is interested in the pictorial map and asks where it is.|An illustrated map... I'd like to see it. Do you know where it is?
DK4_MES_B284_R0016|She apologizes that she does not know its location but suggests looking if interested.|I'm sorry, I don't know that much. But if you're interested, why not go and look for it?
SC3_B285_STYLE_24_0|Polite warning that they will get lost without a map.|Admiral, we'll lose our way without a map.
SC3_B285_STYLE_24_40|Measured warning about lacking a map.|Admiral, we'll get lost without a map.
SC3_B285_STYLE_24_72|Youth warns of getting lost without a map.|Admiral, we're going to get lost without a map.
SC3_B285_STYLE_24_108|Conversational warning that they will lose their way.|Admiral, we'll get lost if we don't have a map.
SC3_B285_STYLE_24_148|Rough warning about getting lost.|Admiral, we'll get ourselves lost without a map.
SC3_B285_STYLE_24_188|Elder warns they will lose the way without a map.|Admiral, we'll lose our way if we have no map.
SC3_B285_STYLE_24_226|Child urgently warns that they will get lost.|Admiral, we're going to get lost without a map!
SC3_B285_STYLE_24_268|Formal warning that a map is necessary.|Admiral, without a map, we shall lose our way.
SC3_B285_STYLE_376_0|Polite remark that it is very hot.|It really is hot.
SC3_B285_STYLE_376_18|Youth complains about intense heat.|It's so hot!
SC3_B285_STYLE_376_34|Rough complaint about the heat.|It sure is hot.
SC3_B285_STYLE_376_50|Elder remarks on the heat.|Hot, isn't it?
SC3_B285_STYLE_376_60|Child moans about the heat.|Ugh... It's so hot.
DK4_MES_B285_R0064|Maria says heat is unavoidable in a desert and urges advance.|It's a desert. We can't do anything about the heat. Come on, let's keep moving.
DK4_MES_B285_R0067|A retainer cries in alarm.|W-whoa!
SC3_B285_STYLE_558_0|Polite alarm at a swarm of scorpions.|A-Admiral! A swarm of scorpions!
SC3_B285_STYLE_558_28|Youth cries out at a swarm.|Aaah! A swarm of scorpions!
SC3_B285_STYLE_558_54|Frightened stammer on seeing scorpions.|Eek! S-scorpions!
SC3_B285_STYLE_558_80|Rough alarm at the large number of scorpions.|A-Admiral! Look at all those scorpions!
SC3_B285_STYLE_558_112|Elder warns of a swarm of scorpions.|A-Admiral! A swarm of scorpions!
SC3_B285_STYLE_558_140|Child cries at seeing scorpions.|Aaaah! Scorpions!
DK4_MES_B285_R0091|Maria hushes and calms the party.|Shh! Everyone, stay calm.
DK4_MES_B285_R0095|A retainer objects nervously and asks what to do.|B-but... What are we going to do?
SC3_B285_CHOICE_814_0|Fight to deal with the scorpions.|Fight
SC3_B285_CHOICE_814_1|Drive the scorpions away.|Drive them away
SC3_B285_CHOICE_814_2|Flee.|Run
DK4_MES_B285_R0114|Maria takes responsibility and gives a forceful shout in attack.|Leave it to me. Hyah!
SC3_B285_STYLE_888_0|Polite relief that they fled and praise for the admiral's reliability.|Oh, they've run off! Just as I'd expect from you, Admiral. We can count on you.
SC3_B285_STYLE_888_56|Measured praise after the scorpions flee.|Ah, they've fled! Well done, Admiral.
SC3_B285_STYLE_888_88|Youth admires the admiral after their flight.|Oh, they ran away! That's our admiral. We can always count on you.
SC3_B285_STYLE_888_136|Rough praise for the reliable admiral after the creatures flee.|Hey, they ran off! That's our admiral. We can count on you!
SC3_B285_STYLE_888_182|Elder admires the admiral's reliability after their flight.|Ah, they've run off! Well done, Admiral. We can depend on you.
SC3_B285_STYLE_888_234|Child is delighted they fled and praises the admiral.|Oh, they ran away! Admiral, you're amazing!
SC3_B285_STYLE_888_278|Formal praise for the admiral's reliability after their flight.|Ah, they have fled! Well done, Admiral. We can always rely on you.
DK4_MES_B285_R0138|Maria takes charge of driving the scorpions away.|Leave it to me. I'll drive them away.
SC3_B285_STYLE_1286_0|Polite relief that they fled and praise for the admiral's reliability.|Oh, they've run off! Just as I'd expect from you, Admiral. We can count on you.
SC3_B285_STYLE_1286_56|Measured praise after the scorpions flee.|Ah, they've fled! Well done, Admiral.
SC3_B285_STYLE_1286_88|Youth admires the admiral after their flight.|Oh, they ran away! That's our admiral. We can always count on you.
SC3_B285_STYLE_1286_136|Rough praise for the reliable admiral after the creatures flee.|Hey, they ran off! That's our admiral. We can count on you!
SC3_B285_STYLE_1286_182|Elder admires the admiral's reliability after their flight.|Ah, they've run off! Well done, Admiral. We can depend on you.
SC3_B285_STYLE_1286_234|Child is delighted they fled and praises the admiral.|Oh, they ran away! Admiral, you're amazing!
SC3_B285_STYLE_1286_278|Formal praise for the admiral's reliability after their flight.|Ah, they have fled! Well done, Admiral. We can always rely on you.
DK4_MES_B285_R0161|Maria cries in pain or effort.|Ugh!
SC3_B285_STYLE_1658_0|Polite urgent concern for the admiral.|Admiral! Are you all right!?
SC3_B285_STYLE_1658_28|Conversational concern for the admiral.|Admiral! Are you okay!?
SC3_B285_STYLE_1658_50|Rough urgent concern for the admiral.|Admiral! You all right!?
SC3_B285_STYLE_1658_74|Child cries out to the admiral.|Admiral!
DK4_MES_B285_R0188|Maria admits letting her guard down.|I let my guard down.
SC3_B285_STYLE_1784_0|Polite warning that immediate treatment is needed.|This needs immediate treatment!
SC3_B285_STYLE_1784_24|Conversational urgent need for first aid.|We need to treat this right away!
SC3_B285_STYLE_1784_48|Alarmed urgent call for treatment.|Oh, no! We need to treat this at once!
SC3_B285_STYLE_1784_78|Rough urgent call for treatment.|We've got to treat this right away!
SC3_B285_STYLE_1784_100|Elder calls for urgent treatment.|This needs urgent treatment!
SC3_B285_STYLE_1784_124|Formal warning about treatment urgency.|Immediate treatment is required!
DK4_MES_B285_R0227|FI is injured; the party stays one day for treatment.|FI was injured. Staying one day for treatment.
DK4_MES_B285_R0236|Maria thanks the others and is now all right.|Thank you. I'm all right now.
DK4_MES_B285_R0240|Maria orders quiet departure without needlessly provoking the scorpions.|Leave quietly. Don't do anything to provoke them.
SC3_B285_STYLE_2156_0|Polite instruction to set off very quietly.|Everyone, we're moving on. Quietly... quietly...
SC3_B285_STYLE_2156_40|Rough instruction to depart quietly.|Everyone, we're moving out. Nice and quiet...
SC3_B285_STYLE_2156_80|Youth urges quiet departure.|Everyone, let's go. Quietly... quietly...
SC3_B285_STYLE_2156_118|Conversational instruction to depart quietly.|Everyone, we're going now. Nice and quiet...
SC3_B285_STYLE_2156_158|Elder instructs quiet movement.|Everyone, let us go. Quietly now, quietly...
SC3_B285_STYLE_2156_202|Child tells everyone to depart quietly.|Everyone, let's go! Quietly... quietly...
DK4_MES_B285_R0273|A dropped load makes a heavy thud.|Thud!
DK4_MES_B285_R0277|A sailor realizes baggage has fallen; no explicit agent is given.|Oops! There goes the baggage!
SC3_B285_STYLE_2510_0|Polite alarm that this is bad.|Oh, no!
SC3_B285_STYLE_2510_16|Brief startled exclamation.|Ah!
SC3_B285_STYLE_2510_24|Rough alarm at trouble.|Uh-oh!
SC3_B285_STYLE_2510_34|Frustrated realization that something has gone wrong.|Oh, no!
DK4_MES_B285_R0301|The sailor cries out in pain.|Aaaagh!
SC3_B285_STYLE_2594_0|Polite stammered concern and urging the sailor to hold on.|A-are you all right? Hold on!
SC3_B285_STYLE_2594_34|Measured urgent concern and encouragement.|Are you all right? Stay with us!
SC3_B285_STYLE_2594_62|Conversational stammered concern and encouragement.|A-are you okay? Hold on!
SC3_B285_STYLE_2594_92|Rough urgent concern and encouragement.|Hey, you all right? Hang in there!
SC3_B285_STYLE_2594_126|Elder's stammered concern and encouragement.|A-are you all right? Stay strong!
SC3_B285_STYLE_2594_158|Urgent stammered concern and encouragement.|A-are you all right? Hold on!
DK4_MES_B285_R0327|Maria orders everyone to run quickly.|Everyone, run! Hurry!
DK4_MES_B285_R0333|System reports that sailors appear to have been injured, without a stated count.|Sailors seem to have been injured.
DK4_MES_B285_R0352|A retainer thinks they have arrived.|Oh, looks like we've arrived!'''

def main():
    output=ROOT/'authored_B281_B285_v1.json';assert not output.exists()
    rows=[r.split('|',2) for r in TEXT.splitlines()];packet=load(ROOT/'clean_source_packet.json')
    expected=[r['id'] for g in packet['groups'] if g['block'] in CONTEXTS for r in g['records']]
    assert [r[0] for r in rows]==expected and len(rows)==204
    save(output,dict(contexts={str(k):v for k,v in CONTEXTS.items()},records=rows,current_English_not_consulted=True,
        source_gloss_precedes_independent_draft_in_each_entry=True,source='Complete clean Japanese exchanges only; item terms and native role/voice consumers remain provisional.',new_credit=0))
    print('Authored204 clean meanings andindependent drafts in five complete groups;current story English unread.')

if __name__=='__main__':main()
