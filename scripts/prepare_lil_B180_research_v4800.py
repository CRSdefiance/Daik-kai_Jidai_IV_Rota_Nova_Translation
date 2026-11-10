"""Prepare exact-current B180 research loading,reference and tail gates."""
from pathlib import Path
from scripts.prepare_lil_B156_layout_v3705 import derive
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/lil_B180_research_tools_v4800')
PARENT=Path('out/all_routes_combined_v4766_candidate.nds')
ROM=Path('out/lil_B180_reference_v4801_RESEARCH_ONLY.nds')
PLAN=Path('work/analysis/lil_B180_relocation_v4798/nested_source_relocation_research.json')

if __name__=='__main__':
    assert not ROOT.exists()
    tools=[]
    original=Path('scripts/verify_lil_B179_loader_v4735.py').read_text()
    start=original.index('    prior_path=');end=original.index("    for label, path in [('research', ROM)]:",start)
    tools.append(derive('scripts/verify_lil_B179_loader_v4735.py','scripts/verify_lil_B180_loader_v4802.py',{
        original[start:end]:'',"for label, path in [('research', ROM)]:":"for label, path in [('current', PARENT),('research', ROM)]:",
        'prepare_lil_B179_research_v4733':'prepare_lil_B180_research_v4800','lil_B179_loader_v4735':'lil_B180_loader_v4802',
        'lil_B179_research_v4734':'lil_B180_research_v4801','B179':'B180',
        "'fresh_research_whole_SC2_loads':336,'exact_parent_reused_whole_SC2_loads':336,'fresh_parent_modes':672,'exact_parent_reused_modes':672":
            "'fresh_research_whole_SC2_loads':336,'fresh_current_whole_SC2_loads':336,'fresh_parent_modes':1344,'exact_parent_reused_modes':0",
        'New B180 research:336 original loads/cache hits and672 modes pass;byte-identical V4701 parent proof reused exactly. Representative/release pending.':
            'Current/research B180:672 fresh original loads/cache hits and1344 fresh parent modes pass;no old parent proof reuse. Representative/release pending.'}))
    tools.append(derive('scripts/verify_lil_B179_references_v4736.py','scripts/verify_lil_B180_references_v4803.py',{
        'Fresh shipped entry census and16-command/no-relative-site one-block mapping.':'Fresh shipped entry census and28-command/ten-relative-site B180 mapping.',
        'prepare_lil_B179_research_v4733':'prepare_lil_B180_research_v4800','lil_B179_reference_census_v4736':'lil_B180_reference_census_v4803',
        'lil_B179_loader_v4735':'lil_B180_loader_v4802','B179':'B180','[179]':'[180]',
        "sum(len(r['mapped_commands'])for r in result)==16":"sum(len(r['mapped_commands'])for r in result)==28",
        "sum(r['typed_relative_span_count']for r in result)==0":"sum(r['typed_relative_span_count']for r in result)==10",
        "sum(r['target_native_skip_cases']for r in result)==0":"sum(r['target_native_skip_cases']for r in result)==50",
        'all16_commands_no_relative_sites_and_shipped_entry_census':'all28_commands_ten_relative_sites_and_shipped_entry_census',
        'all16_clean_current_target_commands_and_no_relative_sites_reexecuted':'all28_clean_current_target_commands_and_ten_relative_sites_reexecuted',
        'native_commands_each=16,relative_sites=0,target_native_skip_cases=0':'native_commands_each=28,relative_sites=10,target_native_skip_cases=50'}))
    tools.append(derive('scripts/prove_lil_B179_ends_v4737.py','scripts/prove_lil_B180_ends_v4804.py',{
        'prepare_lil_B179_research_v4733':'prepare_lil_B180_research_v4800','lil_B179_ends_v4737':'lil_B180_ends_v4804',
        'n==179':'n==180','B179':'B180','two_declared_tail_end_decodes_no_relative_sites':'two_declared_tail_end_decodes_ten_relative_sites'}))
    ROOT.mkdir(parents=True);save(ROOT/'prepared_tools.json',dict(tools=tools,parent=str(PARENT),research=str(ROM),
        plan=str(PLAN),whole_parent_and_research_loader_checks_fresh=True,source_end572_target_end542_requires_actual_native_guarded_decode=True,
        no_ROM_registry_orcredit_change=True,full_goal_complete=False))
    print('Prepared fresh current/research loaders,three entry censuses and guarded572/542 end decodes.')
