"""All8 original logical-role7 speech pipelines and complete native font planes."""
from copy import deepcopy
from pathlib import Path
from types import FunctionType
from PIL import Image, ImageDraw
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.duel_editorial import owned_entries
from dk4tool.patch.grand_race_menu_release import sha
from scripts.sea_responses_native_plan_v1556 import compiled
from scripts.probe_battle_aftermath_fonts_v1256 import consumer
from scripts.verify_personal_gameplay_v841 import get_machine
from scripts.verify_common_alignment_native_v257 import raster as original_raster
from scripts.verify_shipyard_gameplay_v760 import independent_font
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/sea_responses_fonts_v1558')
PLAN = Path('work/analysis/sea_responses_payload_v1556/native_payload_plan.json')
DOC = Path('translations/sea_responses_editorial_manuscript_v1.json')
BASE = 0x02000000


def assigned_role7_raw(arm, raw, actor_id, actor_object):
    cpu, get = get_machine(arm, raw)
    duty = get(0xCB1A8) + 0x2090
    assert get(0x82478, duty, 7) == 18
    slots = [slot for slot in range(31) if get(0x82BC4, duty, slot) == 18]
    assert slots == [9] and get(0x7EE08, actor_object) == actor_id
    get(0x82BB8, duty, 9, actor_id)
    assert get(0x82478, duty, 7) == actor_id
    changed = bytes(cpu.mem_read(BASE, 0x400000))
    addresses = [BASE + i for i, (a, b) in enumerate(zip(raw, changed, strict=True)) if a != b]
    assert addresses == [duty + 6 + 9]
    return changed, {'existing_actor_ID': actor_id, 'actor_object': actor_object, 'original_logical_role': 7,
        'original_setter': BASE + 0x82BB8, 'source_roster_slot': 9, 'only_one_original_roster_byte_changed': addresses,
        'raw_sha256': sha(changed), 'all_actor_objects_IDs_RNG_and_other4MiB_bytes_exact': True,
        'CPU_counterfactual_not_real_recruitment_or_live_gameplay': True}


