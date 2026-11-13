"""Bind the first source review batch and three fuller translations to evidence."""

import json
from dataclasses import replace
from pathlib import Path

from PIL import Image, ImageDraw

from dk4tool.dialogue.codec import parse_markup
from dk4tool.dialogue.encoder import encode_relocatable_dialogue
from dk4tool.dialogue.profiles import DialogueProfile
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.revalidate_name_migration_v276 import safe_literal_markup
from scripts.verify_fixed_name_glyphs_v279 import expand
from scripts.verify_name_catalog_glyphs_v278 import HEIGHT, WIDTH, expected_pixels, raster
from scripts.verify_ordinary_name_fidelity_research import initialized

ROOT = Path('work/analysis/name_source_review_v286')
PACKET = Path('work/analysis/confirmed_names_v276/current_route_migration_packet.json')
FIXES = {
    'DK4_MES_B218_R0109': (
        "{SPEAKER:05}We don't want anything to do with you either! Let's go, {MACRO:FI}!{PAD}",
        'Claudio', 'The merchant calls Rafael a cheapskate and refuses to sell the ceramic earrings; Claudio returns the dismissal and leaves.',
        'Claudio replies that they have no business with the merchant either, then tells Rafael to leave with him.',
        'Restore the reciprocal dismissal instead of the vague Enough; preserve the angry voice and departure.'),
    'DK4_MES_B223_R0040': (
        '{SPEAKER:07}Oh, Admiral {MACRO:FI}! Listen, there was a pair of swans here.{PAD}',
        'Christina', 'Christina watches a pair of swans by the square lake; Rafael calls to her and she explains what she saw.',
        'Christina recognizes Admiral Rafael, gets his attention and says a pair of swans was here.',
        'Retain Admiral and the conversational lead-in; keep the pair of swans and past presence.'),
    'DK4_MES_B227_R0020': (
        "Yes, I'm {MACRO:FI} {MACRO:FA}. What can I do for you?{PAD}",
        'Rafael', 'A local official politely confirms Admiral Castor\'s identity and then thanks him for investment in the town before asking about King Solomon.',
        'Rafael confirms his full name and asks what the official wants.',
        'Use a complete spoken introduction with both name macros; retain the question in friendly natural English.'),
}


def load(path):
    return json.loads(Path(path).read_text(encoding='utf-8'))


