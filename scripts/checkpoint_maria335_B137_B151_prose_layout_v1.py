"""Publish completed source/contextual prose and fresh plans without display or release credit."""
from pathlib import Path
from collections import Counter
from scripts.meaning_maria335_B137_B151_v1 import ROOT
from scripts.audit_story_glyph_consistency import load
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.save_editorial_progress_checkpoint_v9 import checkpoint


def main():
    prosepath=Path('translations/maria_B137_B151_contextual_review_v1.json')
    namespath=Path('translations/maria_B137_B151_scoped_names_v1.json')
    planpath=ROOT/'plan_continuity_v2/automatic_plans.json';initialpath=ROOT/'plan_initial_v1/automatic_plans.json'
    proofpath=ROOT/'prose_gates_v1.json';releasepath=Path('work/maria337_release_v1/registered_release_verification.json')
    prose,names,plan,initial,proof,release=map(load,[prosepath,namespath,planpath,initialpath,proofpath,releasepath])
    assert (prose['source_objects'],prose['complete_exchanges'],prose['proposed_revisions'],prose['justified_retentions'])==(335,15,185,150)
    assert all(r['review']==dict(source=True,context=True,localization=True,naturalness=True,formatting=False) for r in prose['records'])
    assert len(names['records'])==26 and all(r['review']==dict(source=True,context=True,localization=True,naturalness=True,formatting=False) for r in names['records'])
    assert proof['structural_projection_pass'] and proof['unformatted_manuscript_rejected_by_release_gate']
    assert len(plan['records'])==len(plan['formatter_source_bindings'])==333 and sum(r['expected_native_pages'] for r in plan['records'])==333
    assert sum(r['expected_native_pages'] for r in initial['records'])==336
    assert not plan['failures'] and not any(i['severity'] in ['warning','error'] for r in plan['records'] for i in r['base_QA']['issues'])
    assert all(r['all_words_punctuation_and_source_macros_unchanged'] for r in plan['records'])
    v1=load(ROOT/'plan_continuity_v1/automatic_plans.json')
    assert [(r['id'],r['encoded_hex']) for r in v1['records']]==[(r['id'],r['encoded_hex']) for r in plan['records']]
    assert (release['registered_manifest_entries'],release['accepted_layers'],release['passing_release_checks'])==(717,114,52)
    assert digest('translations/release_stack.json')==release['registry_sha256'] and not release['own_registered_startup_pending']
    paths=[prosepath,namespath,proofpath,planpath,initialpath,releasepath,ROOT/'source_selection_v1.json',ROOT/'clean_source_packet.json',
        ROOT/'all335_clean_meanings_v1.json',ROOT/'all335_independent_drafts_v3.json',ROOT/'all335_contextual_proposals_v1.json',
        ROOT/'current_inputs_v1/sealed_drafts.json',ROOT/'current_inputs_v1/projection.json',ROOT/'current_v1/current_effective.json',
        ROOT/'current_objects_v1/current_objects.json',ROOT/'scoped_names_macros_reference_v1.json',ROOT/'scoped_terms_reference_v1.json',
        ROOT/'formatting_v1/formatting_input.json',ROOT/'formatting_v1/native_macro_measurements.json',ROOT/'formatting_v1/role_bindings.json',
        ROOT/'continuity_findings_v1.json',ROOT/'continuity_findings_v2.json',ROOT/'continuity_preferences_v2.json',Path(__file__)]
    evidence={str(p):digest(p) for p in paths}
    summary=('Maria B137–B151 has335 contextual reviews:185 revisions/150 justified retentions across15 complete exchanges and26 scoped name reviews. '
        'All first four individual gates pass; fifth gates remain pending. A full-width plan fits333 bodies on333 pages with no warnings/failures, '
        'removing three premature pages in the plan without shortening prose. Full-width I,corrupt refusal,lone Y,Sir-to-Maria,brotherhood, '
        'first-person speech andtutorial UI terms are corrected in selected prose. Bread teaching andprospective commodity forecasts retain their source meaning. '
        'Fresh native/visual/caption/name/storage/gameplay/release checks remain. No worker is live;registered9913f13e,integrated21,356,main andfull scope are unchanged.')
    text=f'''# Maria335 B137–B151 prose and layout — November 9, 2026

**335 original objects now have complete-exchange contextual decisions:185 revisions and150 justified retentions.** All first four individual gates pass. There are26 scoped name/role reviews and30 distinct current name strings. All fifth formatting gates remain false; no new native previews, gameplay, ROM or completion credit is claimed. The registered [Maria337 candidate](editorial_Maria337_registered_20261109.md), integrated21,356 and the full objective remain unchanged.

Work root: `work/Maria_B137_B151_clean_20261109`. Scope:all15 complete clean SC3 blocks137–151,333 ordinary speech commands (315 progressive/18 FE) andtwo captions in one0x2100 menu. There are no style objects or dynamic selectors. `source_selection_v1.json` verifies every original source reference, complete block and disjointness from earlier credit. All335 meanings were saved before the independent drafts; both preceded current-English extraction. The initial macro-order failure and the data-as-Python derivation failure are preserved; `all335_independent_drafts_v3.json` is the successful sealed draft. All source/current/proposal/final references remain exact.

Final selected prose is `translations/maria_B137_B151_contextual_review_v1.json`; scoped names are `translations/maria_B137_B151_scoped_names_v1.json`. `all335_contextual_proposals_v1.json` preserves184 revisions/151 retentions. Twelve final name/term amendments change that to185/150:the otherwise good crown-admiration retention needed the registered Silla Gold Crown spelling. Six provisional Sang Hyeon mentions become Sanghyeon;five tutorial paragraphs use exact installed terms. Always select `proposed_English` or final `english`, not an independently preserved draft. `prose_gates_v1.json` proves the first four gates and correct rejection by the v2 release validator while formatting is unfinished.

**Actual source and prose errors:** Julio B137R46 has a full-width I. B138s refusal caption is corrupted as `丑o`; use `No, thanks.` at the same source index, paired with `Please do.`. B148R12 is only `Y`, replacing the affirmative 然り; selected prose is `Indeed.`. B141 addresses Maria as Sir and repeatedly makes a senior fellow disciple sound like a biological brother. Preserve the explicit childhood comparison as close as brother and sister, the school expulsion and national travel ban, while attributing the dream/magical-visit accounts to their respective speakers. B146 shortens Yukihisa to unsupported Yuki. Restore first-person agency where earlier text says This man/This woman or uses impersonal notes. All12 non-ASCII current prose/caption targets have ASCII proposed text; this is not yet native font approval.

Review whole emotional and comic progressions. Julios age rivalry uses old hand/old man without inventing retirement or kinship. Manuel loves ships but declines to discuss his past; Maria respects that. Mikhails pepper/rabbit-dropping reversal, intrusive boast and unwelcome familiarity remain in character; the women are not his grandchildren and no exact physical act is added. His Western-custom defense is his claim, not narration. The pirate princess address is a taunt, not Marias rank, and the sword target stays unexplained. Yifas apparent spell and real martial skill remain distinct. Julians hoped-for date is not consent: Mihwa agrees only to consider it. The grandfather in his own recruitment really is family. Maria offers Yukihisa an independent fleet command rather than already executing an assignment or sending him physically alone.

**The bread exchange is cooking instruction.** Retain the already-natural home-baked bread, the one speakers explicitly supported husband, bakery comparison and ingredient shopping. Replace `Let me teach.` with `I'll show you how.` in that context, not trading advice. Keep Wheat, not flour, and the prospective Amsterdam popularity notice. The banana/Seville and tomato/Genoa notices are also prospective popularity, not current shortages or guaranteed profits. Arab/tavern observations remain characters culturally situated speech, without invented universal historical claims.

`scoped_names_macros_reference_v1.json` binds26 actors/52 original short/full getters and all four default macros. Current proper-name forms, Lady/Woman/Owner/Cook, the Angel/Snake/Dandy nicknames and the qualified Sailor/Retainer distinction have individual reasons in the name review. Unused regional metadata is not a player name; no global207-name approval is claimed. The FE pirate remains unidentified and receives no invented static nameplate.

`scoped_terms_reference_v1.json` binds eight actual room aliases and their complete installed Help articles111–117/121, the active Speech skill, Silla Gold Crown, Tomb of King Muryeong, Seoul and three commodities. Use First Mate's Office, Chapel, Galley, Nursery, Sickbay, Private Cabin, Recreation Room and Lumber Room; short native aliases and explanatory expansions are both documented. Use Surgeon and Shipwright consistently with the reviewed Help. The source tutorial benefits are retained rather than rewritten from different Help articles. The whole Help archive is not claimed unchanged. Banana/tomato suffixes inside longer item names were not standalone referenced commodity names;the exact unique referenced pointers were bound. The installed Tomato label is singular, while ordinary plural tomatoes in a sentence remains grammatical. Prior failed reference producers are preserved; v3 succeeds. This is reference evidence, not new widget gameplay or font approval.

**Fresh automatic plans:** `formatting_v1/formatting_input.json` marks21 real macro occurrences explicitly and authors no ordinary line breaks. Twenty prior default macro cases are reused only after complete ARM9/COMMON/font, actor root/model bytes, original captain3 getter and all four default strings match. Per-record fresh native expansion/phase/glyph checks are still required. The explicit empty role proof does not pretend to execute empty permutations.

Selected plan: `plan_continuity_v2/automatic_plans.json`, with `continuity_preferences_v2.json`. All333 bodies/333 pages pass full source/current controls, byte/width/phase/word/macro and warning checks. Initial `plan_initial_v1` had336 pages. Three129/131/110-character paragraphs B141R43/B146R56/B148R8 now fit one page each at the unchanged validated216-pixel width; no words are shortened. The original plans stranded was worse still, and look properly and command respect on extra pages. Both trial versions have identical compiled bytes;v2 only corrects earlier explanatory character counts. These three reclaimed pages are planned, not yet proven native/observed. All18 FE bodies retain the validated228-pixel consumer. Every newly rendered page still needs readable contact-sheet review, with phrase continuity reassessed visually.

**Next run journaled fresh native checks for all333 bodies and view every generated page.** Prioritize the three one-page trials, Julios corrected I, the lone-Y repair, Mikhail tutorials, long FE pirate panels and ordinary named returns, bread/trend prose and all tutorial room/stat words. Compile/provider-test both B138C1274 captions. Its known corrupt old `丑o` cannot be sent to the generic ASCII baseline font comparator:use an exact scoped corrupt-provider binding, retain valid baseline checks and disclose any unapproved old font rendering. Do not repeat the known Unicode failure merely to rediscover it. All four reviewed target normal/highlight planes still require approval. Then verify names, complete script reconstruction/storage/branches/allocation and representative actual gameplay/transitions before registered integration. No exhaustive conditional playthrough or guide photos.

Registered parent: `work/maria337_release_v1/all_routes_maria337_candidate.nds`, SHA-256 `{release['candidate_sha256']}`,717 entries/114 accepted layers/52 checks. Preserve Market allocation/pointers,six-section ARM9,ASCII right bounds,source25 v2 guard,names,fonts,graphics andall earlier amendments. Integrated totals stay21,356 =12,861 revisions+8,495 retentions; historical source/prose/draft counts stay21,359. Native story remainder stays4542 (Lil1805/Maria2737), including this unintegrated335. Shared town/shop/random/player-facing prose and earlier unfinished contextual passes remain in scope. Keep early Rafael/tutorial priority, deferred graphics artwork and the later older-record technical re-audit separate. Main promotion requires acceptance. No cleanup,promotion,commit orpush; no worker is live.
'''
    checkpoint(mutation=ROOT/'prose_layout_progress_checkpoint_v1',batch_key='editorial_execution_priority_20261104',
        batch_updates=dict(new_credit=0,current_batch='Maria335 B137–B151:185 revisions/150 retentions;26 names;four gates and333-body/333-page plans pass.',
            current_batch_not_yet_integrated=True,current_batch_registered_andcredited_once=False,all_current_batch_fifth_gates_pending=True,
            proposed_revisions=185,justified_retentions=150,native_job_live=False,native_sessions=[],registered_build_live=False,
            registered_cumulative_build_live=False,guide_photos=False,current_batch_evidence=evidence,
            next_action='Fresh journaled333-body native checks;review all333 pages,two captions and30 name strings,then storage/representative gameplay/registered integration.'),
        additional_updates={'Maria_SC3_B137_B151_clean_20261109':dict(new_credit=0,proposed_revisions=185,justified_retentions=150,
            clean_meanings_andindependent_drafts_pending=False,current_English_not_read=False,first_four_individual_prose_gates_pass=True,
            all_five_review_gates_pending=False,all_individual_fifth_gates_still_pending=True,scoped_name_retentions=26,
            source_FE_panels=18,style_objects=0,dynamic_source_selectors=[],planned_native_body_pages=333,
            planned_pages_reclaimed=3,native_pixels_andvisual_checks_pending=True,stored_andrepresentative_gameplay_pending=True,
            registered_integration_pending=True,full_goal_complete=False,evidence=evidence)},
        summary=summary,document='docs/editorial_Maria335_B137_B151_prose_layout_20261109.md',document_text=text,completed=21356,
        protected={'translations/release_stack.json':release['registry_sha256'],release['candidate']:release['candidate_sha256'],
            release['manifest']:release['manifest_sha256'],release['patch']:release['patch_sha256'],release['canonical_base']:release['canonical_sha256']})
    print('Saved335 contextual prose/26 names/333-page plan checkpoint;native/visual/release gates pending;registered Maria337 and21,356 credit unchanged.')


if __name__=='__main__':main()
