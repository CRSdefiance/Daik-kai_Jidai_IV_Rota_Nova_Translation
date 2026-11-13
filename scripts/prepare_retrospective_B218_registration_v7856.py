"""Source-lock registration and complete cumulative build/regression producers."""
import ast
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive,checked_text
from scripts.verify_village_wrap_v608 import save
if __name__=='__main__':
    root=Path('work/analysis/retrospective_B218_registration_tools_v7856');assert not root.exists()
    source=Path('scripts/register_Maria_B36_v7820.py').read_text(encoding='utf-8');tree=ast.parse(source)
    call=next(n for n in ast.walk(tree) if isinstance(n,ast.Call) and isinstance(n.func,ast.Attribute)
        and n.func.attr=='update' and any(k.arg=='description' for k in n.keywords))
    description=next(k.value for k in call.keywords if k.arg=='description');note=next(k.value for k in call.keywords if k.arg=='note')
    changes={
        ast.get_source_segment(source,description):repr("Complete V7821 plus one retrospective automatic-wrap refinement in Lil SC2B218 R27. All13 existing English wordings are individually retained after complete clean/current context review;12 stored speeches remain exact. Keep That's a surprise together after the private question. No new words,story facts,names,controls,macros,font,width orduplicate editorial credit."),
        ast.get_source_segment(source,note):repr("All13 individual review gates pass. Fresh own-V7821 Lil context,captain2/whole actors/six RGB controls;one changed native page/before-after planes/12 processor alignments,four stored parity-tail cases,all13 final dispatches,15 original commands13 preambles/no relative predicates ormenus,A000 andfour-byte end/tail2. Old1016/logical1016/tail0 ->1020/logical1018/tail2;both block inverses/full predecessor archive inverse,335 otherblocks/allotherfiles/components exact.336 native loads/cache hits672 parentmodes andbounded shippedcaller census. Paired previous/proposed16001-frame English fixtures each13 speeches/all24 commands,51complete body/name holds;26panes/102holds,eight sheets viewed,zero partials. Both exit5975;onlyeight offset/length comparison rows differ;no durations/results/UI/RNG/167 sampled laterRGB/five finalcomponents/wholeactors/seed differences. Keep natural activation,original location,fullmechanics,fullroute,hardware,everyframe/fullRAM/future/causal limits explicit.13 positive/221 policy rejections;one atomic positive/128 actual-changing production rejections withconfig dependency checks bypassed,no negative commits. Preserve all prior artifacts/fullgoal/207names/retrospectivewraps,graphicsseparation/latertechnicalaudit. MainV4701unchanged;no separatepackage,promotion,pruning,commit orpush."),
        'maria_B36_editorial_v1':'lil_B218_retrospective_v2',
        'scripts.Maria_B36_final_paths_v7816b':'scripts.retrospective_B218_final_paths_v7853',
        'work/analysis/maria_B36_registration_v7820':'work/analysis/retrospective_B218_registration_v7856',
        'work/analysis/maria_B36_atomic_challenges_v7819':'work/analysis/retrospective_B218_atomic_challenges_v7855',
        'editorial_handoff_verification_v7817d':'editorial_handoff_verification_v7852',
        'all-routes-unified-v7821':'all-routes-unified-v7857',
        'all-routes-unified-v7779':'all-routes-unified-v7821',
        "result['positive_records']==16":"result['positive_records']==13 and result['changed_records']==1",
        'len(cases)==120':'len(cases)==128',
        "['batches'])==630":"['batches'])==631",
        "profile_config.get('maria_story_editorial')":"profile_config.get('maria_B36_editorial')",
        'maria_B36_editorial':'lil_B218_retrospective',
        'maria_B36':'lil_B218_retrospective',
        'Maria B36':'B218 retrospective',
        'V7779':'V7821',
        'negative_count=120':'negative_count=128',
        'expected_manifest_batches=631':'expected_manifest_batches=632',
        'experimentalV7821:631expectedbatches':'experimentalV7857:632expectedbatches',
        'build_integrated_release_v7778.tmp':'build_integrated_release_v7856.tmp',
    }
    jobs=[('scripts/register_Maria_B36_v7820.py','scripts/register_retrospective_B218_v7856.py',changes),
        ('scripts/build_Maria_B36_v7821.py','scripts/build_retrospective_B218_v7857.py',{
            'maria_B36_build_v7821':'retrospective_B218_build_v7857',
            'all_routes_combined_v7821_candidate':'all_routes_combined_v7857_candidate',
            'maria_B36_registration_v7820':'retrospective_B218_registration_v7856',
            'all-routes-unified-v7821':'all-routes-unified-v7857'}),
        ('scripts/run_Maria_B36_regressions_v7821.py','scripts/run_retrospective_B218_regressions_v7857.py',{
            'maria_B36_regressions_v7821':'retrospective_B218_regressions_v7857'})]
    for a,b,c in jobs:assert not Path(b).exists();checked_text(Path(a).read_text(encoding='utf-8'),c)
    outputs=[derive(*job) for job in jobs]
    root.mkdir(parents=True);save(root/'provenance.json',dict(derivations=outputs,
        complete_predecessorV7821_registry_builder_one_stage_andall_prior_profiles_preserved=True,
        parent631_expected632_batches114accepted_mainV4701_unchanged=True,
        atomic13_reviewed_one_changed_record128_rejections_required=True,
        no_duplicate_editorial_credit_orpromotion=True,full_goal_complete=False))
