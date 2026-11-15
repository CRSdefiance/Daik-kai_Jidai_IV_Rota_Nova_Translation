"""Source-lock the registered release/xdelta audit andone affected own-Lil startup."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive,checked_text
from scripts.verify_village_wrap_v608 import save
if __name__=='__main__':
    root=Path('work/analysis/retrospective_B218_release_startup_tools_v7858');assert not root.exists()
    block_guard="""    from dk4tool.formats.ilnk import IlnkContainer
    mapping=read('translations/lil_B218_retrospective_relocation_map_v1.json')
    old_blocks,new_blocks=[IlnkContainer.parse(im.read_file('/data/SC2.DK4')).blocks for im in [previous,image]]
    assert len(old_blocks)==len(new_blocks)==336 and [i for i,(a,b) in enumerate(zip(old_blocks,new_blocks,strict=True)) if a!=b]==[218]
    assert sha(old_blocks[218])==mapping['groups'][0]['source_block_sha256'] and sha(new_blocks[218])==mapping['groups'][0]['target_block_sha256']
    for path in ['/__arm9__.bin','/COMMON/MESFILE.DK4','/GRP/KANJI.FNT']:"""
    jobs=[
        ('scripts/verify_Maria_B36_release_v7822.py','scripts/verify_retrospective_B218_release_v7858.py',{
            'maria_B36_editorial_v1':'lil_B218_retrospective_v2',
            'maria_B36_editorial':'lil_B218_retrospective',
            'maria_B36_release_v7822':'retrospective_B218_release_v7858',
            'all_routes_combined_v7821_candidate':'all_routes_combined_v7857_candidate',
            'all_routes_combined_v7779_candidate':'all_routes_combined_v7821_candidate',
            'maria_B36_registration_v7820':'retrospective_B218_registration_v7856',
            'maria_B36_build_v7821':'retrospective_B218_build_v7857',
            'maria_B36_regressions_v7821':'retrospective_B218_regressions_v7857',
            'all-routes-unified-v7821':'all-routes-unified-v7857',
            'all-routes-unified-v7779':'all-routes-unified-v7821',
            'len(manifest[\'batches\'])==631':'len(manifest[\'batches\'])==632',
            'maria_B36_atomic_v7818b':'retrospective_B218_atomic_v7854b',
            '/data/SC3.DK4':'/data/SC2.DK4',
            'len(ids)==16':'len(ids)==1',
            'len(a)==len(b)==303':'len(a)==len(b)==336',
            'if x!=y]==[36]':'if x!=y]==[218]',
            "profile_config.get('maria_story_editorial')":"profile_config.get('maria_B36_editorial')",
            'Maria B36 editorial candidate;all631batches':'B218 retrospective wrap candidate;all632batches',
            'registered Maria B36 candidate':'registered B218 retrospective candidate',
            'manifest_batches=631':'manifest_batches=632',
            'all631_manifest_batches_and114_accepted_layers_present':'all632_manifest_batches_and114_accepted_layers_present',
            'only_SC3_B36_change_all302others_exact':'only_SC2_B218_change_all335others_exact',
            'batches=631':'batches=632',
        }),
        ('scripts/run_retrospective_Lil_context_v7836.py','scripts/run_retrospective_B218_startup_v7859.py',{
            'work/analysis/retrospective_Lil_context_runs_v7836':'work/analysis/retrospective_B218_startup_runs_v7859',
            'work/analysis/maria_B36_release_v7822':'work/analysis/retrospective_B218_release_v7858',
            'all-routes-unified-v7821':'all-routes-unified-v7857',
            "priorroot=Path('work/analysis/papal_trade_startup_runs_v7663b' if case in ['route0','route1'] else 'work/analysis/papal_trade_startup_runs_v7663')/case":
            "priorroot=Path('work/analysis/retrospective_Lil_context_runs_v7836')/case",
            'Lil_wrap_V7821_{case}_v7836':'Lil_wrap_V7857_{case}_v7859',
            'own V7821 startup':'own V7857 startup',
        }),
        ('scripts/bind_retrospective_Lil_context_v7837.py','scripts/bind_retrospective_B218_startup_v7860.py',{
            'work/analysis/retrospective_Lil_context_binding_v7837':'work/analysis/retrospective_B218_startup_binding_v7860',
            'work/analysis/retrospective_Lil_context_runs_v7836/route2':'work/analysis/retrospective_B218_startup_runs_v7859/route2',
            'work/analysis/current_V7821_Lil_native_v7837':'work/analysis/current_V7857_Lil_native_v7860',
            "    for path in ['/__arm9__.bin','/COMMON/MESFILE.DK4','/data/SC2.DK4','/GRP/KANJI.FNT']:":block_guard,
            'V7821 Lil':'V7857 Lil',
        }),
    ]
    for a,b,c in jobs:assert not Path(b).exists();checked_text(Path(a).read_text(encoding='utf-8'),c)
    outputs=[derive(*job) for job in jobs]
    root.mkdir(parents=True);save(root/'provenance.json',dict(derivations=outputs,
        original_manifest_baseline_reference_patch_inverse_andownership_guards_preserved=True,
        affected_Lil_own_ROM_startup_only_previous_V7821_ordinary_inputs_unchanged=True,
        changed_SC2_block_bound_explicitly_instead_of_dropping_the_file_guard=True,
        new_credit=0,full_goal_complete=False))
