"""Reproduce the standalone ARM946 Thumb formatter with a pinned local compiler."""
import os
from pathlib import Path
import subprocess
import struct

from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import save

ROOT = Path('work/analysis/duel_layout_native_v1133')
TOOLCHAIN = Path('work/analysis/duel_toolchain_v1128')
COMPILER = TOOLCHAIN / 'ziglang/zig.exe'
SOURCE = Path('scripts/duel_layout_native_v1133.c')
LINKER = Path('scripts/duel_layout_native_v1128.ld')


def main():
    assert not ROOT.exists()
    version = subprocess.check_output([str(COMPILER.absolute()), 'version'], text=True).strip()
    assert version == '0.13.0'
    ROOT.mkdir(parents=True)
    environment = {**os.environ,
        'ZIG_GLOBAL_CACHE_DIR': str((TOOLCHAIN / 'global_cache').absolute()),
        'ZIG_LOCAL_CACHE_DIR': str((TOOLCHAIN / 'local_cache').absolute())}
    elf, binary = ROOT / 'formatter.elf', ROOT / 'formatter.bin'
    command = [str(COMPILER.absolute()), 'cc', '-target', 'thumb-freestanding-eabi', '-mcpu=arm946e_s',
        '-Oz', '-ffreestanding', '-fno-builtin', '-fno-lto', '-fno-stack-protector',
        '-fno-unwind-tables', '-fno-asynchronous-unwind-tables', '-ffunction-sections', '-fdata-sections',
        '-nostdlib', '-Wl,-T,' + str(LINKER), '-Wl,--gc-sections', '-Wl,--build-id=none',
        '-Wl,--entry=duel_layout', str(SOURCE), '-o', str(elf)]
    result = subprocess.run(command, env=environment, text=True, capture_output=True)
    (ROOT / 'compiler_stdout.txt').write_text(result.stdout, encoding='utf-8')
    (ROOT / 'compiler_stderr.txt').write_text(result.stderr, encoding='utf-8')
    assert result.returncode == 0, result.stderr
    objcopy = [str(COMPILER.absolute()), 'objcopy', '-O', 'binary', str(elf), str(binary)]
    subprocess.run(objcopy, env=environment, check=True, text=True, capture_output=True)
    raw = elf.read_bytes()
    assert raw[:7] == b'\x7fELF\x01\x01\x01' and struct.unpack_from('<H', raw, 18)[0] == 40
    entry = struct.unpack_from('<I', raw, 24)[0]
    assert entry == 0x02470001 and len(binary.read_bytes()) > 0
    save(ROOT / 'compiler_provenance.json', {
        'compiler': str(COMPILER), 'compiler_version': version, 'compiler_sha256': sha(COMPILER.read_bytes()),
        'distribution':'ziglang==0.13.0 pinned project-local binary wheel',
        'source': str(SOURCE), 'source_sha256': sha(SOURCE.read_bytes()),
        'linker_script': str(LINKER), 'linker_sha256': sha(LINKER.read_bytes()),
        'compile_command': command, 'objcopy_command': objcopy, 'entry': entry,
        'ELF': str(elf), 'ELF_sha256': sha(raw), 'binary': str(binary),
        'binary_sha256': sha(binary.read_bytes()), 'binary_bytes': binary.stat().st_size,
        'no_standard_library_heap_global_mutable_state_or_added_ROM_section': True,
        'CPU_research_address_not_approved_ROM_storage': 0x02470000,
        'original1024byte_expanded_buffer_contains_workspace_by_static_size_assertion': True,
        'native_execution_font_proofs_scope_and_owned_storage_integration_pending': True,
        'producer_sha256': sha(Path(__file__).read_bytes()), 'full_goal_complete': False})
    print(f'ARM946 Thumb formatter compiled:{binary.stat().st_size} bytes;entry{entry:#x}. Native execution/storage gates remain open.')


if __name__ == '__main__':
    main()
