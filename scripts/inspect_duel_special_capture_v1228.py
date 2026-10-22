"""Read-only actual special fonts, full RGB crops and original actor bindings."""
import argparse
import struct
from pathlib import Path
from PIL import Image
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.duel_special_editorial import current_entries
from scripts.duel_special_dispatch_v1217 import IDS
from scripts.verify_duel_actual_holds_v1171 import actual_widget
from scripts.verify_personal_gameplay_v841 import get_machine
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/duel_special_actual_v1228')
CAP = Path('E:/Rota Nova translations/Generated/work/emulation_v193/duel_special_v1225_1224')
ROM = Path('out/all_routes_combined_v1224_candidate.nds')
BASE = 0x02000000


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--through', type=int, required=True)
    args = parser.parse_args()
    target = ROOT/f'scan_through{args.through}.json'
    assert not target.exists()
    rom = NdsImage.open(ROM)
    arm, common = rom.read_file('/__arm9__.bin'), rom.read_file('/COMMON/MESFILE.DK4')
    entries = current_entries(common, arm)
    native = read('work/analysis/duel_special_native_v1219b/native_font_scope_verification.json')
    assert native['ARM9_sha256'] == sha(arm) and native['COMMON_sha256'] == sha(common)
    by_sha = {c['source_208x36_4bit_SHA256']: c for c in native['cases'] if c['message_ID'] in IDS}
    doc = {r['message_id']: r for r in read('translations/duel_special_editorial_manuscript_v2.json')['records']}
    cases, holds, scanned, states = [], [], [], []
    owner = struct.unpack_from('<I', arm, 0x552A0)[0]
    for path in sorted(CAP.glob('frame_*_arm9_ram.bin')):
        frame = int(path.name.split('_')[1])
        if frame < 5782 or frame > args.through:
            continue
        image_path = CAP/f'frame_{frame:06d}_navigation.png'
        if not image_path.exists():
            continue
        raw = path.read_bytes()
        assert len(raw) == 0x400000
        scanned.append({'frame': frame, 'RAM_sha256': sha(raw)})
        cpu, get = get_machine(arm, raw)
        actors = get(0xCB184)
        states.append({'frame': frame, 'own_enemy_HP': [get(0x7E19C, p) for p in (actors+0x19E4, actors+4+32*32)]})
        try:
            widget, controller, header, h = actual_widget(raw)
        except AssertionError:
            continue
        assert h[:3] == (4, 52, 36) and h[4] == 40
        packed = raw[header-BASE+40:header-BASE+40+3744]
        pixels = bytes((v>>shift)&15 for v in packed for shift in (0, 4))
        case = by_sha.get(sha(pixels))
        if not case:
            continue
        n = case['message_ID']
        image = Image.open(image_path).convert('RGB')
        objects = list(struct.unpack('<2I', cpu.mem_read(controller+0x34, 8)))
        actor_ids = [get(0x7EE08, a) for a in objects]
        assert actor_ids == [1, 32]
        assert doc[n]['source_actor_ID'] == 1, 'Only original Hodram special is expected in this fixture'
        assert raw[0x535E8:0x53628] == arm[0x535E8:0x53628]
        assert raw[0xDAF0:0xDB5C] == arm[0xDAF0:0xDB5C]
        mismatch = 0
        for row in range(3):
            for y in range(12):
                for x in range(144):
                    expected = (0,8,0) if pixels[(row*12+y)*208+x] else (255,255,255)
                    mismatch += image.getpixel((56+x,212+row*20+y)) != expected
        last = raw[owner-BASE+0x2030:owner-BASE+0x2230].split(b'\0')[0]
        cached_component = raw[owner-BASE+0x30:owner-BASE+0x30+1480]
        resident = sha(cached_component) == '64474a4c40ba1aeb655be68297ca676e79b9b090760b83e46dbb50140a3e7aac'
        record = {'message_ID': n, 'frame': frame, 'source_actor_IDs': actor_ids,
            'speaker_source_side': 0, 'original_D4D0_binding': doc[n]['source_call_return'],
            'whole208x36_native_font_plane_sha256': sha(pixels), 'lines': case['lines'],
            'source_widget': widget, 'source_controller': controller,
            'RAM': str(path), 'RAM_sha256': sha(raw), 'capture': str(image_path),
            'capture_sha256': sha(image_path.read_bytes()),
            'actual_visible_three144x12_crops_exact': mismatch == 0, 'RGB_mismatch_pixels': mismatch,
            'unchanged1480byte_PIC_is_resident': resident,
            'last_native_copy_is_carrier1931': last == entries[1931].text,
            'last_native_copy_hex': last.hex()}
        cases.append(record)
        if mismatch == 0:
            holds.append(record)
    ROOT.mkdir(parents=True, exist_ok=True)
    save(target, {'candidate': str(ROM), 'candidate_sha256': sha(ROM.read_bytes()),
        'through': args.through, 'scanned_RAM_frames': scanned, 'native_bitmap_match_candidates': cases,
        'complete_visible_holds': holds, 'visible_message_IDs': sorted({r['message_ID'] for r in holds}),
        'original_HP_evolution': states,
        'persisting_bitmap_without_matching_RGB_is_not_visible_activation': True,
        'source_geometry_full_ink_and_blank_masks_not_fitted_to_letters': True,
        'read_only_no_emulator_input_or_state_changes': True, 'no_editorial_completion_credit': True,
        'producer_sha256': sha(Path(__file__).read_bytes()), 'full_goal_complete': False})
    print('Scanned',len(scanned),'frames;visible special IDs',sorted({r['message_ID'] for r in holds}),
          'complete visible holds',len(holds),'latest HP',states[-1:] if states else [],flush=True)


if __name__ == '__main__':
    main()
