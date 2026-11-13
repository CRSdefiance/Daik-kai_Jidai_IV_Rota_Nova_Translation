"""Review independent regional rumors against exact clean Japanese selections."""

from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import common_message_entries
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/regional_rumors_v749')
ROM = Path('out/all_routes_combined_v748_candidate.nds')
MANUSCRIPT = Path('translations/regional_rumors_manuscript_v1.json')
RETAIN = {713, 714, 716, 717, 722, 723, 726, 727, 728}
TEXTS = {
    709: "Clifford used to be a pirate, but I hear the Queen knighted him for his service as a naval admiral.",
    710: "These days, even young women are setting sail to trade. Times certainly have changed!",
    711: "Speyer works hard leading the fading Hanseatic League. I wish he'd be a bit more realistic...",
    712: "I hear Sweden's new naval fleet lives by self-sufficiency, funding its operations through trade and privateering.",
    715: "The Centurione Company once traded far and wide, as if the Mediterranean belonged to it.",
    718: "Admiral Hayreddin took his father-in-law's name. The man was so great, the Ottomans made him Sultan of Algiers!",
    719: "That Silveira is such a miser! He's far richer than we are, yet he's so cheap. Honestly!",
    720: "Espinosa's crimes are countless. Everyone turns a blind eye, though. Who knows what he'd do to anyone who stood up to him...",
    721: "Admiral Uddin can more than hold his own against the European powers. We can count on him! They say he's Arab royalty.",
    724: "Kuhn will stop at nothing to turn a profit. Oh, please don't tell anyone you heard that from me...",
    725: "They say an empress would ruin China. I disagree. If only that female admiral who routs Japanese pirates ruled our country...",
    729: "I hear Governor Escante will be appointed Viceroy of Mexico and Peru one day.",
}
MEANINGS = {
    709: "Clifford was formerly a pirate; the speaker has heard that, as a naval admiral, he received the title Sir from the Queen.",
    710: "The speaker marvels that nowadays even young women go out by ship to conduct trade.",
    711: "Speyer works hard leading the declining Hanseatic League; the speaker wishes he would see reality a little more clearly.",
    712: "Sweden's newly established naval fleet reportedly makes self-sufficiency its motto, paying operating costs through trade and privateering.",
    713: "Admiral Albuquerque's ancestor reportedly distinguished himself long ago commanding Portuguese fleets in the Indian Ocean.",
    714: "The Spanish navy led by Admiral Valdes is called the Invincible Armada because of the formidable strength of its fleet.",
    715: "The Centurione Company formerly operated widely and sailed the Mediterranean as though it owned it.",
    716: "Athens continues, as always, to be blessed with profitable trade goods.",
    717: "The Ottoman Turkish Empire controls the eastern Mediterranean.",
    718: "Admiral Hayreddin inherited the name of his giri-no-chichi (father-in-law, a non-birth father). That man was so distinguished that the Ottoman Empire invested him as Sultan, meaning king, of Algiers.",
    719: "Silveira is exceptionally miserly; despite being much richer than the speaker and their peers, he is terribly cheap. The speaker complains emphatically.",
    720: "Espinosa has committed countless evil deeds. Everyone pretends not to see them because they do not know what he might do if opposed.",
    721: "Uddin is a reassuring figure who can fight the European powers on equal or better terms; rumor says he is Arab royalty.",
    722: "Nagalpur lives comfortably while money comes rolling in; the speaker envies his position intensely.",
    723: "Admiral Pereira is a tough, thoroughly patriotic man, but utterly ruthless toward anyone outside his own group.",
    724: "Kuhn uses any means for commercial profit; the speaker suddenly asks the listener to conceal who said this.",
    725: "In China people say a female emperor ruins the country, but the speaker does not believe it and wishes the female admiral who scatters Japanese pirates were ruler here.",
    726: "Whether Hideyoshi or Kurushima, the speaker vows to drive them away every time they come.",
    727: "After his defeat by Nobunaga, Kurushima reportedly became captivated by and obsessed with the strength of ironclad ships.",
    728: "Maldonado is unable to resist gold and shiny valuables.",
    729: "The speaker has heard Governor Escante is expected eventually to take office as Viceroy of Mexico and Peru.",
}
NOTES = {
    709: "Restore the former pirate, naval admiral and Queen's knighthood as hearsay. Knighted naturally conveys receiving Sir without inventing a new inherited rank.",
    710: "Restore the speaker's surprise at young women entering maritime trade; times have changed voices that surprise rather than inventing a new event.",
    711: "Keep both respect for his efforts and the regretful wish for greater realism; do not turn the wish into an accusation of insanity.",
    712: "Privateering preserves the specific authorized-raiding term shiraku, distinct from generic piracy; retain operating funds and self-sufficiency as reported policy.",
    715: "Keep the company, former wide operations and cocky Mediterranean image; Centurione follows the current ARM9 name spelling.",
    718: "The Japanese explicitly states giri-no-chichi, not biological father. Read it as father-in-law and preserve inheritance of the name and Ottoman appointment of that earlier man, not the present admiral. Sultan is already the established English title; its Japanese parenthetical king need not be repeated. No spouse name or adoption story is invented.",
    719: "Restore the complaining voice and richer-than-us comparison without adding a claim about a specific failed transaction.",
    720: "Keep both countless crimes and the community's deliberate silence out of fear, without inventing a specific punishment.",
    721: "More than hold his own preserves equal-or-better military standing. Keep the speaker's confidence and mark royal ancestry as rumor.",
    724: "Preserve the abrupt confidential aside and ruthless pursuit of profit; use the established Kuhn spelling.",
    725: "Keep the contrast between prejudice and the speaker's wish. Empress establishes the female-ruler meaning, so ruled our country avoids the awkward emperor for a woman; both references are to the same admiral. No extra identity is inserted.",
    729: "Preserve both Mexico and Peru, the expected future appointment and hearsay. Do not turn the rumor into a completed promotion.",
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
    for i in range(709, 730):
        old = ' '.join(before[i].text.decode('cp932').split())
        english = old.replace('ï¼©', 'I') if i in RETAIN else TEXTS[i]
        rows.append({'id': f'COMMON_MESSAGE_{i}', 'message_id': i,
            'source_hex': source[i].text.hex(), 'japanese': source[i].text.decode('cp932'),
            'canonical_source_hex': accepted[i].text.hex(), 'current_text_hex': before[i].text.hex(),
            'current_English': old, 'english': english + '{PAD}', 'source_meaning': MEANINGS[i],
            'localization_note': NOTES.get(i, 'Retain the natural wording and all source facts; normalize the old full-width Latin I to the proven safe literal ASCII path where present.'),
            'speaker': 'Original Square shopkeeper selected by town actor getter at5F9C4',
            'context': 'Original5FA60 selects709+native town region when the current-company town-share getterB4A88 returns zero; nonzero selects the separately reviewed688+region country family. Direct portrait parent54014. Each is an independent regional rumor, not consecutive dialogue.',
            'decision': 'retain-wording' if i in RETAIN else 'revise',
            'source_reference': {'block': source[i].block, 'record': source[i].record_index, 'native_offset': source[i].block_offset},
            'current_reference': {'block': before[i].block, 'record': before[i].record_index, 'native_offset': before[i].block_offset},
            'review': {'source': True, 'context': False, 'localization': True, 'naturalness': True, 'formatting': False},
            'status': 'source-prose-reviewed-native-context-and-formatting-pending'})
    save(MANUSCRIPT, {'format': 'dk4-common-entry-manuscript-v1', 'translation_policy': 'natural-dialogue-v2',
        'encoder': 'dialogue-fixed-v1', 'target_locale': 'en-US',
        'review_gates': ['source', 'context', 'localization', 'naturalness', 'formatting'],
        'status': 'editorial-draft-unintegrated', 'file_path': path,
        'source_clean_COMMON_sha256': sha(clean.read_file(path)), 'source_canonical_COMMON_sha256': sha(canonical.read_file(path)),
        'source_ROM_sha256': sha(clean.source.read_bytes()), 'current_ROM_sha256': sha(ROM.read_bytes()), 'records': rows})
    save(ROOT / 'source_context_packet.json', {'clean_ROM_sha256': sha(clean.source.read_bytes()),
        'current_ROM_sha256': sha(ROM.read_bytes()),
        'source_and_current_neighbors': [{'message_id': i, 'Japanese_hex': source[i].text.hex(), 'current_hex': before[i].text.hex()}
                                        for i in range(708, 731)],
        'full_goal_complete': False})
    prose = ['# Regional rumors: clean-source editorial review', '', 'Twelve revisions and nine retained wordings. Native/context/format gates remain open.', '']
    for row in rows:
        prose += [f'## {row["message_id"]}: {row["decision"]}', '', row['japanese'].replace('\n', ' / '), '',
                  '**Current:** ' + row['current_English'], '', '**Reviewed:** ' + row['english'].removesuffix('{PAD}'), '',
                  '**Meaning:** ' + row['source_meaning'], '', '**Reason:** ' + row['localization_note'], '']
    (ROOT / 'review.md').write_text('\n'.join(prose), encoding='utf-8')
    print('21 regional rumors source/prose reviewed; native and gameplay checks pending.', flush=True)


if __name__ == '__main__':
    main()
