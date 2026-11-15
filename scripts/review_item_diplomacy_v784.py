"""Clean-source item-shop/diplomatic drafts; no production formatting approval."""

from collections import Counter
from dataclasses import asdict
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import common_message_entries
from scripts.context_item_diplomacy_v784 import ROOT, CURRENT, TABLES
from scripts.verify_village_wrap_v608 import read, save

MANUSCRIPT = Path('translations/item_diplomacy_editorial_manuscript_v1.json')
TEXTS = {
1070: "Sorry, I'm sold out.",
1071: "Which one would you like?",
1072: "That's %s coins. A bit out of your price range, isn't it?",
1073: "That's %s coins. Want to buy it?",
1074: "Thanks for your business!",
1075: "That's rather expensive. Could you lower the price?",
1076: "That's expensive. Surely you can do better?",
1077: "That's a bit steep. Give me a better price.",
1078: "Oh, that's expensive. You can go a little lower, can't you?",
1079: "Come on, that's way too much. You can do better than that!",
1080: "That's a steep price. Surely you can lower it?",
1081: "Hmm, that's expensive. You'll give me a discount, won't you?",
1082: "That's rather pricey. Could you make it a little cheaper?",
1083: "All right, then. %s coins it is.",
1084: "Hold on. You don't have anything to sell.",
1085: "What would you like to sell?",
1086: "Hmm... I'll give you %s coins for it. How's that?",
1087: "You're joking, right? This is one of a kind. Take a closer look.",
1088: "Surely you don't mean to offer so little for an item of this quality?",
1089: "This is incredibly valuable! Did you even take a good look at it?",
1090: "That price?! Pass this up, and you might never find another like it.",
1091: "You're kidding, right? This is one of a kind. Take a better look!",
1092: "Eh? You don't know what this is worth. Take a closer look!",
1093: "That's way too low! Take a good look. This is really valuable!",
1094: "You must be joking. This is a remarkable piece... Surely you can see what it's worth?",
1095: "...All right. I'll give you %s coins.",
1096: "Thanks!",
1097: "For 1,000 coins, I'll deliver a letter to another faction.",
1098: "Which faction should we send this %s to?",
1099: "Who should get this %s?",
1100: "This %s... Whom shall we send it to?",
1101: "Who's getting this %s?",
1102: "Who is to receive this %s?",
1103: "Choose the enemy we'll face together.",
1104: "And which enemy are we teaming up against?",
1105: "Who shall we join forces against?",
1106: "Who are we picking a fight with?",
1107: "Which faction shall we stand against together?",
1108: "We'll sign a pact with %s to oppose %s, correct?",
1109: "We're making a pact with %s against %s, right?",
1110: "We shall make a pact with %s against %s. Is that right?",
1111: "We're promising to team up with %s against %s, right?",
1112: "We are to make a pact with %s against %s, correct?",
1113: "We're sending %s our %s, correct?",
1114: "You're sending %s our %s, right?",
1115: "So %s is to receive our %s. Is that right?",
1116: "We're sending %s our %s, right?",
1117: "I'll draft the diplomatic letter. What should it say?",
1118: "Then I'll draft the diplomatic letter. What should it say?",
1119: "I'll write the letter for you. So, what do you want it to say?",
1120: "I'll draw up the diplomatic letter. What shall I put in it?",
1121: "I'll write the letter! What should I say?",
1122: "Allow me to compose the diplomatic letter. What should it say?",
1123: "Don't worry. I'll see that it gets delivered.",
1124: "Admiral, there's no faction in these waters we can send a diplomatic letter to.",
1125: "...Come to think of it, there's no faction in these waters we can send a diplomatic letter to.",
1126: "Now that I think about it, there's nobody in these waters to send a diplomatic letter to.",
1127: "...Admiral, there's no faction in these waters we can send a diplomatic letter to.",
1128: "Right, nobody in these waters can receive a diplomatic letter.",
1129: "Well now, no faction in these waters can receive diplomatic letters.",
1130: "Sorry, the couriers are all out now. Please wait five or six days.",
1131: "There's no faction for us to join forces against.",
1132: "We have no enemy to face together.",
1133: "There's nobody we can team up against.",
1134: "There's nobody for us to join forces against.",
1135: "There is no enemy for us to oppose together.",
1136: "There's nobody we can team up to beat!",
1137: "There is no enemy for us to face together.",
1138: "I really don't think %s would come under our command. Are you sure?",
1139: "I can't imagine %s agreeing to come under our command... Are you certain?",
1140: "I can't imagine %s coming under our command... Are you really going ahead with this?",
1141: "There's no way %s would come under our command. Do you really want to do this?",
1142: "%s would never come under our command... Want to try anyway?",
1143: "I can't imagine %s coming under our command. Do you still mean to try?",
1144: "I don't think %s will ever surrender... Still want to try?",
1145: "I doubt %s would come under our command. Are you certain you wish to proceed?",
}

