"""Original eight-voice/two-argument pipelines and complete ordered font planes."""
import struct
from copy import deepcopy
from pathlib import Path
from types import FunctionType
from PIL import Image, ImageDraw
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.duel_editorial import owned_entries
from dk4tool.patch.grand_race_menu_release import sha
from scripts.search_reports_native_plan_v1661 import compiled, IDS
from scripts.search_reports_native_consumers_v1662 import speech, loss, assigned_role
from scripts.verify_personal_gameplay_v841 import get_machine
from scripts.verify_common_alignment_native_v257 import raster as original_raster
from scripts.verify_shipyard_gameplay_v760 import independent_font
from scripts.probe_inspection_status_fonts_v1574 import literal_independent
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/search_reports_fonts_v1663')
PLAN = Path('work/analysis/search_reports_payload_v1661/native_payload_plan.json')
DOC = Path('translations/search_reports_editorial_manuscript_v1.json')
RAW = Path('E:/Rota Nova translations/Generated/work/emulation_v193/hot_spring_crew_v1651_1637/frame_026531_arm9_ram.bin')
BASE = 0x02000000
PAIRS = [(0, 0), (1, 9), (9, 10), (10, 99), (99, 100), (100, 999), (999, 1000),
         (1000, 9999), (9999, 65535), (65535, 99999), (100000, 2147483647),
         (2147483647, 1), (35, 105), (140, 105), (70, 35)]
AMOUNTS = [0, 1, 9, 10, 12, 99, 100, 999, 1000, 9999, 65535, 99999, 100000, 2147483647]

