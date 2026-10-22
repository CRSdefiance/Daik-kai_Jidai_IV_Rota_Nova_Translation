"""Read-only export of the pinned core's GPU matrices and serialized geometry.

The state is inspected, never loaded. Keep the older CPU/TCM exporter unchanged.
"""

import ctypes as ct
import struct
import zlib
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from scripts.inspect_desmume_state_v249 import parse
from scripts.verify_village_wrap_v608 import save


def chunks(raw):
    # Reuse the existing complete header/chunk and selected CPU/MMU field guards.
    fields, bounded = parse(raw)
    size, compressed = struct.unpack_from('<2I', raw, 24)
    body = raw[32:size] if compressed == 0xFFFFFFFF else zlib.decompress(raw[32:32 + compressed])
    result, position = {}, 0
    while True:
        kind = struct.unpack_from('<I', body, position)[0]
        position += 4
        if kind == 0xFFFFFFFF:
            assert position == len(body)
            break
        length = struct.unpack_from('<I', body, position)[0]
        position += 4
        result[kind] = body[position:position + length]
        position += length
    assert 90 in result and 91 in result
    return result, fields, bounded


def tags(raw):
    result, position = {}, 0
    while position < len(raw):
        if position + 12 > len(raw):
            raise ValueError('Truncated GPU tagged field')
        name = raw[position:position + 4].decode('ascii')
        item, count = struct.unpack_from('<2I', raw, position + 4)
        position += 12
        size = item * count
        if name in result or position + size > len(raw):
            raise ValueError('Invalid GPU tagged field extent or duplicate')
        result[name] = raw[position:position + size]
        position += size
    return result


def export(core, directory, expected_ram):
    core.retro_serialize_size.argtypes = []
    core.retro_serialize_size.restype = ct.c_size_t
    size = core.retro_serialize_size()
    if not 0 < size <= 32 * 1024 * 1024:
        raise ValueError('Unexpected pinned core serialized-state allocation')
    data = (ct.c_ubyte * size)()
    core.retro_serialize.argtypes = [ct.c_void_p, ct.c_size_t]
    core.retro_serialize.restype = ct.c_bool
    if not core.retro_serialize(data, size):
        raise ValueError('GPU read-only state export failed')
    raw = bytes(data)
    parts, fields, bounded = chunks(raw)
    if fields[4]['WRAM'] != expected_ram:
        raise ValueError('GPU state main RAM differs from same-frame direct export')
    if ct.string_at(core.retro_get_memory_data(2), len(expected_ram)) != expected_ram:
        raise ValueError('GPU export changed main RAM')
    gpu = tags(parts[90])
    assert len(gpu['GMCU']) == 256 and len(gpu['G3CX']) == 256 * 192 * 4
    directory = Path(directory)
    directory.mkdir(parents=True, exist_ok=True)
    files = {}
    for name, value in (('gpu_tagged_chunk90.bin', parts[90]), ('gpu_geometry_chunk91.bin', parts[91]),
                        ('arm9_main_ram.bin', expected_ram), ('gpu_framebuffer_RGBA8888.bin', gpu['G3CX']),
                        ('gpu_current_matrices_FX12.bin', gpu['GMCU'])):
        path = directory / name
        path.write_bytes(value)
        files[name] = {'path': str(path), 'bytes': len(value), 'sha256': sha(value)}
    matrices = struct.unpack('<64i', gpu['GMCU'])
    proof = {**bounded, 'read_only_export': True, 'state_loaded': False,
             'main_RAM_unchanged_by_export': True, 'main_RAM_sha256': sha(expected_ram),
             'serialized_state_sha256': sha(raw), 'files': files,
             'GPU_tagged_field_extents': {k: len(v) for k, v in gpu.items()},
             'current_matrices_FX12_by_mode': [list(matrices[i:i + 16]) for i in range(0, 64, 16)],
             'geometry_chunk_version': struct.unpack_from('<I', parts[91])[0],
             'geometry_chunk_not_yet_interpreted': True,
             'source_commit': '95b4d798731caa809125b6c3c11d17cc332ff6ef',
             'script_sha256': sha(Path(__file__).read_bytes())}
    path = directory / 'gpu_state.json'
    save(path, proof)
    return {'path': str(path), 'sha256': sha(path.read_bytes()), **proof}
