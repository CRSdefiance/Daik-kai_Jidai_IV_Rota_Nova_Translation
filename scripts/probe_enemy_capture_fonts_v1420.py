"""Full native capture font planes after exact-caller literal-name/wrap repair.

Record awkward wraps for further work rather than approving a merely safe fit.
Existing actor objects and original one-name printf path only. CPU file success
and portrait construction remain explicit boundaries,not gameplay claims.
"""
from copy import deepcopy
from pathlib import Path
from types import FunctionType
from PIL import Image,ImageDraw
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.duel_editorial import owned_entries
from dk4tool.rom.nds import NdsImage
from scripts.enemy_capture_native_plan_v1419 import compiled
from scripts.probe_battle_aftermath_fonts_v1256 import consumer
from scripts.verify_common_alignment_native_v257 import raster as original_raster
from scripts.verify_shipyard_gameplay_v760 import independent_font
from scripts.verify_village_wrap_v608 import read,save

ROOT = Path('work/analysis/enemy_capture_fonts_v1420')
PLAN = Path('work/analysis/enemy_capture_payload_v1419/native_payload_plan.json')
DOC = Path('translations/enemy_capture_editorial_manuscript_v1.json')

if __name__=='__main__':
    assert not ROOT.exists()
    plan,doc = read(PLAN),read(DOC)
    assert sha(DOC.read_bytes())==plan['manuscript_sha256']
    context = read(doc['source_context'])
    assert sha(Path(doc['source_context']).read_bytes())==doc['source_context_sha256']
    observed = context['prior_actual_2082']
    raw = Path(observed['snapshot']).read_bytes()
    assert sha(raw)==observed['snapshot_sha256']
    arm,common = Path(plan['target_ARM9']).read_bytes(),Path(plan['target_COMMON']).read_bytes()
    assert sha(arm)==plan['target_ARM9_sha256'] and sha(common)==plan['target_COMMON_sha256']
    entries = owned_entries(common,arm,plan['directory_sha256'])
    current = NdsImage.open(doc['current_ROM'])
    class CurrentFont:
        @staticmethod
        def open(path):
            assert path=='out/all_routes_combined_v255_candidate.nds'
            return current
    raster = FunctionType(original_raster.__code__,{**original_raster.__globals__,'NdsImage':CurrentFont},argdefs=original_raster.__defaults__)
    representatives = {}
    for source in context['all206_existing_actor_choices']:
        representatives.setdefault(source['source_voice'],source)
        if source['existing_actor_ID']==18:
            representatives[source['source_voice']] = source
    assert set(representatives)==set(range(8))
    bound_path = Path('work/analysis/ship_name_bound_v1335b/original_ship_rename_capacity.json')
    assert read(bound_path)['max_name_bytes_excluding_NUL']==18
    names = [b'Hanse Cog']+[b'F'+b'A'*(n-1) for n in range(1,19)]
    names += [s.encode('cp932') for s in ['FALCON','ICARUS','FIFOFOFU','Santa Maria',"F's Hope",'長崎丸'*3,'ＦＡＬＣＯＮ']]
    assert len(names)==26 and all(1<=len(n)<=18 for n in names)
    visual = [0,1,18,19,20,21,24,25]
    ROOT.mkdir(parents=True)
    cases,findings = [],[]
    for row in doc['records']:
        source = representatives[row['source_voice']]
        value = compiled(row)
        assert entries[row['message_id']].text==value
        for index,name in enumerate(names):
            native = consumer(arm,common,raw,plan,0x53F0C,source['actor_object'],context['source_table'],name)
            expected = value.replace(b'%s',name)
            assert native['input_hex']==expected.hex()
            formatted = bytes.fromhex(native['formatted_hex'])
            lines = [v.strip().decode('cp932') for v in formatted.split(b'\n')]
            assert ' '.join(lines)==expected.decode('cp932')
            assert 1<=len(lines)<=4 and all(0<len(v.encode('cp932'))<=35 and '  ' not in v for v in lines)
            events = []
            pixels = raster(arm,formatted,0x01FFCE40-0x02000000,size=(228,64),instruction_limit=2000000,glyph_events=events)
            assert pixels==independent_font(arm,current.read_file('/GRP/KANJI.FNT'),lines),(row['message_id'],index,lines)
            issues = []
            if len(lines)>1 and len(lines[-1].split())==1:
                issues.append('single-word-final-line-needs-editorial-layout-decision')
            weak = [i for i,v in enumerate(lines[:-1]) if v.split()[-1].strip('.,!?;:').lower() in
                {'a','an','the','to','of','with','for','from','on','in','as','at','and','or'}]
            if weak:
                issues.append('weak-line-ending')
            path = ROOT/f'ID{row["message_id"]}_name{index:02d}_complete_native.png' if index in visual else None
            if path:
                Image.frombytes('L',(228,64),bytes(0 if p else 255 for p in pixels)).save(path)
            case = {'message_ID':row['message_id'],'source_voice':source['source_voice'],
                'existing_actor_ID':source['existing_actor_ID'],'existing_actor_object':source['actor_object'],
                'variant':index,'name':name.decode('cp932'),'name_hex':name.hex(),
                'compiled_hex':value.hex(),'native_pipeline':native,'lines':lines,'findings':issues,
                'weak_line_end_indices':weak,'full228x64_native_and_independent_font_exact':True,
                'all_name_bytes_complete_leading_trailing_glyphs_uniform6px_margin_bounds_and_blank_paper_pass':True,
                'whole_native_font_plane_sha256':sha(bytes(pixels)),'complete_native_glyph_events':events,
                'preview':str(path) if path else None,'preview_sha256':sha(path.read_bytes()) if path else None,
                'CPU_only_not_original_GPU_or_individual_gameplay_activation':True}
            cases.append(case)
            if issues:
                findings.append({k:case[k] for k in ['message_ID','variant','name','lines','findings']})
        print(row['message_id'],'26 complete native font/name/margin/bounds cases pass',flush=True)
    invalid = []
    for label,field,value in [('leading-space','english',' '+doc['records'][0]['english']),
        ('trailing-space','english',doc['records'][0]['english']+' '),('internal-gap','english','Enemy  ship %s captured!'),
        ('LF','english','Enemy ship %s\ncaptured!'),('NUL','english','Enemy ship %s\0captured!'),
        ('missing-argument','english','Enemy ship captured!'),('extra-argument','english','%s and %s captured!'),
        ('wrong-argument','english','Enemy ship %d captured!'),('literal-percent','english','Enemy ship %s captured 100%!'),
        ('markup','english','Enemy ship %s captured! {LB}'),('empty','english',''),
        ('non-ASCII','english','Enemy ship %s captured\u2014yes!'),('wrong-ID','message_id',2090),
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
        sheet = Image.new('RGB',(936,608),'#263238');draw = ImageDraw.Draw(sheet)
        selected = [case for case in cases if case['variant']==variant]
        assert len(selected)==8
        for i,case in enumerate(selected):
            x,y = i%2*468,i//2*152
            draw.text((x+5,y+3),f'ID{case["message_ID"]} voice{case["source_voice"]} name{variant}',fill='white')
            with Image.open(case['preview']) as preview:
                sheet.paste(preview.resize((456,128),Image.Resampling.NEAREST),(x+5,y+22))
        path = ROOT/f'name{variant:02d}_all8_native_review.png';sheet.save(path)
        sheets.append({'path':str(path),'sha256':sha(path.read_bytes())})
    save(ROOT/'native_font_research.json',{'manuscript':str(DOC),'manuscript_sha256':sha(DOC.read_bytes()),
        'plan':str(PLAN),'plan_sha256':sha(PLAN.read_bytes()),'ARM9_sha256':sha(arm),'COMMON_sha256':sha(common),
        'cases':cases,'findings':findings,'invalid_compiler_inputs_rejected':invalid,
        'all208_original_selection_printf_macro_wrap_full_font_planes_verified':True,
        'all206_source_existing_actor_choices':context['all206_existing_actor_choices'],
        'captured_editor18_byte_bound_proof':str(bound_path),'captured_editor18_byte_bound_proof_sha256':sha(bound_path.read_bytes()),
        'byte_capacity_not_every_keyboard_page_or_legacy_name_reachability':True,
        'name_corruption_width_and_unequal_visible_margin_absent_in_all208_research_cases':True,
        'no_identity_role_RNG_result_or_emulator_mutation':True,'sheets_for_visual_review':sheets,
        'visual_review_layout_refinement_registered_release_and_original_gameplay_still_pending':True,
        'producer_sha256':sha(Path(__file__).read_bytes()),'full_goal_complete':False})
    print('208 full font planes and15 compiler rejection cases pass;layout findings',len(findings),';no completion approval.',flush=True)
