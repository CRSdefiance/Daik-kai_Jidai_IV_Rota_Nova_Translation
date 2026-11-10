"""Prepare registry/build/regression/exact-patch tools after complete B49 atomic validation."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/Rafael_B49_release_tools_v8121')
if __name__=='__main__':
    assert not ROOT.exists()
    source=Path('scripts/register_Rafael_B48_v8065.py').read_text('utf8')
    old_profile=source[source.index('    profile.update('):source.index('    updated=deepcopy',source.index('    profile.update('))]
    profile='''    profile.update(status='experimental',rafael_B49_editorial=owned.CONFIG,
        description='Complete V8066 plus Rafael B49:61 speeches,31 contextual revisions and30 justified retentions.',
        note="Complete clean Japanese exchange,22-speech B39 prerequisite and27-speech B41 destination context precede current English. Seven source speakers andthree mentioned identity components;256 complete structural text paths,156250 result compositions. Preserve Lil's blunt bravado,Camille's restraint,Rafael's mild perceptiveness,conditional Janus/Claudio alternatives,prospective regional ambition,unfinished Hodram Ber... something joke,surname-only Clifford,Martin Speyer/Hanseatic League,temporary trade request,proposed pact rather than completed alliance,common-enemy optional exchange andqualified closing. All154commands/56relative sites/13raw predicates/one completion query/sevenA000/C281/fullend andcomplete inverses remain. Original00/02/09 andseven selectors,twoFI,noFE,all61singlepages216px/four rows. Final native20fresh224reused,stored124fresh120reused;22original infos/three exact warning scopes.343load/cache paths/686parent modes,61policy positives/1014guard rejections,one final file-list commit exact full-reference positive and413independent precommit semantic rejects. Paired disclosed B44initialized-entry fixtures48002frames,50actual speeches/50pages perlanguage,318complete body/name holds,22directly viewed sheets. Actual headers Rafael,Lil,Claudio,Camille;three native-only headers andeleven native-only conditional speeches remain explicit. C281's original effect executes at4016-4017,2bytes,[3,0],equal UIrequests/no internal RNGadvance;transition/Lil/Camille names/return verified. Normal exits16013/16016;retain111comparisonrows/18duration differences,exitEnglishLCG+3/final+2,seeds3456469704/204362374. Final sampled state/models/persistent/tasks/calendar/wholeactor equal;19of134later fullRGB differ. No natural Amsterdam event49 activation,fullroute,hardware,every-call causal orfuture-state equivalence claim. Full editorial goal/allfourstories/earlier dialogue/sharedshop/town/random/Help/wraps/all207names remain active;graphics andlater older-record technical re-audit separate. Preserve allprior ROMs/translations. MainV4701 unchanged;no separate unified package,promotion,pruning,commit orpush.")
'''
    a=derive('scripts/register_Rafael_B48_v8065.py','scripts/register_Rafael_B49_v8121.py',{
        old_profile:profile,
        'Rafael_B48_release_paths_v8060':'Rafael_B49_release_paths_v8114',
        'Rafael_B48_registration_v8065':'Rafael_B49_registration_v8121',
        'Rafael_B48_atomic_challenges_v8064':'Rafael_B49_atomic_challenges_v8120',
        'editorial_handoff_verification_v8045':'editorial_handoff_verification_v8116',
        'all-routes-unified-v8066':'all-routes-unified-v8122',
        'all-routes-unified-v8013':'all-routes-unified-v8066',
        'B48':'B49','V8013':'V8066','V8066:637':'V8122:638',
        'Rafael_B47_editorial':'Rafael_B48_editorial','rafael_B47_editorial':'rafael_B48_editorial',
        "result['positive_records']==91":"result['positive_records']==61",
        "result['negative_count']==len(cases)==455":"result['negative_count']==len(cases)==413",
        "['batches'])==636":"['batches'])==637",'negative_count=455':'negative_count=413','expected_manifest_batches=637':'expected_manifest_batches=638',
        'build_integrated_release_v8065.tmp':'build_integrated_release_v8121.tmp',
        'complete91-object':'complete61-object','one new91-object':'one new61-object',
    })
    b=derive('scripts/build_Rafael_B48_v8066.py','scripts/build_Rafael_B49_v8122.py',{
        'Rafael_B48_build_v8066':'Rafael_B49_build_v8122',
        'all_routes_combined_v8066':'all_routes_combined_v8122','all-routes-unified-v8066':'all-routes-unified-v8122',
        'Rafael_B48_registration_v8065':'Rafael_B49_registration_v8121',
    })
    c=derive('scripts/run_Rafael_B48_regressions_v8066.py','scripts/run_Rafael_B49_regressions_v8122.py',{
        'Rafael_B48_regressions_v8066':'Rafael_B49_regressions_v8122',
    })
    d=derive('scripts/verify_Rafael_B48_release_v8067.py','scripts/verify_Rafael_B49_release_v8123.py',{
        'Rafael_B48_release_v8067':'Rafael_B49_release_v8123',
        'all_routes_combined_v8066':'all_routes_combined_v8122',
        'all_routes_combined_v8013':'all_routes_combined_v8066',
        'all-routes-unified-v8066':'all-routes-unified-v8122','all-routes-unified-v8013':'all-routes-unified-v8066',
        'Rafael_B48_registration_v8065':'Rafael_B49_registration_v8121',
        'Rafael_B48_build_v8066':'Rafael_B49_build_v8122','Rafael_B48_regressions_v8066':'Rafael_B49_regressions_v8122',
        'Rafael_B48_atomic_positive_v8063':'Rafael_B49_atomic_positive_v8119',
        'B48':'B49','B47':'B48',
        "registration['negative_count']==455":"registration['negative_count']==413",
        "registration['expected_manifest_batches']==637":"registration['expected_manifest_batches']==638",
        "len(manifest['batches'])==637":"len(manifest['batches'])==638",'manifest_batches=637':'manifest_batches=638','all637':'all638','batches=637':'batches=638',
        'len(ids)==91':'len(ids)==61','==[48]':'==[49]',
    })
    ROOT.mkdir(parents=True);save(ROOT/'source_locked_derivations.json',[a,b,c,d])
    print('Prepared registered B49 V8122 build and checks; registration requires all413 atomic rejects first.')
