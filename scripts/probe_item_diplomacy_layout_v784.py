"""Direct existing-formatter prototypes; no new selector/provider approval."""

import struct
from itertools import product
from pathlib import Path

from PIL import Image, ImageDraw
from unicorn.arm_const import UC_ARM_REG_R0

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.context_item_diplomacy_v784 import ROOT, CURRENT
from scripts.review_item_diplomacy_v784 import MANUSCRIPT, TYPE_PHRASES
from scripts.native_call_abi_v764 import call
from scripts.native_machine_scoped_v764 import machine
from scripts.probe_tavern_continuation_layout_v768 import format_case
from scripts.verify_common_alignment_native_v257 import raster
from scripts.verify_shipyard_gameplay_v760 import independent_font
from scripts.verify_village_wrap_v608 import read, save

OUT = ROOT/'layout_prototypes'


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    rom = NdsImage.open(CURRENT)
    arm = rom.read_file('/__arm9__.bin')
    doc = read(MANUSCRIPT)
    context = read(ROOT/'native_context.json')
    raw = Path(context['pre_fixture_snapshot']['path']).read_bytes()
    assert sha(raw) == context['pre_fixture_snapshot']['sha256']
    u = machine(arm)
    u.mem_write(0x02000000, raw)

    def get(fn, args=()):
        call(u, fn, args)
        return u.reg_read(UC_ARM_REG_R0)

    def ptr(at): return struct.unpack('<I', u.mem_read(at, 4))[0]
    def text(at): return bytes(u.mem_read(at, 256)).split(b'\0')[0]

    company_store = get(0xCB160)
    names = []
    for i in range(20):
        obj = company_store+4+i*76
        name = text(get(ptr(ptr(obj)+8)-0x02000000, (obj,)))
        assert name and name.isascii()
        names.append({'index': i, 'name_hex': name.hex(), 'name': name.decode('ascii')})
    companies = sorted({bytes.fromhex(r['name_hex']) for r in names})
    numbers = sorted({text(get(0xABF50, (i,))) for i in (1, 9, 10, 99, 100, 999, 1000, 9999, 99999, 999999, 2147483647)})
    phrases = [s.encode('ascii') for s in TYPE_PHRASES]
    save(OUT/'supplied_values.json', {'current_native_company_names': names,
        'company_catalog_bound': 'Original diplomatic candidate loops use indices0-19;slot20 is an empty sentinel,not a named faction.',
        'current_native_numeric_strings_hex': [n.hex() for n in numbers],
        'DRAFT_English_type_phrase_values': TYPE_PHRASES,
        'these_type_phrases_are_not_current_getter_output': True,
        'no_claim_every_supplied_pair_or_numeric_bound_is_eligible_or_earned': True})
    cases, findings, previews = [], [], []
    for row in doc['records']:
        n = row['message_id']
        if n in (1072, 1073, 1083, 1086, 1095): values = ((s,) for s in numbers)
        elif 1098 <= n <= 1102: values = ((s,) for s in phrases)
        elif 1108 <= n <= 1112: values = product(companies, companies)
        elif 1113 <= n <= 1116: values = product(companies, phrases)
        elif 1138 <= n <= 1145: values = ((s,) for s in companies)
        else: values = [()]
        local = []
        for i, args in enumerate(values):
            if i % 64 == 0:
                cpu = machine(arm)
            result = format_case(cpu, row, args)
            cases.append(result)
            local.append(result)
            if result['findings']:
                findings.append(result)
        previews.append(max(local, key=lambda c: (len(c['lines']), len(bytes.fromhex(c['formatted_hex'])))))
    save(OUT/'native_layout_matrix.json', {'count': len(cases), 'cases': cases,
        'findings_count': len(findings), 'findings': findings,
        'direct_existing_literal_formatter_prototype_not_production_dispatch': True})
    if findings:
        print(f'{len(cases)} prototype layouts;{len(findings)} findings. No formatting approvals or release changes.', flush=True)
        for f in findings[:12]:
            print(f['id'], f['findings'], f['lines'], flush=True)
        return
    fonts = []
    for row in previews:
        plane = raster(arm, bytes.fromhex(row['formatted_hex']), 0x01FFCE40-0x02000000,
                       size=(228, 64), instruction_limit=1000000)
        assert plane == independent_font(arm, rom.read_file('/GRP/KANJI.FNT'), row['lines'])
        path = OUT/f'complete_font_ID{row["id"]}.png'
        Image.frombytes('L', (228, 64), bytes(0 if p else 255 for p in plane)).save(path)
        fonts.append({**row, 'path': str(path), 'sha256': sha(path.read_bytes()), 'full_independent_native_font_exact': True})
    sheets = []
    for start in range(0, len(fonts), 12):
        sheet = Image.new('RGB', (1428, 720), '#30343c')
        draw = ImageDraw.Draw(sheet)
        for i, row in enumerate(fonts[start:start+12]):
            x, y = i % 3*476, i // 3*180
            draw.text((x+5, y+4), f'RESEARCH ONLY ID{row["id"]}', fill='white')
            sheet.paste(Image.open(row['path']).convert('RGB').resize((456, 128), Image.Resampling.NEAREST), (x+5, y+24))
        path = OUT/f'complete_fonts_{start//12:02d}_2x.png'
        sheet.save(path)
        sheets.append({'path': str(path), 'sha256': sha(path.read_bytes())})
    save(OUT/'verification.json', {'candidate_sha256': sha(CURRENT.read_bytes()),
        'manuscript_sha256': sha(MANUSCRIPT.read_bytes()), 'complete_native_layouts': len(cases),
        'all76_IDs': [r['id'] for r in fonts], 'complete_font_planes': fonts, 'preview_sheets': sheets,
        'type_phrases_are_explicit_proposed_inputs_not_current_getter_output': True,
        'direct_existing_formatter_only_not_new_dispatch_provider_or_gameplay_approval': True,
        'visual_review_pending': True, 'no_ROM_change': True,
        'producer_sha256': sha(Path(__file__).read_bytes()), 'full_goal_complete': False})
    print(f'{len(cases)} prospective layouts and76 full independent font planes pass;visual review and production gates remain.', flush=True)


if __name__ == '__main__':
    main()
