"""Source-locked persistent name storage outside native scratch, BSS and heap."""

import json
import struct
from pathlib import Path

from ndspy.code import MainCodeFile

from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage

SOURCE = '33dc6e6ac7ababb513a773647edd6f93cb5c08b19fad2500e7695f95d8629d75'
TARGET = 'bb637907df8e9a4334f29219cd8273ea92731992b2bc4f9852525c68f9fed6af'
BASE, POOL, HEAP_LOW = 0x02000000, 0x02387A20, 0x02388000


def transform(source, allocation, clean_dtcm):
    if sha(source) != SOURCE:
        raise ValueError('Persistent names require the exact complete V147 stack')
    code = MainCodeFile(source, BASE)
    if len(code.sections) != 3 or code.codeSettingsOffs is None:
        raise ValueError('Original native section ownership differs')
    original = [bytes(s.data) for s in code.sections]
    settings = code.codeSettingsOffs
    if (struct.unpack_from('<I', source, settings + 16)[0] != POOL
            or struct.unpack_from('<I', source, 0xE45DC)[0] != POOL):
        raise ValueError('Original BSS/heap boundary differs')
    payload = bytes.fromhex(allocation['payload_hex'])
    if (len(payload) != 1504 or allocation['used_bytes'] != 1480
            or allocation['runtime_base'] != POOL or allocation['heap_low'] != HEAP_LOW
            or any(payload[1480:]) or len(clean_dtcm) != 1632):
        raise ValueError('Complete aligned reserved name section differs')
    fields = set()
    for move in allocation['moves']:
        at = move['field']
        old = bytes.fromhex(move['source_hex'])
        pointer = move['runtime_pointer']
        delta = pointer - POOL
        if (at in fields or len(old) != 4 or source[at:at + 4] != old
                or not 0 <= delta < 1480 or delta % 4
                or payload[delta:].split(b'\0', 1)[0].decode('cp932') != move['text']):
            raise ValueError('Persistent complete name ownership/field differs')
        fields.add(at)
        struct.pack_into('<I', code.sections[0].data, at, pointer)
    if len(fields) != 239:
        raise ValueError('All 239 persistent name references required')
    shop = allocation['shopkeeper']
    if shop['source_span'] != [0x15D088, 0x15D0A0]:
        raise ValueError('Original square-shopkeeper owner span differs')
    at, end = shop['source_span']
    if source[at:end] != bytes.fromhex(shop['source_hex']):
        raise ValueError('Original square-shopkeeper Japanese bytes differ')
    code.sections[0].data[at:end] = b'Square Shopkeeper\0'.ljust(24, b'\0')
    if len(shop['references']) != 2:
        raise ValueError('Both original shopkeeper references required')
    for ref in shop['references']:
        field = ref['field']
        if field in fields or source[field:field + 4] != bytes.fromhex(ref['source_hex']):
            raise ValueError('Square-shopkeeper reference lock differs')
        struct.pack_into('<I', code.sections[0].data, field, BASE + at)
    if original[2][1540:] != clean_dtcm[1540:]:
        raise ValueError('Existing SDK trailing state differs')
    code.sections[2].data = bytearray(clean_dtcm)
    struct.pack_into('<I', code.sections[0].data, 0xE45DC, HEAP_LOW)
    code.sections.append(MainCodeFile.Section(payload, POOL, 0))
    saved = bytes(code.save())
    loaded = MainCodeFile(saved, BASE)
    if (len(loaded.sections) != 4 or bytes(loaded.sections[1].data) != original[1]
            or bytes(loaded.sections[2].data) != clean_dtcm
            or bytes(loaded.sections[3].data) != payload
            or saved[settings + 12:settings + 20] != source[settings + 12:settings + 20]):
        raise ValueError('Persistent names change native resident/SDK/BSS ownership')
    restored = bytearray(loaded.sections[0].data)
    spans = [(at, end), (0xE45DC, 0xE45E0), (settings, settings + 8)]
    spans += [(field, field + 4) for field in fields]
    spans += [(ref['field'], ref['field'] + 4) for ref in shop['references']]
    for begin, finish in spans:
        restored[begin:finish] = original[0][begin:finish]
    if restored != original[0] or sha(saved) != TARGET:
        raise ValueError('Persistent names change unreviewed bytes or reviewed target identity')
    return saved


