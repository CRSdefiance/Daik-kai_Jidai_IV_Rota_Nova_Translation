"""Verify the initialized Cappadocia route and the original discovery outcome."""

from pathlib import Path

from PIL import Image, ImageChops, ImageDraw

from dk4tool.dialogue.font_audit import GameAsciiFont
from scripts import replay_ruin_discovery_display_20261120 as replay
from scripts import stage_ruin_discovery_display_20261120 as stage
from scripts.check_swimmer_leak_square_dialogue_20261120 import one_frame, ram_at
from scripts.preflight_shared_dynamic_notice_wrap_v1 import font_tools, render
from scripts.verify_personal_gameplay_v841 import get_machine


RUNS = Path('E:/Rota Nova translations/Generated/work/ruin_discovery_20261120')
PROOF = stage.ROOT / 'discovery_gameplay.json'
SHEET = stage.ROOT / 'discovery_gameplay.png'
PALACE = stage.ROOT.parent / 'palace_fee_finding.json'
BANNER_FRAMES = (7560, 7710, 7870)
POWER_FRAMES = (8030, 8200)
STATE_FRAMES = (4380, 7870, 8200, 8530)
POWER_CROP = (16, 296, 244, 344)
LABELS = ('Ruins Found', 'Cappadocia discovered')
ROMS = (stage.parent.ROM, stage.ROM)
OLD, NEW = ('current', 'revised')
batch = stage.batch
digest = stage.parent.base.digest


def check_banner(arm, image):
    font = GameAsciiFont.from_arm9(arm)
    for text, top in zip(LABELS, (194, 256), strict=True):
        start = 128 - 3 * len(text)
        observed = {(x, y) for y in range(top, top + 16) for x in range(20, 236)
                    if image.getpixel((x, y)) == (230, 230, 230)}
        expected = set()
        for index, char in enumerate(text):
            glyph = font.decode(char)
            expected.update((start + 6 * index + x, top + 1 + y) for y in range(11) for x in range(6)
                            if glyph.getpixel((x, y)))
        assert observed == expected


def check_power(rom, image, ram, revised):
    arm, kanji = rom.read_file(batch.ARM), rom.read_file('/GRP/KANJI.FNT')
    raster, _, _ = font_tools(rom)
    text = ('Power increased by 5.' if revised else 'Power increased by ５.').encode('cp932')
    assert ram[0x28E474:0x28E474 + len(text) + 1] == text + b'\0'
    plane, _ = render(raster, arm, kanji, text)
    pixels = image.crop(POWER_CROP).get_flattened_data()
    assert bytes(px == (0, 8, 0) for px in pixels) == bytes(px == 1 for px in plane)
    return text.hex()


def state(arm, ram):
    _, get = get_machine(arm, ram)
    assert get(0xB65E4) == 22
    town = get(0xB6618)
    assert get(0xB5170, town) == 8 and get(0xB2B48, town) == 1
    site = get(0xCB16C) + 4 + 8 * 8 - stage.BASE
    company = get(0xCB160) + 4 + 0x4C * get(0x397D8) - stage.BASE
    return dict(site_flags=ram[site + 4], company=ram[company:company + 0x4C].hex())


def verify_palace(roms):
    reports = [RUNS / 'paired_v2' / side / 'capture_report.json' for side in (OLD, NEW)]
    loaded = [batch.load(path) for path in reports]
    frames, rams = [], []
    for report, rom in zip(loaded, ROMS, strict=True):
        assert report['ROM_sha256'] == digest(rom) and not report['callback_errors']
        frames.append([one_frame(report, n)[0] for n in (25400, 25540, 25680, 25810)])
        snap, ram = ram_at(report, 25400)
        assert b'is ' + '２８４２'.encode('cp932') + b' gold coins.\0' in ram
        rams.append(snap)
    assert [x['framebuffer_sha256'] for x in frames[0]] == [x['framebuffer_sha256'] for x in frames[1]]
    clean = batch.NdsImage.open(batch.CLEAN)
    source = batch.common_message_entries(clean.read_file(batch.COMMON), clean.read_file(batch.ARM))
    arm, common = roms[0].read_file(batch.ARM), roms[0].read_file(batch.COMMON)
    current = batch.owned_entries(common, arm, batch.digest(arm[batch.DIRECTORY_OFFSET:batch.TABLE_OFFSET]))
    rows = [dict(message_ID=n, clean_Japanese=source[n].text.decode('cp932'), source_reference=batch.reference(source[n]),
                 english=current[n].text.decode('ascii'), current_reference=batch.reference(current[n]),
                 source_hex=source[n].text.hex(), current_hex=current[n].text.hex())
            for n in (1156, 1157, 1149)]
    batch.write(PALACE, dict(status='confirmed display issue', message_ID=1156, observed_fee=2842,
        followup_message_ID=1157, alternate_fee_message_ID_not_visited=1149, clean_and_current=rows,
        frame_25400_full_width_CP932='２８４２'.encode('cp932').hex(), regular_digits_in_payment_frame=25680,
        accepted_payment_frame=25810, observed_playthrough='Istanbul Gate access fixture only; Palace contract uses ordinary inputs',
        paired_frames=frames, fee_RAM=rams, capture_reports={str(p): digest(p) for p in reports}))


