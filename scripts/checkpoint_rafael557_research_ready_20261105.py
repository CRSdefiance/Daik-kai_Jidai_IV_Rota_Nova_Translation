"""Record completed research gates, corrected runtime punctuation and no integration credit."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load
from scripts.save_editorial_progress_checkpoint_v5 import checkpoint

A=Path('work/analysis')
ROOT=A/'Rafael557_research_final_v1_20261105'
READY=ROOT/'research_completion.json'
REBUILT=A/'Rafael557_reconstruction_v2_20261105/reconstruction.json'
DELTA=A/'Rafael557_company_punctuation_v1_20261105/observed_punctuation_andprose_revision.json'
OLD=A/'Rafael557_stored_checkpoint_v1_20261105/offline_completion.json'
PACKAGE=A/'Weekend_testing_package_v1_20261105/package_verification.json'
RELEASE=A/'Rafael867_extended_release_verified_v3_20261105/registered_release_verification.json'

if __name__=='__main__':
    ready,actual,rebuilt,delta,old,package,release=map(load,[READY,ROOT/'actual_review.json',REBUILT,DELTA,OLD,PACKAGE,RELEASE])
    assert ready['all_individual_five_gates_pass'] and (ready['records'],ready['revisions'],ready['retentions'])==(557,235,322)
    assert (actual['source_speech_variants_observed'],actual['native_body_pages_observed'],actual['offline_only_speech_variants'])==(188,193,361)
    assert actual['all_four_menus_default_cursor_andfollowing_fixture_speech_observed'] and len(actual['observed_public_name_actor_IDs'])==13
    assert rebuilt['research_ROM_sha256']=='5d40f92077efd6782e34c7146f4046b2aa4672a1f0b7366164c2503e06371d35'
    assert sha(Path(rebuilt['research_ROM']).read_bytes())==rebuilt['research_ROM_sha256']
    assert rebuilt['parent_sha256']==release['candidate_sha256']==package['ROM_sha256']
    assert ready['registered_integration_pending'] and ready['new_credit']==old['new_credit']==0 and len(delta['findings'])==2
    summary=('Rafael B141–B160 passed all five research gates for 557 records: 235 revisions and 322 justified retentions. '
        'Gameplay review caught two doubled periods after Castor Co.; both were corrected and verified in a focused replay. '
        'All 558 final pages, eight captions and 20 public names passed offline checks. '
        'Disclosed emulator fixtures observed 188 speech variants/193 final pages, 13 names and all four default-menu returns; 361 variants remain offline-only. '
        'Research 5d40f920 is ready for registered integration. No new credit or live jobs. Integrated 12,712, registered 3bf3, main 3cb8 and the weekend package are unchanged.')
    detail=f'''# Rafael557 research ready — November 5, 2026

All **557** B141–B160 records now pass all five individual research gates: **235 revisions and 322 justified retentions**. Exact clean/current and planned target references, individual findings, native controls, reviewed layout exceptions and gates are in `{ready['manuscript']}`. Reuse the sealed evidence in `{READY}`. This is a research milestone; integration credit remains zero.

The two initial representative fixtures completed the reviewed tutorial, map, private identity, alliance and Barkeep display sequences. A host checker initially counted the CP932 ellipsis shadow as dark ink. The successor matches both exact colors on the retained source punctuation, keeps FE checks separate and changes no ROM or font. The first story attempt lost its process before a terminal receipt at frame 8,520; its artifacts remain. Only that incomplete run was repeated.

Visual review found **two doubled periods** after the original FO substitution `Castor Co.` (B154R84/R114). The new wording keeps the Barkeep's reason for confiding, what the locals think of Maldonado and his cautious minimum expectation. Exact before/after clean context and retired captures: `{DELTA}`. All ten substitutions were checked; the other eight needed no change. Both revised pages passed fresh native and stored checks and a focused ordinary-input replay. The 547 other speech plans and 556 prior native page views are exact reuses. Three previously documented tutorial page boundaries remain because they keep whole thoughts together within the validated width; no prose was shortened to fit.

Three completed automated emulator runs total 65,763 frames. Exact final coverage in `{ROOT/'actual_review.json'}` is **188 speech variants, 193 pages, six FE notices, both FU substitutions, 13 of the 20 scoped names, and eight captions across four menus**. All four default cursor states and the next fixture speech after ordinary A were observed. The original story branch, location, chronology, other cursor states, cancellation and hardware were not exercised. **361 variants remain offline-only**. The focused replay replaces the same 14 observed B154 variants; there is no duplicate coverage credit. The 25 directly viewed QA sheets and all original captures are bound in `{ROOT/'complete_visual_approval.json'}`. No guide photography.

The corrected research ROM is `{rebuilt['research_ROM']}` (SHA-256 `{rebuilt['research_ROM_sha256']}`). It changes only the 20 owned SC0 blocks over registered 3bf3, and only B154 differs from the previous research reconstruction. Complete inverses, controls, glyphs, stored pages, all 1,190 relocated cases, 549 effective catalogue bodies and 343 archive loads pass. Exact reuse is recorded; the new run refreshed only B154 branch/handoff cases, two catalogue lookups and two native pages. All four stored choice objects preserve exact caption bytes and index order. This is a pinned research image, not a playable release handoff.

Next integrate this exact revised research target through the registered cumulative extension workflow. Use the five-gate manuscript and release plans in `{ROOT}`. Preserve all 114 accepted layers, all eight final stages including ASCII right bounds, original core, previous profiles and prior evidence. Require the semantic/order rejections, manifest, exact clean-input patch, own startup and once-only credit before claiming integration. No native or gameplay check needs repeating without a changed dependency. No live jobs remain.

Integrated totals remain **12,712 = 7,283 revisions + 5,429 retentions**. Registered 3bf3, main 3cb8 and the weekend ZIP are unchanged. All remaining storylines, tutorials, shared shop/town/random dialogue, names and player-facing prose remain in scope. The two full-catalogue particle fixes, deferred artwork and later older-record technical re-audit remain separate. Preserve all ROMs and translations; no pruning or main promotion.
'''
    evidence={str(p):sha(p.read_bytes()) for p in [READY,ROOT/'actual_review.json',ROOT/'complete_visual_approval.json',REBUILT,DELTA,OLD,PACKAGE,Path(__file__)]}
    checkpoint(mutation=A/'Rafael557_research_ready_ledger_20261105',batch_key='Rafael_SC0_B141_B160_clean_20261105',
        batch_updates=dict(new_credit=0,manuscript=ready['manuscript'],manuscript_sha256=ready['manuscript_sha256'],
            release_plans=ready['plan'],release_plans_sha256=ready['plan_sha256'],all_fifth_formatting_gates_pending=False,
            all_five_research_gates_pass=True,all557_individual_five_gates_pass=True,representative_gameplay_pending=False,
            registered_integration_pending=True,actual_source_variants=188,actual_pages=193,offline_only_source_variants=361,
            actual_nameplates=13,actual_menu_cursor_states=[0],observed_FO_punctuation_revisions=2,
            research_completion=str(READY),research_completion_sha256=sha(READY.read_bytes()),
            research_ROM=rebuilt['research_ROM'],research_ROM_sha256=rebuilt['research_ROM_sha256'],evidence=evidence),
        additional_updates={'editorial_execution_priority_20261104':dict(new_credit=0,
            current_batch='Rafael557: all five research gates and corrected B154 replay pass. Registered cumulative integration next.',
            next_action='Register and build the exact 557 successor over verified 3bf3, verify all eight stages and clean patch, then credit once.',
            native_job_live=False,guide_photos=False)},summary=summary,
        document='docs/editorial_Rafael557_research_ready_20261105.md',document_text=detail,completed=12712,
        protected={'translations/release_stack.json':release['registry_sha256'],
            'dk4tool/rom/nds.py':'27ce07965815b1c71ce39ce166406507fab621631b2373a96733eccd75dc2963',
            'out/raphael_natural_v2_accepted_base.nds':'3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe',
            release['candidate']:release['candidate_sha256'],package['zip']:package['zip_sha256']})
    print('Saved all 557 research gates and exact observed/offline coverage. Integration remains pending; protected builds and weekend ZIP are unchanged.')
