"""Source-led31-entry conversation manuscript;production approval is separate."""

from dataclasses import asdict
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import common_message_entries
from scripts.context_barmaid_dialogue_v779 import ROOT, CURRENT
from scripts.verify_village_wrap_v608 import read, save

MANUSCRIPT = Path('translations/barmaid_editorial_manuscript_v1.json')
TEXTS = {
    989: "I'm %s. Your name is... %s? Got it! Stop by anytime. You're always welcome!",
    990: "%s? What a nice name! I'm %s. Nice to meet you!",
    991: "Are you rich? I'm jealous! I hope I find someone nice soon. I want to be happy, too.",
    992: "Stay and listen to me sing. This is fado. La la la...",
    993: "I fall in love so easily, and it always goes wrong.",
    994: "Sorry, I have to head home early today. My younger siblings are waiting for me.",
    995: "It's such a nuisance when people get drunk and fall asleep.",
    996: "Sailors risk their lives. I admire them! I must work harder too, so my parents can have an easier life.",
    997: "My age? Hehe... How old do I look?",
    998: "Take your time and relax.",
    999: "Ah! That's why I love you, %s!",
    1000: "You're giving me something this expensive? Oh, thank you!",
    1001: "Oh, thank you... You didn't have to.",
    1002: "Are you calling me Venus? Hehe... I like the sound of that.",
    1003: "Let's drink and have some fun!",
    1004: "On my days off, I always take a stroll in the garden. Seeing the flowers and trees refreshes my spirit.",
    1005: "I baked a pie. Stay and have some!",
    1006: "I can't stand stingy people. You're not like that, are you?",
    1007: "La la la... This song's about a woman waiting for her lover to return from sea. Being in love with a sailor is so hard...",
    1008: "Hey, tell me about foreign lands!",
    1009: "I love this town. It's always lively! Gloomy towns get me down.",
    1010: "Exploring ruins sounds like fun. There's something romantic about glimpsing ancient cultures and the way people lived.",
    1011: "Some people just don't keep up with fashion. I wouldn't want to walk down the street with someone like that.",
    1012: "You're wonderful... Strong, kind...",
    1013: "If something's troubling you, would you like me to tell your fortune? Oh? You don't have any worries?",
    1014: "Tired, aren't you? I'll spoil you... just a little.",
    1015: "Men go to sea and women stay home? That's outdated! Don't you think it's time women took a more active role in society, too?",
    1016: "Foreigners used to make me uneasy, but you're special.",
    1017: "Sailors are so wonderful! Have you seen dolphins? What about whales?",
    1018: "Tell me about pirates! What ships do they sail? Are they really strong?",
    1019: "Lately, people have been hunting animals for their fur. Why would anyone do something so cruel?",
}
GLOSSES = {
    989: 'Introduces herself,asks/recognizes the captain\'s name and remembers it;invites return anytime and promises a welcome.',
    990: 'Repeats and compliments the captain\'s name,then introduces herself and offers a friendly greeting.',
    991: 'Asks whether the listener is rich,is envious,and wants to find a nice romantic partner and be happy soon herself.',
    992: 'Invites listening to her singing,names fado and vocalizes a melody.',
    993: 'Falls in love easily and always ends up failing or disappointed as a result.',
    994: 'Apologizes for needing to go home early today;younger brothers/sisters are waiting there.',
    995: 'Finds people who get drunk and fall asleep troublesome.',
    996: 'Admires those who risk their lives at sea;must work harder herself and wants her parents to have an easier life.',
    997: 'Coy laugh and invitation to guess her age.',
    998: 'Invites the listener to stay and relax.',
    999: 'Delighted squeal and affectionate statement that this is why she loves the named captain.',
    1000: 'Surprised and grateful to receive something so expensive.',
    1001: 'Thanks the giver while saying they need not have gone to such trouble or overextended themself.',
    1002: 'Asks whether the gift compares her to Venus;laughs and admits being pleased by the implication.',
    1003: 'Enthusiastically invites drinking and making merry together.',
    1004: 'Always walks in the garden on days off;looking at flowers and trees makes her feel her spirit is refreshed/purified.',
    1005: 'Has baked a pie and invites the listener to eat some before leaving.',
    1006: 'Strongly dislikes stingy people and playfully asks whether the listener is different.',
    1007: 'Vocalizes a tune;explains it is about a woman waiting for her seafaring lover\'s return and reflects how hard loving a sailor is.',
    1008: 'Eagerly asks for stories about foreign lands.',
    1009: 'Likes this town because it is lively;gloomy towns depress her.',
    1010: 'Exploring ruins sounds enjoyable;glimpsing ancient people\'s culture and daily life seems romantic.',
    1011: 'Dislikes walking together with people who do not keep up with fashion.',
    1012: 'Warmly compliments the listener as wonderful,strong and kind,leaving the thought unfinished.',
    1013: 'Offers fortune-telling if the listener has troubles,then reacts to being told there are no worries.',
    1014: 'Teasingly notes tiredness and offers to indulge the listener a little.',
    1015: 'Calls the idea of men sailing and women staying home outdated;asks whether women should also take a more active role in society in the coming age.',
    1016: 'Was uncomfortable with foreigners,but regards this listener as an exception.',
    1017: 'Admires sailors and eagerly asks whether the listener has seen dolphins and whales.',
    1018: 'Eagerly asks about pirates,the ships they sail and their strength.',
    1019: 'Laments recent hunting of animals for their fur and wonders why people act so cruelly.',
}