if __name__ == '__main__':
    assert not ROOT.exists()
    plan, doc = read(PLAN), read(DOC)
    assert plan['manuscript_sha256'] == sha(DOC.read_bytes())
    arm, common = Path(plan['target_ARM9']).read_bytes(), Path(plan['target_COMMON']).read_bytes()
    rom, raw = NdsImage.open(doc['current_ROM']), RAW.read_bytes()
    source_arm = rom.read_file('/__arm9__.bin')
    entries = owned_entries(common, arm, plan['directory_sha256'])
    rows = {r['message_id']: r for r in doc['records']}
    class CurrentFont:
        @staticmethod
        def open(path): return rom
    raster = FunctionType(original_raster.__code__, {**original_raster.__globals__, 'NdsImage': CurrentFont}, argdefs=original_raster.__defaults__)
    assert not any(raster(arm, b' ', 0x01FFCE40-BASE, size=(228, 64), instruction_limit=2000000))
    cpu, get = get_machine(source_arm, raw)
    actors, captain = get(0xCB184), get(0x7F244)
    ROOT.mkdir(parents=True)
    cases, findings, choices, previews = [], [], [], []

    def check(n, native, voice=None, fixture=None):
        row = rows[n]
        value = compiled(row)
        assert entries[n].text == value
        assert native.get('input_hex', native.get('loaded_template_hex')) == value.hex()
        expected = value
        for argument in native['source_ABF50_argument_hex']:
            expected = expected.replace(b'%s', bytes.fromhex(argument), 1)
        formatted = bytes.fromhex(native['formatted_hex'])
        lines = [line.strip().decode('cp932') for line in formatted.split(b'\n')]
        assert ' '.join(lines).encode('cp932') == expected
        assert 1 <= len(lines) <= (1 if n == 312 else 4)
        assert all(0 < len(line.encode('cp932')) <= 35 and '  ' not in line for line in lines)
        events = []
        pixels = raster(arm, formatted, 0x01FFCE40-BASE, size=(228, 64), instruction_limit=2000000, glyph_events=events)
        independent = literal_independent(arm, rom.read_file('/GRP/KANJI.FNT'), lines[0]) if n == 312 else independent_font(arm, rom.read_file('/GRP/KANJI.FNT'), lines)
        assert pixels == independent, (n, voice, native['source_amounts'], lines)
        guards = []
        for row_index, line in enumerate(lines):
            actual = [e for e in events if e['y'] == row_index*16]
            pos, x = 0, 0 if n == 312 else 6
            for char_index, char in enumerate(line):
                encoded = char.encode('cp932')
                code = int.from_bytes(encoded, 'big')
                if code != 32 and actual[pos]['code'] == 32 and actual[pos]['x'] == x:
                    assert len(encoded) == 2 or (row_index > 0 and char_index == 0)
                    guards.append(actual[pos]);pos += 1
                assert actual[pos]['code'] == code and (actual[pos]['x'], actual[pos]['y']) == (x, row_index*16), (n, voice, char, actual[pos])
                pos += 1;x += 6*len(encoded)
            assert x <= 228
            assert all(e['code'] == 32 for e in actual[pos:])
        issues = []
        if len(lines) > 1 and len(lines[-1].split()) == 1: issues.append('isolated-final-word')
        weak = [i for i, line in enumerate(lines[:-1]) if line.split()[-1].strip('.,!?;:').lower() in {'a','an','the','to','of','with','for','from','on','in','as','at','and','or'}]
        if weak: issues.append('weak-line-ending')
        path = ROOT/f'case_{len(cases):03d}_ID{n}_complete_native.png'
        Image.frombytes('L', (228,64), bytes(0 if p else 255 for p in pixels)).save(path)
        case = {'message_ID': n, 'source_voice': voice, 'CPU_role_fixture': fixture, 'compiled_hex': value.hex(),
                'native_pipeline': native, 'lines': lines, 'findings': issues, 'weak_line_end_indices': weak,
                'all_ordered_complete_native_glyph_events': events, 'zero_ink_phase_guards': guards,
                'full228x64_native_and_independent_ink_shadow_planes_equal': True,
                'complete_leading_trailing_letters_source_quantities_margins_bounds_and_blank_paper_verified': True,
                'native_origin_x': 0 if n == 312 else 6, 'preview': str(path), 'preview_sha256': sha(path.read_bytes()),
                'native_font_plane_sha256': sha(bytes(pixels)), 'CPU_only_not_gameplay': True}
        cases.append(case)
        if issues: findings.append({k: case[k] for k in ['message_ID','source_voice','lines','findings','weak_line_end_indices']})
        if n == 312 or not native['source_amounts'] or native['source_amounts'] in [[35,105],[100000,2147483647]]:
            previews.append(case)

    for role, table in [(1, 0x02116EC0), (7, 0x02116E80)]:
        members = struct.unpack_from('<8i', source_arm, table-BASE)
        reps = {}
        for actor_id in range(207):
            actor = actors+0x19E4 if actor_id == captain else actors+4+32*actor_id
            voice, n = get(0x7E988, actor), get(0x53F4C, actor, table)
            assert n == (members[voice] if members[voice] >= 0 else members[0])
            choices.append({'role':role,'table':table,'actor_ID':actor_id,'source_voice':voice,'message_ID':n,'original_minus1_fallback':members[voice]<0})
            if actor_id != captain: reps.setdefault(voice, (actor_id, actor, n))
        assert set(reps) == set(range(8))
        for voice, (actor_id, actor, n) in sorted(reps.items()):
            assigned, fixture = assigned_role(source_arm, raw, role, actor_id, actor)
            for values in PAIRS if role == 7 else [()]:
                check(n, speech(arm, common, assigned, plan, role, table, values), voice, fixture)
    for amount in AMOUNTS:
        check(312, loss(arm, common, raw, plan, amount))
    assert {c['message_ID'] for c in cases} == set(IDS) and len(cases) == 142 and len(choices) == 414
    invalid = []
    for label, field, value in [('leading','english',' Lost %s sailors.'),('trailing','english','Lost %s sailors. '),
        ('gap','english','Lost  %s sailors.'),('LF','english','Lost\n%s sailors.'),('NUL','english','Lost\0%s sailors.'),
        ('brace','english','Lost %s sailors. {LB}'),('nonASCII','english','Lost %s sailors—oh.'),('extra-conversion','english','Lost %s %s sailors.'),
        ('wrong-conversion','english','Lost %d sailors.'),('missing-conversion','english','Lost sailors.'),('literal-percent','english','Lost %s sailors,10%.'),
        ('long','english','A'*159+'%s'),('wrong-ID','message_id',311),('argc','native_argument_count',0),('macro','source_native_macros',['IC']),
        ('role','source_role',1),('table','source_table',0x02116EC0)]:
        row = deepcopy(doc['records'][0]);row[field] = value
        try: compiled(row)
        except (ValueError, AssertionError): invalid.append(label)
        else: raise AssertionError(label)
    sheet = Image.new('RGB', (936, 152*((len(previews)+1)//2)), '#263238')
    draw = ImageDraw.Draw(sheet)
    for j, case in enumerate(previews):
        x,y=j%2*468,j//2*152
        draw.text((x+5,y+3),f'ID{case["message_ID"]} voice{case["source_voice"]} {case["native_pipeline"]["source_amounts"]}',fill='white')
        with Image.open(case['preview']) as preview: sheet.paste(preview.resize((456,128), Image.Resampling.NEAREST),(x+5,y+22))
    path = ROOT/'Search_reports_native_review.png';sheet.save(path)
    save(ROOT/'native_font_research.json', {'manuscript':str(DOC),'manuscript_sha256':sha(DOC.read_bytes()),'plan':str(PLAN),'plan_sha256':sha(PLAN.read_bytes()),
        'source_snapshot':str(RAW),'source_snapshot_sha256':sha(raw),'ARM9_sha256':sha(arm),'COMMON_sha256':sha(common),
        'cases':cases,'all414_existing_actor_selections':choices,'findings':findings,'invalid_compiler_inputs_rejected':invalid,
        'all16_voice_table_combinations_plus_numeric_boundary_pairs_verified':True,
        'sheets_for_visual_review':[{'path':str(path),'sha256':sha(path.read_bytes())}],
        'visual_review_copies_release_and_original_revised_gameplay_pending':True,'producer_sha256':sha(Path(__file__).read_bytes()),'full_goal_complete':False})
    print(f'142 native/independent complete font cases,414 actor choices,17 compiler negatives;layout findings:{findings}')
