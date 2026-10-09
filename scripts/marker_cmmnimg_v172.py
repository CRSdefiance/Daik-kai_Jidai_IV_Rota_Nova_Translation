"""Synchronize accepted English marker artwork into its exact embedded copy."""
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
    apply_ilnk_pxl_sync_batches,
    load_release_stack,
    resolve_release_batches,
    rom_files,
    verify_golden_content,
)
from scripts.fleet_row_graphics_v162 import save
from scripts.frame_buttons_v165 import ARCHIVE, BASE, atlas_indices, embedded_preview
from scripts.frame_date_units_v171 import SYNC as FRAME_SYNC

MARKER = '/_pxl/__marker.pxl'
FRAME = '/_pxl/__frame.pxl'
PRIOR = Path('out/all_routes_combined_v171_candidate.nds')
PRIOR_SHA = '7a51d00eae25b50c9b914b6e3a26cff6ca7b0940b445f67107f7328c60759888'
CANDIDATE = Path('out/all_routes_combined_v172_candidate.nds')
SYNC = Path('translations/marker_cmmnimg_sync_v1.json')
PROFILE = 'all-routes-unified-v172'
OUT = Path('work/qa/marker_v172')
PROOF = Path('work/analysis/marker_v172_saved_proof.json')
REPRO = Path('work/analysis/v171_region_builder_reproduction.nds')


def sources():
    if sha(BASE.read_bytes()) != CANONICAL_BASELINE_SHA256 or sha(PRIOR.read_bytes()) != PRIOR_SHA:
        raise ValueError('Exact canonical and V171 required')
    base, prior, clean = [NdsImage.open(p) for p in (BASE, PRIOR, Path('work/clean.nds'))]
    indices = atlas_indices(base.read_file(ARCHIVE))
    left = b''.join(indices[y * 512:y * 512 + 256] for y in range(256))
    jp = PxlImage.from_bytes(clean.read_file(MARKER))
    if bytes(jp.indices) != left or base.read_file(MARKER) != prior.read_file(MARKER):
        raise ValueError('Exact Japanese embedded source and unchanged accepted English marker required')
    if base.read_file(ARCHIVE) != clean.read_file(ARCHIVE):
        raise ValueError('Embedded source differs from clean original')
    return base, prior


def targets():
    base, prior = sources()
    return apply_ilnk_pxl_sync_batches([FRAME_SYNC, SYNC], base.read_file(ARCHIVE),
                                     {FRAME: prior.read_file(FRAME), MARKER: base.read_file(MARKER)})


def preservation(target):
    base, prior = sources()
    a, b = IlnkContainer.parse(prior.read_file(ARCHIVE)), IlnkContainer.parse(target)
    if len(target) != len(prior.read_file(ARCHIVE)) or len(a.blocks) != len(b.blocks):
        raise ValueError('Archive extent differs')
    if any(x != y for i, (x, y) in enumerate(zip(a.blocks, b.blocks, strict=True)) if i != 5):
        raise ValueError('Unrelated archive blocks or palette banks differ')
    if a.blocks[5][:20] != b.blocks[5][:20]:
        raise ValueError('Atlas header differs')
    old, new = atlas_indices(prior.read_file(ARCHIVE)), atlas_indices(target)
    marker = PxlImage.from_bytes(base.read_file(MARKER))
    clean = PxlImage.from_bytes(NdsImage.open('work/clean.nds').read_file(MARKER))
    changes = 0
    for y in range(256):
        if old[y * 512 + 256:y * 512 + 512] != new[y * 512 + 256:y * 512 + 512]:
            raise ValueError('V171 right-half frame or leading letters lost')
        for x in range(256):
            i, j = y * 512 + x, y * 256 + x
            if new[i] != marker.indices[j]:
                raise ValueError('Complete accepted marker pixel/first or final letter differs')
            if old[i] != new[i]:
                changes += 1
                if clean.indices[j] == marker.indices[j]:
                    raise ValueError('Unchanged source ornament or gender icon differs')
    if not changes:
        raise ValueError('No translated embedded pixels')
    return {'changed_pixel_count': changes, 'entire_accepted_marker_indices_exact': True,
            'all_v171_frame_indices_exact': True, 'all_palette_banks_headers_other_blocks_extent_exact': True,
            'unchanged_source_ornament_gender_icons_exact': True}


def materialize():
    base, prior = sources()
    batch = copy.deepcopy(json.loads(FRAME_SYNC.read_text(encoding='utf-8')))
    batch.pop('supersedes', None)
    batch.update(source_image_path=MARKER, source_image_sha256=sha(base.read_file(MARKER)),
                 target_x=0, id='DK4_MARKER_CMMNIMG_SYNC_V1',
                 scope='Synchronize the exact original-matching left half with accepted canonical English marker pixels. Preserve all V171 right-half frame pixels and all palette banks/headers/other blocks. Male/female icons remain Japanese. Actual loading/crops/banks/GPU/input unproved.')
    save(SYNC, batch)
    target, ids = targets()
    evidence = preservation(target)
    OUT.mkdir(parents=True, exist_ok=True)
    sheet = Image.new('RGB', (1048, 1080), '#303030')
    draw = ImageDraw.Draw(sheet)
    for y, title, raw in ((0, 'V171: Japanese duplicate on left', prior.read_file(ARCHIVE)),
                          (540, 'V172: accepted English marker + unchanged V171 frame', target)):
        draw.text((12, y + 8), title, fill='white')
        sheet.paste(embedded_preview(raw).resize((1024, 512), Image.Resampling.NEAREST).convert('RGB'), (12, y + 28))
    sheet.save(OUT / 'review.png')
    save(OUT / 'evidence.json', dict(evidence, ids=ids, visual_review=False,
         scope='Bank-zero storage preview only; native palette selection/actual consumers unproved. Existing accepted loose typography reused exactly. No runtime/font edits.'))
    print(json.dumps(evidence))


