"""Prepare exact B49 reference seal with a fresh reversible reconstruction helper."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/Rafael_B49_seal_tools_v8114')
if __name__=='__main__':
    assert not ROOT.exists()
    result=derive('scripts/seal_Rafael_B48_references_v8060.py','scripts/seal_Rafael_B49_references_v8114.py',{
        'Rafael_B48_release_paths_v8060':'Rafael_B49_release_paths_v8114',
        'Rafael_B48_reference_tools_v8060':'Rafael_B49_reference_tools_v8114',
        'B48':'B49','Rafael91':'Rafael61',
        "policy['positive_count']==91 and policy['negative_count']==1454":"policy['positive_count']==61 and policy['negative_count']==1014",
        "group['block']==48":"group['block']==49",
        'oldbank[48]':'oldbank[49]','cleanbank[48]':'cleanbank[49]','newbank[48]':'newbank[49]','restored[48]':'restored[49]',
        'len(target)==4948':'len(target)==3792','==[48]':'==[49]','block=48':'block=49',
        'ninety-one exact source/context/prose/native':'sixty-one exact source/context/prose/native',
        'all91_five_gates_andexact_references_approved':'all61_five_gates_andexact_references_approved',
        'all163_commands28_relative_sites140_cases_source_bound':'all154_commands56_relative_sites280_cases_source_bound',
        'R347_two_pages_andtwo_exact_warning_exceptions_unchanged':'all61_single_pages_three_exact_warning_exceptions22_infos_unchanged',
        'thirteen_native_only_speeches_andthree_headers_explicit':'eleven_native_only_speeches_andthree_headers_explicit',
        'all91_records_exact':'all61_records_exact',
        'B48 references sealed:91 exact records/163 commands/28 fixups,full block/archive inverses. Two-page andwaiver scopes unchanged. Atomic integration pending.':'B49 references sealed:61 exact records/154commands/56fixups,full block/archive inverses. Single-page/three-warning scopes unchanged. Atomic integration pending.',
    })
    ROOT.mkdir(parents=True);save(ROOT/'source_locked_derivation.json',result)
    print('Prepared B49 seal producer; policy validation must pass before sealing.')
