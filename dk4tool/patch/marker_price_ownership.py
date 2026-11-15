"""Restore the original bag and localize the two actual marker price cells."""
import json
import zlib
from pathlib import Path

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.graphics.pxl import PxlImage
from dk4tool.patch.grand_race_menu_release import sha


def apply_release(candidate, clean, config_path):
    config = json.loads(Path(config_path).read_text(encoding='utf-8'))
    if config['format'] != 'dk4-marker-price-ownership-v1':
        raise ValueError('Unknown marker ownership format')
    path, archive_path = '/_pxl/__marker.pxl', '/GRP/CMMNIMG.DK4'
    before, source, archived = candidate.read_file(path), clean.read_file(path), candidate.read_file(archive_path)
    if (sha(before), sha(source), sha(archived)) != (
            config['source_sha256'], config['clean_sha256'], config['source_archive_sha256']):
        raise ValueError('Marker ownership source lock differs')
    result, original = PxlImage.from_bytes(before), PxlImage.from_bytes(source)
    inherited_indices = bytes(result.indices)
    payload = zlib.decompress(bytes.fromhex(config['indices_zlib_hex']))
    if len(payload) != 33*48 or max(payload) > 15:
        raise ValueError('Marker ownership payload extent or palette differs')
    for y in range(48):
        result.indices[(48+y)*256+112:(48+y)*256+145] = payload[y*33:(y+1)*33]
    output = result.to_bytes()
    if sha(output) != config['target_sha256'] or output[:result.pixels_offset] != source[:original.pixels_offset]:
        raise ValueError('Marker ownership target or original metadata differs')
    font = GameAsciiFont.from_arm9(candidate.read_file('/__arm9__.bin'))
    rows = []
    for top, text in ((48, 'Sell'), (60, 'Buy')):
        left = 112+(32-len(text)*5)//2
        ink = set()
        for n, ch in enumerate(text):
            glyph = font.decode(ch)
            if any(glyph.getpixel((x,y)) for y in range(2) for x in range(6)) or any(glyph.getpixel((5,y)) for y in range(11)):
                raise ValueError('Price glyph trimming would remove original ink')
            ink |= {(left+n*5+x, top+1+y-2) for y in range(2,11) for x in range(5) if glyph.getpixel((x,y))}
        actual = {(x,y) for y in range(top,top+12) for x in range(112,144) if result.indices[y*256+x] == 15}
        if actual != ink:
            raise ValueError('Complete price font mask differs')
        rows.append({'text': text, 'source_box': [112,top,144,top+12], 'complete_original_font_ink': len(ink)})
    if not all(result.indices[y*256+x] == original.indices[y*256+x] for y in range(72,112) for x in range(112,152)):
        raise ValueError('Original bag illustration differs')
    archive = IlnkContainer.parse(archived)
    block = archive.blocks[5]
    packed = bytearray(block[20:])
    for y in range(256):
        for x in range(0,256,2):
            pos = (y*512+x)//2
            old = packed[pos]
            if (old&15,old>>4) != (inherited_indices[y*256+x], inherited_indices[y*256+x+1]):
                raise ValueError('Inherited embedded marker is not synchronized')
            packed[pos] = result.indices[y*256+x] | result.indices[y*256+x+1]<<4
    archive.blocks[5] = block[:20]+bytes(packed)
    archive_output = archive.to_bytes()
    if sha(archive_output) != config['target_archive_sha256'] or len(archive_output) != len(archived):
        raise ValueError('Embedded ownership target or allocation differs')
    return {path:output, archive_path:archive_output}, [
        {'file_path':path, 'changed_records':config['record_ids'], 'source_sha256':sha(before), 'target_sha256':sha(output),
         'price_cells':rows, 'original_bag_40x40_exact':True},
        {'file_path':archive_path, 'changed_records':['DK4_MARKER_PRICE_OWNERSHIP_EMBEDDED'],
         'source_sha256':sha(archived), 'target_sha256':sha(archive_output), 'left_marker_only_synchronized':True}]