def apply_release(source, config_path):
    config = json.loads(Path(config_path).read_text(encoding='utf-8'))
    if (config.get('format') != 'dk4-persistent-name-release-v1'
            or config['source_arm9_sha256'] != SOURCE or config['target_arm9_sha256'] != TARGET):
        raise ValueError('Persistent-name release identity differs')
    required = {config['allocation'], config['native_review'], *config['manuscripts']}
    if set(config['dependencies']) != required:
        raise ValueError('All persistent-name review dependencies required')
    for path, digest in config['dependencies'].items():
        if sha(Path(path).read_bytes()) != digest:
            raise ValueError('Persistent-name source/allocation/native review changed')
    if len(config['manuscripts']) != 2:
        raise ValueError('Both complete shopkeeper manuscripts required')
    row_count = 0
    for path in config['manuscripts']:
        document = json.loads(Path(path).read_text(encoding='utf-8'))
        validate_natural_dialogue_batch(document)
        row_count += len(document['records'])
        if any(r['japanese'] != '広場の店主' or r['english'] != 'Square Shopkeeper{PAD}'
               for r in document['records']):
            raise ValueError('Source-faithful square-shopkeeper prose differs')
    if row_count != 10:
        raise ValueError('All ten source-reviewed shopkeeper names required')
    clean_path = Path('work/clean.nds')
    if sha(clean_path.read_bytes()) != 'f4f07c975cc293f5b2ba469747693d3dd37f2e6dfc408cf5910adf5e83d9177d':
        raise ValueError('Persistent-name clean source changed')
    clean = NdsImage.open(clean_path).read_file('/__arm9__.bin')
    dtcm = bytes(MainCodeFile(clean, BASE).sections[2].data)
    allocation = json.loads(Path(config['allocation']).read_text(encoding='utf-8'))
    review = json.loads(Path(config['native_review']).read_text(encoding='utf-8'))
    if (any(review[key]['research_sha256'] != TARGET
            for key in ('persistent', 'consumers', 'pixels', 'references'))
            or review['references']['status'] != 'pass-direct-reference-ownership-persistent-section'
            or review['pixels']['native_ink_visual_review']['complete_leading_and_final_glyphs'] is not True
            or review['pixels']['native_ink_visual_review']['no_clipping_or_row_overlap'] is not True):
        raise ValueError('Exact target reference and complete native glyph review required')
    if (review['research_sha256'] != TARGET or review['persistent']['scratch_preserves_complete_pool'] is not True
            or review['persistent']['same_machine_sdk_arena_initialization_preserves_names'] is not True
            or len(review['consumers']['native_item_name_getter_cases']) != 218
            or len(review['consumers']['native_item_virtual_caller_cases']) != 436
            or len(review['consumers']['native_static_item_catalogue_cases']) != 218
            or len(review['consumers']['native_ordinary_given_names']) != 207
            or len(review['consumers']['native_map_label_selection_cases']) != 4
            or len(review['pixels']['rasters']) != 20
            or review['pixels']['native_ink_visual_review']['panels_reviewed'] != 10
            or any(not r['independent_pixels_match'] or not r['header_descriptor_and_pixel_guards_preserved']
                   for r in review['pixels']['rasters'])):
        raise ValueError('Full persistent-name native persistence/consumer/pixel evidence required')
    saved = transform(source, allocation, dtcm)
    return saved, {'status': 'pass-reserved-persistent-name-release-gameplay-pending',
                   'arm9_sha256': sha(saved), 'runtime_section': [POOL, HEAP_LOW],
                   'name_references': 239, 'shopkeeper_references': 2,
                   'native_scratch_restored': True, 'itcm_preserved': True,
                   'native_main_heap_reserved': True, 'runtime_verified': False}
