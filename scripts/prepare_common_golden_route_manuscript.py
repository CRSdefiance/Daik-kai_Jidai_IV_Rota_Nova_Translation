"""Prepare the complete clean-source Golden Route discovery/reward dialogue."""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import common_message_entries

# Each gloss describes the clean source; the English preserves argument order.
TEXT = {
    3320: ('We made quite a profit on %s this time. Could this be a Golden Route?', 'This time %s earned considerable profit; tentative question whether this is a Golden Route.'),
    3321: ('We made quite a profit on %s this time. This could be a Golden Route.', 'Considerable profit on %s this time; masculine casual possibility of a Golden Route.'),
    3322: ("We made quite a profit on %s this time. I'm sure this will be a Golden Route!", 'Considerable profit on %s this time; enthusiastic confidence that it will be a Golden Route.'),
    3323: ('We made quite a profit on %s this time. Could this be a Golden Route?', 'Considerable profit on %s this time; feminine conversational tentative question.'),
    3324: ('We made quite a profit on %s this time! Could this be a Golden Route?', 'Considerable profit on %s this time; emphatic casual question about possible Golden Route.'),
    3325: ('We made a handsome profit on %s this time. Hmm... This may be a Golden Route...', 'Considerable profit on %s; older reflective voice, hesitation and possibility rather than certainty.'),
    3326: ("We made quite a profit on %s this time. I'm sure this will be a Golden Route!", 'Considerable profit this time and enthusiastic confidence that this will be a Golden Route.'),
    3327: ('We made quite a profit on %s this time. Could this perhaps be a Golden Route?', 'Polite older voice noting considerable profit on %s and suggesting a possible Golden Route.'),
    3328: ('A Golden Route?', 'Brief surprised question repeating the term Golden Route.'),
    3329: ('A Golden Route, you say?', 'More forceful surprised repetition of Golden Route.'),
    3330: ("What's a Golden Route?", 'Asks what the term Golden Route means, rather than merely repeating it.'),
    3331: ("What's a Golden Route?", 'Asks what Golden Route means.'),
    3332: ("I hear the guild is looking for information on profitable trade routes.", 'Reported information that the guild seeks information about profitable trade routes.'),
    3333: ('Apparently, the guild is looking for information on profitable trade routes.', 'Reported guild search for information about profitable trade routes, restrained tone.'),
    3334: ("I hear the guild is looking for information on profitable trade routes.", 'Conversational report of the guild seeking profitable trade-route information.'),
    3335: ("I've heard the guild wants information on lucrative trade routes.", 'Feminine conversational report of the guild seeking money-making trade-route information.'),
    3336: ("Word is, the guild is looking for information on profitable trade routes.", 'Casual report of guild demand for profitable trade-route information.'),
    3337: ('Apparently, the guild wants information on profitable trade routes.', 'Older speaker reports guild search for profitable trade-route information.'),
    3338: ("I hear the guild wants information on profitable trade routes!", 'Enthusiastic reported guild search for profitable trade-route information.'),
    3339: ("I'm told the guild is looking for information on profitable trade routes.", 'Polite reported guild search for profitable trade-route information.'),
    3340: ('They call routes with especially high potential profits Golden Routes. Apparently, they pay a substantial reward for that information.', 'Routes expected to generate particularly large profits are named Golden Routes; reportedly substantial rewards are paid to the informant.'),
    3341: ('They call routes with high potential profit margins Golden Routes. Apparently, they pay a substantial reward for that information.', 'Routes expected to have high profit rates are called Golden Routes; reportedly substantial informant rewards. Preserve rate versus absolute profit distinction.'),
    3342: ("They call routes that could make lots of money Golden Routes. I hear they give you a big reward for telling them about one.", 'Conversational explanation: routes likely to earn lots of money are Golden Routes, with substantial rewards to those reporting them.'),
    3343: ("They call promising trade routes Golden Routes. I hear they give a substantial reward to anyone who tells them about one.", 'Money-making routes called Golden Routes; reportedly substantial rewards for informants.'),
    3344: ("They call routes with especially high potential profits Golden Routes. Word is, they pay a hefty reward for that information.", 'Emphatic casual explanation of particularly profitable Golden Routes and reported substantial rewards to informants.'),
    3345: ('They call routes with especially high potential profits Golden Routes. Apparently, they pay a handsome sum to whoever tells them about one.', 'Older voice: particularly profitable routes called Golden Routes, and reportedly a considerable payment to the informant.'),
    3346: ("They're called Golden Routes, apparently. I've heard they'll pay a big reward if you tell them about a particularly profitable route.", 'Heard term Golden Routes; particularly profitable route information reportedly earns substantial reward.'),
    3347: ("I'm told they call particularly profitable trade routes Golden Routes. They say they'll pay a substantial reward if you tell them about one.", 'Polite explanation: particularly profitable routes termed Golden Routes; reported substantial payment for information.'),
    3348: ("That's amazing!", 'Impressed response to the reward explanation.'),
    3349: ("That's impressive!", 'Impressed response, restrained masculine tone.'),
    3350: ("That's amazing!", 'Feminine impressed response.'),
    3351: ("That's amazing!", 'Feminine impressed response.'),
    3352: ("Let's report it right away when we next reach a port with a guild.", 'Proposes immediate reporting upon next arrival at a port that has a guild.'),
    3353: ("Let's tell them right away when we next reach a port with a guild.", 'Casual proposal to inform guild immediately at next port with one.'),
    3354: ('We need to tell them as soon as we next reach a port with a guild.', 'Need to inform guild immediately at next port with one; apparent source teach/tell form preserved as intent.'),
    3355: ('We must tell them as soon as we next reach a port with a guild.', 'Conversational necessity to inform guild immediately at next port with one.'),
    3356: ("Let's tell them right away when we next reach a port with a guild!", 'Emphatic casual proposal to inform guild immediately at next port with one.'),
    3357: ('We must tell them as soon as we next reach a port with a guild.', 'Older voice: duty to inform guild immediately at next port with one.'),
    3358: ("Let's tell them as soon as we next reach a port with a guild!", 'Enthusiastic proposal to inform guild immediately at next port with one.'),
    3359: ("Let's tell them as soon as we next reach a port with a guild.", 'Polite proposal to inform guild immediately at next port with one.'),
    3360: ("Yes, let's do that.", 'Agrees to the proposed guild report.'),
    3361: ("Right, let's do that.", 'Masculine agreement to proposed report.'),
    3362: ("Yes, that's what I'll do.", 'Feminine first-person agreement to act as proposed.'),
    3363: ("Yes, let's do that.", 'Polite agreement to do as proposed.'),
    3364: ('We made quite a profit on %s this time, too. Could this also be a Golden Route?', 'Another considerable profit on %s; tentative suggestion that this too is a Golden Route.'),
    3365: ('We made quite a profit on %s this time, too. Could this be another Golden Route?', 'Masculine casual observation of another profitable transaction and tentative Golden Route identification.'),
    3366: ('We made quite a profit on %s this time, too. Could this also be a Golden Route?', 'Feminine conversational observation of additional profit and possible additional Golden Route.'),
    3367: ('We made quite a profit on %s this time, too. I wonder if this is another Golden Route.', 'Feminine reflective question about an additional Golden Route after another profitable transaction.'),
    3368: ('Yes. I think the guild will recognize it, too.', 'Agreement; thinks the guild also will recognize it as a Golden Route.'),
    3369: ('Yes, the guild will probably recognize it, too.', 'Masculine agreement and prediction of guild recognition, not an already granted classification.'),
    3370: ("Yes. I'm sure the guild will recognize it, too.", 'Confident agreement predicting guild recognition.'),
    3371: ("Yes. I'm sure the guild will recognize it, too.", 'Feminine agreement with confident expectation of guild recognition.'),
    3372: ('Yeah, I think the guild will recognize it, too.', 'Casual emphatic agreement with expectation of guild recognition.'),
    3373: ('Indeed. The guild will probably recognize it, too.', 'Older voice agreeing and predicting guild recognition.'),
    3374: ("Yes! I'm sure the guild will recognize it, too!", 'Enthusiastic confident agreement predicting guild recognition.'),
    3375: ('Yes, I feel sure the guild will recognize it, too.', 'Polite agreement; confident thought about future guild recognition.'),
    3376: ("Then let's report it right away when we next reach a port with a guild.", 'Then proposes immediate report at next port with a guild.'),
    3377: ("All right, let's tell them as soon as we next reach a port with a guild.", 'Decisive masculine proposal to inform guild immediately at next port with one.'),
    3378: ("Then let's report it as soon as we next reach a port with a guild.", 'Polite proposal to report immediately at next port with a guild.'),
    3379: ("Then let's tell them as soon as we next reach a port with a guild.", 'Polite proposal to inform guild immediately at next port with one.'),
    3380: ('You discovered a Golden Route! Is that true?', 'Guild reaction to claimed Golden Route discovery, surprised request for confirmation.'),
    3381: ('You can make a huge profit by selling goods bought in %s: %s.', 'Selling the named trade good purchased at the named town produces great profit. First argument is town, second is commodity; no positional reordering.'),
    3382: ('You can make a huge profit selling goods bought in %s: %s!', 'Casual masculine report of profitable sale; first town, then commodity.'),
    3383: ('You can make a huge profit selling goods bought in %s: %s.', 'Feminine report of profitable sale; first town, then commodity.'),
    3384: ('You can make a huge profit selling goods bought in %s: %s.', 'Feminine conversational report of profitable sale; first town, then commodity.'),
    3385: ("For two years, in the months when %s arrives in stock, I'll pay you %s gold coins as a reward.", 'Guild promises two years of reward payments, in the named commodity arrival months, for the specified gold amount. First commodity, then gold count; preserve arrival-month timing.'),
    3386: ('You discovered several Golden Routes! How astonishing!', 'Guild surprised at multiple Golden Route discoveries.'),
    3387: ("I've prepared a report on how to make a huge profit from goods bought in %s, including %s.", 'Speaker compiled profitable information in written documents, including the named commodity bought at named town. First town, second commodity.'),
    3388: ("I've prepared a report on profitable trades involving goods bought in %s, starting with %s.", 'Masculine speaker compiled profitable information in documents, starting with named commodity from named town; first town then commodity.'),
    3389: ("I've put together a report on lucrative trades in goods bought in %s, such as %s.", 'Feminine speaker compiled documents for the listener about large profits from goods such as named commodity from named town; town then commodity.'),
    3390: ("I've written up the details of profitable trades in goods bought in %s, such as %s.", 'Feminine speaker has written up information for great profits, such as named commodity purchased at named town; town then commodity.'),
    3391: ("So this is the report. I'll pay a generous reward! For two years, in each good's arrival months, I'll pay you gold coins equal to its trading profit.", 'Guild receives document, promises generous reward: for two years, in each respective commodity arrival month, pay gold amount equal to profitable amount. No monthly-every-month or single lump-sum invention.'),
    3392: ('You received %s gold coins from the guild as a reward for discovering a Golden Route.', 'System notification of gold income from guild as Golden Route discovery reward; one gold-count substitution.'),
}

