"""Seven current native paragraphs,eight original role7 voices;no shot-event claim."""
from pathlib import Path
from copy import deepcopy
from PIL import Image, ImageDraw
from scripts.current_common_native_context_v2620b import CurrentContext
from scripts.probe_reinforcement_sniping_layout_v1030 import native_layout
from scripts.verify_arrival_native_v792 import prepared
from scripts.verify_shipyard_gameplay_v760 import independent_font
from scripts.search_reports_native_consumers_v1662 import assigned_role
from scripts.probe_common_single_cache_v862 import Loader
from scripts.reinforcement_sniping_layout_v1024 import compiled
from scripts.verify_village_wrap_v608 import read, save
from dk4tool.patch.grand_race_menu_release import sha

ROOT = Path('work/analysis/admiral_shot_fonts_v2658')
DOC = Path('translations/admiral_shot_contextual_editorial_manuscript_v1.json')
BASE, TABLE = 0x02000000, 0x02117300

if __name__ == '__main__':
    assert not ROOT.exists()
    doc = read(DOC)
    ctx = CurrentContext(DOC, 'out/all_routes_combined_v1807_candidate.nds', ROOT)
    context = read(doc['native_context_proof'])
    goldenpath = Path('work/analysis/current_reinforcement_matrix_v1801d/current694_native_wrap_and_font_reconciliation.json')
    golden = read(goldenpath)
    prior = {c['message_ID']: c for c in golden['cases'] if 1924 <= c['message_ID'] <= 1930}
    rows = {r['message_id']: r for r in doc['records']}
    assert set(rows) == set(prior) == set(range(1924,1931))
    cpu = prepared(ctx.arm)
    font = ctx.rom.read_file('/GRP/KANJI.FNT')
    cases = []
    for n, row in rows.items():
        template = compiled(row)
        assert template == ctx.entries[n].text and row['native_argument_count'] == 0
        formatted, lines = native_layout(cpu, template, n, None, TABLE)
        assert formatted.hex() == prior[n]['formatted_hex'] and lines == prior[n]['lines']
        assert 1 <= len(lines) <= 4 and all(0 < len(line) <= 35 for line in lines)
        assert not (len(lines) > 1 and len(lines[-1].split()) == 1)
        assert not [line for line in lines[:-1] if line.split()[-1].strip('.,!?;:').lower() in {'a','an','the','to','of','with','for','from','on','in','as','at'}]
        events = []
        native = bytes(ctx.raster(ctx.arm, formatted, 0x01FFCE40-BASE, size=(228,64), instruction_limit=2000000, glyph_events=events))
        pixels = bytes(independent_font(ctx.arm, font, lines))
        assert native == pixels and sha(pixels) == prior[n]['font_plane_sha256']
        guards = []
        for y, line in enumerate(lines):
            actual = [e for e in events if e['y'] == y*16]
            assert all(e['code'] == 32 and e['x'] == 0 for e in actual if e['x'] < 6)
            actual = [e for e in actual if e['x'] >= 6]
            pos, x = 0, 6
            for j, char in enumerate(line):
                if ord(char) != 32 and actual[pos]['code'] == 32 and actual[pos]['x'] == x:
                    assert y > 0 and j == 0
                    guards.append(actual[pos]); pos += 1
                assert actual[pos]['code'] == ord(char) and (actual[pos]['x'],actual[pos]['y']) == (x,y*16)
                pos += 1; x += 6
            assert x <= 228 and all(e['code'] == 32 for e in actual[pos:])
        path = ROOT/f'ID{n}_complete_native.png'
        Image.frombytes('L',(228,64),bytes(0 if p else 255 for p in pixels)).save(path)
        cases.append(dict(message_ID=n, compiled_hex=template.hex(), formatted_hex=formatted.hex(), lines=lines,
            font_plane_sha256=sha(pixels), complete_ordered_glyph_events=events, zero_ink_phase_guards=guards,
            complete_current_native_and_independent_plane_equal=True,
            current_font_mask_equals_historical_reference=True,
            preview=str(path), preview_sha256=sha(path.read_bytes())))
    pipelines = []
    for voice in range(8):
        if voice == 1:
            choice = next(c for c in context['all207_original_actor_choices'] if c['actor_ID'] == 16)
            raw = ctx.raw
            fixture = dict(no_roster_fixture=True, actual_logical_fallback_actor=16,
                physical_Lookout_remains_unassigned=True, not_original_shot_eligibility=True)
        else:
            choice = next(c for c in context['all207_original_actor_choices'] if c['source_voice'] == voice and c['actor_ID'] != 1)
            raw, fixture = assigned_role(ctx.arm,ctx.raw,7,choice['actor_ID'],choice['actor_object'])
        n = choice['message_ID']
        assert choice['source_voice'] == voice
        result = ctx.speak(0x53D44,7,TABLE,None,raw=raw)
        owner = int.from_bytes(ctx.arm[0x552A0:0x552A4],'little')
        loaded = bytes(ctx.machines[-1][0].mem_read(owner+0x2030,512)).split(b'\0')[0]
        assert loaded == ctx.entries[n].text and result['input_hex'] == loaded.hex()
        assert result['formatted_hex'] == next(c['formatted_hex'] for c in cases if c['message_ID'] == n)
        result['loaded_template_hex'] = loaded.hex()
        pipelines.append(dict(source_voice=voice,message_ID=n,original_actor_choice=choice,
            CPU_only_voice_fixture=fixture,native_pipeline=result))
        print(f'Original role7 voice{voice} message{n} complete current pipeline passed.',flush=True)
    invalid = []
    for title,field,value in [
        ('leading','english',' '+rows[1924]['english']),('trailing','english',rows[1924]['english']+' '),
        ('gap','english','We  won!'),('LF','english','We\nwon!'),('NUL','english','We\0won!'),
        ('layout','english','We {LB}won!'),('nonASCII','english','We—won!'),
        ('extra-arg','english','We shot %s!'),('percent','english','We won 100%!'),
        ('wrong-ID','message_id',1931),('wrong-argc','native_argument_count',1),
        ('family','source_family','reinforcement'),('macro','english','FI won!'),
        ('overflow','english','A'*220)]:
        row = deepcopy(rows[1924]); row[field] = value
        try: compiled(row)
        except (ValueError,AssertionError): invalid.append(title)
        else: raise AssertionError(title)
    copies = [Loader(ctx.arm,ctx.common).copy(n,ctx.entries[n].text,mode) for mode in ['cold','warm'] for n in rows]
    assert not any(ctx.raster(ctx.arm,b' ',0x01FFCE40-BASE,size=(228,64),instruction_limit=2000000))
    sheet = Image.new('RGB',(936,608),'#263238')
    draw = ImageDraw.Draw(sheet)
    for i,c in enumerate(cases):
        x,y = i%2*468,i//2*152
        draw.text((x+5,y+3),f'Lookout ID{c["message_ID"]}: complete native paragraph',fill='white')
        sheet.paste(Image.open(c['preview']).resize((456,128),Image.Resampling.NEAREST),(x+5,y+22))
    sheetpath = ROOT/'all7_native_review_sheet.png'; sheet.save(sheetpath)
    save(ROOT/'native_font_proof.json',dict(candidate=str(ctx.rompath),candidate_sha256=sha(ctx.rompath.read_bytes()),
        ARM9_sha256=sha(ctx.arm),COMMON_sha256=sha(ctx.common),manuscript=str(DOC),manuscript_sha256=sha(DOC.read_bytes()),
        cases=cases,all8_original_role7_speech_pipelines=pipelines,all14_cold_warm_copies=copies,
        invalid_compiler_inputs_rejected=invalid,blank_space_glyph_zero_ink=True,findings=[],
        all_executed_pipeline_instructions_current_ROM_byte_exact=True,all_original_actor_models_unchanged=True,
        pipeline_plan=str(ctx.proof_path),pipeline_plan_sha256=sha(ctx.proof_path.read_bytes()),
        historical_reference=str(goldenpath),historical_reference_sha256=sha(goldenpath.read_bytes()),
        review_sheet=str(sheetpath),review_sheet_sha256=sha(sheetpath.read_bytes()),visual_review_pending=True,
        scope='Current scoped CPU/font/layout tests only. Eight voices cover the seven no-argument reports and original voice1 fallback. One unchanged actual speech fallback and seven original-setter duty-byte fixtures are disclosed. These execute speech selection/loading/printf/macros/wrapping,not the chance gate or post-shot result. No new emulator event,earned assignment,altered skills,RNG or gameplay outcome.',
        completion_credit_added=0,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print('Seven complete fonts,eight original voice pipelines,14copies and14negative compiler inputs pass. Visual and distinct outcome reconciliation pending.',flush=True)
