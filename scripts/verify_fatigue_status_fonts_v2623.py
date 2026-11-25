"""Current signed fatigue pipelines and all202 literal native font planes."""
from pathlib import Path
from types import FunctionType
from scripts import probe_fatigue_status_fonts_v1590 as old
from scripts.current_common_native_context_v2620 import CurrentContext
from scripts.verify_main_head_cache_v480 import Loader
from scripts.verify_village_wrap_v608 import read,save
from dk4tool.patch.grand_race_menu_release import sha
DOC=Path('translations/fatigue_status_contextual_editorial_manuscript_v1.json')
ROOT=Path('work/analysis/fatigue_status_fonts_v2623')
if __name__=='__main__':
 ctx=CurrentContext(DOC,'out/all_routes_combined_v1594_candidate.nds',ROOT)
 source=Path(old.__file__).read_text().split("if __name__=='__main__':\n",1)[1]
 import textwrap
 source=textwrap.dedent(source);start=source.index('assert not ROOT.exists()');end=source.index('cases=[];previews=[]')
 source="assert not any(raster(arm,b' ',0x01FFCE40-BASE,size=(228,64),instruction_limit=2000000))\ncpu,get,provider=machine(arm,common,raw,plan);zero_before=bytes(cpu.mem_read(BASE,0x400000));get(0x79728,0)\nassert bytes(cpu.mem_read(BASE,0x400000))==zero_before and not provider.reads\n"+source[end:]
 def pipeline(a,c,r,p,n,amount):return ctx.execute(old.pipeline,n,amount,raw=r)
 env={**old.__dict__,'__file__':__file__,'ROOT':ROOT,'DOC':DOC,'doc':read(DOC),'arm':ctx.arm,'common':ctx.common,'rom':ctx.rom,'raw':ctx.raw,'plan':ctx.plan,'raster':ctx.raster,'machine':ctx.machine,'pipeline':pipeline}
 exec(compile(source,__file__,'exec'),env)
 path=ROOT/'native_font_proof.json';proof=read(path);gold=read('work/analysis/fatigue_status_fonts_v1590/native_font_proof.json');assert len(proof['cases'])==len(gold['cases'])==202
 for a,b in zip(proof['cases'],gold['cases'],strict=True):
  for k in ['message_ID','amount','compiled_hex','english_expanded','all_ordered_real_glyphs','zero_ink_ASCII_to_CP932_transition_guards','zero_ink_final_pair_padding','native_plane_sha256']:assert a[k]==b[k],(a['message_ID'],a['amount'],k)
  for k in ['source_amount_hex','loaded_template_hex','formatted_hex','original_varargs_output_hex']:assert a['native_pipeline'][k]==b['native_pipeline'][k]
 assert all(bytes(cpu.mem_read(ctx.actor_root,0x1A04))==before for cpu,before in ctx.machines)
 proof.update(candidate_sha256=sha(ctx.rompath.read_bytes()),all2_complete_native_cases=[next(c for c in proof['cases']if c['message_ID']==n and c['amount']==(3 if n==308 else 10))for n in [308,309]],all4_native_cold_warm_copies=[Loader(ctx.arm,ctx.common).copy(n,ctx.entries[n].text,mode)for mode in ['cold','warm']for n in [308,309]],all202_current_signed_numeric_native_planes_golden_exact=True,complete_native_font_cases=202,all_executed_pipeline_instructions_current_ROM_byte_exact=True,all_original_actor_models_unchanged=True,blank_space_font_freshly_verified_zero_ink=True,findings=[],review_sheets=[dict(path=proof['review_sheet'],sha256=proof['review_sheet_sha256'])],pipeline_plan=str(ctx.proof_path),pipeline_plan_sha256=sha(ctx.proof_path.read_bytes()),scope='Current CPU full signed helper/COMMON printf/macro/native font cases, values0..100. Zero is formatting-only because original helper exits. Requested magnitude is preserved even at clamp. File IO is hosted; UI constructor is not executed. No new emulator visit.',full_goal_complete=False)
 save(path,proof);print('202 current full font cases golden-exact; 4 native cold/warm copies; zero helper preserves4MiB; actor models exact.')
