"""Derive the standard registered integration, patch and own-route startup workflow."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/Rafael_B45_registered_tools_v7910')
if __name__=='__main__':
    assert not ROOT.exists()
    a=Path('scripts/register_retrospective_B218_v7856.py');s=a.read_text('utf8')
    old=s[s.index('    profile.update('):s.index('    updated=deepcopy(registry)')]
    new="""    profile.update(status='experimental',rafael_B45_editorial=owned.CONFIG,
        description="Complete V7857 plus Rafael's complete twelve-speech B45 trade tutorial: seven source-grounded wording revisions and five contextual retentions.",
        note="Fresh clean Japanese whole exchange and exact current comparison; Rafael Castor/Julio Erneco retained from source getters. Conditional Lisbon cargo, local ruler contract fee at Palace/Governor's Office, minimum-fee advice, Ceuta and optional sale preserved. Market share limits purchases, not selling. Original 00/06/FE selectors, six-byte preambles, FO, all24 commands/five relative spans preserved. Twelve complete native/stored pages, 48 compiled alignments, 28 fresh stored/20 reused alignments,343 loads/686 parent modes,25 relocated cases and full inverses. Paired disclosed entry fixtures play all12 speeches in both languages,90 complete holds,normal [0,1] returns6653. Preserve21 comparison rows/seven duration differences and English one LCG step ahead; future random outcomes not proven equal. 12 policy positives/159 rejections; atomic whole-ROM positive/131 independent rejections before commit. No natural activation/full route/hardware claim. Full207 names, four storylines, earlier dialogue, broad town/random,Help/remaining prose and wrap review remain open; graphics/later technical re-audit separate. MainV4701 unchanged; no separate package,promotion,pruning,commit orpush.")
