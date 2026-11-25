"""Record an original ordinary Tavern rumor hold; no new-ROM verification claim."""

import struct
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import common_message_entries
from scripts.verify_market_gameplay_v753 import snapshot
from scripts.verify_shipyard_gameplay_v760 import models
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/tavern_storage_v764')
REPORT = Path('E:/Rota Nova translations/Generated/work/emulation_v193/tavern_editorial_v764_drink_pilot_v762/capture_report.json')


def main():
    report = read(REPORT)
    assert report['cold_boot'] and not report['savestate_loaded'] and not report['callback_errors']
    assert report['frames'] == 6201 and not report['goal_complete'] and not report['hardware_device_verification']
    assert report['core_DLL_sha256'] == '42160dbfef89adfb3cfd975070a3047d8ad0979cead55607ebdfd3b931046c2b'
    assert report['ROM_sha256'] == read('out/editorial_review_latest.json')['sha256']
    assert not any(value for key, value in report.items() if key.startswith('synthetic_'))
    donor = report['battery_save_preloaded']
    assert donor['source_sha256'] == sha(Path(donor['source']).read_bytes()) == 'd991cb3bcdf74eed7aeb58c9a75957766b7c820d002423fd2b55cc8493cf8132'
    assert donor['source'] != donor['destination'] and donor['copied_byte_exact_before_cold_boot']
    rom = NdsImage.open(report['ROM']); arm = rom.read_file('/__arm9__.bin')
    entries = common_message_entries(rom.read_file('/COMMON/MESFILE.DK4'), arm, clean=False)
    raw = snapshot(report, 5000)
    def cstring(at): return raw[at - 0x02000000:at - 0x02000000 + 256].split(b'\0')[0]
    original, wrapped, cache = [struct.unpack_from('<I', arm, at)[0] for at in (0x5444C, 0x54450, 0x552A0)]
    assert cstring(cache + 0x2030) == entries[821].text
    assert cstring(original).strip().startswith(b'Hayreddin of Alexandria is an influential local Pirate.')
    capture = next(r for r in report['frames_captured'] if r['frame'] == 5000)
    assert sha(Path(capture['path']).read_bytes()) == capture['PNG_sha256']
    save(ROOT / 'actual_tavern_pilot_context.json', {'original_candidate': report['ROM'],
        'original_candidate_sha256': report['ROM_sha256'], 'capture_report': str(REPORT),
        'capture_report_sha256': sha(REPORT.read_bytes()), 'actual_message_ID': 821, 'held_frame': 5000,
        'exact_cached_original_template_hex': entries[821].text.hex(),
        'actual_printf_text_hex': cstring(original).hex(), 'actual_wrapped_text_hex': cstring(wrapped).hex(),
        'current_company_fleet_ship_models': models(arm, raw),
        'capture': capture, 'visually_inspected_original_rumor_hold': True,
        'no_synthetic_RAM_fixture_no_savestate': True,
        'scope': 'Ordinary V762 Order Drink pilot with a protected battery-save copy,followed by an original Hodram/barmaid sequence. No revised dialogue or V765 scene verification claimed.',
        'producer_sha256': sha(Path(__file__).read_bytes())})
    print('Original V762 Tavern821 hold confirmed by resident template,printf/wrap buffers and visible framebuffer;no fixture.', flush=True)


if __name__ == '__main__': main()