def main():
    context = read(ROOT/'native_context.json')
    assert context['candidate_sha256'] == sha(CURRENT.read_bytes())
    assert len(context['all84_original_city_and_name_provider_cases']) == 84
    paths = [Path('work/clean.nds'), Path('out/raphael_natural_v2_accepted_base.nds'), CURRENT]
    roms = [NdsImage.open(p) for p in paths]
    arms = [r.read_file('/__arm9__.bin') for r in roms]
    commons = [r.read_file('/COMMON/MESFILE.DK4') for r in roms]
    entries = [common_message_entries(c, a, clean=i == 0) for i, (c, a) in enumerate(zip(commons, arms))]
    pins = [{'path': str(p), 'ROM_sha256': sha(p.read_bytes()), 'ARM9_sha256': sha(a), 'COMMON_sha256': sha(c)}
            for p, a, c in zip(paths, arms, commons)]
    sources, rows = [], []
    for n in range(985, 1029):
        source, canonical, current = [e[n] for e in entries]
        refs = [{**asdict(e), 'text': None} for e in (source, current)]
        s = {'id': n, 'source_hex': source.text.hex(), 'Japanese': source.text.decode('cp932'),
             'canonical_hex': canonical.text.hex(), 'current_hex': current.text.hex(),
             'current_English': current.text.decode('cp932'), 'source_reference': refs[0], 'current_reference': refs[1]}
        sources.append(s)
        if n not in TEXTS:
            continue
        prose = TEXTS[n]
        args = ['barmaid', 'captain_first_name'] if n == 989 else ['captain_first_name', 'barmaid'] if n == 990 else ['captain_first_name'] if n == 999 else []
        assert prose.isascii() and prose == ' '.join(prose.split())
        assert prose.count('%s') == source.text.count(b'%s') == len(args)
        selections = [r for r in context['all84_original_city_and_name_provider_cases'] if r['id'] == n]
        if n in (989, 990):
            scene = 'Original5964C first-introduction branch,selected by town and actual barmaid object.989 names barmaid THEN captain;990 names captain THEN barmaid. Other towns use the already reviewed827.'
        elif n <= 998:
            scene = 'Original59358 one-in-three selected ordinary-chat branch of the special-gift/request path. The port selects one independent paragraph,not a sequence after the neighboring stored record.'
        elif n <= 1002:
            scene = 'Original5950C city-specific response after accepting the requested special gift.999 alone supplies the original mutable captain first name. The following item-state updates are unchanged.'
        else:
            scene = 'Original58F4C town-specific casual-chat branch,called by original591D0 on its random selection. The normal fallback is998;these are independent city/personality variants.'
        note = 'Preserve the source facts,personal voice and conversational tone;retain existing natural wording where appropriate. One logical paragraph,without inherited alignment or line breaks.'
        if n in (989, 990, 999):
            note += ' Keep native first-name identities/order;do not replace with a full name,surname,title or faction. The editable first-name field has a separately verified16-byte limit.'
        if n == 991:
            note += ' State the wish for a nice partner and happiness soon without inventing marriage or an established relationship.'
        elif n == 992:
            note += ' Retain fado without treating it as an invented proper song title;ASCII vocalization conveys the source melody.'
        elif n == 1001:
            note += ' You didn\'t have to is idiomatic grateful modesty,not a refusal or a claim about a new cost.'
        elif n == 1004:
            note += ' 休日 means her days off,not necessarily public holidays. Refreshes my spirit conveys the nature/heart-cleansing image in natural English.'
        elif n == 1007:
            note += ' Preserve the woman waiting for her lover at sea;do not add death,abandonment or a named singer/song.'
        elif n == 1014:
            note += ' Spoil you... just a little preserves the teasing offer without making it more sexually explicit or specifying an act.'
        elif n == 1015:
            note += ' Preserve the criticism of gender roles and support for women\'s wider social participation;do not reduce it to a generic compliment.'
        elif n == 1019:
            note += ' Preserve the concern about hunting for fur as this character\'s opinion,not a narrator\'s new policy or game mechanic.'
        if n == 996:
            scene += ' Original branch tests city58,which has no entry in the current21-barmaid catalog. Only a disclosed supplied city58/actor59 CPU case reaches it;normal reachability still needs closure.'
            note += ' Retain wording. No ordinary activation or fully mapped reachable context is claimed;context approval stays false pending source closure.'
        rows.append({'id': f'COMMON_MESSAGE_{n}', 'message_id': n, 'interaction_group': 'Tavern-barmaid-conversations',
                     'source_hex': s['source_hex'], 'japanese': s['Japanese'], 'source_reference': refs[0],
                     'canonical_source_hex': s['canonical_hex'], 'current_text_hex': s['current_hex'],
                     'current_English': s['current_English'], 'current_reference': refs[1],
                     'english': prose+'{PAD}', 'source_meaning': GLOSSES[n],
                     'speaker': 'Original selected town barmaid;see native city/actor/name catalog',
                     'context': scene, 'localization_note': note, 'source_voice_table': None,
                     'source_native_arguments': args, 'English_argument_source_indices': list(range(len(args))),
                     'native_catalog_selections': selections,
                     'decision': 'retain' if ' '.join(s['current_English'].replace('\uff29', 'I').replace('\uff26', 'F').split()) == prose else 'revise',
                     'review': {'source': True, 'context': n != 996, 'localization': True, 'naturalness': True, 'formatting': False},
                     'status': 'source-prose-reviewed-context996-and-production-formatting-integration-gameplay-pending'})
    save(ROOT/'source_and_neighbors.json', {'pins': pins, 'rows': sources, 'storage_adjacency_is_not_scene_order': True})
    save(MANUSCRIPT, {'format': 'dk4-common-entry-manuscript-v1', 'translation_policy': 'natural-dialogue-v2',
                      'encoder': 'dialogue-fixed-v1', 'target_locale': 'en-US',
                      'review_gates': ['source', 'context', 'localization', 'naturalness', 'formatting'],
                      'file_path': '/COMMON/MESFILE.DK4', 'source_pins': pins,
                      'native_context_proof': str(ROOT/'native_context.json'),
                      'status': 'source-prose-reviewed-NOT-playable', 'records': rows,
                      'producer_sha256': sha(Path(__file__).read_bytes())})
    print('31 source/prose drafts;', sum(r['decision'] == 'revise' for r in rows), 'revisions;996 context and all production gates remain open.', flush=True)


if __name__ == '__main__':
    main()
