"""Exact clean-source review of trade advice, relief and promoter conversations."""

from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import common_message_entries
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/town_events_v750')
MANUSCRIPT = Path('translations/town_events_editorial_manuscript_v1.json')
RETAIN = {731, 734, 735, 743, 745, 746}
TEXT = {
    730: 'Something in the %s market is sure to catch on soon.',
    732: "This trend looks like it'll last a while yet.",
    733: 'I wonder if the craze for %s is about to die down.',
    736: 'With this, no one will have to starve to death!',
    737: "We shouldn't have to worry about running out of stock anymore!",
    738: 'Thanks a lot! Time to get straight to work!',
    739: 'Hey, sailor! Could you do me a favor and take me to the square in another town? Any town will do...',
    740: "Really? I owe you one! Let's bring a fresh wave of fashion to towns all over the world!",
    741: "I see. I'm sorry to impose on you.",
    742: 'Hey! Could you spare that %s? With it, I think we could make %s a local specialty. What do you say?',
    744: "Oh, I see. You're a real miser.",
}
MEANING = {
    730: 'Some individual good within the supplied product category is certain to become popular in the future; this does not predict every good in that category.',
    731: 'The speaker thinks the supplied specific product will sell well.',
    732: 'The current trend appears likely to continue for quite some time yet.',
    733: 'The speaker wonders if the vogue for the supplied specific product is approaching its end.',
    734: 'The speaker must make a good profit before the trend dies out and exclaims how busy they are.',
    735: 'The recipient thanks the player: because of the player, everyone will recover from illness.',
    736: 'Because of this aid, everyone will avoid starving to death.',
    737: 'The speaker expects no further trouble from running out of stock.',
    738: 'The speaker thanks the player, then proposes getting straight to work. Source5E4B8 selects this on arrival in a different town with the traveling-promoter flag set.',
    739: 'The promoter addresses the passing sailor and asks for transport to the square of any other town; the destination is unrestricted except that it is another town.',
    740: 'The promoter is delighted at acceptance, says they owe the player, and rallies to bring a breath of new fashion to towns around the world.',
    741: 'The promoter accepts the refusal and apologizes for making an unreasonable request.',
    742: 'The local asks the player to hand over the first supplied item, believing it could make the second supplied product a local specialty, and asks for a decision.',
    743: 'The local joyfully confirms acceptance and praises the player as a good person and the best.',
    744: 'The local accepts the refusal and bluntly calls the player stingy.',
    745: 'The shopkeeper asks if the player still needs anything else.',
    746: 'The shopkeeper asks, with a slight pause, whether the player is merely browsing.',
}
NOTES = {
    730: 'Preserve one unspecified future hit within the supplied category. The original category getter currently supplies compact UI labels such as Cond., Delic. and Med. Full-name expansion/readability remains an explicit open issue before accepting this prose.',
    732: 'Restore the continuing-trend observation rather than a generic information placeholder; a while yet retains the ongoing duration.',
    733: 'Keep both uncertainty and the approaching end of a trend. Craze for takes either plural or mass product names naturally; preserve the source %s.',
    736: 'Restore explicit prevention of death from starvation, not merely a vague improvement in food supply.',
    737: 'Restore expected freedom from stock shortages; should preserves the source expectation rather than an unconditional mechanical guarantee.',
    738: 'Keep grateful, brisk speech. Time to get straight to work avoids inventing additional workers. This is an arrival acknowledgment, not a random shop reply.',
    739: 'Preserve direct address, the favor, the square and any other town. Do not invent a specified destination. This is a Yes/No question and requires its own actual consumer formatting check.',
    740: 'A fresh wave of fashion localizes the breath-of-new-trends metaphor while keeping the enthusiastic worldwide ambition; do not invent a proven economic effect.',
    741: 'Use a complete natural apology to the listener; do not leave the literal fragment Sorry to ask so much.',
    742: 'Keep both item and output-product substitutions in their original order. Could spare naturally asks for the handover; I think preserves the speculative claim. This is a dynamic Yes/No question, not the ordinary direct portrait consumer.',
    744: 'Preserve the disappointed stinginess insult in natural spoken English without inventing a threat or penalty.',
}


