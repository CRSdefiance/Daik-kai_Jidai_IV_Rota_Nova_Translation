"""Review Sound Setup track titles against clean and registered COMMON records."""

from collections import Counter
from hashlib import sha256
from pathlib import Path

from dk4tool.patch.bgm_title_tracking import title_geometry
from dk4tool.patch.duel_editorial import owned_entries
from dk4tool.script.common_message_table import DIRECTORY_OFFSET, TABLE_OFFSET, common_message_entries
from scripts import prepare_common_bgm_complete_titles as previous
from scripts import register_ancient_map_text_v2 as parent
from scripts.seal_shared_text_source_v1 import reference
from scripts.verify_native_sound_selector import SELECTOR_CODE_RANGES


base, ARM, COMMON, CLEAN = parent.base, parent.stage.ARM, parent.stage.COMMON, parent.stage.prior.document.CLEAN
OUTPUT = Path('translations/editorial_checkpoints/SharedText_20261110_v1/sound_bgm_titles_context_v1.json')

# Follow the original track order. Each note explains a specific wording decision.
NOTES = (
    'Captures the buoyant energy in the title without assigning it to a specific character or event.',
    'The plain closing-track label matches the paired Opening entry.',
    'Keeps the sense of sailing with a wind from behind and reads smoothly as a track title.',
    'Departure keeps the original setting-out theme without specifying where the journey starts.',
    'The invitation and friendly tone carry the Japanese volitional form.',
    'A lyrical plural keeps India as the source of the wind and suits the regional track titles.',
    'The geographic phrasing retains the southern seas and leaves the particular islands unspecified.',
    'Keeps the region explicit and treats its waters as the setting.',
    'The familiar phrase preserves the motion and promise of what lies past the horizon.',
    'Use Northern European to identify the setting naturally alongside the Southern European title.',
    'Use Southern European to match the paired northern town title and keep the location clear.',
    'Retains the source’s cultural region and the town setting without assigning a country.',
    'Plain geographic label consistent with the other town themes.',
    'Keeps India as the town’s setting in the original run of regional titles.',
    'Keeps the narrower village setting and the full Southeast Asian region.',
    'The straightforward title preserves the source setting and the recurring town-title pattern.',
    'Retains Japan and the original town scale.',
    'Preserves the historical New World terminology used by this game and the town-track pattern.',
    'Names the sea-battle theme directly and distinguishes it from the following larger battle.',
    'Great retains the battle’s scale and Naval keeps it at sea.',
    'The road and its destination both carry the title’s image.',
    'True Treasure keeps the source open as to what the treasure represents.',
    'The plural reads naturally for the motion of the sea.',
    'Keeps the metaphor and intensity of passion in a short title.',
    'Use the approved spelling Rafael, consistent with his story and other player-facing text.',
    'The existing title already uses the approved name Hodram.',
    'Use the approved spelling Camille. The ampersand connects the same two names as the Japanese title.',
    'The repeated call and exclamation marks preserve the original enthusiasm.',
    'The title retains the image of gathering trouble without spelling out a particular threat.',
    'Fair Maiden matches the deliberately old-fashioned register of the title.',
    'Keeps the feeling unspecified and leaves room for the musical context.',
    'Merry and Companions preserve the upbeat group feeling and fit the period register.',
    'Sorrow keeps the emotional weight of the short title.',
    'The title preserves both piracy and the explicit King title.',
    'Conqueror conveys conquest and preserves the identity implied by the definite article.',
    'Keeps both the opponent’s strength and the moment of their arrival.',
    'The emphatic Great and exclamation point carry the celebration.',
    'The plain opening-track label matches Ending.',
)
REVISIONS = {3260: 'Northern European Town', 3261: 'Southern European Town',
             3275: 'Rafael', 3277: 'Lil & Camille'}


def main():
    assert not OUTPUT.exists()
    release = base.load(parent.RELEASE)
    assert base.digest(parent.ROM) == release['candidate_sha256']
    assert base.digest(CLEAN) == release['clean_input_sha256']
    clean, current = (base.NdsImage.open(path) for path in (CLEAN, parent.ROM))
    clean_arm, arm = (image.read_file(ARM) for image in (clean, current))
    source = common_message_entries(clean.read_file(COMMON), clean_arm)
    old = owned_entries(current.read_file(COMMON), arm, sha256(arm[DIRECTORY_OFFSET:TABLE_OFFSET]).hexdigest())
    records = []
    for n, ((japanese, inherited, gloss), note) in enumerate(zip(previous.TITLES, NOTES, strict=True), 3251):
        clean_row, old_row = source[n], old[n]
        assert clean_row.text.decode('cp932') == japanese and old_row.text.decode('ascii') == inherited
        proposed = REVISIONS.get(n, inherited)
        geometry = title_geometry(proposed, 5)
        assert proposed.isascii() and geometry['fits_panel']
        records.append(dict(id=f'COMMON_MESSAGE_{n}', message_ID=n, file_path=COMMON, source_Japanese=japanese,
            source_reference=reference(clean_row), source_hex=clean_row.text.hex(), source_meaning=gloss,
            current_English=inherited, current_reference=reference(old_row), current_hex=old_row.text.hex(),
            english=proposed, decision='revision' if n in REVISIONS else 'retention', localization_note=note,
            speaker='Sound Setup music title', context='Single centered track title in the original Sound Setup BGM selector.',
            original_substitution_count=0, planned_geometry=geometry,
            review=dict(source=True, context=True, localization=True, naturalness=True, formatting=False)))
    ledger = base.load(base.LEDGER)
    credited = {(row['file_path'], row['id']) for row in ledger[base.CONTEXT]['integrated_record_keys']}
    assert not any((row['file_path'], row['id']) in credited for row in records)
    counts = Counter(row['decision'] for row in records)
    assert counts == {'revision': 4, 'retention': 34}
    base.save(OUTPUT, dict(translation_policy='natural-dialogue-v2', target_locale='en-US', encoder='dialogue-relocatable-v1',
        review_gates=['source', 'context', 'localization', 'naturalness', 'formatting'],
        records=records, counts=counts, current_ROM_sha256=release['candidate_sha256'], clean_ROM_sha256=release['clean_input_sha256'],
        selector_code=[dict(start=first, end=last, sha256=sha256(arm[first:last]).hexdigest())
                       for first, last in SELECTOR_CODE_RANGES],
        formatter_evidence='translations/bgm_title_native_layout_evidence_v155.json',
        formatting_pending=True, gameplay_pending=True, new_credit=0, full_goal_complete=False))
    print(f'{len(records)} Sound Setup titles reviewed: four proposed revisions and 34 justified retentions.')


if __name__ == '__main__':
    main()
