"""Complete the creature introduction bubbles without touching neighboring portrait art."""

import argparse
import copy
import json
import struct
import zlib
from pathlib import Path

from PIL import Image, ImageDraw

from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.graphics.pxl import bgr555
from dk4tool.graphics.raw_bgr555_art import (
    BLOCK_SHA,
    FRAME_BYTES,
    apply_raw_bgr555_art,
    render_region_payload,
)
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.xdelta import apply_xdelta, make_xdelta
from dk4tool.rom.nds import NdsImage
from scripts.build_integrated_release import (
    CANONICAL_BASELINE_SHA256,
    RELEASE_STACK_PATH,
    accepted_batch_paths,
    load_release_stack,
    resolve_release_batches,
    rom_files,
    verify_golden_content,
)
from scripts.chase_comic_v182 import BATCH as OLD
from scripts.closing_gallery_v179 import BASE
from scripts.fleet_row_graphics_v162 import save
from scripts.maria_gallery_v180 import region_bytes

PATH = '/GRP/SLACKIMG.DK4'
PRIOR = Path('out/all_routes_combined_v182_candidate.nds')
PRIOR_SHA = '87513b3f8661413eaa382c22ffd684358301a3128bdbc41319ee66461ac00419'
PROFILE = 'all-routes-unified-v183'
CANDIDATE = Path('out/all_routes_combined_v183_candidate.nds')
BATCH = Path('translations/gallery_creature_raw_art_v5.json')
OUT = Path('work/qa/creature_comic_v183')
REPRO = Path('work/analysis/v182_creature_builder_reproduction.json')
PROOF = Path('work/analysis/creature_comic_v183_saved_proof.json')
SPECS = [
    {'id': 'DK4_GALLERY_CREATURE_QUESTION_V1', 'image_index': 8,
     'box': [239,29,284,89], 'size': 11,
     'protected_source_boxes': [[239,29,243,33], [239,81,245,89], [280,82,284,89]],
     'source_text': '……お前ダレ？', 'english': '...Who are you?',
     'background': 32767, 'ink_word': 0,
     'background_rule': 'neutral-ink-erasure-protect-connected-art-v1',
     'source_meaning': 'A hesitant, blunt question asking who the creature is.',
     'context': 'Right speech bubble after a giant horned sea creature appears during the recruitment comic.',
     'localization_note': 'Natural question retaining the leading hesitation; no unproved speaker name.'},
    {'id': 'DK4_GALLERY_CREATURE_REPLY_V1', 'image_index': 8,
     'box': [43,144,73,209], 'size': 11,
     'source_text': 'うみうし', 'english': 'Sea cow.',
     'background': 32767, 'ink_word': 0,
     'background_rule': 'neutral-ink-erasure-protect-connected-art-v1',
     'source_meaning': 'The creature identifies itself as umiushi, a sea slug; literally sea/cow.',
     'context': 'Creature speech bubble following the runner’s bullfighter declaration and the horned sea-slug reveal.',
     'localization_note': 'Sea cow carries the source cow/bullfighter wordplay into English. It is an explicit comic localization choice, not an official game creature name or a biological claim about manatees.'},
]



def sources():
    if sha(BASE.read_bytes()) != CANONICAL_BASELINE_SHA256 or sha(PRIOR.read_bytes()) != PRIOR_SHA:
        raise ValueError('Exact canonical/V182 required')
    base, prior = [NdsImage.open(p) for p in (BASE, PRIOR)]
    source = base.read_file(PATH)
    block = IlnkContainer.parse(source).blocks[19]
    previous = IlnkContainer.parse(prior.read_file(PATH)).blocks[19]
    if sha(block) != BLOCK_SHA:
        raise ValueError('Exact source artwork required')
    for f in (8,):
        if block[f * FRAME_BYTES:(f + 1) * FRAME_BYTES] != previous[f * FRAME_BYTES:(f + 1) * FRAME_BYTES]:
            raise ValueError('Unchanged original target frame required')
    old_art, _ = apply_raw_bgr555_art(OLD, source)
    if IlnkContainer.parse(old_art).blocks[19] != previous:
        raise ValueError('Earlier raw artwork differs')
    return base, prior, source, block


def authored():
    _, _, _, block = sources()
    old = json.loads(OLD.read_text(encoding='utf-8'))
    records, cases = copy.deepcopy(old['records']), []
    for spec in SPECS:
        f = spec['image_index']
        frame = block[f * FRAME_BYTES:(f + 1) * FRAME_BYTES]
        source = region_bytes(frame, spec['box'])
        row = dict(spec)
        payload, evidence = render_region_payload(row, source, old, block)
        records.append(dict(row, block_index=19, dimensions=[320, 240],
                            source_block_sha256=BLOCK_SHA, source_frame_sha256=sha(frame),
                            source_region_sha256=sha(source), words_sha256=sha(payload),
                            words_zlib_hex=zlib.compress(payload).hex(), speaker='static-comic-caption-credit',
                            review={k: True for k in ('source', 'context', 'localization', 'naturalness', 'formatting')}
                            | {'visual': False, 'physical_gameplay': False}))
        cases.append(dict(evidence, id=spec['id'], image_index=f))
    return records, cases


