"""Review Maria's final flagged story wraps and adjacent clue and letter corrections."""

import argparse
from pathlib import Path
from types import FunctionType

from scripts import register_maria_late_wraps_20261114 as parent
from scripts import stage_maria_opening_wraps_20261114 as previous
from scripts.source_locked_derivation_v5118 import checked_text


base, sha, prior = previous.base, previous.sha, previous.prior
FILE, ARM, CLEAN, IlnkContainer = previous.FILE, previous.ARM, previous.CLEAN, previous.IlnkContainer
ROOT = Path('work/maria_final_wraps_20261114_v1')
CAPTURE = ROOT / 'maria_startup/capture_report.json'
RUNTIME = ROOT / 'maria_native_context.json'
REVIEW = parent.TRIAGE.with_name('maria_final_wraps_context_v1.json')
PROOF = ROOT / 'stored_and_native.json'
native, expanded, expand_bytes = previous.native, previous.expanded, previous.expand_bytes
initial_names = previous.initial_names

# Exact current offsets for the linked letter signature and clue correction.
EXTRA = {
    (209, 48): (969, b'Jam Jack Ludwyan'),
    (212, 105): (1021, b'I thought you knew the thief'),
}

DECISIONS = {
    (200, 8): ("Maria", "Training this late? Don't wear yourself out.",
        "Maria notices Yifa training late and cautions her not to overwork herself if she wants to keep going.",
        "Keep Maria's concern in response to the sounds of practice, before Yifa explains what takes courage.",
        ("Don't wear yourself out.",)),
    (200, 15): ("Yifa", "If fear of the blade makes you hesitate when you move in, you'll set yourself up for a nasty injury. That's why you need the nerve to face fear head-on.",
        "Yifa says that half-committing out of fear makes serious injury more likely and that courage matters.",
        "Let her speak with the confidence of someone who trains. It follows her admission that facing a sword is frightening and leads into the armor rumor.",
        ("If fear of the blade", "when you move in,", "a nasty injury.", "face fear head-on.",)),
    (200, 18): ("Yifa", "That reminds me. I heard there's a training uniform so tough a sword can chip on it. Have you heard of it?",
        "Yifa asks about a martial arts uniform reportedly tough enough to chip a sword on impact.",
        "Keep the rumor as a follow-up to her advice about courage, with a direct question that draws Maria's doubt.",
        ("a training uniform", "a sword can chip on it.", "Have you heard of it?",)),
    (204, 11): ("Carlo", "Herophilus was an ancient physician. He wrote the world's oldest medical book.",
        "Carlo identifies Herophilus as a physician from long ago who left behind the oldest medical book in the world.",
        "Keep the game character's historical claim in his speech. The explanation answers Maria's question about the unfamiliar name.",
        ("Herophilus was an ancient physician.", "the world's oldest medical book.",)),
    (209, 41): ("Jam", "But nobody's selling it. I can't even find anyone who's seen it.",
        "Jam has found neither a seller nor anyone who has seen the object.",
        "His frustration follows his hope to beat Fernando at gambling. He next asks Maria to look for the item herself.",
        ("nobody's selling it.", "anyone who's seen it.",)),
    (209, 48): ("Jam", "Oops! I've got to set sail. Hope you find the treasure. See ya! -- Jam Jack Ludwyan",
        "Jam says he should sail soon, wishes the crew luck in finding the treasure and signs his letter.",
        "Keep his easy farewell and full signature. Put the signature on its own line as in the Japanese. Fernando reacts to the letter next.",
        ("I've got to set sail.", "Hope you find the treasure. See ya!", "-- Jam Jack Ludwyan",)),
    (209, 63): ("Fernando", "Hah! Beating me with a trinket? He's five hundred years too early!",
        "Fernando scoffs at Jam's plan to beat him with the object, saying Jam is five hundred years too early.",
        "Keep the five-hundred-year boast as his answer to the letter, before Maria laughs at how little they have changed.",
        ("Beating me with a trinket?", "five hundred years too early!",)),
    (211, 61): ("Port Worker", "That's right, the Jutland Peninsula! No doubt about it. It's true! You've got to believe me!",
        "The worker confirms Jutland and repeatedly insists he is telling the truth.",
        "Keep his insistence after the question about Denmark. Maria agrees to search without endorsing the claim.",
        ("the Jutland Peninsula!", "No doubt about it.", "You've got to believe me!",)),
    (212, 105): ("Maria", "That's tricky. From what you said earlier, I thought the thief might be in the New World...",
        "Maria sees the difficulty and recalls suspecting from the earlier conversation that the thief might be in the New World.",
        "Keep the suspicion Maria's own and leave it tentative. Francisca follows with a report from a friend of a friend.",
        ("From what you said earlier,", "the thief might be", "in the New World...",)),
    (212, 109): ("Francisca", "A friend of a friend told me about a swindler in Havana who passes off glass ornaments as jade or crystal. They charge a fortune for them.",
        "The speaker heard through a friend about a Havana swindler charging high prices for glass objects advertised as jade or crystal.",
        "Keep it an indirect lead before Xien cautions that it does not prove the swindler is the thief.",
        ("A friend of a friend", "a swindler in Havana", "glass ornaments as jade or crystal.", "They charge a fortune for them.",)),
    (213, 102): ("Barkeep", "Thanks! He nearly fooled me. This is what you came for, right?",
        "The barkeep thanks them, says he was nearly duped and asks if this is what they sought.",
        "Keep the near miss after the swindler escapes. The next line asks them to return it to its owner.",
        ("He nearly fooled me.", "what you came for, right?",)),
    (214, 9): ("Maria", "Is this the stolen ornament?",
        "Maria tentatively identifies the recovered ornament as the stolen one.",
        "Keep it as a question until Francisca recognizes it. Avoid the implication of an accident by identifying the actual theft.",
        ("the stolen ornament?",)),
    (214, 43): ("Francisca", "You explore the world, don't you?",
        "Francisca asks whether the crew explores around the world.",
        "Keep her friendly question after she calls them back, before she recommends the church.",
        ("the world, don't you?",)),
    (221, 5): ("Fernando", "Admiral, over here! There's writing on the wall!",
        "Fernando calls the admiral over to see something written on the wall.",
        "Use Fernando's urgent call and the same discovery wording as the parallel route. The next panel gives the riddle.",
        ("Admiral, over here!", "There's writing on the wall!",)),
    (221, 172): ("Fernando", "What was that about? If we use it, we won't be cursed, will we?",
        "Fernando wonders what happened and asks if using the object might curse the crew.",
        "Put the question tag with the question after the apparition hands over the statue. Maria teases him with uncertainty.",
        ("What was that about?", "we won't be cursed, will we?",)),
    (225, 24): ("Guildmaster", "All I know is he's hiding somewhere around Indonesia.",
        "The speaker's only lead places Plett somewhere around Indonesia.",
        "Keep the purposeful disclosure after the guildmaster pretends he cannot ask for such a favor. Maria sees through his approach.",
        ("hiding somewhere around Indonesia.",)),
    (226, 23): ("Plett", "N-no point in hiding it now. I'm Plett Perrault, all right.",
        "Plett stammers that he has been found out and confirms his full name.",
        "Let his nervous confession answer Maria's identification. It leads to her comment on his surprising honesty.",
        ("N-no point in hiding it now.", "Plett Perrault, all right.",)),
    (227, 11): ("Guildmaster", "I-I see. Sorry for the trouble. It's so little I'm embarrassed to offer it, but please take it...",
        "The guildmaster stammers an apology and offers a payment so small he fears it might be insulting.",
        "Keep the apologetic humility before the separate reward notice shows the amount. Avoid treating his self-deprecation as a change to the amount.",
        ("I-I see.", "please take it",)),
    (230, 49): ("Jean", "N-now, listen. I'm no smuggler. Hah! I mean it. No smuggling. You can take my word for it. That's right!",
        "Jean nervously repeats that he is not a smuggler and asks his listeners to take his word for it.",
        "Keep his forced laugh and repeated denial after the witness calls him a liar. Maria cuts through his protest.",
        ("N-now, listen.", "You can take my word for it.",)),
    (231, 11): ("Guildmaster", "Now that you're cornered, you get defiant? You're pathetic.",
        "The guildmaster scorns Jean for becoming defiant when cornered.",
        "Keep his contempt after Jean switches from denials to defending smuggling. He turns to thank the crew next.",
        ("Now that you're cornered,", "You're pathetic.",)),
    (233, 13): ("Guildmaster", "Find Peralonso Aguirre, a Spanish spy. Word is he's operating around Southeast Asia.",
        "The guildmaster asks the crew to find a Spanish spy reportedly active around Southeast Asia.",
        "Use the same full name and broad reported location as the parallel mission. Maria then comments on why she is suited to it.",
        ("Peralonso Aguirre,", "a Spanish spy.", "around Southeast Asia.",)),
    (234, 21): ("Maria", "Barkeep, I'm after Peralonso Aguirre.",
        "Maria ignores the interruption and asks the barkeep for the man by name.",
        "Keep this as a search request rather than assuming the barkeep knows where he is. The man answers for himself.",
        ("I'm after", "Peralonso Aguirre.",)),
    (239, 23): ("Guildmaster", "Word is Yuris the ship thief is hiding in Southeast Asia.",
        "The guildmaster says the ship thief Yuris is reportedly hiding in Southeast Asia.",
        "Keep the report tentative as it follows Maria's recollection of where to find his fleet.",
        ("Yuris the ship thief", "in Southeast Asia.",)),
    (249, 14): ("Guildmaster", "I hear he's prowling the Mediterranean. I'm counting on you. Here's your advance.",
        "The guildmaster relays a report of the outlaw in the Mediterranean and gives an advance.",
        "Keep the location hearsay and distinguish the advance from a completed reward. The exact amount appears next.",
        ("prowling the Mediterranean.", "I'm counting on you.", "Here's your advance.",)),
    (250, 58): ("Guildmaster", "Say, have you seen our landmark yet?",
        "The guildmaster remembers to ask if the crew has visited the town's notable sight.",
        "Keep the casual change of topic after the Athens share increase. Maria asks what landmark he means.",
        ("seen our landmark yet?",)),
    (253, 5): ("Port Worker", "There you are! You're {MACRO:FA}, right? The London Guild's been looking for you.",
        "The worker checks the listener's family name and says the London Guild has been looking for her.",
        "Give the personal tag and the sender room to read together. Match the approved guild name and preserve the family-name substitution.",
        ("There you are!", "You're {MACRO:FA}, right?", "The London Guild's",)),
    (256, 17): ("Maria", "So Lime Drops cure scurvy. I'd better get them to the London Guild...",
        "Maria recognizes Lime Drops as the remedy for scurvy and reminds herself to deliver them promptly to the London Guild.",
        "Keep the connection to her earlier question about finding the remedy and make the delivery destination clear.",
        ("So Lime Drops cure scurvy.", "the London Guild...",)),
    (258, 51): ("Guildmaster", "Yes, a little way from London. A map will get you there easily. One thing, though. Some odd folks have been hanging around there lately.",
        "The guildmaster says the ruins are some distance from London, accessible with a map, and that odd people have been spending time there lately.",
        "Keep the practical map advice together and let the warning lead into Maria asking about the strange people.",
        ("a little way from London.", "A map will get you there easily.", "One thing, though.", "hanging around there lately.",)),
    (259, 39): ("Xien", "Must be this jungle air. Wild beasts lurk here, Admiral. Let's pick our path carefully.",
        "Xien attributes the humidity to the jungle and warns that wild animals lurk there, urging care in choosing the route.",
        "Keep his tentative answer to Maria and the precise reason for caution before she notices the cave.",
        ("Must be this jungle air.", "Wild beasts lurk here, Admiral.", "Let's pick our path carefully.",)),
    (260, 4): ("Guildmaster", "Hey, {MACRO:FI}. You're from China. You know about shark fin, right?",
        "The guildmaster greets Maria and asks if someone from China knows about shark fin.",
        "Use a familiar direct address. Keep the specific food and his assumption before he explains the ruler's request.",
        ("You're from China.", "shark fin, right?",)),
    (261, 67): ("Maria", "An ancient kingdom... That's hard to believe.",
        "Maria reacts skeptically to the report of an ancient kingdom.",
        "Her understated doubt fits between the account of intact ruins and the guildmaster admitting it is only a rumor.",
        ("An ancient kingdom...", "That's hard to believe.",)),
    (265, 5): ("Patron", "The Istanbul Guild's looking for you.",
        "The patron says the Istanbul Guild has been looking for the listener.",
        "Keep this routine directional line short and identify the guild and city fully.",
        ("The Istanbul Guild's",)),
    (267, 108): ("Xien", "Looks like everyone got out safely.",
        "Xien thinks everyone has escaped unharmed.",
        "His relief answers the immediate danger before Maria's hesitant agreement.",
        ("everyone got out safely.",)),
    (267, 170): ("Maria", "Yes... Thanks. I'm all right now. But a bog in a place like this...",
        "Maria thanks Xien and says she is all right, then expresses surprise at a bog in such a place.",
        "Keep the reassurance and trailing surprise before the crew's fatigue appears.",
        ("I'm all right now.", "a bog in a place like this...",)),
    (270, 15): ("Safia", "There's a mosque far inland that honors a king from long ago. They say it holds quite a treasure.",
        "Safia says a mosque far inland commemorates a former king and reportedly contains a wonderful treasure.",
        "Use the parallel wording from the other routes, then leave the restriction on claiming it to her next line.",
        ("a mosque far inland", "a king from long ago.", "They say it holds quite a treasure.",)),
    (271, 287): ("Cesare", "This material should hold up well!",
        "Cesare expects the material will be difficult to break.",
        "Let his confidence follow the cannon damage assessment. He explains where to add armor in the next turn.",
        ("should hold up well!",)),
    (272, 89): ("Cesare", "This material should hold up well!",
        "Cesare expects the material will be difficult to break.",
        "Keep the same prediction in the other version of the cannon and armor exchange.",
        ("should hold up well!",)),
    (273, 14): ("Guildmaster", "Thanks on the shipwright's behalf.",
        "The guildmaster asks to thank the crew on the shipwright's behalf.",
        "Keep the thanks on behalf of the shipwright, introducing the separate reward.",
        ("on the shipwright's behalf.",)),
    (275, 91): ("Patron", "Once your hands are dirty, you can't go straight again. You're in it till you die.",
        "The man thinks that once someone enters criminal life, they can never go straight as long as they live.",
        "Keep his fatalism after he says they are pursuing him. Maria immediately insists that an honest living is still possible.",
        ("can't go straight again.", "You're in it till you die.",)),
    (275, 98): ("Maria", "They'd only be after your life if you knew one of their secrets.",
        "Maria infers that they would not be trying to kill him unless he knew a secret of theirs.",
        "Bring back the actual danger after Maria has told him he can still go straight. He begins to consider what he might know.",
        ("after your life", "one of their secrets.",)),
    (275, 128): ("Patron", "Dunno. The boss was tight-lipped about that. Kept telling a lout like me to stay away from such distinguished guests.",
        "The man does not know the time or port because the boss kept quiet and repeatedly told an uncouth man like him to avoid their distinguished guests.",
        "Keep his informal self-deprecation and the boss's instruction after Maria asks for details. His next comment treats the missionaries wryly.",
        ("was tight-lipped about that.", "a lout like me", "distinguished guests.",)),
    (275, 151): ("Patron", "Hurt or not, I'm safer on your ship than I am in this town. You see that, don't you, Admiral? You're a sharp one.",
        "The injured man says he expects it would be safer to go aboard than stay in town and appeals to Maria's judgment as a capable admiral.",
        "Keep the practical comparison and the coaxing address after Sakura objects to him boarding in his condition.",
        ("safer on your ship", "in this town.", "don't you, Admiral?", "You're a sharp one.",)),
    (277, 139): ("Maria", "They're headed to the governor's office. Hurry!",
        "Maria says the group has gone toward the governor's office and tells her own companions to hurry.",
        "Keep her decision brisk after they realize they may have to act themselves.",
        ("the governor's office.",)),
    (278, 111): ("Governor", "Oh... They left without a word to me?",
        "The governor is puzzled that they left without coming to greet him.",
        "Let the quiet question follow the report they left. He goes on to wonder about the presence of Westerners and Japanese in the Ming army.",
        ("They left without a word to me?",)),
    (279, 38): ("Sakura", "Why not visit Kyoto? It's easy to get there with a map. I can show you part of the way.",
        "Sakura suggests sightseeing in Kyoto, says a map makes it easy, and offers to guide them partway.",
        "Keep her friendly offer and the limit on her guidance after the crew prepares to leave.",
        ("Why not visit Kyoto?", "with a map.", "part of the way.",)),
    (286, 13): ("Verisa", "They say it makes fortune-telling much more accurate. I'd love to try it just once...",
        "Verisa has heard the burner makes divinations more accurate and wishes to use it once.",
        "Use the phrasing from the parallel artifact conversation, with the claim attributed and her wish left personal.",
        ("much more accurate.", "I'd love to try it just once...",)),
    (287, 23): ("Guildmaster", "Our guards are struggling. They have little experience fighting on land, and they're short on weapons and armor.",
        "The guards have little experience fighting on land and lack weapons and armor, so they are struggling.",
        "Keep both causes after the description of the well-trained attackers. The guildmaster's request for armor follows.",
        ("Our guards are struggling.", "fighting on land,", "short on weapons and armor.",)),
    (290, 47): ("Maria", "And where's the bandits' hideout?",
        "Maria asks the guildmaster where the bandits are based.",
        "After the reward notice, Maria asks for the next lead. The guildmaster is surprised she wants to go after them.",
        ("the bandits' hideout?",)),
    (293, 78): ("Villager", "We're here. We continue overland.",
        "The guide announces arrival and says they will continue by land.",
        "Use the same direct transition as the parallel expeditions. The next sight confirms they have reached the trail toward the discovery.",
        ("We continue overland.",)),
    (296, 93): ("Villager", None,
        "The villager admits they have been asking anyone who looks strong to help.",
        "The candid wording works after he admits the search is vague. His next remark about failure prompts Maria's joke.",
        ("anyone who looks strong", "asking you now.",)),
    (296, 123): ("Villager", "First, we'll need the Ancient City Map. Let me know when you find it. I'll go with you.",
        "The villager asks the crew to obtain the Ancient City Map, tell him when they have it and let him accompany the search.",
        "Keep the exact item name and distinguish the map as a prerequisite from the nonrefundable advance. The next instruction sets the meeting point.",
        ("the Ancient City Map.", "Let me know", "I'll go with you.",)),
}