# Natural editorial refinements retain the glosses and let the formatter wrap.
REFINED = {
    3322: "This time, %s earned a fine profit. Surely it'll be a Golden Route!",
    3325: 'This time, %s earned a handsome profit. Hmm... Perhaps this qualifies as a Golden Route...',
    3326: "This time, %s earned a fine profit. Surely it'll be a Golden Route!",
    3327: 'We made quite a profit on %s this time. Might this be a Golden Route?',
    3332: 'I hear the guild wants information on profitable trade routes.',
    3333: 'They say the guild seeks information on profitable trade routes.',
    3334: 'I hear the guild wants information on profitable trade routes.',
    3335: 'I hear the guild wants information on lucrative trade routes.',
    3336: 'Word is, the guild wants information on profitable trade routes.',
    3337: 'They say the guild seeks information on profitable trade routes.',
    3339: 'I hear the guild wants information on profitable trade routes.',
    3340: 'They call especially lucrative trade routes Golden Routes. I hear they pay a substantial reward to whoever reports one.',
    3342: 'They call routes that could make lots of money Golden Routes. I hear telling them about one earns you a big reward.',
    3343: 'They call lucrative trade routes Golden Routes. Anyone who reports one earns a substantial reward, so they say.',
    3345: 'They call especially promising routes Golden Routes. Apparently, whoever reports these lucrative routes earns a handsome reward.',
    3347: 'I hear they call particularly lucrative trade routes Golden Routes, and pay a substantial reward to whoever reports one.',
    3364: 'We made quite a profit on %s again. Could this also be a Golden Route?',
    3366: 'We made quite a profit on %s again. Could this also be a Golden Route?',
    3377: "All right, let's tell them right away at the next port with a guild.",
    3387: "I've prepared a report on hugely profitable trades in goods bought in %s, including %s.",
    3389: "I've prepared a report for you on hugely profitable trades involving goods bought in %s, such as %s.",
    3390: "I've written a report on hugely profitable trades involving goods bought in %s, such as %s.",
    3391: "So this is it! I'll reward you generously. For two years, I'll pay gold equal to each good's profit in its arrival months.",
    3392: 'You received a Golden Route discovery reward from the guild: %s gold coins.',
}
for message_id, english in REFINED.items():
    TEXT[message_id] = (english, TEXT[message_id][1])


