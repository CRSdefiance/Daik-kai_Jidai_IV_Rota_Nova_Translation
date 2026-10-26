"""Actual original role/name selection, whole native text planes and return controls."""
import struct
from pathlib import Path
from types import FunctionType
from PIL import Image
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.retreat_transfer_editorial import current_entries
from dk4tool.patch.grand_race_menu_release import sha
from scripts.probe_battle_aftermath_fonts_v1256 import consumer
from scripts.verify_personal_gameplay_v841 import get_machine
from scripts.verify_common_alignment_native_v257 import raster as original_raster
from scripts.verify_shipyard_gameplay_v760 import independent_font
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/retreat_transfer_actual_fonts_v1526')
CAP = Path('E:/Rota Nova translations/Generated/work/emulation_v193/retreat_transfer_v1524_1520')
ROM = Path('out/all_routes_combined_v1520_candidate.nds')
BASE, TABLE = 0x02000000, 0x02117080

if __name__ == '__main__':
    assert not ROOT.exists()
    audit_path = Path('work/analysis/retreat_transfer_control_verified_v1525/actual_declaration_defeat_and_transfer_return.json')
    audit = read(audit_path)
    assert audit['candidate_sha256'] == sha(ROM.read_bytes())
    assert audit['entire4MiB_sole_prebattle40_owned_byte_fixture_and_all_validated_input_schedule_audited']
    assert audit['original_Y_Auto_duel_loss_and_normal_evacuate_flagship_defeat_transfer_and_return_to_sailing']
    report_path = CAP / 'capture_report.json'
    report = read(report_path)
    assert sha(report_path.read_bytes()) == audit['terminal_report_sha256']
    snapshots = {r['frame']: r for r in report['read_only_capture_RAM_snapshots'] + report['read_only_pause_RAM_snapshots']}
    rom = NdsImage.open(ROM)
    arm, common = rom.read_file('/__arm9__.bin'), rom.read_file('/COMMON/MESFILE.DK4')
    entries = current_entries(common, arm)
    fonts = read('work/analysis/retreat_transfer_fonts_v1515/native_font_research.json')
    assert fonts['ARM9_sha256'] == sha(arm) and fonts['COMMON_sha256'] == sha(common)
    case = next(c for c in fonts['cases'] if c['source_voice'] == 1 and c['variant'] == 0)
    assert case['message_ID'] == 2684 and case['name'] == 'Latina'

    class CurrentFont:
        @staticmethod
        def open(path):
            assert path == 'out/all_routes_combined_v255_candidate.nds'
            return rom

    raster = FunctionType(original_raster.__code__, {**original_raster.__globals__, 'NdsImage': CurrentFont}, argdefs=original_raster.__defaults__)
    owner, wrapped = [struct.unpack_from('<I', arm, p)[0] for p in [0x552A0, 0x54450]]
    holds = []
    for frame in [8800, 8850]:
        row = snapshots[frame]
        raw = Path(row['path']).read_bytes()
        assert sha(raw) == row['sha256']
        cpu, get = get_machine(arm, raw)
        fleets, actors = get(0xCB1A8), get(0xCB184)
        identity = get(0x82478, fleets + 0x2090, 1)
        actor = get(0x82428, fleets + 0x2090, 1)
        assert identity == get(0x7EE08, actor) == 16 and actor == actors + 4 + 16 * 32
        assert get(0x7E988, actor) == 1 and get(0x53F4C, actor, TABLE) == 2684
        model = get(0x36C94, fleets + 4 + 132 + 12)
        vtable = struct.unpack('<I', cpu.mem_read(model, 4))[0]
        getter = struct.unpack('<I', cpu.mem_read(vtable + 4, 4))[0]
        pointer = get(getter - BASE, model)
        name = bytes(cpu.mem_read(pointer, 64)).split(b'\0')[0]
        assert name == b'Latina'
        assert raw[owner - BASE + 0x2030:owner - BASE + 0x2230].split(b'\0')[0] == entries[2684].text
        formatted = raw[wrapped - BASE:wrapped - BASE + 512].split(b'\0')[0]
        assert formatted.hex() == case['native_pipeline']['formatted_hex']
        native = consumer(arm, common, raw, {'patches': []}, 0x53D44, 1, TABLE, name)
        assert native['formatted_hex'] == formatted.hex()
        assert native['input_hex'] == entries[2684].text.replace(b'%s', name).hex()
        assert native['parent'] == 0x02053DB8 and native['selector_offset'] == 0x27C
        pixels = raster(arm, formatted, 0x01FFCE40 - BASE, size=(228, 64), instruction_limit=2000000)
        assert pixels == independent_font(arm, rom.read_file('/GRP/KANJI.FNT'), case['lines'])
        with Image.open(case['preview']) as original_preview:
            reference = original_preview.convert('L')
            assert all(bool(p) == (reference.getpixel((i % 228, i // 228)) == 0) for i, p in enumerate(pixels))
        picture_path = CAP / f'frame_{frame:06d}_navigation.png'
        with Image.open(picture_path) as source_picture:
            picture = source_picture.convert('RGB')
            expected = {(16 + i % 228, 296 + i // 228) for i, p in enumerate(pixels) if p}
            actual = {(x, y) for y in range(294, 366) for x in range(16, 244) if picture.getpixel((x, y)) == (0, 8, 0)}
            assert actual == expected, (frame, len(expected - actual), len(actual - expected))
        block = IlnkContainer.parse(common).blocks[28]
        assert raw.count(block) == 1
        holds.append({'frame': frame, 'message_ID': 2684, 'actual_original_role': 1, 'actual_actor_ID': identity,
            'actual_source_voice': 1, 'source_table': TABLE, 'parent': 0x02053DB8,
            'replacement_ship_model': model, 'original_virtual_ship_name': name.decode('ascii'),
            'native_pipeline': native, 'formatted_hex': formatted.hex(), 'lines': case['lines'],
            'entire228x64_native_independent_reference_and_actual_RGB_exact': True,
            'complete_edge_letters_uniform_margin_bounds_blank_paper_and_literal_name_pass': True,
            'actual_current_COMMON28_resident_exactly_once': True, 'foreground_pixels': len(expected),
            'PNG': str(picture_path), 'PNG_sha256': sha(picture_path.read_bytes()), 'RAM_sha256': row['sha256']})
    old_proof = read('work/analysis/stronger_fleet_return_verified_v1505/actual_declaration_defeat_and_transfer_return.json')
    old_report_path = Path(old_proof['terminal_report'])
    assert sha(old_report_path.read_bytes()) == old_proof['terminal_report_sha256']
    old_report = read(old_report_path)
    old_frames = {r['frame']: r for r in old_report['frames_captured']}
    controls = []
    for row in report['frames_captured']:
        frame = row['frame']
        if frame in [8800, 8850]:
            continue
        old = old_frames[frame]
        assert sha(Path(old['path']).read_bytes()) == old['PNG_sha256']
        with Image.open(row['path']) as current_picture, Image.open(old['path']) as old_picture:
            assert current_picture.convert('RGB').tobytes() == old_picture.convert('RGB').tobytes(), frame
        controls.append({'frame': frame, 'whole256x384_RGB_exact_to_V1492': True, 'source': old['path'], 'source_sha256': old['PNG_sha256']})
    assert {9000, 9200} <= {c['frame'] for c in controls}
    ROOT.mkdir(parents=True)
    save(ROOT / 'actual_retreat_font_and_transition_verification.json', {
        'candidate': str(ROM), 'candidate_sha256': sha(ROM.read_bytes()), 'report': str(report_path),
        'report_sha256': sha(report_path.read_bytes()), 'complete_original_event_audit': str(audit_path),
        'complete_original_event_audit_sha256': sha(audit_path.read_bytes()), 'complete_actual2684_holds': holds,
        'all_other_sampled_whole_frames_exact_to_V1492': controls,
        'original_declaration_damage_auto_duel_defeat_evacuation_flagship_loss_transfer_A_dismissal_and_sailing_return': True,
        'only2684_individually_activated_other6_templates_and_voice3_fallback_have_native_proof': True,
        'one40byte_prebattle_location_fixture_no_later_mutations_and_saves_unchanged': True,
        'targeted_headless_not_full_route_or_physical_device': True,
        'visual_review_still_pending': True, 'producer_sha256': sha(Path(__file__).read_bytes()), 'full_goal_complete': False})
    print('Actual2684 two full native/reference/RGB holds and all other sampled V1492 frames/normal sailing return pass.')
