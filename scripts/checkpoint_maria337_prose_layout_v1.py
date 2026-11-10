"""Save completed contextual prose and passing plans without adding release credit."""
from pathlib import Path
from scripts.meaning_maria337_clean_v1 import ROOT
from scripts.audit_story_glyph_consistency import load
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.save_editorial_progress_checkpoint_v9 import checkpoint

def main():
    prosepath=Path('translations/maria_B125_B136_contextual_review_v1.json')
    namespath=Path('translations/maria_B125_B136_scoped_names_v1.json')
    proofpath=ROOT/'prose_gates_v1.json'; planpath=ROOT/'plan_continuity_v2/automatic_plans.json'
    releasepath=Path('work/maria330_release_v1/registered_release_verification.json')
    prose,names,proof,plan,release=map(load,[prosepath,namespath,proofpath,planpath,releasepath])
    assert (prose['source_objects'],prose['complete_exchanges'],prose['proposed_revisions'],prose['justified_retentions'])==(337,12,224,113)
    assert all(r['review']==dict(source=True,context=True,localization=True,naturalness=True,formatting=False) for r in prose['records'])
    assert len(names['records'])==21 and all(r['review']==dict(source=True,context=True,localization=True,naturalness=True,formatting=False) for r in names['records'])
    assert proof['structural_projection_pass'] and proof['unformatted_manuscript_rejected_by_release_gate']
    assert len(plan['records'])==len(plan['formatter_source_bindings'])==335 and sum(r['expected_native_pages'] for r in plan['records'])==339
    assert not plan['failures'] and not any(i['severity'] in ['warning','error'] for r in plan['records'] for i in r['base_QA']['issues'])
    assert all(r['all_words_punctuation_and_source_macros_unchanged'] for r in plan['records'])
    assert digest(plan['manuscript'])==plan['manuscript_sha256'] and digest(prosepath)==proof['manuscript_sha256']
    trialpath=ROOT/'plan_continuity_v3_onepage_trial/automatic_plans.json'; trial=load(trialpath)
    row=next(r for r in trial['records'] if r['id']=='DK4_MES_B135_R0335')
    assert row['expected_native_pages']==1 and any(i['severity']=='warning' and i['code']=='weak-line-ending' for i in row['base_QA']['issues'])
    assert (release['registered_manifest_entries'],release['accepted_layers'],release['passing_release_checks'])==(716,114,51)
    assert digest('translations/release_stack.json')==release['registry_sha256'] and not release['own_registered_startup_pending']
    paths=[prosepath,namespath,proofpath,planpath,releasepath,ROOT/'clean_source_packet.json',ROOT/'source_selection_v1.json',
        ROOT/'all337_clean_meanings_v1.json',ROOT/'all337_independent_drafts_v1.json',ROOT/'all337_contextual_proposals_v1.json',
        ROOT/'current_inputs_v1/sealed_drafts.json',ROOT/'current_v1/current_effective.json',ROOT/'current_objects_v1/current_objects.json',
        ROOT/'scoped_names_macros_reference_v1.json',ROOT/'scoped_terms_reference_v1.json',ROOT/'formatting_v1/formatting_input.json',
        ROOT/'formatting_v1/native_macro_measurements.json',ROOT/'formatting_v1/role_bindings.json',ROOT/'continuity_preferences_v2.json',
        ROOT/'continuity_findings_v2.json',ROOT/'plan_initial_v1/automatic_plans.json',ROOT/'plan_continuity_v1/automatic_plans.json',trialpath,Path(__file__)]
    evidence={str(p):digest(p) for p in paths}
    summary=('Maria337 has 337 contextual prose reviews across 12 complete exchanges: 224 revisions/113 justified retentions and 21 scoped name reviews. '
        'The first four individual gates pass; all fifth gates remain pending. Two corrupted gambling captions, two full-width-I lines, '
        'Carlo/Cesare body-name inconsistencies, the missing Fernando introduction and unsupported sir are corrected in the selected prose. '
        'Fresh plans cover 335 bodies/339 pages with no warnings or failures; four tutorial page boundaries improve without shortening words. '
        'Native/visual/menu/name/storage/gameplay/release checks remain. No worker is live; registered 2ea13d92, integrated 21,019, main and the full objective are unchanged.')
    text=f'''# Maria337 prose and layout checkpoint — November 9, 2026

**337 records in 12 complete SC3 exchanges now have contextual decisions: 224 revisions and 113 justified retentions.** The first four individual gates pass, with 21 scoped name/role retentions. All fifth formatting gates remain false. No native previews, new gameplay, ROM integration or completion credit are claimed for this batch. Registered Maria330 and integrated 21,019 remain unchanged.

Work root: `work/Maria_B125_B136_clean_20261109`. Scope is all objects in blocks125–136: 335 ordinary source speech commands (329 progressive and six FE panels) and two captions in one two-choice menu. There are no 4100 style objects or dynamic role selectors. `source_selection_v1.json` verifies all source positions and disjoint completed keys using the existing SC3_v8 inventory. Clean Japanese was read in complete exchanges. `all337_clean_meanings_v1.json` was sealed before `all337_independent_drafts_v1.json`; both preceded current-English extraction. All exact bytes, references and independent drafts remain preserved.

Final prose: `translations/maria_B125_B136_contextual_review_v1.json`. Names: `translations/maria_B125_B136_scoped_names_v1.json`. `prose_gates_v1.json` proves four individual gates, the structural check and the release validator correctly refusing the unfinished fifth gate. `all337_contextual_proposals_v1.json` retains the original 222 revision/115 retention decisions; nine final name/term/read-aloud amendments change that to 224/113. Always select `proposed_English` when deriving final prose, not the independently preserved draft.

**Editorial findings include real errors.** Both gambling captions are corrupted (`産es` and `札ecline`); the replacements express acceptance/refusal and preserve their source indices. Two story lines contain mixed full-width Latin I characters. The old Carlo Sinato and Cesare Tohni introductions disagree with current name consumers Carlo Sinat and Cesare Tony; final prose matches those consumers. Fernando's full self-introduction replaces the repeated Dias. Cesare no longer addresses Maria as unsupported sir or refers to himself as This man. Personal agency, fever, timing, reported-information uncertainty, figurative family bonds, dance context and comic cause/effect are restored where compressed English obscured them.

Review each recruit's whole emotional progression. Angelo's sister is explicitly missing in the earlier scene's belief and explicitly died three years ago in the later confession. His reported fever encounter remains unexplained, with the final private thought in parentheses. Carlo's daughter and wife died a year ago; retain responsibility and grief without inventing a diagnosis or completed treatment. Maria offers a new family, not erasure of the old one. Adil remains a scene name for the shared Trader; the innkeeper is not globally renamed Wife. The dating couple retain Man/Woman, without marriage or age assumptions. B133/B134 preserve a neutral absent referent and apparently/not-yet nuance rather than inventing identity.

`scoped_names_macros_reference_v1.json` binds 21 actors/42 current getters and four default substitutions. The already-qualified Sailor/Retainer distinction for153 is retained, not replaced from unused metadata. `scoped_terms_reference_v1.json` binds Ceremonial Knife and Sun-Crest Sheath to source/current item fields; three complete installed Help articles59/66/83 are byte-exact at their current table offsets. The whole HELP archive is explicitly not claimed unchanged. Use Quarters, Batteries, Cargo, Supplies, Sail Handler and regional fleet consistently. The full Proof of Conquest term reuses its exact unchanged registered B53 anchor and compatible native lookup proof. No new global207-name, catalogue UI, font or gameplay approval is implied.

**Fresh formatting is planned for every body.** `formatting_v1/formatting_input.json` marks 13 source macro occurrences explicitly (FI5/FA5/FO3) and adds no authored ordinary line breaks. `native_macro_measurements.json` rebinds the 20 completed default measurement cases after whole ARM9, COMMON, font, complete actor-model block, actor root, native captain getter and all default strings match. Those default measurements were not rerun; every new paragraph still requires fresh native display checks. `role_bindings.json` proves this scope has no dynamic selectors and does not pretend to run empty role permutations.

Selected plan: `plan_continuity_v2/automatic_plans.json`, using `continuity_preferences_v2.json` and `scripts/plan_maria337_v1.py`. All335 source/current body bindings and339 planned pages pass byte/width/phase/word/macro checks, with zero warnings, errors or failures. Four tutorial records remain two pages: B135R325/R335/R351/R366. Their quantity rule, unfillable-cargo consequence, equipment recommendation and ship-retention recommendation stay together. The remaining text uses the validated216/228-pixel widths. No prose is shortened. Source-specific shorter setup rows are documented where necessary to avoid stranded objects or lists.

The initial plan split one/to-five, stranded its hold, separated the Batteries list and split old/medium ships across A. The first clause trial omitted punctuation from two word-matching targets and stopped with333 results; it remains preserved. The successful v2 targets use complete exact phrases and retain useful setup content on page1. A fresh full-width one-page trial for the only paragraph below144 raw characters, B135R335, produced a weak-line-ending warning after to. Do not waive it or adopt that338-page trial. Keep the selected339-page zero-warning plan until native/visual evidence supports a change. These are formatted-line findings, not viewed native screenshots or proven gameplay fixes.

**Next run fresh journaled native checks for all335 bodies and review all339 generated pages on readable contact sheets.** Check the four tutorial page turns, both family-loss FE panels, inline patron/applause labels, controls, substitutions and all leading/internal/trailing glyphs. Use the qualified two-choice compiler/provider for the two repaired captions, and exact compatible name-plane proofs where available. Then perform whole-script reconstruction, storage/allocation/relative checks and representative gameplay for the distinct behaviors and returns. No exhaustive conditional playthrough or guide photos are required. Integrate through the registered cumulative workflow once necessary checks pass; main promotion requires acceptance.

Current registered [Maria330](editorial_Maria330_registered_20261109.md) is `work/maria330_release_v1/all_routes_maria330_candidate.nds`, SHA-256 `{release['candidate_sha256']}`, with716 entries/114 accepted layers/51 checks. Preserve its Market allocation/pointers, six-section ARM9, ASCII right-bound correction, v2 source25 guard, names, fonts, graphics and all earlier amendments. Integrated totals stay21,019 =12,637 revisions +8,382 retentions; historical source/prose/draft counts stay21,022. Remaining native story objects stay4,879 (Lil1,805/Maria3,074), including this unintegrated batch. All earlier unfinished contextual passes, shared shop/town/random exchanges, names/roles and remaining prose stay in scope, with early Rafael/tutorial priority preserved. Deferred graphics artwork and the later older-record technical re-audit remain separate. All generated ROMs, translations, drafts and proofs are preserved. No worker is live; no promotion, cleanup, commit or push occurred.
'''
    checkpoint(mutation=ROOT/'prose_layout_progress_checkpoint_v1',batch_key='editorial_execution_priority_20261104',
        batch_updates=dict(new_credit=0,current_batch='Maria337:224 revisions/113 retentions;21 names;four prose gates and335-body/339-page plans pass.',
            current_batch_not_yet_integrated=True,current_batch_registered_andcredited_once=False,all_current_batch_fifth_gates_pending=True,
            proposed_revisions=224,justified_retentions=113,native_job_live=False,native_sessions=[],registered_build_live=False,registered_cumulative_build_live=False,
            guide_photos=False,current_batch_evidence=evidence,next_action='Render335 bodies/339 pages with journals; review all pages, two captions and names, then storage/gameplay andregistered integration.'),
        new_entries={'Maria_SC3_B125_B136_clean_20261109':dict(new_credit=0,source_objects=337,complete_exchanges=12,proposed_revisions=224,justified_retentions=113,
            first_four_individual_prose_gates_pass=True,all_individual_fifth_gates_still_pending=True,scoped_name_retentions=21,
            source_speech_objects=335,source_FE_panels=6,typed_choice_labels=2,typed_choice_objects=1,style_objects=0,dynamic_source_selectors=[],
            planned_native_body_pages=339,native_pixels_andvisual_checks_pending=True,stored_andrepresentative_gameplay_pending=True,
            registered_integration_pending=True,full_goal_complete=False,evidence=evidence)},
        summary=summary,document='docs/editorial_Maria337_prose_layout_20261109.md',document_text=text,completed=21019,
        protected={'translations/release_stack.json':release['registry_sha256'],release['candidate']:release['candidate_sha256'],release['manifest']:release['manifest_sha256'],
            release['patch']:release['patch_sha256'],release['canonical_base']:release['canonical_sha256']})
    print('Saved337 prose/layout checkpoint; integrated21,019 andregistered Maria330 remain unchanged;fresh native/visual work is next.')

if __name__=='__main__':main()
