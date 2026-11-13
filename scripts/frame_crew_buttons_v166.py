"""Extend canonical frame batches while preserving every V165 translated pixel."""

import argparse
import copy
import json
from pathlib import Path

from PIL import Image, ImageDraw

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
    real_format_glyphs,
)
from scripts.frame_buttons_v165 import BATCH as OLD_BATCH
from scripts.frame_buttons_v165 import SYNC as OLD_SYNC
from scripts.frame_buttons_v165 import targets as old_targets
from scripts.probe_name_treasure_graphics_v161 import sizing

PRIOR = Path('out/all_routes_combined_v165_candidate.nds')
PRIOR_SHA = '2d40853f541e43d023cf708499c142e6bf81e08614ba865812daf3c89f5f98cd'
CANDIDATE = Path('out/all_routes_combined_v166_candidate.nds')
PROFILE = 'all-routes-unified-v166'
BATCH = Path('translations/frame_action_buttons_graphics_v2.json')
SYNC = Path('translations/frame_action_buttons_cmmnimg_sync_v2.json')
OUT = Path('work/qa/frame_buttons_v166')
ART = Path('work/analysis/frame_buttons_v166_artwork.json')
NATIVE = Path('work/analysis/frame_buttons_v166_native.json')
LABELS = [('水夫編成', 'Set Crew', [43, 162, 85, 173], 'Set the sailors assigned to the fleet; crew arrangement.'),
          ('平均化', 'Balance', [43, 178, 85, 189], 'Balance the crew distribution.'),
          ('必要最小', 'Minimum', [139, 162, 181, 173], 'Use the minimum necessary crew allocation.'),
          ('変更終了', 'Done', [139, 194, 181, 205], 'Finish making crew changes.')]


def sources():
    if sha(BASE.read_bytes()) != CANONICAL_BASELINE_SHA256 or sha(PRIOR.read_bytes()) != PRIOR_SHA:
        raise ValueError('Exact canonical and V165 sources required')
    base, prior, clean = [NdsImage.open(p) for p in (BASE, PRIOR, Path('work/clean.nds'))]
    for path in (RESOURCE, ARCHIVE):
        if base.read_file(path) != clean.read_file(path):
            raise ValueError('Exact clean Japanese source required')
    if tuple(prior.read_file(p) for p in (RESOURCE, ARCHIVE)) != old_targets():
        raise ValueError('V165 does not match its reviewed graphics batches')
    return base, prior


def targets():
    base, prior = sources()
    target, _ = apply_pxl_native_label_batch(BATCH, base.read_file(RESOURCE), prior.read_file('/__arm9__.bin'))
    embedded, _ = apply_ilnk_pxl_sync_batch(SYNC, base.read_file(ARCHIVE), target)
    return target, embedded


def materialize():
    base, prior = sources()
    batch = copy.deepcopy(json.loads(OLD_BATCH.read_text(encoding='utf-8')))
    for jp, text, box, meaning in LABELS:
        batch['records'].append({
            'id': 'DK4_FRAME_' + text.upper().replace(' ', '_') + '_GRAPHIC_V2',
            'source_japanese': jp, 'source_meaning': meaning, 'text': text, 'box': box,
            'context': 'Shared Assign Sailors/crew distribution screen buttons.',
            'localization_note': 'Complete natural English action in its crew-screen context; every visible native glyph pixel retained.',
            'background_note': 'Original white faces/dark shadows reconstructed from nearest row colors only within this lettering rectangle; chrome exact.',
            'review': {'source': True, 'context': True, 'localization': True,
                       'naturalness': True, 'formatting': True, 'visual': False,
                       'physical_gameplay': False}})
    batch['supersedes'] = OLD_BATCH.as_posix()
    batch['preserved_record_ids'] = [r['id'] for r in batch['records'][:6]]
    save(BATCH, batch)
    target, _ = apply_pxl_native_label_batch(BATCH, base.read_file(RESOURCE), prior.read_file('/__arm9__.bin'))
    sync = copy.deepcopy(json.loads(OLD_SYNC.read_text(encoding='utf-8')))
    sync['source_image_sha256'] = sha(target)
    sync['supersedes'] = OLD_SYNC.as_posix()
    sync['scope'] = 'Exact canonical matching right half, all six prior labels plus four crew buttons; no unrelated storage changes. Native banks/consumers pending.'
    save(SYNC, sync)
    target, embedded = targets()
    OUT.mkdir(parents=True, exist_ok=True)
    sheet = Image.new('RGB', (1100, 900), '#303030')
    draw = ImageDraw.Draw(sheet)
    for i, (label, raw) in enumerate((('Original Japanese frame', base.read_file(RESOURCE)), ('English frame: V166', target))):
        raster = PxlImage.from_bytes(raw).render().convert('RGB')
        x = 12 + i * 550
        draw.text((x, 8), label, fill='white')
        sheet.paste(raster.resize((512, 512), Image.Resampling.NEAREST), (x, 28))
        draw.text((x, 552), 'Crew buttons', fill='white')
        sheet.paste(raster.crop((38, 158, 186, 210)).resize((518, 182), Image.Resampling.NEAREST), (x, 576))
    sheet.save(OUT / 'review.png')
    embedded_preview(embedded).save(OUT / 'english_embedded_bank_zero.png')
    save(ART, {'status': 'draft-four-new-crew-buttons-six-prior-labels-exact',
               'source_sha256': sha(base.read_file(RESOURCE)), 'target_sha256': sha(target),
               'visual_review': False, 'embedded_bank_zero_review': False,
               'labels_added': [x[1] for x in LABELS], 'prior_labels_preserved': 6,
               'native_palette_bank_and_live_consumers_proved': False})
    print('Materialized four crew buttons in expanded canonical batches; six earlier labels retained.')


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
    return {'all_six_prior_labels_and_unowned_pixels_exact': True,
            'headers_palettes_flags_other_blocks_and_extents_exact': True,
            'embedded_right_half_exact_translated_frame_indices': True}


