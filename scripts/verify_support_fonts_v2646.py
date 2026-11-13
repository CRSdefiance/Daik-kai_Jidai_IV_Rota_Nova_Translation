"""Current support687 matrices,142 full native planes and13 original pipelines."""
from pathlib import Path
from copy import deepcopy
from PIL import Image,ImageDraw
from scripts.current_common_native_context_v2620b import CurrentContext
from scripts.probe_reinforcement_sniping_layout_v1030 import native_layout,TABLES
from scripts.verify_arrival_native_v792 import prepared
from scripts.verify_shipyard_gameplay_v760 import independent_font
from scripts.search_reports_native_consumers_v1662 import assigned_role
from scripts.probe_common_single_cache_v862 import Loader
from scripts.reinforcement_sniping_layout_v1024 import compiled
from scripts.verify_village_wrap_v608 import read,save
from dk4tool.patch.grand_race_menu_release import sha
ROOT=Path('work/analysis/support_fonts_v2646');BASE=0x02000000
if __name__=='__main__':
 assert not ROOT.exists();ROOT.mkdir(parents=True)
 for label,name,ids,goldenpath,key in[('reinforcement','reinforcement_faction',list(range(1911,1917)),'work/analysis/reinforcement_faction_prose_v1802/six_paragraphs120_complete_native_cases.json','all120_cases'),('covering','covering_fire',list(range(1917,1924)),'work/analysis/covering_fire_current_v1818/current567_layouts_and22_native_planes.json','cases')]:
  dp=Path('translations')/f'{name}_contextual_editorial_manuscript_v1.json';doc=read(dp);ctx=CurrentContext(dp,'out/all_routes_combined_v1807_candidate.nds',ROOT/label);context=read(doc['native_context_proof']);golden=read(goldenpath);prior=golden[key];rows={r['message_id']:r for r in doc['records']};table=TABLES['reinforcement'if label=='reinforcement'else'covering_fire'];cpu=prepared(ctx.arm);font=ctx.rom.read_file('/GRP/KANJI.FNT');cases=[];samples=[];pipelines=[];findings=[]
  selected={max((i for i,c in enumerate(prior)if c['message_ID']==n),key=lambda i:len(prior[i]['formatted_hex']))for n in ids}
  if label=='covering':selected|={i for i,c in enumerate(prior)if c['argument_case']['hex'].startswith('8265')or(c['message_ID']==1917 and c['argument_case']['label']=='Manuel')}
  for index,old in enumerate(prior):
   n=old['message_ID'];argument=bytes.fromhex(old['argument_case']['hex']);text=compiled(rows[n]);assert text==ctx.entries[n].text;formatted,lines=native_layout(cpu,text,n,argument,table);assert formatted.hex()==old['formatted_hex']and lines==old['lines'];pixels=bytes(independent_font(ctx.arm,font,lines));assert 1<=len(lines)<=4 and all(0<len(s.encode('cp932'))<=35 for s in lines)
   if label=='covering':assert sha(pixels)==old['font_plane_sha256']
   weak=[i for i,s in enumerate(lines[:-1])if s.split()[-1].strip('.,!?;:').lower()in{'a','an','the','to','of','with','for','from','on','in','as','at'}];orphan=len(lines)>1 and len(lines[-1].split())==1;assert not weak and not orphan
   case=dict(message_ID=n,argument_case=old['argument_case'],formatted_hex=formatted.hex(),lines=lines,font_plane_sha256=sha(pixels),current_native_printf_wrap_ABI_and_guards_pass=True,current_independent_complete_plane_equals_prior=True,source_or_disclosed_stress_argument_preserved=True)
   if label=='reinforcement'or index in selected:
    events=[];fresh=bytes(ctx.raster(ctx.arm,formatted,0x01FFCE40-BASE,size=(228,64),instruction_limit=2000000,glyph_events=events));assert fresh==pixels
    if label=='reinforcement':
     image=Image.open(old['preview']).convert('L');assert sha(Path(old['preview']).read_bytes())==old['preview_sha256']and bytes(bool(p)for p in pixels)==bytes(v==0 for v in image.tobytes())
    # Ordered visible characters retain exact six-pixel ASCII/twelve-pixel CP932
    # advances. Only native zero-ink phase blanks may appear in between.
    guards=[]
    for y,line in enumerate(lines):
     actual=[e for e in events if e['y']==y*16];margin=[e for e in actual if e['x']<6];assert all(e['code']==32 and e['x']==0 for e in margin);actual=[e for e in actual if e['x']>=6];pos=0;x=6
     for j,char in enumerate(line):
      encoded=char.encode('cp932');code=int.from_bytes(encoded,'big')
      if code!=32 and actual[pos]['code']==32 and actual[pos]['x']==x:
       assert len(encoded)==2 or(y>0 and j==0);guards.append(actual[pos]);pos+=1
      assert actual[pos]['code']==code and(actual[pos]['x'],actual[pos]['y'])==(x,y*16);pos+=1;x+=6*len(encoded)
     assert x<=228 and all(e['code']==32 for e in actual[pos:])
    path=ROOT/label/f'ID{n}_case{index:03d}_native.png';Image.frombytes('L',(228,64),bytes(0 if p else255 for p in pixels)).save(path);case.update(fresh_native_full_plane_equal_independent=True,complete_ordered_glyph_events=events,zero_ink_phase_guards=guards,preview=str(path),preview_sha256=sha(path.read_bytes()))
    if index in selected:samples.append(case)
   cases.append(case)
  for n in ids:
   sample=next(c for c in samples if c['message_ID']==n);choices=next(t['all207_original_actor_choices']for t in context['voice_tables']if t['table']==table);rep=next(c for c in choices if c['actor_ID']==18 and c['message_ID']==n)if n in[1911,1917]else next(c for c in choices if c['message_ID']==n and c['actor_ID']!=1);raw,fixture=(ctx.raw,dict(no_roster_fixture=True,actual_logical_actor=18))if n in[1911,1917]else assigned_role(ctx.arm,ctx.raw,1,rep['actor_ID'],rep['actor_object']);native=ctx.speak(0x53D44,1,table,bytes.fromhex(sample['argument_case']['hex']),raw=raw);assert native['input_hex']==ctx.entries[n].text.hex()and native['formatted_hex']==sample['formatted_hex'];pipelines.append(dict(message_ID=n,native_pipeline=native,original_actor_choice=rep,CPU_only_voice_fixture=fixture))
  assert len(cases)==(120 if label=='reinforcement'else567)and len(samples)==(6 if label=='reinforcement'else22)and len(pipelines)==len(ids);invalid=[]
  for title,field,value in[('leading','english',' '+rows[ids[0]]['english']),('trailing','english',rows[ids[0]]['english']+' '),('gap','english','Ships  %s!'),('LF','english','Ships\n%s!'),('NUL','english','Ships\0%s!'),('layout','english','Ships %s {LB}!'),('nonASCII','english','Ships—%s!'),('missing-arg','english','Ships!'),('extra-arg','english','Ships %s %s!'),('percent','english','Ships %s 100%!'),('wrong-ID','message_id',1910),('wrong-argc','native_argument_count',0),('family','source_family','admiral_shot'),('macro','english','FI %s!'),('overflow','english','A'*220+'%s')]:
   row=deepcopy(rows[ids[0]]);row[field]=value
   try:compiled(row)
   except(ValueError,AssertionError):invalid.append(title)
   else:raise AssertionError(title)
  sheets=[]
  for start in range(0,len(samples),10):
   group=samples[start:start+10];sheet=Image.new('RGB',(936,152*((len(group)+1)//2)),'#263238');draw=ImageDraw.Draw(sheet)
   for i,c in enumerate(group):
    x,y=i%2*468,i//2*152;draw.text((x+5,y+3),f'ID{c["message_ID"]}: {c["argument_case"]["label"]}',fill='white');sheet.paste(Image.open(c['preview']).resize((456,128),Image.Resampling.NEAREST),(x+5,y+22))
   path=ROOT/label/f'native_review_sheet{start//10+1}.png';sheet.save(path);sheets.append(dict(path=str(path),sha256=sha(path.read_bytes())))
  proof=dict(candidate=str(ctx.rompath),candidate_sha256=sha(ctx.rompath.read_bytes()),ARM9_sha256=sha(ctx.arm),COMMON_sha256=sha(ctx.common),manuscript=str(dp),manuscript_sha256=sha(dp.read_bytes()),cases=cases,all_complete_native_cases=[next(c for c in samples if c['message_ID']==n)for n in ids],all_original_role1_speech_pipelines=pipelines,complete_native_font_cases=(120 if label=='reinforcement'else22),current_native_matrix_cases=len(cases),native_full_font_samples=len(samples),review_sheets=sheets,findings=findings,invalid_compiler_inputs_rejected=invalid,all_executed_pipeline_instructions_current_ROM_byte_exact=True,all_original_actor_models_unchanged=True,blank_space_font_freshly_verified_zero_ink=not any(ctx.raster(ctx.arm,b' ',0x01FFCE40-BASE,size=(228,64),instruction_limit=2000000)),pipeline_plan=str(ctx.proof_path),pipeline_plan_sha256=sha(ctx.proof_path.read_bytes()),golden_proof=goldenpath,golden_proof_sha256=sha(Path(goldenpath).read_bytes()),scope='Current complete native support paragraphs;reinforcement uses20full factions,covering uses81original compact-commander/regular-officer and explicit length/parity stress labels. Whole13original role1 pipelines execute current code;actual1911/1917 keep Charles18 raw unchanged,other11 voices use isolated original-setter duty bytes. Fullwidth Ｆernan/Ｆernando retain CP932 glyph/shadow bytes. No new actual visits,appointments,RNG or outcomes.',producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False);proof[f'all{len(ids)}_complete_native_cases']=proof['all_complete_native_cases'];proof[f'all{len(ids)*2}_native_cold_warm_copies']=[Loader(ctx.arm,ctx.common).copy(n,ctx.entries[n].text,mode)for mode in['cold','warm']for n in ids];save(ROOT/label/'native_font_proof.json',proof);print(label,len(cases),'matrix cases;',proof['complete_native_font_cases'],'current native font planes;',len(pipelines),'whole pipelines;no findings.',flush=True)
