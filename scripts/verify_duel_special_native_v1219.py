"""Source D4D0 special calls, resident PIC, complete native fonts and crops.

CPU research only. File I/O, SDK clear, UI registration, GPU submission and
hardware cache effects retain the explicit boundaries of the frozen verifiers.
No numeric message or actor ID is injected into an emulator.
"""
import inspect
from pathlib import Path
from PIL import Image, ImageDraw
from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts import probe_duel_cache_scope_v1150 as scope
from scripts import probe_duel_resident_fonts_v1151 as fonts
from scripts.duel_special_dispatch_v1217 import TABLES, IDS
from scripts.verify_personal_gameplay_v841 import get_machine
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/duel_special_native_v1219')
PLAN = Path('work/analysis/duel_special_native_v1218/native_payload_plan.json')
SOURCE = Path('out/all_routes_combined_v1206_candidate.nds')


def bindings(rom):
    class ExactSource:
        @staticmethod
        def open(path):
            assert str(path) == 'out/all_routes_combined_v1105_candidate.nds'
            return rom
    source = inspect.getsource(scope.pipeline)
    replacements = {
        "spans=[*plan['metadata_fields'],[0xDA28,0x134]]":
        "spans=[*plan['metadata_fields'],[0xDA28,0x134],[0x535E8,64]]",
        "'eligible':parent==BASE+0xD4BC and table in TABLES":
        "'eligible':(parent==BASE+0xD4BC and table in TABLES) or (parent==BASE+0xD528 and table in IDS)",
    }
    for old, new in replacements.items():
        assert source.count(old) == 1
        source = source.replace(old, new)
    env = {**scope.__dict__, 'NdsImage': ExactSource, 'PLAN_PATH': PLAN,
           'TABLES': TABLES, 'IDS': IDS}
    exec(compile(source, __file__, 'exec'), env)
    pipeline = env['pipeline']
    fs = inspect.getsource(fonts.execute)
    old = "get(0xD458, controller, 0 if family == 'challenge' else 1, 60, table)"
    new = "get(0xD4D0 if family == 'special_move_numeric' else 0xD458, controller, 0 if family in ('challenge','positive_action_reaction','negative_action_reaction','special_move_numeric') else 1, 120 if family == 'special_move_numeric' else 60, number if family == 'special_move_numeric' else table)"
    assert fs.count(old) == 1
    fs = fs.replace(old, new)
    fe = {**fonts.__dict__, 'pipeline': pipeline, 'PLAN_PATH': PLAN}
    exec(compile(fs, __file__, 'exec'), fe)
    ss = inspect.getsource(scope.execute)
    old = "side=0 if family=='challenge' else 1"
    assert ss.count(old) == 1
    ss = ss.replace(old, "side=0 if family in ('challenge','positive_action_reaction','negative_action_reaction') else 1")
    se = {**scope.__dict__, 'pipeline': pipeline, 'TABLES': TABLES, 'PLAN_PATH': PLAN}
    exec(compile(ss, __file__, 'exec'), se)
    return fe['execute'], se['execute'], {'pipeline': source, 'fonts': fs, 'scope': ss}


