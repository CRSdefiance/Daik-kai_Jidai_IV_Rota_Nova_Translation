"""Merge all444 source reviews on V296 with source-native actor metadata.

Compile full paragraphs before choosing fixed storage or a runtime catalog.
Historical preparation/evidence is preserved; no playable ROM is written.
"""

import json
from dataclasses import asdict, replace
from pathlib import Path

from dk4tool.dialogue.codec import parse_markup
from dk4tool.dialogue.encoder import encode_relocatable_dialogue
from dk4tool.dialogue.layout import token_width
from dk4tool.dialogue.profiles import DialogueProfile
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.revalidate_name_migration_v276 import safe_literal_markup

ROOT = Path('work/analysis/reviewed_names_v297')
VERSIONS = (286, 287, 289, 290, 291, 292, 293, 294, 295)
ROM = Path('out/all_routes_combined_v296_candidate.nds')
DIGEST = '6096fb457d460c53964f1fe3c7aac33e152ac7eef28fefe6309e202760497833'


def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8'))


def main():
    ROOT.mkdir(parents=True, exist_ok=True)
    assert sha(ROM.read_bytes()) == DIGEST
    packet_path = Path('work/analysis/confirmed_names_v276/current_route_migration_packet.json')
    packet = read(packet_path)
    ledger, dependencies = {}, {}
    for version in VERSIONS:
        path = Path(f'work/analysis/name_source_review_v{version}/native_correction_proof.json')
        proof = read(path)
        dependencies[str(path)] = sha(path.read_bytes())
        for row in proof['reviewed_records']:
            key = row['file_path'], row['id']
            assert key not in ledger and row['source_context_localization_naturalness_reviewed']
            ledger[key] = row
    assert len(ledger) == len(packet['records']) == 444
    clean, canonical, current = [NdsImage.open(path) for path in (
        'work/clean.nds', 'out/raphael_natural_v2_accepted_base.nds', ROM)]
    paths = sorted({r['file_path'] for r in packet['records']})
    blocks = [{p: IlnkContainer.parse(image.read_file(p)).blocks for p in paths}
              for image in (clean, canonical, current)]
    records, errors = [], []
    for row in packet['records']:
        path, ident = row['file_path'], row['id']
        reviewed = ledger[path, ident]
        block = int(ident.split('_B')[1].split('_')[0])
        index = int(ident.split('_R')[1])
        original_parts = blocks[0][path][block].split(b'\0')
        clean_raw = original_parts[index]
        canonical_raw = blocks[1][path][block].split(b'\0')[index]
        key = blocks[2][path][block].split(b'\0')[index]
        assert reviewed['clean_source_hex'] == clean_raw.hex()
        assert reviewed['canonical_source_hex'] == canonical_raw.hex()
        assert canonical_raw == bytes.fromhex(row['source_hex'])
        data = dict(packet['proposed_profiles_not_registered'][row['proposed_profile']])
        data['leading_speaker_bytes'] = frozenset(data['leading_speaker_bytes'])
        profile = replace(DialogueProfile(**data), balanced_wrapping=True)
        english = reviewed['reviewed_english']
        source_at = sum(len(s) + 1 for s in original_parts[:index])
        actor = None
        metadata_recovery = None
        if blocks[0][path][block][max(0, source_at - 5):source_at] == b'\0\x40\xFF\xFF\0':
            actor = clean_raw[0]
            assert key[0] == actor, 'V296 actor repair must precede preparation'
            profile = replace(profile, name=profile.name + '-native-actor',
                              leading_speaker_bytes=profile.leading_speaker_bytes | {actor})
            tokens = parse_markup(english)
            if not tokens or tokens[0].kind != 'speaker':
                english = f'{{SPEAKER:{actor:02X}}}' + english
                metadata_recovery = 'Original native message header defines actor; add formatter model only, not prose.'
            else:
                assert tokens[0].raw == bytes([actor])
        if ident in ('DK4_MES_B298_R0046', 'DK4_MES_B298_R0054') and path == '/data/SC0.DK4':
            paging = read('work/analysis/dialogue_pagination_v288/actual_page_proof.json')
            assert paging['normal_native_four_row_page_then_complete_continuation_verified']
            profile = replace(profile, max_lines=5)
        markup = safe_literal_markup(english).removesuffix('{PAD}')
        try:
            encoded = encode_relocatable_dialogue(clean_raw, markup, profile)
            target = encoded.encoded
            assert actor is None or target[0] == actor
            padding = len(key) - len(target)
            final_width, lines = 0, 1
            for token in parse_markup(encoded.formatted_markup):
                if token.kind == 'line_break':
                    lines += 1
                    final_width = profile.glyph_width(' ') if profile.guard_linebreaks else 0
                else:
                    final_width += token_width(token, profile)
            padding_safe = padding >= 0 and lines + (final_width + padding * profile.glyph_width(' ')) // profile.window_width_px <= profile.max_lines
            storage = 'fixed' if padding_safe else 'catalog'
            fixed = target + b' ' * padding if padding_safe else None
            profile_data = asdict(profile)
            profile_data['leading_speaker_bytes'] = sorted(profile.leading_speaker_bytes)
            records.append({'file_path': path, 'id': ident, 'clean_source_hex': clean_raw.hex(),
                            'canonical_source_hex': canonical_raw.hex(), 'current_key_hex': key.hex(),
                            'english': english, 'reviewed_prose': reviewed['reviewed_english'],
                            'formatted_markup': encoded.formatted_markup, 'target_hex': target.hex(),
                            'fixed_target_hex': fixed.hex() if fixed is not None else None,
                            'storage': storage, 'old_slot_bytes': len(key), 'complete_target_bytes': len(target),
                            'padding_bytes': padding if padding_safe else None,
                            'native_actor': actor, 'actor_model_recovery': metadata_recovery,
                            'profile': profile_data, 'source_review_ledger': reviewed,
                            'all_source_meananing_and_English_words_retained': True})
        except (ValueError, AssertionError) as error:
            errors.append({'file_path': path, 'id': ident, 'english': english, 'error': str(error)})
    result = {'format': 'dk4-all-reviewed-name-preparation-v297', 'parent_ROM': str(ROM),
              'parent_ROM_sha256': DIGEST, 'packet_sha256': sha(packet_path.read_bytes()),
              'source_review_dependencies': dependencies, 'records': records, 'errors': errors,
              'source_reviews': 444, 'compiled_records': len(records),
              'fixed_records': sum(r['storage'] == 'fixed' for r in records),
              'catalog_records': sum(r['storage'] == 'catalog' for r in records),
              'native_actor_model_recoveries': sum(bool(r['actor_model_recovery']) for r in records),
              'current_source_file_sha256': {p: sha(current.read_file(p)) for p in paths},
              'full_name_COMMON_HELP_art_catalog_and_native_glyph_integration_pending': True,
              'playable_ROM_modified': False, 'full_goal_complete': False}
    (ROOT / 'preparation.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({k: result[k] for k in ('compiled_records', 'fixed_records', 'catalog_records', 'native_actor_model_recoveries')}))
    for error in errors:
        print(error['file_path'], error['id'], error['error'])


if __name__ == '__main__':
    main()
