"""Save clean-first meanings/drafts for six complete blocks before exposing current English."""
from copy import deepcopy
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load, save

ROOT = Path('work/analysis/Rafael_B121_B140_clean_20261105')
OUT = ROOT/'B121_B126_meanings_andindependent_drafts_v1.json'

# Faithful meaning, then an independent conversational draft. Neither is a final comparison approval.
TEXT = {
121: {
6: ('Rafael remarks on the large palace they visited and suggests returning to town.', "That was a huge palace. Come on, let's head back to town."),
12: ('Wordless questioning reaction.', '?'),
40: ('Rafael politely asks what is wrong.', "What's the matter?"),
45: ('An older man urgently appeals to the travelers to save his grandchild.', "Travelers! Thank goodness you're here! Please save my grandson!"),
48: ('The dynamic companion questions the mention of a grandchild.', 'Your grandson?'),
52: ('The frightened boy cries out for his actual grandfather.', 'Waaah! Grandpa!'),
56: ('Rafael realizes a boy is drowning.', "That boy's drowning!"),
86: ('After rescue, the boy is still crying and frightened.', 'Waaah! I was so scared!'),
90: ('His grandfather reassures him and expresses relief.', "You're safe now! Oh, thank goodness!"),
93: ('The old man thanks the travelers deeply.', "Thank you, travelers! I can't tell you how grateful I am!"),
96: ('Rafael shares the grandfather’s relief that the boy is unharmed.', "I'm glad your grandson is safe."),
100: ('The man initially has nothing to offer, then remembers something and asks them to wait.', "I've nothing to give you in thanks... Ah, I know! Please wait a moment!"),
104: ('He asks the travelers to accept an object.', 'Please, take this.'),
108: ('Rafael asks what the offered object is.', "What's this?"),
113: ('In his youth the man defeated local bandits; the governor gave him this object as a reward.', 'When I was young, I defeated the bandits that plagued this area. The governor gave me this as a reward.'),
116: ('He does not know the object’s origins but has heard it is quite valuable.', "I don't know its history, but I'm told it's quite valuable."),
120: ('Rafael modestly declines, saying the older stranger should keep the reward as a memento of his bravery.', "I couldn't... Sir, you should keep it as a reminder of your bravery."),
124: ('The man insists on thanking his grandson’s saviors and says the object is of no use to him, not objectively worthless.', "No, no. I can't let the people who saved my grandson leave empty-handed. Please don't worry. It's no use to me."),
127: ('Rafael gratefully accepts after the insistence.', "Well, then... Thank you. I'll gladly accept it."),
134: ('The old man bids the travelers a safe journey.', 'Safe travels, then. Take care of yourselves.'),
138: ('The child affectionately says goodbye to an older boy/man; this does not establish a sibling relationship.', 'Bye! See you!'),
},
122: {
27: ('Rafael admires the exceptional jade.', "Wow! What beautiful jade!"),
40: ('The speaker explains that jade is especially prized among gems in the New World, as in the East.', 'In the New World, as in the East, jade is particularly prized among gemstones.'),
43: ('The quantity of jade offerings suggests this building had considerable significance; it is an inference.', 'With so much jade offered here, this building must have held great significance.'),
},
123: {
29: ('Rafael initially takes the object for an ordinary stone tablet.', "Hmm. It's just a stone tablet."),
48: ('Janus rejects that assumption: local stone scarcity explains why the mosque is made of dried mud.', "...This is no ordinary stone tablet. For a start, there's no stone around here. That's why they built the mosque out of dried mud."),
51: ('Rafael asks whether that means the tablet was not made locally.', "You mean this tablet wasn't made here?"),
55: ('Janus agrees, while preserving uncertainty.', 'Yes, most likely.'),
63: ('In an alternative companion exchange, the speaker tells the admiral this is no ordinary tablet.', 'Admiral... This is no ordinary stone tablet.'),
66: ('Rafael asks for an explanation.', 'What do you mean?'),
71: ('The companion explains that total local stone scarcity is why the mosque is built of dried mud.', "There's no stone to be found here. That's why even the mosque is built out of dried mud."),
75: ('Rafael begins to grasp the implication.', 'What? Then that means...'),
80: ('The conclusion is that the tablet was brought from elsewhere.', 'This tablet must have been brought here from somewhere else.'),
83: ('Rafael understands the inference.', 'Oh, I see!'),
98: ('A system/ambient whisper precedes another branch of the scene.', '(Whispering...)'),
102: ('Speaker3 reacts inquisitively.', '?'),
106: ('A rough speaker complains that the current situation makes attacking impossible.', "This is trouble. We can't make a move with things like this..."),
109: ('Speaker3 asks whether these are the bandits who were attacking the town named in the source.', '...Are you the bandits who were attacking Sao Jorge?'),
112: ('The bandit is startled and aggressively asks the stranger’s identity.', 'Wh-what?! Who the hell are you?'),
115: ('Speaker3 identifies affiliation through the original FO organization substitution.', "I'm with FO."),
119: ('The bandit resents the group’s help with the town’s defenses.', "What?! You've been helping guard that town! You've really screwed us over!"),
123: ('Their attacks are now prevented, so the bandit complains about losing his livelihood; the food expression is idiomatic.', "We can't raid it because of you! How are we supposed to make a living now?"),
126: ('Another companion rebukes the bandits and insists they cannot abandon the troubled townspeople.', "You've got some nerve, for a bandit! We can't just abandon the townspeople when they need help!"),
130: ('The bandit says Europeans ruined their village, explaining his anger.', 'Shut up! Those Europeans left our village in ruins!'),
133: ('He vows revenge regardless of objections.', "I don't care what anyone says. We'll have our revenge!"),
136: ('Speaker3 distinguishes the corrupt slave traders and cruel plundering soldiers from all Europeans.', 'Wait. The people you should blame are the corrupt merchants trading slaves here in Africa and the cruel soldiers who loot and pillage.'),
139: ('Indiscriminately hating and attacking all Europeans would make the bandits guilty of the same cruelty.', "If you hate every European and attack them indiscriminately, you're no better than those brutes. You're guilty of the same thing."),
142: ('The bandit rejects the outsider’s apparent understanding.', 'You talk like you know everything!'),
146: ('Speaker3 urges him to abandon meaningless revenge because it cannot restore their happiness.', "Give up your revenge. It's pointless. It won't bring back the life you had, will it?"),
150: ('Revenge would perpetuate conflict and bring suffering to more of his own people.', "It'll only lead to more fighting. More of your own people will suffer."),
154: ('The bandit falters and demands an alternative.', 'Th-then what are we supposed to do?!'),
157: ('Speaker3 proposes ending the European powers’ rivalry, which causes many conflicts across the seas.', "We have to put an end to the rivalry among the European powers. It's behind so many conflicts on the world's seas."),
161: ('The bandit reacts in astonishment.', '!?'),
165: ('The powers are about to partition the world; the group collects the Proofs sought as a pretext for those claims in order to stop them.', "The great powers are about to divide up the whole world. They want the Proofs to justify it. We're collecting them to stop that."),
168: ('The bandit is incredulous that the group intends to stop the great powers.', 'Stop the great powers?! Are... are you serious?'),
171: ('Speaker3 denies bluffing and says their reach into Africa gives confidence in facing the powers on equal or better terms.', "We're not bluffing. Our influence already reaches this far into Africa. I'm confident we can meet them on equal terms. Or better."),
174: ('A silent pause as he considers this.', '...'),
178: ('Speaker3 invites him to entrust the matter of revenge to the group.', 'Well? How about leaving your revenge to us?'),
181: ('He is startled by the offer.', 'What?!'),
185: ('Speaker3 invites him to sea, expressing confidence that his spirit will let him succeed.', "Come to sea with us. With spirit like that, I'm sure you can do it."),
189: ('He pauses again before deciding.', '...'),
193: ('He concludes staying here will achieve nothing.', "Staying here won't change anything..."),
196: ('He decides to take a chance on the speaker.', "All right. I'll take a chance on you!"),
200: ('Speaker3 welcomes him.', 'Welcome aboard.'),
207: ('He offers an object hidden in the ruins, explicitly uncertain whether it relates to the Proof.', "I don't know whether it's got anything to do with that Proof you're after, but I found this hidden in the ruins."),
210: ('Speaker3 identifies the offered object with uncertainty.', 'A stone tablet...?'),
},
124: {
6: ('The speaker asks the departing party to wait.', 'Hey, wait.'),
10: ('The dynamic recipient reacts inquisitively.', '?'),
14: ('The speaker wants to reciprocate a present by sharing useful information.', "I can't just take a present without giving anything back. So here's a useful tip to say thanks."),
18: ('A magnificent building in India is worth visiting after traveling this far; the current location is not specified.', "There's a magnificent building in India. If you've come this far, you really ought to see it."),
22: ('A map is required to reach it, but the speaker encourages a visit.', "The trouble is, you can't get there without a map. Do try to visit it."),
25: ('Rafael thanks the speaker and conditionally promises a visit if he finds a map.', "Thanks. If I find a map, I'll go and see it."),
},
125: {
6: ('A dynamic companion draws the admiral’s attention to the statue.', 'Admiral, this statue...'),
10: ('Rafael asks in surprise.', 'Huh?'),
33: ('Rafael questions the companion’s observation.', 'You think so?'),
55: ('Rafael recognizes that the observation is right.', "Oh, you're right!"),
},
126: {
6: ('The speaker recognizes an object with surprise.', 'Oh! This is...!'),
10: ('The discoverers have the right to own the small knife.', 'As its discoverers, you have the right to keep this knife.'),
16: ('The speaker thanks the party for finding the tribe’s spiritual support and asks them to accept the offering; no extra religious doctrine is specified.', "Thanks to you, we've finally found the source of our tribe's spiritual strength. Please accept it."),
20: ('An FE acquisition notice awards exactly24000 gold coins.', 'You received 24,000 gold coins.'),
27: ('The speaker suggests returning because the people in the fleet will be waiting.', "Now, let's head back. Everyone in the fleet must be waiting for us."),
},
}
STYLE = {
'SC0_B121_STYLE_80_0': ('A companion notices someone on a river sandbar; standard alert with five alias slots.', "Hm? Someone's out on that sandbar."),
'SC0_B121_STYLE_80_24': ('A feminine-register companion notices someone on the sandbar, without identifying that person.', "Hm? There's someone on that sandbar."),
'SC0_B121_STYLE_80_46': ('An older-register companion notices someone on the sandbar.', "Hmm? There's someone out on the sandbar."),
'SC0_B121_STYLE_80_70': ('A youthful companion simply notices someone; this variant does not explicitly repeat the sandbar.', "Huh? There's someone over there."),
'SC0_B121_STYLE_342_0': ('A politely confident companion volunteers to handle the rescue.', "I'll take care of it!"),
'SC0_B121_STYLE_342_18': ('A casual companion volunteers.', 'Leave it to me!'),
'SC0_B121_STYLE_342_28': ('A feminine-register companion volunteers to go personally.', "I'll go!"),
'SC0_B121_STYLE_342_42': ('A rough, confident companion volunteers.', "I've got this!"),
'SC0_B121_STYLE_342_54': ('An older, emphatic companion volunteers without stating a family relationship or rank.', 'You just leave it to me!'),
'SC0_B121_STYLE_342_76': ('A youthful companion volunteers to go.', "I'll go!"),
'SC0_B122_STYLE_16_0': ('A companion calls the admiral’s attention to an object; standard variant with five aliases.', 'Admiral, look at this!'),
'SC0_B122_STYLE_16_16': ('A casual companion asks the admiral to look.', 'Admiral, look!'),
'SC0_B122_STYLE_16_30': ('A youthful companion points an object out to the admiral.', 'Admiral! Look at this!'),
'SC0_B123_STYLE_16_0': ('A polite companion asks the admiral to inspect the object.', 'Admiral, please look at this!'),
'SC0_B123_STYLE_16_28': ('A casual companion asks the admiral to look at the object.', 'Admiral, look at this!'),
'SC0_B123_STYLE_16_48': ('A rough, familiar companion asks the admiral to look.', 'Admiral, take a look at this!'),
'SC0_B123_STYLE_16_74': ('An older-register companion directs the admiral to look.', 'Admiral, have a look at this!'),
'SC0_B123_STYLE_16_100': ('A youthful companion calls the admiral’s attention to the object.', 'Admiral! Look at this!'),
'SC0_B125_STYLE_54_0': ('A polite companion tentatively notes the statue’s design does not suit the building.', "Its design doesn't seem to suit this building."),
'SC0_B125_STYLE_54_46': ('A reserved companion says the design appears out of place in the building.', 'The design seems out of place in this building.'),
'SC0_B125_STYLE_54_92': ('A casual companion says the statue stands out awkwardly from the building.', "It just looks out of place in this building."),
'SC0_B125_STYLE_54_132': ('A feminine conversational register describes a mismatch with the building.', "It doesn't really go with this building, does it?"),
'SC0_B125_STYLE_54_170': ('A rough companion directly asks whether the statue fits the building.', "Don't you think it looks out of place in this building?"),
'SC0_B125_STYLE_54_214': ('An older companion cautiously feels the statue does not suit the building.', "Hmm. It doesn't seem to belong in this building."),
'SC0_B125_STYLE_54_268': ('A youthful companion informally senses a mismatch.', "It just doesn't fit in with this building."),
'SC0_B125_STYLE_54_300': ('A measured, deferential companion asks whether the design is unsuitable.', "Doesn't its design seem out of place in this building?"),
'SC0_B125_STYLE_440_0': ('The companion first notes a resemblance, then wonders whether it was originally a figurehead.', "It's shaped like a figurehead... Could that be what it was originally?"),
'SC0_B125_STYLE_440_52': ('A reserved companion recognizes the shape and questions whether it was actually a figurehead from the start.', "It's shaped like a figurehead... Wait, could it actually be one?"),
'SC0_B125_STYLE_440_106': ('A casual companion moves from resemblance to the thought that the statue may actually be a figurehead.', "Doesn't it look like a figurehead? Actually, maybe that's what it is."),
'SC0_B125_STYLE_440_182': ('A feminine-register companion reconsiders whether the figurehead resemblance reflects the object’s original identity.', "It looks like a figurehead... Oh, maybe that's what it was all along?"),
'SC0_B125_STYLE_440_238': ('A rough companion thinks it looks like a figurehead, then trails off as he realizes it might be one.', "Looks like a figurehead to me... Hang on, isn't that what this is...?"),
'SC0_B125_STYLE_440_304': ('The older-register variant concludes it actually is a figurehead, rather than merely asking.', "It has the shape of a figurehead... Ah, that's exactly what it is."),
'SC0_B125_STYLE_440_366': ('Unlike the other variants, the youthful speaker proposes using it as a figurehead, without asserting its original identity.', 'You could make a figurehead out of this. Look!'),
'SC0_B125_STYLE_440_394': ('A measured companion recognizes a figurehead’s shape and questions whether it actually was one originally.', "It has the shape of a figurehead... Could that have been its original purpose?"),
}
CONTEXT = {
121: 'Leaving a palace, the party notices someone on a river sandbar and meets an older man whose grandson is drowning. A runtime-selected volunteer rescues the boy. Relief leads to an offered reward, a modest refusal, the grandfather’s insistence and grateful acceptance. The child’s familiar address to the rescuer is not a sibling relationship. The gift’s monetary value is reported, not proven; its lack of usefulness to its owner does not mean it is worthless. Source event actions and alternative volunteers do not establish a full natural playthrough.',
122: 'A selected companion points out jade offerings. Rafael admires them and another speaker explains the New World/East comparison, then infers this building’s significance from the abundance of offerings. Keep the inference and do not add a civilization, deity, date or named gem.',
123: 'The block contains structurally separate exchanges, not a single uninterrupted party conversation. Rafael calls the object an ordinary stone tablet; alternative companions explain that local stone scarcity makes the mud-built mosque evidence of an imported tablet. Another branch has speaker3 confront bandits who attacked a town the group helped guard. Their grievance concerns European slave traders and plundering soldiers; speaker3 condemns indiscriminate retaliation, explains opposition to great-power partition and use of the Proofs as a pretext, then recruits a bandit. His eventual tablet offer remains uncertainly related to the Proof. Preserve anger, firm moral argument, hesitation and acceptance without inventing participants or suppressing the colonial/slavery context.',
124: 'The speaker reciprocates a present with information about a worthwhile building in India. Reaching it requires a map; Rafael’s promise is conditional on finding one. Do not invent a romance, identify the unnamed landmark, or assume the current town is in India.',
125: 'A runtime-selected companion notices a statue that does not fit its building. Another runtime role discusses its resemblance to a figurehead. Most variants wonder whether it originally was one; the older variant concludes it is, while the youthful variant proposes using it as one. Preserve these factual and personality differences. No dynamic selector is assigned a fixed character in the translation.',
126: 'The speaker recognizes a discovery, explains the discoverers’ right to keep a small knife, thanks them for finding the tribe’s spiritual support, and suggests returning to the waiting fleet. A native FE notice awards24000 gold coins in its source path. Do not invent a named deity, specific ceremonial practice, speaker rank, or universal reward activation.',
}

