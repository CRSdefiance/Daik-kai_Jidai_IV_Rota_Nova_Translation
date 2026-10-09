"""Finish two preset labels with complete native ink and exact V166 inheritance."""

import argparse
import copy
import json
import struct
from pathlib import Path

from PIL import Image, ImageDraw

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.graphics.pxl import PxlImage
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.xdelta import apply_xdelta, make_xdelta
from dk4tool.rom.nds import NdsImage
from scripts.build_integrated_release import (
    CANONICAL_BASELINE_SHA256,
    RELEASE_STACK_PATH,
    accepted_batch_paths,
    apply_ilnk_pxl_sync_batch,
    apply_pxl_native_label_batch,
    load_release_stack,
    resolve_release_batches,
    rom_files,
    verify_golden_content,
)
from scripts.fleet_row_graphics_v162 import save
from scripts.frame_buttons_v165 import (
    ARCHIVE,
    BASE,
    RESOURCE,
    atlas_indices,
    embedded_preview,
)
from scripts.frame_crew_buttons_v166 import BATCH as OLD_BATCH
from scripts.frame_crew_buttons_v166 import SYNC as OLD_SYNC
from scripts.frame_crew_buttons_v166 import targets as old_targets
from scripts.probe_button_prompt_native import HEADER, STACK, call, machine
from scripts.probe_name_treasure_graphics_v161 import sizing

PRIOR = Path('out/all_routes_combined_v166_candidate.nds')
PRIOR_SHA = 'd53b7d22c913bf862f10f09b4a456326950173870887732bf2eb17c61c415ee5'
CANDIDATE = Path('out/all_routes_combined_v167_candidate.nds')
PROFILE = 'all-routes-unified-v167'
BATCH = Path('translations/frame_action_buttons_graphics_v3.json')
SYNC = Path('translations/frame_action_buttons_cmmnimg_sync_v3.json')
OUT = Path('work/qa/frame_buttons_v167')
ART = Path('work/analysis/frame_buttons_v167_artwork.json')
NATIVE = Path('work/analysis/frame_buttons_v167_native.json')
LABELS = [('旗艦重視', 'Flagship', [91, 162, 133, 173], 'Prioritize assigning sailors to the flagship.'),
          ('均等補給', 'Fill Evenly', [91, 178, 133, 189], 'Refill water and food evenly.') ]


def sources():
    if sha(BASE.read_bytes()) != CANONICAL_BASELINE_SHA256 or sha(PRIOR.read_bytes()) != PRIOR_SHA:
        raise ValueError('Exact canonical and V166 sources required')
    base, prior, clean = [NdsImage.open(p) for p in (BASE, PRIOR, Path('work/clean.nds'))]
    for path in (RESOURCE, ARCHIVE):
        if base.read_file(path) != clean.read_file(path):
            raise ValueError('Exact clean Japanese source required')
    if tuple(prior.read_file(p) for p in (RESOURCE, ARCHIVE)) != old_targets():
        raise ValueError('V166 does not match its reviewed graphics batches')
    return base, prior


def targets():
    base, prior = sources()
    target, _ = apply_pxl_native_label_batch(BATCH, base.read_file(RESOURCE), prior.read_file('/__arm9__.bin'))
    embedded, _ = apply_ilnk_pxl_sync_batch(SYNC, base.read_file(ARCHIVE), target)
    return target, embedded


def source_context():
    raw = NdsImage.open('work/clean.nds').read_file('/COMMON/HELP.DK4')
    entries = []
    for needle in ('［旗艦重視］旗艦へ優先的に配置。', '水・食料を均等に最大量まで補給'):
        offset = raw.find(needle.encode('cp932'))
        if offset < 0:
            raise ValueError('Original Help context differs')
        start, end = raw.rfind(b'\0', 0, offset) + 1, raw.find(b'\0', offset)
        entries.append({'start': start, 'end': end, 'japanese': raw[start:end].decode('cp932')})
    return {'file': '/COMMON/HELP.DK4', 'source_sha256': sha(raw), 'entries': entries,
            'correction': 'The source graphic says 旗艦重視 (flagship priority), not 横帆重視 (square-sail priority). Original Help independently confirms this.',
            'supply_scope': 'Help confirms even replenishment of water and food; actual contexts of this shared sprite still require native mapping.'}


