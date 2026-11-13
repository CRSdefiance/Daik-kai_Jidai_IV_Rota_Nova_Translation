"""Verify V1986 full inheritance, tested ROM identity and exact clean-input patch."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha

SOURCE = Path('scripts/verify_lil_london_release_v1910.py')
SOURCE_SHA = 'f79e44087153e5381f78a5b09e3c3c13e593f3d4ac1267b46febf583ad0f4ab4'
ROM = Path('out/all_routes_combined_v1986_candidate.nds')

if __name__ == '__main__':
    assert sha(SOURCE.read_bytes()) == SOURCE_SHA
    text = SOURCE.read_text(encoding='utf-8')
    changes = {
        'lil_london_editorial':'lil_lookout_affiliation',
        'scripts.register_lil_london_v1908b':'scripts.register_lil_lookout_v1985',
        'out/all_routes_combined_v1909_candidate.nds':'out/all_routes_combined_v1986_candidate.nds',
        '872f4047dd3c9ee335dc7e6dbff5e96af668c67b07e145f29422db71c0871d97':
            'c4c998e446b7ac410d2294563fc4e5d5181cef6938c25254b1bd3679492efa20',
        "registry['profiles']['all-routes-unified-v1875']":"registry['profiles']['all-routes-unified-v1971']",
        "len(manifest['batches']) == 480":"len(manifest['batches']) == 485",
        '== [26]':'== [23]',
        "assert len(stage['changed_records']) == 111 and stage['block_growth_bytes'] == 864":
            "assert len(stage['changed_records']) == 1 and sum(r['growth_bytes'] for r in stage['blocks']) == -12",
        'all480_batches114_accepted_layers_and_prior_profiles_preserved':'all485_batches114_accepted_layers_and_prior_profiles_preserved',
        'only_SC2_block26_changed_relative_to_V1875':'only_SC2_block23_changed_relative_to_V1971',
        'batches=480, changed_SC2_blocks=[26]':'batches=485, changed_SC2_blocks=[23]',
    }
    for old,new in changes.items():
        assert old in text,old
        text = text.replace(old,new)
    exec(compile(text,str(SOURCE),'exec'),{'__name__':'__main__','__file__':__file__})
