"""Source-lock full ancestry, exact reference equality andclean-input patch verification."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/maria_B207_release_tools_v7718')
if __name__=='__main__':
    assert not ROOT.exists()
    tool=derive('scripts/verify_papal_trade_release_v7661.py','scripts/verify_Maria_B207_release_v7718.py',{
        'papal_trade_editorial_v1':'maria_B207_editorial_v2',
        'papal_trade_release_v7661':'maria_B207_release_v7718',
        'all_routes_combined_v7660_candidate':'all_routes_combined_v7717_candidate',
        'all_routes_combined_v7611_candidate':'all_routes_combined_v7660_candidate',
        'papal_trade_registration_v7659':'maria_B207_registration_v7716',
        'papal_trade_build_v7660':'maria_B207_build_v7717',
        'papal_trade_regressions_v7660':'maria_B207_regressions_v7717',
        'all-routes-unified-v7660':'all-routes-unified-v7717',
        'all-routes-unified-v7611':'all-routes-unified-v7660',
        "'papal_trade_editorial'":"'maria_B207_editorial'",
        'papal_trade_atomic_v7657':'maria_B207_atomic_v7714b',
        '==628':'==629','manifest_batches=628':'manifest_batches=629','all628_manifest_batches':'all629_manifest_batches',
        "builder.index(b\"profile_config.get('lil_B234_editorial')\")":"builder.index(b\"profile_config.get('papal_trade_editorial')\")",
        'exact_to_V7611':'exact_to_V7660',
    })
    ROOT.mkdir(parents=True);save(ROOT/'source_locked_release_andpatch_verifier.json',dict(tool=tool,full_V7660_plusone_sealed_Maria_manuscript_expected629_batches=True,all_original_native_high_constants_andmultiplicity_preserved=True,no_test_package_orpromotion=True,new_credit=0,full_goal_complete=False))