def layout_masks(source, batch):
    """Independent native masks; store complete cell origins for every letter."""
    font = GameAsciiFont.from_arm9(source)
    canvas = Image.new('L', (256, 256))
    positions, widths = [], []
    for row in batch['records']:
        x0, y0, x1, y1 = row['box']
        glyphs = [font.decode(c).convert('L') for c in row['text']]
        proportional = row.get('glyph_spacing') == 'native-ink-v1'
        metrics = []
        for c, glyph in zip(row['text'], glyphs, strict=True):
            bounds = glyph.getbbox()
            if glyph.crop((0, 0, 6, 2)).getbbox() or (bounds and bounds[2] > 5):
                raise ValueError('Visible native glyph would be cropped')
            if bounds is None and c != ' ':
                raise ValueError('Unexpected blank native glyph')
            metrics.append((bounds[0] if bounds else 0,
                            bounds[2] - bounds[0] + 1 if bounds else 3)
                           if proportional else (0, batch['advance']))
        width = sum(m[1] for m in metrics)
        if width > x1 - x0:
            raise ValueError('Complete label exceeds its original button')
        x = x0 + (x1 - x0 - width) // 2
        y = y0 + (y1 - y0 - 9) // 2 - 2
        origins = []
        for glyph, (bearing, step) in zip(glyphs, metrics, strict=True):
            origin = (x - bearing, y)
            canvas.paste(glyph, origin, glyph)
            origins.append(origin)
            x += step
        positions.append(origins)
        widths.append(width)
    return canvas, positions, widths


def real_format_glyphs(source, target, batch, expected_mask=None):
    p = PxlImage.from_bytes(target)
    expected, positions, widths = layout_masks(source, batch)
    if expected_mask is not None:
        expected = expected_mask
    packed = bytes(p.indices)
    p.indices[:] = bytes(len(p.indices))
    blank = p.to_bytes()
    uc = machine(source)
    uc.mem_write(HEADER - 16, b'\xA5' * (len(blank) + 32))
    uc.mem_write(HEADER, blank)
    executed = set()
    proportional_cases = []
    for row, origins in zip(batch['records'], positions, strict=True):
        if row.get('glyph_spacing') == 'native-ink-v1':
            continue
        for char, (x, y) in zip(row['text'], origins, strict=True):
            uc.mem_write(STACK, struct.pack('<2I', ord(char), batch['color_index']))
            executed |= call(uc, 0xD16B4, (0, HEADER, x, y))
    result = PxlImage.from_bytes(bytes(uc.mem_read(HEADER, len(blank))))
    combined = bytearray(result.indices)
    # The native four-bit font routine clears all six columns, including
    # blank side bearings. It cannot draw overlapping cells sequentially.
    # Verify each proportional glyph in isolation, then compose its complete
    # native ink offline, as the bitmap generator does. This is glyph/storage
    # proof, not a claim that live native text acquired proportional spacing.
    font = GameAsciiFont.from_arm9(source)
    for row, origins in zip(batch['records'], positions, strict=True):
        if row.get('glyph_spacing') != 'native-ink-v1':
            continue
        for char, (x, y) in zip(row['text'], origins, strict=True):
            uc.mem_write(HEADER, blank)
            uc.mem_write(STACK, struct.pack('<2I', ord(char), batch['color_index']))
            executed |= call(uc, 0xD16B4, (0, HEADER, x, y))
            raster = PxlImage.from_bytes(bytes(uc.mem_read(HEADER, len(blank))))
            single = Image.new('L', (256, 256))
            single.paste(font.decode(char).convert('L'), (x, y))
            wanted = bytes(batch['color_index'] if value else 0 for value in single.tobytes())
            if (bytes(raster.indices) != wanted
                    or raster.source[:p.pixels_offset] != blank[:p.pixels_offset]):
                raise ValueError('Isolated native glyph lost ink or gained pixels')
            for i, value in enumerate(raster.indices):
                if value:
                    combined[i] = value
            proportional_cases.append({'character': char, 'cell_origin': [x, y],
                                       'complete_native_raster_sha256': sha(wanted)})
    pixels = bytes(batch['color_index'] if value else 0 for value in expected.tobytes())
    if (bytes(combined) != pixels or not {0x020D16B4, 0x020D1820} <= executed
            or result.source[:p.pixels_offset] != blank[:p.pixels_offset]
            or bytes(uc.mem_read(HEADER - 16, 16)) != b'\xA5' * 16
            or bytes(uc.mem_read(HEADER + len(blank), 16)) != b'\xA5' * 16):
        raise ValueError('Complete native preset raster/first letter/header/guards differ')
    for row in batch['records']:
        x0, y0, x1, y1 = row['box']
        for y in range(y0, y1):
            for x in range(x0, x1):
                if (packed[y * 256 + x] == batch['color_index']) != bool(pixels[y * 256 + x]):
                    raise ValueError('Packed preset glyph pixels/first letter differ')
    return {'dimensions': [256, 256], 'format': 'actual-source-four-bit-PXL',
            'complete_native_pixel_sha256': sha(pixels), 'all_glyph_cells_ABI_header_and_guards_pass': True,
            'label_widths': widths, 'isolated_proportional_glyphs': proportional_cases,
            'composition_scope': 'Fixed labels execute together. Proportional glyphs execute separately in actual source format; their full native ink is composed offline and checked against packed pixels. No live proportional font consumer claimed.',
            'preset_layout': 'Flagship fixed advance; Fill Evenly native ink widths plus one blank column, three-column word space. No ink cropped.'}


