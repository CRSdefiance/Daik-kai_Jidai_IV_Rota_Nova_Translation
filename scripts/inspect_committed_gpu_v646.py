"""Read the pinned core's committed render lists using source-bound SF anchors.

This reads the calling process's exact-hash core image and its source-declared
allocated render arrays. It neither loads state nor changes emulator memory.
Pending-list serialization remains a separate export. Heap ranges are checked
with VirtualQuery before copying; source anchors always remain in the DLL image.
"""

import ctypes as ct
import struct
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import save

CORE_SHA = '42160dbfef89adfb3cfd975070a3047d8ad0979cead55607ebdfd3b931046c2b'
CORE = Path('work/emulation_v193/desmume_libretro.dll')
SOURCE = Path('work/analysis/ending_gpu_state_v630/desmume-95b4d79/desmume/src')
STATE_SIZE, POLY_SIZE, VERT_SIZE = 304, 40, 64
IMAGES = {}
STATE_MEMBERS = {'SET': 4, 'SEA': 8, 'SEB': 12, 'SEX': 16, 'SEE': 20,
    'SEC': 24, 'SEF': 28, 'SEO': 32, 'SSH': 36, 'SWB': 40, 'SSM': 44,
    'SAR': 48, 'SAF': 52, 'SPF': 56, 'SCD': 60, 'SCC': 64, 'SFC': 68,
    'SFO': 84, 'FSH': 88, 'ST4': 94, 'SSU': 158}


class ImageReader:
    def __init__(self, core):
        self.raw = CORE.read_bytes()
        assert sha(self.raw) == CORE_SHA and ct.sizeof(ct.c_void_p) == 8
        pe = struct.unpack_from('<I', self.raw, 60)[0]
        assert self.raw[:2] == b'MZ' and self.raw[pe:pe + 4] == b'PE\0\0'
        count, optional = struct.unpack_from('<H', self.raw, pe + 6)[0], pe + 24
        assert struct.unpack_from('<H', self.raw, optional)[0] == 0x20B
        opt_size = struct.unpack_from('<H', self.raw, pe + 20)[0]
        self.link_base = struct.unpack_from('<Q', self.raw, optional + 24)[0]
        self.runtime_base = core._handle
        self.sections = []
        for i in range(count):
            at = optional + opt_size + i * 40
            vsize, rva, fsize, start = struct.unpack_from('<4I', self.raw, at + 8)
            flags = struct.unpack_from('<I', self.raw, at + 36)[0]
            self.sections.append((rva, max(vsize, fsize), start, fsize, flags))
        self.entries = {}

    def source_va(self, offset):
        for rva, size, start, fsize, flags in self.sections:
            if start <= offset < start + fsize:
                return self.link_base + rva + offset - start
        raise ValueError('No source PE section for offset')

    def anchor(self, key, size, count):
        if key in self.entries:
            entry = self.entries[key]
            assert (entry['size'], entry['count']) == (size, count)
            actual = struct.unpack('<QIIQ', self.read(entry['runtime_record_address'], 24))
            assert actual == (entry['runtime_description_address'], size, count, entry['runtime_address'])
            return entry['runtime_address']
        needle, matches, at = key.encode('ascii') + b'\0', [], 0
        while (found := self.raw.find(needle, at)) >= 0:
            at = found + 1
            pointer = struct.pack('<Q', self.source_va(found))
            pos = 0
            while (record := self.raw.find(pointer, pos)) >= 0:
                pos = record + 1
                if record + 24 > len(self.raw):
                    continue
                desc, sz, number, value = struct.unpack_from('<QIIQ', self.raw, record)
                assert desc == self.source_va(found)
                if (sz, number) == (size, count):
                    matches.append((record, value))
        if len(matches) != 1:
            raise ValueError(f'Unique source SFORMAT anchor failed: {key}/{size}/{count}')
        record, value = matches[0]
        address = self.runtime_base + value - self.link_base
        self.entries[key] = {'record_file_offset': record, 'source_VA': value,
            'runtime_record_address': self.runtime_base + self.source_va(record) - self.link_base,
            'runtime_description_address': self.runtime_base + struct.unpack_from('<Q', self.raw, record)[0] - self.link_base,
            'runtime_address': address, 'size': size, 'count': count}
        return self.anchor(key, size, count)

    def read(self, address, size):
        rva = address - self.runtime_base
        if not any(start <= rva and rva + size <= start + extent and flags & 0x40000000
                   for start, extent, _offset, _fsize, flags in self.sections):
            raise ValueError('Native read escapes a readable pinned-core image section')
        return ct.string_at(address, size)

    def qword(self, address):
        return struct.unpack('<Q', self.read(address, 8))[0]


def allocated_read(address, size, base, limit):
    """Copy only a source-pointer-derived, bounded, committed readable allocation."""
    if not (0x10000 <= base <= address and address + size <= base + limit and limit <= 5120000):
        raise ValueError('Render-array read escapes source-declared bounded allocation')

    class MemoryInfo(ct.Structure):
        _fields_ = [('base', ct.c_void_p), ('allocation', ct.c_void_p), ('allocation_protect', ct.c_uint32),
                    ('partition', ct.c_uint16), ('region_size', ct.c_size_t), ('state', ct.c_uint32),
                    ('protect', ct.c_uint32), ('kind', ct.c_uint32)]

    query = ct.windll.kernel32.VirtualQuery
    query.argtypes, query.restype = [ct.c_void_p, ct.POINTER(MemoryInfo), ct.c_size_t], ct.c_size_t
    assert ct.sizeof(MemoryInfo) == 48
    cursor, end = address, address + size
    while cursor < end:
        info = MemoryInfo()
        if query(cursor, ct.byref(info), ct.sizeof(info)) != ct.sizeof(info):
            raise ValueError('Cannot verify render allocation')
        if info.state != 0x1000 or info.protect & 0x100 or info.protect & 0xFF not in (2, 4, 8, 0x20, 0x40, 0x80):
            raise ValueError('Render allocation is not committed and readable')
        assert info.base <= cursor < info.base + info.region_size
        cursor = min(end, info.base + info.region_size)
    return ct.string_at(address, size)