def main():
    assert not ROOT.exists()
    plan = read(PLAN)
    arm, common = Path(plan['target_ARM9']).read_bytes(), Path(plan['target_COMMON']).read_bytes()
    assert sha(arm) == plan['target_ARM9_sha256'] and sha(common) == plan['target_COMMON_sha256']
    context = read('work/analysis/duel_special_context_v1215b/source_context_packet.json')
    raw = Path(context['actual_snapshot']).read_bytes()
    assert sha(raw) == context['actual_snapshot_sha256']
    assert sha(SOURCE.read_bytes()) == context['current_ROM_sha256']
    rom = NdsImage.open(SOURCE)
    assert sha(rom.read_file('/__arm9__.bin')) == plan['source_ARM9_sha256']
    execute, execute_scope, sources = bindings(rom)
    ROOT.mkdir(parents=True)
    effective = []
    for name, source in sources.items():
        p = ROOT / f'effective_{name}.py'
        p.write_text(source, encoding='utf-8')
        effective.append({'path': str(p), 'sha256': sha(p.read_bytes())})
    records = {r['message_id']: r for r in read('translations/duel_special_editorial_manuscript_v1.json')['records']}
    actors = {r['message_ID']: r['actor_object'] for r in context['all15_original_message_call_bindings']}
    font, kanji = GameAsciiFont.from_arm9(arm), rom.read_file('/GRP/KANJI.FNT')
    cases, previews, excluded = [], [], []
    for n in IDS:
        row = records[n]
        result, visible = execute(arm, common, raw, actors[n], b'', 'special_move_numeric', 0,
                                  n, row['english'].encode('ascii'), font, kanji)
        assert result['native_getter_IDs'] == [n, 1931]
        result.update(original_entry='D4D0', side=0, duration=120,
                      source_speaker=row['speaker'], source_actor_ID=row['source_actor_ID'])
        cases.append(result)
        p = ROOT / f'COMMON{n}_native.png'
        image = Image.frombytes('L', (144, 36), bytes(255-v*17 for v in visible))
        image.save(p)
        previews.append({'message_ID': n, 'path': str(p), 'sha256': sha(p.read_bytes()), 'lines': result['lines']})
        print(n, result['lines'], 'complete native special fonts/crops pass', flush=True)
    cpu, get = get_machine(arm, raw)
    source_barks = read('work/analysis/duel_bark_context_v1199/source_context_packet.json')
    bark_actors = {}
    for row in source_barks['all416_unchanged_native_voice_selections']:
        bark_actors.setdefault(row['message_ID'], row['actor_object'])
    old = {r['message_id']: r for r in read('translations/duel_editorial_manuscript_v5.json')['records']}
    barks = {r['message_id']: r for r in read('translations/duel_bark_editorial_manuscript_v2.json')['records']}
    root = get(0xCB184)
    actor_objects = [root+4+i*32 for i in range(207)]+[root+0x19E4]
    for n, row in {**{k:v for k,v in old.items() if 1931 <= k <= 1950}, **barks}.items():
        table = row['source_table']
        if n in bark_actors:
            actor = bark_actors[n]
            family = row['source_family']
        else:
            actor = next(o for o in actor_objects if get(0x53F4C, o, table) == n)
            family = 'challenge' if n <= 1938 else 'acceptance' if n <= 1944 else 'threat'
        assert get(0x53F4C, actor, table) == n
        name = b'Rafael'
        text = row['english'].encode('ascii').replace(b'%s', name)
        result, visible = execute(arm, common, raw, actor, name, family, table, n, text, font, kanji)
        result['preserved_prior_voice_selection'] = True
        cases.append(result)
        excluded.append(execute_scope(arm, common, raw, actor, name, 'direct_negative', 0,
                                      n, row['english'].encode('ascii'), direct=True))
    # Both independent escape tables remain excluded from this static widget.
    selected = {}
    for table in (0x02117500, 0x02117620):
        for actor in actor_objects:
            n = get(0x53F4C, actor, table)
            selected.setdefault(n, (actor, table))
    assert set(selected) == {*range(1951, 1957), *range(1973, 1980)}
    for n, (actor, table) in sorted(selected.items()):
        excluded.append(execute_scope(arm, common, raw, actor, b'Rafael', 'escape_voice_negative',
                                      table, n, old[n]['english'].encode('ascii')))
    assert len(cases) == 51 and len(excluded) == 49 and all(not r['eligible'] for r in excluded)
    sheet = Image.new('RGB', (4*308, 4*110), '#263238')
    draw = ImageDraw.Draw(sheet)
    for i, row in enumerate(previews):
        x, y = i%4*308, i//4*110
        draw.text((x+5, y+3), f"COMMON{row['message_ID']}; native CPU fonts", fill='white')
        with Image.open(row['path']) as im:
            sheet.paste(im.resize((288, 72), Image.Resampling.NEAREST), (x+5, y+24))
    p = ROOT/'all15_special_native_review.png'
    sheet.save(p)
    dispatch = Path('work/analysis/duel_special_dispatch_v1217/owned_dispatch_proof.json')
    save(ROOT/'native_font_scope_verification.json', {
        'ARM9_sha256': sha(arm), 'COMMON_sha256': sha(common),
        'payload_plan': str(PLAN), 'payload_plan_sha256': sha(PLAN.read_bytes()),
        'dispatch_proof': str(dispatch), 'dispatch_proof_sha256': sha(dispatch.read_bytes()),
        'source_ROM': str(SOURCE), 'source_ROM_sha256': sha(SOURCE.read_bytes()),
        'snapshot': context['actual_snapshot'], 'snapshot_sha256': sha(raw),
        'cases': cases, 'all15_numeric_special_and36_preserved_voice_full_native_fonts_pass': True,
        'excluded_cases': excluded, 'all36_old_numeric_and13_escape_voice_calls_excluded': True,
        'original_loader_printf_macro_PIC_ASCII_CP932_painters_and_all_three_native_crops_execute': True,
        'all47_cache_flush_invalidate_lines_and_no_COMMON_reentry_or_code_write_during_PIC': True,
        'patch_after_snapshot_only_declared_metadata_DA28_and64byte_helper': True,
        'bound_effective_sources': effective, 'previews': previews,
        'review_sheet': str(p), 'review_sheet_sha256': sha(p.read_bytes()),
        'visual_review_pending': True, 'actual_special_and_registered_integration_pending': True,
        'no_completed_editorial_credit': True, 'producer_sha256': sha(Path(__file__).read_bytes()),
        'full_goal_complete': False})
    print('51 full native fonts and49 source caller exclusions pass; no gameplay/completion credit.', flush=True)


if __name__ == '__main__':
    main()
