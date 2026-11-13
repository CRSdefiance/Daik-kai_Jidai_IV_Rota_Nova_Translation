"""Original direct speech pipelines and complete font planes for all8 fire voices."""
from copy import deepcopy
from pathlib import Path
from types import FunctionType
import struct
from PIL import Image, ImageDraw
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.duel_editorial import owned_entries
from dk4tool.rom.nds import NdsImage
from scripts.powder_fire_native_plan_v1309 import compiled
from scripts.powder_fire_layout_v1304 import IDS, paragraph
from scripts.probe_battle_aftermath_fonts_v1256 import consumer
from scripts.verify_common_alignment_native_v257 import raster as original_raster
from scripts.verify_shipyard_gameplay_v760 import independent_font
from scripts.verify_personal_gameplay_v841 import get_machine
from scripts.verify_village_wrap_v608 import read,save

ROOT = Path('work/analysis/powder_fire_fonts_v1310')
PLAN = Path('work/analysis/powder_fire_payload_v1309/native_payload_plan.json')
RUNTIME = Path('work/analysis/powder_fire_runtime_v1308/native_runtime_verification.json')
MANUSCRIPT = Path('translations/powder_fire_editorial_manuscript_v1.json')
RAW = Path('E:/Rota Nova translations/Generated/work/emulation_v193/town_gunnery_v1300_1266/frame_007210_arm9_ram.bin')
BASE, TABLE = 0x02000000, 0x02117980


