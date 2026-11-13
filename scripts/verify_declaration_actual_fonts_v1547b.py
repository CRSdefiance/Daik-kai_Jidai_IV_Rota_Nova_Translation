"""Bind every changed original war-response frame to full native text and exact pixels."""
import struct
from pathlib import Path
from types import FunctionType
from PIL import Image
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.declaration_responses_editorial import current_entries
from dk4tool.patch.grand_race_menu_release import sha
from scripts.probe_battle_aftermath_fonts_v1256 import consumer
from scripts.verify_personal_gameplay_v841 import get_machine
from scripts.verify_common_alignment_native_v257 import raster as original_raster
from scripts.verify_shipyard_gameplay_v760 import independent_font
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/declaration_responses_actual_fonts_v1547b')
AUDIT = Path('work/analysis/declaration_responses_control_verified_v1547/actual_declaration_defeat_and_transfer_return.json')
BASE, TABLE = 0x02000000, 0x021184E0

if __name__ == '__main__':
    assert not ROOT.exists()
    audit = read(AUDIT)
    assert audit['entire4MiB_sole_prebattle40_owned_byte_fixture_and_all_validated_input_schedule_audited']
    assert audit['original_Y_Auto_duel_loss_and_normal_evacuate_flagship_defeat_transfer_and_return_to_sailing']
    assert audit['source_and_disposable_donor_unchanged'] and audit['terminal_frame'] == 9200
    rom = NdsImage.open(audit['candidate'])
    arm, common = rom.read_file('/__arm9__.bin'), rom.read_file('/COMMON/MESFILE.DK4')
    assert sha(Path(audit['candidate']).read_bytes()) == audit['candidate_sha256']
    report = read(audit['terminal_report'])
    assert sha(Path(audit['terminal_report']).read_bytes()) == audit['terminal_report_sha256']
    snapshots = {r['frame']: r for r in report['read_only_capture_RAM_snapshots'] + report['read_only_pause_RAM_snapshots']}
    previous_proof = read('work/analysis/retreat_transfer_control_verified_v1525/actual_declaration_defeat_and_transfer_return.json')
    previous_report = read(previous_proof['terminal_report'])
    assert sha(Path(previous_proof['terminal_report']).read_bytes()) == previous_proof['terminal_report_sha256']
    old_rom = NdsImage.open(previous_proof['candidate'])
    assert rom.read_file('/GRP/KANJI.FNT') == old_rom.read_file('/GRP/KANJI.FNT')
    old_arm = old_rom.read_file('/__arm9__.bin')
    old_frames = {r['frame']: r for r in previous_report['frames_captured']}
    old_snapshots = {r['frame']: r for r in previous_report['read_only_capture_RAM_snapshots'] + previous_report['read_only_pause_RAM_snapshots']}
    entries = current_entries(common, arm)
    fonts = read('work/analysis/declaration_responses_fonts_v1537c/native_font_research.json')
    assert fonts['ARM9_sha256'] == sha(arm) and fonts['COMMON_sha256'] == sha(common)
    case = next(r for r in fonts['cases'] if r['message_ID'] == 2205)
    assert case['existing_actor_ID'] == 28 and case['source_voice'] == 4

    class CurrentFont:
        @staticmethod
        def open(path):
            assert path == 'out/all_routes_combined_v255_candidate.nds'
            return rom

    raster = FunctionType(original_raster.__code__, {**original_raster.__globals__, 'NdsImage': CurrentFont}, argdefs=original_raster.__defaults__)
    owner, wrapped = [struct.unpack_from('<I', arm, p)[0] - BASE for p in [0x552A0, 0x54450]]
    old_wrapped = struct.unpack_from('<I', old_arm, 0x54450)[0] - BASE
    holds, controls = [], []
    for row in report['frames_captured']:
        frame = row['frame']
        old = old_frames[frame]
        assert sha(Path(row['path']).read_bytes()) == row['PNG_sha256']
        assert sha(Path(old['path']).read_bytes()) == old['PNG_sha256']
        with Image.open(row['path']) as current_image, Image.open(old['path']) as old_image:
            picture, old_picture = current_image.convert('RGB'), old_image.convert('RGB')
            differences = {(i % 256, i // 256) for i, (x, y) in enumerate(zip(picture.get_flattened_data(), old_picture.get_flattened_data(), strict=True)) if x != y}
            if not differences:
                controls.append({'frame': frame, 'whole256x384_RGB_exact_to_V1520': True, 'source': old['path'], 'source_sha256': old['PNG_sha256']})
                continue
            snapshot = snapshots[frame]
            raw = Path(snapshot['path']).read_bytes()
            assert sha(raw) == snapshot['sha256']
            cpu, get = get_machine(arm, raw)
            company = get(0xCB160) + 4 + 4 * 76
            actor = get(0x3CD2C, company)
            assert actor == get(0xCB184) + 4 + 28 * 32
            assert get(0x7EE08, actor) == 28 and get(0x7E988, actor) == 4
            assert get(0x53F4C, actor, TABLE) == 2205
            template = raw[owner + 0x2030:owner + 0x2230].split(b'\0')[0]
            assert template == entries[2205].text
            formatted = raw[wrapped:wrapped + 512].split(b'\0')[0]
            assert formatted.hex() == case['native_pipeline']['formatted_hex']
            native = consumer(arm, common, raw, {'patches': []}, 0x53F0C, actor, TABLE)
            assert native['input_hex'] == template.hex() and native['formatted_hex'] == formatted.hex()
            assert native['parent'] == 0x02053F40 and native['selector_offset'] == 0x274
            pixels = raster(arm, formatted, 0x01FFCE40 - BASE, size=(228, 64), instruction_limit=2000000)
            assert pixels == independent_font(arm, rom.read_file('/GRP/KANJI.FNT'), case['lines'])
            with Image.open(case['preview']) as preview:
                reference = preview.convert('L')
                assert all(bool(p) == (reference.getpixel((i % 228, i // 228)) == 0) for i, p in enumerate(pixels))
            expected = {(16 + i % 228, 296 + i // 228) for i, p in enumerate(pixels) if p}
            actual = {(x, y) for y in range(294, 366) for x in range(16, 244) if picture.getpixel((x, y)) == (0, 8, 0)}
            assert actual == expected, (frame, len(expected - actual), len(actual - expected))
            old_snapshot = old_snapshots[frame]
            old_raw = Path(old_snapshot['path']).read_bytes()
            assert sha(old_raw) == old_snapshot['sha256']
            old_formatted = old_raw[old_wrapped:old_wrapped + 512].split(b'\0')[0]
            old_lines = [r.strip().decode('cp932') for r in old_formatted.split(b'\n')]
            old_pixels = raster(arm, old_formatted, 0x01FFCE40 - BASE, size=(228, 64), instruction_limit=2000000)
            # The old unscoped first line has zero indent; compare the native
            # complete old plane directly rather than imposing the repaired margin.
            old_expected = {(16 + i % 228, 296 + i // 228) for i, p in enumerate(old_pixels) if p}
            old_actual = {(x, y) for y in range(294, 366) for x in range(16, 244) if old_picture.getpixel((x, y)) == (0, 8, 0)}
            assert old_actual == old_expected
            assert differences == old_expected ^ expected, frame
        block = IlnkContainer.parse(common).blocks[entries[2205].block]
        assert entries[2205].block == 23 and raw.count(block) == 1
        holds.append({'frame': frame, 'message_ID': 2205, 'actual_original_company': 4, 'actual_company_leader_getter': 0x0203CD2C,
            'actual_actor_ID': 28, 'actual_voice': 4, 'source_table': TABLE, 'original_parent': 0x02053F40,
            'native_pipeline': native, 'lines': case['lines'], 'formatted_hex': formatted.hex(),
            'whole228x64_native_independent_reference_and_actual_RGB_exact': True,
            'complete_first_final_letters_uniform6px_margins_bounds_blank_paper_and_pagination_pass': True,
            'whole_current_COMMON23_resident_exactly_once': True,
            'whole256x384_changed_pixels': len(differences), 'every_changed_pixel_exact_old_new_native_glyph_symmetric_difference': True,
            'all_other_portrait_scenery_border_and_paper_pixels_unchanged': True,
            'old_formatted_hex': old_formatted.hex(), 'old_lines': old_lines,
            'PNG': row['path'], 'PNG_sha256': row['PNG_sha256'], 'RAM_sha256': snapshot['sha256'],
            'source_PNG': old['path'], 'source_PNG_sha256': old['PNG_sha256']})
    assert holds and 6150 in {h['frame'] for h in holds}
    assert {6300, 8750, 8800, 8850, 9000, 9200} <= {c['frame'] for c in controls}
    assert len(holds) + len(controls) == len(report['frames_captured']) == 45
    ROOT.mkdir(parents=True)
    save(ROOT / 'actual_NPC_response_font_and_transition_verification.json', {
        'candidate': audit['candidate'], 'candidate_sha256': audit['candidate_sha256'],
        'report': audit['terminal_report'], 'report_sha256': audit['terminal_report_sha256'],
        'complete_original_event_audit': str(AUDIT), 'complete_original_event_audit_sha256': sha(AUDIT.read_bytes()),
        'complete_actual2205_holds': holds, 'all_other_sampled_whole_frames_exact_to_V1520': controls,
        'every_changed_frame_and_pixel_explained_no_mask_waiver_or_retiming': True,
        'normal_declaration_Yes_NPC_response_A_close_battle_duel_defeat_retreat_transfer_and_return_to_sailing': True,
        'only2205_individually_activated_other7_voices_have_complete_native_and_representative_family_proof': True,
        'one40byte_prebattle_location_fixture_no_combat_actor_RNG_outcome_changes_saves_unchanged': True,
        'targeted_headless_not_full_route_or_hardware': True, 'visual_review_still_pending': True,
        'producer_sha256': sha(Path(__file__).read_bytes()), 'full_goal_complete': False})
    print('Original2205 complete native/RGB holds:', len(holds), ';unchanged whole V1520 controls:', len(controls), ';all changed pixels and normal battle/retreat return verified.')
