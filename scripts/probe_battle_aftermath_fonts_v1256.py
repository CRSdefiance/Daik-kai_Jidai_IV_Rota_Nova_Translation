"""Original speech pipelines and complete 228x64 glyphs for aftermath prose.

All fixtures are CPU-only research. Role alternatives use original roster
setters and existing actor objects; no actor identity, RNG, result or emulator
event is injected. File success and portrait UI construction are boundaries.
"""
import struct
from pathlib import Path
from types import FunctionType

from PIL import Image, ImageDraw
from unicorn import UC_HOOK_CODE
from unicorn.arm_const import UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3, UC_ARM_REG_PC, UC_ARM_REG_SP, UC_ARM_REG_LR

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.duel_editorial import owned_entries
from dk4tool.rom.nds import NdsImage
from scripts.battle_aftermath_native_plan_v1255 import compiled, MANUSCRIPT
from scripts.battle_aftermath_runtime_v1253 import contract_rows
from scripts.native_call_abi_v764 import call
from scripts.probe_escape_direct_source_v1186 import machine as portrait_machine
from scripts.probe_button_prompt_native import BASE, STACK, STOP
from scripts.verify_personal_gameplay_v841 import get_machine
from scripts.verify_common_alignment_native_v257 import raster as original_raster
from scripts.verify_shipyard_gameplay_v760 import independent_font
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/battle_aftermath_fonts_v1256')
PLAN = Path('work/analysis/battle_aftermath_payload_v1255/native_payload_plan.json')
RUNTIME = Path('work/analysis/battle_aftermath_runtime_v1254c/native_runtime_verification.json')
CONTEXT = Path('work/analysis/battle_aftermath_context_v1248d/source_context_and_consumer_frames.json')
REGS = (UC_ARM_REG_R0,UC_ARM_REG_R1,UC_ARM_REG_R2,UC_ARM_REG_R3)


def consumer(arm,common,raw,plan,entry,actor_or_role,key,argument=None):
    cpu,get,provider = portrait_machine(arm,common,raw,plan)
    pointer = 0x02470000
    if argument is not None:
        assert len(argument) < 64 and b'\0' not in argument
        cpu.mem_write(pointer,argument+b'\0')
    seen = {}
    def observe(u,pc,size,unused):
        if pc == BASE+0x5408C:
            u.reg_write(UC_ARM_REG_PC,BASE+0x54144)
        elif pc == 0x01FFCF3C:
            sp = u.reg_read(UC_ARM_REG_SP)
            offset = 0x27C if entry == 0x53D44 else 0x274
            seen.update(parent=struct.unpack('<I',u.mem_read(sp+0x264,4))[0],
                selector_offset=offset,selector=struct.unpack('<I',u.mem_read(sp+offset,4))[0],
                input_hex=bytes(u.mem_read(u.reg_read(UC_ARM_REG_R1),512)).split(b'\0')[0].hex(),
                output=u.reg_read(UC_ARM_REG_R0))
        else:
            seen['formatted_hex'] = bytes(u.mem_read(seen['output'],512)).split(b'\0')[0].hex()
            u.emu_stop()
    for pc in (BASE+0x5408C,0x01FFCF3C,BASE+0x54164):
        cpu.hook_add(UC_HOOK_CODE,observe,begin=pc,end=pc)
    cpu.reg_write(UC_ARM_REG_SP,STACK)
    cpu.reg_write(UC_ARM_REG_LR,STOP)
    for reg,value in zip(REGS,(actor_or_role,key,pointer if argument is not None else 0,0)):
        cpu.reg_write(reg,value)
    cpu.emu_start(BASE+entry,STOP,count=3000000)
    assert cpu.reg_read(UC_ARM_REG_PC) == BASE+0x54164
    assert seen['parent'] == {0x53D44:0x02053DB8,0x53F0C:0x02053F40,0x53FE4:0x02054014}[entry]
    assert seen['selector'] == key
    return {**seen,'original_entry':BASE+entry,'file_reads':provider.reads,
        'original_native_selection_loader_printf_macro_and_scoped_formatter_execute':True,
        'CPU_file_success_and_UI_constructor_boundaries_not_gameplay':True}