def native():
    _, prior = sources()
    source = prior.read_file('/__arm9__.bin')
    target, embedded = targets()
    batch = json.loads(BATCH.read_text(encoding='utf-8'))
    size = sizing(source, target, 20, 0x02313F60, supplied_table=True)
    size['table_input'] = 'controlled-frame-image-sizing-contract'
    save(NATIVE, {'status': 'pass-ten-complete-frame-labels-and-four-new-crew-buttons',
                  'source_arm9_sha256': sha(source), 'actual_format': real_format_glyphs(source, target, batch),
                  'preservation': preservation(target, embedded), 'scoped_image_size': size,
                  'limitations': ['Sizing loaded header/resource/selector are controlled inputs.',
                                  'Embedded exact pixel storage and bank-zero preview do not prove native bank selection/loading.',
                                  'Actual loaders, all live crops/contexts, parent/GPU palette/alpha, controller/gameplay pending.']})
    print('Pass: all ten complete actual-format native labels and exact prior/artwork preservation.')


def register():
    art = json.loads(ART.read_text(encoding='utf-8'))
    if (not art['visual_review'] or not art['embedded_bank_zero_review']
            or json.loads(NATIVE.read_text(encoding='utf-8'))['status'] != 'pass-ten-complete-frame-labels-and-four-new-crew-buttons'):
        raise ValueError('Full previews and native evidence required')
    batch = json.loads(BATCH.read_text(encoding='utf-8'))
    for row in batch['records']:
        row['review']['visual'] = True
    save(BATCH, batch)
    registry = load_release_stack()
    profile = copy.deepcopy(registry['profiles']['all-routes-unified-v165'])
    replacements = {OLD_BATCH.as_posix(): BATCH.as_posix(), OLD_SYNC.as_posix(): SYNC.as_posix()}
    profile['batches'] = [replacements.get(p, p) for p in profile['batches']]
    profile['description'] = 'All V165 text/code/stages, with its two frame batches explicitly superseded by expanded canonical v2 batches; 452 total, all six prior labels exact.'
    profile['note'] = 'Four crew buttons added; prior labels exact. Square-sail emphasis/equal supply and live consumers/loading/banks/GPU/input pending; experimental.'
    registry['profiles'][PROFILE] = profile
    save(RELEASE_STACK_PATH, registry)
    print('Registered experimental V166: 450 unchanged batches plus two expanded frame batches.')


def verify():
    base, prior = sources()
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
            if manifest['changed_records'][path][:6] != ids or len(manifest['changed_records'][path]) != 10:
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
    patch, reconstruction = CANDIDATE.with_suffix('.xdelta'), Path('work/analysis/frame_v166_patch_reconstruction.nds')
    make_xdelta(clean, CANDIDATE, patch)
    apply_xdelta(clean, patch, reconstruction)
    if reconstruction.read_bytes() != CANDIDATE.read_bytes():
        raise ValueError('Patch reconstruction differs')
    report = {'status': 'pass-saved-v166-four-crew-buttons-and-complete-inheritance',
              'candidate': str(CANDIDATE), 'candidate_sha256': sha(CANDIDATE.read_bytes()),
              'candidate_arm9_sha256': sha(new.read_file('/__arm9__.bin')),
              'canonical_base': str(BASE), 'canonical_base_sha256': CANONICAL_BASELINE_SHA256,
              'previous_sha256': PRIOR_SHA, 'profile': PROFILE, 'profile_status': 'experimental',
              'batch_count': 452, 'accepted_batches': manifest['required_batches'],
              'explicitly_superseded_batches': replacements, 'registry_sha256': manifest['release_stack_sha256'],
              'changed_paths_vs_v165': changed, 'changed_paths_vs_canonical': canonical_changed,
              'all_prior_translations_components_stages_and_records_preserved': True,
              'patch': str(patch), 'patch_bytes': patch.stat().st_size, 'patch_sha256': sha(patch.read_bytes()),
              'clean_patch_base_sha256': sha(clean.read_bytes()), 'patch_reconstruction_exact': True,
              'new_logical_labels': 4, 'physical_live_loading_crops_banks_input_gameplay_verified': False}
    save(Path('work/analysis/frame_v166_saved_proof.json'), report)
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('action', choices=['materialize', 'native', 'register', 'verify'])
    globals()[parser.parse_args().action]()
