"""Source-pinned editorial drafts; no layout approval or ROM mutation."""

import re
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import common_message_entries
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/shop_editorial_v744')
MANUSCRIPT = Path('translations/shop_town_editorial_manuscript_v1.json')
LEDGER = Path('translations/editorial_review_current_v1.json')

# Each gloss was written from Japanese before localizing the corresponding line.
# Existing English is retained explicitly where its wording already reads well.
REVIEW = {
    656: (None, 'The shop specializes in retail sales.',
          'The existing short explanation is idiomatic and preserves the retail distinction.'),
    657: ("You're a sailor, aren't you? For bulk trade, try the trade house.",
          'The merchant recognizes the player as a sailor and recommends the trading post for large-volume business.',
          'Restore the omitted sailor observation and retain the established trade-house term. The source question is friendly recognition, not a new profession assignment.'),
    658: ("Business? Oh, it's been all right. I'm hoping a good deal comes along.",
          'Business is going reasonably, and the shopkeeper wishes a profitable opportunity would turn up.',
          'Render the casual qualification and hope conversationally. A good deal conveys a business opportunity without implying an illegal scheme or adding a quest.'),
    659: (None, 'Confirm that the trade goods are to be distributed free of charge.',
          'The concise existing confirmation is natural American English; for is optional in give away free.'),
    660: ("You'd like the goods handed out for free, correct?",
          'The speaker politely checks that distributing the trade goods without charge is the requested action.',
          'Keep the courteous confirmation while replacing the clipped Hand the goods out free wording.'),
    661: (None, 'Confirm that the trade goods will be distributed as samples.',
          'The existing brief confirmation is clear, natural and source-faithful.'),
    662: ("You're giving these goods away for nothing, then?",
          'The speaker bluntly confirms that the goods are being given away without payment.',
          'The colloquial for nothing retains the rougher source register without inventing hostility.'),
    663: ("Give the goods to the townspeople for free, then?",
          'Confirm that the goods are to be distributed to local residents for free, in a measured older-style register.',
          'Keep local residents and the confirming then; avoid a caricatured elderly accent or an invented family relationship.'),
    664: ("You're giving the goods to the townspeople for free, right?",
          'The speaker casually confirms that local residents will receive the goods without charge.',
          'Restore the specific townspeople rather than the less precise everyone and retain the friendly confirmation.'),
    665: ("You'll be handing out the goods as free samples, then?",
          'The speaker formally confirms distribution of the goods without charge as samples.',
          'Use a complete conversational confirmation while retaining both the sample purpose and absence of payment.'),
    666: (None, 'Invite people to take samples freely and say they are free today.',
          'The existing invitation and No charge today are natural; preserve the source emphasis instead of rewriting merely for variation.'),
    667: (None, 'Invite everyone to help themselves without hesitation because there is no charge.',
          'The existing polite invitation and do not be shy preserve the welcome and reassurance naturally.'),
    668: ("Come take a look! Free samples, just for you!",
          'A lively hawker urges people to look and take a sample, presenting the gift as a generous current offer.',
          'Replace the stiff Come look and take one with an energetic sales call. Just for you is promotional address, not a claim of restricted availability.'),
    669: (None, 'Invite the listener to try the product freely because it is a sample.',
          'The existing short invitation is fluent and conveys the sample purpose in this free-distribution interaction.'),
    670: (None, 'Urge people to try and take the product because it is free at present.',
          'The existing brisk Try this and take one preserve the informal sales pitch.'),
    671: ("Here, give this a try! It's a sample, and it's free right now!",
          'Warmly urge people to try the product, explaining that it is a sample and currently free.',
          'Replace It costs nothing today with a conversational invitation. Right now preserves the source current offer without inventing a whole-day limit.'),
    672: (None, 'Call attention to samples and tell people that now is their opportunity to try them.',
          'The existing sales call is natural and complete within the free-sample context.'),
    673: (None, 'Politely invite listeners to take a sample and try it free of charge now.',
          'The current polite invitation and free-samples announcement are adequate natural localization.'),
    674: (None, 'A listener reacts with interest and agrees to try the product if it is free.',
          'The current Free? Then I will try it reaction preserves the casual enthusiasm.'),
    675: ("Take a look at this %s. It's top quality, without a doubt!",
          'Draw attention to the substituted product and emphatically claim it is of the highest quality.',
          'Replace surely the finest quality with a fluent sales claim, preserving the one source product substitution.'),
    676: ("Let me show you just how delicious this can be! Come take a look, ma'am!",
          'Introduce the excellent flavors made using the product and call to a nearby woman to come watch.',
          'Restore the complete cooking demonstration as its own selection. The current final word Discover belongs to the next independent fashion pitch and must not remain here.'),
    677: ("Come see the fashions and furnishings that'll soon be the talk of society! If you fancy yourself a lady or gentleman, step right up!",
          'Introduce fashions and interior furnishings expected to attract high-society attention; invite anyone considering themselves a lady or gentleman to come over.',
          'Restore the independent introduction and the omitted invitation to ladies and gentlemen. Do not start this native selection with the fashions as a continuation of message 676.'),
    678: (None, 'Praise the aroma and flavor, promise relief from daily fatigue, and urge people to try the product.',
          'The current sales patter is natural enough and preserves fatigue rather than substituting unrelated worries.'),
    679: ("New inventions and industries are springing up everywhere. My lecture is well worth your time. Wait too long, and you'll miss out on the profits!",
          'In an age full of new inventions and industries, the speaker boasts that the lecture is worth hearing and warns slow listeners that money-making opportunities will pass them by.',
          'Restore the full boast and warning in fluent sentences. Keep the speaker selling a lecture, not a newly invented product effect.'),
    680: ("This cures every illness! Humor me and give it a try.",
          'The promoter claims a cure for every illness and asks a skeptical listener to give it a try anyway.',
          'Humor me expresses the idiom asking someone to try despite doubts. This remains the promoter\'s boast; it is not confirmation of a game-item effect.'),
    681: (None, 'Take note of the substituted product as worth watching and suggest trying to sell it in the substituted area.',
          'The thoughtful fragments are natural spoken reactions. Both product and location substitutions remain in order.'),
    682: ("Business? That's the least of my worries. I just hope peace returns soon.",
          'Business is not the speaker\'s immediate concern; the speaker hopes peace returns quickly.',
          'Replace the brusque Forget that with a natural worried response, preserving the wish for peace.'),
    683: ("Business? People are collapsing from the epidemic! Are you kidding me?",
          'The speaker angrily challenges the business question because people are collapsing in an epidemic.',
          'The Japanese says collapsing, not confirmed deaths. Restore that distinction and preserve indignation without naming a specific disease.'),
    684: ("Business? Food comes first. People have to eat to survive.",
          'Food is a more urgent concern than business because people cannot survive without eating.',
          'Keep the plain, urgent explanation with a natural contraction-free final sentence.'),
    685: (None, 'Business is visibly excellent and the speaker cannot stop smiling or laughing.',
          'The current upbeat look around and cannot stop smiling response is already natural.'),
    686: ("Business? Don't ask. How's anyone supposed to do business like this?",
          'The speaker asks not to be questioned and complains that business is impossible under the current circumstances.',
          'Use a natural rhetorical complaint, without adding a particular disaster or financial outcome.'),
    687: ("Business? The ship on the regular route sank, and everyone's in a bind.",
          'A regularly scheduled service vessel has sunk, causing difficulty for everyone.',
          'Express the scheduled vessel without suggesting a modern cruise liner or inventing a passenger/cargo purpose.'),
}