def preservation(target):
    _, prior, _, _ = sources()
    a, b = [IlnkContainer.parse(r).blocks for r in (prior.read_file(PATH), target)]
    if len(target) != len(prior.read_file(PATH)) or any(x != y for i, (x, y) in enumerate(zip(a, b, strict=True)) if i != 19):
        raise ValueError('Earlier atlas blocks/allocation changed')
    owned = set()
    for row in SPECS:
        x0, y0, x1, y1 = row['box']
        owned.update(row['image_index'] * FRAME_BYTES + (y * 320 + x) * 2 + c
                     for y in range(y0, y1) for x in range(x0, x1) for c in (0, 1))
    if any(x != y for i, (x, y) in enumerate(zip(a[19], b[19], strict=True)) if i not in owned):
        raise ValueError('Unowned scenery/other raw frames changed')
    return {'prior_atlas_syncs_and_other_frames_byte_exact': True,
                'changed_frame_indices': [8], 'unowned_bytes_exact': True,
                'original_hidden_scenery_recovered': False, 'actual_native_display_verified': False}


def materialize():
    _, prior, source, block = sources()
    records, cases = authored()
    batch = json.loads(OLD.read_text(encoding='utf-8'))
    batch['records'] = records
    batch['limits'] = 'Cumulative source-locked raw art. Frame8 has both complete creature-introduction bubbles within original white text planes; portraits/borders unchanged. Sea cow is comic wordplay, not an official species/name claim. Earlier scenery estimates remain approximate; native loading/display/gameplay pending.'
    save(BATCH, batch)
    draft = copy.deepcopy(batch)
    for row in draft['records']:
        row['review']['visual'] = True
    OUT.mkdir(parents=True, exist_ok=True)
    scratch = OUT / 'reviewed-format-draft.json'
    save(scratch, draft)
    result, _ = apply_raw_bgr555_art(scratch, source)
    combined = IlnkContainer.parse(prior.read_file(PATH))
    combined.blocks[19] = IlnkContainer.parse(result).blocks[19]
    evidence = preservation(combined.to_bytes())
    canvas = Image.new('RGB', (1296, 518), '#303030')
    draw = ImageDraw.Draw(canvas)
    for row, f in enumerate((8,)):
        for col, raw in enumerate((block, combined.blocks[19])):
            frame = raw[f * FRAME_BYTES:(f + 1) * FRAME_BYTES]
            raster = Image.new('RGB', (320, 240))
            raster.putdata([bgr555(v)[:3] for v, in struct.iter_unpack('<H', frame)])
            raster.save(OUT / (f'original_{f}.png' if col == 0 else f'english_{f}.png'))
            draw.text((col * 648 + 8, row * 518 + 6),
                      f'Frame {f}: ' + ('Original' if col == 0 else 'English; original portraits/borders exact; native pending'), fill='white')
            canvas.paste(raster.resize((640, 480), Image.Resampling.NEAREST), (col * 648 + 4, row * 518 + 28))
    canvas.save(OUT / 'review.png')
    masks = Image.new('RGB', (648, 518), '#303030')
    mask_draw = ImageDraw.Draw(masks)
    for col, f in enumerate((8,)):
        raster = Image.open(OUT / f'original_{f}.png').convert('RGB')
        for spec, case in zip(SPECS, cases, strict=True):
            if spec['image_index'] != f:
                continue
            x0, y0, x1, y1 = spec['box']
            for y in range(y0, y1):
                for x in range(x0, x1):
                    if not any(b[0] <= x < b[2] and b[1] <= y < b[3]
                               for b in spec.get('protected_source_boxes', [])):
                        raster.putpixel((x, y), (64, 160, 255))
        mask_draw.text((col * 648 + 8, 6), f'Frame {f}: blue = text planes; protected corners excluded', fill='white')
        masks.paste(raster.resize((640, 480), Image.Resampling.NEAREST), (col * 648 + 4, 28))
    masks.save(OUT / 'owned_text_planes.png')
    save(OUT / 'evidence.json', dict(evidence, cases=cases, visual_review=False))
    print('Prepared complete creature introduction; inspect lettering and original portrait/bubble borders.')


def register():
    if json.loads((OUT / 'evidence.json').read_text(encoding='utf-8'))['visual_review'] is not True:
        raise ValueError('Complete source/candidate/restoration review required')
    batch = json.loads(BATCH.read_text(encoding='utf-8'))
    old = json.loads(OLD.read_text(encoding='utf-8'))
    if batch['records'][:11] != old['records']:
        raise ValueError('Earlier eleven raw records changed')
    for row in batch['records']:
        row['review']['visual'] = True
    save(BATCH, batch)
    stack = load_release_stack()
    profile = copy.deepcopy(stack['profiles']['all-routes-unified-v182'])
    if profile['batches'].count(OLD.as_posix()) != 1:
        raise ValueError('Expected one cumulative raw batch')
    profile['batches'] = [BATCH.as_posix() if p == OLD.as_posix() else p for p in profile['batches']]
    profile.update(description='All 463 V182 batches/stages inherited; cumulative raw v5 adds both creature introduction bubbles.',
                   note='Frame8 only: both complete bubble phrases. Comic sea cow wordplay documented; original portraits/borders and earlier layers exact. Native/gameplay pending; experimental.')
    stack['profiles'][PROFILE] = profile
    save(RELEASE_STACK_PATH, stack)


