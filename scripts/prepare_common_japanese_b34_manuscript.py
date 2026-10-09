"""Prepare clean-source production prospects, item appraisal, crew equipment and officer duties."""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import common_message_entries

TEXT = {
    3038: ('Southeast Asia has the perfect climate for growing pepper.', 'Judges Southeast Asia climate ideal for growing pepper.'),
    3039: ("Southeast Asia's climate is ideal for cloves. The Mediterranean might prove difficult...", 'Southeast Asia climate is very suitable for cloves; growing them in the Mediterranean may be difficult.'),
    3040: ("We'd make a fortune if we could grow cinnamon in the Mediterranean.", 'Predicts large profits if cinnamon production in the Mediterranean becomes possible.'),
    3041: ('If only we could market this aromatic product in Africa...', 'Wishes to commercialize the unspecified aromatic substance in Africa; does not identify the item beyond the source.'),
    3042: ('The New World should be well suited to growing coffee.', 'Expects the New World to be suitable for coffee production.'),
    3043: ('It looks as though we could grow tea in Africa too.', 'Tentatively suggests tea could also be produced around Africa.'),
    3044: ('This apparently needs tropical conditions to grow. Why not try taking it to Africa?', 'Apparently grows only in the tropics; proposes taking it to Africa.'),
    3045: ('Growing this in the Mediterranean and selling it seems promising. We might become very wealthy.', 'Tentatively recommends growing and selling the item in the Mediterranean and suggests possible great wealth.'),
    3046: ('African ore could be a new product.', 'Suggests African ore may become a newly available product.'),
    3047: ('In Africa and East Asia, glass is valuable.', 'Glass is a precious commodity in Africa and East Asia.'),
    3048: ("Silk has long been one of East Asia's main trade goods.", 'Silk has been a leading East Asian product since long ago.'),
    3049: ('The textile industries of the North Sea and Mediterranean still have plenty of room to grow.', 'North Sea and Mediterranean textile industries have considerable room for further development.'),
    3050: ('Perhaps we could find pearls in East Asia too.', 'Suggests pearls might also be obtained in East Asia.'),
    3051: ('I hear there are still many unusual herbal medicines in China.', 'Hearsay about many more unusual Chinese traditional medicines remaining to be found.'),
    3053: ('This should prove very useful if we have a rat infestation.', 'Expects the item to be very effective when rats appear.'),
    3055: ('No sailor can defy the weather. This is sure to come in handy.', 'Weather cannot be resisted even by sailors; expects the item to be very useful.'),
    3056: ('A marvel of Eastern medicine. They say it works especially well against infectious diseases.', 'Marvels at Eastern medicine and reports that the item is particularly effective against infectious diseases; preserves hearsay.'),
    3058: ('A deckhand or the boarding chief should carry this.', 'Recommends assigning the item to a deck crew member or boarding chief.'),
    3059: ('They say Lohengrin was a swan incarnate who had supernatural powers. This saber looks remarkably sharp too.', 'Reports the legend that Lohengrin was the incarnation of a swan and possessed supernatural powers; judges the saber apparently very sharp.'),
    3060: ('Give this to the boarding chief.', 'Recommends giving the item to the boarding chief.'),
    3061: ('A deckhand or the boarding chief should carry this.', 'Recommends giving the item to a deck crew member or boarding chief.'),
    3062: ("It isn't useful enough to justify its price, but it might make you look a little more impressive.", 'Judges utility below the asking price, with a possible modest improvement in appearance.'),
    3064: ('A deckhand or the boarding chief should carry this.', 'Recommends giving the item to a deck crew member or boarding chief.'),
    3066: ('A deckhand or the boarding chief should carry this.', 'Recommends giving the item to a deck crew member or boarding chief.'),
    3071: ("It's called Gentian. Any warrior who can master it must be formidable.", 'Weapon named Rindo, meaning Gentian; a warrior who can master it must be very strong.'),
    3072: ('This is just the thing for a skilled boarding chief.', 'Emphatically recommends the item for a competent boarding chief in particular.'),
    3073: ("I'd certainly give a skilled boarding chief this item.", 'Strongly recommends giving the item to a competent boarding chief.'),
    3075: ('A deckhand could use this to defend themselves.', 'Suggests giving the item to a deck crew member for personal protection.'),
    3076: ('A deckhand or the boarding chief should carry this.', 'Recommends giving the item to a deck crew member or boarding chief.'),
    3077: ('Give this fine piece to a formidable fighter you can trust.', 'Exceptional item should be entrusted to a dependable strong fighter.'),
    3079: ('Hmm! This is a superb blade. I sense some unseen power in it.', 'Praises the weapon craftsmanship and senses an invisible force.'),
    3080: ("So this is the legendary... I never thought I'd see it for myself.", 'Amazed recognition of a legendary item; never expected to see it personally.'),
    3081: ('Now this is a magic sword. Hmm... The longer I look at it, the more it draws me in.', 'Identifies a magical sword and feels increasingly captivated when looking at it.'),
    3082: ('A deckhand should keep this on hand.', 'Recommends keeping the item with a deck crew member.'),
    3083: ('Even someone who doubts their fighting skills could handle this.', 'Item can be used even by someone without confidence in their combat ability.'),
    3084: ('A handy piece of armor.', 'Describes armor as convenient and easy to use.'),
    3085: ("I'd like our deckhands and boarding chief to carry this.", 'Wants the item provided to deck crew and boarding chief.'),
    3088: ('Give this to the boarding chief.', 'Says the item should be entrusted to the boarding chief.'),
    3089: ('Give this to the boarding chief.', 'Says the item should be entrusted to the boarding chief.'),
    3090: ("I'd like our deckhands and boarding chief to carry this.", 'Wants the item provided to deck crew and boarding chief.'),
    3091: ("I'd like our deckhands and boarding chief to carry this.", 'Wants the item provided to deck crew and boarding chief.'),
    3092: ('Give this to the boarding chief.', 'Says the item should be entrusted to the boarding chief.'),
    3093: ('Give this to the boarding chief.', 'Says the item should be entrusted to the boarding chief.'),
    3094: ("I'd like our deckhands and boarding chief to carry this.", 'Wants the item provided to deck crew and boarding chief.'),
    3095: ("I'd like our deckhands and boarding chief to carry this.", 'Wants the item provided to deck crew and boarding chief.'),
    3096: ('Give a confident fighter equipment of this quality.', 'Says a fighter with confidence in their ability should be equipped to this standard.'),
    3097: ('A confident fighter would benefit from equipment like this.', 'Recommends equipment of this standard for someone confident in their combat ability.'),
    3098: ('Give a confident fighter equipment of this quality.', 'Says a fighter with confidence in their ability should be equipped to this standard.'),
    3099: ('Even the admiral would be well served by this armor.', 'Judges the item suitable for the admiral own armor as well.'),
    3100: ("You don't often come across an item this fine.", 'Says items of this quality are rarely encountered.'),
    3101: ("You don't often come across an item this fine.", 'Says items of this quality are rarely encountered.'),
    3102: ('Hmm... A truly splendid piece.', 'Thoughtfully praises the item as magnificent.'),
    3103: ('There is a power within it that words cannot describe.', 'Senses indescribable hidden power in the item.'),
    3104: ('Armor worthy of a true hero!', 'Declares the item worthy of being worn by a true hero.'),
    3105: ("It has a great conqueror's dignity and bearing... What a sight! Seeing this makes life as a naturalist worthwhile.", 'Describes an item with the dignity and presence of a hegemonic ruler; delighted to see it and regards the experience as fulfilling for a naturalist.'),
    3108: ('The mainmast sail handler should carry this.', 'Recommends entrusting the item to the sail handler at the mainmast specifically.'),
    3109: ('A lookout needs to know which way the ship is heading.', 'A lookout must know the direction of the ship travel.'),
    3111: ('Deck work is dull. Reading some poetry would make a nice change.', 'Deck work is tedious; reading a poetry collection would provide a refreshing diversion.'),
    3114: ('A survey chart is only as accurate as the tools used to make it.', 'Survey chart accuracy is affected by the quality of the instruments used.'),
    3115: ("With accurate timekeeping, we can calculate the ship's exact speed. That should aid surveying.", 'Accurate time allows accurate calculation of ship speed, which should assist surveying.'),
    3116: ('Learning the tricks gained through years of practice can greatly improve your steering.', 'Knowing practical techniques accumulated through repeated experience greatly helps steering.'),
    3117: ("A captain's ability is what earns the heavens' favor.", 'Heavenly protection is attributed to the captain competence or personal caliber.'),
    3118: ('A captain needs charisma to win over the officers.', 'Captain requires the charisma or power to attract the other navigators and officers.'),
    3119: ("A captain also has an important duty to keep the sailors' morale high.", 'Raising sailor morale is also an important duty of the captain.'),
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
            'speaker': 'Older naturalist advising on trade goods, items and crew roles',
            'context': (f'Independent native message {e.message_id}, clean COMMON B34 '
                        f'R{e.record_index}; production prospects, item appraisal, crew equipment and officer duties. '
                        'All native selections in each selected source owner are included.'),
            'localization_note': ('Fresh clean-source American English preserves region, commodity, climate '
                                  'and production advice, conditional profit, hearsay and uncertainty, '
                                  'Lohengrin and the Gentian weapon alias, item quality and price caveats, '
                                  'deckhand versus boarding-chief roles, mainmast specificity, survey accuracy, '
                                  'speed calculation, steering, captain ability, charisma and morale. '
                                  'Recommendations do not invent gameplay effects. Naturalist wording follows '
                                  'the established speaker term. One paragraph; safe full-width I/F. '
                                  'Exact-font previews await review.'),
            'review': {'source': True, 'context': True, 'localization': True,
                       'naturalness': True, 'formatting': False},
        })
    payload = {'format': 'dk4-common-entry-manuscript-v1',
               'translation_policy': 'natural-dialogue-v2', 'target_locale': 'en-US',
               'encoder': 'dialogue-fixed-v1',
               'review_gates': ['source', 'context', 'localization', 'naturalness', 'formatting'],
               'status': 'draft-awaiting-reblocking-and-formatting-review', 'records': rows}
    Path('translations/common_japanese_b34_manuscript_v1.json').write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(f'Prepared {len(rows)} clean-source native messages')


if __name__ == '__main__':
    main()
