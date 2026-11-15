"""Current32 whole direct-actor pipelines/fonts,copies andcompiler controls."""
from pathlib import Path
from copy import deepcopy
from PIL import Image,ImageDraw
from scripts.current_common_native_context_v2677 import CurrentContext
from scripts.battle_reaction_native_plan_v1484 import compiled,IDS
from scripts.verify_shipyard_gameplay_v760 import independent_font
from scripts.probe_common_single_cache_v862 import Loader
from scripts.verify_village_wrap_v608 import read,save
from dk4tool.patch.grand_race_menu_release import sha

ROOT=Path('work/analysis/battle_reactions_fonts_v2697');DOC=Path('translations/battle_reactions_contextual_editorial_manuscript_v1.json');BASE=0x02000000
if __name__=='__main__':
    assert not ROOT.exists();ctx=CurrentContext(DOC,'out/all_routes_combined_v1807_candidate.nds',ROOT);doc=read(DOC);source=read(doc['native_context_proof']);font=ctx.rom.read_file('/GRP/KANJI.FNT')
    oldpath=Path('work/analysis/battle_reaction_fonts_v1486/native_font_research.json');old=read(oldpath);gold={c['message_ID']:c for c in old['cases']};assert len(gold)==32 and old['findings']==[];cases=[]
    for row in doc['records']:
        n=row['message_id'];table=next(t for t in source['voice_tables'] if n in t['members']);choice=next(c for c in table['all207_original_actor_choices'] if c['message_ID']==n)
        value=compiled(row);assert value==ctx.entries[n].text;pipeline=ctx.speak(0x53F0C,choice['actor_object'],table['table']);cpu=ctx.machines[-1][0];owner=int.from_bytes(ctx.arm[0x552A0:0x552A4],'little');loaded=bytes(cpu.mem_read(owner+0x2030,512)).split(b'\0')[0]
        assert loaded==value and pipeline['input_hex']==value.hex() and pipeline['parent']==0x02053F40 and pipeline['selector']==table['table'];ctx.machines.pop()
        formatted=bytes.fromhex(pipeline['formatted_hex']);lines=[v.strip().decode('ascii') for v in formatted.split(b'\n')]
        assert ' '.join(lines)==row['english'] and 1<=len(lines)<=4 and all(0<len(line)<=35 for line in lines)
        weak=[i for i,line in enumerate(lines[:-1]) if line.split()[-1].strip('.,!?;:').lower() in {'a','an','the','to','of','with','for','from','on','in','as','at','and','or'}]
        assert not weak and not(len(lines)>1 and len(lines[-1].split())==1)
        events=[];pixels=bytes(ctx.raster(ctx.arm,formatted,0x01FFCE40-BASE,size=(228,64),instruction_limit=2000000,glyph_events=events));assert pixels==bytes(independent_font(ctx.arm,font,lines))
        for y,line in enumerate(lines):
            ev=[e for e in events if e['y']==16*y];assert all(e['code']==32 and e['x']==0 for e in ev if e['x']<6);actual=[e for e in ev if e['x']>=6];pos=0
            for j,char in enumerate(line):
                x=6+6*j
                if char!=' ' and actual[pos]['code']==32 and actual[pos]['x']==x:assert y>0 and j==0;pos+=1
                assert actual[pos]['code']==ord(char) and (actual[pos]['x'],actual[pos]['y'])==(x,16*y);pos+=1
            assert all(e['code']==32 for e in actual[pos:]) and 6+6*len(line)<=228
        reference=gold[n];assert formatted.hex()==reference['native_pipeline']['formatted_hex'] and lines==reference['lines'] and sha(pixels)==reference['whole_native_font_plane_sha256']
        path=ROOT/f'ID{n}_complete_native.png';Image.frombytes('L',(228,64),bytes(0 if p else 255 for p in pixels)).save(path)
        cases.append(dict(message_ID=n,compiled_hex=value.hex(),loaded_template_hex=loaded.hex(),native_pipeline=pipeline,lines=lines,original_actor_choice=choice,existing_actor_object_passed_directly_no_roster_fixture=True,complete_ordered_glyph_events=events,
            complete_native_and_independent_plane_equal=True,complete_ordered_glyphs_margins_blank_paper_and_bounds_pass=True,whole_native_font_plane_sha256=sha(pixels),all_prior_formatted_bytes_lines_and_full_palette_plane_equal=True,weak_line_end_indices=weak,single_word_final_row=False,preview=str(path),preview_sha256=sha(path.read_bytes())))
    invalid=[];baseline=doc['records'][0]
    for label,field,value in [('leading-space','english',' '+baseline['english']),('trailing-space','english',baseline['english']+' '),('gap','english','A  battle!'),('LF','english','A\nbattle!'),('NUL','english','A\0battle!'),('printf','english','A battle with %s!'),('percent','english','100% ready!'),('markup','english','A battle! {LB}'),('empty','english',''),('non-ASCII','english','A battle\u2014yes!'),('long-contract','english','A'*160),('wrong-ID','message_id',2146),('argument-count','native_argument_count',1),('macro','source_native_macros',['IC'])]:
        row=deepcopy(baseline);row[field]=value
        try:compiled(row)
        except (ValueError,AssertionError):invalid.append(dict(case=label,rejected=True))
        else:raise AssertionError(label)
    copies=[Loader(ctx.arm,ctx.common).copy(n,ctx.entries[n].text,mode) for mode in ['cold','warm'] for n in IDS];assert len(copies)==64 and len(invalid)==14 and not ctx.machines
    sheets=[]
    for start in [0,16]:
        sheet=Image.new('RGB',(936,1216),'#263238');draw=ImageDraw.Draw(sheet)
        for i,c in enumerate(cases[start:start+16]):
            x,y=i%2*468,i//2*152;draw.text((x+5,y+3),f'ID{c["message_ID"]}: current controlled native preview',fill='white');sheet.paste(Image.open(c['preview']).resize((456,128),Image.Resampling.NEAREST),(x+5,y+22))
        path=ROOT/f'current_native_sheet{start//16+1}.png';sheet.save(path);sheets.append(dict(path=str(path),sha256=sha(path.read_bytes())))
    save(ROOT/'native_font_and_pipeline_proof.json',dict(candidate=str(ctx.rompath),candidate_sha256=sha(ctx.rompath.read_bytes()),ARM9_sha256=sha(ctx.arm),COMMON_sha256=sha(ctx.common),manuscript=str(DOC),manuscript_sha256=sha(DOC.read_bytes()),cases=cases,all32_original_pipelines_and_full_native_independent_planes_pass=True,all32_prior_full_palette_planes_and_formatted_bytes_exact=True,all64_current_cold_warm_copies=copies,invalid_compiler_inputs=invalid,all_executed_pipeline_instructions_current_exact_and_actor_models_unchanged=True,all_source_native_arguments_remain_zero=True,findings=[],review_sheets=sheets,visual_review_pending=True,current_context_plan=str(ctx.proof_path),current_context_plan_sha256=sha(ctx.proof_path.read_bytes()),original_native_proof=str(oldpath),original_native_proof_sha256=sha(oldpath.read_bytes()),no_actual_selected_reaction_event_RNG_health_or_gameplay_change=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print('32current full pipelines/native planes match old full-palette cases;64copies/14compiler rejections pass.2sheets await review;no forced health/RNG/event orcompletion credit.')
