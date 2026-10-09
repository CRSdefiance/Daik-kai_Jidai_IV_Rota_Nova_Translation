"""Prepare clean-source cease-fire, submission, trade news, forged documents and rumor reactions."""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import common_message_entries

TEXT = {
    2745: ('Very well... We too have no desire for pointless conflict.', 'Formal agreement to a cease-fire; both parties have no desire for fruitless conflict.'),
    2746: ("All right. We don't want a pointless fight either.", 'Informal acceptance because the speaker also does not want a pointless conflict.'),
    2747: ("All right... We don't want to fight needlessly either.", 'Feminine agreement; the speaker also does not wish for a useless conflict.'),
    2748: ('All right. Pointless fighting does nobody any good.', 'Rough acceptance because pointless fighting brings no benefit.'),
    2749: ('How dare they! Tell them to prepare for death!', 'Angry rejection; the wash-your-neck idiom threatens death and tells the other party to prepare.'),
    2750: ('What are they talking about...? Tell them to brace themselves!', 'Dismisses the proposal and orders a warning that the other party must prepare for the consequences.'),
    2751: ('What nonsense... Tell them to get ready to die!', 'Feminine scornful rejection followed by the death-threatening wash-your-neck idiom.'),
    2752: ("That's taking the joke too far. Tell them to get ready to die!", 'Rough angry rejection and death-threatening warning to prepare.'),
    2753: ("What?! Damn %s... They've got nerve! I'll teach them a lesson!", 'Shocked anger at the named party, acknowledges their audacity and threatens retaliation.'),
    2755: ("If that's your plan, I have plans of my own! Just you wait!", 'Feminine threat to respond with a plan of her own if the other party takes that stance.'),
    2756: ('What?! Looks like they want to get hurt... %s had better be ready!', 'Rough surprise and threat that the named party seems to want painful consequences and should prepare.'),
    2757: ("They're telling us to submit to %s?", 'Questions a demand to become subordinate to the named party.'),
    2758: ('They want us to submit to %s?', 'Formal disbelief at a demand that our faction become subordinate to the named party.'),
    2759: ('They say we should submit to %s?', 'Informal question about a demand to submit to the named party.'),
    2760: ("They're telling us to submit to %s?", 'Feminine question about being told to become subordinate to the named party.'),
    2761: ('Grr... We have no choice.', 'Angry reluctant acceptance that there is no alternative.'),
    2762: ('We have no choice...', 'Formal resigned recognition that there is no alternative.'),
    2763: ('Oh, all right... I guess we have no choice...', 'Youthful reluctant acceptance with uncertainty and resignation.'),
    2764: ("So... there's no other way.", 'Feminine resigned realization that there is no alternative.'),
    2765: ('We have no choice...', 'Resigned recognition that there is no alternative.'),
    2766: ("What nonsense! We needn't entertain such a ridiculous proposal!", 'Formal contempt and refusal to engage with the absurd proposal.'),
    2767: ("So that's what this is about... I won't entertain such an absurd proposal!", 'Surprised realization of the subject followed by an emphatic refusal to engage.'),
    2768: ("So that's what this is about... I won't entertain such a ridiculous proposal!", 'Youthful realization followed by refusal to engage with the absurd proposal.'),
    2769: ("So that's what this is about... I have no time for such nonsense!", 'Feminine realization followed by refusal to spend time on the absurd proposal.'),
    2770: ('A new product is being made in %s?', 'Questions news that the named town has begun producing a new product.'),
    2773: ('Huh? A new product in %s?', 'Youthful surprise at a new product in the named town.'),
    2774: ('At %s, an enemy merchant fleet has appeared?', 'Questions a report of an enemy merchant fleet appearing at the named location.'),
    2775: ('At %s, an enemy merchant fleet has shown up?', 'Informal question about an enemy merchant fleet appearing at the named location.'),
    2776: ('Huh? An enemy merchant fleet at %s?', 'Youthful surprise at an enemy merchant fleet at the named location.'),
    2777: ("Good. Let's send a fleet right away.", 'Approving decision to dispatch a fleet immediately.'),
    2778: ('Send a fleet at once!', 'Emphatic order to dispatch a fleet immediately.'),
    2781: ('Suspicious... It may be false information. Ignore it.', 'Suspects the information may be false and orders it ignored.'),
    2782: ('Can we really trust that report...? Never mind. Just leave it alone.', 'Youthful doubt about the reliability of the report followed by instructions to ignore it.'),
    2783: ('That sounds suspicious... It must be false information. Ignore it.', 'Feminine suspicion with a stronger judgment that the information is false, then an order to ignore it.'),
    2784: ("They're telling us to submit to %s?!", 'Angry incredulity at being ordered to become subordinate to the named party.'),
    2785: ('They say we should submit to %s?!', 'Youthful incredulity at a demand to become subordinate to the named party.'),
    2786: ('They want us to submit to %s?!', 'Feminine incredulity at a demand to become subordinate to the named party.'),
    2787: ("I was being polite, and now they're getting too full of themselves!", 'Angry complaint that the other party has become arrogant in response to the speaker taking a deferential stance.'),
    2789: ('They must be joking!', 'Feminine emphatic rejection of an outrageous demand.'),
    2790: ("They're mocking us! I won't stand for this!", 'Rough angry accusation that the other party is fooling around and rejection of the outrageous demand.'),
    2791: ('This is a forgery... Just ignore it.', 'Identifies the document as forged and says to ignore it.'),
    2792: ('This is a forgery... Never mind it. Ignore it.', 'Identifies the document as forged and dismisses it with an order to ignore.'),
    2793: ("I think... this is a forgery. Let's ignore it.", 'Tentative youthful judgment that the document is forged and proposal to ignore it.'),
    2794: ("Heh... This is a forgery. Let's just ignore it.", 'Feminine amused recognition that the document is forged and proposal to ignore it.'),
    2795: ('This is a forgery... Ignore it.', 'Identifies the document as forged and orders it ignored.'),
    2796: ('I hear %s is involved in smuggling.', 'Rough hearsay accusation that the named party engages in illicit trade; not established fact.'),
    2797: ('They say %s is utterly ruthless.', 'Hearsay characterization of the named party as cruel and without compassion; not established fact.'),
    2798: ("Hmm... Perhaps %s isn't a suitable trading partner for our town?", 'Older uncertain question whether the named party is an appropriate trading partner for our town.'),
    2799: ("%s, smuggling? Obviously, that rumor is false.", 'Youthful rejection of a smuggling accusation as clearly false.'),
    2800: ("%s, heartless? Well, it's only hearsay. We don't know the truth.", 'Qualified response to a cruelty rumor; its truth is unknown.'),
    2801: ("This town has too many trading partners to guarantee you a share. But pay me %s gold, and I'll cut %s's share for you.", 'Cannot secure a share because the town has too many contracted partners; offers to reduce the second named party share for the first quoted gold payment.'),
    2802: ("You want my help? Well... I'll need %s gold as a fee.", 'Rough response to a request for cooperation, requiring the quoted gold amount as an arrangement fee.'),
    2804: ('All right. Leave it to me.', 'Rough agreement to take care of the task.'),
    2805: ("You want my help? Sorry, but I can't do that.", 'Rough apologetic refusal to cooperate with the requested task.'),
    2806: ('%s tried to spread malicious rumors in %s, but we managed to stop them.', 'Reports an attempt by the first named party to spread bad rumors in the second location, successfully prevented with some difficulty.'),
    2807: ('%s tried to spread malicious rumors in %s, but we stopped them before they could.', 'Formal report of preventing the first named party rumor-spreading attempt in the second location before it could happen.'),
    2808: ("It looks like %s tried to spread malicious rumors in %s. Don't worry. We've got it covered.", 'Youthful tentative report of attempted rumor spreading by the first party in the second location; assures that countermeasures are fully in place.'),
    2809: ("%s spread malicious rumors in %s. We certainly won't be fooled.", 'Feminine report that the first named party spread bad rumors in the second location and refusal to be fooled.'),
    2810: ("%s spread nasty rumors in %s. As if we'd fall for that trick!", 'Rough report of malicious rumors spread by the first party in the second location and emphatic refusal to be fooled.'),
    2811: ("It seems %s is spreading nasty rumors in %s. We won't be fooled!", 'Older qualified report of ongoing malicious rumors by the first party in the second location and refusal to be fooled.'),
    2812: ("It seems %s is trying to spread bad rumors in %s. Don't worry, Admiral! The townspeople are on your side!", 'Childlike tentative report of an attempted rumor campaign by the first party in the second location; assures the admiral that the town residents support them.'),
    2813: ('%s was trying to spread malicious rumors in %s, so we took precautions.', 'Formal older report of a rumor-spreading attempt by the first party in the second location and advance arrangements to counter it.'),
    2814: ('You have to choose at least one coin before we can continue the game.', 'Rough instruction that the game cannot proceed unless the player selects at least one coin.'),
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
            'speaker': 'Crew report, faction leader or retainer voice variant',
            'context': (f'Independent native message {e.message_id}, clean COMMON B29 '
                        f'R{e.record_index}; cease-fire, submission, trade news, forged documents and rumor reactions. '
                        'All native selections in each selected source owner are included.'),
            'localization_note': ('Fresh clean-source American English preserves cease-fire acceptance and refusal, '
                                  'death threats versus general retaliation, subordinate status, reluctance, '
                                  'fleet dispatch, uncertain versus confident misinformation, forged-document '
                                  'certainty, hearsay and uncertain rumor truth, market-share bargaining and '
                                  'the fee, attempted versus ongoing or completed rumor campaigns, prevention '
                                  'and advance countermeasures. The neck-washing threat is localized by intent. '
                                  'Actor, destination, gold and target argument order remains intact. No invented '
                                  'relationships. One paragraph; safe full-width I/F. Exact-font previews await review.'),
            'review': {'source': True, 'context': True, 'localization': True,
                       'naturalness': True, 'formatting': False},
        })
    payload = {'format': 'dk4-common-entry-manuscript-v1',
               'translation_policy': 'natural-dialogue-v2', 'target_locale': 'en-US',
               'encoder': 'dialogue-fixed-v1',
               'review_gates': ['source', 'context', 'localization', 'naturalness', 'formatting'],
               'status': 'draft-awaiting-reblocking-and-formatting-review', 'records': rows}
    Path('translations/common_japanese_b29_manuscript_v1.json').write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(f'Prepared {len(rows)} clean-source native messages')


if __name__ == '__main__':
    main()
