"""Derive the one-block reference image and original loader/census/end proofs."""
from pathlib import Path
from scripts.prepare_lil_B156_layout_v3705 import derive
from scripts.verify_village_wrap_v608 import save

ROOT = Path('work/analysis/lil_B166_research_tools_v4095')
PARENT = Path('out/all_routes_combined_v4046_candidate.nds')
ROM = Path('out/lil_B166_reference_v4096_RESEARCH_ONLY.nds')
PLAN = Path('work/analysis/lil_B166_relocation_v4093/nested_source_relocation_research.json')

if __name__ == '__main__':
    assert not ROOT.exists()
    pairs = [derive('scripts/create_lil_B164_reference_v3988.py', 'scripts/create_lil_B166_reference_v4096.py', {
        'lil_B164_research_v3988': 'lil_B166_research_v4096',
        'lil_B164_reference_v3988': 'lil_B166_reference_v4096',
        'lil_B164_relocation_v3986': 'lil_B166_relocation_v4093',
        'lil_B164_stored_v3987/all47_final_stored_targets188': 'lil_B166_stored_v4094/all42_final_stored_targets168',
        'all_routes_combined_v3954': 'all_routes_combined_v4046',
        'editorial_handoff_verification_v3959': 'editorial_handoff_verification_v4091',
        'all47_final_targets': 'all42_final_targets',
        "current_final_stored_macro_alignment_cases']==188": "current_final_stored_macro_alignment_cases']==168",
        'current_final_stored_macro_alignment_cases=188': 'current_final_stored_macro_alignment_cases=168',
        '[164]': '[166]', 'V3954': 'V4046', 'actual_selected_B164_IDs': 'actual_selected_B166_IDs',
    })]
    common = {'prepare_lil_B164_research_v3988': 'prepare_lil_B166_research_v4095',
              'lil_B164_research_v3988': 'lil_B166_research_v4096'}
    pairs.append(derive('scripts/verify_lil_B164_loader_v3989.py', 'scripts/verify_lil_B166_loader_v4097.py', {
        **common, 'lil_B164_loader_v3989': 'lil_B166_loader_v4097', 'B164': 'B166'}))
    pairs.append(derive('scripts/verify_lil_B164_references_v3990.py', 'scripts/verify_lil_B166_references_v4098.py', {
        **common, 'lil_B164_reference_census_v3990': 'lil_B166_reference_census_v4098',
        'lil_B164_loader_v3989': 'lil_B166_loader_v4097', 'B164': 'B166', '[164]': '[166]',
        'for r in result)==61': 'for r in result)==62', 'for r in result)==4': 'for r in result)==8',
        'for r in result)==20': 'for r in result)==40', 'all61_commands4_relative_sites': 'all62_commands8_relative_sites',
        'all61_clean_current_target_commands_and4_relative_sites': 'all62_clean_current_target_commands_and8_relative_sites',
        'native_commands_each=61,relative_sites=4,target_native_skip_cases=20': 'native_commands_each=62,relative_sites=8,target_native_skip_cases=40',
        '61-command/4-span': '62-command/8-span',
    }))
    pairs.append(derive('scripts/prove_lil_B164_ends_v3991.py', 'scripts/prove_lil_B166_ends_v4099.py', {
        **common, 'lil_B164_ends_v3991': 'lil_B166_ends_v4099',
        'Decode both declared endwords per image,including both separated advice endwords.':
            'Decode the single declared tail end in both images with poisoned post-payload guards.',
        'assert len(ends)==(2 if n==164 else 1)': 'assert n==166 and len(ends)==1',
        "assert len(cases)==4 and sum(not c['at_logical_tail'] for c in cases)==2":
            "assert len(cases)==2 and all(c['at_logical_tail'] for c in cases)",
        'four_declared_end_decodes_and_all4': 'two_declared_end_decodes_and_all8',
        'all4_declared_end_decodes': 'all2_declared_end_decodes',
        'B164_first_end_precedes_second_end_and_declared_logical_end': 'B166_single_end_is_declared_logical_tail',
        'second_B164_declared_word_decoder_probe_not_actual_reachability_claim': 'single_B166_end_decoder_probe_not_actual_reachability_claim',
        'Four declared current/target endwords pass with poisoned unread post-payload guards;B164 bothwords preserved.':
            'Two declared current/target endwords pass with poisoned unread post-payload guards;single B166 tail preserved.',
    }))
    ROOT.mkdir(parents=True)
    save(ROOT / 'source_derivation.json', dict(tools=pairs, source_block=166, source_commands=62,
        source_relative_sites=8, target_skip_cases=40, single_tail_end=True, no_registry_ledger_credit_change=True))
    print('B166 reference image and original loader/census/single-end successors created.')