def main():
    assert not ROOT.exists()
    plan,doc,scope = read(PLAN),read(MANUSCRIPT),read(RUNTIME)
    assert plan['manuscript_sha256'] == sha(MANUSCRIPT.read_bytes())
    arm,common = Path(plan['target_ARM9']).read_bytes(),Path(plan['target_COMMON']).read_bytes()
    assert sha(arm) == plan['target_ARM9_sha256'] and sha(common) == plan['target_COMMON_sha256']
    assert scope['source_ARM9_sha256'] == plan['source_ARM9_sha256']
    current = NdsImage.open(doc['current_ROM'])
    raw = RAW.read_bytes()
    binding = read(doc['source_context'])
    assert sha(raw) == binding['actual_old_wording_holds'][0]['RAM_sha256']
    entries = owned_entries(common,arm,plan['directory_sha256'])
    cpu,get = get_machine(current.read_file('/__arm9__.bin'),raw)
    actors,captain = get(0xCB184),get(0x7F244)
    expected = [2052,2053,2052,2052,2054,2055,2056,2057]
    selected,representatives = [],{}
    for actor_id in range(207):
        if actor_id == captain:
            continue
        actor = actors+4+actor_id*32
        voice,number = get(0x7E988,actor),get(0x53F4C,actor,TABLE)
        assert get(0x7EE08,actor) == actor_id and 0 <= voice < 8 and number == expected[voice]
        row = {'existing_actor_ID':actor_id,'actor_object':actor,'source_voice':voice,'source_message_ID':number}
        selected.append(row)
        representatives.setdefault(voice,row)
        if actor_id == 16:
            representatives[voice] = row
    assert len(selected) == 206 and set(representatives) == set(range(8))
    assert representatives[1]['existing_actor_ID'] == 16
    class CurrentFont:
        @staticmethod
        def open(path):
            assert path == 'out/all_routes_combined_v255_candidate.nds'
            return current
    raster = FunctionType(original_raster.__code__,{**original_raster.__globals__,'NdsImage':CurrentFont},argdefs=original_raster.__defaults__)
    ROOT.mkdir(parents=True)
    previews = ROOT/'previews'
    previews.mkdir()
    records = {row['message_id']:row for row in doc['records']}
    cases,findings = [],[]
    for voice,source in sorted(representatives.items()):
        number = source['source_message_ID']
        row = records[number]
        value = compiled(row)
        assert entries[number].text == value and b'\n' not in value
        native = consumer(arm,common,raw,plan,0x53F0C,source['actor_object'],TABLE)
        assert native['parent'] == 0x02053F40 and native['selector'] == TABLE
        assert native['input_hex'] == value.hex()
        formatted = bytes.fromhex(native['formatted_hex'])
        lines = [line.strip().decode('ascii') for line in formatted.split(b'\n')]
        assert ' '.join(lines) == row['english'] and 1 <= len(lines) <= 4
        assert all(0 < len(line) <= 35 and '  ' not in line and line == line.strip() for line in lines)
        pixels = raster(arm,formatted,0x01FFCE40-BASE,size=(228,64),instruction_limit=2000000)
        assert pixels == independent_font(arm,current.read_file('/GRP/KANJI.FNT'),lines)
        path = previews/f'voice{voice}_ID{number}_complete_native.png'
        Image.frombytes('L',(228,64),bytes(0 if pixel else 255 for pixel in pixels)).save(path)
        orphan = len(lines)>1 and len(lines[-1].split()) == 1
        weak = [i for i,line in enumerate(lines[:-1]) if line.split()[-1].strip('.,!?;:').lower() in {'a','an','the','to','of','with','for','from','on','in','as','at'}]
        case = {**source,'message_id':number,'compiled_hex':value.hex(),'native_pipeline':native,
            'native_formatted_hex':formatted.hex(),'lines':lines,'name_case':None,
            'complete228x64_native_independent_font_and_all_letters_equal':True,
            'uniform_visible_origins_no_authored_indent_and_bounds_pass':True,
            'single_word_final_row':orphan,'weak_line_end_indices':weak,'preview':str(path),'preview_sha256':sha(path.read_bytes()),
            'CPU_direct_call_existing_actor_not_actual_event_or_membership_claim':True}
        cases.append(case)
        if orphan or weak:
            findings.append({'source_voice':voice,'message_id':number,'lines':lines,'single_word_final_row':orphan,'weak_line_end_indices':weak})
        print(f'Voice{voice},ID{number}: original pipeline and whole native font pass: {lines}',flush=True)
    assert len(cases) == 8 and {row['message_id'] for row in cases} == set(IDS)
    invalid = []
    baseline = records[2052]
    for label,text in [('leading-space',' '+baseline['english']),('trailing-space',baseline['english']+' '),
        ('double-space',baseline['english'].replace(' ','  ',1)),('authored-LF','First\nSecond'),('embedded-NUL','First\0Second'),
        ('invented-printf','Fire %s!'),('layout-markup','Fire! {LB} Help!'),('non-ASCII','Fire\u2014help!'),('empty','')]:
        row = deepcopy(baseline)
        row['english'] = text
        try:
            paragraph(row)
        except ValueError:
            invalid.append(label)
        else:
            raise AssertionError(label)
    for label,field,value in [('wrong-family','message_id',2058),('invented-argument','native_argument_count',1),('invented-macro','source_native_macros',['FI'])]:
        row = deepcopy(baseline)
        row[field] = value
        try:
            paragraph(row)
        except ValueError:
            invalid.append(label)
        else:
            raise AssertionError(label)
    assert len(invalid) == 12
    sheet = Image.new('RGB',(936,608),'#263238')
    draw = ImageDraw.Draw(sheet)
    for index,case in enumerate(cases):
        x,y = index%2*468,index//2*152
        draw.text((x+5,y+3),f"Voice{case['source_voice']} ID{case['message_id']}",fill='white')
        with Image.open(case['preview']) as preview:
            sheet.paste(preview.resize((456,128),Image.Resampling.NEAREST),(x+5,y+22))
    sheet_path = ROOT/'all8_voice_native_review.png'
    sheet.save(sheet_path)
    save(ROOT/'native_font_proof.json',{'ARM9_sha256':sha(arm),'COMMON_sha256':sha(common),
        'manuscript':str(MANUSCRIPT),'manuscript_sha256':sha(MANUSCRIPT.read_bytes()),
        'payload_plan':str(PLAN),'payload_plan_sha256':sha(PLAN.read_bytes()),'runtime_proof':str(RUNTIME),'runtime_proof_sha256':sha(RUNTIME.read_bytes()),
        'source_actor_voice_matrix':selected,'all206_existing_noncaptain_source_selections_and_both_fallback_voices_pass':True,
        'all8_voice_pipelines_and6_unique_messages_full_native_fonts_pass':True,'cases':cases,
        'line_boundary_findings_requiring_visual_review':findings,'all12_malformed_compiler_inputs_rejected':invalid,
        'review_sheet':str(sheet_path),'review_sheet_sha256':sha(sheet_path.read_bytes()),'visual_review_pending':True,
        'native_copies_registered_release_exact_patch_and_revised_actual_scene_pending':True,
        'producer_sha256':sha(Path(__file__).read_bytes()),'full_goal_complete':False})
    print('All8 voices,6 messages and12 compiler rejection controls pass;visual/native release gates remain open.',flush=True)


if __name__ == '__main__':
    main()
