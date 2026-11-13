"""Prepare source-locked registered build, regression, patch and startup successors."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/Rafael_B46_registered_tools_v7963')
if __name__=='__main__':
    assert not ROOT.exists()
    a=Path('scripts/register_Rafael_B45_v7910b.py');s=a.read_text('utf8')
    old=s[s.index('    profile.update('):s.index('    updated=deepcopy(registry)')]
    new="""    profile.update(status='experimental',rafael_B46_editorial=owned.CONFIG,
        description="Complete V7911 plus Rafael B46:24 speeches andtwo choices;seven source-grounded revisions andnineteen contextual retentions.",
        note="Fresh clean Japanese/B38 prerequisite andwhole conditional exchange before current comparison. Rafael Castor,Claudio Manaus,Julio Erneco retained from scoped source getters. Hayreddin component retention;full207 name review remains open. Accepting plays22speeches including12FE panels;declining plays7;both share unfinished private thought. Exact Y/L/R/A instructions,opposite mode orders,icons,city/fleet targets,land inside search frame,no invented kinship/rank/ambition/guaranteed discovery. Automatic full216px usable body width;FE228bitmap distinct;24full pages/96alignments,44fresh stored52reused,14original row-count infos/no waivers;native66px two-choice captions without padding. All37commands/five A000/6300/61FF/four relative spans,complete preambles/source00/zero macros andfull end/inverses preserved.343loads/686parent modes. Four disclosed original-entry fixtures,64004frames,58speech occurrences/214holds;all24unique speech/all37command union each language,original menu[2,0]/[2,1],normal[0,0]/[0,1].Source accept4930 highlight-off retained;no phase equality claim. Preserve27/12comparison rows,6/2duration differences;English+1LCGstep at B46 exits,later-159/-316,41/113 and96/173RGB differences;models,persistent objects,actors differ,accept calendar differs. No future-state/full simulation/complete causal equivalence.24policy positives/two labels/300rejections;whole-ROM atomic positive/187 independent precommit rejections. Two manifest batches include26objects exactly once. Fullgoal active;allfour stories/earlier prose,shared shops/towns/random/Help,retrospective wraps/names open;graphics/later older-record re-audit separate. MainV4701 unchanged;no separate unified package,promotion,pruning,commit orpush.")
