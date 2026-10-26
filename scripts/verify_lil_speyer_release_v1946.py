"""Verify cumulative Speyer inheritance and byte-exact clean-input patch."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha

SOURCE=Path('scripts/verify_lil_london_release_v1910.py')
SOURCE_SHA='f79e44087153e5381f78a5b09e3c3c13e593f3d4ac1267b46febf583ad0f4ab4'
ROM=Path('out/all_routes_combined_v1945_candidate.nds')

if __name__=='__main__':
    assert sha(SOURCE.read_bytes())==SOURCE_SHA
    text=SOURCE.read_text(encoding='utf-8')
    changes={
        'lil_london_editorial':'lil_speyer_editorial',
        'scripts.register_lil_london_v1908b':'scripts.register_lil_speyer_v1944',
        'out/all_routes_combined_v1909_candidate.nds':'out/all_routes_combined_v1945_candidate.nds',
        '872f4047dd3c9ee335dc7e6dbff5e96af668c67b07e145f29422db71c0871d97':
            'fdc6757a13af0a04c4f2355ade3c66163a6382a0a7081efa03a457b1198dd1d1',
        "registry['profiles']['all-routes-unified-v1875']":"registry['profiles']['all-routes-unified-v1909']",
        "[normal(config['manuscript'])]":"[normal(config['manuscript']),normal(config['choices'])]",
        "len(manifest['batches']) == 480":"len(manifest['batches']) == 482",
        "== [26]":"== [25,128]",
        "assert len(stage['changed_records']) == 111 and stage['block_growth_bytes'] == 864":
            "assert len(stage['changed_records']) == 59 and sum(r['growth_bytes']for r in stage['blocks']) == 108",
        'all480_batches114_accepted_layers_and_prior_profiles_preserved':'all482_batches114_accepted_layers_and_prior_profiles_preserved',
        'only_SC2_block26_changed_relative_to_V1875':'only_SC2_blocks25_and128_changed_relative_to_V1909',
        'all335_other_blocks_every_other_file_and_native_component_exact':'all334_other_blocks_every_other_file_and_native_component_exact',
        'batches=480, changed_SC2_blocks=[26]':'batches=482, changed_SC2_blocks=[25,128]',
    }
    for old,new in changes.items():
        assert old in text,old
        text=text.replace(old,new)
    exec(compile(text,str(SOURCE),'exec'),{'__name__':'__main__','__file__':__file__})
