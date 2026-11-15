"""Save substantial source/prose progress andthe existing build's authoritative process state."""
import ctypes as ct
from datetime import datetime,timezone
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load,save
from scripts.save_editorial_progress_checkpoint_v3 import checkpoint

ROOT=Path('work/analysis/Rafael_B61_B80_clean_20261104')
PREP=Path('work/analysis/Rafael_B51_B60_release_registry_v2_20261104/registered_preparation.json')
RELEASE=Path('work/analysis/Shared_tutorial_name_data_release_verified_20261104/registered_release_verification.json')
PID=24560
SESSION=94922

if __name__=='__main__':
    source_path=ROOT/'all539_clean_meanings_v1.json';identity_path=ROOT/'source_identity_event_andterm_checkpoint_v1.json'
    drafts_path=ROOT/'B61_B64_all197_sealed_drafts_v1.json';comparison_path=ROOT/'B61_B63_77_whole_exchange_comparison_v1.json'
    names_path=Path('translations/rafael_B61_B80_scoped_names_andterms_v1.json')
    current_path=Path('work/analysis/Rafael_B61_B64_current_20261104/current_effective.json')
    source,identity,drafts,comparison,names,current,prepared,release=map(load,[source_path,identity_path,drafts_path,comparison_path,names_path,current_path,PREP,RELEASE])
    assert len(source['records'])==len(identity['records'])==539 and len(drafts['records'])==current['records']==197
    assert len(comparison['records'])==77 and (comparison['proposed_revisions'],comparison['justified_retentions'])==(40,37)
    assert sum(r['fullwidth_I_replaced'] for r in comparison['fullwidth_I_corrections'])==4 and len(names['records'])==22
    kernel=ct.WinDLL('kernel32',use_last_error=True)
    kernel.OpenProcess.argtypes=[ct.c_ulong,ct.c_int,ct.c_ulong];kernel.OpenProcess.restype=ct.c_void_p
    kernel.GetExitCodeProcess.argtypes=[ct.c_void_p,ct.POINTER(ct.c_ulong)];kernel.GetExitCodeProcess.restype=ct.c_int
    kernel.CloseHandle.argtypes=[ct.c_void_p];kernel.CloseHandle.restype=ct.c_int
    handle=kernel.OpenProcess(0x1000,False,PID)
    status=None
    if handle:
        try:
            value=ct.c_ulong();assert kernel.GetExitCodeProcess(handle,ct.byref(value));status=value.value
        finally:kernel.CloseHandle(handle)
    observed=datetime.now(timezone.utc).isoformat();live=status==259
    state=('OS-confirmed live' if live else 'process terminal ormissing;poll its existing exec session for the final result')
    snapshot=ROOT/'existing_build_status_at_language_checkpoint_v1.json';assert not snapshot.exists()
    save(snapshot,dict(PID=PID,exec_session_id=SESSION,Windows_process_exit_code=status,observed_UTC=observed,
        process_confirmed_live=live,state=state,repoll_same_session_before_any_restart=True,
        expected_final_ROM_sha256=prepared['target_ROM_sha256'],no_release_completion_claim=True,new_credit=0))
    summary=(f'Rafael/tutorial priority:the249-record eight-stage build94922/PID24560 is{state}. Final manifest/patch/own RAM binding remain. '
        'Next B61–B80 hasall539 clean source meanings,22 individually retained speaker names/roles,and197 independent English drafts. '
        'First77 whole-exchange comparisons yield40 revisions/37 justified retentions,plusfour full-width I corrections inthree retained speeches;formatting gates pending. '
        '120 extracted speeches await comparison;342 older-English speeches remain unselected. 10525 integrated completions/verified4b10fd67/main unchanged;full scope/all ROMs preserved;no guide photos.')
    document=Path('docs/editorial_rafael_539_source197_drafts77_comparisons_20261104.md')
    text=f'''# Rafael source andnatural-dialogue progress — 2026-11-04

The previous goal turn made concrete progress:registered/qualified249 reviews andbegan the cumulative build. This turn completes539 source meanings,22 scoped name/role decisions,197 independent English drafts and77 contextual comparisons. Full all-story/shared/town/random/tutorial/player prose scope remains active. Preserve all earlier translations,retentions,coverage credit,evidence andROMs. No main promotion,commit/push,pruning orguide photos. Graphics artwork andlater older-record technical re-audit remain separate.

## Existing registered build

Session `{SESSION}`,PID `{PID}`,status at`{observed}`:`{state}`;Windows exit code`{status}`. Snapshot:`{snapshot}`. Poll this exact session orverify its command/process;quiet output is not failure. Do not restart it because an observation times out. The canonical log wasquiet butthe process was repeatedly confirmed live;the last explicit session poll still returned session94922 rather than terminal output.

Eight-stage command/profile/configs/12 semantic rejections andthe repaired lowercase adapter aredocumented in `docs/editorial_rafael_B51_B60_build_and197_source_20261104.md`. Authoritative preparation:`{PREP}`;current registry SHA256`{prepared['registry_sha256']}`. Expected final target`{prepared['target_ROM_sha256']}` at`out/all_routes_combined_rafael_b51_b60_Fernan_20261104_candidate.nds`. Work path`work/f8`.

No final output/manifest/patch/own registered RAM binding or249 completion credit is granted by this checkpoint. The exact planned final identity already has4001 ordinary coldboot frames/ten reviewed RGB matches under`work/analysis/Rafael_B51_B60_identity_coldboot_20261104`;reuse those captures once registered output equality is proved. Then verify all114 accepted layers,eight final stages,source-bound SC0/Fernan bytes/unowned preservation,clean-input xdelta reconstruction andown native captain0/route0/payload/name getters before once-only credit. Main remains`out/raphael_natural_v2_accepted_base.nds`,SHA256`{release['canonical_sha256']}`. Prior verified release4b10fd67 andits patch remain protected.

## Next539 source meanings andidentities

`{source_path}` contains539 exact individual clean meanings forB61–B80;all six constituent glosses arepreserved. B68 iszero-speech/control-only,not omitted prose. All20 complete source blocks,including the pause/gesture records,were read before the matching current English. Broad clean context andcross-scene links remain in the consolidated receipt. No current prose has been read forthe remaining342 speeches inB65–B80.

`{identity_path}` binds22 identities,all source/current given/surname/middle fields,20EV0 entry/dependency contexts andsource command cues. Twelve actors havefresh clean/current native getter/voice bindings (24 clean and24 current consumers);ten actor proofs areexact qualified reuses. The two previously corrected catalogue components arequalified by undoing only four disjoint tutorial spans to recover their tested name image. Current539-name/context proof uses the verified4b10fd67 own Rafael snapshot;the pending successor changes onlyB51–B60 andactor35,which is absent from these22 actors. After that release isverified,qualify exact code/font/SC0B61–B80/actor inputs before reusing these proofs. Do not simply relabel the old snapshot asnew gameplay.

Source event membership isstructural,not earned activation:63 requires145;65 requires131;66 requires65;67 requires158;68 requires67;69 requires68/151;71 excludes72;73 requires63;75 requires151/excludes21/11/77/78;76 requires141;77 requires23/excludes78/22;78 excludes22/77. Remaining native eligibility predicates areunexecuted. Numerical block order is not chronology. All raw event conditions/prerequisites arepreserved in the receipt.

`{names_path}` individually retains22 public progressive identities/roles,withspecific reasons andexact references. Private Eirene/Clau uses areexplicitly distinguished from public Arcadius/Claudio nameplates. The actual clean actor151 progressive getter is水夫/Sailor;its unused catalogue配下 must not become feudal Retainer. Trader104/106 remain distinct source actors,PortWorker113 isnot a royal official merely forcarrying a summons,Priest139 isnot HighPriest,andVillager179 isnot an invented chief/ethnicity. Xien Yan remains the established sound-preserving spelling without a claim of official romanization. Maria Huamei Li/user-approved names remain locked. All name display gates remain pending;full catalogue/global207 approval isnot granted. Actor40 full-middleフォン/currentＦong spelling/glyph issue stays explicitly open.

Clean source definesエシュタード as交易圏 inSC0B152R50/B166R100;B164 explains the worldwide expansion. It meansPortuguese overseas trading sphere/network,not an invented city orcountry. Exact clean occurrences arebound;B77 final English wording remains to be drafted. Do not invent a formal royal appointment before the source actually grants one later.

B69 hasfive FE-presented Charlotte speeches,not narrator notices. Its pause/reaction/apology action cues include4636/051E/2000/6241/4620/632A andremain source-bound;the precise CG gesture isunconfirmed. Do not invent a kiss orother unstated action from punctuation. Use a representative original-scene/CG-transition check later. B77 explicitly acknowledges a direct loss toValdes despite Mediterranean supremacy. Preserve that branch result,not a generic naval victory. B63/B73 showprivate female identity/jealousy subtext without a declared couple. B64/B69 distinguish threatened from completed Portugal annexation. Village Romani identity,reported prejudice,investment,trade progress andapproximate dates remain explicit.

##197 drafts and77 complete comparisons

Sealed drafts:`{drafts_path}`. First77 arein`B61_B63_77_logical_English_drafts_v1.json`;the120-speech village draft is`B64_120_logical_English_drafts_v2.json`,withv1 preserved. The v2 whole-exchange reread removes one redundant double hesitation andone added optimistic assertion from a source open question. All197 drafts preceded their current-ROM extraction. Every paragraph islogical prose withruntime substitutions preserved;no authored wraps/padding. Firstfour draft gates pass;formatting remains false.

The village offer/reaction/reflection consistently useshelp you out to recreate the offense atbenefactive買ってあげる. The offended reply echoes that English phrase rather than mechanically repeatingよかったら. Keep Rafael well-intentioned,Charlotte proud/vulnerable andClaudio eventual change of heart. Romani travelers preserves ethnic identity without implying thatsettlement ended it. Theft/disease accusations areattributed prejudice. Gold/land claims remain recruiters promises;two/three-year farming andone-year barter dates remain distinct. Final dialogue isnot approved merely because a source gloss exists.

Onlyfour complete blocks61–64 (197 speeches) were selected forcurrent extraction through the unchanged own-Rafael native lookup.`{current_path}` hasexact current stored/effective text,source/current controls,commands andreferences. The other342 older-English speeches were not selected orconsulted. Do not expose all539 current lines before the remaining342 independent drafts aresaved;either finish those drafts orkeep any next extraction explicitly limited to already-drafted complete exchanges.

`{comparison_path}` contains77 individual complete-exchange decisions:40 proposed revisions/37 justified retentions. Source/current/draft were considered together. Working lines includePereira No trouble,Janus My word,the formal villager gift speech,Claudio inn invitation andmany natural short replies/apologies;each hasits own reason. Revisions correctKoon→Kuhn,the threatRemember me,missing Indochina self-boast,sourceI→currentWe errors inR63R95/R108,compressed/wrong question meaning,missing blush andlost venting advice,andunnatural phrasings. Three wording retentions atR63R113/R122/R134 still requirefour full-widthＩ→ASCII I corrections. Source-valid silent ellipsis remains intentionally retained. These areeditorial/glyph changes,not merely validation.

All77 fifth formatting gates remain false. No new pages,stored reconstruction,actual gameplay orregistered completion credit areclaimed forthe539 batch. The bound village120 still awaits current comparison;remaining342 require independent drafts andthen comparison. Keep the539-record objective intact through fresh consumer-specific wrapping/native pages,visual review,stored checks,representative CG/pagination/transition tests andregistered integration. Integrate substantial reviewed batches without replaying compatible proofs.

Totals remain10525 integrated completions,6254 revisions/4271 retentions;historicalsource/prose/draft counters10528 unchanged. The future249 once-only credit still awaits release verification. All new539 work isuncredited. Update concise progress fromthis checkpoint rather than reproducing all prior technical history.
'''
    checkpoint(mutation=ROOT/'539_source197_drafts77_comparison_checkpoint_mutation_v1',batch_key='Rafael_SC0_B61_B80_clean_20261104',
        batch_updates=dict(new_credit=0,source_meanings=539,remaining_source_meanings=0,all539_source_meanings=str(source_path),
            all539_source_meanings_sha256=sha(source_path.read_bytes()),source_identity_context=str(identity_path),source_identity_context_sha256=sha(identity_path.read_bytes()),
            source_meaning_blocks=[b for b in range(61,81) if b!=68],scoped_names=str(names_path),scoped_names_sha256=sha(names_path.read_bytes()),
            scoped_name_retentions=22,source_first_logical_drafts=197,sealed_drafts=str(drafts_path),sealed_drafts_sha256=sha(drafts_path.read_bytes()),
            remaining_independent_drafts=342,contextual_prose_comparisons=77,proposed_revisions=40,justified_retentions=37,
            comparison=str(comparison_path),comparison_sha256=sha(comparison_path.read_bytes()),proposed_fullwidth_I_glyph_corrections=4,glyph_correction_records=3,
            current_binding=str(current_path),current_binding_sha256=sha(current_path.read_bytes()),current_bound_records=197,current_bound_uncompared_records=120,
            remaining_older_English_unselected_andunconsulted=342,earlier_English_unconsulted=False,
            fresh_name_consumer_actors=12,qualified_reused_name_consumer_actors=10,source_event_contexts=20,
            all_individual_fifth_gates_pending=True,actual_gameplay_records=0,global_full_catalogue_and207_names_open=True,
            CG_gesture_andEstado_final_wording_pending=True),
        additional_updates={'Rafael_SC0_B51_B60_contextual_20261104':dict(new_credit=0,build_exec_session_id=SESSION,build_PID=PID,
            build_process_status_at_language_checkpoint=status,build_process_confirmed_live_at_language_checkpoint=live,
            latest_build_observation_UTC=observed,registered_integration_pending=True),
            'editorial_execution_priority_20261104':dict(new_credit=0,current_batch='Rafael_SC0_B51_B60_contextual_20261104',
                next_batch='Rafael_SC0_B61_B80_clean_20261104',Rafael_early_story_andall_tutorials_first=True,
                registered_cumulative_build_live=live,next_source_meanings=539,next_independent_drafts=197,next_contextual_comparisons=77,
                full_editorial_scope_preserved=True,guide_photos=False)},
        summary=summary,document=document,document_text=text,completed=10525,
        protected={'translations/release_stack.json':prepared['registry_sha256'],release['candidate']:release['candidate_sha256'],
            release['patch']:release['patch_sha256'],'out/raphael_natural_v2_accepted_base.nds':release['canonical_sha256']})
    print(f'Saved539 meanings/197 drafts/77 comparisons(40 revisions37 retentions,four I fixes);build94922 state:{state}. No new completion credit.',flush=True)
