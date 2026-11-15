"""Original capture table's eight voice pipelines with the precision correction."""
import struct
from copy import deepcopy
from pathlib import Path
from types import FunctionType
from PIL import Image,ImageDraw
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.duel_editorial import owned_entries
from dk4tool.rom.nds import NdsImage
from scripts.flagship_precision_native_plan_v1356 import compiled
from scripts.probe_battle_aftermath_fonts_v1256 import consumer,assigned_role_raw
from scripts.verify_personal_gameplay_v841 import get_machine
from scripts.verify_common_alignment_native_v257 import raster as original_raster
from scripts.verify_shipyard_gameplay_v760 import independent_font
from scripts.verify_village_wrap_v608 import read,save

ROOT = Path('work/analysis/flagship_precision_fonts_v1357')
PLAN = Path('work/analysis/flagship_precision_payload_v1356/native_payload_plan.json')
MANUSCRIPT = Path('translations/flagship_capture_precision_manuscript_v1.json')
RAW = Path('E:/Rota Nova translations/Generated/work/emulation_v193/ship_sinking_v1353_1344/frame_010800_arm9_ram.bin')
BASE,TABLE = 0x02000000,0x02117740


def main():
    assert not ROOT.exists()
    plan,doc = read(PLAN),read(MANUSCRIPT)
    assert plan['manuscript_sha256']==sha(MANUSCRIPT.read_bytes())
    arm,common = Path(plan['target_ARM9']).read_bytes(),Path(plan['target_COMMON']).read_bytes()
    assert sha(arm)==plan['target_ARM9_sha256'] and sha(common)==plan['target_COMMON_sha256']
    current = NdsImage.open(doc['current_ROM'])
    raw = RAW.read_bytes()
    actual = read('work/analysis/flagship_capture_verified_v1354b/actual_flagship_capture_verification.json')
    assert actual['complete_actual2011_holds'][0]['RAM_sha256']==sha(raw)
    entries = owned_entries(common,arm,plan['directory_sha256'])
    table = list(struct.unpack_from('<8I',arm,TABLE-BASE))
    assert table==[2011,0xFFFFFFFF,2012,0xFFFFFFFF,0xFFFFFFFF,2013,2014,2015]
    expected = [2011,2011,2012,2011,2011,2013,2014,2015]
    cpu,get = get_machine(arm,raw)
    actors,captain = get(0xCB184),get(0x7F244)
    selections,representatives = [],{}
    for identity in range(207):
        if identity==captain:
            continue
        actor = actors+4+identity*32
        voice,number = get(0x7E988,actor),get(0x53F4C,actor,TABLE)
        assert get(0x7EE08,actor)==identity and number==expected[voice]
        row = {'existing_actor_ID':identity,'actor_object':actor,'source_voice':voice,'message_ID':number}
        selections.append(row)
        representatives.setdefault(voice,row)
        if identity==16:
            representatives[voice] = row
    assert len(selections)==206 and set(representatives)==set(range(8))
    class CurrentFont:
        @staticmethod
        def open(path):
            assert path=='out/all_routes_combined_v255_candidate.nds'
            return current
    raster = FunctionType(original_raster.__code__,{**original_raster.__globals__,'NdsImage':CurrentFont},argdefs=original_raster.__defaults__)
    old_font = read('work/analysis/battle_aftermath_fonts_v1260/native_font_proof.json')
    ROOT.mkdir(parents=True)
    cases,findings,fixtures = [],[],[]
    for voice,source in sorted(representatives.items()):
        number = source['message_ID']
        if voice==1:
            assigned,fixture = raw,None
        else:
            assigned,fixture = assigned_role_raw(current.read_file('/__arm9__.bin'),raw,source['existing_actor_ID'],source['actor_object'])
            fixtures.append(fixture)
        native = consumer(arm,common,assigned,plan,0x53D44,1,TABLE)
        assert native['parent']==0x02053DB8 and native['selector']==TABLE
        assert native['input_hex']==entries[number].text.hex()
        formatted = bytes.fromhex(native['formatted_hex'])
        lines = [line.strip().decode('ascii') for line in formatted.split(b'\n')]
        assert ' '.join(lines)==entries[number].text.decode('ascii').strip()
        assert 1<=len(lines)<=4 and all(0<len(line)<=35 and '  ' not in line for line in lines)
        pixels = raster(arm,formatted,0x01FFCE40-BASE,size=(228,64),instruction_limit=2000000)
        assert pixels==independent_font(arm,current.read_file('/GRP/KANJI.FNT'),lines)
        if number!=2015:
            old = next(r for r in old_font['cases'] if r['message_id']==number and r['name_case'] is None)
            assert native['formatted_hex']==old['native_formatted_hex']
        if number==2011:
            assert native['formatted_hex']==actual['complete_actual2011_holds'][0]['native_pipeline']['formatted_hex']
        if number==2015:
            assert entries[number].text==compiled(doc['records'][0])
        path = ROOT/f'voice{voice}_ID{number}_complete_native.png'
        Image.frombytes('L',(228,64),bytes(0 if p else 255 for p in pixels)).save(path)
        orphan = len(lines)>1 and len(lines[-1].split())==1
        weak = [i for i,line in enumerate(lines[:-1]) if line.split()[-1].strip('.,!?;:').lower() in {'a','an','the','to','of','with','for','from','on','in','as','at'}]
        case = {**source,'native_pipeline':native,'lines':lines,'compiled_hex':entries[number].text.hex(),
            'full228x64_native_independent_font_and_complete_glyphs_equal':True,
            'uniform_margins_no_authored_alignment_and_bounds_pass':True,
            'single_word_final_row':orphan,'weak_line_end_indices':weak,
            'preview':str(path),'preview_sha256':sha(path.read_bytes()),'CPU_role_fixture':fixture,
            'CPU_only_not_new_ROM_GPU_or_individual_gameplay_activation':True}
        cases.append(case)
        if orphan or weak:
            findings.append({'voice':voice,'message_ID':number,'lines':lines,'orphan':orphan,'weak':weak})
        print(f'Voice{voice} ID{number}:original pipeline and complete fonts pass:{lines}',flush=True)
    invalid = []
    baseline = doc['records'][0]
    for label,text in [('leading-space',' '+baseline['english']),('trailing-space',baseline['english']+' '),
        ('internal-gap',baseline['english'].replace(' ','  ',1)),('authored-LF','First\nSecond'),('NUL','First\0Second'),
        ('invented-printf','The flagship %s is captured!'),('layout-markup','Captured! {LB}'),('non-ASCII','Captured\u2014yes!'),('empty','')]:
        row = deepcopy(baseline)
        row['english'] = text
        try:
            compiled(row)
        except (AssertionError,ValueError):
            invalid.append(label)
        else:
            raise AssertionError(label)
    assert len(invalid)==9
    sheet = Image.new('RGB',(936,608),'#263238')
    draw = ImageDraw.Draw(sheet)
    for i,case in enumerate(cases):
        x,y = i%2*468,i//2*152
        draw.text((x+5,y+3),f"Voice{case['source_voice']} ID{case['message_ID']}",fill='white')
        with Image.open(case['preview']) as preview:
            sheet.paste(preview.resize((456,128),Image.Resampling.NEAREST),(x+5,y+22))
    image = ROOT/'all8_native_capture_voices.png'
    sheet.save(image)
    save(ROOT/'native_font_proof.json',{'ARM9_sha256':sha(arm),'COMMON_sha256':sha(common),
        'manuscript_sha256':sha(MANUSCRIPT.read_bytes()),'all206_existing_actor_choices':selections,
        'source_raw8_voice_table':table,'all8_effective_selections':expected,'cases':cases,'findings':findings,
        'only2015_prose_changed_other4_capture_alternatives_native_bytes_exact':True,
        '2011_target_native_bytes_match_the_prior_actual2011_GPU_holds':True,
        'CPU_only_counterfactual_physical_FirstMate_assignments':fixtures,
        'actual_role1_fallback16_used_without_assignment_in_voice1':True,'invalid_compiler_inputs_rejected':invalid,
        'review_sheet':str(image),'review_sheet_sha256':sha(image.read_bytes()),'visual_review_pending':True,
        'registered_release_new_candidate_actual_cache_loading_and_completion_pending':True,
        'producer_sha256':sha(Path(__file__).read_bytes()),'full_goal_complete':False})
    print(f'All8 capture voices/five unique native texts pass;{len(findings)} wrap findings;new registered release and gameplay remain pending.',flush=True)


if __name__=='__main__':
    main()
