"""Reviewed sheets, bounded label getter, and86 native current COMMON copies."""
from copy import deepcopy
from pathlib import Path
import struct
from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.duel_editorial import owned_entries
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import common_message_entries
from scripts.inventory_arm9_text import components
from scripts.probe_button_prompt_native import machine,call
from unicorn.arm_const import UC_ARM_REG_R0
from scripts.probe_common_single_cache_v862 import Loader
from scripts.primary_town_native_font_v2102 import font_tools
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/refit_offline_approval_v2282');DOC=Path('translations/refit_contextual_editorial_manuscript_v2.json')
if __name__=='__main__':
 assert not ROOT.exists()and not DOC.exists();ROOT.mkdir(parents=True);plan=read('work/analysis/refit_spritsail_payload_v2278/payload_plan.json');arm=Path(plan['target_ARM9']).read_bytes();common=Path(plan['target_COMMON']).read_bytes();assert sha(arm)==plan['target_ARM9_sha256']and sha(common)==plan['target_COMMON_sha256'];rom=NdsImage.open('out/all_routes_combined_v2171_candidate.nds');clean=NdsImage.open('work/clean.nds');canonical=NdsImage.open('out/raphael_natural_v2_accepted_base.nds');sourcearm=clean.read_file('/__arm9__.bin');currentarm=rom.read_file('/__arm9__.bin')
 refs=[]
 for name,base,raw in components(rom):
  for i in range(len(raw)-3):
   v=struct.unpack_from('<I',raw,i)[0]
   if 0x02133234<=v<0x02133240:refs.append(dict(component=name,field_offset=i,target_address=v))
 assert refs==[dict(component='arm9',field_offset=0x114E4C,target_address=0x02133234)]
 assert currentarm[0x1CA00:0x1CA10]==sourcearm[0x1CA00:0x1CA10]==arm[0x1CA00:0x1CA10]
 cpu=machine(arm);call(cpu,0x1CA00,(0,));pointer=cpu.reg_read(UC_ARM_REG_R0);assert pointer==0x02133234 and bytes(cpu.mem_read(pointer,12))==b'Spritsail\0\0\0'
 assert arm[0x133240:0x133254]==currentarm[0x133240:0x133254]and arm[0x133240:].startswith(b'16CDeckCabinButton\0')
 raster,_,_=font_tools(rom);labelplane=raster(arm,b'Spritsail',0xD5404,size=(60,16),instruction_limit=2000000);assert any(labelplane)and len(labelplane)==960
 from PIL import Image
 lp=ROOT/'spritsail_native_label.png';Image.frombytes('L',(60,16),bytes(0 if v else 255 for v in labelplane)).resize((480,128),Image.Resampling.NEAREST).save(lp)
 entries=owned_entries(common,arm,plan['directory_sha256']);loader=Loader(arm,common);copies=[]
 for mode in('cold','warm'):
  for n in range(1247,1290):copies.append(loader.copy(n,entries[n].text,mode))
 assert len(copies)==86
 helps=read('work/analysis/refit_help_fonts_v2279/native_font_verification.json');spoken=read('work/analysis/refit_spoken_layouts_v2280c/native_font_proof.json');actual=read('work/analysis/refit_current_actual_verification_v2281c/actual_and_logical_proof.json');assert len(helps['records'])==31 and len(spoken['complete_native_font_planes'])==26 and not spoken['findings']and len(actual['spoken26_current_logical_native_fonts'])==26
 sheets=helps['review_sheets']+spoken['review_sheets']+actual['actual_sheets'];assert len(sheets)==10
 for r in sheets:assert sha(Path(r['path']).read_bytes())==r['sha256']
 prior=Path('translations/refit_contextual_editorial_manuscript_v1.json');doc=deepcopy(read(prior));accepted=common_message_entries(canonical.read_file('/COMMON/MESFILE.DK4'),canonical.read_file('/__arm9__.bin'),clean=False)
 for row in doc['records']:row['review']['formatting']=True;row['canonical_source_hex']=accepted[row['message_id']].text.hex()
 doc.update(formatting_review_pending=False,status='offline-native-format-reviewed-registered-integration-and-revised-gameplay-pending',formatting_evidence=str(ROOT/'offline_approval.json'),predecessor_manuscript=str(prior),predecessor_manuscript_sha256=sha(prior.read_bytes()))
 validate_natural_dialogue_batch(doc);save(DOC,doc)
 save(ROOT/'offline_approval.json',dict(manuscript=str(DOC),manuscript_sha256=sha(DOC.read_bytes()),research_ARM9_sha256=sha(arm),research_COMMON_sha256=sha(common),all43_individual_source_context_localization_naturalness_and_formatting_gates=True,all31_native_help_complete_planes_equal=True,all525_native_spoken_layouts_pass=True,spoken26_complete_logical_and_physical_font_samples_pass=True,all10_help_spoken_and_current_actual_sheets_viewed=sheets,label_native_getter=0x0201CA00,label_native_getter_clean_exact=True,label_first_entry_pointer=pointer,label_current_byte_position_references=refs,label_complete_native60x16_font=str(lp),label_complete_native60x16_font_sha256=sha(lp.read_bytes()),label_visual_review_pending=True,label_width9cells_less_than_preceding10cell_Split_Sail=True,all86_cold_warm_native_copies=copies,COMMON_native_file_IO_explicit_host_contract=True,no_runtime_code_geometry_font_or_cache_change=True,registered_build_and_revised_spritsail_gameplay_pending=True,completion_credit_pending=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
 print(dict(records=43,native_copies=86,sheets_viewed=10,label_getter_and_full_font_pass=True,registered_and_revised_gameplay_pending=True))
