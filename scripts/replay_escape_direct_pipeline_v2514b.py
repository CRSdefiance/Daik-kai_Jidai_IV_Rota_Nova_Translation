"""Apply the verified8-byte immutable name delta instead of assuming payload equality."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import save
OLD=Path('scripts/replay_escape_direct_pipeline_v2514.py')
if __name__=='__main__':
 source=OLD.read_text()
 old=" assert current_sections[3].data[:-48]==old_sections[3].data[:-48]"
 new=""" assert len(current_sections[3].data)-48==len(old_sections[3].data)-48==123040
 payload_diff=[i for i,(a,b)in enumerate(zip(current_sections[3].data[:-48],old_sections[3].data[:-48],strict=True))if a!=b]
 assert payload_diff==list(range(0x5D4,0x5DC))
 payload_at=current_sections[3].ramAddress+0x5D4
 assert bytes(old_sections[3].data[0x5D4:0x5DC])==bytes.fromhex('8265617469636961')
 assert bytes(current_sections[3].data[0x5D4:0x5DC])==b'Faticia\\0'
 assert raw[payload_at-BASE:payload_at-BASE+8]==bytes(old_sections[3].data[0x5D4:0x5DC])
 patches.append(dict(address=payload_at,source_hex=bytes(old_sections[3].data[0x5D4:0x5DC]).hex(),target_hex=bytes(current_sections[3].data[0x5D4:0x5DC]).hex()))
"""
 assert source.count(old)==1
 source=source.replace(old,new).replace('escape_pipeline_v2514','escape_pipeline_v2514b')
 old=" name=bytes(cpu.mem_read(pointer,64)).split(b'\\0')[0]"
 new=old+"""
 current_names=[]
 for slot,obj in enumerate(actors):
  vt=struct.unpack('<I',cpu.mem_read(obj,4))[0]
  get_name=get(struct.unpack('<I',cpu.mem_read(vt+0x20,4))[0]-BASE,obj)
  value=bytes(cpu.mem_read(get_name,64)).split(b'\\0')[0]
  current_names.append(dict(actor_slot=slot,actor_object=obj,name_hex=value.hex(),name=value.decode('cp932')))
"""
 assert source.count(old)==1
 source=source.replace(old,new)
 source=source.replace('complete123040_staged_payload_current_historical_equal=True,','complete123040_staged_payload_footprint_equal_8_current_immutable_name_bytes_applied=True,all208_current_compact_names_with_current_immutable_labels=current_names,')
 compile(source,__file__,'exec')
 exec(compile(source,__file__,'exec'),{'__name__':'__main__','__file__':__file__})
 save('work/analysis/escape_pipeline_v2514b/producer_binding.json',dict(failed_preflight=str(OLD),failed_preflight_sha256=sha(OLD.read_bytes()),
  initial_assumption_rejected_before_output_or_credit='123040-byte footprint is preserved but8 immutable Faticia label bytes differ',
  exact_old_CP932_fullwidth_F_to_current_ASCII_Faticia_bytes_declared_and_applied=True,effective_source_sha256=sha(source.encode()),full_goal_complete=False))