def register():
    evidence = json.loads((OUT / 'evidence.json').read_text(encoding='utf-8'))
    if not evidence['visual_review']:
        raise ValueError('Review complete preview before registration')
    registry = load_release_stack()
    p = copy.deepcopy(registry['profiles']['all-routes-unified-v171'])
    p['batches'].append(SYNC.as_posix())
    p['description'] = 'All 452 V171 batches/stages exact, plus one canonical marker-to-CMMNIMG left-half synchronization.'
    p['note'] = 'Accepted English marker artwork reused byte-exactly; all V171 frame pixels exact. Gender symbols remain Japanese. Native actual loading/crops/banks/GPU/input pending; experimental.'
    registry['profiles'][PROFILE] = p
    save(RELEASE_STACK_PATH, registry)
    print('Registered experimental V172, 453 batches.')


def verify():
    base, prior = sources()
    if REPRO.read_bytes() != PRIOR.read_bytes():
        raise ValueError('Full byte-identical V171 reproduction required')
    repro_manifest = json.loads(REPRO.with_suffix('.manifest.json').read_text(encoding='utf-8'))
    if (repro_manifest['release_stack_sha256'] != sha(RELEASE_STACK_PATH.read_bytes())
            or repro_manifest['profile'] != 'all-routes-unified-v171'):
        raise ValueError('Fresh V171 reproduction manifest required')
    new = NdsImage.open(CANDIDATE)
    m = json.loads(CANDIDATE.with_suffix('.manifest.json').read_text(encoding='utf-8'))
    old = json.loads(PRIOR.with_suffix('.manifest.json').read_text(encoding='utf-8'))
    registry = load_release_stack()
    if (m['candidate_sha256'] != sha(CANDIDATE.read_bytes()) or m['base_sha256'] != CANONICAL_BASELINE_SHA256
            or m['profile'] != PROFILE or m['release_stack_sha256'] != sha(RELEASE_STACK_PATH.read_bytes())
            or m['batches'] != [str(p) for p in resolve_release_batches(PROFILE, [], registry)]
            or m['batches'] != old['batches'] + [str(SYNC)] or len(m['batches']) != 453
            or m['required_batches'] != [str(p) for p in accepted_batch_paths(registry)]
            or m['relocations'] != old['relocations'] or not all(m['checks'].values())):
        raise ValueError('Saved identity/profile/stages differ')
    before, after = rom_files(prior), rom_files(new)
    changed = sorted(p for p in before.keys() | after.keys() if before.get(p) != after.get(p))
    if changed != [ARCHIVE] or m['changed_paths'] != old['changed_paths']:
        raise ValueError('Unexpected prior/canonical path changes')
    for path, ids in old['changed_records'].items():
        expected = ids + ['DK4_MARKER_CMMNIMG_SYNC_V1'] if path == ARCHIVE else ids
        if m['changed_records'][path] != expected:
            raise ValueError('Earlier record IDs lost')
    expected, _ = targets()
    if expected != new.read_file(ARCHIVE):
        raise ValueError('Saved artwork differs from review')
    evidence = preservation(expected)
    verify_golden_content(base, new)
    clean = Path('work/clean.nds')
    clean_sha = 'f4f07c975cc293f5b2ba469747693d3dd37f2e6dfc408cf5910adf5e83d9177d'
    if sha(clean.read_bytes()) != clean_sha:
        raise ValueError('Wrong clean patch source')
    patch = CANDIDATE.with_suffix('.xdelta')
    reconstruction = Path('work/analysis/marker_v172_patch_reconstruction.nds')
    make_xdelta(clean, CANDIDATE, patch)
    apply_xdelta(clean, patch, reconstruction)
    if reconstruction.read_bytes() != CANDIDATE.read_bytes():
        raise ValueError('Patch reconstruction differs')
    report = dict(evidence, status='pass-saved-v172-marker-sync-and-full-inheritance',
        candidate=str(CANDIDATE), candidate_sha256=sha(CANDIDATE.read_bytes()),
        candidate_arm9_sha256=sha(new.read_file('/__arm9__.bin')),
        canonical_base=str(BASE), canonical_base_sha256=CANONICAL_BASELINE_SHA256,
        previous_sha256=PRIOR_SHA, profile=PROFILE, profile_status='experimental',
        batch_count=453, accepted_batches=m['required_batches'], registry_sha256=m['release_stack_sha256'],
        builder_sha256=sha(Path('scripts/build_integrated_release.py').read_bytes()),
        complete_v171_builder_reproduction_exact=True, changed_paths_vs_v171=changed,
        changed_paths_vs_canonical=m['changed_paths'], all_prior_translations_components_stages_and_records_preserved=True,
        patch=str(patch), patch_bytes=patch.stat().st_size, patch_sha256=sha(patch.read_bytes()),
        clean_patch_base_sha256=clean_sha, patch_reconstruction_exact=True,
        physical_live_loading_crops_banks_input_gameplay_verified=False)
    save(PROOF, report)
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('action', choices=['materialize', 'register', 'verify'])
    globals()[parser.parse_args().action]()
