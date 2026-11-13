"""624 original role1 name/macro/wrap/full-font cases;record layout findings."""
from copy import deepcopy
from pathlib import Path
from types import FunctionType
from PIL import Image,ImageDraw
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.duel_editorial import owned_entries
from dk4tool.rom.nds import NdsImage
from scripts.ship_loss_surrender_native_plan_v1444b import compiled
from scripts.probe_battle_aftermath_fonts_v1256 import consumer,assigned_role_raw
from scripts.verify_common_alignment_native_v257 import raster as original_raster
from scripts.verify_shipyard_gameplay_v760 import independent_font
from scripts.verify_village_wrap_v608 import read,save

ROOT = Path('work/analysis/ship_loss_surrender_fonts_v1445')
PLAN = Path('work/analysis/ship_loss_surrender_payload_v1444b/native_payload_plan.json')
DOC = Path('translations/ship_loss_surrender_editorial_manuscript_v1.json')

def main():
    assert not ROOT.exists()
    plan,doc = read(PLAN),read(DOC)
    assert sha(DOC.read_bytes())==plan['manuscript_sha256']
    context = read(doc['source_context'])
    assert sha(Path(doc['source_context']).read_bytes())==doc['source_context_sha256']
    raw = Path(context['snapshot']).read_bytes();assert sha(raw)==context['snapshot_sha256']
    arm,common = Path(plan['target_ARM9']).read_bytes(),Path(plan['target_COMMON']).read_bytes()
    assert sha(arm)==plan['target_ARM9_sha256'] and sha(common)==plan['target_COMMON_sha256']
    entries = owned_entries(common,arm,plan['directory_sha256']);current = NdsImage.open(doc['current_ROM'])
    old_arm = current.read_file('/__arm9__.bin')
    class CurrentFont:
        @staticmethod
        def open(path):
            assert path=='out/all_routes_combined_v255_candidate.nds'
            return current
    raster = FunctionType(original_raster.__code__,{**original_raster.__globals__,'NdsImage':CurrentFont},argdefs=original_raster.__defaults__)
    representatives = {}
    for family in context['families']:
        for source in family['all206_existing_actor_choices']:
            n = source['message_ID']
            representatives.setdefault(n,source)
            if source['existing_actor_ID'] in [16,18]:
                representatives[n] = source
    assert len(representatives)==24
    bound_path = Path('work/analysis/ship_name_bound_v1335b/original_ship_rename_capacity.json')
    assert read(bound_path)['max_name_bytes_excluding_NUL']==18
    tail = [b'F'+b'A'*(n-1) for n in range(1,19)]
    tail += [s.encode('cp932') for s in ['FALCON','ICARUS','FIFOFOFU','Santa Maria',"F's Hope",'長崎丸'*3,'ＦＡＬＣＯＮ']]
    assert len(tail)==25 and all(1<=len(n)<=18 for n in tail)
    visual = [0,1,18,19,20,21,24,25]
    ROOT.mkdir(parents=True)
    cases,findings,fixtures,assigned_cache = [],[],[],{}
    for row in doc['records']:
        n = row['message_id'];source = representatives[n]
        identity = source['existing_actor_ID']
        if source['source_voice']==1:
            assert identity==16
            assigned,fixture = raw,None
        else:
            if identity not in assigned_cache:
                assigned_cache[identity] = assigned_role_raw(old_arm,raw,identity,source['actor_object'])
                fixtures.append(assigned_cache[identity][1])
            assigned,fixture = assigned_cache[identity]
        value = compiled(row);assert entries[n].text==value
        names = [b'Vestaros' if n<2098 else b'Hanse Cog']+tail
        for index,name in enumerate(names):
            native = consumer(arm,common,assigned,plan,0x53D44,1,row['source_table'],name)
            expected = value.replace(b'%s',name)
            assert native['input_hex']==expected.hex()
            assert native['parent']==row['original_native_parent'] and native['selector_offset']==row['selector_stack_offset']
            formatted = bytes.fromhex(native['formatted_hex'])
            lines = [v.strip().decode('cp932') for v in formatted.split(b'\n')]
            assert ' '.join(lines)==expected.decode('cp932')
            assert 1<=len(lines)<=4 and all(0<len(v.encode('cp932'))<=35 and '  ' not in v for v in lines)
            events = []
            pixels = raster(arm,formatted,0x01FFCE40-0x02000000,size=(228,64),instruction_limit=2000000,glyph_events=events)
            assert pixels==independent_font(arm,current.read_file('/GRP/KANJI.FNT'),lines),(n,index,lines)
            issues = []
            atomic_name = len(lines)>1 and lines[-1] in [name.decode('cp932')+'!',name.decode('cp932')+'.'] and len(name)>=8
            if len(lines)>1 and len(lines[-1].split())==1 and not atomic_name:
                issues.append('isolated-non-name-final-word')
            weak = [i for i,v in enumerate(lines[:-1]) if v.split()[-1].strip('.,!?;:').lower() in
                {'a','an','the','to','of','with','for','from','on','in','as','at','and','or'}]
            if weak:
                issues.append('weak-line-ending')
            path = ROOT/f'ID{n}_name{index:02d}_complete_native.png' if index in visual else None
            if path:
                Image.frombytes('L',(228,64),bytes(0 if p else 255 for p in pixels)).save(path)
            case = {'message_ID':n,'source_family':row['source_family'],'source_voice':source['source_voice'],
                'existing_actor_ID':identity,'existing_actor_object':source['actor_object'],'CPU_role_fixture':fixture,
                'variant':index,'name':name.decode('cp932'),'name_hex':name.hex(),'compiled_hex':value.hex(),
                'native_pipeline':native,'lines':lines,'findings':issues,'weak_line_end_indices':weak,
                'full228x64_native_and_independent_font_exact':True,
                'complete_name_leading_trailing_letters_uniform6px_margin_bounds_and_blank_paper_pass':True,
                'complete_atomic_runtime_name_on_final_row':atomic_name,
                'whole_native_font_plane_sha256':sha(bytes(pixels)),'complete_native_glyph_events':events,
                'preview':str(path) if path else None,'preview_sha256':sha(path.read_bytes()) if path else None,
                'CPU_only_not_original_event_or_individual_gameplay_activation':True}
            cases.append(case)
            if issues:
                findings.append({k:case[k] for k in ['message_ID','variant','name','lines','findings']})
        print(n,'26 complete original role/name/font cases pass',flush=True)
    invalid = []
    for label,field,value in [('leading-space','english',' '+doc['records'][0]['english']),
        ('trailing-space','english',doc['records'][0]['english']+' '),('internal-gap','english','Admiral,  %s surrendered!'),
        ('LF','english','Admiral, %s\nsurrendered!'),('NUL','english','Admiral, %s\0surrendered!'),
        ('missing-argument','english','Admiral, the ship surrendered!'),('extra-argument','english','%s and %s surrendered!'),
        ('wrong-argument','english','Admiral, %d surrendered!'),('literal-percent','english','Admiral, %s surrendered 100%!'),
        ('markup','english','Admiral, %s surrendered! {LB}'),('empty','english',''),
        ('non-ASCII','english','Admiral, %s surrendered\u2014yes!'),('wrong-ID','message_id',2082),
        ('wrong-argument-count','native_argument_count',0),('invented-macro','source_native_macros',['FI'])]:
        row = deepcopy(doc['records'][0]);row[field] = value
        try:
            compiled(row)
        except (ValueError,AssertionError):
            invalid.append(label)
        else:
            raise AssertionError(label)
    sheets = []
    for variant in visual:
        sheet = Image.new('RGB',(1404,1216),'#263238');draw = ImageDraw.Draw(sheet)
        selected = [case for case in cases if case['variant']==variant];assert len(selected)==24
        for i,case in enumerate(selected):
            x,y = i%3*468,i//3*152
            draw.text((x+5,y+3),f'ID{case["message_ID"]} voice{case["source_voice"]} name{variant}',fill='white')
            with Image.open(case['preview']) as preview:
                sheet.paste(preview.resize((456,128),Image.Resampling.NEAREST),(x+5,y+22))
        path = ROOT/f'name{variant:02d}_all24_native_review.png';sheet.save(path)
        sheets.append({'path':str(path),'sha256':sha(path.read_bytes())})
    save(ROOT/'native_font_research.json',{'manuscript':str(DOC),'manuscript_sha256':sha(DOC.read_bytes()),
        'plan':str(PLAN),'plan_sha256':sha(PLAN.read_bytes()),'ARM9_sha256':sha(arm),'COMMON_sha256':sha(common),
        'cases':cases,'findings':findings,'invalid_compiler_inputs_rejected':invalid,
        'all624_original_role_selection_printf_macro_wrap_full_font_planes_verified':True,
        'all618_source_existing_actor_choices':[v for f in context['families'] for v in f['all206_existing_actor_choices']],
        'CPU_only_role_counterfactuals_entire4MiB_audited':fixtures,
        'actual_logical_member16_with_empty_physical_FirstMate_used_for_all3_voice1_reports':True,
        'captured_editor18_byte_bound_proof':str(bound_path),'captured_editor18_byte_bound_proof_sha256':sha(bound_path.read_bytes()),
        'byte_capacity_not_every_keyboard_page_or_legacy_name_reachability':True,
        'no_identity_RNG_result_or_emulator_mutation':True,'sheets_for_visual_review':sheets,
        'visual_review_layout_refinement_registered_release_and_original_gameplay_still_pending':True,
        'producer_sha256':sha(Path(__file__).read_bytes()),'full_goal_complete':False})
    print('624 full native font cases and15 compiler rejections pass;layout findings',len(findings),';no approval.',flush=True)

if __name__=='__main__':
    main()
