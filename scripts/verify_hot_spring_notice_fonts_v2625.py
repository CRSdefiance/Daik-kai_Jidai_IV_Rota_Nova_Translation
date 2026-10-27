"""Current literal Experience notice and complete x0 native font plane."""
import textwrap
from pathlib import Path
from scripts import probe_inspection_status_fonts_v1574 as old
from scripts.current_common_native_context_v2620 import CurrentContext
from scripts.probe_common_single_cache_v862 import Loader
from scripts.hot_spring_notice_plan_v1632 import compiled
from scripts.verify_village_wrap_v608 import read,save
from dk4tool.patch.grand_race_menu_release import sha
ROOT=Path('work/analysis/hot_spring_notice_fonts_v2625')
DOC=Path('translations/hot_spring_notice_contextual_editorial_manuscript_v1.json')
if __name__=='__main__':
 ctx=CurrentContext(DOC,'out/all_routes_combined_v1676_candidate.nds',ROOT)
 source=textwrap.dedent(Path(old.__file__).read_text().split("if __name__=='__main__':\n",1)[1]);end=source.index('cases=[]')
 source="assert not any(raster(arm,b' ',0x01FFCE40-BASE,size=(228,64),instruction_limit=2000000))\n"+source[end:]
 source=source.replace("'wrong-ID','message_id',308","'wrong-ID','message_id',309")
 def pipeline(a,c,r,p,n):return ctx.execute(old.pipeline,n,raw=r)
 env={**old.__dict__,'__file__':__file__,'ROOT':ROOT,'DOC':DOC,'doc':read(DOC),'compiled':compiled,'arm':ctx.arm,'common':ctx.common,'rom':ctx.rom,'raw':ctx.raw,'plan':ctx.plan,'raster':ctx.raster,'pipeline':pipeline}
 exec(compile(source,__file__,'exec'),env)
 path=ROOT/'native_font_proof.json';proof=read(path);case=proof['cases'][0];gold=read('work/analysis/hot_spring_notice_fonts_v1633/native_font_proof.json')['cases'][0]
 for k in ['message_ID','compiled_hex','all_ordered_complete_native_glyph_events','zero_ink_pair_padding','native_plane_sha256']:assert case[k]==gold[k],k
 assert case['native_pipeline']['formatted_hex']==gold['native_pipeline']['formatted_hex']
 proof.update(candidate_sha256=sha(ctx.rompath.read_bytes()),all1_complete_native_cases=proof['cases'],all2_native_cold_warm_copies=[Loader(ctx.arm,ctx.common).copy(310,ctx.entries[310].text,mode)for mode in ['cold','warm']],review_sheets=[dict(path=proof['review_sheet'],sha256=proof['review_sheet_sha256'])],findings=[],complete_native_font_cases=1,all_current_literal_native_planes_golden_exact=True,all_executed_pipeline_instructions_current_ROM_byte_exact=True,all_original_actor_models_unchanged=True,blank_space_font_freshly_verified_zero_ink=True,pipeline_plan=str(ctx.proof_path),pipeline_plan_sha256=sha(ctx.proof_path.read_bytes()),scope='Current literal546B8 CPU pipeline and independent full228x64 font plane at original x0. No authored line break, argument or new gameplay.',full_goal_complete=False)
 save(path,proof);print('Notice310 current native literal pipeline/plane golden-exact;2cold/warm copies.')
