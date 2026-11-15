"""Bind clean scenes to current stored and effective catalogue text after clean review."""
import argparse
from copy import deepcopy
import struct
from pathlib import Path

from unicorn.arm_const import UC_ARM_REG_LR, UC_ARM_REG_PC, UC_ARM_REG_R1, UC_ARM_REG_SP

from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.confirmed_name_message_catalog import CALLS, MACRO
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.main_pool_cache_visibility import BASE
from dk4tool.patch.reviewed_name_catalog import ROUTE
from scripts.audit_story_glyph_consistency import load, save
from scripts.inventory_lil_after_crew_items_complete_v3152 import scoped_inventory
from scripts.registered_editorial_runtime import RegisteredRuntime


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--meanings', type=Path, required=True)
    ap.add_argument('--out', type=Path, required=True)
    args = ap.parse_args()
    assert not args.out.exists()
    meanings = load(args.meanings)
    assert meanings['clean_meanings'] == 144 and meanings['earlier_English_dialogue_unconsulted']
    packet = load(meanings['source_packet'])
    assert sha(Path(meanings['source_packet']).read_bytes()) == meanings['source_packet_sha256']
    ctx = RegisteredRuntime('work/analysis/Hodram_Julio_release_verified_20261101/registered_release_verification.json',
                            'work/analysis/Hodram_Julio_release_verified_20261101/own_registered_startup_verification.json')
    route, path = packet['route'], packet['file_path']
    archive = ctx.image.read_file(path)
    bank = IlnkContainer.parse(archive).blocks
    inventory, _, _ = scoped_inventory()
    cpu, _, provider = ctx.machine(ctx.arm, ctx.common, ctx.raw, ctx.plan)
    assert struct.unpack('<I', cpu.mem_read(ROUTE, 4))[0] == route
    instruction = struct.unpack_from('<I', ctx.arm, CALLS[0])[0]
    assert instruction >> 24 == 0xEB
    delta = (instruction & 0xFFFFFF) << 2
    if delta & 0x2000000:
        delta -= 0x4000000
    entry = BASE + CALLS[0] + 8 + delta
    groups = []
    for original, meaning in zip(packet['groups'], meanings['groups'], strict=True):
        number = original['block']
        assert number == meaning['block']
        block = bank[number]
        commands, speeches = inventory(ctx.arm, block)
        assert len(commands) == len(original['all_source_commands']) and len(speeches) == len(meaning['records'])
        command_map = []
        for source, current in zip(original['all_source_commands'], commands, strict=True):
            assert source['word'] == current['word']
            a, b = bytes.fromhex(source['whole_command_hex']), bytes.fromhex(current['whole_command_hex'])
            if source['word'] == 0x4000:
                assert a[:6] == b[:6]
            elif source['word'] in (0x100, 0x200, 0x300, 0x400):
                assert a[:2] == b[:2]
            else:
                assert a == b
            command_map.append(dict(word=source['word'], source_offset=source['offset'],
                                     current_offset=current['offset'], source_hex=a.hex(), current_hex=b.hex()))
        rows = []
        for source, command in zip(meaning['records'], speeches, strict=True):
            at = command['offset'] + 5
            raw = block[at:block.index(0, at + 1)]
            assert raw[0] == source['source_selector'] and block[at - 5:at + 1].hex() == source['source_complete_preamble_hex']
            pointer = 0x02468020
            body = raw[1:]
            cpu.mem_write(pointer - 16, b'\xa5' * (len(body) + 33))
            cpu.mem_write(pointer, body + b'\0')
            before = bytes(cpu.mem_read(pointer - 16, len(body) + 33))
            cpu.reg_write(UC_ARM_REG_R1, pointer)
            cpu.reg_write(UC_ARM_REG_LR, BASE + CALLS[0] + 4)
            cpu.reg_write(UC_ARM_REG_SP, 0x027F0000)
            cpu.emu_start(entry, MACRO, count=1000000)
            assert cpu.reg_read(UC_ARM_REG_PC) == MACRO
            selected = cpu.reg_read(UC_ARM_REG_R1)
            target = bytes(cpu.mem_read(selected, 1024)).split(b'\0')[0]
            assert len(target) < 1024 and bytes(cpu.mem_read(pointer - 16, len(body) + 33)) == before
            r = deepcopy(source)
            r.update(current_hex=raw.hex(), current_reference=dict(file_path=path, block=number,
                offset=at, header_offset=at - 5, record_index=block[:at].count(b'\0'), length=len(raw)),
                current_record_index=block[:at].count(b'\0'),
                current_stored_text=body.decode('cp932'), current_effective_hex=target.hex(),
                current_effective_text=target.decode('cp932'),
                current_comparison_paragraph=' '.join(target.decode('cp932').split()),
                current_catalogue_selected=selected != pointer, selected_native_pointer=selected,
                current_English_now_exposed=True, earlier_English_unconsulted=False)
            rows.append(r)
        groups.append(dict(block=number, file_path=path, clean_block_hex=original['clean_block_hex'],
                           clean_block_sha256=original['clean_block_sha256'],
                           current_block_hex=block.hex(), current_block_sha256=sha(block),
                           all_source_commands=original['all_source_commands'],
                           all_current_commands=commands, command_map=command_map, records=rows))
    assert bytes(cpu.mem_read(ctx.actor_root, 0x1A04)) == ctx.actor_bytes
    ctx.calls.clear()
    args.out.mkdir(parents=True)
    save(args.out / 'current_effective.json', dict(current_ROM=str(ctx.rompath),
        current_ROM_sha256=ctx.release['candidate_sha256'], current_archive_sha256=sha(archive),
        file_path=path, groups=groups, records=sum(len(g['records']) for g in groups),
        clean_meanings=str(args.meanings), clean_meanings_sha256=sha(args.meanings.read_bytes()),
        original_current_catalogue_lookups=144, native_macro_expansion_not_executed_here=True,
        runtime=ctx.receipt(), all_source_preambles_andcommand_kinds_preserved=True,
        new_localized_English_andformatting_approval_pending=True,
        source_owned_inventory_reused_not_new_branch_reachability_proof=True,
        producer_sha256=sha(Path(__file__).read_bytes()), new_credit=0))
    print('144 current stored/effective records bound after complete clean meanings; no new credit.')


if __name__ == '__main__':
    main()