pair_source = checked_text(previous.get_source, {
    'extras = {712} if block == 87 else set()': 'extras = set()',
    """            if en['offset'] not in leads:
                continue
            lead = leads[en['offset']]
            assert en['raw_hex'][2:] == lead['stored_body_hex'] and en['selector'] == lead['source_selector']""":
        """            linked = EXTRA.get((block, ja['record_index']))
            if linked is None:
                if en['offset'] not in leads:
                    continue
                lead = leads[en['offset']]
                assert en['raw_hex'][2:] == lead['stored_body_hex'] and en['selector'] == lead['source_selector']
            else:
                offset, anchor = linked
                assert en['offset'] == offset and offset not in leads
                assert anchor in bytes.fromhex(en['raw_hex'])[1:]""",
})
env = previous.get_exchanges.__globals__ | globals()
exec(compile(pair_source, __file__ + '::original-Maria-commands-and-linked-letter-and-clue', 'exec'), env)
get_exchanges = env['get_exchanges']

# Four rows can store at most three 35-cell lines, one 36-cell line and three LF bytes.
contract_source = checked_text(previous.contract_source, {
    "'if line==4:': 'if line==limit:',": """'if line==4:': 'if line==limit:',
        'if tail is None:continue':
            'if tail is None or (final and line < 4 and len(bytes.fromhex(row["current_hex"])) - 1 > 144):continue',
        'tiny=int(final and start>0 and (stop-start==1 or length<=8))':
            'tiny=int((final and start>0 and (stop-start==1 or length<=8)) or (not final and not terminal and length<12))',""",
})
env = previous.contract.__globals__ | globals() | {'previous': initial_names}
exec(compile(contract_source, __file__ + '::native-four-row-storage-limit', 'exec'), env)
contract = env['contract']
compile_rows = FunctionType(previous.compile_rows.__code__, previous.compile_rows.__globals__ | globals()
                            | {'previous': initial_names})
bind_runtime = FunctionType(previous.bind_runtime.__code__, previous.bind_runtime.__globals__ | globals())
main = FunctionType(previous.main.__code__, previous.main.__globals__ | globals())


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--preview', action='store_true')
    main(parser.parse_args().preview)