"""
    rows=[]
    rows.append(derive(a,'scripts/register_Rafael_B45_v7910.py',{
        s.splitlines()[0]:'"""Register the approved twelve-speech Rafael B45 layer after the complete V7857 stack."""',
        'lil_B218_retrospective_v2':'rafael_B45_editorial_v2',
        'scripts.retrospective_B218_final_paths_v7853':'scripts.Rafael_B45_release_paths_v7903',
        'retrospective_B218_registration_v7856':'Rafael_B45_registration_v7910',
        "PROFILE='all-routes-unified-v7857'":"PROFILE='all-routes-unified-v7911'",
        'retrospective_B218_atomic_challenges_v7855':'Rafael_B45_atomic_challenges_v7909',
        "assert not ROOT.exists() and not Path(owned.CONFIG).exists()":"assert not ROOT.exists() and Path(owned.CONFIG).exists()",
        "result['positive_records']==13 and result['changed_records']==1 and result['negative_count']==len(cases)==128":"result['positive_records']==12 and result['negative_count']==len(cases)==131",
        "result['all_dependency_digests_deliberately_bypassed']":"result['config_dependency_digests_deliberately_bypassed']",
        'editorial_handoff_verification_v7852':'editorial_handoff_verification_v7900',
        "==631":"==632",
        'lil_B218_retrospective':'rafael_B45_editorial',
        'apply_lil_B218_retrospective':'apply_rafael_B45_editorial',
        'B218 retrospective must run once after the complete V7821 stack':'Rafael B45 must run once after the complete V7857 stack',
        "b\"profile_config.get('maria_B36_editorial')\"":"b\"profile_config.get('lil_B218_retrospective')\"",
        "registry['profiles']['all-routes-unified-v7821']":"registry['profiles']['all-routes-unified-v7857']",
        old:new,
        ";save(owned.CONFIG,conf)":"",
        'build_integrated_release_v7856.tmp':'build_integrated_release_v7910.tmp',
        "parent_profile='all-routes-unified-v7821'":"parent_profile='all-routes-unified-v7857'",
        'negative_count=128':'negative_count=131',
        'expected_manifest_batches=632':'expected_manifest_batches=633',
        "print('Registered experimentalV7857:632expectedbatches/114accepted;all prior profiles/mainV4701 preserved.No credit orpromotion.')":"print('Registered experimental V7911:633 expected batches/114 accepted; prior profiles and main preserved. No credit or promotion.')",
    }))
    rows.append(derive('scripts/build_retrospective_B218_v7857.py','scripts/build_Rafael_B45_v7911.py',{
        'retrospective_B218_build_v7857':'Rafael_B45_build_v7911',
        'retrospective_B218_registration_v7856':'Rafael_B45_registration_v7910',
        'all_routes_combined_v7857':'all_routes_combined_v7911',
        'all-routes-unified-v7857':'all-routes-unified-v7911'}))
    rows.append(derive('scripts/run_retrospective_B218_regressions_v7857.py','scripts/run_Rafael_B45_regressions_v7911.py',{
        'retrospective_B218_regressions_v7857':'Rafael_B45_regressions_v7911'}))
    rows.append(derive('scripts/verify_retrospective_B218_release_v7858.py','scripts/verify_Rafael_B45_release_v7912.py',{
        'lil_B218_retrospective_v2':'rafael_B45_editorial_v2',
        'retrospective_B218_release_v7858':'Rafael_B45_release_v7912',
        'all_routes_combined_v7857':'all_routes_combined_v7911',
        'all_routes_combined_v7821':'all_routes_combined_v7857',
        'retrospective_B218_registration_v7856':'Rafael_B45_registration_v7910',
        'retrospective_B218_build_v7857':'Rafael_B45_build_v7911',
        'retrospective_B218_regressions_v7857':'Rafael_B45_regressions_v7911',
        'all-routes-unified-v7857':'all-routes-unified-v7911',
        'all-routes-unified-v7821':'all-routes-unified-v7857',
        '==632':'==633',
        'all632':'all633',
        'all632batches':'all633batches',
        'manifest_batches=632':'manifest_batches=633',
        'lil_B218_retrospective':'rafael_B45_editorial',
        '/data/SC2.DK4':'/data/SC0.DK4',
        'retrospective_B218_atomic_v7854b':'Rafael_B45_atomic_positive_v7908',
        'len(ids)==1':'len(ids)==12',
        '==336':'==343',
        '==[218]':'==[45]',
        "conf['required_runtime_arm9_sha256']":"conf['predecessor_component_hashes']['/__arm9__.bin']",
        "b\"profile_config.get('maria_B36_editorial')\"":"b\"profile_config.get('lil_B218_retrospective')\"",
        'B218 retrospective wrap candidate;all632batches':'Rafael B45 candidate;all633batches',
        'B218 retrospective candidate':'Rafael B45 candidate',
        'only_SC2_B218_change_all335others_exact':'only_SC0_B45_change_all342others_exact',
        'batches=632':'batches=633',
    }))
    rows.append(derive('scripts/capture_Rafael_B45_context_v7867.py','scripts/capture_Rafael_B45_context_v7913.py',{
        'Rafael_B45_context_runs_v7867':'Rafael_B45_context_runs_v7913',
        'work/analysis/editorial_handoff_verification_v7866/verified_handoff.json':'work/analysis/Rafael_B45_release_v7912/registered_release_verification.json',
        'all-routes-unified-v7857':'all-routes-unified-v7911',
        'v7867_V7857':'v7913_V7911'}))
    rows.append(derive('scripts/bind_Rafael_B45_context_v7868.py','scripts/bind_Rafael_B45_context_v7914.py',{
        'Rafael_B45_context_binding_v7868':'Rafael_B45_context_binding_v7914',
        'Rafael_B45_context_runs_v7867/route0':'Rafael_B45_context_runs_v7913/route0',
        'papal_trade_startup_runs_v7663b/route0':'Rafael_B45_context_runs_v7867/route0',
        'current_V7857_Rafael_native_v7868':'current_V7911_Rafael_native_v7914',
        "'/data/SC0.DK4',":"",
        "    arm=image.read_file('/__arm9__.bin')":"    from dk4tool.formats.ilnk import IlnkContainer\n    a,b=[IlnkContainer.parse(im.read_file('/data/SC0.DK4')).blocks for im in [image,previous]]\n    assert len(a)==len(b)==343 and [i for i,(x,y) in enumerate(zip(a,b,strict=True)) if x!=y]==[45]\n    assert a[44]==b[44]\n    arm=image.read_file('/__arm9__.bin')",
        'V7857 Rafael':'V7911 Rafael',
        'Own V7857 Rafael':'Own V7911 Rafael'}))
    ROOT.mkdir(parents=True);save(ROOT/'source_locked_derivations.json',rows)
    print('Prepared registered workflow successors; no registry or ROM mutation.')