def materialize():
    base, prior = sources()
    batch = copy.deepcopy(json.loads(OLD_BATCH.read_text(encoding='utf-8')))
    for jp, text, box, meaning in LABELS:
        batch['records'].append({
            'id': 'DK4_FRAME_' + text.upper().replace(' ', '_') + '_GRAPHIC_V3',
            'source_japanese': jp, 'source_meaning': meaning, 'text': text, 'box': box,
            'context': 'Crew distribution flagship priority preset.' if text == 'Flagship' else 'Shared water/food replenishment button; native context mapping remains pending.',
            'glyph_spacing': 'fixed' if text == 'Flagship' else 'native-ink-v1',
            'localization_note': 'Flagship names the priority preset documented in original Help. Fill Evenly retains the equal-refill action; proportional spacing removes blank side bearings only, with every visible native pixel retained.',
            'background_note': 'Original white faces/dark shadows reconstructed from nearest row colors only within this lettering rectangle; chrome exact.',
            'review': {'source': True, 'context': True, 'localization': True,
                       'naturalness': True, 'formatting': True, 'visual': False,
                       'physical_gameplay': False}})
    batch['supersedes'] = OLD_BATCH.as_posix()
    batch['preserved_record_ids'] = [r['id'] for r in batch['records'][:10]]
    save(BATCH, batch)
    target, _ = apply_pxl_native_label_batch(BATCH, base.read_file(RESOURCE), prior.read_file('/__arm9__.bin'))
    sync = copy.deepcopy(json.loads(OLD_SYNC.read_text(encoding='utf-8')))
    sync['source_image_sha256'] = sha(target)
    sync['supersedes'] = OLD_SYNC.as_posix()
    sync['scope'] = 'Exact canonical matching right half, all ten prior labels plus two preset buttons; no unrelated storage changes. Native banks/consumers pending.'
    save(SYNC, sync)
    target, embedded = targets()
    OUT.mkdir(parents=True, exist_ok=True)
    sheet = Image.new('RGB', (1100, 900), '#303030')
    draw = ImageDraw.Draw(sheet)
    for i, (label, raw) in enumerate((('Original Japanese frame', base.read_file(RESOURCE)), ('English frame: V167', target))):
        raster = PxlImage.from_bytes(raw).render().convert('RGB')
        x = 12 + i * 550
        draw.text((x, 8), label, fill='white')
        sheet.paste(raster.resize((512, 512), Image.Resampling.NEAREST), (x, 28))
        draw.text((x, 552), 'Crew buttons', fill='white')
        sheet.paste(raster.crop((38, 158, 186, 210)).resize((518, 182), Image.Resampling.NEAREST), (x, 576))
    sheet.save(OUT / 'review.png')
    embedded_preview(embedded).save(OUT / 'english_embedded_bank_zero.png')
    save(ART, {'status': 'draft-two-new-presets-ten-prior-labels-exact',
               'source_sha256': sha(base.read_file(RESOURCE)), 'target_sha256': sha(target),
               'visual_review': False, 'embedded_bank_zero_review': False,
               'labels_added': [x[1] for x in LABELS], 'prior_labels_preserved': 10,
               'native_palette_bank_and_live_consumers_proved': False})
    save(OUT / 'source_context.json', source_context())
    print('Materialized two preset buttons in expanded canonical batches; ten earlier labels retained.')


