"""Repair later native printf-shape defects from clean Japanese and all neighbors."""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import common_message_entries

TEXT = {
    964: ("I'll make the arrangements. I'm looking forward to seeing how it turns out.", "Offers to arrange the scheme and looks forward to its outcome."),
    965: ("I'll make the arrangements. Let's wait for good news.", "Offers to arrange the scheme and await favorable news."),
    966: ("Leave the arrangements to me. I wonder how it'll turn out...", "Informal offer to arrange the scheme and uncertainty about the result."),
    967: ("Leave the rest to me. I hope it goes well.", "Informal offer to handle what remains and hope for success."),
    968: ("Leave the arrangements to me. I'm looking forward to seeing how it turns out...", "Rough voice offers to arrange the scheme and anticipates its result."),
    969: ("I'll see to the arrangements. I'm eager to see what happens...", "Older voice offers to arrange the scheme and anticipates the result."),
    970: ("I'll handle the rest. I wonder if it'll work out...", "Youthful offer to handle what remains, wondering whether it will succeed."),
    971: ("I'll make the arrangements. I'm looking forward to the results.", "Formal older offer to arrange the scheme and anticipation of the results."),
    972: ("The ship on the regular service was due in port this month. Apparently, it sank in a storm...", "Regular-service vessel was expected in port this month but reportedly sank in a storm; retains uncertainty."),
    974: ("Which town's broker will you bribe?", "Informal question selecting the town whose broker will be bribed."),
    975: ("Which town's broker are we bribing?", "Rough question about which town's broker to bribe."),
    984: ("Admiral, it's packed, and there's no seat where we can talk privately. Let's try another day.", "Many customers leave no suitable seat for confidential conversation; proposes returning another day."),
    987: ("There's no seat for a private talk with all these customers. Admiral, shall we come back later?", "Older voice cites crowds and no suitable private seat, asking the admiral to return later."),
    988: ("Wow, it's so crowded! We can't talk privately here. Let's try tomorrow.", "Youthful voice says crowds prevent a secret conversation and specifically proposes tomorrow."),
    998: ("Take your time and relax.", "Friendly invitation to stay leisurely."),
    999: ("Ah! That's why I love you, %s!", "Excited affectionate reaction addressing the substituted name, without inventing kinship or rank."),
    1016: ("Foreigners used to make me uneasy, but you're special.", "The speaker previously felt uncomfortable with foreigners but treats this listener as an exception."),
    1020: ("We have no information on the towns where that faction has contracts.", "No information is available about towns contracted with the selected faction."),
    1021: ("I really don't think this will work... Are you sure?", "Strong personal doubt that the plan will succeed, followed by confirmation."),
    1022: ("The chances of success seem very low... Do you want to proceed?", "Success probability appears very low; asks whether to proceed."),
    1023: ("I don't think there's much chance of success... Want to try anyway?", "Informal opinion that success is unlikely, then asks whether to try nonetheless."),
    1024: ("...Looks like the odds of success are pretty low. Still want to try?", "Rough voice says success appears quite unlikely and asks whether to proceed anyway."),
    1025: ("I can't see this working at all... Are you sure?", "Older voice strongly doubts success and seeks confirmation."),
    1026: ("I don't think we can pull this off... Want to try anyway?", "Youthful voice thinks the plan is probably infeasible and asks whether to try anyway."),
    1027: ("There's almost no hope of success... Shall we try anyway?", "Formal older voice says there is almost no prospect of success and asks whether to try nonetheless."),
    1034: ("I don't know whose fleet it is, but it's anchored at %s.", "Fleet affiliation is unknown, but its anchorage is the substituted location."),
    1101: ("%s: Which faction?", "Informal question choosing the other faction for the substituted diplomatic operation; uses a neutral action heading."),
    1102: ("%s: Which faction shall we choose?", "Formal older question about the other faction for the substituted operation; heading avoids inventing an inflected verb."),
    1108: ("We'll sign a pact with %s to oppose %s, correct?", "Confirms a pact with the first party to jointly oppose the second."),
    1109: ("We're making a pact with %s against %s, right?", "Informal confirmation of cooperating with the first party against the second."),
    1110: ("We shall make a pact with %s against %s. Is that right?", "Older confirmation of a pact with the first party to oppose the second."),
    1111: ("We're promising to team up with %s against %s, right?", "Youthful confirmation of promising cooperation with the first party against the second."),
    1112: ("We are to make a pact with %s against %s, correct?", "Formal older confirmation of the first party as partner and the second as opposing force."),
    1114: ("You're sending %s the %s document. Is that right?", "Confirms sending a document of the second substituted type to the first substituted recipient."),
    1115: ("%s is to receive the %s document. Is that right?", "Older confirmation of recipient first and document type second."),
    1182: ("In %s, the price of %s has plummeted, they say.", "Hearsay that the second substituted commodity's price crashed in the first substituted town."),
    1183: ("They say %s suffered a huge loss.", "Rumor that the named party suffered a large loss; not a confirmed fact."),
    1194: ("There's not enough money.", "Insufficient money; no runtime argument belongs to this message."),
    1195: ("%s, I hear %s fought %s's fleet and won a brilliant victory!", "Addresses the first person and reports that the second party fought the third party's fleet and won impressively."),
    1213: ("You want to help?", "Question reacting to an offer of help."),
    1214: ("Help out?", "Brief questioning reaction to helping."),
    1215: ("Come on, keep working!", "Repeated urging not to stop working."),
    1354: ("I gave the villagers %s gold coins to thank them for their help.", "Older report of giving the substituted gold amount in gratitude for help."),
    1355: ("I gave the villagers %s gold coins as a thank-you.", "Youthful report of giving the substituted gold amount to express gratitude."),
    1936: ("You must be %s! We shall settle this with a duel!", "Older recognition of the opponent and challenge to single combat."),
    1937: ("You're %s! Fight me in a duel!", "Youthful recognition and enthusiastic demand to duel the speaker."),
    1955: ("%s, escape! Everyone, cover them!", "Older voice urges the named person to escape and orders everyone to provide covering support."),
    1956: ("%s, run! We'll all protect you!", "Youthful voice urges the named person to escape and promises protection from everyone."),
    2189: ("%s defeated!", "Brief report of defeating the named target."),
    2190: ("%s defeated!", "The same source report of defeating the named target; no added identity or sinking claim."),
    2559: ("The %s / %s fleet was tougher than expected. We have retreated...", "The paired-identifier fleet was stronger than expected, so our side withdrew; argument order retained."),
    2562: ("The %s / %s fleet was tougher than we thought. Our fleet has retreated...", "Rough voice reports the paired-identifier opponent stronger than expected and our fleet retreating."),
    2563: ("The %s / %s fleet was stronger than expected. Our fleet has withdrawn...", "Older voice reports unexpectedly strong paired-identifier opponents and our fleet withdrawing."),
    3381: ("For a huge profit, sell what you bought in %s: %s.", "Selling the second substituted commodity bought in the first substituted place offers a very large profit; source argument order retained."),
}


