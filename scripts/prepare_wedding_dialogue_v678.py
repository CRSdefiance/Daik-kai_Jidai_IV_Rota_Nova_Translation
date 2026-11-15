"""Two clean-source editorial repairs, canonical batch and frozen integration inputs."""

from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from dk4tool.script.mesfile import iter_mesfile_records
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/wedding_dialogue_v678')
BATCH = Path('translations/lil_wedding_dialogue_v2.json')


def main():
    ROOT.mkdir(parents=True, exist_ok=True)
    stack = read('translations/release_stack.json')
    paths = {'clean': Path('work/clean.nds'), 'canonical': Path(stack['canonical_baseline']['path']),
             'current': Path('out/all_routes_combined_v666_candidate.nds')}
    sources = {tag: NdsImage.open(path).read_file('/data/SC2.DK4') for tag, path in paths.items()}
    rows = {tag: {r.row_id: r for r in iter_mesfile_records(data, include_non_japanese=True)} for tag, data in sources.items()}
    ids = ('DK4_MES_B70_R0397', 'DK4_MES_B70_R0615')
    original = read('translations/lil_deep_route_v15.json')['records']
    # Source gloss and context are reviewed before the localized paragraphs.
    glosses = {
        ids[0]: 'Camille promises that he will always be at Lil\'s side and protect her, whatever happens.',
        ids[1]: 'Camille realizes he must hurry. Unaccustomed to clothes like these, he has taken too long getting dressed.'}
    packet = []
    for key in ids:
        assert rows['canonical'][key].raw_bytes == rows['clean'][key].raw_bytes
        at = next(i for i, row in enumerate(original) if row['id'] == key)
        neighbors = [row['id'] for row in original[at - 1:at + 2]]
        packet.append({'id': key, 'clean_Japanese': rows['clean'][key].text,
            'source_hex': rows['clean'][key].raw_bytes.hex(), 'source_meaning': glosses[key],
            'adjacent_spoken_records': [{'id': n, 'Japanese': rows['clean'][n].text} for n in neighbors],
            'current_encoded_bytes_for_version_guard_only': rows['current'][key].raw_bytes.hex(),
            'speaker_control09_and_Camille_portrait_name_verified_in_V677': True})
    save(ROOT / 'source_context_review.json', {'records': packet, 'canonical_source_SC2_sha256': sha(sources['canonical']),
        'clean_ROM_sha256': sha(paths['clean'].read_bytes()), 'source_first_editorial_review_not_older_English_as_translation_source': True})
    paragraphs = {
        ids[0]: "You'll always have me by your side to protect you.",
        ids[1]: 'Better hurry! Dressing up like this took me forever!'}
    notes = {
        ids[0]: 'Combines the two emphatic promises into one idiomatic sentence; always preserves the unrestricted commitment. The formatter owns the break, eliminating the orphan final word without a manual break or alignment space.',
        ids[1]: 'Localizes the unfamiliar formal attire and resulting dressing delay as dressing up like this took me forever. Avoids the false garment-specific dress reading of 服. Better hurry is Camille\'s natural self-directed urgency.'}
    batch = {'format': 'dk4-ilnk-translation-batch-v1', 'file_path': '/data/SC2.DK4',
        'source_file_sha256': sha(sources['canonical']), 'encoder': 'dialogue-fixed-v1',
        'dialogue_profile': 'lil-story-deep-route-live', 'translation_policy': 'natural-dialogue-v2',
        'target_locale': 'en-US', 'review_gates': ['source', 'context', 'localization', 'naturalness', 'formatting'],
        'scope': 'Two source-checked Lil wedding chapter records only; original allocations and speaker09 retained.',
        'records': [{'id': key, 'english': '{SPEAKER:09}' + paragraphs[key] + '{PAD}',
            'speaker': 'Camille Marinus Overijssel',
            'context': ('Lil chapter70: Camille reassures Lil during his confession before the later wedding.' if key == ids[0]
                        else 'Lil chapter70: Camille rushes to the wedding after struggling with unfamiliar formal clothes, immediately before his surprised apology and the original wedding movie.'),
            'source_meaning': glosses[key], 'localization_note': notes[key],
            'review': {gate: True for gate in ('source', 'context', 'localization', 'naturalness', 'formatting')}} for key in ids]}
    save(BATCH, batch)
    frozen = read('work/analysis/confirm_material_v572/audit_scope_before.json')
    assert not (ROOT / 'preflight.json').exists()
    save(ROOT / 'preflight.json', {'source_candidate': str(paths['current']),
        'source_candidate_sha256': sha(paths['current'].read_bytes()),
        'source_registry': stack, 'source_registry_sha256': sha(Path('translations/release_stack.json').read_bytes()),
        'source_release_hashes': read('work/analysis/wedding_playback_v677/preflight.json')['release_hashes'],
        'canonical_baseline': stack['canonical_baseline'], 'accepted_layers': stack['accepted_layers'],
        'profile': 'all-routes-unified-v678', 'batch': str(BATCH), 'batch_sha256': sha(BATCH.read_bytes()),
        'previous_goal_turn_classification': 'progress: V677 original M26 playback source pixels/crops/crossfade verified;3511 archive files checked',
        'all_original_audits_before': {name: read(Path('translations') / name) for name in frozen},
        'full_goal_complete': False})
    (ROOT / 'release_stack_before.json').write_bytes(Path('translations/release_stack.json').read_bytes())
    print('V678 two clean-source paragraphs and canonical natural-dialogue-v2 batch prepared.', flush=True)


if __name__ == '__main__':
    main()
