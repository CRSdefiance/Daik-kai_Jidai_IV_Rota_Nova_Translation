"""Record the source stochastic cause and matching-phase verification honestly."""

import copy
import shutil
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from scripts.native_ceremony_rand_trace_v822 import ROOT
from scripts.verify_village_wrap_v608 import read,save

LEDGER=Path('translations/editorial_review_current_v1.json')
DOC=Path('docs/ceremony_random_cause_v824_checkpoint.md')
SUMMARY=('V821-V824 maps the post-climb mismatch to original scheduler entropy:the input-release wait at020C9CAC yields through020C9D98,whose020C9DA0 RAND call advances the generator then discards its result.'
    'The first early difference is exactly that source call;later growth/daily updates receive different ordinary random inputs.'
    '168 trace checkpoints are audited;one transient observer difference at18233 is retained,so no all-frame transparency claim is made.'
    'A separate4-byte test control omits only the discarded scheduler advance after18200,without supplying seeds or outcomes.'
    '44 matching-phase checkpoints across V803/V809/V820 have identical complete state and PRNG,including the192-tick return;two in-progress points have explicitly different native calendar progress.'
    'Original strict frame/uncontrolled-outcome failures remain recorded and unchanged;they are not presented as passes.'
    'An ordinary V820 replay independently matches V809 at46 state/PRNG checkpoints,44 whole-screen controls,26 complete ceremony holds andtwo repaired stat holds.'
    'No production ROM,patch or registry changes. V820 remains current;14 other-protagonist reactions and final ceremony approval remain next.'
    '550 completed/605 source-prose/55 pending unchanged;full editorial and separate graphics goals remain unfinished.')


