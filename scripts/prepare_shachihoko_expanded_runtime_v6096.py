"""Prepare town input regression and a strictly rebound current-snapshot native context."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/shachihoko_runtime_preparation_v6096')
if __name__=='__main__':
    assert not ROOT.exists();receipt=read('work/analysis/shachihoko_item116_research_v6094/coordinated_research_receipt.json');plan=receipt['data_plan'];assert plan['new_payload_bytes']==123264
    tools=[derive('scripts/run_shachihoko_expanded_boot_v6095.py','scripts/run_shachihoko_expanded_town_v6096.py',{
        'shachihoko_runs_v6095':'shachihoko_runs_v6096','shachihoko_v6095':'shachihoko_v6096',"assert case=='newgame'":"assert case=='town'"})]
    tools.append(derive('scripts/current_build_native_context_v4774.py','scripts/current_build_native_context_v6097.py',{
        'len(payload)==123040':"len(payload)==123264 and sha(self.arm)=="+repr(plan['target_ARM9_sha256'])+" and sha(self.common)=="+repr(plan['target_COMMON_sha256']),
        'POOL-BASE+123040':'POOL-BASE+123264','original_current123040_deployed_payload_exact':'original_current123264_deployed_payload_exact',
        'exact current123040-byte deployed pool':'exact current123264-byte deployed pool',
    }))
    ROOT.mkdir(parents=True);save(ROOT/'strict_runtime_successors.json',dict(tools=tools,expanded_research_receipt_sha256=__import__('hashlib').sha256(Path('work/analysis/shachihoko_item116_research_v6094/coordinated_research_receipt.json').read_bytes()).hexdigest(),
        new_context_requires_exact_target_ARM9_COMMON_whole_ROM_and_actual_deployed_payload=True,no_source_instruction_or_hook_scope_changed=True,full_goal_complete=False))
    print('Same-source town regression and exact target-hash123264 current context prepared;no native numeric addresses changed.')
