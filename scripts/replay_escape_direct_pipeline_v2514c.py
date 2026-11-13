"""Use the observed deployed pool address for the8 immutable name bytes."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import save
OLD=Path('scripts/replay_escape_direct_pipeline_v2514b.py')
if __name__=='__main__':
 source=OLD.read_text()
 a='payload_at=current_sections[3].ramAddress+0x5D4'
 assert source.count(a)==1
 source=source.replace(a,'from dk4tool.patch.main_pool_cache_visibility import POOL\n payload_at=POOL+0x5D4')
 a='for section in current_sections:'
 source=source.replace("source=source.replace(old,new)\n source=source.replace('complete123040", "source=source.replace(old,new)\n source=source.replace('for section in current_sections:',\"for section in [*current_sections,__import__('types').SimpleNamespace(ramAddress=POOL,data=current_sections[3].data[:-48])]:\")\n source=source.replace('complete123040")
 source=source.replace('escape_pipeline_v2514b','escape_pipeline_v2514c')
 compile(source,__file__,'exec')
 exec(compile(source,__file__,'exec'),{'__name__':'__main__','__file__':__file__})
 save('work/analysis/escape_pipeline_v2514c/successor_binding.json',dict(failed_preflight=str(OLD),failed_preflight_sha256=sha(OLD.read_bytes()),
  corrected_deployed_immutable_pool_address='POOL+0x5D4;staged source address is not the live deployed string',
  current_instruction_checks_include_deployed_pool_alias=True,effective_source_sha256=sha(source.encode()),full_goal_complete=False))