def preservation(target, embedded):
    base, prior = sources()
    before, after = [PxlImage.from_bytes(raw) for raw in (prior.read_file(RESOURCE), target)]
    owned = {(x, y) for _, _, box, _ in LABELS for y in range(box[1], box[3]) for x in range(box[0], box[2])}
    if (len(target) != len(before.source) or target[:after.pixels_offset] != before.source[:before.pixels_offset]
            or any(before.indices[y * 256 + x] != after.indices[y * 256 + x]
                   for y in range(256) for x in range(256) if (x, y) not in owned)):
        raise ValueError('Prior labels or unowned frame artwork/header/palette changed')
    a, b = [IlnkContainer.parse(raw) for raw in (prior.read_file(ARCHIVE), embedded)]
    if (len(embedded) != len(prior.read_file(ARCHIVE)) or a.blocks[5][:20] != b.blocks[5][:20]
            or any(x != y for i, (x, y) in enumerate(zip(a.blocks, b.blocks, strict=True)) if i != 5)):
        raise ValueError('Archive header/flags/palette/unrelated blocks changed')
    ai, bi = atlas_indices(prior.read_file(ARCHIVE)), atlas_indices(embedded)
    if any(ai[y * 512 + x] != bi[y * 512 + x]
           for y in range(256) for x in range(512) if x < 256 or (x - 256, y) not in owned):
        raise ValueError('Prior embedded labels or unowned pixels changed')
    if b''.join(bi[y * 512 + 256:y * 512 + 512] for y in range(256)) != bytes(after.indices):
        raise ValueError('Embedded English half differs')
    if base.read_file(RESOURCE)[:after.pixels_offset] != target[:after.pixels_offset]:
        raise ValueError('Canonical frame header/palette differs')
    return {'all_ten_prior_labels_and_unowned_pixels_exact': True,
            'headers_palettes_flags_other_blocks_and_extents_exact': True,
            'embedded_right_half_exact_translated_frame_indices': True}


def native():
    _, prior = sources()
    source = prior.read_file('/__arm9__.bin')
    target, embedded = targets()
    batch = json.loads(BATCH.read_text(encoding='utf-8'))
    size = sizing(source, target, 20, 0x02313F60, supplied_table=True)
    size['table_input'] = 'controlled-frame-image-sizing-contract'
    save(NATIVE, {'status': 'pass-twelve-complete-frame-labels-and-two-presets',
                  'source_arm9_sha256': sha(source), 'actual_format': real_format_glyphs(source, target, batch),
                  'preservation': preservation(target, embedded), 'scoped_image_size': size,
                  'source_context': source_context(),
                  'limitations': ['Sizing loaded header/resource/selector are controlled inputs.',
                                  'Embedded exact pixel storage and bank-zero preview do not prove native bank selection/loading.',
                                  'Actual loaders, all live crops/contexts, parent/GPU palette/alpha, controller/gameplay pending.']})
    print('Pass: all twelve complete actual-format native labels and exact prior/artwork preservation.')


def register():
    art = json.loads(ART.read_text(encoding='utf-8'))
    if (not art['visual_review'] or not art['embedded_bank_zero_review']
            or json.loads(NATIVE.read_text(encoding='utf-8'))['status'] != 'pass-twelve-complete-frame-labels-and-two-presets'):
        raise ValueError('Full previews and native evidence required')
    batch = json.loads(BATCH.read_text(encoding='utf-8'))
    for row in batch['records']:
        row['review']['visual'] = True
    save(BATCH, batch)
    registry = load_release_stack()
    profile = copy.deepcopy(registry['profiles']['all-routes-unified-v166'])
    replacements = {OLD_BATCH.as_posix(): BATCH.as_posix(), OLD_SYNC.as_posix(): SYNC.as_posix()}
    profile['batches'] = [replacements.get(p, p) for p in profile['batches']]
    profile['description'] = 'All V166 text/code/stages, with its two frame batches explicitly superseded by expanded canonical v3 batches; 452 total, all ten prior labels exact.'
    profile['note'] = 'Flagship and Fill Evenly added, source misreading corrected against original Help; ten prior labels exact. Other frame labels and live consumers/loading/banks/GPU/input pending; experimental.'
    registry['profiles'][PROFILE] = profile
    save(RELEASE_STACK_PATH, registry)
    print('Registered experimental V167: 450 unchanged batches plus two expanded frame batches.')