def main():
    assert not any(path.exists() for path in (PROOF, SHEET, PALACE))
    paths = [RUNS / 'paired_late_v2' / side / 'capture_report.json' for side in (OLD, NEW)]
    loaded = [batch.load(path) for path in paths]
    roms = [batch.NdsImage.open(path) for path in ROMS]
    evidence = {str(path): digest(path) for path in paths}
    sheets = Image.new('RGB', (1036, 2 * 795), '#263238')
    draw = ImageDraw.Draw(sheets)
    journals, states, rows, captures = [], [], [], []
    for index, (report, path, rom, rompath) in enumerate(zip(loaded, paths, roms, ROMS, strict=True)):
        assert report['ROM_sha256'] == digest(rompath) and report['frames'] == 8530
        assert report['cold_boot'] and not report['savestate_loaded'] and not report['callback_errors']
        donor = report['battery_save_preloaded']
        assert digest(donor['source']) == donor['source_sha256'] == replay.LATE_DONOR_SHA
        assert donor['copied_byte_exact_before_cold_boot']
        assert {key for key, value in report.items() if key.startswith('synthetic_') and value} == {'synthetic_condition_fixtures'}
        reset, map_transfer = report['synthetic_condition_fixtures']
        assert reset['frame'] == 4260 and reset['only_existing_discovery_bit_reset']
        assert [(row['before'], row['after']) for row in reset['changes']] == [(1, 0)]
        assert map_transfer['frame'] == 4320 and map_transfer['item_ID'] == 164 and len(map_transfer['changes']) == 3
        assert map_transfer['quests_calendar_facility_flags_location_dialogue_and_every_other_RAM_byte_exact']
        journal = path.with_name('navigation_command_journal.json')
        transcript = batch.load(journal)
        assert transcript['last_command_frame'] == report['frames'] and transcript['commands_are_not_execution_receipts']
        rejected = [row for row in transcript['commands_received'] if not row['validation_passed']]
        assert len(rejected) == 2 and all(row['frame'] == 3200 and 'until' not in row['command'] for row in rejected)
        journals.append(transcript['commands_received'])
        evidence[str(journal)] = digest(journal)

        arm = rom.read_file(batch.ARM)
        shot_cache = {n: one_frame(report, n) for n in (7420, *BANNER_FRAMES, *POWER_FRAMES, 8530)}
        memory = {n: ram_at(report, n) for n in sorted(set(BANNER_FRAMES + POWER_FRAMES + STATE_FRAMES))}
        for records in (value[0] for value in list(shot_cache.values()) + list(memory.values())):
            evidence[records['path']] = records.get('PNG_sha256', records.get('sha256'))
        states.append({n: state(arm, raw) for n, (_, raw) in memory.items() if n in STATE_FRAMES})
        for n in BANNER_FRAMES:
            suffix = stage.SUFFIX if index else stage.SOURCE_SUFFIX.encode('cp932')
            assert memory[n][1][0x2A47F8:0x2A4800 + 64].split(b'\0', 1)[0] == b'Cappadocia' + suffix
            if index:
                check_banner(arm, shot_cache[n][1])
        rows.append([check_power(rom, shot_cache[n][1], memory[n][1], index) for n in POWER_FRAMES])
        for j, n in enumerate((7870, 8200)):
            x, y = index * 518, j * 795
            title = 'Revised' if index else 'Previous'
            draw.text((x + 5, y + 4), f'{title}  /  frame {n}', fill='white')
            image = shot_cache[n][1]
            sheets.paste(image.resize((512, 768), Image.Resampling.NEAREST), (x + 3, y + 20))
        captures.append(shot_cache)
    assert journals[0] == journals[1]
    assert loaded[0]['core_DLL_sha256'] == loaded[1]['core_DLL_sha256'] and loaded[0]['core_options'] == loaded[1]['core_options']
    assert [r['changes'] for r in loaded[0]['synthetic_condition_fixtures']] == [r['changes'] for r in loaded[1]['synthetic_condition_fixtures']]
    assert states[0] == states[1]
    assert [v['site_flags'] for v in states[0].values()] == [0, 0, 1, 1]
    assert states[0][4380] == states[0][7870] and states[0][8200] == states[0][8530]
    before, after = (bytes.fromhex(states[0][n]['company']) for n in (7870, 8200))
    assert [i for i, (a, b) in enumerate(zip(before, after, strict=True)) if a != b] == [0x12]
    assert after[0x12] - before[0x12] == 10
    for n in (7420, 8530):
        assert captures[0][n][0]['framebuffer_sha256'] == captures[1][n][0]['framebuffer_sha256']
    differences = {}
    for n in BANNER_FRAMES + POWER_FRAMES:
        diff = ImageChops.difference(*(capture[n][1] for capture in captures))
        differences[n] = diff.getbbox()
        ranges = ((194, 210), (256, 272)) if n in BANNER_FRAMES else ((296, 308),)
        assert differences[n] and all(diff.crop((0, y, 256, y + 1)).getbbox() is None
                                      for y in range(384) if not any(a <= y < b for a, b in ranges))
    sheets.save(SHEET)
    verify_palace(roms)
    batch.write(PROOF, dict(candidate_sha256=digest(ROMS[1]), predecessor_sha256=digest(ROMS[0]),
        banner_frames=BANNER_FRAMES, power_frames=POWER_FRAMES, regular_digit_notice_hex=rows[1][0],
        old_wide_digit_notice_hex=rows[0][0], displayed_reward=5, independent_full_english_banner_ink=True,
        both_power_notice_full_native_masks=True, original_banner_and_reward_after_normal_inputs=True,
        identical_frames_before_and_after=[7420, 8530], differences=differences,
        paired_native_site_and_company_states=states[0], hardware=False, ordinary_initialization=False,
        original_donor_sha256=replay.LATE_DONOR_SHA, fixture_modes=['restore-first-discovery', 'ceremony-Cappadocia-map'],
        reviewed_contact_sheet=dict(path=str(SHEET), sha256=digest(SHEET)), evidence=evidence))
    print('Paired original discovery, both Power notices, exact return and Palace fee finding verified.')


if __name__ == '__main__':
    main()
