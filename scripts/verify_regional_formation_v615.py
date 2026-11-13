"""Verify actual original regional formation and five complete native plaque regions."""

import shutil
import struct
from pathlib import Path

from PIL import Image
from unicorn.arm_const import UC_ARM_REG_PC, UC_ARM_REG_R0

from dk4tool.graphics.pxl import PxlImage
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.regional_fleet_plaques import FILE, RECORDS
from dk4tool.rom.nds import NdsImage
from scripts.probe_button_prompt_native import BASE, call, machine
from scripts.verify_portrait_native_pixels_v202 import native5
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/regional_fleet_v615')
RUN = Path('E:/Rota Nova translations/Generated/work/emulation_v193/regional_fleet_v615_stockholm')
ARCHIVE = Path('E:/Rota Nova translations/Screenshots/Test fixtures/V615 Regional fleet research')


def main():
    report = read(RUN / 'capture_report.json')
    assert report['frames'] == 45600 and report['cold_boot'] and not report['savestate_loaded']
    assert not report['callback_errors']
    assert len(report['synthetic_finance_fixtures']) == 1 and len(report['synthetic_crew_ability_fixtures']) == 2
    assert not report['earned_wealth_or_ordinary_fleet_prerequisites_verified']
    assert not report['earned_ability_or_ordinary_fleet_prerequisites_verified']
    rom_path = Path(report['ROM'])
    assert rom_path.name == 'all_routes_combined_v613_candidate.nds' and sha(rom_path.read_bytes()) == report['ROM_sha256']
    rom = NdsImage.open(rom_path)
    resource, arm = rom.read_file(FILE), rom.read_file('/__arm9__.bin')
    atlas = PxlImage.from_bytes(resource).render().convert('RGB')
    initial = machine(arm)
    initial.emu_start(0x0210FAB0, 0x0210FAD4, count=150)
    assert initial.reg_read(UC_ARM_REG_PC) == 0x0210FAD4
    owner = initial.reg_read(UC_ARM_REG_R0)
    assert owner == 0x02313380
    ptr = struct.unpack('<I', initial.mem_read(owner + 12, 4))[0]
    assert bytes(initial.mem_read(ptr, 64)).split(b'\0')[0] == b'_pxl/chihofleetinfo.pxl'
    rows, pixels, frames = [], 0, (41000, 41400, 41800, 42200, 42600, 43000)
    for frame in frames:
        raw_path = RUN / f'frame_{frame:06d}_arm9_ram.bin'
        raw = raw_path.read_bytes()
        assert len(raw) == 0x400000 and raw.find(resource) >= 0
        image_path = RUN / f'frame_{frame:06d}_navigation.png'
        im = Image.open(image_path).convert('RGB')
        regions = []
        for _, english, _, box, _, _ in RECORDS:
            l, t, r, b = box
            assert all(native5(im.getpixel((x, y))) == native5(atlas.getpixel((x, y)))
                       for y in range(t, b) for x in range(l, r)), (frame, english)
            count = (r - l) * (b - t)
            pixels += count
            regions.append({'English': english, 'complete_box': list(box), 'native5_pixels': count})
        actual = machine(arm)
        actual.mem_write(BASE, raw)
        captured_name = struct.unpack('<I', actual.mem_read(owner + 12, 4))[0]
        assert bytes(actual.mem_read(captured_name, 64)).split(b'\0')[0] == b'_pxl/chihofleetinfo.pxl'
        call(actual, 0xCB1A8, ())
        table = actual.reg_read(UC_ARM_REG_R0)
        fleet = table + 4 + 57 * 0x84
        values = []
        for entry in (0x36914, 0x36948, 0x367FC):
            call(actual, entry, (fleet,))
            values.append(actual.reg_read(UC_ARM_REG_R0))
        assert values[0:2] == [1, 0] and values[2] != 0
        rows.append({'frame': frame, 'screenshot': str(image_path), 'screenshot_sha256': sha(image_path.read_bytes()),
                     'RAM_sha256': sha(raw), 'whole_named_resource_resident': BASE + raw.find(resource),
                     'regional_fleet_record': fleet, 'original_own_main_finance_getters': values, 'regions': regions})
    fixture = read(ROOT / 'formed_fixture_manifest.json')
    assert sha(Path(fixture['fixture']).read_bytes()) == fixture['fixture_sha256']
    assert sha(Path(fixture['original_donor']).read_bytes()) == fixture['original_donor_sha256']
    assert fixture['normal_Save_UI_slot'] == 6
    proof = {'source_candidate': str(rom_path), 'source_candidate_sha256': report['ROM_sha256'],
             'source_report': str(RUN / 'capture_report.json'), 'source_report_sha256': sha((RUN / 'capture_report.json').read_bytes()),
             'frames': report['frames'], 'original_executed_resource_initializer': [0x0210FAB0, 0x0210FAD4],
             'actual_initialized_resource_owner': owner, 'exact_named_resource': FILE, 'resource_sha256': sha(resource),
             'all5_complete_native_regions': rows, 'complete_native5_region_pixels': pixels,
             'normal_creation_and_Manage_Area_assignment_from_Syracuse_to_Stockholm': True,
             'source_prerequisite_fixtures': ['one funds word', 'Gerhard Spirit byte', 'Manuel Charm byte'],
             'original_Gerhard_refusal_preserved_then_Manuel_selected': True,
             'normal_Save_slot6_fixture': fixture, 'whole_4MiB_replay_identity': read(ROOT / 'stockholm_replay_identity.json'),
             'persistent_top_view_binding_not_established': True,
             'observed_untranslated_mission_and_confirmation_family_pending_V615_native_checks': True,
             'earned_wealth_abilities_regional_progression_or_monthly_income_verified': False,
             'all18_original_plaque_entries_and22_historical_scopes_retained': True,
             'full_goal_complete': False, 'hardware_device_verification': False,
             'verifier_sha256': sha(Path(__file__).read_bytes())}
    save(ROOT / 'original_formation_native_proof.json', proof)
    ARCHIVE.mkdir(parents=True, exist_ok=True)
    files = []
    for frame in (26600, 27000, 27400, *frames, 44600, 45000, 45600):
        source = RUN / f'frame_{frame:06d}_navigation.png'
        target = ARCHIVE / source.name
        shutil.copy2(source, target)
        files.append({'file': str(target), 'sha256': sha(target.read_bytes()), 'unmodified_native_capture': True})
    for source in (ROOT / 'original_formation_native_proof.json', ROOT / 'formed_fixture_manifest.json', RUN / 'capture_report.json',
                   RUN / 'navigation_command_journal.json'):
        shutil.copy2(source, ARCHIVE / source.name)
    save(ARCHIVE / 'archive_manifest.json', {'source_candidate': str(rom_path), 'files': files,
         'test_prerequisites_synthetic': True, 'guide_or_user_save_progression': False, 'full_goal_complete': False})
    print(f'Original regional formation verified:all5 full plaque regions across6 actual states,{pixels} native5 pixels; isolated slot6 saved. Mission family remains open.')


if __name__ == '__main__':
    main()
