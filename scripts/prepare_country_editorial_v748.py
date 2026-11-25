"""Clean-source editorial decisions for the complete21 country briefings."""

from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import common_message_entries
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/country_editorial_v748')
ROM = Path('out/all_routes_combined_v747_candidate.nds')
MANUSCRIPT = Path('translations/country_editorial_manuscript_v1.json')
RETAIN = {693, 696, 698, 699, 703, 706}
REVISIONS = {
    688: "Britain is a union of England, Scotland and Wales. It'll keep prospering. Long live the Queen!",
    689: 'The Netherlands only recently won independence from Spain, after a long war.',
    690: "The Hanseatic League once dominated European trade. It's faded since the sea route to India and the New World were discovered.",
    691: 'Sweden only recently gained independence from the Kalmar Union with Denmark and Norway.',
    692: "Portugal? Until recently, it ruled almost all the world's seas.",
    694: 'Since the sea route to India opened, Italian city-states like Genoa and Venice have lost their hold on eastern trade.',
    695: 'Since the Ottoman Turks occupied Greece, all the churches have been turned into mosques.',
    697: "North Africa's cities are all under Ottoman rule. Even the pirates of the Mediterranean seem to answer to the Sultan.",
    700: "You're an infidel, aren't you? ...I have nothing more to say to you.",
    701: "Don't blame others for your misfortune. It all comes from karma in your past life.",
    702: "The kingdoms here once bowed to the Ming Empire. There's not a trace of its former glory left now, though.",
    704: "The Ming dynasty once thrived, but eunuchs now hold all the power. The government is in ever worse chaos. It's dreadful.",
    705: 'Korea became a unified nation under its founder, Yi Seong-gye, about two centuries ago.',
    707: 'Did you know? The Caribbean is full of pirates from all over Europe.',
    708: "Since Spain's Admiral Cortes conquered the Aztec kingdom, conquistadors have flocked to the New World.",
}
MEANINGS = {
    688: 'Britain is a united kingdom of England, Scotland and Wales; the speaker predicts further development and cheers the Queen.',
    689: 'The Netherlands has only recently won independence from Spain following a long war of independence.',
    690: 'The Hanseatic League formerly controlled European trade but has faded markedly since discovery of the India sea route and the New World.',
    691: 'Sweden has recently become independent from the Kalmar Union with Denmark and Norway.',
    692: 'Until quite recently Portugal held almost all the seas of the world; the speaker sounds wistful.',
    693: 'Spain is prospering; people in other countries reportedly call it the empire on which the sun never sets.',
    694: 'Opening the India route stripped Italian city-states such as Genoa and Venice of their eastern-trade rights.',
    695: 'The speaker claims that all the churches became mosques after Ottoman Turkish occupation of Greece.',
    696: 'Istanbul used to be called Constantinople and was capital of the Eastern Roman and Byzantine empires, as the game phrases it.',
    697: 'North African cities are all Ottoman dependencies; even Mediterranean pirates apparently cannot defy the great ruler.',
    698: 'Everyone seeks West African trade rights because the region produces ivory and gold.',
    699: 'Muslim powers once controlled trade in the surrounding region.',
    700: 'The speaker identifies the visitor as an unbeliever and refuses further conversation with an unbeliever.',
    701: 'Do not blame others for your misfortune: it is all due to karma from a previous life.',
    702: 'Surrounding kingdoms once submitted to the Ming Empire; its present prestige is only a shadow of its peak, indeed the speaker says none remains.',
    703: 'Majapahit once held power in these seas but perished under pressure from Muslim powers.',
    704: 'The Ming dynasty formerly prospered; eunuchs now act arbitrarily, government grows more chaotic and the speaker calls it dreadful.',
    705: 'Korea became a unified state under founder Yi Seong-gye around200 years ago.',
    706: 'The long warring-states age is finally approaching its end.',
    707: 'Ask if the listener knows the Caribbean is a haunt of pirates from European countries.',
    708: 'Since Spain\'s Admiral Cortes occupied the Aztec kingdom, many conquistadors have come to the New World.',
}
NOTES = {
    688: 'Restore Britain as the union, distinct from constituent England; preserve the game\'s setting and Queen cheer without substituting modern history.',
    689: 'Won independence is more idiomatic and explicit than broke from Spain; retain only recently and the long war.',
    690: 'Keep the discovery of both the sea route and New World and the loss of commercial dominance in natural spoken prose.',
    691: 'Restore gained independence rather than merely left the union.',
    692: 'Preserve the wistful recent loss of dominance over nearly all seas in fluent prose, without leaving seas isolated on a short final row.',
    694: 'Hold on eastern trade naturally conveys the trade-rights loss; retain the India route and both city-state examples.',
    695: 'The source says all, not many; preserve this NPC\'s historical claim rather than silently qualifying it.',
    697: 'Restore the all-cities scope and tentative seem for the pirates; Sultan follows the established localization of this ruler.',
    700: 'Preserve the religiously hostile refusal and original confirmation question; retain the existing infidel register without adding threats.',
    701: 'Restore your misfortune and the explicit karma concept; this is NPC doctrine, not advice from the translator.',
    702: 'Keep the speaker\'s emphatic judgment about former Ming prestige and the contrast with subject kingdoms.',
    704: 'Restore worsening disorder and the speaker\'s dismay, omitted by the terse current draft.',
    705: 'Became a unified nation is natural English and retains the game\'s founder and approximate chronology.',
    707: 'Restore the conversational Did you know opener and the all-Europe scope.',
    708: 'Replace the generic placeholder with the complete source claim, preserving Admiral, Spain, the Aztec kingdom and arriving conquistadors.',
}


