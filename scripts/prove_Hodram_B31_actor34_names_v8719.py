"""Fresh actor34 getters/voice/nameplanes, before existing B31/B53 English.

Clean name fields are evidence, not automatically a biography or full-name
approval. Actor113 retains its prior scoped proof through exact current inputs.
"""
import inspect
import struct
from pathlib import Path
from types import FunctionType
from PIL import Image, ImageDraw
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.Hodram_B52_registered_route_context_v8707 import RouteCurrentContext
from scripts.audit_native_given_name_table import string
from scripts.prove_lil_B167_names_v4124b import names
from scripts.reconcile_lil_B142_B145_voices_v3572 import selectors
from scripts import lil_B207_name_style_v6354d as style
from scripts.Hodram_FE_font_oracles_v8315 import bind
from scripts.prove_lil_B208_name_planes_v6405 import codes, original_name_events
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/Hodram_B31_actor34_names_v8719')
GLOSS = Path('work/analysis/Hodram_B31_B53_clean_context_v8714/three_clean_glosses_explicit52_31_53_dependency_andunnamed_man_before_current_English.json')
CONTROL = Path('work/analysis/Hodram_B31_B53_source_controls_v8718/source_controls.json')
INPUT = Path('work/analysis/current_V8704_Hodram_native_v8707/current_native_input.json')
VIEW = Path('work/analysis/Hodram_B52_registered_startup_view_v8708/own_registered_startup6_RGBpairs_actor_equal_unchanged_names_direct_view.json')
PRIOR = Path('work/analysis/Hodram_target_names_v8271/six_current_identities12_getters6_native_nameplanes_own_captain1_context.json')
PRIOR_FIELDS = Path('work/analysis/Hodram_B137_B45_B46_names_v8192/six_static_speakers12_getters_clean_fields24_synthetic_macro_alignments.json')


def current_fields(arm, common, raw, plan):
    cpu, get, provider = machine(arm, common, raw, plan)
    before = bytes(cpu.mem_read(0x02000000, 0x400000))
    table = struct.unpack_from('<I', arm, 0xCDAC0)[0]
    result = []
    for ident in [34, 113]:
        fields = []
        for col, kind in [(0, 'given'), (4, 'surname'), (8, 'middle')]:
            address = table + 32 * ident + col
            pointer = struct.unpack('<I', cpu.mem_read(address, 4))[0]
            assert arm[address-0x02000000:address-0x02000000+4] == bytes(cpu.mem_read(address, 4))
            value = None
            if pointer:
                assert 0x02000000 <= pointer < 0x02400000
                value = bytes(cpu.mem_read(pointer, 128)).split(b'\0')[0]
                assert len(value) < 128 and before[pointer-0x02000000:pointer-0x02000000+len(value)+1] == value+b'\0'
            fields.append(dict(kind=kind, table_field=address-0x02000000, table_field_hex=arm[address-0x02000000:address-0x02000000+4].hex(), pointer=pointer,
                actual_current_RAM_string_hex=None if value is None else value.hex(), actual_current_RAM_text=None if value is None else value.decode('cp932'),
                null_pointer_is_not_an_empty_string=not pointer, outside_static_ARM9=bool(pointer and pointer-0x02000000 >= len(arm))))
        result.append(dict(actor_ID=ident, fields=fields))
    assert bytes(cpu.mem_read(0x02000000, 0x400000)) == before
    return dict(rows=result, all4MiB_andoriginal_ABI_exact=True, deployed_orstatic_bytes_from_own_current_capture=True)