GLOSSES = {
1070: 'Rough but apologetic merchant says the stock is sold out.',
1071: 'Merchant asks which item the customer chooses.',
1072: 'States the supplied gold-coin price and taunts that the customer cannot afford it;does not ask whether to buy.',
1073: 'States the supplied gold-coin price and asks whether to buy.',
1074: 'Merchant thanks the customer for the purchase.',
1075: 'Politely says the asking price is high and asks whether it can be lowered.',
1076: 'Firmly says it is expensive and expects a lower price to be possible.',
1077: 'Casually says the price is a little high and asks for a discount.',
1078: 'Feminine voice reacts to the expensive price and expects the seller can go lower.',
1079: 'Roughly protests that the price is far too high and says the seller should be able to lower it.',
1080: 'Older voice says the price is expensive and expects it can be lowered.',
1081: 'Hesitates at the high price and seeks agreement that the seller will give a greater discount.',
1082: 'Courteous voice observes the high price and asks if it can be cheaper.',
1083: 'Merchant reluctantly agrees to the newly supplied gold-coin price.',
1084: 'Merchant protests that the player possesses no saleable item.',
1085: 'Merchant asks which item the player will sell.',
1086: 'Merchant considers the item,offers the supplied number of gold coins,and asks if that is acceptable.',
1087: 'Politely protests that the offer is a joke for a one-of-a-kind object and asks the seller to look more carefully.',
1088: 'Skeptically asks whether the merchant really intends to buy such a fine item at that price.',
1089: 'Emphatically calls the item very valuable and asks whether it was properly inspected.',
1090: 'Protests the price and warns that passing up this opportunity may mean never obtaining such an item again.',
1091: 'Rough voice calls the offer a joke for a peerless item and insists on a closer look.',
1092: 'Older voice reacts in disbelief,says the item value is not understood,and demands closer inspection.',
1093: 'Casually protests that the offer is too low and asks for a thorough look at this highly valuable object.',
1094: 'Courteous voice calls the offer a joke for a fine piece and questions whether the merchant recognizes its value.',
1095: 'Merchant relents and offers the newly supplied amount of gold coins.',
1096: 'Merchant gives a rough friendly thank-you.',
1097: 'Guild courier offers to undertake delivery of diplomatic documents to another faction for1000 gold coins.',
1098: 'Politely asks the player to select the faction targeted by the specified diplomatic action.',
1099: 'Casually asks who should be targeted by the specified diplomatic action.',
1100: 'Older voice asks who is the target of the specified diplomatic action.',
1101: 'Young casual voice asks which faction is to be targeted by the specified diplomatic action.',
1102: 'Courteous older voice asks which faction is the target of the specified diplomatic action.',
1103: 'Asks the player to select the enemy the allied factions will oppose together.',
1104: 'Casually asks which enemy will be jointly opposed.',
1105: 'Older voice asks whom the factions will oppose together.',
1106: 'Young voice asks who the opponent in the intended fight will be.',
1107: 'Courteous voice asks which faction will be jointly resisted.',
1108: 'Politely confirms a pact with the first supplied faction to jointly oppose the second.',
1109: 'Casually confirms making a pact with the first supplied faction against the second.',
1110: 'Older voice confirms an agreement with the first supplied faction to jointly oppose the second.',
1111: 'Young voice confirms a promise to team up with the first supplied faction against the second.',
1112: 'Courteous older voice confirms a pact with the first supplied faction against the second.',
1113: 'Politely confirms sending the second supplied letter type to the first supplied recipient faction.',
1114: 'Casually confirms sending the second supplied letter type to the first supplied recipient faction.',
1115: 'Older voice confirms sending the second supplied letter type to the first supplied recipient faction.',
1116: 'Young voice confirms sending the second supplied letter type to the first supplied recipient faction.',
1117: 'First Mate offers to draft a diplomatic letter and asks what its contents should be.',
1118: 'Casual voice offers to write the diplomatic letter and asks its contents;IC is a first-person pronoun.',
1119: 'Rough voice offers to write the diplomatic letter for the player and asks what it should say.',
1120: 'Older voice offers to compose the diplomatic letter and asks what to put in it.',
1121: 'Young voice offers to write the letter and asks its contents.',
1122: 'Courteous older voice offers to compose the diplomatic letter and asks its contents.',
1123: 'Guild courier assures the player that the letter will be properly delivered.',
1124: 'Politely addresses the admiral and says no faction in this sea region can be sent a diplomatic letter.',
1125: 'Casually realizes that no faction in the current sea region can receive a diplomatic letter.',
1126: 'Rough voice recalls that there is no appropriate recipient for a diplomatic letter in this sea region.',
1127: 'Older voice addresses the admiral and says no faction in the current sea region can receive a diplomatic letter.',
1128: 'Young voice remembers that no one in this sea region can receive a diplomatic letter.',
1129: 'Courteous older voice admits no faction in this sea region is available to receive a diplomatic letter.',
1130: 'Apologizes that all couriers are out and asks the player to wait five or six days.',
1131: 'States there is no faction available to oppose jointly.',
1132: 'Politely states there is no enemy for the intended joint opposition.',
1133: 'Casually states there is no faction to oppose together;this is an absence statement,not a selection question.',
1134: 'Rough voice says there is no opponent to face jointly.',
1135: 'Older voice states there is no faction for the intended joint opposition.',
1136: 'Young voice says there is nobody to cooperate in defeating.',
1137: 'Courteous older voice states there is no enemy for the intended joint opposition.',
1138: 'Doubts that the supplied faction would become subordinate and asks whether to proceed.',
1139: 'Formally cannot imagine the supplied faction coming under player command and asks for confirmation.',
1140: 'Casual voice cannot imagine the supplied faction submitting to the speakers group and asks if the player really intends to act;IC plural is our group.',
1141: 'Feminine voice cannot imagine the supplied faction submitting and asks whether the player really means to proceed.',
1142: 'Rough voice sees the supplied faction submitting as impossible but asks whether to try anyway.',
1143: 'Older voice cannot imagine the supplied faction coming under player command and questions the intent to try.',
1144: 'Young voice thinks the supplied faction will certainly not surrender and asks whether to try anyway.',
1145: 'Courteous older voice doubts that the supplied faction will become subordinate and asks for confirmation.',
}