def assigned_role_raw(arm,raw,actor_id,actor_object):
    cpu,get = get_machine(arm,raw)
    duty = get(0xCB1A8)+0x2090
    assert get(0x82428,duty,1) == 0 and get(0x82BC4,duty,15) == 208
    assert get(0x7EE08,actor_object) == actor_id
    get(0x82BB8,duty,15,actor_id)
    assert get(0x82428,duty,1) == actor_object
    changed = bytes(cpu.mem_read(BASE,0x400000))
    addresses = [BASE+i for i,(a,b) in enumerate(zip(raw,changed,strict=True)) if a != b]
    assert addresses == [duty+6+15]
    return changed,{'existing_actor_ID':actor_id,'actor_object':actor_object,
        'original_setter':BASE+0x82BB8,'original_type6_duty_slot':15,
        'only_original_roster_byte_changed':addresses,'raw_sha256':sha(changed),
        'all_actor_objects_IDs_RNG_and_other4MiB_bytes_exact':True,
        'CPU_counterfactual_duty_only_no_real_membership_or_emulator_event_claim':True}


def main():
    assert not ROOT.exists()
    plan,context,doc = read(PLAN),read(CONTEXT),read(MANUSCRIPT)
    runtime = read(RUNTIME)
    assert plan['manuscript_sha256'] == sha(MANUSCRIPT.read_bytes())
    arm,common = Path(plan['target_ARM9']).read_bytes(),Path(plan['target_COMMON']).read_bytes()
    assert sha(arm) == plan['target_ARM9_sha256'] and sha(common) == plan['target_COMMON_sha256']
    assert runtime['source_ARM9_sha256'] == plan['source_ARM9_sha256']
    raw = Path(context['snapshot']).read_bytes()
    assert sha(raw) == context['snapshot_sha256']
    current = NdsImage.open(doc['current_ROM'])
    entries = owned_entries(common,arm,plan['directory_sha256'])
    original_arm = current.read_file('/__arm9__.bin')
    clean_arm = NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    assert original_arm[0x82BA8:0x82BD0] == clean_arm[0x82BA8:0x82BD0]
    names = [{'kind':'source-native-town','town_index':t['town_index'],
        'name':t['town_name'],'hex':t['town_name_hex'],'source_getter':t['native_name_getter']}
        for t in context['all114_original_town_surrender_exchange_prefixes']]
    assert len(names) == 114 and max(len(bytes.fromhex(n['hex'])) for n in names) == 14
    for name in ('A','ABCDEFGHIJKLMNOPQRSTUVW','ABCDEFGHIJKLMNOPQRSTUVWXYZ12345','Long Harbor of the Eastern Isles','長崎'):
        names.append({'kind':'synthetic-layout-stress-not-real-town','town_index':None,
            'name':name,'hex':name.encode('cp932').hex(),'source_getter':None})
    tables = {t['table']:t for t in context['voice_tables']}
    representatives = {}
    for table,t in tables.items():
        for choice in t['all208_original_selections']:
            representatives.setdefault(choice['message_ID'],{**choice,'table':table})
    direct_keys = set(next(v for p,o,h,v in contract_rows() if p == 0x02053F40))
    numeric_speaker = context['all114_original_town_surrender_exchange_prefixes'][0]['original_calls'][1]['arguments'][0]
    role_fixtures, role_cache = [], {}
    class CurrentFont:
        @staticmethod
        def open(path):
            assert path == 'out/all_routes_combined_v255_candidate.nds'
            return current
    raster = FunctionType(original_raster.__code__,{**original_raster.__globals__,'NdsImage':CurrentFont},argdefs=original_raster.__defaults__)
    ROOT.mkdir(parents=True)
    previews = ROOT/'previews'
    previews.mkdir()
    cases,findings,review_cases = [],[],[]
    for row in doc['records']:
        n = row['message_id']
        value = compiled(row)
        assert entries[n].text == value and b'\n' not in value
        if n == 2192:
            entry,actor,key,assigned,fixture = 0x53FE4,numeric_speaker,n,raw,None
        else:
            source = representatives[n]
            key = source['table']
            if key in direct_keys:
                entry,actor,assigned,fixture = 0x53F0C,source['actor_object'],raw,None
            else:
                entry,actor = 0x53D44,1
                identity = source['actor_ID']
                if identity not in role_cache:
                    role_cache[identity] = assigned_role_raw(original_arm,raw,identity,source['actor_object'])
                    role_fixtures.append(role_cache[identity][1])
                assigned,fixture = role_cache[identity]
        variants = names if row['native_argument_count'] else [None]
        for index,name in enumerate(variants):
            argument = bytes.fromhex(name['hex']) if name else None
            native = consumer(arm,common,assigned,plan,entry,actor,key,argument)
            expected = value.replace(b'%s',argument) if name else value
            assert native['input_hex'] == expected.hex(),(n,name,native['input_hex'],expected.hex())
            formatted = bytes.fromhex(native['formatted_hex'])
            lines = [v.strip().decode('cp932') for v in formatted.split(b'\n')]
            assert ' '.join(lines) == expected.decode('cp932').strip(),(n,name,lines)
            assert 1 <= len(lines) <= 4 and all(len(t.encode('cp932')) <= 35 for t in lines),(n,name,lines)
            assert all(t == t.strip() and '  ' not in t for t in lines)
            pixels = raster(arm,formatted,0x01FFCE40-BASE,size=(228,64),instruction_limit=2000000)
            assert pixels == independent_font(arm,current.read_file('/GRP/KANJI.FNT'),lines),(n,name,lines)
            path = previews/f'ID{n}_variant{index:03d}_complete_native.png'
            Image.frombytes('L',(228,64),bytes(0 if p else 255 for p in pixels)).save(path)
            orphan = len(lines)>1 and len(lines[-1].split()) == 1
            weak = [i for i,line in enumerate(lines[:-1]) if line.split()[-1].strip('.,!?;:').lower() in {'a','an','the','to','of','with','for','from','on','in','as','at'}]
            result = {'message_id':n,'source_family':row['source_family'],'name_case':name,
                'native_pipeline':native,'compiled_hex':value.hex(),'native_formatted_hex':formatted.hex(),
                'lines':lines,'native_cell_widths':[len(t.encode('cp932')) for t in lines],
                'role_fixture':fixture,'whole228x64_native_independent_font_and_all_letters_equal':True,
                'first_and_continuation_visible_origins_x6_no_authored_alignment':True,
                'single_word_final_row':orphan,'weak_line_end_indices':weak,
                'preview':str(path),'preview_sha256':sha(path.read_bytes()),
                'CPU_only_not_original_gameplay_or_GPU_capture':True}
            cases.append(result)
            if name is None or index == 0 or name['kind'].startswith('synthetic') or name['name'] == 'Rio de Janeiro':
                review_cases.append(len(cases)-1)
            if orphan or weak:
                findings.append({'case_index':len(cases)-1,'message_id':n,'name_case':name,
                    'lines':lines,'single_word_final_row':orphan,'weak_line_end_indices':weak})
        print(str(n)+': '+str(len(variants))+' original-pipeline/full-native-font cases pass.',flush=True)
    assert len(cases) == 6*119+69 == 783
    sheets = []
    for start in range(0,len(review_cases),20):
        indices = review_cases[start:start+20]
        sheet = Image.new('RGB',(936,152*((len(indices)+1)//2)),'#263238')
        draw = ImageDraw.Draw(sheet)
        for slot,index in enumerate(indices):
            case = cases[index]
            x,y = slot%2*468,slot//2*152
            label = str(case['message_id'])+'; '+(case['name_case']['name'] if case['name_case'] else case['source_family'])
            draw.text((x+5,y+3),label,fill='white')
            with Image.open(case['preview']) as im:
                sheet.paste(im.resize((456,128),Image.Resampling.NEAREST),(x+5,y+22))
        path = ROOT/f'native_review_page{start//20+1:02d}.png'
        sheet.save(path)
        sheets.append({'path':str(path),'sha256':sha(path.read_bytes()),'case_indices':indices})
    save(ROOT/'native_font_proof.json',{'ARM9_sha256':sha(arm),'COMMON_sha256':sha(common),
        'manuscript':str(MANUSCRIPT),'manuscript_sha256':sha(MANUSCRIPT.read_bytes()),
        'payload_plan':str(PLAN),'payload_plan_sha256':sha(PLAN.read_bytes()),
        'native_runtime':str(RUNTIME),'native_runtime_sha256':sha(RUNTIME.read_bytes()),
        'source_context':str(CONTEXT),'source_context_sha256':sha(CONTEXT.read_bytes()),
        'all75_representative_original_source_pipelines_and783_full_font_cases':True,
        'all114_native_town_names_for_each_of6_templates':684,
        'synthetic_ASCII_and_CP932_name_stress_cases':30,'static_cases':69,
        'all_existing_actor_identity_RNG_and_results_unchanged_CPU_duty_variants':role_fixtures,
        'cases':cases,'line_boundary_findings_requiring_review':findings,'review_sheets':sheets,
        'visual_review_pending':True,'native_copy_release_patch_actual_scenes_and_transitions_pending':True,
        'no_formatting_approval_ROM_or_completion_credit':True,
        'producer_sha256':sha(Path(__file__).read_bytes()),'full_goal_complete':False})
    print('783 full original-pipeline/native-font cases pass; '+str(len(findings))+' boundary findings await review. No ROM built.',flush=True)


if __name__ == '__main__':
    main()
