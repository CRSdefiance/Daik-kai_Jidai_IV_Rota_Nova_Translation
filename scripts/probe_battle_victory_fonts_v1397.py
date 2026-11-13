"""All eight original victory voice pipelines and complete native font planes."""
import struct
from copy import deepcopy
from pathlib import Path
from types import FunctionType
from PIL import Image,ImageDraw
from dk4tool.patch.duel_editorial import owned_entries
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.battle_victory_native_plan_v1396 import compiled
from scripts.probe_battle_aftermath_fonts_v1256 import consumer,assigned_role_raw
from scripts.verify_common_alignment_native_v257 import raster as original_raster
from scripts.verify_personal_gameplay_v841 import get_machine
from scripts.verify_shipyard_gameplay_v760 import independent_font
from scripts.verify_village_wrap_v608 import read,save

ROOT = Path('work/analysis/battle_victory_fonts_v1397')
PLAN = Path('work/analysis/battle_victory_payload_v1396/native_payload_plan.json')
MANUSCRIPT = Path('translations/battle_victory_editorial_manuscript_v1.json')
BASE,TABLE = 0x02000000,0x02117EE0


if __name__=='__main__':
    assert not ROOT.exists()
    plan,doc = read(PLAN),read(MANUSCRIPT)
    assert plan['manuscript_sha256']==sha(MANUSCRIPT.read_bytes())
    arm,common = Path(plan['target_ARM9']).read_bytes(),Path(plan['target_COMMON']).read_bytes()
    assert sha(arm)==plan['target_ARM9_sha256'] and sha(common)==plan['target_COMMON_sha256']
    context = read(doc['source_context'])
    observed = context['prior_actual_2131']
    raw = Path(observed['snapshot']).read_bytes()
    assert sha(raw)==observed['snapshot_sha256']
    current = NdsImage.open(doc['current_ROM'])
    entries = owned_entries(common,arm,plan['directory_sha256'])
    assert list(struct.unpack_from('<8I',arm,TABLE-BASE))==list(range(2130,2138))
    cpu,get = get_machine(arm,raw)
    actors,captain = get(0xCB184),get(0x7F244)
    choices,representatives = [],{}
    for identity in range(207):
        if identity==captain:
            continue
        actor = actors+4+32*identity
        voice,number = get(0x7E988,actor),get(0x53F4C,actor,TABLE)
        assert get(0x7EE08,actor)==identity and number==2130+voice
        row = {'existing_actor_ID':identity,'actor_object':actor,'source_voice':voice,'message_ID':number}
        choices.append(row)
        representatives.setdefault(voice,row)
        if identity==16:
            representatives[voice] = row
    assert len(choices)==206 and set(representatives)==set(range(8))
    assert choices==context['all206_existing_actor_choices']
    class CurrentFont:
        @staticmethod
        def open(path):
            assert path=='out/all_routes_combined_v255_candidate.nds'
            return current
    raster = FunctionType(original_raster.__code__,{**original_raster.__globals__,'NdsImage':CurrentFont},argdefs=original_raster.__defaults__)
    ROOT.mkdir(parents=True)
    rows = {r['message_id']:r for r in doc['records']}
    cases,fixtures = [],[]
    for voice,source in sorted(representatives.items()):
        n = source['message_ID']
        if voice==1:
            assigned,fixture = raw,None
        else:
            assigned,fixture = assigned_role_raw(current.read_file('/__arm9__.bin'),raw,source['existing_actor_ID'],source['actor_object'])
            fixtures.append(fixture)
        native = consumer(arm,common,assigned,plan,0x53D44,1,TABLE)
        value = compiled(rows[n])
        assert entries[n].text==value and native['input_hex']==value.hex()
        formatted = bytes.fromhex(native['formatted_hex'])
        assert formatted==b' '+value and b'\n' not in formatted
        assert native['parent']==0x02053DB8 and native['selector']==TABLE
        events = []
        pixels = raster(arm,formatted,0x01FFCE40-BASE,size=(228,64),instruction_limit=2000000,glyph_events=events)
        line = value.decode('ascii')
        assert pixels==independent_font(arm,current.read_file('/GRP/KANJI.FNT'),[line])
        assert [e['code'] for e in events]==list(formatted)
        assert [(e['x'],e['y'],e['style']) for e in events]==[(6*i,0,1) for i in range(len(formatted))]
        assert events[1]['x']==6 and events[-1]['x']+6<=228
        assert all(p==0 for p in pixels[228*11:])
        if n==2131:
            assert formatted.hex()==observed['native_formatted_hex'] and value.hex()==observed['compiled_hex']
        path = ROOT/f'voice{voice}_ID{n}_complete_native.png'
        Image.frombytes('L',(228,64),bytes(0 if p else 255 for p in pixels)).save(path)
        cases.append({**source,'native_pipeline':native,'lines':[line],'compiled_hex':value.hex(),
            'native_formatted_hex':formatted.hex(),'original_leading_cell_count':1,
            'complete_glyph_events':events,'whole228x64_native_and_independent_font_exact':True,
            'complete_first_final_glyphs_uniform_single_line_margin_bounds_and_blank_paper_pass':True,
            'no_scoped_formatter_membership_or_code_change_required_for_these_exact_short_paragraphs':True,
            'preview':str(path),'preview_sha256':sha(path.read_bytes()),'whole_native_font_plane_sha256':sha(bytes(pixels)),
            'CPU_role_fixture':fixture,'CPU_only_not_new_GPU_or_individual_gameplay_activation':True})
        print(f'Voice{voice} ID{n}:full native glyph plane passes:{line}',flush=True)
    invalid = []
    baseline = doc['records'][0]
    bad = [('leading-space','english',' '+baseline['english']),('trailing-space','english',baseline['english']+' '),
        ('internal-gap','english',baseline['english'].replace(' ','  ',1)),('authored-LF','english','First\nSecond'),
        ('NUL','english','First\0Second'),('invented-printf','english','Admiral, %s won!'),
        ('layout-markup','english','We won! {LB}'),('non-ASCII','english','We won\u2014yes!'),('empty','english',''),
        ('unreviewed-long-layout','english','The entire crew has returned to report that we have won this battle.'),
        ('invented-argument-count','native_argument_count',1),('unreviewed-source-macro','source_native_macros',['IC']),
        ('unreviewed-message-ID','message_id',2129)]
    for label,field,value in bad:
        row = deepcopy(baseline)
        row[field] = value
        try:
            compiled(row)
        except (ValueError,AssertionError):
            invalid.append(label)
        else:
            raise AssertionError(label)
    row = deepcopy(rows[2132])
    row['source_native_macros'] = []
    try:
        compiled(row)
    except ValueError:
        invalid.append('missing-reviewed-collective-pronoun-binding')
    else:
        raise AssertionError('collective-pronoun-binding')
    assert len(invalid)==14
    sheet = Image.new('RGB',(936,608),'#263238')
    draw = ImageDraw.Draw(sheet)
    for i,case in enumerate(cases):
        x,y = i%2*468,i//2*152
        draw.text((x+5,y+3),f"Voice{case['source_voice']} ID{case['message_ID']}",fill='white')
        with Image.open(case['preview']) as preview:
            sheet.paste(preview.resize((456,128),Image.Resampling.NEAREST),(x+5,y+22))
    image = ROOT/'all8_native_victory_voices.png'
    sheet.save(image)
    save(ROOT/'native_font_proof.json',{'ARM9_sha256':sha(arm),'COMMON_sha256':sha(common),
        'manuscript_sha256':sha(MANUSCRIPT.read_bytes()),'all206_existing_actor_choices':choices,
        'source_raw8_voice_table':list(range(2130,2138)),'cases':cases,'findings':[],
        'all8_whole_native_font_planes_and_complete_ordered_glyph_events_exact':True,
        'actual2131_retained_native_formatted_bytes_preserved':True,
        'original_single_leading_cell_verified_no_authored_alignment':True,
        'all_runtime_selector_code_and_allocations_unchanged':True,
        'CPU_only_counterfactual_physical_FirstMate_assignments':fixtures,
        'actual_logical_FirstMate16_used_without_assignment_for_voice1':True,
        'invalid_compiler_inputs_rejected':invalid,'review_sheet':str(image),'review_sheet_sha256':sha(image.read_bytes()),
        'visual_review_pending':True,'registered_release_and_original_gameplay_still_pending':True,
        'producer_sha256':sha(Path(__file__).read_bytes()),'full_goal_complete':False})
    print('Eight victory native font planes and206 source actor choices pass;14 invalid inputs rejected;visual/release/gameplay gates remain.',flush=True)