def export(core, directory, expected_ram):
    if core._handle not in IMAGES:
        IMAGES[core._handle] = ImageReader(core)
    image = IMAGES[core._handle]
    a, b = image.anchor('GSET', 4, 1), image.anchor('gSET', 4, 1)
    assert b - a == STATE_SIZE
    state, committed = a - 4, b - 4
    for prefix, base in (('G', state), ('g', committed)):
        for name, offset in STATE_MEMBERS.items():
            size, count = (1, 1) if name == 'SAR' else (2, 32) if name == 'ST4' else (1, 128) if name == 'SSU' else (4, 4) if name == 'SFC' else (4, 1)
            assert image.anchor(prefix + name, size, count) == base + offset
    vram, io = image.anchor('LCDM', 1, 0xA4000), image.anchor('9REG', 1, 0x2000)
    # GFX3D: two304-byte states, two pointers, INDEXLIST's80000 int entries,
    # clipped count/opaque count/pointer, then size_t vertListCount.
    poly_pointer, vertex_pointer = image.qword(state + 608), image.qword(state + 616)
    vertex_count = image.qword(state + 320648)
    polygon_count = struct.unpack('<Q', allocated_read(poly_pointer + 800000, 8, poly_pointer, 800016))[0]
    assert 0 <= vertex_count <= 80000 and 0 <= polygon_count <= 20000
    snapshot = image.read(state, 624)
    poly_bytes = allocated_read(poly_pointer, polygon_count * POLY_SIZE, poly_pointer, 800016)
    vertex_bytes = allocated_read(vertex_pointer, vertex_count * VERT_SIZE, vertex_pointer, 5120000)
    polygons = []
    for i in range(polygon_count):
        kind, primitive, *words = struct.unpack_from('<2I4H4I2f', poly_bytes, i * POLY_SIZE)
        assert kind in (3, 4) and primitive <= 7
        indices, attributes, tex, palette, viewport = words[:kind], words[4], words[5], words[6], words[7]
        assert all(j < vertex_count for j in indices)
        vertices, colors = [], []
        for j in indices:
            vertices.append(list(struct.unpack_from('<6f', vertex_bytes, j * VERT_SIZE)))
            colors.append(list(vertex_bytes[j * VERT_SIZE + 48:j * VERT_SIZE + 51]))
        polygons.append({'indices': indices, 'attributes': attributes,
            'texture_parameter': tex, 'palette': palette, 'viewport': viewport,
            'vertices': vertices, 'vertex_colors_RGB6': colors})
    lcdm, registers = image.read(vram, 0xA4000), image.read(io, 0x2000)
    assert image.read(state, 624) == snapshot
    assert allocated_read(poly_pointer, len(poly_bytes), poly_pointer, 800016) == poly_bytes
    assert allocated_read(vertex_pointer, len(vertex_bytes), vertex_pointer, 5120000) == vertex_bytes
    assert image.read(vram, len(lcdm)) == lcdm and image.read(io, len(registers)) == registers
    assert ct.string_at(core.retro_get_memory_data(2), len(expected_ram)) == expected_ram
    directory = Path(directory)
    files = {}
    for name, data in (('committed_polygons_native.bin', poly_bytes), ('committed_vertices_native.bin', vertex_bytes),
                       ('committed_state_native.bin', snapshot[304:608]), ('source_lcdc_vram.bin', lcdm),
                       ('source_arm9_io.bin', registers)):
        path = directory / name
        path.write_bytes(data)
        files[name] = {'path': str(path), 'bytes': len(data), 'sha256': sha(data)}
    proof = {'read_only_same_process_core_image_export': True,
        'core_DLL_sha256': CORE_SHA, 'source_commit': '95b4d798731caa809125b6c3c11d17cc332ff6ef',
        'source_files': {str(SOURCE / name): sha((SOURCE / name).read_bytes()) for name in
                         ('gfx3d.h', 'gfx3d.cpp', 'saves.h', 'saves.cpp', 'MMU.h', 'GPU.h', 'types.h')},
        'source_SFORMAT_anchors': image.entries, 'source_anchors_inside_readable_core_image_sections': True,
        'render_array_pointers_from_source_GFX3D_layout_bounded_and_VirtualQuery_checked': True,
        'both_state_layouts_all_declared_member_addresses_verified_against_binary_SFORMAT': len(STATE_MEMBERS),
        'committed_render_lists_not_pending_serialization_lists': True,
        'native_polygon_size': POLY_SIZE, 'native_vertex_size': VERT_SIZE,
        'polygon_count': polygon_count, 'vertex_count': vertex_count,
        'polygons': polygons, 'files': files,
        'RAM_geometry_and_source_VRAM_unchanged_by_read_export': True,
        'framebuffer_pixels_not_used_as_source_data': True, 'script_sha256': sha(Path(__file__).read_bytes())}
    path = directory / 'committed_geometry.json'
    save(path, proof)
    return {'path': str(path), 'sha256': sha(path.read_bytes()), **proof}
