"""Original sinking speech pipelines and whole native glyph planes.

Existing actor selections and CPU-only First Mate assignment counterfactuals
exercise all voices. Synthetic names are stress cases, not proven UI limits.
"""
import struct
from pathlib import Path
from types import FunctionType
from copy import deepcopy
from PIL import Image,ImageDraw
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.duel_editorial import owned_entries
from dk4tool.rom.nds import NdsImage
from scripts.ship_sinking_native_plan_v1330 import IDS,compiled,paragraph
from scripts.probe_battle_aftermath_fonts_v1256 import consumer
from scripts.verify_common_alignment_native_v257 import raster as original_raster
from scripts.verify_shipyard_gameplay_v760 import independent_font
from scripts.verify_personal_gameplay_v841 import get_machine
from scripts.verify_village_wrap_v608 import read,save

ROOT = Path('work/analysis/ship_sinking_fonts_v1331')
PLAN = Path('work/analysis/ship_sinking_payload_v1330/native_payload_plan.json')
SCOPE = Path('work/analysis/ship_sinking_runtime_v1329/native_runtime_verification.json')
MANUSCRIPT = Path('translations/ship_sinking_editorial_manuscript_v1.json')
BASE = 0x02000000


def assigned(arm,raw,identity,actor):
    cpu,get = get_machine(arm,raw)
    duty = get(0xCB1A8)+0x2090
    assert get(0x7EE08,actor)==identity
    before = get(0x82BC4,duty,15)
    get(0x82BB8,duty,15,identity)
    assert get(0x82428,duty,1)==actor
    changed = bytes(cpu.mem_read(BASE,0x400000))
    delta = [BASE+i for i,(a,b) in enumerate(zip(raw,changed,strict=True)) if a!=b]
    assert delta==([] if identity==before else [duty+6+15])
    return changed,{'existing_actor_ID':identity,'actor_object':actor,'previous_duty_actor_ID':before,
        'original_setter':BASE+0x82BB8,'original_type6_slot':15,'only_roster_byte_delta':delta,
        'all_other4MiB_actor_IDs_RNG_objects_exact':True,'raw_sha256':sha(changed),
        'CPU_counterfactual_only_no_emulator_crew_membership_or_event_claim':True}


