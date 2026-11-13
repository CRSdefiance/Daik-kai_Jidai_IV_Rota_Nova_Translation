"""Source-led drafts for the next 50 shared entries; no release approval."""

from dataclasses import asdict
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import common_message_entries
from scripts.context_shared_dialogue_v781 import ROOT, CURRENT, TABLES
from scripts.verify_village_wrap_v608 import read, save

MANUSCRIPT = Path('translations/shared_dialogue_editorial_manuscript_v1.json')
TEXTS = {
    1020: "We have no information on the towns where that faction has contracts.",
    1021: "I really don't think this will work... Are you sure?",
    1022: "The chances of success seem very low... Do you want to proceed?",
    1023: "I don't think there's much chance of success... Want to try anyway?",
    1024: "...Looks like the odds of success are pretty low. Still want to try?",
    1025: "I can't see this working at all... Are you sure?",
    1026: "I don't think we can pull this off... Want to try anyway?",
    1027: "There's almost no hope of success... Shall we try anyway?",
    1028: "Did you know? There's a village near %s where you can get supplies.",
    1029: "Have you heard? There's a village near %s where you can get supplies.",
    1030: "They say an unfamiliar fleet is anchored at %s.",
    1031: "An unknown fleet is bound for %s.",
    1032: "Some strange fleet is headed to %s.",
    1033: "An unknown fleet is anchored at %s.",
    1034: "I don't know whose fleet it is, but it's anchored at %s.",
    1035: "You're still %s short of the crew you need. Shall I recruit more?",
    1036: "You're still %s short of the crew you need. Should I recruit more?",
    1037: "You're still %s short of the crew you need. Would you like me to recruit more?",
    1038: "You're still %s short of the crew you need. Want me to round up some more?",
    1039: "You're still %s short of the crew you need. Shall I recruit some more?",
    1040: "We couldn't get the whole crew you need. You're still %s short. Want me to try again?",
    1041: "You're still %s short of the crew you need. Shall I try recruiting more?",
    1042: "There's still room for %s more aboard. Shall I recruit more?",
    1043: "You've still got room for %s more aboard. Should I recruit more?",
    1044: "There's still room for %s more aboard. Would you like me to recruit more?",
    1045: "You've still got room for %s more aboard. Want me to round up some more?",
    1046: "There seems to be room for %s more aboard. Shall I recruit some more?",
    1047: "Looks like you can take %s more aboard. Want me to recruit more?",
    1048: "There's still room for %s more aboard. Shall I try recruiting more?",
    1049: "What a lovely afternoon. Let's open the window and let the breeze in.",
    1050: "I'm not all that interested in romance. Call me childish, but I'd rather be here having fun with everyone.",
    1051: "Mom worked here for a long time. She was everyone's favorite. I'll work hard and outdo her someday!",
    1052: "Cooking is so much fun. Seeing you enjoy my food makes me happier than anything... Oh, listen to me!",
    1053: "I'm so glad everyone likes my singing. I want to help Mom, even a little. Ever since Dad left, she's been working nonstop...",
    1054: "I'd love to visit faraway lands. Imagine a huge castle unlike any I've seen, with a charming foreign prince... Oh, my!",
    1055: "Never fall in love with a sailor. All that waiting, never knowing when he'll come home... But when you're in love, what can you do?",
    1056: "I can't stand people with no brains. I wish every sailor were as smart as you.",
    1057: "A woman doesn't get to be the center of attention for long. That's why I can't afford to neglect my looks.",
    1058: "Watching a fight really gets me fired up! Maybe I'm just hot-blooded.",
    1059: "I don't care much about money or luxury, but I've dreamed of being a princess ever since I was little.",
    1060: "I don't mind looking after my younger siblings. Still, sometimes I dream of marrying someone rich and escaping this life.",
    1061: "Men are so simple. Just let them feel important, and it goes straight to their heads. Is taking advantage of that sneaky of me?",
    1062: "Oh, I want a passionate romance! Isn't there someone nice out there?",
    1063: "Even if you grew up in a cultured country, you're a barbarian if you settle things by force. I hate people like that.",
    1064: "Hehe... They'll scold me for drinking too much again... but I'm having another anyway!",
    1065: "They say I go for looks, but I just love a romantic mood. If someone's not my type, though, where's the romance?",
    1066: "Talking to people from other countries is hard, with all the different languages... You do understand me, don't you?",
    1067: "Thanks for always coming by. Have a drink on the house today, and take your time.",
    1068: "I'd love to try steering a ship myself. I enjoy this job, though. I get to hear stories from all sorts of people.",
    1069: "The parrot you gave me is doing great! It's mischievous, but adorable.",
}
GLOSSES = {
    1020: 'No information is available about towns with which the selected faction has contracts.',
    1021: 'Strongly doubts the attempt will succeed, then asks for confirmation.',
    1022: 'Formally estimates that the probability of success is very low and asks for confirmation.',
    1023: 'Casually considers success unlikely and asks whether to try despite that.',
    1024: 'A hesitant rough-voiced assessment of very low chances, followed by a proceed-anyway question.',
    1025: 'An elderly speaker finds success very hard to imagine and asks whether proceeding is acceptable.',
    1026: 'Softens an assessment that the attempt seems impracticable, then asks whether to try anyway.',
    1027: 'A courteous speaker sees almost no prospect of success, then asks whether to try regardless.',
    1028: 'Politely asks whether the listener knows that a resupply village exists near the supplied coordinates.',
    1029: 'A colloquial speaker introduces the same information about a resupply village near the supplied coordinates.',
    1030: 'A woman relays hearsay about an unidentified fleet anchored at the supplied town.',
    1031: 'Politely reports that an unidentified fleet is moving toward the supplied town.',
    1032: 'Colloquially reports an unidentified fleet heading for the supplied town.',
    1033: 'Politely reports an unidentified fleet anchored at the supplied town.',
    1034: 'Does not know whose fleet it is, but reports that it is anchored at the supplied town.',
    1035: 'Required sailor count remains short by the supplied number; politely asks whether to gather more.',
    1036: 'Notes the supplied shortfall from the necessary crew total and asks whether to gather more.',
    1037: 'Politely notes that the current total is the supplied number below requirements and asks whether to gather more.',
    1038: 'A rough speaker notes the supplied recruitment shortfall and asks whether to gather more.',
    1039: 'An elderly voice notes the supplied shortfall from the required sailor total and offers further recruiting.',
    1040: 'The attempt did not gather the necessary total; the supplied number is still missing, so asks about another attempt.',
    1041: 'A courteous elderly voice notes the supplied shortage against requirements and offers further recruiting.',
    1042: 'There is cabin capacity for the supplied number of additional people; asks whether to gather more.',
    1043: 'Notes remaining space for the supplied number of people and asks whether to gather more.',
    1044: 'Politely notes remaining cabin capacity for the supplied number and asks whether to continue recruiting.',
    1045: 'A rough voice notes spare cabin space for the supplied number and offers further recruiting.',
    1046: 'An elderly voice observes that there seems to be room for the supplied number and offers another recruitment attempt.',
    1047: 'A casual young voice observes that the supplied number of additional sailors can still board, then asks about recruiting more.',
    1048: 'A courteous elderly voice notes spare capacity for the supplied number of additional people and offers further recruiting.',
    1049: 'Finds the afternoon very pleasant and refreshing; proposes opening a window to let a breeze in.',
    1050: 'Has little interest in romance and prefers making merry with everyone, even if others call her childish.',
    1051: 'Her mother worked here for a long time and was the most popular; she vows to work hard and surpass her.',
    1052: 'Enjoys cooking and feels happiest when the listener clearly enjoys her food, ending with a coy self-conscious aside.',
    1053: 'Is pleased that everyone likes her singing; wants to be of some help to her mother, who has worked constantly since her father left.',
    1054: 'Wants to visit distant countries and fantasizes about a magnificent unfamiliar castle and a charming foreign prince, then squeals.',
    1055: 'Says one should not love sailors because of endless waiting without knowing when they will return, but admits that love leaves one vulnerable.',
    1056: 'Cannot abide unintelligent people and wishes all sailors were as intelligent as the listener.',
    1057: 'Considers the time when a woman is fawned over very brief; therefore feels she cannot afford to neglect cultivating her beauty.',
    1058: 'Gets excited by watching fights and wonders whether she is hot-blooded.',
    1059: 'Has little interest in wealth or luxury but has long yearned to be a princess, since childhood.',
    1060: 'Does not regard caring for younger brothers and sisters as a burden, but sometimes dreams of marrying someone wealthy and escaping her present life.',
    1061: 'Considers men simple: a little deference makes them feel important; wonders whether taking advantage of that is sly of her.',
    1062: 'Longs for an intense passionate romance and wonders whether there is a suitable person somewhere.',
    1063: 'Calls people who solve things by force barbaric despite growing up in a culturally advanced country; strongly dislikes such people.',
    1064: 'Laughs about being scolded again for drinking too much but decides to drink anyway.',
    1065: 'Is often called looks-conscious but says she is really susceptible to romantic atmosphere; nevertheless thinks the mood cannot develop with a face she does not find attractive.',
    1066: 'Finds conversations with foreigners difficult because languages differ across countries; asks whether this listener properly understands her language.',
    1067: 'Thanks a regular visitor, offers one complimentary drink today and invites a leisurely stay.',
    1068: 'Would like to operate a ship herself, although she also enjoys hearing many different people in her current work.',
    1069: 'Reports that the parrot the listener gave her is healthy and energetic, mischievous but cute.',
}