if __name__ == '__main__':
    assert not ROOT.exists()
    plan, doc = read(PLAN), read(DOC)
    assert sha(DOC.read_bytes()) == plan['manuscript_sha256']
    context = read(doc['source_context'])
    assert sha(Path(doc['source_context']).read_bytes()) == doc['source_context_sha256']
    raw = Path(context['snapshot']).read_bytes()
    assert sha(raw) == context['snapshot_sha256']
    arm, common = Path(plan['target_ARM9']).read_bytes(), Path(plan['target_COMMON']).read_bytes()
    entries = owned_entries(common, arm, plan['directory_sha256'])
    current = NdsImage.open(doc['current_ROM'])

    class CurrentFont:
        @staticmethod
        def open(path):
            assert path == 'out/all_routes_combined_v255_candidate.nds'
            return current

    raster = FunctionType(original_raster.__code__, {**original_raster.__globals__, 'NdsImage': CurrentFont}, argdefs=original_raster.__defaults__)
    assert not any(raster(arm, b' ', 0x01FFCE40 - BASE, size=(228, 64), instruction_limit=2000000))
    source_arm = current.read_file('/__arm9__.bin')
    cpu, get = get_machine(source_arm, raw)
    captain = get(0x7F244)
    reps = {}
    for item in context['all207_existing_actor_choices']:
        if item['existing_actor_ID'] == captain:
            continue
        reps.setdefault(item['source_voice'], item)
        if item['existing_actor_ID'] in [18, 16]:
            reps[item['source_voice']] = item
    assert set(reps) == set(range(8)) and reps[0]['existing_actor_ID'] == 18
    ROOT.mkdir(parents=True)
    cases, findings, fixtures = [], [], []
    for row in doc['records']:
        n, value = row['message_id'], compiled(row)
        voice = n - 2209
        rep = reps[voice]
        assert rep['message_ID'] == n and entries[n].text == value
        if voice == 0:
            assigned, fixture = raw, None
        else:
            assigned, fixture = assigned_role7_raw(source_arm, raw, rep['existing_actor_ID'], rep['actor_object'])
            fixtures.append(fixture)
        native = consumer(arm, common, assigned, plan, 0x53D44, 7, row['source_table'])
        assert native['input_hex'] == value.hex() and native['parent'] == 0x02053DB8
        assert native['selector'] == 0x021186E0 and native['selector_offset'] == 0x27C
        formatted = bytes.fromhex(native['formatted_hex'])
        lines = [r.strip().decode('ascii') for r in formatted.split(b'\n')]
        assert ' '.join(lines) == row['english'] and 1 <= len(lines) <= 4
        assert all(0 < len(line) <= 35 and '  ' not in line for line in lines)
        events = []
        pixels = raster(arm, formatted, 0x01FFCE40 - BASE, size=(228, 64), instruction_limit=2000000, glyph_events=events)
        assert pixels == independent_font(arm, current.read_file('/GRP/KANJI.FNT'), lines)
        blank_guards = []
        for index, line in enumerate(lines):
            actual = [e for e in events if e['y'] == 16 * index and 6 <= e['x'] < 6 + 6 * len(line)]
            guards = []
            while actual and actual[0]['code'] == 32 and actual[0]['x'] == 6:
                guards.append(actual.pop(0))
            assert len(guards) <= 1 and (not guards or index > 0)
            blank_guards.append({'row': index, 'zero_ink_guard_events': guards})
            assert [e['code'] for e in actual] == list(line.encode('ascii'))
            assert [e['x'] for e in actual] == [6 + 6 * i for i in range(len(line))]
            assert actual[0]['x'] == 6 and actual[-1]['x'] + 6 <= 228
        issues = []
        if len(lines) > 1 and len(lines[-1].split()) == 1:
            issues.append('isolated-final-word')
        weak = [i for i, line in enumerate(lines[:-1]) if line.split()[-1].strip('.,!?;:').lower() in {'a', 'an', 'the', 'to', 'of', 'with', 'for', 'from', 'on', 'in', 'as', 'at', 'and', 'or'}]
        if weak:
            issues.append('weak-line-ending')
        path = ROOT / f'ID{n}_complete_native.png'
        Image.frombytes('L', (228, 64), bytes(0 if p else 255 for p in pixels)).save(path)
        case = {'message_ID': n, 'source_voice': voice, 'existing_actor_ID': rep['existing_actor_ID'], 'actor_object': rep['actor_object'],
            'CPU_only_role_fixture': fixture, 'compiled_hex': value.hex(), 'native_pipeline': native, 'lines': lines, 'findings': issues,
            'weak_line_end_indices': weak, 'full228x64_native_and_independent_font_exact': True,
            'complete_ordered_glyph_events': events, 'native_zero_ink_continuation_guards': blank_guards,
            'complete_first_final_letters_uniform6px_margins_bounds_and_blank_paper_pass': True,
            'whole_native_font_plane_sha256': sha(bytes(pixels)), 'preview': str(path), 'preview_sha256': sha(path.read_bytes()),
            'CPU_counterfactual_not_original_inspection_gameplay': True}
        cases.append(case)
        if issues:
            findings.append({k: case[k] for k in ['message_ID', 'lines', 'findings']})
    invalid = []
    base = doc['records'][0]
    for label, field, value in [('leading-space', 'english', ' ' + base['english']), ('trailing-space', 'english', base['english'] + ' '),
        ('internal-gap', 'english', 'A  creature!'), ('LF', 'english', 'A\ncreature!'), ('NUL', 'english', 'A\0creature!'),
        ('invented-printf', 'english', 'Look at %s!'), ('literal-percent', 'english', '100% ready!'),
        ('layout-markup', 'english', 'A creature! {LB}'), ('empty', 'english', ''), ('non-ASCII', 'english', 'A creature\u2014yes!'),
        ('unreviewed-long-contract', 'english', 'A' * 160), ('wrong-ID', 'message_id', 2208),
        ('invented-argument-count', 'native_argument_count', 1), ('invented-macro', 'source_native_macros', ['IC'])]:
        row = deepcopy(base)
        row[field] = value
        try:
            compiled(row)
        except (ValueError, AssertionError):
            invalid.append(label)
        else:
            raise AssertionError(label)
    sheet = Image.new('RGB', (936, 608), '#263238')
    draw = ImageDraw.Draw(sheet)
    for j, case in enumerate(cases):
        x, y = j % 2 * 468, j // 2 * 152
        draw.text((x + 5, y + 3), f'ID{case["message_ID"]} voice{case["source_voice"]}', fill='white')
        with Image.open(case['preview']) as preview:
            sheet.paste(preview.resize((456, 128), Image.Resampling.NEAREST), (x + 5, y + 22))
    path = ROOT / 'all8_creature_ghost_inspection_native_review.png'
    sheet.save(path)
    save(ROOT / 'native_font_research.json', {'manuscript': str(DOC), 'manuscript_sha256': sha(DOC.read_bytes()),
        'plan': str(PLAN), 'plan_sha256': sha(PLAN.read_bytes()), 'ARM9_sha256': sha(arm), 'COMMON_sha256': sha(common),
        'cases': cases, 'findings': findings, 'invalid_compiler_inputs_rejected': invalid,
        'all8_original_role7_selection_printf_macro_wrap_and_full_glyph_planes_verified': True,
        'all207_existing_actor_choices': context['all207_existing_actor_choices'], 'seven_CPU_only_role_counterfactuals': fixtures,
        'sheets_for_visual_review': [{'path': str(path), 'sha256': sha(path.read_bytes())}],
        'visual_review_copies_registered_release_and_original_inspection_pending': True,
        'producer_sha256': sha(Path(__file__).read_bytes()), 'full_goal_complete': False})
    print('All8 original role7/full font cases,7 one-byte CPU counterfactuals and14 compiler negatives pass;findings:', findings)
