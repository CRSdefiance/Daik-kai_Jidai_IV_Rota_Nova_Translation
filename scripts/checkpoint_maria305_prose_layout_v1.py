"""Publish exact uncredited Maria305 prose/layout progress without changing a release."""
from pathlib import Path
from collections import Counter
from scripts.audit_story_glyph_consistency import load,save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.save_editorial_progress_checkpoint_v10 import checkpoint

ROOT=Path('work/Maria_B176_B195_clean_20261110')


def main():
    rp=Path('work/maria390_B152_B175_release_v1/registered_release_verification.json');release=load(rp)
    manuscript=Path('translations/maria_B176_B195_contextual_review_v1.json');doc=load(manuscript)
    planpath=ROOT/'plan_v5/automatic_plans.json';plans=load(planpath);initial=load(ROOT/'plan_v1/automatic_plans.json')
    namespath=Path('translations/maria_B176_B195_scoped_names_v1.json');names=load(namespath)
    assert len(doc['records'])==305 and doc['complete_exchanges']==19 and (doc['proposed_revisions'],doc['justified_retentions'])==(205,100)
    assert all(r['review']==dict(source=True,context=True,localization=True,naturalness=True,formatting=False) for r in doc['records'])
    assert len(plans['records'])==294 and not plans['failures'] and len(names['records'])==27
    assert not any(i['severity'] in ['error','warning'] for r in plans['records'] for i in r['base_QA']['issues'])
    assert sum(r['expected_native_pages'] for r in plans['records'])==302
    old={r['id']:r for r in initial['records']};changed=[r['id'] for r in plans['records'] if r['lines']!=old[r['id']]['lines']]
    assert len(changed)==7
    issues=Counter(i['severity'] for r in plans['records'] for i in r['base_QA']['issues'])
    evidencepaths=[rp,manuscript,namespath,planpath,*[ROOT/n for n in ['source_selection_v1.json','all305_clean_meanings_v2.json',
        'all305_independent_drafts_v2.json','clean_actor_context_amendment_v1.json','contextual_comparisons_v1.json',
        'scoped_names_macros_reference_v1.json','scoped_names_reference_v2.json','scoped_terms_reference_v1.json',
        'dynamic_roles_current_v1.json','prose_gates_v1.json','current_v1/current_effective.json',
        'current_objects_v1/current_objects.json','formatting_v1/formatting_input.json','formatting_v1/page_preferences_v6.json']],Path(__file__)]
    evidence={str(p):digest(p) for p in evidencepaths}
    summary=('Maria B176–B195 now has305 contextual reviews across19 complete exchanges:205 proposed revisions/100 justified retentions and27 scoped name reviews. '
        'All four individual prose gates pass;all fifth gates remain pending. Fresh full-width plans cover294 bodies/302 pages plus11 captions,with zero errors/warnings/failures. '
        'Seven page/phrase layouts are refined andone complete-question boundary is narrowly retained;native pixels andvisual approval are unrun. '
        'Self-reference,parrot echoes,one Japanese reply,mixed-width glyphs,letter signatures,clue facts anditem titles are corrected in proposed prose. '
        'No new ROM orcompletion credit;integrated22,081,registered48c60d68,main andfull scope are unchanged. No batch worker is live.')
    document='docs/editorial_Maria305_B176_B195_prose_layout_20261110.md'
    text=f'''# Maria305 B176–B195 prose/layout checkpoint — November 10, 2026

{summary}

The previous goal turn made progress:Maria390 registration was verified,390 records were credited once,censusv11 was reconciled andthe registered checkpoint was published. This turn selects305 disjoint exact clean objects in19 complete native exchanges:blocks176–191 and193–195. Block192 was already covered andis not repeated. The source/current/source-prose references andindividual decisions are in `{manuscript}`. Completed coverage remains22,081 =13,200 revisions+8,881 retentions. Native story remainder3,817 includes all305 unintegrated objects:Maria2,012/Lil1,805;separate shared/player-facing inventories remain open.

The clean meanings were sealed before independent English,then current English was extracted. Preserve both original drafts andthe qualified context amendment:clean actor metadata identifies Mikhail76 in the medicine scene,Angelo15 in the parrot scene,andEmilio14 in the weapon request. The three initial provisional attributions were wrong;version2 corrects the contexts andmeaning attributions before any current-English reading orprose-gate approval. The English drafts remain byte-identical. Current extraction/control/alias bindings are exact andnot falsely credited asfresh editorial approval.

Concrete findings include Emilio andJulian referring to themselves as this man,mismatched parrot echoes,one still-Japanese Guan Yu response,full-width reaction glyphs andtwo full-width I characters,missing gold-seal/retainer ancestry details,a missing Iceland guess,unsupported certainty,personal ignorance broadened to universal ignorance,andletter signatures Ludwayer/Pasha inconsistent with native Ludwyan/Pasar. The final Janus Pasar,Jam Jack Ludwyan andYukihisa Genjo Shiraki signatures match the native full consumers. Natural first-person speech,source-specific quantities/directions andthe conditional treasure leads are preserved. The 205 selected revisions include editorial improvements;they are not205 independent technical bugs.

All305 records have individual findings andsource/context/localization/naturalness gates. The100 retentions have specific reasons,including clear questions/replies,conditional reports,existing natural humor andfunctional one-point Charm notices. Item binding reopens two proposed retentions:Minotaur Axe andthe repeated Empress Gown title. Holy Spear of Ares also uses its installed title. Nine exact item pointer/string references do not license adding Red-Haired Pirate Sword orJudas' Demonblade names where the source only says a generic sword. The medicinal book remains unnamed in dialogue. No rank,kinship,romance,guaranteed profit,confirmed legendary event orfound treasure is invented.

Scoped names27/54 getters are qualified:52 original getter bindings plus two for the newly resolved startup fallback actor156. Retain the actual Sailor nameplate/Retainer catalogue distinction. Three original4100 style objects have22 distinct physical alternatives/24 aliased slots;all24 source/current native getters pass. Eleven captions occupyfive native two/three-choice objects. Role208 is proved by the original dispatcher with207 asan explicit captain control. Startup fallback156/voice4 is not a new scene roster orvisit. The first role-wrapper attempt lacked the original207 control andstopped;v2 includes that control without removing the assertion. No role oractor assignment is altered.

Formatting input:`formatting_v1/formatting_input.json`;current selected plan:`plan_v5/automatic_plans.json`;preferences:`formatting_v1/page_preferences_v6.json`. All294 bodies have complete clean/current control bindings,unchanged paragraphs andfour exact FI/FA occurrences. The existing20 default macro proofs are reused only after complete ARM9,COMMON,font,actor model/root andnative captain dependencies match. No new ordinary line breaks are authored. Native widths stay216px progressive/228px FE. The plan has302 pages,zero errors/warnings/failures and{issues.get('info',0)} informational findings. This is a plan,not a glyph/pixel/storage orgameplay pass.

Seven layouts change fromthe first plan:the earrings' condition/result,Zhuge Liang andfavorite comment,the complete sword-giving imperative,repeated persecution,the short question tag,the humane-conduct closing thought,andthe Noritsune armor complement. Early overconstraints made pages unnecessarily sparse;those rejected/intermediate preferences andallfailed attempts remain preserved. The Muramasa whole-clause constraint proved impossible andwas removed in favor of small descriptor/name pairs. Its original six-line layout remains;do not claim an eighth fix. Every selected native page still needs readable visual review,including sparse rows andpage boundaries. Further refinement may be needed after observing native rows.

One narrow grammatical retention is bound to exact B191R31 source/current/prose,the exactfirst line andits only weak-ending warning:Admiral? What's that look for? The final for? completes a grammatical question. Versioned `plan_scoped_clean_editorial_v2.py` keeps the original planner contracts,permits only that exact new case alongside the two historical owners,anddoes not waive native leading/trailing glyphs,bounds,allocation,pagination orstored bytes. Changed prose cannot inherit it. The overall fifth gate stays false.

**Next:**run the calibrated native-page checks onthis exact294-body plan using the compatible macro/role proofs;review every new page onreadable contact sheets andrepair actual row/phrase/page findings. Then checkthe22 style alternatives/11 captions/27 scoped names,the complete source/current/stored block/branch/allocation/loader inverses,andrepresentative gameplay for letters,parrot FE echoes,menu branching,pagination andreturns. Integrate only after necessary checks pass through the current registered cumulative workflow. No new batch gameplay,conditional activation,hardware coverage orrelease is claimed. All jobs started this turn are terminal;no native render worker has been launched.

The registered testing parent remains[Maria390](../work/maria390_B152_B175_release_v1/all_routes_maria390_B152_B175_candidate.nds),SHA256 `{release['candidate_sha256']}`,719 entries/114accepted layers/54checks. Its exact clean-input patch,Market Goods Info correction,ASCII right bounds,all prior translations,fonts andgraphics remain preserved. The user's older Rafael2952 build contains the known Market suffix defect;the registered parent has the fix. The earlier chat ROM link had a path typo;the local file underthis actual project directory exists andits hash is verified. Main `all-routes-unified-v4701` is unchanged;acceptance remains required forpromotion.

Keep thefull editorial goal active:allfour storylines,earlier unfinished contextual passes,shared town/shop/random/player prose,speaker labels,natural dialogue,wrapping andglyph consistency. Early Rafael/tutorial priority remains;no guide photos. Preserve every ROM,translation,producer,draft,proof andfailure. Deferred graphics artwork andthe later older-record technical re-audit remain separate.
'''
    checkpoint(mutation=ROOT/'prose_layout_checkpoint_v1',batch_key='editorial_execution_priority_20261104',
        batch_updates=dict(new_credit=0,current_batch='Maria305 B176–B195:four prose gates andfull-width plans complete;native/visual/storage/gameplay/release pending.',
            current_batch_not_yet_integrated=True,current_batch_registered_andcredited_once=False,
            proposed_revisions=205,justified_retentions=100,all_current_batch_fifth_gates_pending=True,
            native_job_live=False,native_sessions=[],stored_job_live=False,registered_build_live=False,
            current_batch_evidence=evidence,next_action='Native checkandvisually reviewall294 bodies/302 planned pages;thenstyles/captions/names/storage/gameplay/registration.',guide_photos=False),
        new_entries={'Maria_SC3_B176_B195_clean_20261110':dict(new_credit=0,source_objects=305,complete_exchanges=19,
            ordinary_speeches=272,physical_style_alternatives=22,typed_captions=11,clean_meanings=305,independent_drafts=305,
            individual_contextual_comparisons=305,proposed_revisions=205,justified_retentions=100,scoped_name_reviews=27,
            first_four_individual_prose_gates_pass=True,all_fifth_gates_pending=True,planned_body_pages=302,
            native_pages_visually_reviewed=0,actual_batch_gameplay_records=0,registered_integration_pending=True,evidence=evidence,full_goal_complete=False)},
        summary=summary,document=document,document_text=text,completed=22081,
        protected={'translations/release_stack.json':release['registry_sha256'],release['candidate']:release['candidate_sha256'],
            release['manifest']:release['manifest_sha256'],release['patch']:release['patch_sha256'],release['canonical_base']:release['canonical_sha256']})
    save(ROOT/'current_checkpoint.json',dict(document=document,source_objects=305,revisions=205,retentions=100,source_bound_layouts=294,
        planned_pages=302,changed_layouts=changed,first_four_gates_pass=True,all_fifth_gates_pending=True,
        no_batch_worker_live=True,no_new_ROM_orcompletion_credit=True,full_goal_complete=False,evidence=evidence))
    print('Published Maria305:205 revisions/100 retentions,four prose gates,302 planned pages;integrated22081/main unchanged.')


if __name__=='__main__':main()