def verify():
    base, prior = sources()
    reproduction = json.loads(Path('work/analysis/v166_spacing_builder_reproduction.json').read_text(encoding='utf-8'))
    if (reproduction['status'] != 'pass-byte-identical-v166-reproduction'
            or reproduction['candidate_sha256'] != PRIOR_SHA
            or reproduction['builder_sha256'] != sha(Path('scripts/build_integrated_release.py').read_bytes())):
        raise ValueError('Fresh byte-identical prior ROM reproduction required')
    new = NdsImage.open(CANDIDATE)
    manifest = json.loads(CANDIDATE.with_suffix('.manifest.json').read_text(encoding='utf-8'))
    old = json.loads(PRIOR.with_suffix('.manifest.json').read_text(encoding='utf-8'))
    registry = load_release_stack()
    if (manifest['candidate_sha256'] != sha(CANDIDATE.read_bytes()) or manifest['base_sha256'] != CANONICAL_BASELINE_SHA256
            or manifest['profile'] != PROFILE or manifest['release_stack_sha256'] != sha(RELEASE_STACK_PATH.read_bytes())
            or manifest['batches'] != [str(p) for p in resolve_release_batches(PROFILE, [], registry)]
            or len(manifest['batches']) != 452 or not all(manifest['checks'].values())
            or manifest['required_batches'] != [str(p) for p in accepted_batch_paths(registry)]
            or manifest['relocations'] != old['relocations']):
        raise ValueError('Saved identity/profile/stages differ')
    replacements = {str(OLD_BATCH): str(BATCH), str(OLD_SYNC): str(SYNC)}
    if manifest['batches'] != [replacements.get(p, p) for p in old['batches']]:
        raise ValueError('Prior batches differ beyond explicit frame supersession')
    before, after = rom_files(prior), rom_files(new)
    changed = sorted(p for p in before.keys() | after.keys() if before.get(p) != after.get(p))
    if changed != sorted([RESOURCE, ARCHIVE]):
        raise ValueError('Unexpected prior text/code/graphics changes')
    canonical = rom_files(base)
    canonical_changed = sorted(p for p in canonical.keys() | after.keys() if canonical.get(p) != after.get(p))
    if manifest['changed_paths'] != canonical_changed or canonical_changed != old['changed_paths']:
        raise ValueError('Canonical changed paths differ')
    for path, ids in old['changed_records'].items():
        if path == RESOURCE:
            if manifest['changed_records'][path][:10] != ids or len(manifest['changed_records'][path]) != 12:
                raise ValueError('Prior frame record IDs lost')
        elif manifest['changed_records'][path] != ids:
            raise ValueError('Inherited changed-record sets differ')
    target, embedded = targets()
    if (target, embedded) != tuple(new.read_file(p) for p in (RESOURCE, ARCHIVE)):
        raise ValueError('Saved graphics differ from reviewed batches')
    preservation(target, embedded)
    real_format_glyphs(new.read_file('/__arm9__.bin'), target, json.loads(BATCH.read_text(encoding='utf-8')))
    verify_golden_content(base, new)
    clean = Path('work/clean.nds')
    if sha(clean.read_bytes()) != 'f4f07c975cc293f5b2ba469747693d3dd37f2e6dfc408cf5910adf5e83d9177d':
        raise ValueError('Wrong clean patch base')
    patch, reconstruction = CANDIDATE.with_suffix('.xdelta'), Path('work/analysis/frame_v167_patch_reconstruction.nds')
    make_xdelta(clean, CANDIDATE, patch)
    apply_xdelta(clean, patch, reconstruction)
    if reconstruction.read_bytes() != CANDIDATE.read_bytes():
        raise ValueError('Patch reconstruction differs')
    report = {'status': 'pass-saved-v167-two-preset-buttons-and-complete-inheritance',
              'candidate': str(CANDIDATE), 'candidate_sha256': sha(CANDIDATE.read_bytes()),
              'candidate_arm9_sha256': sha(new.read_file('/__arm9__.bin')),
              'canonical_base': str(BASE), 'canonical_base_sha256': CANONICAL_BASELINE_SHA256,
              'previous_sha256': PRIOR_SHA, 'profile': PROFILE, 'profile_status': 'experimental',
              'batch_count': 452, 'accepted_batches': manifest['required_batches'],
              'explicitly_superseded_batches': replacements, 'registry_sha256': manifest['release_stack_sha256'],
              'builder_sha256': reproduction['builder_sha256'], 'complete_v166_builder_reproduction_exact': True,
              'changed_paths_vs_v166': changed, 'changed_paths_vs_canonical': canonical_changed,
              'all_prior_translations_components_stages_and_records_preserved': True,
              'patch': str(patch), 'patch_bytes': patch.stat().st_size, 'patch_sha256': sha(patch.read_bytes()),
              'clean_patch_base_sha256': sha(clean.read_bytes()), 'patch_reconstruction_exact': True,
              'new_logical_labels': 2, 'physical_live_loading_crops_banks_input_gameplay_verified': False}
    save(Path('work/analysis/frame_v167_saved_proof.json'), report)
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('action', choices=['materialize', 'native', 'register', 'verify'])
    globals()[parser.parse_args().action]()
