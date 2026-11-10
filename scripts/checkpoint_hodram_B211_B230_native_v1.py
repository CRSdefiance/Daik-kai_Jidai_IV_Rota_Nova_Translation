"""Save complete prose/name review and initial native visual checks, keeping wrap trials open."""
from pathlib import Path
from scripts.audit_story_glyph_consistency import load
from scripts.build_registered_rafael5186_v1 import RELEASE,REGISTRY
from scripts.finish_hodram_B211_B230_contextual_v1 import OUT as PROSE
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.prepare_hodram_B211_B230_formatting_v1 import FORMATTING,MACROS,TERMS,ROLES
from scripts.refine_hodram_B211_B230_visual_v1 import VIEW,PREFERENCES
from scripts.review_hodram_B211_B230_names_v1 import NATIVE as NAMES,OUT as NAME_REVIEW
from scripts.review_hodram_B221_B230_contextual_v1 import ROOT
from scripts.save_editorial_progress_checkpoint_v7 import checkpoint
from scripts.save_rafael3222_weekend_checkpoint_v1 import LEDGER,PACKAGE

NATIVE=ROOT/'native_resume_v2/compiled_native_pages.json'
TRIAL=ROOT/'formatting_v1/visual_trial_v3/automatic_plans.json'

def main():
    prose,native,view,names,trial,release,ledger,package=map(load,
        (PROSE,NATIVE,VIEW,NAME_REVIEW,TRIAL,RELEASE,LEDGER,PACKAGE))
    assert prose['records_count']==277 and prose['counts']=={'revision':170,'retention':107}
    assert prose['remaining_contextual_comparisons']==0 and prose['first136_decisions_exactly_preserved']
    assert len(native['records'])==270 and native['pages']==285
    assert native['fresh_compiled_alignments']==812 and native['reused_compiled_alignments']==268
    assert native['all_first_internal_final_glyph_codes_pixels_input_canaries_andbounds_pass'] and native['complete_consumption_andpagination_exact']
    assert view['all285_initial_body_pages_directly_viewed'] and view['all_initial_name_andmenu_sheets_directly_viewed']
    assert len(view['observed_layout_candidates'])==31 and len(view['sheets'])==17
    assert len(names['records'])==23 and names['name_revisions']==0
    assert len(trial['failures'])==1 and trial['failures'][0]['id']=='DK4_MES_B217_R0042'
    warnings=[(r['id'],i['code']) for r in trial['records'] for i in r['base_QA']['issues'] if i['severity']=='warning']
    assert len(warnings)==3 and len(trial['records'])==269
    assert ledger['records_editorially_completed']==17031 and not ledger['full_goal_complete']
    summary=('Hodram B211–B230 has all 277 contextual decisions complete: 170 revisions and 107 justified '
        'retentions, preserving the first 136 exactly. All 23 scoped names are retained with reasons. '
        'All 270 bodies/285 initial pages, four style objects and three menus pass native checks; every '
        'initial page and name/menu sheet was viewed. One FE punctuation wrap is fixed. Thirty-one '
        'further layout candidates remain; the first trial is not approved. Integrated coverage stays 17,031.')
    doc=f'''# Hodram B211–B230 prose, names and initial native display

{summary}

The [complete contextual manuscript](../{PROSE.as_posix()}) contains all 277 exact clean/current comparisons and individual four-prose-gate decisions. The first 136 decisions remain exactly intact. All 114 earlier independent drafts are preserved. Corrections additionally include the wholly untranslated Guan Yu reply, inconsistent Cristina/Christina and Janus/Gennas spellings, Yukihisa's signature, an added blade glow, lost retainer descent, premature item-ownership wording and a claim that no one ever found Avalon instead of the host never hearing of it. Working short questions, letter announcements, ceremonial voice and source punctuation have specific retention reasons. All formatting gates remain false.

The [23 scoped name decisions](../{NAME_REVIEW.as_posix()}) retain existing names and role labels with individual source and scene reasons. Both current original getters passed for all 23; exact clean field bytes and pointers reuse the preserved clean proofs. Progressive Sailor and catalogue Retainer remain distinct source consumers. Vivienne is spoken self-identification in a shared Alluring Woman slot; this does not rename every use of the slot. Region metadata is not a surname or new biography. No global 207-name or full catalogue UI completion is claimed.

The [current formatting inputs](../{FORMATTING.as_posix()}) preserve every reviewed word, preamble, original macro and style alias. All 18 equipment terms and two Amsterdam aliases have exact current data/pointer dependencies. Native macro execution confirms FI/FA/FO lengths 6/9/15 and the only FI-bearing speech in all four alignments. The original role-1 selector 208 resolves to the normal startup fallback Sailor; that is a display context, not new duty assignment or actual conditional participation. All 32 physical style-selection slots and 36 compiler rejection cases pass for four compiled style objects. Three menus preserve all seven caption identities, including complete Zhao Yun/Guan Yu/Zhuge Liang names, and pass their native provider, return and caption-plane checks.

Initial host planning produced 270 bodies and 285 pages with zero errors or warnings. The first native run stopped on the long B215 R17 swan call: its final exclamation moved to a second native row despite the 38-cell host plan. Glyphs were present, but row membership failed. The existing supported 36-cell FE budget for that exact record now wraps complete calls safely, with unchanged prose and physical 228px geometry. The failed run remains. Completed B211–B214 proofs were reused: 67 records/268 alignments. The remaining 203 records/812 alignments were checked freshly. The [combined native proof](../{NATIVE.as_posix()}) passes all 270 bodies, 285 pages, leading/internal/final codes and independent pixels, input guards, bounds, consumption and pagination.

All 285 initial body pages were directly inspected in 12 readable 2x contact sheets. Both name sheets and all three menu sheets were viewed. The name proof uses 13 fresh and nine exact cached native planes, qualified by the registered nine-byte metadata inverse and unchanged renderer/font/input strings; it does not claim complete ARM9 byte identity across that name stage. [Direct-view receipt and individual layout findings](../{VIEW.as_posix()}). These are offline/native checks, not B211–B230 gameplay.

The visual pass found 31 further candidates: split names and short question tags; weak opening phrases; and tails such as this news, me thinking, against it, out of that, and all and to face your fears stranded on a new page. The [bound preferences](../{PREFERENCES.as_posix()}) preserve all prose. One current page boundary is explicitly retained: B224 R68 ends a complete conditional clause before a complete invitation question. Do not shorten good prose or manufacture dramatic breaks to fit.

The first visual trial is retained as rejected evidence. It produced 269 plans, three warnings and one failed plan: the B217 R42 page-clause token must include its closing quotation mark. The three gentle letter-announcement preferences created two weak from endings and one isolated Admiral row; reject or refine those constraints. Several large page-clause constraints also make first pages sparse or leave another internal split. Some soft pair preferences leave names split. Compare each trial with its existing layout and retain the better result with a reason. The current valid initial plan/native proof remains intact; no failed trial has display or release approval. Only textually changed final plans need new native renders, followed by direct review of every new page. Do not rerun the 270 already completed initial checks wholesale.

Next resolve the 31 candidates, assemble the approved final native/visual evidence and seal the fifth gates after stored reconstruction and representative scene checks. Full catalogue UI, these conditional scenes and natural battle/tavern transitions remain unvisited. The earlier candidate-owned Hodram startup is a separate 4,001-frame ordinary route-context proof, not observation of this newly reviewed text. Registered integration, exact clean-input patch, successor-owned startup and once-only credit remain pending.

Current Rafael5186, promoted main and weekend ZIP are unchanged. All other routes, shared/shop/town/random dialogue, player-facing prose and wider name review remain in scope. Keep graphics artwork and the later older-record technical re-audit separate. No guide photographs are collected.
'''
    evidence={str(p):digest(p) for p in (PROSE,NAME_REVIEW,NAMES,NATIVE,VIEW,PREFERENCES,TRIAL,FORMATTING,MACROS,TERMS,ROLES,Path(__file__))}
    checkpoint(mutation=ROOT/'native_visual_checkpoint_v1',batch_key='Hodram_B211_B230_clean_next_20261104',
        batch_updates=dict(new_credit=0,current_English_comparisons=277,proposed_revisions=170,justified_retentions=107,
            remaining_current_English_comparisons=0,all_four_prose_gate_records=277,scoped_names_reviewed=23,
            scoped_name_revisions=0,scoped_name_retentions=23,scoped_current_name_review_pending=False,
            native_identity_andterms_still_pending=False,initial_native_body_objects=270,initial_native_pages=285,
            initial_body_pages_directly_viewed=285,initial_body_sheets_directly_viewed=12,
            name_sheets_directly_viewed=2,menu_sheets_directly_viewed=3,
            initial_FE_punctuation_wraps_corrected=1,remaining_visual_layout_candidates=31,
            first_visual_trial_approved=False,first_visual_trial_warnings=3,first_visual_trial_failed_plans=1,
            prose_comparison_anddisplay_pending=True,final_formatting_andvisual_approval_pending=True,
            current_batch_story_gameplay_utterances=0,representative_gameplay_pending=True,
            stored_reconstruction_andregistered_release_pending=True,native_job_live=False,
            native_terminal_exit_code=0,registered_build_live=False,guide_photos=False,evidence=evidence),
        additional_updates={'editorial_execution_priority_20261104':dict(new_credit=0,
            current_batch='Hodram B211–B230: all prose and scoped names reviewed; initial native pages and visual pass complete.',
            next_action='Resolve 31 layout candidates using targeted plans and fresh changed-page checks, then stored scripts and representative gameplay.',
            current_batch_not_yet_integrated=True,registered_integration_pending=True,native_job_live=False,
            registered_build_live=False,registered_cumulative_build_live=False,guide_photos=False)},
        summary=summary,document='docs/editorial_Hodram_B211_B230_native_20261107.md',document_text=doc,
        completed=17031,protected={str(REGISTRY):release['registry_sha256'],
            release['canonical_base']:release['canonical_sha256'],release['candidate']:release['candidate_sha256'],
            release['patch']:release['patch_sha256'],package['zip']:package['zip_sha256']})
    print('Saved complete prose, scoped names and all initial native/visual pages; 31 layout candidates and integration remain.')

if __name__=='__main__':main()