def main():
    clean = NdsImage.open('work/clean.nds')
    entries = common_message_entries(clean.read_file('/COMMON/MESFILE.DK4'),
                                     clean.read_file('/__arm9__.bin'))
    assert set(TEXT) == set(range(3320, 3393))
    owners = {(entries[i].block, entries[i].record_index) for i in TEXT}
    selected = [e for e in entries if (e.block, e.record_index) in owners]
    assert {e.message_id for e in selected} == set(TEXT)
    rows = []
    for e in selected:
        english, gloss = TEXT[e.message_id]
        rows.append({
            'id': f'COMMON_MESSAGE_{e.message_id}', 'message_id': e.message_id,
            'block': e.block, 'record': e.record_index,
            'source_hex': e.text.hex().upper(), 'japanese': e.text.decode('cp932'),
            'previous_japanese': entries[e.message_id - 1].text.decode('cp932'),
            'next_japanese': entries[e.message_id + 1].text.decode('cp932'),
            'english': english.replace('I', 'Ｉ').replace('F', 'Ｆ') + '{PAD}',
            'source_meaning': gloss,
            'speaker': ('Guild representative' if e.message_id in (3380, 3385, 3386, 3391)
                        else 'System notification' if e.message_id == 3392
                        else 'Golden Route discovery/report participant; named speaker not inferred'),
            'context': (f'Native COMMON {e.message_id}, clean B{e.block} R{e.record_index}. '
                        'Complete discovery, explanation, repeat-discovery and guild reward conversation '
                        'with adjacent alternative voices. All selections in every targeted source owner '
                        'are included. The trading term in early one-argument lines remains neutral; '
                        'town/commodity/count meanings follow the explicit source grammar. Runtime '
                        'name widths and caller substitution samples remain separate checks.'),
            'localization_note': ('Clean-source American English preserves uncertainty versus confidence, '
                                  'profit margins versus profit amounts, substantial informant rewards, '
                                  'immediate reporting at the next port with a guild, multiple discoveries, '
                                  'written reports, arrival-month timing and two-year duration. No invented '
                                  'speaker identity, source argument reordering or copied legacy line breaks. '
                                  'Safe full-width I/F. Exact-font previews await review.'),
            'review': {'source': True, 'context': True, 'localization': True,
                       'naturalness': True, 'formatting': False},
        })
    payload = {'format': 'dk4-common-entry-manuscript-v1',
               'translation_policy': 'natural-dialogue-v2', 'target_locale': 'en-US',
               'encoder': 'dialogue-fixed-v1',
               'review_gates': ['source', 'context', 'localization', 'naturalness', 'formatting'],
               'status': 'draft-awaiting-formatting-review', 'records': rows}
    Path('translations/common_golden_route_manuscript_v2.json').write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(f'Prepared {len(rows)} complete-owner Golden Route messages')


if __name__ == '__main__':
    main()