if __name__ == '__main__':
    assert not OUT.exists()
    packet_path = ROOT/'clean_source_packet.json'; style_path = ROOT/'clean_style_objects.json'
    packet, styles, choices = map(load,[packet_path,style_path,ROOT/'clean_choice_objects.json'])
    ordinary = [r for g in packet['groups'] for r in g['records'] if 121 <= g['block'] <= 126]
    selected_styles = [r for r in styles['records'] if 121 <= r['block'] <= 126]
    assert len(ordinary) == 81 and len(selected_styles) == 34 and len(styles['records']) == 34
    assert not any(121 <= r['block'] <= 126 for r in choices['records'])
    assert sum(map(len,TEXT.values())) == 81 and len(STYLE) == 34
    records = []
    for row in ordinary+selected_styles:
        if row['id'] in STYLE:
            meaning, draft = STYLE[row['id']]
        else:
            meaning, draft = TEXT[row['block']][row['source_reference']['record_index']]
        record = deepcopy(row)
        record.update(source_meaning=meaning,independent_English_draft=draft,source_exchange_context=CONTEXT[row['block']],
            source_names_roles_terms_anddynamic_bindings_pending=True,current_English_comparison_pending=True,
            no_fixed_identity_inferred_for_dynamic_selector=row['source_selector'] >= 207,
            no_blanket_historical_English_exposure_claim=True,
            review=dict(source=False,context=False,localization=False,naturalness=False,formatting=False),new_credit=0)
        if row['id'] == 'DK4_MES_B123_R0109':
            record['town_name_spelling_pending_approved_label_binding'] = True
        records.append(record)
    assert len({r['id'] for r in records}) == len(records) == 115
    save(OUT,dict(clean_packet=str(packet_path),clean_packet_sha256=sha(packet_path.read_bytes()),
        clean_style_objects=str(style_path),clean_style_objects_sha256=sha(style_path.read_bytes()),
        records=records,complete_blocks=[121,122,123,124,125,126],ordinary_speeches=81,physical_style_variants=34,
        all34_style_variants_in_packet_included=True,independent_drafts_precede_current_English_extraction_in_this_intake=True,
        no_blanket_historical_unexposure_orfinal_approval_claim=True,
        specific_source_risks=['Grandpa is real kinship;the child’s rescuer address is not.','Bandit loss-of-food idiom means lost livelihood.',
            'Gift of no use to its owner is not worthless.','Imported tablet conclusion follows local stone scarcity.',
            'Maintain anti-slave-trade context anddistinguish indiscriminate retaliation.','Figurehead certainty andproposed use differ between personality variants.',
            'India clue is map-conditional;no invented landmark orrelationship.'],
        current_comparisons_names_terms_allfive_gates_anddisplay_pending=True,new_credit=0,
        producer_sha256=sha(Path(__file__).read_bytes())))
    print('115 clean-first meanings andindependent drafts saved acrosssix whole blocks:81 speeches/all34 personality variants. Current comparison/identity/display gates remain pending.')
