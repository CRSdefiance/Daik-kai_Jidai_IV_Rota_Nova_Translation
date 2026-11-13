"""Every complete static/dynamic native font canvas for22 original speech entries."""
import struct
from pathlib import Path
from types import FunctionType

from PIL import Image, ImageDraw
from unicorn.arm_const import UC_ARM_REG_R0

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.native_call_abi_v764 import call
from scripts.prepare_product_pitches_v747 import native_layout as original_layout
from scripts.probe_button_prompt_native import BASE, STACK
from scripts.verify_arrival_native_v792 import prepared
from scripts.verify_common_alignment_native_v257 import raster as original_raster
from scripts.verify_shipyard_gameplay_v760 import independent_font
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/battle_declaration_v995b')
ROM = Path('out/all_routes_combined_v987_candidate.nds')
MANUSCRIPT = Path('translations/battle_declaration_editorial_manuscript_v2.json')
RUNTIME = Path('work/analysis/battle_declaration_v993c/native_runtime_verification.json')
ARM = Path('work/analysis/battle_declaration_v993b/ARM9_RUNTIME_RESEARCH_ONLY.bin')
GENERATED_TEMPLATES = {}


def robust_call(cpu, offset, args):
    return call(cpu, offset, args, instruction_limit=2000000)


native_layout = FunctionType(original_layout.__code__, {**original_layout.__globals__, 'call': robust_call},
                            argdefs=original_layout.__defaults__)