def main(*, start=0, end=100, root=ROOT, fixes=FIXES,
         editorial_path=Path('translations/confirmed_name_editorial_v286.json'), previous_reviewed=0,
         review_version=286, held_indices=(14,), indices=None, presentation_map=None):
    root.mkdir(parents=True, exist_ok=True)
    packet = load(PACKET)
    assert len(packet['records']) == 444
    clean = NdsImage.open('work/clean.nds')
    canonical = NdsImage.open('out/raphael_natural_v2_accepted_base.nds')
    selected_rows = (list(enumerate(packet['records'][start:end], start)) if indices is None
                     else [(index, packet['records'][index]) for index in indices])
    selected_paths = {row['file_path'] for _, row in selected_rows}
    blocks = {path: IlnkContainer.parse(clean.read_file(path)).blocks for path in selected_paths}
    baked = {path: IlnkContainer.parse(canonical.read_file(path)).blocks for path in selected_paths}
    fixed_evidence = Path('work/analysis/name_editorial_v280/fixed/native_proof.json')
    catalog_evidence = Path('work/analysis/name_editorial_v280/catalog_native_proof.json')
    cases = {}
    for path in (fixed_evidence, catalog_evidence):
        for case in load(path)['cases']:
            cases[case['file_path'], case['id']] = (path, case)
    reviewed, corrections, held_records = [], [], []
    native_contexts = {}
    context_cache = {}

    def native_context(path):
        if path not in context_cache:
            name = {'/data/SC0.DK4': 'rafael', '/data/SC1.DK4': 'hodram',
                    '/data/SC2.DK4': 'lil', '/data/SC3.DK4': 'maria'}[path]
            fixture = Path('work/analysis/name_editorial_v280/' + (
                'maria_selection_research_only.nds' if name == 'maria' else 'named_catalog_research_only.nds'))
            report = load(f'work/emulation_v193/name_editorial_v280_{name}/capture_report.json')
            assert report['ROM_sha256'] == sha(fixture.read_bytes())
            assert report['cold_boot'] and not report['savestate_loaded'] and not report['callback_errors']
            snapshot = report['read_only_RAM_snapshot']
            ram = Path(snapshot['path']).read_bytes()
            assert snapshot['read_only_export'] and len(ram) == 4194304 and sha(ram) == snapshot['sha256']
            arm = NdsImage.open(fixture).read_file('/__arm9__.bin')
            cpu = initialized(arm)
            cpu.mem_write(0x02000000, ram)
            native_contexts[path] = {'player': name, 'RAM_snapshot': snapshot,
                                     'research_fixture_sha256': report['ROM_sha256'],
                                     'Maria_is_test_selection_not_legitimate_unlock': name == 'maria'}
            context_cache[path] = (arm, cpu)
        return context_cache[path]
    pictures = []
    for index, row in selected_rows:
        if index in held_indices:
            block = int(row['id'].split('_B')[1].split('_')[0])
            record = int(row['id'].split('_R')[1])
            raw = blocks[row['file_path']][block].split(b'\0')[record]
            held_records.append({'file_path': row['file_path'], 'id': row['id'],
                                 'clean_source_hex': raw.hex(),
                                 'reason': 'Resolve baked actor/preamble and spoken context before changing this record.'})
            continue
        block = int(row['id'].split('_B')[1].split('_')[0])
        record = int(row['id'].split('_R')[1])
        source = bytes.fromhex(row['source_hex'])
        assert baked[row['file_path']][block].split(b'\0')[record] == source
        clean_raw = blocks[row['file_path']][block].split(b'\0')[record]
        evidence_path, case = cases[row['file_path'], row['id']]
        review = {'file_path': row['file_path'], 'id': row['id'],
                  'canonical_source_hex': source.hex(), 'clean_source_hex': clean_raw.hex(),
                  'reviewed_english': row['english'],
                  'source_gloss': row.get('source_meaning'),
                  'context': row.get('context'),
                  'source_context_localization_naturalness_reviewed': True,
                  'prior_complete_native_glyph_evidence': evidence_path.as_posix(),
                  'prior_complete_native_glyph_evidence_sha256': sha(evidence_path.read_bytes()),
                  'prior_expanded_body_hex': case['expanded_body_hex'],
                  'native_full_scene_or_hardware_claim': False}
        if row['id'] in fixes:
            arm, cpu = native_context(row['file_path'])
            english, speaker, context, meaning, note = fixes[row['id']]
            profile_data = dict(packet['proposed_profiles_not_registered'][row['proposed_profile']])
            profile_data['leading_speaker_bytes'] = frozenset(profile_data['leading_speaker_bytes'])
            profile = replace(DialogueProfile(**profile_data), balanced_wrapping=True)
            presentation = (presentation_map or {}).get((row['file_path'], row['id']))
            if presentation:
                assert source.hex().lower() == presentation['expected_source_hex'].lower()
                assert source[0] == clean_raw[0] == presentation['presentation_byte']
                proof_path = Path(presentation['native_proof'])
                assert sha(proof_path.read_bytes()) == presentation['native_proof_sha256']
                profile = replace(profile, name=profile.name + '-source-actor-v295',
                                  leading_speaker_bytes=profile.leading_speaker_bytes | {source[0]})
            formatter_reserve = 0
            pagination_pending = False
            verified_pagination = None
            markup = safe_literal_markup(english).removesuffix('{PAD}')
            try:
                encoded = encode_relocatable_dialogue(source, markup, profile)
            except ValueError as error:
                if not any(code in str(error) for code in ('pair-phase-auto-wrap', 'page-overflow')):
                    raise
                # A taller diagnostic canvas preserves the complete paragraph.
                # This does not approve its actual four-row story display.
                pagination_pending = True
                profile = replace(profile, name=profile.name + '-pagination-research', max_lines=5)
                encoded = encode_relocatable_dialogue(source, markup, profile)
                paging_path = Path('work/analysis/dialogue_pagination_v288/actual_page_proof.json')
                if paging_path.exists():
                    paging = load(paging_path)
                    paging_fixture = load('work/analysis/dialogue_pagination_v288/fixture_manifest.json')
                    if (paging.get('normal_native_four_row_page_then_complete_continuation_verified')
                            and row['file_path'] == '/data/SC0.DK4'
                            and row['id'] in paging['both_identical_puzzle_bodies_covered']
                            and sha(Path(paging_fixture['research_ROM']).read_bytes()) == paging['ROM_sha256']
                            and bytes.fromhex(paging_fixture['complete_target_hex'])[1:] == encoded.encoded[1:]):
                        verified_pagination = paging_path.as_posix()
                        pagination_pending = False
            payload = encoded.encoded
            tokens = parse_markup(encoded.formatted_markup)
            if tokens and tokens[0].kind == 'speaker':
                assert payload[0] == source[0]
                payload = payload[1:]
            expanded = expand(cpu, payload)
            canvas_height = 96 if pagination_pending or verified_pagination else HEIGHT
            pixels, events, font = raster(arm, expanded, canvas_height=canvas_height)
            assert pixels == expected_pixels(arm, font, events, canvas_height=canvas_height)
            semantic = [('ascii', ord(c)) if len(c.encode('cp932')) == 1 else
                        ('cp932', int.from_bytes(c.encode('cp932'), 'big'))
                        for c in expanded.decode('cp932') if c not in ' \n']
            assert [(e['kind'], e['code']) for e in events if e['code'] != 32] == semantic
            lines = sorted({e['y'] for e in events if e['code'] != 32})
            assert lines == list(range(0, len(lines) * 16, 16)) and len(lines) <= canvas_height // 16
            image = Image.new('RGB', (WIDTH, canvas_height))
            image.putdata([(239, 232, 201) if p == 0 else (0, 8, 0) if p == 1 else (98, 97, 98) for p in pixels])
            pictures.append((row['id'], image.resize((WIDTH * 3, canvas_height * 3), Image.Resampling.NEAREST)))
            corrected = {'file_path': row['file_path'], 'id': row['id'],
                         'expected_source_hex': row['source_hex'], 'expected_previous_english': row['english'],
                         'clean_source_hex': clean_raw.hex(), 'clean_Japanese': row['japanese_source'],
                         'english': english, 'speaker': speaker, 'context': context,
                         'source_meaning': meaning, 'localization_note': note,
                         'translation_policy': 'natural-dialogue-v2', 'target_locale': 'en-US',
                         'review': dict.fromkeys(('source', 'context', 'localization', 'naturalness', 'formatting'), True),
                         'formatted_markup': encoded.formatted_markup, 'compiled_target_hex': encoded.encoded.hex(),
                         'old_slot_bytes': len(source), 'complete_target_bytes': len(encoded.encoded),
                         'formatter_pair_phase_reserve_pixels': formatter_reserve,
                         'actual_native_surface_width_unchanged': WIDTH,
                         'native_research_canvas_height': canvas_height,
                         'actual_four_row_pagination_verification_pending': pagination_pending,
                         'shared_actual_paged_display_proof': verified_pagination,
                         'compiler_max_lines': profile.max_lines,
                         'presentation_recovery': presentation,
                         'allocation_or_catalog_integration_pending': True,
                         'actual_route_expanded_body_hex': expanded.hex(),
                         'complete_independent_font_pixels_glyph_order_bounds_and_guards_pass': True}
            corrections.append(corrected)
            corrected['review']['formatting'] = not pagination_pending
            review.update({'reviewed_english': english, 'source_gloss': meaning, 'context': context,
                           'new_complete_native_glyph_evidence': str(root / 'native_correction_proof.json')})
        reviewed.append(review)
    assert len(reviewed) == len(selected_rows) - len(held_records) and len(corrections) == len(fixes)
    row_height = 96 * 3 + 20
    sheet = Image.new('RGB', (WIDTH * 3, len(pictures) * row_height), 'white')
    draw = ImageDraw.Draw(sheet)
    for index, (name, image) in enumerate(pictures):
        y = index * row_height
        draw.text((0, y), name, fill='black')
        sheet.paste(image, (0, y + 20))
    sheet.save(root / 'correction_review.png')
    for start_row in range(0, len(pictures), 4):
        subset = pictures[start_row:start_row + 4]
        page = Image.new('RGB', (WIDTH * 3, len(subset) * row_height), 'white')
        label = ImageDraw.Draw(page)
        for number, (name, image) in enumerate(subset):
            label.text((0, number * row_height), name, fill='black')
            page.paste(image, (0, number * row_height + 20))
        page.save(root / f'correction_review_{start_row // 4 + 1:02d}.png')
    document = {'format': 'dk4-confirmed-name-editorial-overrides-v1', 'not_a_release_batch': True,
                'records': corrections, 'native_visual_reviewed': False}
    editorial_path.write_text(json.dumps(document, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    proof = {'format': f'dk4-name-source-review-batch-v{review_version}', 'packet_sha256': sha(PACKET.read_bytes()),
             'reviewed_records': reviewed, 'native_corrections': corrections,
             'unchanged_reviewed_records': len(reviewed) - len(corrections),
             'complete_source_reviewed_records': len(reviewed),
             'cumulative_source_reviewed_records': previous_reviewed + len(reviewed),
             'remaining_source_review_records': 444 - previous_reviewed - len(reviewed),
             'held_records': held_records,
             'native_player_contexts': native_contexts,
             'new_corrections_native_pixels_and_route_macro_guards_pass': True,
             'full444_source_review_and_integration_pending': True,
             'playable_ROM_modified': False, 'full_goal_complete': False}
    (root / 'native_correction_proof.json').write_text(json.dumps(proof, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(f'{len(reviewed)} source reviews; {len(corrections)} corrections have complete native glyphs; {proof["remaining_source_review_records"]} source reviews remain.')


if __name__ == '__main__':
    main()
