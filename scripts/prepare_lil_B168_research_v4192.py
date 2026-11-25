"""Derive complete B168 reference image, original loader, entry census and end probes."""
from pathlib import Path
from scripts.prepare_lil_B156_layout_v3705 import derive
from scripts.verify_village_wrap_v608 import save

ROOT = Path('work/analysis/lil_B168_research_tools_v4192')
PARENT = Path('out/all_routes_combined_v4160_candidate.nds')
ROM = Path('out/lil_B168_reference_v4193_RESEARCH_ONLY.nds')
PLAN = Path('work/analysis/lil_B168_relocation_v4190/nested_source_relocation_research.json')

if __name__ == '__main__':
    assert not ROOT.exists()
    tools = []
    tools.append(derive('scripts/create_lil_B167_reference_v4142.py', 'scripts/create_lil_B168_reference_v4193.py', {
        'lil_B167_research_v4142': 'lil_B168_research_v4193',
        'lil_B167_reference_v4142': 'lil_B168_reference_v4193',
        'lil_B167_relocation_v4139': 'lil_B168_relocation_v4190',
        'lil_B167_stored_v4140/all27_final_stored_targets108': 'lil_B168_stored_v4191/all54_final_stored_targets216',
        'all_routes_combined_v4110': 'all_routes_combined_v4160', 'V4110': 'V4160',
        'editorial_handoff_verification_v4137': 'editorial_handoff_verification_v4189',
        'all27_final_targets': 'all54_final_targets',
        "current_final_stored_macro_alignment_cases']==108": "current_final_stored_macro_alignment_cases']==216",
        'current_final_stored_macro_alignment_cases=108': 'current_final_stored_macro_alignment_cases=216',
        '[167]': '[168]', 'actual_selected_B167_IDs': 'actual_selected_B168_IDs',
    }))
    common = {'prepare_lil_B167_research_v4141': 'prepare_lil_B168_research_v4192'}
    tools.append(derive('scripts/verify_lil_B167_loader_v4143.py', 'scripts/verify_lil_B168_loader_v4194.py', {
        **common, 'lil_B167_research_v4142': 'lil_B168_research_v4193',
        'lil_B167_loader_v4143': 'lil_B168_loader_v4194', 'B167': 'B168',
    }))
    tools.append(derive('scripts/verify_lil_B167_references_v4144.py', 'scripts/verify_lil_B168_references_v4195.py', {
        **common, 'lil_B167_reference_census_v4144': 'lil_B168_reference_census_v4195',
        'lil_B167_loader_v4143': 'lil_B168_loader_v4194', 'B167': 'B168', '[167]': '[168]',
        'for r in result)==46': 'for r in result)==82',
        'all46_commands12_relative_sites': 'all82_commands12_relative_sites',
        'all46_clean_current_target_commands_and12_relative_sites': 'all82_clean_current_target_commands_and12_relative_sites',
        'native_commands_each=46': 'native_commands_each=82', '46-command/12-span': '82-command/12-span',
    }))
    tools.append(derive('scripts/prove_lil_B167_ends_v4145.py', 'scripts/prove_lil_B168_ends_v4196.py', {
        **common, 'lil_B167_ends_v4145': 'lil_B168_ends_v4196',
        'assert n==167 and len(ends)==2': 'assert n==168 and len(ends)==2',
        'separated refusal and lecture endwords': 'consecutive B168 endwords', 'B167': 'B168',
    }))
    ROOT.mkdir(parents=True)
    save(ROOT / 'source_derivation.json', dict(tools=tools, source_block=168, commands=82,
        relative_sites=12, consecutive_endwords=2, predicates=3, opaque_leaves=16,
        resource_words=[0x6342, 0x630B, 0x6300, 0x6301], A000=1,
        no_registry_ledger_credit_change=True))
    print('B168 one-block reference, whole loader, entry census and consecutive-end probes prepared.')