def main():
    clean = NdsImage.open('work/clean.nds')
    entries = common_message_entries(clean.read_file('/COMMON/MESFILE.DK4'),
                                     clean.read_file('/__arm9__.bin'))
    owners = {(entries[i].block, entries[i].record_index) for i in TEXT}
    selected = [e for e in entries if (e.block, e.record_index) in owners]
    assert {e.message_id for e in selected} == set(TEXT)
    rows = []
    for e in selected:
        english, meaning = TEXT[e.message_id]
        rows.append({
            'id': f'COMMON_MESSAGE_{e.message_id}', 'message_id': e.message_id,
            'block': e.block, 'record': e.record_index,
            'source_hex': e.text.hex().upper(), 'japanese': e.text.decode('cp932'),
            'previous_japanese': entries[e.message_id - 1].text.decode('cp932'),
            'next_japanese': entries[e.message_id + 1].text.decode('cp932'),
            'english': english.replace('I', 'Ｉ').replace('F', 'Ｆ') + '{PAD}',
            'source_meaning': meaning,
            'speaker': 'Crew confirmation voice, merchant, narrator or strategist',
            'context': (f'Independent native message {e.message_id}, COMMON '
                        f'B{e.block} R{e.record_index}. Repairs older omitted/moved '
                        'arguments and unrelated older text, with every packed neighbor.'),
            'localization_note': ('Fresh clean-source English restores scheme arrangements, '
                                  'anticipation versus hope and uncertainty, this-month ship '
                                  'arrival and reported sinking, broker town selection, private '
                                  'seating and tomorrow versus another day, affectionate name '
                                  'address, foreigner discomfort, contract-town information, '
                                  'low success chances and confirmations, unknown fleet identity, '
                                  'diplomatic partner/enemy and recipient/document type, rumors, '
                                  'gold amounts, help reactions, duel/escape/defeat/retreat and '
                                  'buying-location versus selling-good advice. Every printf '
                                  'argument stays in source order. Operation substitutions '
                                  'use a neutral heading; paired fleet labels use a slash, '
                                  'pending actual-value checks rather than an invented hierarchy. '
                                  'No gender, kinship or rank is invented. Reserved I/F use '
                                  'narrow full-width glyphs. Exact-font previews await review.'),
            'review': {'source': True, 'context': True, 'localization': True,
                       'naturalness': True, 'formatting': False},
        })
    payload = {
        'format': 'dk4-common-entry-manuscript-v1',
        'translation_policy': 'natural-dialogue-v2', 'target_locale': 'en-US',
        'encoder': 'dialogue-fixed-v1',
        'review_gates': ['source', 'context', 'localization', 'naturalness', 'formatting'],
        'status': 'draft-awaiting-native-repack-and-formatting-review', 'records': rows,
    }
    Path('translations/common_printf_late_manuscript_v1.json').write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


if __name__ == '__main__':
    main()
