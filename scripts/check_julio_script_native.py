"""Verify the new native catalogue miss, all archive loads and two changed entries."""
import argparse
import struct
from pathlib import Path

from unicorn.arm_const import UC_ARM_REG_LR, UC_ARM_REG_PC, UC_ARM_REG_R1, UC_ARM_REG_SP

from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.confirmed_name_message_catalog import CALLS, MACRO
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.main_pool_cache_visibility import BASE
from dk4tool.patch.reviewed_name_catalog import ROUTE
from dk4tool.rom.nds import NdsImage
from scripts import trace_event_script_sources_v727 as loader
from scripts import verify_script_handoff_v732 as parent
from scripts.audit_story_glyph_consistency import load, save
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.verify_ordinary_name_fidelity_research import initialized


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    assert not args.out.exists()
    source_path = Path('work/analysis/Julio_script_correction_20261101/reconstruction.json')
    source = load(source_path)
    image = NdsImage.open(source['full_research_ROM'])
    assert sha(Path(source['full_research_ROM']).read_bytes()) == source['full_research_ROM_sha256']
    arm = image.read_file('/__arm9__.bin')
    stored = bytes.fromhex(next(r['stored_hex'] for r in source['block_proof']['text_records'] if r['id'] == source['changed_ID']))
    cpu = initialized(arm)
    instruction = struct.unpack_from('<I', arm, CALLS[0])[0]
    assert instruction >> 24 == 0xEB
    delta = (instruction & 0xFFFFFF) << 2
    if delta & 0x2000000:
        delta -= 0x4000000
    entry = BASE + CALLS[0] + 8 + delta
    cases = []
    for form, raw in [('whole', stored), ('body', stored[1:])]:
        for phase in range(4):
            pointer = 0x02468020 + phase
            cpu.mem_write(pointer - 16, b'\xa5' * (len(raw) + 33))
            cpu.mem_write(pointer, raw + b'\0')
            before = bytes(cpu.mem_read(pointer - 16, len(raw) + 33))
            cpu.mem_write(ROUTE, struct.pack('<I', 0))
            cpu.reg_write(UC_ARM_REG_R1, pointer)
            cpu.reg_write(UC_ARM_REG_LR, BASE + CALLS[0] + 4)
            cpu.reg_write(UC_ARM_REG_SP, 0x027F0000)
            cpu.emu_start(entry, MACRO, count=1000000)
            assert cpu.reg_read(UC_ARM_REG_PC) == MACRO and cpu.reg_read(UC_ARM_REG_R1) == pointer
            assert bytes(cpu.mem_read(pointer - 16, len(raw) + 33)) == before
            cases.append(dict(form=form, alignment=phase, original_macro_input_unchanged=True,
                              old_wide_glyph_catalogue_not_selected=True))
    previous = load('work/analysis/Hodram_B54_B60_loaders_v8813/325_loads14fresh636reused_parent_modes.json')
    count = len(IlnkContainer.parse(image.read_file('/data/SC0.DK4')).blocks)
    begin, end = struct.unpack_from('<2I', image.read_file('/data/EV0.DK4'), 0x4C)
    expected = (end - begin) // 2
    load_source = checked_text(previous['source_owned_loader_adapter'], {
        'for route in (1,):': 'for route in (0,):', 'loaded == 325': f'loaded == {count}'})
    parent_source = checked_text(previous['source_owned_parent_adapter'], {
        'for route in (1,):': 'for route in (0,):',
        '                    cases.extend(REUSED_PARENT_CASES[index])\n': '',
        'assert len(cases) == 650': 'assert len(cases) == 2',
        '{len(blocks) * 2} original handoffs': '{len(cases)} targeted handoffs'})
    env = {**loader.__dict__, 'EXPECTED_ACTIONS': expected}
    exec(compile(load_source, __file__ + '::source-route0-loader', 'exec'), env)
    penv = {**parent.__dict__, 'CHANGED_BLOCKS': {43}}
    exec(compile(parent_source, __file__ + '::two-source-route0-parent-modes', 'exec'), penv)
    args.out.mkdir(parents=True)
    loaded = env['run'](image, 'Julio-script-research')
    modes = penv['run'](image, 'Julio-script-research', loaded)
    save(args.out / 'native_loads.json', loaded)
    save(args.out / 'native_parent_modes.json', modes)
    assert len(modes['native_handoff_and_first_read_cases']) == 2
    save(args.out / 'verification.json', dict(source=str(source_path), source_sha256=sha(source_path.read_bytes()),
        research_ROM=source['full_research_ROM'], research_ROM_sha256=source['full_research_ROM_sha256'],
        new_record_catalogue_miss_cases=cases, unchanged_ARM9_andcatalogue=True,
        native_whole_loads_andcache_hits=count, original_EV0_actions=expected, changed_parent_cases=2,
        source_owned_loader_adapter=load_source, source_owned_parent_adapter=parent_source,
        actual_FI_substitution_verified_separately=True, no_natural_event_activation_claim=True,
        producer_sha256=sha(Path(__file__).read_bytes()), new_credit=0))
    print('Eight native catalogue misses;', count, 'whole loads;two changed parent modes pass.')


if __name__ == '__main__':
    main()
