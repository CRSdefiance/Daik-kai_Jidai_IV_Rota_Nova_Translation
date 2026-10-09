"""Complete standard gender icons in loose and embedded marker copies."""
import argparse
import copy
import json
import zlib
from pathlib import Path

from PIL import Image, ImageDraw

from dk4tool.dialogue.font_audit import REFERENCE_ASCII_FONT_SHA256
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.graphics.compact_font import GENDER_FONT_FACE, GENDER_FONT_SHA256, GENDER_GLYPHS
from dk4tool.graphics.pxl import PxlImage
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.xdelta import apply_xdelta, make_xdelta
from dk4tool.rom.nds import NdsImage
from scripts.build_integrated_release import (
    CANONICAL_BASELINE_SHA256,
    RELEASE_STACK_PATH,
    accepted_batch_paths,
    apply_ilnk_pxl_sync_batches,
    apply_pxl_native_label_batch,
    load_release_stack,
    resolve_release_batches,
    rom_files,
    verify_golden_content,
)
from scripts.fleet_row_graphics_v162 import save
from scripts.frame_buttons_v165 import ARCHIVE, BASE, atlas_indices, embedded_preview
from scripts.frame_date_units_v171 import SYNC as FRAME_SYNC
from scripts.marker_cmmnimg_v172 import FRAME, MARKER
from scripts.marker_cmmnimg_v172 import SYNC as OLD_SYNC

PRIOR = Path('out/all_routes_combined_v172_candidate.nds')
PRIOR_SHA = '051ffe4725434a9dcff1d1d1b34be72c81fc8d1d8cde76d7d59bac92ce0fdc92'
CANDIDATE = Path('out/all_routes_combined_v173_candidate.nds')
PROFILE = 'all-routes-unified-v173'
BATCH = Path('translations/marker_gender_graphics_v1.json')
SYNC = Path('translations/marker_cmmnimg_sync_v2.json')
REPRO = Path('work/analysis/v172_gender_face_reproduction.nds')
OUT = Path('work/qa/marker_gender_v173')
PROOF = Path('work/analysis/marker_gender_v173_saved_proof.json')
LABELS = [('男', '♂', [235, 98, 246, 109], 'Male'),
          ('女', '♀', [243, 114, 254, 124], 'Female')]


def sources():
    if sha(BASE.read_bytes()) != CANONICAL_BASELINE_SHA256 or sha(PRIOR.read_bytes()) != PRIOR_SHA:
        raise ValueError('Exact canonical and V172 required')
    base, prior = NdsImage.open(BASE), NdsImage.open(PRIOR)
    if base.read_file(MARKER) != prior.read_file(MARKER):
        raise ValueError('Accepted marker source changed')
    p = PxlImage.from_bytes(base.read_file(MARKER))
    for _, _, (x0, y0, x1, y1), _ in LABELS:
        indices = {p.indices[y * 256 + x] for y in range(y0, y1) for x in range(x0, x1)}
        if not indices <= {1, 9, 11, 15} or not {1, 15} <= indices:
            raise ValueError('Original lettering/background ownership differs')
    a = atlas_indices(prior.read_file(ARCHIVE))
    if b''.join(a[y*512:y*512+256] for y in range(256)) != bytes(p.indices):
        raise ValueError('Prior embedded marker indices differ')
    return base, prior


def targets():
    base, prior = sources()
    marker, ids = apply_pxl_native_label_batch(BATCH, base.read_file(MARKER), prior.read_file('/__arm9__.bin'))
    embedded, sync_ids = apply_ilnk_pxl_sync_batches([FRAME_SYNC, SYNC], base.read_file(ARCHIVE),
                                                  {FRAME: prior.read_file(FRAME), MARKER: marker})
    return marker, embedded, ids, sync_ids


