"""Publish verified249 completion while retaining the next539-record editorial checkpoint."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load
from scripts.save_editorial_progress_checkpoint_v3 import checkpoint

ROOT=Path('work/analysis/Rafael_B51_B60_release_verified_20261104')
if __name__=='__main__':
    release_path=ROOT/'registered_release_verification.json';completion_path=ROOT/'completion_checkpoint.json'
    release,completion=map(load,[release_path,completion_path])
    assert completion['counts']==dict(completed=10774,revised=6356,retained=4418)
    assert not release['own_registered_startup_pending'] and release['clean_input_patch_byte_exact']
    summary=('Rafael249 isregistered,verified andcredited once:10774 completions(6356 revisions/4418 retentions). '
        'Experimental eb62870b passes669 entries/114 accepted layers/eight stages/26 checks,exact clean-input patch,own Rafael startup andboth Fernan getters. '
        'No live jobs;main unchanged. Next539 source meanings/22 name-role retentions/197 drafts/77 comparisons(40 revisions/37 retentions/four I corrections) arepreserved. '
        'Village120 comparison andremaining342 independent drafts are next;all display gates forthe539 remain pending. Fullscope/all ROMs retained;no guide photos.')
    document=Path('docs/editorial_rafael249_registered_and539_next_20261104.md')
    text=f'''# Verified249-record Rafael release andnext editorial work — 2026-11-04

Rafael early story andall tutorials remain first. Full all-story/earlier translations/shared shop-town/random/remaining player prose scope isactive. Preserve all prior work,retentions,credit,ROMs andevidence. No main promotion,commit/push,pruning orguide photos. Graphics artwork andlater older-record technical re-audit remain separate.

## New verified cumulative candidate

ROM:`{release['candidate']}`

SHA256:`{release['candidate_sha256']}`

Profile:`{release['profile']}`. Registry SHA256:`{release['registry_sha256']}`. All669 manifest entries/114 accepted layers/eight final stages/26 release checks pass. Build94922/PID24560 isterminal exit0. Release verifier47022 isterminal0;own startup andown Fernan name-getter verifiers areterminal0. No live jobs remain from this work.

Manifest:`{release['manifest']}`. Release proof:`{release_path}`. Exactly249 final source/current/target references andall five individual gates arebound in`{ROOT/'integrated_record_bindings.json'}`. Parent isverified4b10fd67 at`{release['parent']}`. Relative tothat parent,onlySC0 blocks51–60 andactor35's exclusive given-name F-width data change. All other files/components,code,fonts,pointers,allocations,graphics andunowned bytes areexact. Whole serialized inverse recovers the parent. The registered ASCII right-bound andall prior name/tutorial layers arepreserved.

Clean-input patch:`{release['patch']}`,SHA256`{release['patch_sha256']}`. It reconstructs thecomplete candidate byte-for-byte from`work/clean.nds`,SHA256`{release['clean_input_sha256']}`. Reconstructed ROM andall8-stage intermediates arepinned/preserved. The rejected uppercase-adapter preparation andrepaired lowercase binding remain historical evidence;no older profile/main was overwritten.

Own startup:`{ROOT/'own_registered_startup_verification.json'}`. Theplanned final image/candidate bytes match exactly,soits existing4001-frame ordinary title/NewGame/Rafael coldboot isreused. Allten frames match the prior directly reviewed RGB chain. Candidate-own final4MiB snapshot,complete123264-byte staged payload,native captain0/route0,actor root,protected names andsource-qualified Fernan-field inverse pass. No historical RAM overlay. Both original actor35 progressive/full-name getters return normal-ASCII Fernan Silveira fromthis own snapshot:`{ROOT/'own_Fernan_name_getter_verification.json'}`. Full catalogue UI remains unvisited.

## Completion credit andhonest coverage

`{completion_path}` credits249 exactly once:102 revisions/147 justified retentions,38 wrap fixes/three ASCII-I corrections. The separate Fernan F field earns no duplicate dialogue credit. Totals10774 complete/6356 revised/4418 retained;source/prose/draft historical counters10777 retain the older difference ofthree. All previous coverage keys,prefixes,unrelated ledger entries,next539 work andlater Hodram drafts remain exact.

Body/native/stored evidence covers all253 speech pages andfour choice captions;scoped18 progressive names arequalified. Two initialized fixtures observed32 distinct speeches/35 body pages/four captions/all18 speakers.213 speeches remain offline-only. Source00/FI/FA/FO,three FE notices,three I fixes,Fernan header,pagination andtwo menu cursor/acceptance continuations arechecked. Actual original location,earned chronology,full routes,hardware,original menu narrative branches/cancellation andfull catalogue UI remain unvisited. Offline branch/bridged-return/loaders checks are not gameplay credit. Reuse the complete existing evidence from`docs/editorial_rafael_B51_B60_research_ready_20261104.md` instead ofrepeating it.

The canonical main remains`out/raphael_natural_v2_accepted_base.nds`,SHA256`{release['canonical_sha256']}`. This candidate isexperimental andisnot promoted. Required user acceptance still applies toany main change.

## Continue next539 efficiently

See`docs/editorial_rafael_539_source197_drafts77_comparisons_20261104.md` forthe precise source/name/event context andfiles. All539 meanings in20source blocks61–80 aresealed;B68 iscontrol-only.22 public names/roles haveindividual justified retentions;private Eirene/Clau andsource-defined Estado trading-sphere references arebound.197 independent English drafts precede their extraction.77 complete-exchange comparisons have40 revisions/37 retentions andfour full-width I corrections;all fifth display gates remain false. The120-speech village conversation isalready drafted/extracted andawaits comparison.342 older-English speeches remain unselected:finish their independent drafts before exposing them.

The next source/current/name proofs still intentionally reference4b10fd67,the verified parent used while the build ran. Before building/formatting under eb62870b,qualify reuse by proving SC0B61–B80,COMMON/fonts/code/event table,22 scoped actor/name fields anddefault Rafael macros unchanged. The onlyARM9 change isactor35,which isabsent fromthose22;the changedSC0 blocks51–60 areoutside the next batch. Rebind current whole-archive/hash ancestry toeb62870b sofuture reconstruction preserves the249 just integrated. Do not relabel older snapshots asnew actual captures orrerun every compatible getter/native proof.

Prioritize natural dialogue andwraps in substantial complete exchanges. Keep the charity offer/offense/self-reflection echo coherent,the Romani identity/reported prejudice/approximate dates,private Eirene identity without a public rename,andPortugal threat versusannexation states. B69 hasfive FE Charlotte speeches duringCG presentation,not system notices;exact gesture remains unconfirmed. B77 includesa real direct-loss-to-Valdes alternative. Actor40's full-middleフォン/currentＦong remains an open text/name defect inside thefull objective,not graphics artwork. All other storylines/shared/town/random/tutorial/player text obligations remain in scope.
'''
    checkpoint(mutation=ROOT/'release_and539_checkpoint_mutation_v1',batch_key='Rafael_SC0_B61_B80_clean_20261104',
        batch_updates=dict(new_credit=0,latest_verified_integrated_parent=release['candidate'],latest_verified_integrated_parent_sha256=release['candidate_sha256'],
            earlier4b10fd67_name_current_andprose_proofs_preserved=True,eb62870b_dependency_requalification_pending=True,
            next_action='Compare thealready-drafted village120;draft remaining342 before current exposure;qualify reuse under verifiedeb62870b before formatting/build.'),
        additional_updates={'editorial_execution_priority_20261104':dict(new_credit=0,current_batch='Rafael_SC0_B61_B80_clean_20261104',
            previous249_registered_verified_andcredited_once=True,registered_cumulative_build_live=False,
            Rafael_early_story_andall_tutorials_first=True,full_editorial_scope_preserved=True,guide_photos=False)},
        summary=summary,document=document,document_text=text,completed=10774,
        protected={'translations/release_stack.json':release['registry_sha256'],release['candidate']:release['candidate_sha256'],
            release['patch']:release['patch_sha256'],'out/raphael_natural_v2_accepted_base.nds':release['canonical_sha256']})
    print('Checkpointed verifiedeb62870b/10774 completions;no live jobs/main unchanged. Next539 work preserved;village120 comparison next.',flush=True)