def main():
    assert not ROOT.exists()
    plan,doc,scope = read(PLAN),read(MANUSCRIPT),read(SCOPE)
    assert sha(MANUSCRIPT.read_bytes())==plan['manuscript_sha256']
    assert scope['source_ARM9_sha256']==plan['source_ARM9_sha256']
    arm,common = Path(plan['target_ARM9']).read_bytes(),Path(plan['target_COMMON']).read_bytes()
    assert sha(arm)==plan['target_ARM9_sha256'] and sha(common)==plan['target_COMMON_sha256']
    context = read(doc['source_context'])
    raw = Path(context['snapshot']).read_bytes()
    assert sha(raw)==context['snapshot_sha256']
    current = NdsImage.open(doc['current_ROM'])
    old_arm = current.read_file('/__arm9__.bin')
    entries = owned_entries(common,arm,plan['directory_sha256'])
    class CurrentFont:
        @staticmethod
        def open(path):
            assert path=='out/all_routes_combined_v255_candidate.nds'
            return current
    raster = FunctionType(original_raster.__code__,{**original_raster.__globals__,'NdsImage':CurrentFont},argdefs=original_raster.__defaults__)
    names = [{'kind':'original-live-ship-getter','name':n['name'],'hex':n['name_hex']} for n in context['original_live_ship_name_getters']]
    for text in ['F','ABCDEFGHIJKLMNOPQRSTUVW','ABCDEFGHIJKLMNOPQRSTUVWXYZ12345','Santa Maria','長崎丸']:
        names.append({'kind':'synthetic-font-stress-not-proven-name-editor-limit','name':text,'hex':text.encode('cp932').hex()})
    assert len(names)==6
    ROOT.mkdir(parents=True)
    previews = ROOT/'previews'
    previews.mkdir()
    cases,findings,fixtures = [],[],[]
    tables = {t['table']:t for t in context['voice_tables']}
    for row in doc['records']:
        number,table = row['message_id'],tables[row['source_table']]
        choices = [r for r in table['all206_existing_actor_selections'] if r['message_ID']==number]
        source = choices[0]
        preferred = 18 if number<2066 else 16
        source = next((r for r in choices if r['existing_actor_ID']==preferred),source)
        if number<2066:
            test_raw,fixture = assigned(old_arm,raw,source['existing_actor_ID'],source['actor_object'])
            fixtures.append(fixture)
            actor_or_role = 1
        else:
            test_raw,actor_or_role = raw,source['actor_object']
        value = compiled(row)
        assert value==entries[number].text and b'\n' not in value
        for variant,name in enumerate(names):
            argument = bytes.fromhex(name['hex'])
            native = consumer(arm,common,test_raw,plan,row['original_native_entry']-BASE,actor_or_role,row['source_table'],argument)
            assert native['parent']==row['original_native_parent'] and native['selector_offset']==row['selector_stack_offset']
            expected = value.replace(b'%s',argument)
            assert native['input_hex']==expected.hex(),(number,name,native)
            formatted = bytes.fromhex(native['formatted_hex'])
            lines = [line.strip().decode('cp932') for line in formatted.split(b'\n')]
            assert ' '.join(lines)==expected.decode('cp932').strip(),(number,name,lines)
            assert 1<=len(lines)<=4 and all(0<len(line.encode('cp932'))<=35 and '  ' not in line for line in lines)
            pixels = raster(arm,formatted,0x01FFCE40-BASE,size=(228,64),instruction_limit=2000000)
            assert pixels==independent_font(arm,current.read_file('/GRP/KANJI.FNT'),lines),(number,name,lines)
            path = previews/f'ID{number}_name{variant}_complete_native.png'
            Image.frombytes('L',(228,64),bytes(0 if p else 255 for p in pixels)).save(path)
            orphan = len(lines)>1 and len(lines[-1].split())==1
            weak = [i for i,line in enumerate(lines[:-1]) if line.split()[-1].strip('.,!?;:').lower() in {'a','an','the','to','of','with','for','from','on','in','as','at'}]
            case = {'message_id':number,'existing_actor_ID':source['existing_actor_ID'],'source_voice':source['source_voice'],
                'compiled_hex':value.hex(),'name_case':name,'native_pipeline':native,'native_formatted_hex':formatted.hex(),
                'lines':lines,'complete228x64_native_and_independent_font_equal':True,
                'uniform_visible_margin_complete_first_and_final_letters_and_bounds':True,
                'single_word_final_row':orphan,'weak_line_end_indices':weak,'preview':str(path),'preview_sha256':sha(path.read_bytes()),
                'CPU_only_not_actual_sinking_activation':True}
            cases.append(case)
            if orphan or weak:
                findings.append({'message_id':number,'name_case':name,'lines':lines,'single_word_final_row':orphan,'weak_line_end_indices':weak})
        print(f'ID{number}:six original substitution/macro/wrap/full-font cases pass.',flush=True)
    invalid = []
    baseline = doc['records'][0]
    for label,text in [('leading-space',' '+baseline['english']),('trailing-space',baseline['english']+' '),
        ('internal-alignment',baseline['english'].replace(' ','  ',1)),('authored-LF','Admiral,\n%s sank!'),
        ('NUL','Admiral, %s\0sank!'),('missing-argument','Admiral, the ship sank!'),
        ('extra-argument','Admiral, %s %s sank!'),('wrong-argument','Admiral, %d sank!'),
        ('literal-percent','Admiral, %s is 100% sunk!'),('layout-markup','Admiral, %s sank! {LB}'),
        ('non-ASCII','Admiral, %s sank\u2014help!'),('empty','')]:
        row = deepcopy(baseline)
        row['english'] = text
        try:
            paragraph(row)
        except ValueError:
            invalid.append(label)
        else:
            raise AssertionError(label)
    for label,field,value in [('wrong-family','message_id',2074),('argument-count','native_argument_count',2),('invented-macro','source_native_macros',['FI'])]:
        row = deepcopy(baseline)
        row[field] = value
        try:
            paragraph(row)
        except ValueError:
            invalid.append(label)
        else:
            raise AssertionError(label)
    assert len(cases)==96 and len(invalid)==15
    sheets = []
    for variant in [0,1,2,3,4,5]:
        sheet = Image.new('RGB',(936,1216),'#263238')
        draw = ImageDraw.Draw(sheet)
        selected = [c for c in cases if c['name_case']==names[variant]]
        assert len(selected)==16
        for i,case in enumerate(selected):
            x,y = i%2*468,i//2*152
            draw.text((x+5,y+3),f"ID{case['message_id']} voice{case['source_voice']} name{variant}",fill='white')
            with Image.open(case['preview']) as preview:
                sheet.paste(preview.resize((456,128),Image.Resampling.NEAREST),(x+5,y+22))
        path = ROOT/f'name{variant}_all16_native_review.png'
        sheet.save(path)
        sheets.append({'path':str(path),'sha256':sha(path.read_bytes())})
    save(ROOT/'native_font_proof.json',{'ARM9_sha256':sha(arm),'COMMON_sha256':sha(common),
        'manuscript_sha256':sha(MANUSCRIPT.read_bytes()),'cases':cases,'findings':findings,
        'all96_complete_native_substitution_macro_wrap_and_font_planes_equal':True,
        'all412_existing_actor_voice_choices_bound_in_source_context':True,
        'CPU_counterfactual_role_fixtures_entire4MiB_audited':fixtures,'invalid_compiler_inputs_rejected':invalid,
        'sheets_for_required_visual_review':sheets,'visual_review_and_name_editor_supported_limit_pending':True,
        'no_ROM_registry_gameplay_or_completion_approval':True,
        'producer_sha256':sha(Path(__file__).read_bytes()),'full_goal_complete':False})
    print(f'96 complete native font cases pass;{len(findings)} wrap findings for review. No gameplay or format approval granted.',flush=True)


if __name__=='__main__':
    main()