def main():
    assert not MANUSCRIPT.exists()
    ROOT.mkdir(parents=True, exist_ok=True)
    pointer = read('out/editorial_review_latest.json')
    current_path = Path(pointer['path'])
    assert sha(current_path.read_bytes()) == pointer['sha256']
    clean, current, canonical = (NdsImage.open(p) for p in ('work/clean.nds', current_path, 'out/raphael_natural_v2_accepted_base.nds'))
    path = '/COMMON/MESFILE.DK4'
    source = common_message_entries(clean.read_file(path), clean.read_file('/__arm9__.bin'))
    before = common_message_entries(current.read_file(path), current.read_file('/__arm9__.bin'), clean=False)
    accepted = common_message_entries(canonical.read_file(path), canonical.read_file('/__arm9__.bin'), clean=False)
    rows = []
    for i in range(730, 747):
        old = ' '.join(before[i].text.decode('cp932').split())
        english = old.replace('ï¼©', 'I') if i in RETAIN else TEXT[i]
        context = ('Independent trend advice from original5FB54, selected by source trend state and random branch; '
                   '730 receives a category name,731/733 a product name;732/734 have no substitutions.') if i <= 734 else (
                   'Original5EBC4 relief routine selects735 for medicine,736 for food,737 for other requested shortage categories after a sufficient handover.') if i <= 737 else (
                   'Traveling promoter:738 arrival acknowledgment at5E4B8;739 Yes/No request at5E620; '
                   '740 acceptance at5E634 sets the travel flag;741 refusal at5E658.') if i <= 741 else (
                   'Local-specialty item handover question742 with item and product names, followed by acceptance743 or refusal744; '
                   'source caller/conditions require native verification.') if i <= 744 else (
                   'Shop continuation/browsing replies share a native NUL owner; retain both independent selections, '
                   'and map their native caller before completion.')
        rows.append({'id': f'COMMON_MESSAGE_{i}', 'message_id': i, 'source_hex': source[i].text.hex(),
            'japanese': source[i].text.decode('cp932'), 'canonical_source_hex': accepted[i].text.hex(),
            'current_text_hex': before[i].text.hex(), 'current_English': old, 'english': english + '{PAD}',
            'speaker': 'Original contextual Square shopkeeper, traveling promoter or local-specialty requester; exact actor getter/caller evidence pending',
            'context': context, 'source_meaning': MEANING[i],
            'localization_note': NOTES.get(i, 'Retain the already natural wording and its complete source meaning; normalize legacy full-width Latin I through the consumer-specific safe literal path where present.'),
            'decision': 'retain-wording' if i in RETAIN else 'revise',
            'source_reference': {'block': source[i].block, 'record': source[i].record_index, 'offset': source[i].block_offset},
            'current_reference': {'block': before[i].block, 'record': before[i].record_index, 'offset': before[i].block_offset},
            'review': {'source': True, 'context': False, 'localization': i != 730, 'naturalness': i != 730, 'formatting': False},
            'status': 'source-prose-draft-native-context-formatting-and-integration-pending'})
    save(MANUSCRIPT, {'format': 'dk4-common-entry-manuscript-v1', 'translation_policy': 'natural-dialogue-v2',
        'encoder': 'dialogue-fixed-v1', 'target_locale': 'en-US',
        'review_gates': ['source', 'context', 'localization', 'naturalness', 'formatting'],
        'status': 'unintegrated-editorial-draft-not-a-release', 'file_path': path,
        'source_clean_COMMON_sha256': sha(clean.read_file(path)), 'source_canonical_COMMON_sha256': sha(canonical.read_file(path)),
        'source_ROM_sha256': sha(clean.source.read_bytes()), 'current_ROM_sha256': sha(current_path.read_bytes()), 'records': rows})
    save(ROOT / 'source_context_packet.json', {'clean_ROM_sha256': sha(clean.source.read_bytes()),
        'current_ROM': str(current_path), 'current_ROM_sha256': sha(current_path.read_bytes()),
        'source_and_current_neighbors': [{'message_id': i, 'Japanese_hex': source[i].text.hex(), 'current_hex': before[i].text.hex()}
                                        for i in range(729, 748)],
        'draft_restores_all8_remaining_exact_placeholder_meanings_but_does_not_remove_them_from_ROM': True,
        'release_or_completion_claim': False})
    text = ['# Town events: source/prose draft', '',
        ('17 entries:11 proposed revisions and6 proposed retained wordings. Native context, formatting and integration are pending. '
         '730 additionally requires readable category expansion. No completed-coverage count increases yet.'), '']
    for row in rows:
        text += [f'## {row["message_id"]}: {row["decision"]}', '', row['japanese'].replace('\n', ' / '), '',
            '**V749:** ' + row['current_English'], '', '**Draft:** ' + row['english'].removesuffix('{PAD}'), '',
            '**Meaning:** ' + row['source_meaning'], '', '**Reason:** ' + row['localization_note'], '', '**Context:** ' + row['context'], '']
    (ROOT / 'review.md').write_text('\n'.join(text), encoding='utf-8')
    print('17 source/prose drafts saved; no ROM or completed-coverage change.', flush=True)


if __name__ == '__main__':
    main()
