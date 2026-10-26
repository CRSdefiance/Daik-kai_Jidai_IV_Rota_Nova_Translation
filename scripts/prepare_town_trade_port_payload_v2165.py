"""Merge guarded two-paragraph repack and bounded selector research; no ROM."""
from pathlib import Path
from copy import deepcopy
from ndspy.code import MainCodeFile
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.duel_editorial import owned_entries
from dk4tool.patch.main_pool_cache_visibility import cache_plan
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/town_trade_port_payload_v2165')
if __name__=='__main__':
 assert not ROOT.exists();ROOT.mkdir(parents=True);path=Path('work/analysis/town_trade_port_payload_v2153/native_payload_plan.json');plan=deepcopy(read(path));rp=Path('work/analysis/town_trend_runtime_v2162/runtime_plan.json');runtime=read(rp);rom=NdsImage.open('out/all_routes_combined_v2143_candidate.nds');source=rom.read_file('/__arm9__.bin');assert sha(source)==plan['source_ARM9_sha256']==runtime['source_ARM9_sha256'];arm=Path(plan['target_ARM9']).read_bytes();code=MainCodeFile(arm,0x02000000)
 for p in runtime['patches']:
  at=p['address']-0x02000000;old,new=bytes.fromhex(p['source_hex']),bytes.fromhex(p['target_hex']);assert bytes(code.sections[0].data[at:at+len(old)])==old;code.sections[0].data[at:at+len(new)]=new
 target=bytes(code.save());common=Path(plan['target_COMMON']).read_bytes();entries=owned_entries(common,target,plan['directory_sha256']);assert len(entries)==3668
 original=MainCodeFile(source,0x02000000);restored=MainCodeFile(target,0x02000000)
 for p in plan['metadata_patches']+runtime['patches']:
  at=p['address']-0x02000000;old=bytes.fromhex(p['source_hex']);restored.sections[0].data[at:at+len(old)]=old
 assert bytes(restored.save())==source and cache_plan(target)==cache_plan(source)
 shape=lambda c:[(s.ramAddress,len(s.data),s.bssSize)for s in c.sections];assert shape(code)==shape(original)and all(bytes(a.data)==bytes(b.data)for a,b in zip(code.sections[1:],original.sections[1:],strict=True))and len(code.sections[3].data)-48==123040
 ap=ROOT/'ARM9_RESEARCH_ONLY.bin';cp=ROOT/'COMMON_RESEARCH_ONLY.DK4';ap.write_bytes(target);cp.write_bytes(common)
 plan.pop('all_executable_font_other_runtime_and123040_staged_bytes_exact');plan.update(target_ARM9_sha256=sha(target),target_COMMON_sha256=sha(common),target_ARM9=str(ap),target_COMMON=str(cp),runtime_plan=str(rp),runtime_plan_sha256=sha(rp.read_bytes()),runtime_patches=runtime['patches'],all_font_geometry_and_other_runtime_except_seven_declared_selector_entry_exit_spans_exact=True,selector_and_code_extents_remain212_and172=True,all_seven_stack_decoder_spans_and_metadata_inverse_restore_exact=True,all_sections_BSS_ITCM_arena_cache_and123040_staged_bytes_exact=True,previous_metadata_only_plan=str(path),previous_metadata_only_plan_sha256=sha(path.read_bytes()),producer_sha256=sha(Path(__file__).read_bytes()),not_a_playable_ROM=True,full_goal_complete=False);save(ROOT/'native_payload_plan.json',plan);print(dict(ARM9=sha(target),COMMON=sha(common),revised_IDs=plan['actual_text_changed_IDs'],blocks=plan['block_sizes'],runtime_spans=7,no_ROM=True))