# Contextual nominal forms preserve all six original types in grammatical English.
# This is a proposal requiring owned runtime storage/routing;it is not a getter patch.
TYPE_PHRASES = ('goodwill letter', 'pact proposal', 'notice of pact termination',
                'truce proposal', 'declaration of war', 'demand for submission')


def arguments(n):
    if n in (1072, 1073, 1083, 1086, 1095): return ['native_gold_coin_amount_without_unit']
    if 1098 <= n <= 1102: return ['native_diplomatic_type_localized_as_nominal_phrase']
    if 1108 <= n <= 1112: return ['partner_faction_name', 'opponent_faction_name']
    if 1113 <= n <= 1116: return ['recipient_faction_name', 'native_diplomatic_type_localized_as_nominal_phrase']
    if 1138 <= n <= 1145: return ['target_faction_name']
    return []


def main():
    assert set(TEXTS) == set(GLOSSES) == set(range(1070, 1146))
    proof = read(ROOT/'native_context.json')
    assert proof['all76_context_IDs'] == list(range(1070, 1146))
    assert len(proof['all2080_actor_voice_selections']) == 2080
    paths = [Path('work/clean.nds'), Path('out/raphael_natural_v2_accepted_base.nds'), CURRENT]
    roms = [NdsImage.open(p) for p in paths]
    arms, commons = [[r.read_file(p) for r in roms] for p in ('/__arm9__.bin', '/COMMON/MESFILE.DK4')]
    entries = [common_message_entries(c, a, clean=i == 0) for i, (c, a) in enumerate(zip(commons, arms))]
    pins = [{'path': str(p), 'ROM_sha256': sha(p.read_bytes()), 'ARM9_sha256': sha(a), 'COMMON_sha256': sha(c)}
            for p, a, c in zip(paths, arms, commons)]
    assert pins[2]['ROM_sha256'] == proof['candidate_sha256']
    packet, rows = [], []
    for n in range(1067, 1149):
        original, canonical, current = [e[n] for e in entries]
        references = [{**asdict(e), 'text': None} for e in (original, current)]
        packet.append({'message_id': n, 'source_hex': original.text.hex(), 'Japanese': original.text.decode('cp932'),
                       'current_hex': current.text.hex(), 'current_English': current.text.decode('cp932'),
                       'source_reference': references[0], 'current_reference': references[1]})
        if n not in TEXTS:
            continue
        text, args = TEXTS[n], arguments(n)
        assert text.isascii() and text == ' '.join(text.split())
        assert text.count('%s') == original.text.count(b'%s') == len(args)
        table = next((k for k, values in TABLES.items() if n in values), None)
        if 1075 <= n <= 1082 or 1087 <= n <= 1094:
            speaker = 'Original role3 Purser speech provider, with native fallback'
            context = 'Original item buy/sell bargaining calls53D44 with role3;the source initializer selects Purser,not the captain. The eight native voice alternatives are independent selections.'
        elif 1098 <= n <= 1122 or 1124 <= n <= 1129 or 1131 <= n <= 1145:
            speaker = 'Original role1 First Mate speech provider, with native fallback'
            context = 'Original Guild diplomatic-letter flow uses role1 through53D44 for statements or53CB0 for confirmation tables. These are independent native voice alternatives,not sequential stored pages.'
        else:
            speaker = 'Original selected Guild merchant/courier NPC'
            context = 'Original item buy/sell or diplomatic courier call selects the current building NPC through B2CD8 and the menu context role field. Original calling fragments establish the message;complete constructor/core binding remains a production gate.'
        note = 'Faithful natural American English,read with the original branch meaning and related voice alternatives. One paragraph;do not preserve manual padding or line breaks.'
        if n == 1072:
            note += ' The insufficient-funds branch does not ask whether to buy;remove the old invented purchase question while preserving the merchant taunt.'
        if n in (1072, 1073, 1083, 1086, 1095):
            note += ' OriginalABF50 supplies full-width digits without a currency unit. The prose supplies coins exactly once;do not reuse another family currency/day helper blindly.'
        if n == 1097:
            note += ' This is a1000-coin courier service fee,not a paid job reward. Original5BB00 subtracts1000 after dispatch.'
        if 1098 <= n <= 1102 or 1113 <= n <= 1116:
            note += ' Current93D5C still returns six Japanese type strings. This draft requires their faithful contextual nominal English phrases from the explicit type-localization proposal. These proposed values are not current getter output or production approval;no Japanese/English hybrid may ship.'
        if 1108 <= n <= 1112:
            note += ' Preserve partner first and opponent second;do not swap the ally and enemy or imply a new successful outcome.'
        if 1113 <= n <= 1116:
            note += ' Preserve recipient first and letter type second;the source second placeholder is a document type,not an owner or faction name.'
        if n in (1118, 1140):
            note += ' IC is the original first-person pronoun token. Use I or our according to grammar;do not invent an actor name. Both exact inherited literal guards retain IC behavior.'
        if 1117 <= n <= 1122 or 1124 <= n <= 1129 or 1131 <= n <= 1137:
            note += ' Restore drafting or absence meaning where earlier English repeated an unrelated faction-choice question. Do not turn an unavailable action into an active selection prompt.'
        if 1138 <= n <= 1145:
            note += ' Preserve the low-confidence submission warning and the confirmation question. The source does not ask which faction to oppose and does not guarantee surrender.'
        current_normal = ' '.join(current.text.decode('cp932').replace('\uff29', 'I').replace('\uff26', 'F').split())
        rows.append({'id': f'COMMON_MESSAGE_{n}', 'message_id': n, 'interaction_group': 'Guild-item-bargaining-and-diplomatic-letters',
            'source_hex': original.text.hex(), 'japanese': original.text.decode('cp932'), 'source_reference': references[0],
            'canonical_source_hex': canonical.text.hex(), 'current_text_hex': current.text.hex(),
            'current_English': current.text.decode('cp932'), 'current_reference': references[1],
            'english': text+'{PAD}', 'source_meaning': GLOSSES[n], 'speaker': speaker, 'context': context,
            'localization_note': note, 'source_voice_table': table, 'source_native_arguments': args,
            'English_argument_source_indices': list(range(len(args))),
            'decision': 'retain' if text == current_normal else 'revise',
            'review': {'source': True, 'context': True, 'localization': True, 'naturalness': True, 'formatting': False},
            'status': 'source-prose-draft-native-formatting-argument-localization-and-production-pending'})
    save(ROOT/'source_and_neighbors.json', {'source_pins': pins, 'entries': packet})
    save(ROOT/'letter_type_localization_DRAFT.json', {
        'source_getter': 0x02093D5C, 'source_current_runtime_values': proof['all_six_current_runtime_letter_types'],
        'proposed_contextual_nominal_phrases': [{'type': i, 'English': s} for i, s in enumerate(TYPE_PHRASES)],
        'consumer_IDs': [*range(1098, 1103), *range(1113, 1117)],
        'established_menu_action_labels_retained': ['Goodwill', 'Sign Pact', 'Break Pact', 'Truce', 'Declare War', 'Threaten'],
        'contextual_grammar_is_not_a_menu_rename': True,
        'owned_storage_native_routing_all_getter_consumers_and_gameplay_pending': True,
        'no_ROM_change': True})
    save(MANUSCRIPT, {'format': 'dk4-common-entry-manuscript-v1', 'translation_policy': 'natural-dialogue-v2',
        'encoder': 'dialogue-fixed-v1', 'target_locale': 'en-US',
        'review_gates': ['source', 'context', 'localization', 'naturalness', 'formatting'],
        'file_path': '/COMMON/MESFILE.DK4', 'source_pins': pins,
        'native_context_proof': str(ROOT/'native_context.json'),
        'required_letter_type_localization': str(ROOT/'letter_type_localization_DRAFT.json'),
        'status': 'source-and-prose-reviewed-not-formatting-approved-or-integrated', 'records': rows})
    print('76 source/context/prose drafts:', dict(Counter(r['decision'] for r in rows)), ';all formatting approvals false;no ROM changed.', flush=True)


if __name__ == '__main__':
    main()