def verify():
    base, prior, source, _ = sources()
    new = NdsImage.open(CANDIDATE)
    manifest = json.loads(CANDIDATE.with_suffix('.manifest.json').read_text(encoding='utf-8'))
    old = json.loads(PRIOR.with_suffix('.manifest.json').read_text(encoding='utf-8'))
    repro = json.loads(REPRO.read_text(encoding='utf-8'))
    stack = load_release_stack()
    expected_batches = [str(BATCH) if Path(p) == OLD else p for p in old['batches']]
    if (manifest['candidate_sha256'] != sha(CANDIDATE.read_bytes()) or manifest['base_sha256'] != CANONICAL_BASELINE_SHA256
            or manifest['profile'] != PROFILE or manifest['release_stack_sha256'] != sha(RELEASE_STACK_PATH.read_bytes())
            or manifest['batches'] != expected_batches or len(expected_batches) != 463
            or manifest['batches'] != [str(p) for p in resolve_release_batches(PROFILE, [], stack)]
            or manifest['required_batches'] != [str(p) for p in accepted_batch_paths(stack)]
            or manifest['relocations'] != old['relocations'] or not all(manifest['checks'].values())
            or repro['reproduction_sha256'] != PRIOR_SHA or sha(Path(repro['reproduction']).read_bytes()) != PRIOR_SHA):
        raise ValueError('Saved identity/full stack/reproduction differs')
    for key, path in [('builder_sha256', 'scripts/build_integrated_release.py'),
                      ('raw_art_module_sha256', 'dk4tool/graphics/raw_bgr555_art.py'),
                      ('caption_module_sha256', 'dk4tool/graphics/raw_caption_restore.py'),
                      ('chase_module_sha256', 'dk4tool/graphics/raw_chase_restore.py')]:
        if repro[key] != sha(Path(path).read_bytes()):
            raise ValueError('Reproduction code dependency changed')
    a, b = [rom_files(r) for r in (prior, new)]
    if sorted(p for p in a.keys() | b.keys() if a.get(p) != b.get(p)) != [PATH] or manifest['changed_paths'] != old['changed_paths']:
        raise ValueError('Unexpected file delta')
    expected, ids = apply_raw_bgr555_art(BATCH, source)
    if IlnkContainer.parse(new.read_file(PATH)).blocks[19] != IlnkContainer.parse(expected).blocks[19]:
        raise ValueError('Saved complete English artwork differs')
    for path, previous_ids in old['changed_records'].items():
        if manifest['changed_records'][path][:len(previous_ids)] != previous_ids:
            raise ValueError('Earlier record IDs lost')
    if manifest['changed_records'][PATH] != old['changed_records'][PATH] + ids[11:]:
        raise ValueError('New record IDs differ')
    evidence = preservation(new.read_file(PATH))
    verify_golden_content(base, new)
    clean = Path('work/clean.nds')
    if sha(clean.read_bytes()) != 'f4f07c975cc293f5b2ba469747693d3dd37f2e6dfc408cf5910adf5e83d9177d':
        raise ValueError('Wrong clean patch base')
    patch = CANDIDATE.with_suffix('.xdelta')
    reconstruction = Path('work/analysis/creature_v183_patch_reconstruction.nds')
    make_xdelta(clean, CANDIDATE, patch)
    apply_xdelta(clean, patch, reconstruction)
    if reconstruction.read_bytes() != CANDIDATE.read_bytes():
        raise ValueError('Patch reconstruction differs')
    save(PROOF, dict(evidence, status='pass-saved-v183-creature-bubbles-and-full-inheritance',
                     candidate=str(CANDIDATE), candidate_sha256=sha(CANDIDATE.read_bytes()), canonical_base_sha256=CANONICAL_BASELINE_SHA256,
                     previous_sha256=PRIOR_SHA, profile=PROFILE, batch_count=463, profile_status='experimental',
                     candidate_arm9_sha256=sha(new.read_file('/__arm9__.bin')), registry_sha256=manifest['release_stack_sha256'],
                     builder_sha256=repro['builder_sha256'], raw_art_module_sha256=repro['raw_art_module_sha256'],
                     caption_module_sha256=repro['caption_module_sha256'], chase_module_sha256=repro['chase_module_sha256'],
                     changed_paths_vs_v182=[PATH], changed_paths_vs_canonical=manifest['changed_paths'],
                     superseded_batch=str(OLD), replacement_batch=str(BATCH),
                     patch=str(patch), patch_bytes=patch.stat().st_size, patch_sha256=sha(patch.read_bytes()),
                     clean_patch_base_sha256=sha(clean.read_bytes()), patch_reconstruction_exact=True))
    print('Saved V183 complete creature introduction, prior inheritance and exact patch.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('action', choices=['materialize', 'register', 'verify'])
    globals()[parser.parse_args().action]()
