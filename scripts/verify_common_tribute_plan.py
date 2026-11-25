"""Validate both native tribute paths against final component/repack outputs."""

import json
from pathlib import Path

from dk4tool.patch.common_tribute_release import transform
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.probe_common_display_name_autoload import execute as autoload
from scripts.probe_common_itcm_arena_reservation import initialize
from scripts.probe_common_monthly_word_wrap_hook import caller_frame
from scripts.probe_common_tribute_loaded_copy import execute as town
from scripts.probe_common_tribute_modal_pixels import verify as pixels


def main():
    rom = NdsImage.open('out/all_routes_combined_v142_candidate.nds')
    source = rom.read_file('/__arm9__.bin')
    document = json.loads(Path('translations/common_tribute_repairs_manuscript_v2.json').read_text(encoding='utf-8'))
    component = json.loads(Path('translations/common_tribute_runtime_component_v1.json').read_text(encoding='utf-8'))
    result = transform(rom.read_file('/COMMON/MESFILE.DK4'), source, document, component)
    names = (b'Fleet', b'Indigo', b'F' * 18, b'I' * 18, 'あ'.encode('cp932') * 9, b'Fleet  Group')
    warm = [town(result.arm9, result.common, name, index, word_wrapped=True)
            for name in names for index in range(32)]
    cold = [town(result.arm9, result.common, name, index, word_wrapped=True, cold_cache=True)
            for name in names for index in (0, 31)]
    monthly = [caller_frame(result.arm9, result.common, index) for index in range(8)]
    font = rom.read_file('/GRP/KANJI.FNT')
    rendered = []
    for portrait, cases in ((False, warm), (True, monthly)):
        texts = list(dict.fromkeys(c['complete_prepared_text'] for c in cases))
        for text in texts:
            for mode in (4, 16):
                native = pixels(source, font, text, mode, guarded=True, portrait=portrait)
                rendered.append({'portrait': portrait, 'mode': mode, 'text': text,
                                 'pixels_sha256': sha(native['pixels'])})
    arena = initialize(result.arm9)
    if arena['low'][3] != component['reserved_arena_low']:
        raise ValueError('Final tribute repack loses resident arena reservation')
    report = {'status': 'pass-final-packed-tribute-native-regression-gameplay-pending',
              'final_common_sha256': sha(result.common), 'final_arm9_sha256': sha(result.arm9),
              'all_native_entries_compared': len(result.entries), 'warm_town_cases': warm,
              'cold_town_cases_with_host_file_contract': cold, 'monthly_cases': monthly,
              'native_pixels': rendered, 'arena': arena, 'autoload': autoload(result.arm9),
              'limitations': 'Warm lookup, formatting and wrapping run against exact final repack. Monthly initial widget construction and actor resolution, cold-cache host file reads, bitmap origin/routing, hardware cache, physical portrait composition and input remain contracts. Native raster is a separate invocation. Cold-boot gameplay remains pending.'}
    Path('work/analysis/common_tribute_final_native_proof.json').write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(f'Final packed outputs pass: {len(warm)} warm town, {len(cold)} cold town, {len(monthly)} monthly and {len(rendered)} native pixel cases.')


if __name__ == '__main__':
    main()