def preservation(marker, embedded):
    base, prior = sources()
    old, new = PxlImage.from_bytes(base.read_file(MARKER)), PxlImage.from_bytes(marker)
    if (len(marker) != len(old.source) or marker[:new.pixels_offset] != old.source[:old.pixels_offset]
            or (new.width, new.height, new.bits_per_pixel) != (256, 256, 4)):
        raise ValueError('Marker header/palette/extent differs')
    expected = bytearray(old.indices)
    cases = []
    for jp, symbol, (x0, y0, x1, y1), meaning in LABELS:
        rows = GENDER_GLYPHS[symbol]
        width = len(rows[0])
        x, y = x0 + (x1-x0-width)//2, y0 + (y1-y0-7)//2
        for gy in range(y0, y1):
            for gx in range(x0, x1):
                expected[gy*256+gx] = 1
        for dy, bits in enumerate(rows):
            for dx, bit in enumerate(bits):
                if bit == '1': expected[(y+dy)*256+x+dx] = 15
        cases.append({'japanese': jp, 'english_symbol': symbol, 'meaning': meaning,
                          'source_owned_box': [x0,y0,x1,y1], 'complete_symbol_origin': [x,y],
                          'complete_symbol_dimensions': [width,7]})
    for offset, wanted in enumerate(expected):
        packed = marker[new.pixels_offset + offset//2]
        actual = (packed >> 4) & 15 if offset & 1 else packed & 15
        if actual != wanted:
            raise ValueError('Independent complete symbol/arrow/cross or unowned marker pixel differs')
    before, after = IlnkContainer.parse(prior.read_file(ARCHIVE)), IlnkContainer.parse(embedded)
    if len(embedded) != len(prior.read_file(ARCHIVE)) or before.blocks[5][:20] != after.blocks[5][:20]:
        raise ValueError('Embedded header/extent differs')
    if any(a != b for i,(a,b) in enumerate(zip(before.blocks,after.blocks,strict=True)) if i != 5):
        raise ValueError('Palette banks or unrelated blocks differ')
    a,b = atlas_indices(prior.read_file(ARCHIVE)), atlas_indices(embedded)
    for y in range(256):
        if a[y*512+256:y*512+512] != b[y*512+256:y*512+512]:
            raise ValueError('All V171 frame pixels must remain exact')
        if b[y*512:y*512+256] != bytes(expected[y*256:y*256+256]):
            raise ValueError('Embedded complete marker copy differs')
    return {'cases': cases, 'independent_raw_packed_nibbles_exact': True,
                'prior_24_marker_captions_and_all_unowned_art_exact': True,
                'prior_22_frame_labels_and_palette_banks_headers_extent_exact': True,
                'changed_marker_pixel_count': sum(a!=b for a,b in zip(old.indices,new.indices,strict=True))}


def materialize():
    base, prior = sources()
    batch = {'format': 'dk4-pxl-native-label-batch-v1', 'file_path': MARKER,
                 'source_file_sha256': sha(base.read_file(MARKER)), 'font_file_path': '/__arm9__.bin',
                 'font_sha256': REFERENCE_ASCII_FONT_SHA256, 'target_locale': 'en-US',
                 'editorial_policy': 'natural-dialogue-v2', 'glyph_width': 5, 'advance': 5,
                 'trim_blank_top_rows': 2, 'color_index': 15, 'erase_palette_indices': [1,9,11,15], 'records': []}
    for jp,symbol,box,meaning in LABELS:
        batch['records'].append({'id': 'DK4_MARKER_'+meaning.upper()+'_SYMBOL_V1',
            'source_japanese': jp, 'source_meaning': meaning, 'text': symbol, 'box': box,
            'font_face': GENDER_FONT_FACE, 'compact_font_sha256': GENDER_FONT_SHA256,
            'background_indices_zlib_hex': zlib.compress(bytes([1])*((box[2]-box[0])*(box[3]-box[1]))).hex(),
            'context': 'Original standalone male/female gender-icon cells beside zodiac symbols.',
            'localization_note': 'Standard gender symbol preserves the meaning of the Japanese icon, complete circle and arrow/cross, without abbreviating or clipping a word. Runtime font unchanged.',
            'review': {'source': True,'context': True,'localization': True,'naturalness': True,'formatting': True,
                        'visual': False,'physical_gameplay': False}})
    save(BATCH,batch)
    marker,_=apply_pxl_native_label_batch(BATCH,base.read_file(MARKER),prior.read_file('/__arm9__.bin'))
    sync=copy.deepcopy(json.loads(OLD_SYNC.read_text(encoding='utf-8')))
    sync.update(source_image_sha256=sha(marker), supersedes=OLD_SYNC.as_posix(),
                scope='Exact accepted marker captions plus standard gender symbols in original cells; preserve right-half frame, all banks/headers/other blocks. Actual consumers/crops/banks unproved.')
    save(SYNC,sync)
    marker,embedded,_,_=targets()
    evidence=preservation(marker,embedded)
    OUT.mkdir(parents=True,exist_ok=True)
    sheet=Image.new('RGB',(1048,900),'#303030');d=ImageDraw.Draw(sheet)
    for i,(title,raw) in enumerate((('Original accepted marker, Japanese gender icons',base.read_file(MARKER)),
                                   ('English-neutral standard gender symbols',marker))):
        x=12+i*520;image=PxlImage.from_bytes(raw).render()
        d.text((x,8),title,fill='white');sheet.paste(image.resize((512,512),Image.Resampling.NEAREST).convert('RGB'),(x,28))
        for j,(_,_,box,meaning) in enumerate(LABELS):
            d.text((x,552+j*152),meaning,fill='white')
            sheet.paste(image.crop(tuple(box)).resize((132,132),Image.Resampling.NEAREST).convert('RGB'),(x,568+j*152))
    sheet.save(OUT/'review.png');embedded_preview(embedded).resize((1024,512),Image.Resampling.NEAREST).save(OUT/'embedded.png')
    arm=prior.read_file('/__arm9__.bin');off=arm.find(b'__marker.pxl')
    evidence.update(visual_review=False, full_marker_visible_japanese_remaining=False,
                    runtime_path_substring_offset=off,
                    scope='Complete storage/glyph checks; actual native loaders/crops/palette banks/GPU/input/gameplay pending.')
    save(OUT/'evidence.json',evidence)
    print(json.dumps(evidence,ensure_ascii=False))


def register():
    if not json.loads((OUT/'evidence.json').read_text())['visual_review']:
        raise ValueError('Review previews first')
    batch = json.loads(BATCH.read_text(encoding='utf-8'))
    for row in batch['records']:
        row['review']['visual'] = True
    save(BATCH, batch)
    registry=load_release_stack();p=copy.deepcopy(registry['profiles']['all-routes-unified-v172'])
    p['batches']=[SYNC.as_posix() if path==OLD_SYNC.as_posix() else path for path in p['batches']]+[BATCH.as_posix()]
    p.update(description='All V172 batches/stages; marker sync explicitly expanded for new complete standard gender icons, 454 batches.',
             note='Male/female symbols in exact original lettering cells. All accepted marker captions and V171 frame labels exact. Loose marker visible Japanese complete; actual consumers/crops/banks/GPU/input pending; experimental.')
    registry['profiles'][PROFILE]=p;save(RELEASE_STACK_PATH,registry)
    print('Registered experimental V173, 454 batches.')


def verify():
    base,prior=sources()
    if REPRO.read_bytes()!=PRIOR.read_bytes(): raise ValueError('Full byte-identical V172 reproduction required')
    rm=json.loads(REPRO.with_suffix('.manifest.json').read_text())
    if rm['release_stack_sha256']!=sha(RELEASE_STACK_PATH.read_bytes()): raise ValueError('Fresh reproduction required')
    new=NdsImage.open(CANDIDATE);m=json.loads(CANDIDATE.with_suffix('.manifest.json').read_text())
    old=json.loads(PRIOR.with_suffix('.manifest.json').read_text());registry=load_release_stack()
    expected_batches=[str(SYNC) if path==str(OLD_SYNC) else path for path in old['batches']]+[str(BATCH)]
    if (m['candidate_sha256']!=sha(CANDIDATE.read_bytes()) or m['base_sha256']!=CANONICAL_BASELINE_SHA256
            or m['profile']!=PROFILE or m['batches']!=expected_batches or len(m['batches'])!=454
            or m['batches']!=[str(p) for p in resolve_release_batches(PROFILE,[],registry)]
            or m['release_stack_sha256']!=sha(RELEASE_STACK_PATH.read_bytes()) or not all(m['checks'].values())
            or m['required_batches']!=[str(p) for p in accepted_batch_paths(registry)] or m['relocations']!=old['relocations']):
        raise ValueError('Saved identity/inheritance differs')
    before,after=rom_files(prior),rom_files(new)
    changed=sorted(p for p in before.keys()|after.keys() if before.get(p)!=after.get(p))
    if changed!=sorted([MARKER,ARCHIVE]) or m['changed_paths']!=sorted(old['changed_paths']+[MARKER]):
        raise ValueError('Unexpected changed paths')
    for path,ids in old['changed_records'].items():
        if m['changed_records'][path]!=ids: raise ValueError('Prior IDs lost')
    marker,embedded,ids,_=targets()
    if ((marker,embedded)!=(new.read_file(MARKER),new.read_file(ARCHIVE)) or m['changed_records'][MARKER]!=ids):
        raise ValueError('Saved artwork differs from review')
    evidence=preservation(marker,embedded);verify_golden_content(base,new)
    clean=Path('work/clean.nds');clean_sha=sha(clean.read_bytes())
    if clean_sha!='f4f07c975cc293f5b2ba469747693d3dd37f2e6dfc408cf5910adf5e83d9177d': raise ValueError('Wrong clean source')
    patch=CANDIDATE.with_suffix('.xdelta');reconstruction=Path('work/analysis/gender_v173_patch_reconstruction.nds')
    make_xdelta(clean,CANDIDATE,patch);apply_xdelta(clean,patch,reconstruction)
    if reconstruction.read_bytes()!=CANDIDATE.read_bytes(): raise ValueError('Patch differs')
    save(PROOF,dict(evidence,status='pass-saved-v173-complete-gender-symbols-and-inheritance',
        candidate=str(CANDIDATE),candidate_sha256=sha(CANDIDATE.read_bytes()),
        canonical_base=str(BASE),canonical_base_sha256=CANONICAL_BASELINE_SHA256,
        previous_sha256=PRIOR_SHA,profile=PROFILE,profile_status='experimental',batch_count=454,
        candidate_arm9_sha256=sha(new.read_file('/__arm9__.bin')), registry_sha256=m['release_stack_sha256'],
        builder_sha256=sha(Path('scripts/build_integrated_release.py').read_bytes()),
        compact_font_module_sha256=sha(Path('dk4tool/graphics/compact_font.py').read_bytes()),
        gender_font_sha256=GENDER_FONT_SHA256, complete_v172_reproduction_exact=True,
        changed_paths_vs_v172=changed,changed_paths_vs_canonical=m['changed_paths'],
        patch=str(patch),patch_bytes=patch.stat().st_size,patch_sha256=sha(patch.read_bytes()),
        clean_patch_base_sha256=clean_sha,patch_reconstruction_exact=True,physical_gameplay_verified=False))
    print(PROOF.read_text())


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('action',choices=['materialize','register','verify'])
    globals()[parser.parse_args().action]()