if __name__ == '__main__':
    assert not ROOT.exists()
    gloss, control, inp, view, prior, oldfields = map(read, [GLOSS, CONTROL, INPUT, VIEW, PRIOR, PRIOR_FIELDS])
    assert gloss['current_English_for_B31_andB53_still_unconsulted'] and control['current_B31_B53_English_dialogue_bodies_still_unconsulted']
    assert view['viewed'] and view['whole_actors_equal'] and view['reuse_requires_identical_complete_ARM9_COMMON_font_andwhole_actual_actors']
    current, clean, old = NdsImage.open(inp['current_ROM']), NdsImage.open('work/clean.nds'), NdsImage.open(prior['candidate'])
    assert sha(Path(inp['current_ROM']).read_bytes()) == inp['current_ROM_sha256'] == control['candidate_sha256'] == view['candidate_sha256']
    for path in ['/__arm9__.bin', '/COMMON/MESFILE.DK4', '/GRP/KANJI.FNT']:
        assert current.read_file(path) == old.read_file(path)
    arm = current.read_file('/__arm9__.bin')
    fields = []
    for ident in [34, 113]:
        versions = {}
        for version, image in [('clean', clean), ('current', current)]:
            data = image.read_file('/__arm9__.bin')
            table = struct.unpack_from('<I', data, 0xCDAC0)[0]-0x02000000
            assert table == 0x120B80
            rows = []
            for col, kind in [(0, 'given'), (4, 'surname'), (8, 'middle')]:
                at = table+32*ident+col
                rows.append(dict(kind=kind, table_field=at, table_field_hex=data[at:at+4].hex(), **string(data, struct.unpack_from('<I', data, at)[0])))
            versions[version] = rows
        fields.append(dict(actor_ID=ident, **versions))
    ROOT.mkdir(parents=True)
    ctx = RouteCurrentContext(INPUT, 'unused-no-historical-ROM', ROOT/'current_context')
    runtime_fields = ctx.execute(current_fields); ctx.machines.pop()
    name_adapter = checked_text(inspect.getsource(names), {'for ident in [2,4,13,23,109]:': 'for ident in [34]:', 'all_ten_original_consumers': 'all_two_original_actor34_consumers'})
    env = dict(names.__globals__); exec(compile(name_adapter, __file__+'::actor34-getters', 'exec'), env)
    getters = ctx.execute(env['names']); ctx.machines.pop()
    voice_adapter = checked_text(inspect.getsource(selectors), {'assert captain==2': 'assert captain==1'})
    env = dict(selectors.__globals__); exec(compile(voice_adapter, __file__+'::captain1-voice', 'exec'), env)
    voices = ctx.execute(env['selectors'], [34]); ctx.machines.pop()
    assert len(getters['rows']) == 2 and len(voices['rows']) == 1 and not ctx.machines
    reused_getters = [r for r in prior['native_twelve_progressive_andfull_getters']['rows'] if r['actor_ID'] == 113]
    reused_voice = [r for r in prior['native_six_source_voices']['rows'] if r['source_selector'] == 113]
    reused_plane = next(r for r in prior['name_planes'] if r['actor_ID'] == 113)
    assert len(reused_getters) == 2 and len(reused_voice) == 1 and reused_plane['complete_first_internal_final_characters_andbounds']
    assert sha(Path(reused_plane['native_plane']).read_bytes()) == reused_plane['native_plane_sha256'] and sha(Path(reused_plane['preview']).read_bytes()) == reused_plane['preview_sha256']
    previous_fields = next(r for r in oldfields['complete_clean_andcurrent_name_fields'] if r['actor_ID'] == 113)
    current113 = next(r for r in fields if r['actor_ID'] == 113)
    assert current113['clean'] == previous_fields['clean_fields'] and current113['current'] == previous_fields['current_fields']
    digest = sha(arm)
    caller = FunctionType(style.style_source_proof.__code__, {**style.style_source_proof.__globals__, 'ARM9': digest}, argdefs=style.style_source_proof.__defaults__)
    raster = FunctionType(style.native_name_raster.__code__, {**style.native_name_raster.__globals__, 'style_source_proof': caller}, argdefs=style.native_name_raster.__defaults__)
    pixels, unused_factory, oracle = bind(current)
    planes = []; pictures = []
    for text in dict.fromkeys(r['text'] for r in getters['rows']):
        raw = text.encode('cp932'); plane, events, font = raster(arm, raw)
        assert font == current.read_file('/GRP/KANJI.FNT') and plane == pixels(arm, font, events)
        emitted, flushes = original_name_events(events, raw); assert emitted == codes(raw)
        assert all(e['style'] == 11 and e['y'] == 0 and 0 <= e['x'] and e['x']+(6 if e['kind'] == 'ascii' else 12) <= 216 for e in events)
        n = len(planes); path = ROOT/f'actor34_name{n}.bin'; path.write_bytes(plane)
        picture = Image.new('RGB', (216, 64)); picture.putdata([(98,97,98) if v else (250,245,223) for v in plane])
        preview = path.with_suffix('.png'); picture.save(preview); pictures.append((text, picture))
        planes.append(dict(actor_ID=34, text=text, input_hex=raw.hex(), native_glyph_events=events, source_owned_zero_ink_flushes=flushes,
            native_plane=str(path), native_plane_sha256=sha(plane), preview=str(preview), preview_sha256=sha(preview.read_bytes()),
            complete_first_internal_final_characters_andbounds=True, one_original_progressive_style11_row=True,
            rendering_full_getter_literal_in_name_style_is_not_full_catalogue_UI_test=True))
    pictures.append(('Port Worker (exact prior plane reused)', Image.open(reused_plane['preview']).convert('RGB')))
    sheet = Image.new('RGB', (912, ((len(pictures)+1)//2)*160), '#263238'); draw = ImageDraw.Draw(sheet)
    for n, (text, picture) in enumerate(pictures):
        x,y=n%2*456,n//2*160; draw.text((x+3,y+3), text+' offline native', fill='white'); sheet.paste(picture.resize((432,128),Image.Resampling.NEAREST),(x,y+24))
    sheetfile = ROOT/'actor34_fresh_and113_reused_names.png'; sheet.save(sheetfile)
    save(ROOT/'source_names_native_getters_andplanes.json', dict(candidate=inp['current_ROM'], candidate_sha256=inp['current_ROM_sha256'], ARM9_sha256=digest,
        source_gloss=str(GLOSS), source_gloss_sha256=sha(GLOSS.read_bytes()), source_controls=str(CONTROL), source_controls_sha256=sha(CONTROL.read_bytes()),
        complete_clean_current_static_fields=fields, exact_current_RAM_fields=runtime_fields, fresh_actor34_two_getters=getters, fresh_actor34_source_voice=voices,
        scoped_reused_actor113=dict(two_getters=reused_getters, source_voice=reused_voice, plane=reused_plane, exact_fields=previous_fields),
        fresh_actor34_name_planes=planes, original_style11_caller=caller(arm), font_oracle_binding=oracle,
        original_name_adapter=name_adapter, original_voice_adapter=voice_adapter,
        current_native_input=str(INPUT), current_native_input_sha256=sha(INPUT.read_bytes()), native_context_plan=str(ctx.proof_path), native_context_plan_sha256=sha(ctx.proof_path.read_bytes()),
        review_sheet=dict(path=str(sheetfile), sha256=sha(sheetfile.read_bytes())), direct_view_andeditorial_full_name_decision_pending=True,
        clean_middle_androle_metadata_not_automatically_biography_or_rank=True, current_B31_B53_English_dialogue_bodies_unconsulted=True,
        no_actual_source_scene_headers_full_catalogue_UI_all207_orcustom_name_claim=True, no_ROM_registry_ledger_orprior_artifact_change=True,
        new_credit=0, new_emulator_runs=0, full_goal_complete=False,
        evidence={str(p):sha(p.read_bytes()) for p in [GLOSS,CONTROL,INPUT,VIEW,PRIOR,PRIOR_FIELDS,Path(__file__)]}))
    print('Actor34 original getters:', [(r['consumer'],r['text']) for r in getters['rows']], flush=True)
    print('Actor34 voice:', voices['rows'], flush=True)
    print('Fresh native actor34 names; actor113 proof reused through exact inputs. Direct view/editorial decision pending.', flush=True)