def arguments(n):
    if n in (1028, 1029): return ['native_village_coordinate_text']
    if 1030 <= n <= 1034: return ['native_town_name']
    if 1035 <= n <= 1041: return ['required_crew_shortfall']
    if 1042 <= n <= 1048: return ['remaining_crew_capacity']
    return []


def main():
    context = read(ROOT/'native_context.json')
    assert context['candidate_sha256'] == sha(CURRENT.read_bytes())
    assert context['all50_context_IDs'] == list(range(1020, 1070))
    assert len(context['all21_private_barmaid_speeches']) == 21
    assert len(context['all624_original_actor_voice_selections']) == 624
    paths = [Path('work/clean.nds'), Path('out/raphael_natural_v2_accepted_base.nds'), CURRENT]
    roms = [NdsImage.open(p) for p in paths]
    arms = [r.read_file('/__arm9__.bin') for r in roms]
    commons = [r.read_file('/COMMON/MESFILE.DK4') for r in roms]
    entries = [common_message_entries(c, a, clean=i == 0) for i, (c, a) in enumerate(zip(commons, arms))]
    pins = [{'path': str(p), 'ROM_sha256': sha(p.read_bytes()), 'ARM9_sha256': sha(a), 'COMMON_sha256': sha(c)}
            for p, a, c in zip(paths, arms, commons)]
    sources, rows = [], []
    for n in range(1016, 1074):
        original, canonical, current = [e[n] for e in entries]
        references = [{**asdict(e), 'text': None} for e in (original, current)]
        row = {'id': n, 'source_hex': original.text.hex(), 'Japanese': original.text.decode('cp932'),
               'canonical_hex': canonical.text.hex(), 'current_hex': current.text.hex(),
               'current_English': current.text.decode('cp932'),
               'source_reference': references[0], 'current_reference': references[1]}
        sources.append(row)
        if n not in TEXTS:
            continue
        prose, args = TEXTS[n], arguments(n)
        assert prose.isascii() and prose == ' '.join(prose.split()) and '%' not in prose.replace('%s', '')
        assert prose.count('%s') == original.text.count(b'%s') == len(args)
        table = next((k for k, v in TABLES.items() if n in v), None)
        if n == 1020:
            speaker, scene = 'Role2 Strategist', 'Original56FB4 no-contract-town-information branch;one independent role message,not a continuation of neighboring private barmaid speech.'
        elif n <= 1027:
            speaker, scene = 'Role2 Strategist, original selected voice', 'Original four low-success warning sites use original voice table021181C0 through53CB0;the player chooses whether to proceed before the original job is scheduled.'
        elif n <= 1029:
            speaker, scene = 'Original selected town information NPC, formal or colloquial mode', 'Original57868 village-point getter and51580 coordinate provider reach53FE4;the argument is coordinates,not a settlement name.'
        elif n <= 1034:
            speaker = 'Original selected barmaid' if n == 1030 else 'Original selected town information NPC, formal or colloquial mode'
            scene = 'Original unknown-fleet branch:1030/1033/1034 refer to the current anchorage town;1031/1032 refer to a destination town. Each supplies one original town-name getter,not a faction or captain name.'
        elif n <= 1048:
            speaker = 'Role1 Barkeep, original selected voice'
            scene = 'Original recruitment continuation after a gathering attempt. The initializer sets role1 for both prompts.57644 supplies required-minus-gathered;57668 supplies capacity-minus-gathered. Both use originalABF50 and a53CB0 yes/no voice table.'
        else:
            binding = next(r for r in context['all21_private_barmaid_speeches'] if r['table_or_ID'] == n)
            speaker = binding['name']+' (original town barmaid)'
            scene = 'Original58F24 selects actor index+863 after the second chance choice in591D0,at relationship stage2. These are independent personal topics,not sequential pages after the neighboring stored message.'
        note = 'Preserve clean-source meaning,voice and facts in natural American English. One logical paragraph,without inherited padding or manual line breaks.'
        if 1035 <= n <= 1048:
            note += ' The barkeep recruits for the player;do not mislabel this as an officer speaking about the barkeep\'s own crew. Number-neutral wording must work for one as well as larger counts. Keep required-crew shortfall separate from spare cabin capacity.'
        elif n in (1028, 1029):
            note += ' The captured coordinate argument includes a leading LF and alignment spaces. Its complete N/S/E/W numbers require an explicitly scoped native provider/formatter route;do not globally alter the coordinate bank or treat it as a village name.'
        elif 1030 <= n <= 1034:
            note += ' Preserve anchorage versus destination and whether the speaker presents hearsay. Do not identify the unknown fleet as pirates or invent a faction.'
        if n == 1050:
            note += ' Little interest in romance is a present preference,not an invented permanent identity. Preserve her liking for company and fun.'
        elif n == 1051:
            note += ' She vows to surpass her mother,not inherit her fame. Do not add that her mother died or retired.'
        elif n == 1052:
            note += ' My food preserves her own cooking;the final self-conscious aside conveysなんてね without saying the happiness was a lie.'
        elif n == 1053:
            note += ' Restore her pleasure in the songs,her wish to help Mom and Mom\'s continuous work since Dad left. Do not turn departure into death.'
        elif n == 1054:
            note += ' Preserve the imagined distant castle and foreign prince without adding a wedding or an actual trip.'
        elif n == 1055:
            note += ' Keep the endless wait and vulnerability of being in love,without inventing death,abandonment or a named lover.'
        elif n == 1057:
            note += ' This is her personal opinion about admiration and appearance,not a new narrator claim or game rule.'
        elif n == 1059:
            note += ' Preserve both money and luxury,and the childhood wish to be a princess. Do not reduce the personal wish to detached interest in royalty.'
        elif n == 1060:
            note += ' Her younger siblings are explicit. The escape she imagines is her own;do not add that marriage will free all her siblings.'
        elif n == 1061:
            note += ' Let them feel important localizes strategic deference without adding a specific claim about intelligence. Preserve her self-directed question about exploiting it,not a generalized verdict on all women.'
        elif n == 1064:
            note += ' Keep both the anticipated scolding for excessive drinking again and her playful decision to continue.'
        elif n == 1066:
            note += ' Preserve the language barrier and her personal comprehension check;avoid telegraphic guest-list fragments.'
        elif n == 1067:
            note += ' One complimentary drink is her original offer. Do not invent a second drink,refund,discount or a new free-service mechanic.'
        elif n == 1068:
            note += ' Restore her wish to handle a ship herself,not merely observe sailing. Preserve her enjoyment of hearing different people\'s stories.'
        elif n == 1069:
            note += ' Preserve that this is the parrot the listener gave her. Its sex is unspecified;keep it rather than inventing he or she.'
        current_normal = ' '.join(row['current_English'].replace('\uff29', 'I').replace('\uff26', 'F').split())
        rows.append({'id': f'COMMON_MESSAGE_{n}', 'message_id': n, 'interaction_group': 'Shared-warnings-rumors-recruitment-and-private-barmaid-chat',
                     'source_hex': row['source_hex'], 'japanese': row['Japanese'], 'source_reference': references[0],
                     'canonical_source_hex': row['canonical_hex'], 'current_text_hex': row['current_hex'],
                     'current_English': row['current_English'], 'current_reference': references[1],
                     'english': prose+'{PAD}', 'source_meaning': GLOSSES[n], 'speaker': speaker,
                     'context': scene, 'localization_note': note, 'source_voice_table': table,
                     'source_native_arguments': args, 'English_argument_source_indices': list(range(len(args))),
                     'decision': 'retain' if prose == current_normal else 'revise',
                     'review': {'source': True, 'context': True, 'localization': True, 'naturalness': True, 'formatting': False}})
    assert len(rows) == 50
    save(ROOT/'source_and_neighbors.json', {'pins': pins, 'records': sources})
    save(MANUSCRIPT, {'format': 'dk4-common-entry-manuscript-v1', 'translation_policy': 'natural-dialogue-v2',
                     'encoder': 'dialogue-fixed-v1', 'target_locale': 'en-US',
                     'review_gates': ['source', 'context', 'localization', 'naturalness', 'formatting'],
                     'file_path': '/COMMON/MESFILE.DK4', 'source_pins': pins,
                     'native_context_proof': str(ROOT/'native_context.json'),
                     'status': 'source-and-prose-reviewed-formatting-integration-gameplay-pending', 'records': rows})
    print('50 source/context/prose drafts:', sum(r['decision'] == 'revise' for r in rows), 'revised,',
          sum(r['decision'] == 'retain' for r in rows), 'retained; formatting approvals remain false.', flush=True)


if __name__ == '__main__':
    main()