def group(message_id):
    if message_id <= 658:
        return 'retail-and-normal-business'
    if message_id <= 665:
        return 'free-distribution-confirmation-variants'
    if message_id <= 674:
        return 'free-sample-announcement-variants'
    if message_id <= 681:
        return 'product-demonstration-and-reaction-variants'
    return 'business-response-event-variants'


def main():
    ROOT.mkdir(parents=True, exist_ok=True)
    assert not MANUSCRIPT.exists()
    ledger = read(LEDGER)
    images = {label: NdsImage.open(pin['path']) for label, pin in ledger['source_pins'].items()}
    for pin in ledger['source_pins'].values():
        assert sha(Path(pin['path']).read_bytes()) == pin['sha256']
    canonical = NdsImage.open('out/raphael_natural_v2_accepted_base.nds')
    tables = {label: common_message_entries(r.read_file('/COMMON/MESFILE.DK4'),
                                           r.read_file('/__arm9__.bin'), clean=label == 'japanese')
              for label, r in {**images, 'canonical': canonical}.items()}
    rows = []
    for i, (draft, meaning, note) in REVIEW.items():
        source, current, accepted = (tables[label][i] for label in ('japanese', 'current', 'canonical'))
        previous = ' '.join(current.text.decode('cp932').split())
        english = draft if draft is not None else previous
        assert re.findall(r'%[sdi]', english) == re.findall(r'%[sdi]', source.text.decode('cp932'))
        assert english == ' '.join(english.split()) and '{' not in english
        rows.append({
            'id': f'COMMON_MESSAGE_{i}', 'message_id': i, 'interaction_group': group(i),
            'source_hex': source.text.hex(), 'japanese': source.text.decode('cp932'),
            'source_reference': {'block': source.block, 'record': source.record_index,
                                 'native_offset': source.block_offset, 'start': source.start, 'end': source.end},
            'canonical_source_hex': accepted.text.hex(),
            'current_text_hex': current.text.hex(), 'current_English': previous,
            'current_reference': {'block': current.block, 'record': current.record_index,
                                  'native_offset': current.block_offset, 'start': current.start, 'end': current.end},
            'english': english + '{PAD}', 'source_meaning': meaning, 'localization_note': note,
            'speaker': 'Square shopkeeper' if i <= 658 or i >= 682 else 'Source-register confirmation or promotion speaker; exact actor assignment pending',
            'context': group(i) + '; alternate native selections, not assumed to form one sequential conversation.',
            'decision': 'revise' if draft is not None else 'retain-wording',
            'review': {'source': True, 'context': i == 658, 'localization': True,
                       'naturalness': True, 'formatting': False},
            'status': 'editorial-draft-native-context-and-formatting-pending',
        })
    document = {
        'format': 'dk4-common-entry-manuscript-v1', 'translation_policy': 'natural-dialogue-v2',
        'encoder': 'dialogue-fixed-v1', 'target_locale': 'en-US',
        'review_gates': ['source', 'context', 'localization', 'naturalness', 'formatting'],
        'status': 'draft-not-build-approved', 'file_path': '/COMMON/MESFILE.DK4',
        'source_clean_COMMON_sha256': ledger['source_pins']['japanese']['MESFILE_sha256'],
        'source_canonical_COMMON_sha256': sha(canonical.read_file('/COMMON/MESFILE.DK4')),
        'source_pins': ledger['source_pins'], 'records': rows,
        'layout_requirement': 'Use the actual COMMON consumer contract, not a story profile with different literal-I/F macro rules. Paragraphs may require native repacking; no truncation or authored alignment/breaks.',
    }
    save(MANUSCRIPT, document)
    packet = []
    for i in range(652, 691):
        a, b = tables['japanese'][i], tables['current'][i]
        packet.append({'message_id': i, 'Japanese': a.text.decode('cp932'),
                       'current_English': b.text.decode('cp932'), 'source_hex': a.text.hex(),
                       'current_hex': b.text.hex(), 'source_owner': [a.block, a.record_index],
                       'current_owner': [b.block, b.record_index]})
    save(ROOT / 'source_context_packet.json', {'source_pins': ledger['source_pins'], 'entries': packet,
         'table_adjacency_is_not_proof_of_dialogue_order': True})
    review_lines = ['# First shop/town editorial pass', '',
                    'Drafts only. Source/prose checks are recorded separately from native context and formatting.', '']
    for row in rows:
        review_lines.extend([f'## {row["message_id"]}: {row["decision"]}', '',
            'Japanese: ' + row['japanese'].replace('\n', ' / '), '',
            'Current: ' + row['current_English'], '',
            'Draft: ' + row['english'].removesuffix('{PAD}'), '',
            'Reason: ' + row['localization_note'], ''])
    (ROOT / 'review.md').write_text('\n'.join(review_lines), encoding='utf-8')
    ledger['first_shop_town_editorial_pass_v744'] = {
        'manuscript': str(MANUSCRIPT), 'manuscript_sha256': sha(MANUSCRIPT.read_bytes()),
        'source_context_packet': str(ROOT / 'source_context_packet.json'),
        'source_context_packet_sha256': sha((ROOT / 'source_context_packet.json').read_bytes()),
        'IDs': list(REVIEW), 'source_and_prose_pass': len(rows),
        'draft_revisions': sum(r['decision'] == 'revise' for r in rows),
        'retained_wording': sum(r['decision'] == 'retain-wording' for r in rows),
        'native_context_and_formatting_approval_pending': True,
    }
    ledger['records_with_source_and_prose_pass'] = len(rows)
    ledger['findings'].extend([
        {'id': 'COMMON-657-omitted-sailor-observation', 'native_message_id': 657,
         'status': 'draft-restores-source-detail-context-formatting-pending'},
        {'id': 'COMMON-676-677-cross-selection-prose', 'native_message_ids': [676, 677],
         'status': 'source-and-current-bytes-confirmed-draft-restores-independent-pitches',
         'detail': 'Current 676 ends with Discover while independent 677 starts with the fashions; 677 also omits the source invitation to ladies and gentlemen. All three native siblings 675/676/677 must remain separately selectable.'},
        {'id': 'COMMON-683-collapsing-not-confirmed-deaths', 'native_message_id': 683,
         'status': 'draft-corrects-overstatement-native-review-pending'},
        {'id': 'COMMON-688-Britain-England-confusion', 'native_message_id': 688,
         'status': 'queued-for-next-country-briefing-source-review',
         'detail': 'Current selection begins England unites England; clean source names Britain and its constituent England/Scotland/Wales. Preserve game narration rather than silently correcting historical setting.'},
    ])
    ledger['findings'][0]['status'] = 'source-and-prose-reviewed-draft-context-known-formatting-integration-pending'
    ledger['latest_checkpoint'] = 'V744 first 32 shop/town source-and-prose drafts; runtime approval pending'
    save(LEDGER, ledger)
    save(ROOT / 'proof.json', {
        'manuscript': str(MANUSCRIPT), 'sha256': sha(MANUSCRIPT.read_bytes()),
        'reviewed_native_IDs': list(REVIEW),
        'draft_revisions': sum(r['decision'] == 'revise' for r in rows),
        'retained_wording': sum(r['decision'] == 'retain-wording' for r in rows),
        'source_printf_placeholder_type_count_order_preserved': True,
        'all_authored_prose_single_paragraph_without_layout_spaces': True,
        'native_context_formatting_and_integration_pending': True,
        'no_ROM_registry_or_graphics_audit_changes': True,
        'previous_goal_turn_classification': 'progress: editorial goal, source pins and initial coverage ledger created',
        'producer_sha256': sha(Path(__file__).read_bytes()), 'full_goal_complete': False,
    })
    print('Prepared 32 source/prose decisions:', ledger['first_shop_town_editorial_pass_v744'], flush=True)


if __name__ == '__main__':
    main()
