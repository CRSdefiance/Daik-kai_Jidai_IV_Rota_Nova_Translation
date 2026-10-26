"""All16 source voice/table combinations and complete native independent fonts."""
from copy import deepcopy
from pathlib import Path
from types import FunctionType
from PIL import Image,ImageDraw
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.duel_editorial import owned_entries
from dk4tool.patch.grand_race_menu_release import sha
from scripts.hot_spring_native_plan_v1615 import compiled
from scripts.probe_battle_aftermath_fonts_v1256 import consumer,assigned_role_raw
from scripts.verify_personal_gameplay_v841 import get_machine
from scripts.verify_common_alignment_native_v257 import raster as original_raster
from scripts.verify_shipyard_gameplay_v760 import independent_font
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/hot_spring_fonts_v1617')
PLAN=Path('work/analysis/hot_spring_payload_v1615/native_payload_plan.json')
DOC=Path('translations/hot_spring_editorial_manuscript_v1.json')
BASE=0x02000000

if __name__=='__main__':
    assert not ROOT.exists()
    plan,doc=read(PLAN),read(DOC);assert sha(DOC.read_bytes())==plan['manuscript_sha256']
    context=read(doc['source_context']);assert sha(Path(doc['source_context']).read_bytes())==doc['source_context_sha256']
    raw=Path(context['snapshot']).read_bytes();assert sha(raw)==context['snapshot_sha256']
    arm,common=Path(plan['target_ARM9']).read_bytes(),Path(plan['target_COMMON']).read_bytes();entries=owned_entries(common,arm,plan['directory_sha256'])
    current=NdsImage.open(doc['current_ROM']);source_arm=current.read_file('/__arm9__.bin');rows={r['message_id']:r for r in doc['records']}
    class CurrentFont:
        @staticmethod
        def open(path):return current
    raster=FunctionType(original_raster.__code__,{**original_raster.__globals__,'NdsImage':CurrentFont},argdefs=original_raster.__defaults__)
    assert not any(raster(arm,b' ',0x01FFCE40-BASE,size=(228,64),instruction_limit=2000000))
    cpu,get=get_machine(source_arm,raw);actors,captain=get(0xCB184),get(0x7F244);cases=[];findings=[]
    ROOT.mkdir(parents=True)
    for table in context['voice_tables']:
        reps={}
        for choice in table['all207_existing_actor_choices']:
            if choice['existing_actor_ID']!=captain:reps.setdefault(choice['source_voice'],choice)
        assert set(reps)==set(range(8))
        for voice,rep in sorted(reps.items()):
            n=rep['resolved_message_ID'];row=rows[n];value=compiled(row);assert entries[n].text==value
            actor_id=rep['existing_actor_ID'];actor=actors+4+32*actor_id
            assigned,fixture=assigned_role_raw(source_arm,raw,actor_id,actor)
            check,query=get_machine(source_arm,assigned);assert query(0x82478,query(0xCB1A8)+0x2090,1)==actor_id
            native=consumer(arm,common,assigned,plan,0x53D44,1,table['table'])
            assert native['input_hex']==value.hex() and native['parent']==0x02053DB8 and native['selector_offset']==0x27C and native['selector']==table['table']
            formatted=bytes.fromhex(native['formatted_hex']);lines=[r.strip().decode('ascii') for r in formatted.split(b'\n')]
            assert ' '.join(lines)==row['english'] and 1<=len(lines)<=4
            assert all(0<len(line)<=35 and '  ' not in line for line in lines)
            events=[];pixels=raster(arm,formatted,0x01FFCE40-BASE,size=(228,64),instruction_limit=2000000,glyph_events=events)
            assert pixels==independent_font(arm,current.read_file('/GRP/KANJI.FNT'),lines)
            guards=[]
            for index,line in enumerate(lines):
                actual=[e for e in events if e['y']==16*index and 6<=e['x']<6+6*len(line)];blank=[]
                while actual and actual[0]['code']==32 and actual[0]['x']==6:blank.append(actual.pop(0))
                assert len(blank)<=1 and (not blank or index>0)
                assert [e['code'] for e in actual]==list(line.encode('ascii'))
                assert [e['x'] for e in actual]==[6+6*i for i in range(len(line))]
                assert actual[-1]['x']+6<=228
                guards.append({'row':index,'zero_ink_guard_events':blank})
            issues=[]
            if len(lines)>1 and len(lines[-1].split())==1:issues.append('isolated-final-word')
            weak=[i for i,line in enumerate(lines[:-1]) if line.split()[-1].strip('.,!?;:').lower() in {'a','an','the','to','of','with','for','from','on','in','as','at','and','or'}]
            if weak:issues.append('weak-line-ending')
            path=ROOT/f'ID{n}_voice{voice}_complete_native.png';Image.frombytes('L',(228,64),bytes(0 if p else 255 for p in pixels)).save(path)
            case={'message_ID':n,'source_table':table['table'],'source_voice':voice,'existing_actor_ID':actor_id,'CPU_only_role_fixture':fixture,
                'source_minus1_fallback_to_voice0':rep['uses_original_minus1_fallback_to_voice0'],'compiled_hex':value.hex(),'native_pipeline':native,'lines':lines,'findings':issues,
                'weak_line_end_indices':weak,'full228x64_native_and_independent_font_exact':True,'complete_ordered_glyph_events':events,
                'native_zero_ink_continuation_guards':guards,'complete_first_final_letters_uniform6px_margins_bounds_and_blank_paper_pass':True,
                'whole_native_font_plane_sha256':sha(bytes(pixels)),'preview':str(path),'preview_sha256':sha(path.read_bytes()),'CPU_counterfactual_not_original_hot_spring_gameplay':True}
            cases.append(case)
            if issues:findings.append({k:case[k] for k in ['message_ID','source_voice','lines','findings']})
    invalid=[];base=doc['records'][0]
    for label,field,value in [('leading-space','english',' '+base['english']),('trailing-space','english',base['english']+' '),
        ('internal-gap','english','Hot  spring!'),('LF','english','Hot\nspring!'),('NUL','english','Hot\0spring!'),
        ('invented-printf','english','Look at %s!'),('literal-percent','english','100% ready!'),('layout','english','Hot spring! {LB}'),
        ('empty','english',''),('non-ASCII','english','Hot spring\u2014yes!'),('long-contract','english','A'*160),('wrong-ID','message_id',2274),
        ('wrong-argc','native_argument_count',1),('invented-macro','source_native_macros',['IC']),('wrong-role','original_role',7),('wrong-table','source_table',0x021186E0)]:
        row=deepcopy(base);row[field]=value
        try:compiled(row)
        except (ValueError,AssertionError):invalid.append(label)
        else:raise AssertionError(label)
    sheet=Image.new('RGB',(936,152*8),'#263238');draw=ImageDraw.Draw(sheet)
    for j,case in enumerate(cases):
        x,y=j%2*468,j//2*152;draw.text((x+5,y+3),f'ID{case["message_ID"]} voice{case["source_voice"]} '+('fallback' if case['source_minus1_fallback_to_voice0'] else ''),fill='white')
        with Image.open(case['preview']) as preview:sheet.paste(preview.resize((456,128),Image.Resampling.NEAREST),(x+5,y+22))
    path=ROOT/'all16_hot_spring_native_review.png';sheet.save(path)
    save(ROOT/'native_font_research.json',{'manuscript':str(DOC),'manuscript_sha256':sha(DOC.read_bytes()),'plan':str(PLAN),'plan_sha256':sha(PLAN.read_bytes()),
        'ARM9_sha256':sha(arm),'COMMON_sha256':sha(common),'cases':cases,'findings':findings,'invalid_compiler_inputs_rejected':invalid,
        'all16_original_role1_selection_printf_macro_wrap_and_full_glyph_planes_verified':True,
        'all414_existing_actor_table_selections':[{k:v for k,v in t.items() if k in ['table','all207_existing_actor_choices']} for t in context['voice_tables']],
        'sheets_for_visual_review':[{'path':str(path),'sha256':sha(path.read_bytes())}],
        'visual_review_copies_registered_release_and_original_hot_spring_pending':True,'producer_sha256':sha(Path(__file__).read_bytes()),'full_goal_complete':False})
    print('All16 original voice/table combinations,13 complete native font planes and16 compiler negatives pass;findings:',findings)