def main():
    assert not ROOT.exists()
    runtime = read(RUNTIME)
    arm = ARM.read_bytes()
    assert sha(arm) == runtime['research_ARM9_sha256']
    doc = read(MANUSCRIPT)
    rom = NdsImage.open(ROM)
    assert sha(ROM.read_bytes()) == doc['current_ROM_sha256'] == runtime['candidate_sha256']
    assert len(doc['records']) == 22 and all(not row['review']['formatting'] for row in doc['records'])
    context_path = Path(doc['native_context_proof'])
    assert sha(context_path.read_bytes()) == doc['native_context_proof_sha256']
    context = read(context_path)
    names = [{'kind': 'native-company-label', 'company_ID': r['company_ID'], 'label': r['complete_faction_label'],
              'hex': r['label_hex'], 'original_virtual_getter': r['virtual_name_getter']}
             for r in context['all20_native_complete_faction_labels']]
    assert len(names) == 20 and all(bytes.fromhex(r['hex']).decode('ascii') == r['label'] for r in names)
    names += [{'kind': 'synthetic-layout-stress-not-real-faction', 'company_ID': None, 'label': label,
               'hex': label.encode('ascii').hex(), 'original_virtual_getter': None}
              for label in ('A', 'ABCDEFGHIJKLMNOPQRSTUVW', 'Northern Compass Co.')]
    assert len(names) == 23
    class CurrentFont:
        @staticmethod
        def open(path):
            assert path == 'out/all_routes_combined_v255_candidate.nds'
            return rom
    raster = FunctionType(original_raster.__code__, {**original_raster.__globals__, 'NdsImage': CurrentFont},
                          argdefs=original_raster.__defaults__)
    ROOT.mkdir(parents=True)
    previews = ROOT/'previews'
    previews.mkdir()
    cases, findings, representative = [], [], []
    for row in doc['records']:
        n = row['message_id']
        assert row['english'].isascii() and row['english'] == ' '.join(row['english'].split())
        assert row['english'].count('%s') == row['native_argument_count']
        compiled = b' '+row['english'].encode('ascii')
        assert b'\n' not in compiled
        GENERATED_TEMPLATES[n] = {'english': row['english'], 'compiled_hex': compiled.hex(),
            'native_argument_count': row['native_argument_count'], 'one_paragraph_before_native_macro_and_wrap': True}
        variants = names if row['native_argument_count'] else [None]
        for index, value in enumerate(variants):
            cpu = prepared(arm)
            parent = 0x02053DB8 if row['source_family'] == 'ready' else 0x02053D24
            table = {'ready': 0x02117440, 'named': 0x02117420, 'unknown': 0x02117400}[row['source_family']]
            cpu.mem_write(STACK+0x27C, struct.pack('<I', table))
            expanded, lines = native_layout(cpu, compiled, n, (value['label'],) if value else (), parent=parent)
            if not value:
                assert b' '.join(expanded.split()) == b' '.join(compiled.split())
            expected = row['english'].replace('%s', value['label']) if value else row['english']
            assert ' '.join(lines) == expected
            assert 1 <= len(lines) <= 4 and max(map(len, lines)) <= 35
            # Full native byte consumption,NUL,input/view/bitmap guard and
            # whole-canvas independent-font equality test every leading,trailing
            # and interior glyph plus blank space at a uniform x6 cell origin.
            pixels = raster(arm, expanded, 0x01FFCE40-BASE, size=(228, 64), instruction_limit=2000000)
            assert pixels == independent_font(arm, rom.read_file('/GRP/KANJI.FNT'), lines)
            filename = previews/f'ID{n}_variant{index:02d}_complete_native.png'
            Image.frombytes('L', (228, 64), bytes(0 if v else 255 for v in pixels)).save(filename)
            orphan = len(lines) > 1 and len(lines[-1].split()) == 1
            weak = [i for i, line in enumerate(lines[:-1]) if line.split()[-1].strip('.,!?;:').lower() in {'a', 'an', 'the', 'to', 'of', 'with', 'for', 'from', 'on', 'in', 'as', 'at'}]
            case = {'message_id': n, 'source_family': row['source_family'], 'faction_name_case': value,
                'compiled_template_hex': compiled.hex(), 'native_formatted_hex': expanded.hex(),
                'generated_native_lines': lines, 'visible_widths': list(map(len, lines)),
                'complete_native_printf_dispatch_and_ABI_pass': True,
                'correct_original_wrapper_parent_and_source_table': [parent, table],
                'all_complete_words_and_source_substitution_preserved': True,
                'whole228x64_native_independent_font_and_input_bitmap_guards_pass': True,
                'all_line_cell_origins_x6_no_authored_indentation': True,
                'full_native_byte_consumption_and_all_leading_trailing_letters_pass': True,
                'single_word_final_row': orphan, 'weak_line_end_indices': weak,
                'preview': str(filename), 'preview_sha256': sha(filename.read_bytes()),
                'native_font_only_not_actual_UI_RGB_or_earned_scene': True}
            cases.append(case)
            if orphan or weak:
                findings.append({'case_index': len(cases)-1, 'message_ID': n, 'faction': value, 'lines': lines,
                                 'single_word_final_row': orphan, 'weak_line_end_indices': weak})
            if value is None or value['company_ID'] == 2:
                representative.append(case)
        print(f"ID{n}: {len(variants)} complete native font canvases;all glyphs,guards and bounds pass.", flush=True)
    assert len(cases) == 176 and len(GENERATED_TEMPLATES) == 22 and len(representative) == 22
    sheets = []
    for page in range(2):
        selected = representative[page*11:(page+1)*11]
        sheet = Image.new('RGB', (936, 912), '#263238')
        draw = ImageDraw.Draw(sheet)
        for index, case in enumerate(selected):
            x, y = index % 2*468, index // 2*152
            draw.text((x+5, y+3), f"ID{case['message_id']} {case['source_family']};native only", fill='white')
            with Image.open(case['preview']) as im:
                sheet.paste(im.resize((456, 128), Image.Resampling.NEAREST), (x+5, y+22))
        path = ROOT/f'all22_native_review_page{page+1}.png'
        sheet.save(path)
        sheets.append({'path': str(path), 'sha256': sha(path.read_bytes())})
    save(ROOT/'native_font_proof.json', {
        'candidate': str(ROM), 'candidate_sha256': sha(ROM.read_bytes()), 'research_ARM9': str(ARM), 'research_ARM9_sha256': sha(arm),
        'runtime_proof': str(RUNTIME), 'runtime_proof_sha256': sha(RUNTIME.read_bytes()),
        'manuscript': str(MANUSCRIPT), 'manuscript_sha256': sha(MANUSCRIPT.read_bytes()),
        'source_context': str(context_path), 'source_context_sha256': sha(context_path.read_bytes()),
        'cases': cases, 'complete_native_font_canvases': 176,
        'all7_templates_all20_native_faction_label_expansions': 140,
        'synthetic_odd_even_short_long_name_layout_stress_cases': 21,
        'all15_static_complete_native_font_cases': 15,
        'generated_paragraph_templates': GENERATED_TEMPLATES, 'all_leading_trailing_letters_uniform_cell_origins_and_bounds_pass': True,
        'line_boundary_findings_requiring_review': findings,
        'read_only_legacy_helper_adapter_changes_only_instruction_limit_to_standard2000000_and_full_ABI': True,
        'short_A_probe100000_instruction_budget_was_insufficient_native_completion_verified_with_standard_limit': True,
        'predecessor_failure': 'V995 prewrapped static1909 before the macro expander. I immediately before LF became native pronoun text. V995b compiles all22 as single paragraphs;original consumer wrapping happens after source macro processing. Named prompts retain the independently verified balancing path to prevent Co. or Fleet orphan tails. No native macro guard or source controls are changed.',
        'all22_input_templates_reject_authored_or_pregenerated_LF_before_macro_processing': True,
        'source_layout_helper_sha256': sha(Path('scripts/prepare_product_pitches_v747.py').read_bytes()),
        'source_font_renderer_sha256': sha(Path('scripts/verify_common_alignment_native_v257.py').read_bytes()),
        'source_independent_font_sha256': sha(Path('scripts/verify_shipyard_gameplay_v760.py').read_bytes()),
        'review_sheets': sheets, 'visual_review_pending': True,
        'native_copy_registered_repack_exact_patch_actual_scenes_and_geometry_pending': True,
        'completed_entries_added': 0, 'full_goal_complete': False,
        'producer_sha256': sha(Path(__file__).read_bytes())})
    print(f'176 complete native font canvases pass;{len(findings)} line-boundary findings require review before formatting approval. No playable ROM built.', flush=True)


if __name__ == '__main__':
    main()