"""
    rows=[]
    rows.append(derive(a,'scripts/register_Rafael_B46_v7963.py',{
        s.splitlines()[0]:'"""Register all26 B46 decisions after the complete V7911 stack, retaining both manifests."""',
        'rafael_B45_editorial_v2':'rafael_B46_editorial_v2',
        'scripts.Rafael_B45_release_paths_v7903':'scripts.Rafael_B46_release_paths_v7958',
        'Rafael_B45_registration_v7910':'Rafael_B46_registration_v7963',
        "PROFILE='all-routes-unified-v7911'":"PROFILE='all-routes-unified-v7964'",
        'Rafael_B45_atomic_challenges_v7909':'Rafael_B46_atomic_challenges_v7962',
        "result['positive_records']==12 and result['negative_count']==len(cases)==131":"result['positive_records']==26 and result['negative_count']==len(cases)==187",
        'editorial_handoff_verification_v7900':'editorial_handoff_verification_v7955',
        "['batches'])==632":"['batches'])==633",
        'rafael_B45_editorial':'rafael_B46_editorial',
        'apply_rafael_B45_editorial':'apply_rafael_B46_editorial',
        'Rafael B45 must run once after the complete V7857 stack':'Rafael B46 must run once after the complete V7911 stack',
        "b\"profile_config.get('lil_B218_retrospective')\"":"b\"profile_config.get('rafael_B45_editorial')\"",
        "registry['profiles']['all-routes-unified-v7857']":"registry['profiles']['all-routes-unified-v7911']",
        old:new,
        'build_integrated_release_v7910.tmp':'build_integrated_release_v7963.tmp',
        "parent_profile='all-routes-unified-v7857'":"parent_profile='all-routes-unified-v7911'",
        'negative_count=131':'negative_count=187',
        'expected_manifest_batches=633':'expected_manifest_batches=635',
        "print('Registered experimental V7911:633 expected batches/114 accepted; prior profiles and main preserved. No credit or promotion.')":
            "print('Registered experimental V7964:635 expected batches/114 accepted;two new manifests for26objects. Main/prior profiles preserved;no credit orpromotion.')",
    }))
    rows.append(derive('scripts/build_Rafael_B45_v7911.py','scripts/build_Rafael_B46_v7964.py',{
        'Rafael_B45_build_v7911':'Rafael_B46_build_v7964',
        'Rafael_B45_registration_v7910':'Rafael_B46_registration_v7963',
        'all_routes_combined_v7911':'all_routes_combined_v7964',
        'all-routes-unified-v7911':'all-routes-unified-v7964'}))
    rows.append(derive('scripts/run_Rafael_B45_regressions_v7911.py','scripts/run_Rafael_B46_regressions_v7964.py',{
        'Rafael_B45_regressions_v7911':'Rafael_B46_regressions_v7964'}))
    rows.append(derive('scripts/verify_Rafael_B45_release_v7912.py','scripts/verify_Rafael_B46_release_v7965.py',{
        'rafael_B45_editorial_v2':'rafael_B46_editorial_v2',
        'Rafael_B45_release_v7912':'Rafael_B46_release_v7965',
        'all_routes_combined_v7911':'all_routes_combined_v7964',
        'all_routes_combined_v7857':'all_routes_combined_v7911',
        'Rafael_B45_registration_v7910':'Rafael_B46_registration_v7963',
        'Rafael_B45_build_v7911':'Rafael_B46_build_v7964',
        'Rafael_B45_regressions_v7911':'Rafael_B46_regressions_v7964',
        'all-routes-unified-v7911':'all-routes-unified-v7964',
        'all-routes-unified-v7857':'all-routes-unified-v7911',
        '==633':'==635','all633':'all635','manifest_batches=633':'manifest_batches=635',
        'batches=633':'batches=635',
        'rafael_B45_editorial':'rafael_B46_editorial',
        'Rafael_B45_atomic_positive_v7908':'Rafael_B46_atomic_positive_v7961',
        'len(ids)==12':'len(ids)==26',
        '==[45]':'==[46]',
        "list(owned.PATHS)":"[owned.PATH]",
        "b\"profile_config.get('lil_B218_retrospective')\"":"b\"profile_config.get('rafael_B45_editorial')\"",
        'Rafael B45 candidate':'Rafael B46 candidate',
        'only_SC0_B45_change_all342others_exact':'only_SC0_B46_change_all342others_exact',
    }))
    rows.append(derive('scripts/capture_Rafael_B45_context_v7913.py','scripts/capture_Rafael_B46_context_v7966.py',{
        'Rafael_B45_context_runs_v7913':'Rafael_B46_context_runs_v7966',
        'Rafael_B45_release_v7912':'Rafael_B46_release_v7965',
        'all-routes-unified-v7911':'all-routes-unified-v7964',
        'Rafael_B45_route':'Rafael_B46_route',
        'v7913_V7911':'v7966_V7964',
        'B45 activation':'B46 activation',
        'optional_B45_activation':'optional_B46_activation',
    }))
    rows.append(derive('scripts/bind_Rafael_B45_context_v7914.py','scripts/bind_Rafael_B46_context_v7967.py',{
        'Rafael_B45_context_binding_v7914':'Rafael_B46_context_binding_v7967',
        'Rafael_B45_context_runs_v7913/route0':'Rafael_B46_context_runs_v7966/route0',
        'Rafael_B45_context_runs_v7867/route0':'Rafael_B45_context_runs_v7913/route0',
        'current_V7911_Rafael_native_v7914':'current_V7964_Rafael_native_v7967',
        '==[45]':'==[46]',
        'V7911 Rafael':'V7964 Rafael',
        'optional_B45_activation':'optional_B46_activation',
        'B45 not activated':'B46 not activated',
    }))
    rows.append(derive('scripts/record_Rafael_B45_startup_view_v7915.py','scripts/record_Rafael_B46_startup_view_v7968.py',{
        'Rafael_B45_startup_view_v7915':'Rafael_B46_startup_view_v7968',
        'Rafael_B45_context_binding_v7914':'Rafael_B46_context_binding_v7967',
        'V7857':'V7911','own-V7911':'own-V7964',
        'no_new_B45_activation':'no_new_B46_activation',
    }))
    ROOT.mkdir(parents=True);save(ROOT/'source_locked_derivations.json',rows)
    print('Prepared B46 registered workflow successors;no registry/ROM mutation. Atomic receipt required before registration.')
