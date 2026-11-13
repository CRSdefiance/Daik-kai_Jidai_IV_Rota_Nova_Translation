"""All native cold/warm copies and opaque-prefix cache sequences for town84."""
import inspect
from pathlib import Path
from dk4tool.patch.duel_editorial import owned_entries,COMPONENT
from scripts import verify_duel_cache_copies_v1163 as previous
from scripts.verify_village_wrap_v608 import save
from dk4tool.patch.grand_race_menu_release import sha
if __name__=='__main__':
 source=inspect.getsource(previous.main)
 for old,new in [('work/analysis/duel_native_release_v1162/final_payload_plan.json','work/analysis/town_services_payload_v2092b/native_payload_plan.json'),("prefix = plan['new_code_prefix']","prefix = {'block':21,'component_bytes':1484,'component_sha256':sha(COMPONENT.read_bytes()+bytes(4))}")]:
  assert source.count(old)==1;source=source.replace(old,new)
 source=source.replace('opaque1480byte_component','opaque1484byte_component')
 env={**previous.__dict__,'__file__':__file__,'entries':owned_entries,'COMPONENT':COMPONENT,'ROOT':Path('work/analysis/town_services_copies_v2093')}
 exec(compile(source,__file__,'exec'),env);env['main']()
 save(env['ROOT']/'verifier_binding.json',dict(effective_verifier_sha256=sha(source.encode()),historical_verifier_sha256=sha(Path(previous.__file__).read_bytes()),producer_sha256=sha(Path(__file__).read_bytes()),all_original_native_full_span_terminator_8192_input_output_ABI_and_cache_assertions_retained=True,physical_file_IO_is_explicit_host_contract=True,full_goal_complete=False))