def main():
    trace=read(ROOT/'phase_scoped_generator_trace_v824.json')
    causal=read(ROOT/'matching_phase_yield_control_v824.json')
    ordinary=read(ROOT/'V820_uncontrolled_ceremony_display_and_state_v824.json')
    failure=read(ROOT/'retained_strict_frame_gate_failures_v824.json')
    assert len(trace['controls'])==168 and len(trace['transient_observer_differences'])==1
    assert causal['count']==44 and len(causal['explicitly_different_in_progress_phases'])==2
    assert len(ordinary['complete_state_and_PRNG_pairs'])==46 and len(ordinary['complete_ceremony_holds'])==26
    assert len(ordinary['two_additional_complete_stat_holds'])==2 and len(failure['failures'])==2
    stage=read('work/analysis/levelup_format_v819/registered_release_verification_v820.json')
    assert sha(Path(stage['candidate']).read_bytes())==stage['candidate_sha256']==ordinary['candidate_sha256']
    assert sha(Path(stage['patch']).read_bytes())==stage['patch_sha256']
    manifest=read('out/all_routes_combined_v820_candidate.manifest.json')
    assert manifest['release_stack_sha256']==sha(Path('translations/release_stack.json').read_bytes())
    cfg=read('translations/levelup_stat_format_release_v1.json')
    assert all(sha(Path(k).read_bytes())==v for k,v in cfg['dependencies'].items())
    DOC.write_text('''# V824: post-climb random-state difference explained

'''+SUMMARY+'''

## Source and actual trace

The original positive-modulus wrapper020519D4 is not the generator's only caller.
The initial source code also calls RAND directly at020C9DA0, inside020C9D98.
The return is overwritten with zero at020C9DA8. The routine then checks the game
state and task status and yields through the original cooperative scheduler.
The input-mask/event wait calls this routine at020C9CAC; the later town wait calls
it at020B6FE0. These functions, the generator, original ritual effects and ordinary
wrapper are byte-identical to clean source in V803,V809 and V820.

The trace is installed only at the existing18200-frame pause in disposable runs.
An existing160-byte alternate-header span holds the logger and four-record ring;
an entry sentinel verifies that header path is not used afterward. No allocation,
seed, actor, town, inventory, calendar or source-ROM file is supplied or changed.
36 direct-generator/wrapper native contracts preserve ABI and all8MiB outside the
owned code/stack. Six source early-return controls prove that the causal test
changes only the otherwise discarded random step and its instruction bytes.

At18203,V803 has one generator call and V809 has zero. Its return address maps to
the original input-wait yield at020C9CAC. At18205 both have one call; later, one
version enters the first stat-growth calculation after one discarded advance,
the other after two. At18600 the observed total generator calls are860 and870,
matching the earlier independently calculated LCG reachability counts. Every
observed ring seed and aggregate count matches the original generator chain.

This is scoped evidence. The logger preserves early controls through18224 and
settled controls from18600,including complete persistent state and random streams.
One V803 intermediate sample at18233 differs under instrumentation. The strict
all-frame trace assertion therefore remains FAILED and is saved verbatim.
The four-record ring is not a complete ordered log of every simulation call.

## Causal control and native completion phases

Separate cold boots of V803,V809 and V820 replay the identical ordinary controller
and isolated calendar/access inputs. At18200 only the four-byte discarded-RAND
call is replaced with a temporary no-op. No seed or expected actor/town outcome is
written. The original generator, ritual effects, stat growth, town simulation,
calendar and UI/input methods continue to run. This is a diagnostic control;
the source-ROM files and production V820 retain the original discarded RAND call.

All three versions agree at44 matching input/completion checkpoints. Comparison
includes all207 actors and the current captain,all90 towns,items,goods,ship/fleet
models,tasks,funds,calendar and PRNG. The original four-day192-tick advance and
town return agree, including subsequent sampled cancellation/off-day returns.

Two extra observations are deliberately inside the update:at18220 the calendar
is33214 versus33215;at18240 it is33218 versus33223. All values are inside the same
33214..33406 four-day update. These are different native progress points. They
are reported,not called equivalent. The original strict all-frame control also
remains FAILED at18220 and is saved without deleting any assertion. Once all
three runs finish at18600 and through20000,the complete states and PRNG agree.

The old unmodified-ROM assertion at18600 is still a historical exact-random-world
failure. Its cause is now mapped:translated UI execution changes source wait-yield
counts,which advance a shared random stream. Equal ordinary random outcomes are
not claimed. The controlled evidence establishes matching source simulation and
effects under matching random input;it does not justify changing the shipped RNG
or waiving unrelated state differences elsewhere.

## Current V820 ordinary replay

An additional V820 cold boot has no post-acknowledgment trace or entropy control.
It retains only the already declared isolated Athens calendar/access inputs.
All46 state/PRNG checkpoints match ordinary V809,including its historical random
results.44 complete two-screen frames match. The only two changed frames are
the intended stat bodies at9000/9800;both have complete independent/native fonts,
aligned rows,all letters/numbers and exact outside pixels.26 ceremony holds are
whole-frame identical to the previously verified complete glyph/blank-plane
captures;COMMON templates,font files and their formatters are unchanged.

## Identity and progress

V820 remains `out/all_routes_combined_v820_candidate.nds`,SHA-256
`'''+stage['candidate_sha256']+'''`. Its exact clean-input patch and registered
manifest are unchanged. No new candidate,production code,registry or prose is
generated by this investigation. All original donor saves remain unchanged.

The source random-yield cause is understood;matching-phase controlled outcomes
and V820 ordinary regression checks pass. The next work is the14 distinct
Rafael/Lil/Maria ceremony reactions under their actual protagonist identities,
including creating a normal-save Lil donor,then final whole-family review.
The52-entry ceremony family receives no completion credit yet. Older750-752,
Angelo/sulfur findings,all remaining routes and player-facing prose stay in scope.
Graphics and all18 plaques remain separate unfinished audit work. The goal is active.
''',encoding='utf-8')
    ledger=read(LEDGER);assert ledger['goal_status']=='active' and not ledger['full_goal_complete']
    assert (ledger['records_editorially_completed'],ledger['records_with_source_and_prose_pass'])==(550,605)
    backup=ROOT/'editorial_ledger_before_v824.json'
    if not backup.exists():shutil.copyfile(LEDGER,backup)
    detail=dict(status='source-discarded-RAND-cause-mapped;matching-native-completion-controlled-outcomes-verified',
        documentation=str(DOC),source_proof=str(ROOT/'source_random_yield_cause_v824.json'),
        scoped_trace=str(ROOT/'phase_scoped_generator_trace_v824.json'),
        controlled_outcomes=str(ROOT/'matching_phase_yield_control_v824.json'),
        retained_strict_failures=str(ROOT/'retained_strict_frame_gate_failures_v824.json'),
        ordinary_V820_replay=str(ROOT/'V820_uncontrolled_ceremony_display_and_state_v824.json'),
        original_V817_exact_random_outcome_gate_remains_failed=True,
        no_unexplained_translation_world_state_regression_observed_in_this_climb_test=True,
        ordinary_random_outcome_equivalence_to_V803_not_claimed=True,
        no_production_RNG_ROM_patch_or_registry_change=True,
        completion_credit=0,full_goal_complete=False)
    ledger['ceremony_post_climb_source_cause_v824']=detail
    pending=ledger['pending_registered_ceremony_candidate']
    if 'broader_ceremony_world_state_failure_unresolved' in pending:
        pending['historical_world_state_failure_unresolved_at_V820_build']=pending.pop('broader_ceremony_world_state_failure_unresolved')
    pending.update(status='source-random-yield-cause-mapped;controlled-completion-and-V820-display-verified;other-protagonists-and-final-family-pending',
        post_climb_source_cause=detail,latest_ordinary_V820_gameplay=str(ROOT/'V820_uncontrolled_ceremony_display_and_state_v824.json'))
    if 'latest_registered_formatting_candidate' in ledger:
        ledger['latest_registered_formatting_candidate']['post_build_ceremony_cause_followup']=detail
    packet=ledger['next_ceremony_source_packet']
    packet.update(status='37-distinct-IDs-glyph-verified;random-source-cause-mapped-and-controlled-effects-verified;other-protagonists-pending',
        post_climb_source_cause=detail,
        next='Verify14 distinct reactions under real Rafael/Lil/Maria identities;create a normal-save Lil donor;finish52-entry ceremony family review,then older750-752 and remaining route/player-facing prose.')
    ledger['active_source_prose_drafts']['note']=('51 production ceremony paragraphs retain201 native fonts/layouts. Historical59 holds cover37 distinct IDs;'
        'V824 replays26 of them under ordinary V820 and verifies the repaired stat notices. Source scheduler RNG explains the earlier post-climb difference;'
        'controlled completed world effects agree across803/809/820.14 real protagonist reactions and whole52 review remain;3 older750-752 contexts stay open.')
    ledger['latest_checkpoint']=SUMMARY
    ident='V821-V824-source-random-yield-cause-and-controlled-effects'
    if not any(r['id']==ident for r in ledger['research_checkpoints']):
        ledger['research_checkpoints'].append(dict(id=ident,documentation=str(DOC),new_ROM=False,
            new_source_prose_reviewed=0,new_editorially_completed=0,full_goal_complete=False))
    assert ledger['next_integrated_profile_for_goal_continuation']=='all-routes-unified-v820'
    save(LEDGER,ledger)
    for name in ('translation_progress.md','known_issues.md','todo.md','editorial_review_goal.md'):
        p=Path('docs')/name;s=p.read_text(encoding='utf-8');heading='## V824: source random-yield cause mapped; controlled effects verified'
        if heading not in s:p.write_text(s+'\n\n'+heading+'\n\n'+SUMMARY+' See [source and controlled evidence](ceremony_random_cause_v824_checkpoint.md).\n',encoding='utf-8')
    archive=Path('E:/Rota Nova translations/Editorial review/V824 Ceremony random-state cause');archive.mkdir(parents=True,exist_ok=True)
    sources=[DOC,LEDGER,Path(__file__),*ROOT.glob('*.json'),
        *Path('work/analysis/ceremony_rng_v821').glob('*.json'),
        *(Path('scripts')/n for n in ('native_ceremony_rng_trace_v821.py','run_ceremony_rng_trace_v821.py',
          'native_ceremony_rand_trace_v822.py','run_ceremony_rand_trace_v822.py',
          'native_ceremony_yield_control_v823.py','run_ceremony_yield_control_v823.py',
          'run_ceremony_uncontrolled_v820_v823.py','verify_ceremony_random_cause_v823.py',
          'audit_ceremony_random_cause_v824.py','verify_ceremony_V820_display_v824.py'))]
    artifacts=[]
    for source in sources:
        sub='scripts' if source.parent==Path('scripts') else 'wrapper-trace' if source.parent.name=='ceremony_rng_v821' else 'verification' if source.parent==ROOT else 'checkpoint'
        target=archive/sub/source.name;target.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(source,target)
        assert sha(source.read_bytes())==sha(target.read_bytes())
        artifacts.append(dict(source=str(source),archived=str(target),sha256=sha(target.read_bytes())))
    save(archive/'archive_manifest.json',dict(artifacts=artifacts,candidate=stage['candidate'],candidate_sha256=stage['candidate_sha256'],
        no_new_ROM_patch_or_registry_changes=True,all_capture_data_already_on_E_drive=True,
        native_random_cause_verified_with_qualified_trace_and_matching_phase_controls=True,
        original_strict_failures_retained=True,no_new_editorial_completion_credit=True,full_goal_complete=False))
    print('V824 source cause,qualified trace,44 matching-phase3-version controls and46 ordinary V820 regression points recorded. No ROM changes;goal active;14 hero reactions next.',flush=True)


if __name__=='__main__':main()