def main():
    assert not MANUSCRIPT.exists()
    ROOT.mkdir(parents=True, exist_ok=True)
    clean, current, canonical = (NdsImage.open(p) for p in ('work/clean.nds', ROM, 'out/raphael_natural_v2_accepted_base.nds'))
    path = '/COMMON/MESFILE.DK4'
    source = common_message_entries(clean.read_file(path), clean.read_file('/__arm9__.bin'))
    before = common_message_entries(current.read_file(path), current.read_file('/__arm9__.bin'), clean=False)
    accepted = common_message_entries(canonical.read_file(path), canonical.read_file('/__arm9__.bin'), clean=False)
    assert sha(ROM.read_bytes()) == read('translations/editorial_review_current_v1.json')['current_integrated_candidate']['sha256']
    rows = []
    for i in range(688, 709):
        old = ' '.join(before[i].text.decode('ascii').split())
        english = old if i in RETAIN else REVISIONS[i]
        rows.append({'id': f'COMMON_MESSAGE_{i}', 'message_id': i,
            'source_hex': source[i].text.hex(), 'japanese': source[i].text.decode('cp932'),
            'canonical_source_hex': accepted[i].text.hex(), 'current_text_hex': before[i].text.hex(),
            'current_English': old, 'english': english + '{PAD}', 'source_meaning': MEANINGS[i],
            'localization_note': NOTES.get(i, 'Retain the already natural wording: it preserves all source facts, register and narrative perspective.'),
            'speaker': 'Original Square shopkeeper selected by town actor getter at5F9C4',
            'context': 'Original5FA60 chooses688+native town region when the company-specific town flag getterB4A88 is nonzero; otherwise709+region selects the separate rumor family. Direct portrait parent54014; independent topic selections, not a sequential history lecture.',
            'decision': 'retain-wording' if i in RETAIN else 'revise',
            'source_reference': {'block': source[i].block, 'record': source[i].record_index, 'native_offset': source[i].block_offset},
            'current_reference': {'block': before[i].block, 'record': before[i].record_index, 'native_offset': before[i].block_offset},
            'review': {'source': True, 'context': False, 'localization': True, 'naturalness': True, 'formatting': False},
            'status': 'source-prose-reviewed-native-context-and-formatting-pending'})
    document = {'format': 'dk4-common-entry-manuscript-v1', 'translation_policy': 'natural-dialogue-v2',
        'encoder': 'dialogue-fixed-v1', 'target_locale': 'en-US', 'review_gates': ['source', 'context', 'localization', 'naturalness', 'formatting'],
        'status': 'editorial-draft-unintegrated', 'file_path': path,
        'source_clean_COMMON_sha256': sha(clean.read_file(path)), 'source_canonical_COMMON_sha256': sha(canonical.read_file(path)),
        'source_ROM_sha256': sha(clean.source.read_bytes()), 'current_ROM_sha256': sha(ROM.read_bytes()), 'records': rows}
    save(MANUSCRIPT, document)
    packet = {'clean_ROM_sha256': sha(clean.source.read_bytes()), 'current_ROM_sha256': sha(ROM.read_bytes()),
        'source_and_current_neighbors': [{'message_id': i, 'Japanese_hex': source[i].text.hex(), 'current_hex': before[i].text.hex()}
                                        for i in range(687, 710)],
        'current_placeholder_IDs': [e.message_id for e in before if b'Here is some local information.' in e.text],
        'full_goal_complete': False}
    save(ROOT / 'source_context_packet.json', packet)
    prose = ['# Country briefings: clean-source editorial review', '', 'Fifteen revisions; six retained wordings. Native/context/format gates remain open.', '']
    for row in rows:
        prose += [f'## {row["message_id"]}: {row["decision"]}', '', row['japanese'].replace('\n', ' / '), '',
                  '**Current:** ' + row['current_English'], '', '**Reviewed:** ' + row['english'].removesuffix('{PAD}'), '',
                  '**Meaning:** ' + row['source_meaning'], '', '**Reason:** ' + row['localization_note'], '']
    (ROOT / 'review.md').write_text('\n'.join(prose), encoding='utf-8')
    print('21 source/prose decisions saved; native context and formatting still pending.', flush=True)


if __name__ == '__main__':
    main()
