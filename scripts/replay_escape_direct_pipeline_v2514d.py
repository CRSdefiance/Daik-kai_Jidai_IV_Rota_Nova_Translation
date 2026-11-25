"""Current audited formatter bank/stack bridges and deployed immutable name bytes."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import save
OLD=Path('scripts/replay_escape_direct_pipeline_v2514.py')
if __name__=='__main__':
 source=OLD.read_text()
 a=" spans=[(a-BASE,b-a)for a,b in oldplan['private_spans']]+[(DIRECTORY_OFFSET,41*4),(TABLE_OFFSET,3668*2),(0x535E8,64)]"
 b=""" # The current compact selector owns a212-byte table and five stack bridges.
 # Use their previously audited extents,not the older188-byte escape-only table.
 audited=[(0x132020,16),(0x147B9C,212),(0x147E54,172),(0x169F78,12),(0x16A010,8),(0x16A05C,8),(0x16A0B0,16)]
 spans=[(a-BASE,b-a)for a,b in oldplan['private_spans']]+audited+[(DIRECTORY_OFFSET,41*4),(TABLE_OFFSET,3668*2),(0x535E8,64)]
 merged=[]
 for at,size in sorted(spans):
  if merged and at<=merged[-1][0]+merged[-1][1]:
   lo,length=merged[-1];merged[-1]=(lo,max(lo+length,at+size)-lo)
  else:merged.append((at,size))
 spans=merged
"""
 assert source.count(a)==1;source=source.replace(a,b)
 a=" assert current_sections[3].data[:-48]==old_sections[3].data[:-48]"
 b=""" from dk4tool.patch.main_pool_cache_visibility import POOL
 from types import SimpleNamespace
 assert len(current_sections[3].data)-48==len(old_sections[3].data)-48==123040
 delta=[i for i,(a,b)in enumerate(zip(current_sections[3].data[:-48],old_sections[3].data[:-48],strict=True))if a!=b]
 assert delta==list(range(0x5D4,0x5DC))
 before=bytes(old_sections[3].data[0x5D4:0x5DC]);after=bytes(current_sections[3].data[0x5D4:0x5DC])
 assert before==bytes.fromhex('8265617469636961')and after==b'Faticia\\0'
 assert raw[POOL-BASE+0x5D4:POOL-BASE+0x5DC]==before
 patches.append(dict(address=POOL+0x5D4,source_hex=before.hex(),target_hex=after.hex()))
"""
 assert source.count(a)==1;source=source.replace(a,b)
 a=" name=bytes(cpu.mem_read(pointer,64)).split(b'\\0')[0]"
 b=a+"""
 current_names=[]
 for slot,obj in enumerate(actors):
  vt=struct.unpack('<I',cpu.mem_read(obj,4))[0]
  q=get(struct.unpack('<I',cpu.mem_read(vt+0x20,4))[0]-BASE,obj)
  value=bytes(cpu.mem_read(q,64)).split(b'\\0')[0]
  current_names.append(dict(actor_slot=slot,actor_object=obj,name_hex=value.hex(),name=value.decode('cp932')))
"""
 assert source.count(a)==1;source=source.replace(a,b)
 source=source.replace('for section in current_sections:','for section in [*current_sections,SimpleNamespace(ramAddress=POOL,data=current_sections[3].data[:-48])]:')
 source=source.replace('complete123040_staged_payload_current_historical_equal=True,','complete123040_staged_payload_footprint_equal_8_current_immutable_name_bytes_applied=True,all208_current_compact_names_with_current_immutable_labels=current_names,')
 source=source.replace('escape_pipeline_v2514','escape_pipeline_v2514d')
 compile(source,__file__,'exec')
 exec(compile(source,__file__,'exec'),{'__name__':'__main__','__file__':__file__})
 save('work/analysis/escape_pipeline_v2514d/producer_binding.json',dict(original=str(OLD),original_sha256=sha(OLD.read_bytes()),
  current_formatter_extent_reference='scripts/audit_town_trend_references_v2166.py',extent_reference_sha256=sha(Path('scripts/audit_town_trend_references_v2166.py').read_bytes()),
  failed_narrow_payload_and_old_stack_bridge_assumptions_preserved=True,current_declared_immutable_spans_source_checked_before_overlay=True,
  current_deployed_pool_instructions_checked_as_well_as_original_ROM_sections=True,effective_source_sha256=sha(source.encode()),full_goal_complete=False))
