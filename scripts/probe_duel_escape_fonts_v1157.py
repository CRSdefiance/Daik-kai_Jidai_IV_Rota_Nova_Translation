"""All original compact actor labels and legal-name stress in escape speech."""
import struct
from pathlib import Path
from types import FunctionType
from PIL import Image, ImageDraw
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.duel_editorial_layout_v1155 import compiled, ESCAPE_IDS
from scripts.probe_reinforcement_sniping_layout_v1030 import native_layout
from scripts.verify_arrival_native_v792 import prepared
from scripts.verify_common_alignment_native_v257 import raster as original_raster
from scripts.verify_shipyard_gameplay_v760 import independent_font
from scripts.verify_personal_gameplay_v841 import get_machine
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/duel_escape_fonts_v1157')
MANUSCRIPT = Path('translations/duel_editorial_manuscript_v3.json')


def main():
    assert not ROOT.exists()
    runtime_path = Path('work/analysis/duel_escape_runtime_v1153/runtime_plan.json')
    runtime, doc = read(runtime_path), read(MANUSCRIPT)
    arm = Path(runtime['research_ARM9']).read_bytes()
    assert sha(arm) == runtime['research_ARM9_sha256']
    verifier = read('work/analysis/duel_escape_runtime_v1154/native_runtime_verification.json')
    assert verifier['research_ARM9_sha256'] == sha(arm)
    catalog = read('work/analysis/duel_scope_names_v1117b/source_name_layout_catalogue.json')
    raw = Path(catalog['snapshot']).read_bytes()
    assert sha(raw) == catalog['snapshot_sha256']
    rom = NdsImage.open('out/all_routes_combined_v1105_candidate.nds')
    assert sha(Path('out/all_routes_combined_v1105_candidate.nds').read_bytes()) == catalog['candidate_sha256']
    kanji = rom.read_file('/GRP/KANJI.FNT')
    cpu, get = get_machine(arm, raw)
    variants = []
    for row in catalog['names']:
        actor = row['object']
        vtable = struct.unpack('<I', cpu.mem_read(actor, 4))[0]
        getter = struct.unpack('<I', cpu.mem_read(vtable+0x20, 4))[0]
        pointer = get(getter-0x02000000, actor)
        name = bytes(cpu.mem_read(pointer, 64)).split(b'\0')[0]
        assert name and len(name) <= 18
        variants.append({'kind': 'source-compact-actor-getter20', 'slot': row['actor_slot'],
            'actor_ID': row['actor_ID'], 'object': actor, 'getter': getter, 'name_hex': name.hex()})
    assert len(variants) == 208
    matrix = read('work/analysis/duel_native_layout_v1134/compiled_native_DP_matrix.json')
    challenge = next(r['english'].encode('ascii') for r in doc['records'] if r['message_id'] == 1931)
    prefix, suffix = challenge.split(b'%s')
    for case in matrix['cases']:
        if case['message_ID'] != 1931 or case['kind'] != 'legal-name-stress':
            continue
        text = bytes.fromhex(case['input_hex'])
        assert text.startswith(prefix) and text.endswith(suffix)
        name = text[len(prefix):-len(suffix)]
        variants.append({'kind': 'legal-name-stress', 'name_hex': name.hex()})
    assert len(variants) == 235

    class CurrentFont:
        @staticmethod
        def open(path):
            assert str(path) == 'out/all_routes_combined_v255_candidate.nds'
            return rom

    raster = FunctionType(original_raster.__code__, {**original_raster.__globals__, 'NdsImage': CurrentFont},
                          argdefs=original_raster.__defaults__)
    ROOT.mkdir(parents=True)
    results, findings, previews, cache = [], [], [], {}
    for row in doc['records']:
        number = row['message_id']
        if number not in ESCAPE_IDS:
            continue
        text = compiled(row)
        table = 0x02117500 if number < 1973 else 0x02117620
        selected = variants if row['native_argument_count'] else [None]
        for index, variant in enumerate(selected):
            name = bytes.fromhex(variant['name_hex']) if variant else None
            formatted, lines = native_layout(prepared(arm), text, number, name, table)
            assert ' '.join(lines) == row['english'].replace('%s', name.decode('cp932')) if name else ' '.join(lines) == row['english']
            assert all(line == line.strip() and '  ' not in line for line in lines)
            if formatted not in cache:
                pixels = raster(arm, formatted, 0x01FFCE40-0x02000000, size=(228, 64), instruction_limit=2000000)
                assert pixels == independent_font(arm, kanji, lines)
                cache[formatted] = pixels
            pixels = cache[formatted]
            weak = [i for i, line in enumerate(lines[:-1]) if line.split()[-1].strip('.,!?;:').lower()
                    in {'a', 'an', 'the', 'to', 'of', 'with', 'for', 'from', 'on', 'in', 'as', 'at', 'and'}]
            orphan = len(lines) > 1 and (len(lines[-1].split()) == 1 or len(lines[-1].encode('cp932')) <= 8)
            result = {'message_ID': number, 'variant': variant, 'compiled_hex': text.hex(),
                'formatted_hex': formatted.hex(), 'lines': lines,
                'cell_widths': [len(line.encode('cp932')) for line in lines],
                'whole228x64_native_independent_font_and_neighbor_guards_exact': True,
                'all_leading_trailing_name_bytes_and_uniform_x6_row_origins_complete': True,
                'source_printf_postmacro_wrap_and_full_stack_register_ABI_pass': True,
                'weak_line_end_indices': weak, 'short_or_orphan_final_row': orphan,
                'complete_native_font_SHA256': sha(pixels), 'not_actual_gameplay': True}
            results.append(result)
            if weak or orphan:
                findings.append({'case_index': len(results)-1, **result})
            if variant is None or index in (0, 20, 28, 186, 208, 223, 234):
                path = ROOT/f'ID{number}_variant{index:03d}.png'
                Image.frombytes('L', (228, 64), bytes(0 if v else 255 for v in pixels)).save(path)
                previews.append({'message_ID': number, 'variant_index': index,
                    'path': str(path), 'sha256': sha(path.read_bytes()), 'lines': lines})
        print(f'ID{number}: {len(selected)} native escape expansion/font cases pass', flush=True)
    assert len(results) == 1417 and {r['message_ID'] for r in results} == set(ESCAPE_IDS)
    sheets = []
    for page, start in enumerate(range(0, len(previews), 12)):
        sheet = Image.new('RGB', (936, 912), '#263238')
        draw = ImageDraw.Draw(sheet)
        for i, row in enumerate(previews[start:start+12]):
            x, y = i % 2*468, i//2*152
            draw.text((x+5, y+3), f"ID{row['message_ID']} variant{row['variant_index']}; CPU font research", fill='white')
            with Image.open(row['path']) as im:
                sheet.paste(im.resize((456, 128), Image.Resampling.NEAREST), (x+5, y+22))
        path = ROOT/f'escape_review_page{page+1}.png'
        sheet.save(path)
        sheets.append({'path': str(path), 'sha256': sha(path.read_bytes())})
    proof = ROOT/'native_escape_fonts.json'
    save(proof, {'runtime_plan': str(runtime_path), 'runtime_plan_sha256': sha(runtime_path.read_bytes()),
        'ARM9_sha256': sha(arm), 'manuscript': str(MANUSCRIPT), 'manuscript_sha256': sha(MANUSCRIPT.read_bytes()),
        'all208_original_virtual_compact_getters_and27_legal_name_stress_variants': variants,
        'source_catalog_includes_NPC_labels_as_additional_stress_not_claimed_actual_duel_participants':True,
        'cases': results, 'complete_font_cases': len(results), 'unique_font_planes': len(cache),
        'review_sheets': sheets, 'previews': previews, 'findings_requiring_review': findings,
        'compiler_owned_leading_state_for_shared_speech_and_one_paragraph_before_macro': True,
        'original_table_dispatch_printf_wrap_and_ASCII_CP932_painters_execute': True,
        'not_actual_duel_playback_or_registered_ROM': True, 'visual_review_pending': True,
        'all33_formatting_gates_still_false': True, 'no_completion_credit': True,
        'producer_sha256': sha(Path(__file__).read_bytes()), 'full_goal_complete': False})
    path = Path('translations/editorial_review_current_v1.json')
    ledger = read(path)
    assert ledger['records_editorially_completed'] == 1196 and ledger['records_with_source_and_prose_pass'] == 1267
    ledger['duel_prose_v1103'].update(escape_native_fonts=str(proof),
        escape_boundary_findings=len(findings), formatting_status='resident-duel-and-escape-native-fonts-pass;visual-review-and-integration-actual-open')
    save(path, ledger)
    print(f'1417 escape font cases, {len(cache)} distinct planes; {len(findings)} boundary findings for review.', flush=True)


if __name__ == '__main__':
    main()
