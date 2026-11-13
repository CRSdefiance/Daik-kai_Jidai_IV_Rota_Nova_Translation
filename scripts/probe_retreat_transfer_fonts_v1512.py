"""Eight original voice selections,26 ship names and208 full native font planes."""
from copy import deepcopy
from pathlib import Path
from types import FunctionType
from PIL import Image,ImageDraw
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.duel_editorial import owned_entries
from dk4tool.patch.grand_race_menu_release import sha
from scripts.retreat_transfer_native_plan_v1511b import compiled
from scripts.probe_battle_aftermath_fonts_v1256 import consumer,assigned_role_raw
from scripts.verify_common_alignment_native_v257 import raster as original_raster
from scripts.verify_shipyard_gameplay_v760 import independent_font
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/retreat_transfer_fonts_v1512')
PLAN=Path('work/analysis/retreat_transfer_payload_v1511b/native_payload_plan.json')
DOC=Path('translations/retreat_transfer_editorial_manuscript_v1.json')

if __name__=='__main__':
    assert not ROOT.exists()
    plan,doc=read(PLAN),read(DOC);assert sha(DOC.read_bytes())==plan['manuscript_sha256']
    context=read(doc['source_context']);assert sha(Path(doc['source_context']).read_bytes())==doc['source_context_sha256']
    raw=Path(context['snapshot']).read_bytes();assert sha(raw)==context['snapshot_sha256']
    arm,common=Path(plan['target_ARM9']).read_bytes(),Path(plan['target_COMMON']).read_bytes()
    assert sha(arm)==plan['target_ARM9_sha256'] and sha(common)==plan['target_COMMON_sha256']
    entries=owned_entries(common,arm,plan['directory_sha256']);current=NdsImage.open(doc['current_ROM'])
    class CurrentFont:
        @staticmethod
        def open(path):
            assert path=='out/all_routes_combined_v255_candidate.nds'
            return current
    raster=FunctionType(original_raster.__code__,{**original_raster.__globals__,'NdsImage':CurrentFont},argdefs=original_raster.__defaults__)
    representatives={}
    for choice in context['all206_existing_actor_choices']:
        voice=choice['source_voice'];representatives.setdefault(voice,choice)
        if choice['existing_actor_ID']==16:representatives[voice]=choice
    assert set(representatives)==set(range(8)) and representatives[1]['existing_actor_ID']==16
    rows={r['message_id']:r for r in doc['records']}
    bound_path=Path('work/analysis/ship_name_bound_v1335b/original_ship_rename_capacity.json')
    assert read(bound_path)['max_name_bytes_excluding_NUL']==18
    names=[b'Latina']+[b'F'+b'A'*(n-1) for n in range(1,19)]
    names += [s.encode('cp932') for s in ['FALCON','ICARUS','FIFOFOFU','Santa Maria',"F's Hope",'長崎丸'*3,'ＦＡＬＣＯＮ']]
    assert len(names)==26 and all(1<=len(n)<=18 for n in names)
    visual=[0,1,18,19,20,21,24,25]
    ROOT.mkdir(parents=True);cases=[];findings=[];fixtures=[]
    for voice,choice in sorted(representatives.items()):
        n=choice['message_ID'];row=rows[n];identity=choice['existing_actor_ID'];value=compiled(row)
        assert entries[n].text==value
        if voice==1:assigned,fixture=raw,None
        else:
            assigned,fixture=assigned_role_raw(current.read_file('/__arm9__.bin'),raw,identity,choice['actor_object'])
            fixtures.append(fixture)
        for index,name in enumerate(names):
            native=consumer(arm,common,assigned,plan,0x53D44,1,context['source_table'],name)
            expected=value.replace(b'%s',name);assert native['input_hex']==expected.hex()
            assert native['parent']==0x02053DB8 and native['selector_offset']==0x27C and native['selector']==0x02117080
            formatted=bytes.fromhex(native['formatted_hex']);lines=[s.strip().decode('cp932') for s in formatted.split(b'\n')]
            assert ' '.join(lines)==expected.decode('cp932')
            assert 1<=len(lines)<=4 and all(0<len(s.encode('cp932'))<=35 and '  ' not in s for s in lines)
            events=[];pixels=raster(arm,formatted,0x01FFCE40-0x02000000,size=(228,64),instruction_limit=2000000,glyph_events=events)
            assert pixels==independent_font(arm,current.read_file('/GRP/KANJI.FNT'),lines)
            issues=[];atomic=len(lines)>1 and lines[-1]==name.decode('cp932')+'!' and len(name)>=8
            if len(lines)>1 and len(lines[-1].split())==1 and not atomic:issues.append('isolated-non-name-final-word')
            weak=[i for i,s in enumerate(lines[:-1]) if s.split()[-1].strip('.,!?;:').lower() in {'a','an','the','to','of','with','for','from','on','in','as','at','and','or'}]
            if weak:issues.append('weak-line-ending')
            path=ROOT/f'voice{voice}_ID{n}_name{index:02d}_complete_native.png' if index in visual else None
            if path:Image.frombytes('L',(228,64),bytes(0 if p else 255 for p in pixels)).save(path)
            case={'message_ID':n,'source_voice':voice,'existing_actor_ID':identity,'actor_object':choice['actor_object'],
                'CPU_only_role_fixture':fixture,'variant':index,'name_hex':name.hex(),'name':name.decode('cp932'),
                'compiled_hex':value.hex(),'native_pipeline':native,'lines':lines,'findings':issues,'weak_line_end_indices':weak,
                'complete_atomic_name_on_final_row':atomic,'full228x64_native_and_independent_font_exact':True,
                'all_literal_name_bytes_complete_first_final_letters_uniform6px_margins_bounds_and_blank_paper_pass':True,
                'complete_native_glyph_events':events,'whole_native_font_plane_sha256':sha(bytes(pixels)),
                'preview':str(path) if path else None,'preview_sha256':sha(path.read_bytes()) if path else None,
                'CPU_only_not_revised_gameplay_or_earned_membership':True}
            cases.append(case)
            if issues:findings.append({k:case[k] for k in ['message_ID','source_voice','variant','name','lines','findings']})
        print('voice',voice,'ID',n,':26 native literal-name/full-font cases pass',flush=True)
    invalid=[]
    for label,field,value in [('leading-space','english',' '+doc['records'][0]['english']),('trailing-space','english',doc['records'][0]['english']+' '),
        ('internal-gap','english','Get  aboard %s!'),('LF','english','Get aboard\n%s!'),('NUL','english','Get aboard\0%s!'),
        ('missing-argument','english','Get aboard!'),('extra-argument','english','%s and %s!'),('wrong-argument','english','Get aboard %d!'),
        ('literal-percent','english','Get aboard %s,100%!'),('markup','english','Get aboard %s! {LB}'),('empty','english',''),
        ('non-ASCII','english','Get aboard %s\u2014now!'),('wrong-ID','message_id',2690),('wrong-argument-count','native_argument_count',0),
        ('invented-macro','source_native_macros',['FI'])]:
        row=deepcopy(doc['records'][0]);row[field]=value
        try:compiled(row)
        except (ValueError,AssertionError):invalid.append(label)
        else:raise AssertionError(label)
    sheets=[]
    for variant in visual:
        sheet=Image.new('RGB',(936,608),'#263238');draw=ImageDraw.Draw(sheet)
        selected=[r for r in cases if r['variant']==variant];assert len(selected)==8
        for i,case in enumerate(selected):
            x,y=i%2*468,i//2*152;draw.text((x+5,y+3),f'ID{case["message_ID"]} voice{case["source_voice"]} name{variant}',fill='white')
            with Image.open(case['preview']) as preview:sheet.paste(preview.resize((456,128),Image.Resampling.NEAREST),(x+5,y+22))
        path=ROOT/f'name{variant:02d}_all8_voices_native_review.png';sheet.save(path);sheets.append({'path':str(path),'sha256':sha(path.read_bytes())})
    save(ROOT/'native_font_research.json',{'manuscript':str(DOC),'manuscript_sha256':sha(DOC.read_bytes()),
        'plan':str(PLAN),'plan_sha256':sha(PLAN.read_bytes()),'ARM9_sha256':sha(arm),'COMMON_sha256':sha(common),
        'cases':cases,'findings':findings,'invalid_compiler_inputs_rejected':invalid,'CPU_only_role_counterfactuals_entire4MiB_audited':fixtures,
        'all208_original_role_voice_printf_macro_wrap_full_font_planes_verified':True,
        'source_voice3_original_negative_member_falls_back_to2683_without_identity_or_source_table_changes':True,
        'all206_source_existing_actor_choices':context['all206_existing_actor_choices'],'sheets_for_visual_review':sheets,
        'source_name_bound_proof':str(bound_path),'source_name_bound_proof_sha256':sha(bound_path.read_bytes()),
        'visual_refinement_copy_cache_release_and_revised_actual_transfer_still_pending':True,
        'producer_sha256':sha(Path(__file__).read_bytes()),'full_goal_complete':False})
    print('208 complete literal-name/font cases,15 compiler rejections;layout findings',len(findings),';no approval yet.')
