"""Actual Guild context plus original native NPC lookup/caller evidence."""

import struct
from pathlib import Path

from ndspy.code import MainCodeFile
from PIL import Image
from unicorn import UC_HOOK_CODE
from unicorn.arm_const import UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R10, UC_ARM_REG_SP, UC_ARM_REG_LR

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import common_message_entries
from scripts.native_call_abi_v764 import call
from scripts.native_machine_scoped_v764 import machine
from scripts.prepare_item_type_provider_v786 import ROOT, CURRENT
from scripts.probe_button_prompt_native import BASE, STACK, STOP
from scripts.record_navigation_v327 import dark_text
from scripts.verify_market_gameplay_v753 import state
from scripts.verify_port_gameplay_v762 import cstring
from scripts.verify_shipyard_gameplay_v760 import models
from scripts.verify_tavern_gameplay_v767 import persistent_objects
from scripts.verify_village_wrap_v608 import read, save

CAP = Path('E:/Rota Nova translations/Generated/work/emulation_v193/item_guild_v786')
SAVE_SHA = '942c74828a7b7396f7567ca2d405ddc4cdd329e4837f591777d35ee458794b0f'


def main():
    report_path = CAP/'capture_report.json'
    report = read(report_path)
    assert report['frames'] == 8400 and report['cold_boot'] and not report['savestate_loaded']
    assert not report['callback_errors'] and not report['goal_complete'] and not report['hardware_device_verification']
    assert not any(v for k, v in report.items() if k.startswith('synthetic_'))
    assert report['core_DLL_sha256'] == '42160dbfef89adfb3cfd975070a3047d8ad0979cead55607ebdfd3b931046c2b'
    assert sha(Path('scripts/headless_desmume_v193.py').read_bytes()) == 'd5bcc9a11b5602bfb44d54e75b02a7a7a0165c9ee819a07cd0cbdac2130b8c6e'
    assert sha(CURRENT.read_bytes()) == report['ROM_sha256'] == '9f55817772d2b1e940462f69103536654f0cbedbe959fb42670fc601f2d6e31d'
    donor = report['battery_save_preloaded']
    assert donor['source'] != donor['destination'] and donor['copied_byte_exact_before_cold_boot']
    assert sha(Path(donor['source']).read_bytes()) == donor['source_sha256'] == SAVE_SHA
    snapshots = {}
    for row in report.get('read_only_capture_RAM_snapshots', [])+report['read_only_pause_RAM_snapshots']:
        raw = Path(row['path']).read_bytes()
        assert len(raw) == row['bytes'] == 0x400000 and row['read_only_export'] and sha(raw) == row['sha256']
        if row['frame'] in snapshots:
            assert snapshots[row['frame']] == raw
        snapshots[row['frame']] = raw
    frames = {}
    for row in report['frames_captured']:
        assert sha(Path(row['path']).read_bytes()) == row['PNG_sha256']
        frames[row['frame']] = row
    old_path = Path('E:/Rota Nova translations/Generated/work/emulation_v193/shared_v783_private_live2/capture_report.json')
    old = read(old_path)
    old_png = next(r for r in old['frames_captured'] if r['frame'] == 3200)
    old_ram = next(r for r in old['read_only_capture_RAM_snapshots'] if r['frame'] == 3200)
    assert Image.open(frames[3200]['path']).tobytes() == Image.open(old_png['path']).tobytes()
    assert snapshots[3200] == Path(old_ram['path']).read_bytes()
    assert struct.unpack_from('<I', snapshots[5600], 0x279678)[0] == 5
    assert struct.unpack_from('<I', snapshots[7200], 0x279678)[0] == 5
    rom, clean_rom = NdsImage.open(CURRENT), NdsImage.open('work/clean.nds')
    arm, clean = [r.read_file('/__arm9__.bin') for r in (rom, clean_rom)]
    source_spans = [(0x5BE00, 0x5C450), (0xB2CD8, 0xB2D58), (0xB51B4, 0xB51CC),
                    (0xB65E4, 0xB6660), (0x7F1D4, 0x7F1F4), (0x7F37C, 0x7F39C)]
    for lo, hi in source_spans:
        assert arm[lo:hi] == clean[lo:hi]
    table, length = 0x11948C, 21*14
    assert arm[table:table+length] == clean[table:table+length]
    assert [arm[table+n*14] for n in range(21)] == list(range(21))

    def cpu_for(raw_arm, raw, original=False):
        cpu = machine(raw_arm)
        cpu.mem_write(BASE, raw)
        if original:
            for section in MainCodeFile(raw_arm, BASE).sections:
                cpu.mem_write(section.ramAddress, bytes(section.data))
        return cpu

    def ptr(cpu, at): return struct.unpack('<I', cpu.mem_read(at, 4))[0]
    def get(cpu, fn, args=()):
        call(cpu, fn, args)
        return cpu.reg_read(UC_ARM_REG_R0)
    def name(cpu, obj):
        method = ptr(cpu, ptr(cpu, obj)+8)
        value = get(cpu, method-BASE, (obj,))
        return bytes(cpu.mem_read(value, 128)).split(b'\0', 1)[0].decode('cp932')

    all_towns, live = [], []
    for label, raw_arm in (('clean-Japanese', clean), ('V783', arm)):
        cpu = cpu_for(raw_arm, snapshots[5600], label == 'clean-Japanese')
        town_root = get(cpu, 0xCB178)
        actor_root = get(cpu, 0xCB184)
        current_town = get(cpu, 0xB6618)
        assert get(cpu, 0xB65E4) == 57 and current_town == town_root+4+57*108
        for town_id in range(90):
            town = town_root+4+town_id*108
            culture = get(cpu, 0xB51B4, (town,))
            assert 0 <= culture < 21
            actor = get(cpu, 0xB2CD8, (town, 5))
            actor_id = (actor-actor_root-4)//32
            assert actor == actor_root+4+actor_id*32
            assert actor_id == arm[table+culture*14+6]
            title = name(cpu, actor)
            assert title == ('ギルドの元締め' if label == 'clean-Japanese' else 'Guildmaster')
            all_towns.append({'version': label, 'town_id': town_id, 'culture': culture,
                'actor_id': actor_id, 'actor': actor, 'title': title})
        actor = get(cpu, 0xB2CD8, (current_town, 5))
        assert (actor-actor_root-4)//32 == 149
        # Original buy/sell prefixes obtain town and actual role from the
        # captured global state. No NPC sentinel or replacement getter is used.
        for begin, end, text_begin, expected_id in ((0x5C130, 0x5C144, 0x5C21C, 1071),
                                                   (0x5BE20, 0x5BE34, 0x5BE84, 1085)):
            cpu.reg_write(UC_ARM_REG_SP, STACK)
            cpu.reg_write(UC_ARM_REG_LR, STOP)
            cpu.emu_start(BASE+begin, BASE+end, count=100000)
            assert cpu.reg_read(UC_ARM_REG_R10) == actor
            observed = []
            def stop(c, pc, size, data):
                observed.append([pc, c.reg_read(UC_ARM_REG_R0), c.reg_read(UC_ARM_REG_R1)])
                c.emu_stop()
            hook = cpu.hook_add(UC_HOOK_CODE, stop, begin=0x02053FE4, end=0x02053FE4)
            try:
                cpu.emu_start(BASE+text_begin, STOP, count=100000)
            finally:
                cpu.hook_del(hook)
            assert observed == [[0x02053FE4, actor, expected_id]], observed
            live.append({'version': label, 'lookup_span': [BASE+begin, BASE+end],
                'speech_fragment': BASE+text_begin, 'native_role_from_actual_Guild_RAM': 5,
                'actor_id': 149, 'original_wrapper': 0x02053FE4, 'message_id': expected_id,
                'CPU_fragment_only_sell_menu_not_activated_in_capture': expected_id == 1085})
    assert {r['actor_id'] for r in all_towns} == {147, 148, 149, 150}

    # The actual old1071 consumer is proven from its full resident block,
    # owner template and printf buffer, rather than inferred from a short line.
    entries = common_message_entries(rom.read_file('/COMMON/MESFILE.DK4'), arm, clean=False)
    from dk4tool.formats.ilnk import IlnkContainer
    blocks = IlnkContainer.parse(rom.read_file('/COMMON/MESFILE.DK4')).blocks
    raw_ptr, wrapped_ptr, owner = [struct.unpack_from('<I', arm, at)[0] for at in (0x5444C, 0x54450, 0x552A0)]
    entry = entries[1071]
    assert entry.text == b' Which item?'
    raw = snapshots[7200]
    assert cstring(raw, owner+0x2030) == entry.text
    assert raw.count(blocks[entry.block]) == 1
    assert cstring(raw, raw_ptr) == entry.text
    font = GameAsciiFont.from_arm9(arm)
    glyph = dark_text(font, entry.text.removeprefix(b' ').decode(),
        Image.open(frames[7200]['path']).convert('RGB'), (12, 294, 250, 322))
    states = {str(f): state(arm, snapshots[f]) for f in (3200, 7200, 7600, 8400)}
    assert all(row == states['3200'] for row in states.values())
    assert states['3200']['cash'] == 38816
    assert models(arm, snapshots[3200]) == models(arm, snapshots[8400])
    before_objects, after_objects = [persistent_objects(arm, snapshots[f]) for f in (3200, 8400)]
    assert before_objects == after_objects
    save(ROOT/'Guild_context_verification.json', {'candidate': str(CURRENT), 'candidate_sha256': sha(CURRENT.read_bytes()),
        'capture_report': str(report_path), 'capture_report_sha256': sha(report_path.read_bytes()),
        'ordinary_unmodified_save_cold_boot_frames': 8400, 'normal_town_return_frame': 8400,
        'no_gameplay_fixtures_or_dialogue_injection': True,
        'initial_full_frame_and4MiB_match_prior_source': {'report': str(old_path), 'frame': 3200},
        'source_current_21_tagged_NPC_rows_sha256': sha(arm[table:table+length]),
        'all180_original_source_current_town_Guild_lookup_cases': all_towns,
        'Guild_availability_not_claimed_for_every_town': True,
        'four_original_buy_sell_lookup_and_speech_fragments': live,
        'actual_V783_COMMON1071_hold': {'frame': 7200, 'template_hex': entry.text.hex(),
            'resident_complete_block_sha256': sha(blocks[entry.block]), 'complete_native_glyphs': glyph,
            'formatted_hex': cstring(raw, wrapped_ptr).hex()},
        'original_cash_share_investment_growth_states': states,
        'company_fleet_ships_and_all_persistent_actors_towns_items_goods_preserved_after_cancel': True,
        'new_manuscript_prose_or_nominal_name_gameplay_approval': False,
        'full_Guild_diplomacy_branches_and_virtual_name_consumers_remain_pending': True,
        'source_executable_spans': [{'offsets': [lo, hi], 'sha256': sha(clean[lo:hi])} for lo, hi in source_spans],
        'producer_sha256': sha(Path(__file__).read_bytes()), 'full_goal_complete': False})
    print('Actual Guild role5/actor149 and old1071 complete hold;180 original source/current town mappings,four caller fragments and cancelled-item return pass. Revised prose and diplomacy gameplay remain pending.', flush=True)


if __name__ == '__main__':
    main()
