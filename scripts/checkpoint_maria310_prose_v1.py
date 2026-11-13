"""Checkpoint310 contextual reviews without adding coverage credit or changing a ROM."""
from pathlib import Path
from collections import Counter
from scripts.audit_story_glyph_consistency import load,save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.save_editorial_progress_checkpoint_v9 import checkpoint
from scripts.meaning_maria_B51_B52_clean_v1 import ROOT

PROSE=Path('translations/maria_B51_B57_contextual_review_v1.json')

def main():
    proof=ROOT/'prose_gate_qualification_v1.json';q=load(proof);doc=load(PROSE)
    plans_path=ROOT/'plan_v1/automatic_plans.json';plans=load(plans_path)
    release_path=Path('work/maria_B50_release_v1/registered_release_verification.json');release=load(release_path)
    assert q['records']==len(doc['records'])==len(plans['records'])==310
    assert q['all_four_prose_gates_pass'] and q['all_fifth_gates_false'] and q['final_manuscript_sha256']==digest(PROSE)
    assert doc['current_ROM_sha256']==release['candidate_sha256'] and not release['own_registered_startup_pending']
    assert Counter(r['decision'] for r in doc['records'])=={'revision':184,'retention':126}
    assert all(r['review']==dict(source=True,context=True,localization=True,naturalness=True,formatting=False) for r in doc['records'])
    assert not plans['failures'] and sum(r['expected_native_pages'] for r in plans['records'])==318
    assert plans['native_pixels_visual_stored_actual_andregistered_release_pending']
    assert digest('translations/release_stack.json')==release['registry_sha256']
    paths=[PROSE,proof,ROOT/'all310_clean_meanings_andindependent_drafts_v1.json',
        ROOT/'all310_contextual_proposals_v1.json',ROOT/'contextual_proposals_qualification_v1.json',
        ROOT/'current_v1/current_effective.json',ROOT/'scoped_names_macros_reference_v1.json',
        ROOT/'scoped26_name_editorial_review_v1.json',ROOT/'scoped_terms_v1.json',
        ROOT/'formatting_v1/native_macro_measurements.json',ROOT/'formatting_v1/formatting_input.json',
        plans_path,ROOT/'plan_v1/diagnostics.json',release_path,Path(__file__)]
    evidence={str(p):digest(p) for p in paths}
    save(ROOT/'prose_and_initial_plan_checkpoint_v1.json',dict(source_objects=310,complete_exchanges=7,
        clean_meanings=310,independent_drafts=310,current_native_catalogue_bindings=310,
        contextual_comparisons=310,proposed_revisions=184,justified_retentions=126,
        scoped_name_retentions=26,original_native_name_getters=52,default_macro_cases=20,
        native_token_occurrences=9,current_nonASCII_record_targets=15,mixed_width_letter_records=2,
        mixed_width_letters=3,host_planned_pages=318,host_format_errors=0,host_format_warnings=0,
        progressive_two_page_records=[r['id'] for r in plans['records'] if r['expected_native_pages']>1],
        all_four_prose_gates_pass=True,all_formatting_gates_false=True,
        newly_generated_PNG_pages=0,new_actual_batch_gameplay_observations=0,
        stored_script_andnative_page_bounds_not_yet_approved=True,
        current_registered_candidate=release['candidate'],current_registered_candidate_sha256=release['candidate_sha256'],
        no_new_ROM_orcompletion_credit=True,new_credit=0,full_goal_complete=False,evidence=evidence))
    summary=('Maria B51–B57 now has310 complete-exchange contextual reviews:184 proposed revisions/126 justified retentions '
        'and26 scoped name retentions. Four prose gates pass;all formatting gates remain false. The initial full-width '
        'plan has318 pages withzero host errors/warnings,including eight two-page progressive records. Fifteen glyph '
        'targets include three mixed-width letters in two records. Fresh native page/glyph/visual,stored andrepresentative '
        'gameplay checks precede registration. Integrated19,748/registeredde2ffce1/main andfull scope are unchanged;zero new credit.')
    text=f'''# Maria310 contextual checkpoint — November 9, 2026

**All310 source objects in seven complete B51–B57 exchanges have contextual decisions:184 proposed revisions and126 justified retentions.** Every record has the four prose gates;every formatting gate remains false. The release validator correctly rejects the unformatted manuscript. This is editorial progress,not integrated or gameplay-tested content.

The [contextual manuscript](../translations/maria_B51_B57_contextual_review_v1.json) holds each exact clean/current reference,faithful meaning,logical paragraph,decision and specific rationale. Clean meanings were sealed before independent drafts;all drafts preceded this intake's current-English extraction. The unchanged v7 binder performs310 original catalogue lookups on the registered candidate's own Maria startup context,preserving complete commands,preambles and actor state. No blanket claim about historical screenshot exposure is made. The32 exact repeated ending utterances reuse their meaning analysis with separate source bindings;three repunctuated variants were read separately. All35 repeated contextual decisions were reviewed in the complete B54 variant and retain individual references.

Concrete proposals restore Richard's west-of-India limit and rights claim,remove unsupported Lord/Lady and This officer/This warrior substitutions,restore personal subjects and uncertainty,and preserve Maria's cultural comparison between the Proofs and the Imperial Seal. The epilogue again explicitly names the Industrial Revolution and joins its split sentences. Angelo's dream regains his navigator identity,childhood promise,flowers and Bianca's actual here-all-along line;no diagnosis or supernatural explanation is added. Emilio throws the bull,not the reverse,and Jam's surprise concerns Maria recruiting that picador,not Jam. Cristina is the woman being introduced;Maria says your grandfather rather than implying Julio is her own Grandpa. The obstacle to a woman challenging other sword schools is restored. All these remain proposals until fresh display checks pass.

Working wording is individually retained,including Richard's initial disbelief,Maria's recognition of the all-talk act,Xien's inference question and retirement joke,the seal counterexample,formal military acknowledgments,many spectator reactions and the quiet final Bianca farewell. Retentions are justified by the complete exchange,not by an old approval. All former translations,drafts and failed producers are preserved.

`scoped26_name_editorial_review_v1.json` has26 individual name/role retentions with exact source fields and52 original nameplate/catalogue getters. Maria's approved full name remains Maria Huamei Li. Julio/Cristina's real grandfather-granddaughter relationship is explicit here;other respectful or familiar addresses do not supply kinship or noble titles. Mivor's spoken surname is reconciled to native Genz,and Emilio's missing spoken Ferog is restored. Herald in Julio's parenting remark is distinct from actor16 Gerhard. Shopkeeper,Patron,Trader,Port Worker and Guildmaster remain their source-supported labels even while cheering at a bullfight. These scoped decisions do not complete the wider207-name or Cristina/Christina/older-field audits.

`scoped_terms_v1.json` records the Imperial Seal,Proofs,national defense-force review,source military titles,amaryllis,picador/matador distinction,proverb and historical narration. Nine FI/FA occurrences remain live. The registered Maria defaults FI=Maria,FA=Li,FO=Li Clan,FU=Maria Huamei Li are bound;the formatter preparation passes16 progressive/default andfour null-actor FE macro alignment cases using the unchanged original ABI and guards.

The body scope is279 progressive and31 FE records,with no menus or personality alternatives. The initial `plan_v1/automatic_plans.json` uses validated216px progressive/228px FE geometry without shortening prose,authoring ordinary breaks or changing engine/font/viewport. Its310 objects plan318 pages withzero host errors/warnings;the eight two-page cases are B51R31/R82,B53R117/R127,B54R122/R132 andB57R17/R136. **This host result is not native rendering approval.** No new PNGs have been generated or viewed yet. All generated native pages will still require direct visual review. The final source FE narrator continuations and the135-character B54R507 paragraph need native consumption/row/bounds checks;reuse the exact-source B50 continuation helper only if a concrete failure requires it. B54R515's initial four-row split is a readability lead to assess on the fresh page,not an accepted dramatic break.

Fifteen non-ASCII target records remain for fresh native checks. Twelve contain ellipses/full-width reactions;two contain actual mismatched letters:Maria B56R185 has full-width I,andJulio B57R129 has full-width I/F. B57R172 is another full-width reaction. The final proposals use ASCII consistently while preserving selectors and substitutions. These are15 targets,not15 newly confirmed glyph failures. Native font planes,complete leading/trailing characters,wrapped bounds,allocation,pagination and transitions remain to check on changed text.

Next run fresh native pages for all310 logical paragraphs,review all318 or updated pages with readable contact sheets,resolve phrase/tag/blank-row/page-boundary findings,then perform stored/native loading checks and representative FE/progressive gameplay. Include the eight two-page behaviors,inline Bianca/Angelo voice identification,ending FE transitions and the three letter fixes. The existing own31,000-frame Maria startup may be reused as compatible context;it is not new B51–B57 gameplay. No guide photos,natural late-event activation orhardware coverage is claimed.

The registered cumulative remains `{release['candidate']}`, SHA-256 `{release['candidate_sha256']}`, with712 entries/114 accepted layers/47 release checks and an exact clean-input patch. The market terminator andASCII right-bound corrections are preserved. Integrated totals remain **19,748 =11,880 revisions +7,868 retentions**;native story objects remaining stay6,150 (Lil1,805/Maria4,345),because this batch has not earned completed credit. Other shared town/shop/random/UI prose remains separately tracked. Main,canonical input,all ROMs and earlier evidence are unchanged. Full editorial scope,earlier contextual passes and all outstanding routes/prose remain active. Deferred graphics artwork and the later older-record technical re-audit remain separate. No worker is live at this checkpoint.
'''
    checkpoint(mutation=ROOT/'prose_progress_checkpoint_v1',batch_key='editorial_execution_priority_20261104',
        batch_updates=dict(new_credit=0,current_batch='Maria310:184 revisions/126 retentions;four prose gates pass;fresh native pages next.',
            new_source_meanings=310,new_independent_drafts=310,new_current_comparisons=310,
            proposed_revisions=184,justified_retentions=126,all_current_batch_five_gates_pending=False,
            all_current_batch_fifth_gates_pending=True,current_batch_not_yet_integrated=True,
            native_job_live=False,registered_build_live=False,guide_photos=False,
            next_action='Run fresh native formatting for279 progressive/31 FE bodies;directlyview every page andscoped names;stored/representative checks,thenregistered integration.'),
        additional_updates={'Maria_SC3_B51_B57_clean_20261109':dict(new_credit=0,
            clean_meanings_completed=310,source_meanings=310,independent_logical_drafts=310,independent_drafts=310,
            current_comparisons=310,remaining_current_comparisons=0,current_English_not_consulted=False,
            proposed_revisions=184,justified_retentions=126,all_five_review_gates_pending=False,
            all_four_prose_gates_pass=True,all_fifth_formatting_gates_pending=True,
            scoped_name_retentions=26,native_name_getters=52,contextual_manuscript=str(PROSE),
            contextual_manuscript_sha256=digest(PROSE),host_planned_pages=318,host_format_errors=0,host_format_warnings=0,
            glyph_targets=15,mixed_width_letter_records=2,actual_current_batch_gameplay_observations=0,
            registered_integration_pending=True,evidence=evidence)},
        summary=summary,document='docs/editorial_Maria310_contextual_20261109.md',document_text=text,
        completed=19748,protected={'translations/release_stack.json':release['registry_sha256'],
            release['canonical_base']:release['canonical_sha256'],release['candidate']:release['candidate_sha256'],
            release['manifest']:release['manifest_sha256'],release['patch']:release['patch_sha256']})
    print('Saved Maria310 contextual checkpoint;19,748 integrated unchanged;fresh native/visual checks next;zero credit.')
if __name__=='__main__':main()
