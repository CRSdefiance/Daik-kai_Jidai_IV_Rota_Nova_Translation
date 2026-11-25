"""Save the verified-live678 build and261 new contextual comparisons without completion credit."""
from pathlib import Path
from scripts.audit_story_glyph_consistency import load
from scripts.save_editorial_progress_checkpoint_v5 import checkpoint
from dk4tool.patch.grand_race_menu_release import sha

if __name__=='__main__':
    prep_path=Path('work/analysis/Help97_Rafael330_release_v2_20261105/registered_preparation.json')
    qualification=Path('work/analysis/Help97_Rafael330_release_qualification_20261105/qualification.json')
    startup=Path('work/analysis/Help97_Rafael330_identity_coldboot_20261105/identity_RGB_qualification.json')
    review_path=Path('translations/rafael_B85_B100_contextual_prose_review_v1.json')
    sealed=Path('work/analysis/Rafael_B85_B100_clean_drafts_20261105/261_source_meanings_andindependent_drafts_v1.json')
    prep,q,opening,review=map(load,[prep_path,qualification,startup,review_path])
    assert len(q['changed_scope_andordering_rejections'])==11 and q['direct_prepublication_andshared_targets_equal']
    assert len(opening['exact_RGB_pairs'])==10 and opening['actual_coldboot_frames']==4001
    assert len(review['records'])==261 and (review['proposed_revisions'],review['justified_retentions'],review['four_gate_passes'])==(108,153,229)
    assert len(review['pending_name_term_IDs'])==32 and not any(r['review']['formatting'] for r in review['records'])
    assert prep['registry_sha256']=='86770091eb469009f039c35185a51e7731478fa21b6869527b7d2042d601d5b8'
    summary=('Rafael/tutorial priority continues. Three ordered extensions (97 new Help articles, zero-credit Coerce33 amendment, '
        'and Rafael330) are registered as profile all-routes-help97-rafael330-v2-20261105. Shared plans and11 semantic/order '
        'rejections pass;114 accepted layers andall eight final stages remain exact. The678-entry original-source build is '
        'OS-confirmed live in session24565/PID98840; expected cc71ec06. Its own4001-frame planned startup matches10 reviewed '
        'RGB pairs;final registered identity/manifest/patch/RAM binding and427 once-only credits remain. Next Rafael255 speeches '
        'plus6 choices now have clean meanings, independent drafts and261 complete-exchange comparisons:108 proposed revisions/'
        '153 justified retentions,229 four-gate passes/32 name-term holds. Found10 untranslated speeches,4 full-width I letters '
        'and concrete participant/payer/identity-exposure/rumor errors. All261 fresh display gates remain pending. '
        '11418 integrated;verified81511/main unchanged. No guide photos;full scope andall ROMs/evidence preserved.')
    text='''# Ordered Help97/Rafael330 build and next Rafael261 comparisons — November 5, 2026

Rafael’s early story and all tutorials remain first. Preserve all earlier translations, completed reviews, justified retentions, ROMs and evidence, with every storyline, shared town/shop exchange, random scene, speaker label and text-display issue still in scope. No guide-photo collection, promotion, pruning or commit/push. Reuse [the Rafael330 five-gate research checkpoint](editorial_Rafael330_research_ready_20261105.md).

## Registered build — preserve the live process

Profile `all-routes-help97-rafael330-v2-20261105` adds three ordered layers: Deck30 plus the zero-credit Coerce33 correction, remaining Help67, then Rafael330. There are427 new source editorial objects (191 revisions/236 retentions), with one additional amendment that earns no duplicate credit. All114 accepted layers and eight final stages, including ASCII right bounds and Fernan’s F, are preserved. Expected678 manifest entries and final SHA-256 `cc71ec06ce5345dcc71f8b631232f4d8d501152f6989374741616260fa0ca448`.

Preparation: `work/analysis/Help97_Rafael330_release_v2_20261105/registered_preparation.json`. The frozen registry hash is `86770091eb469009f039c35185a51e7731478fa21b6869527b7d2042d601d5b8`. Qualification: `Help97_Rafael330_release_qualification_20261105/qualification.json`; three direct/shared targets and11 changed-scope/order rejections pass. Reuse the seven FE/15 menu native negatives and all unchanged stage proofs. V1’s direct source reconstructions remain valid; its registration preflight found uppercase identity, shared module ownership and missing transaction-contract metadata. V2 uses three exclusive adapters and reuses all11 exact research ROMs. V1 modules/configs/profile and findings are preserved; no v1 playable-build claim.

**Build session24565/PID98840 is OS-confirmed live**, using unchanged `run_registered_build_with_gc_v3.py`, all nine original drivers and original ROM core `27ce0796`. Command profile/output/work: `all-routes-help97-rafael330-v2-20261105`, `out/all_routes_combined_help97_rafael330_20261105_candidate.nds`, `work/h97r330`. Telemetry: `work/analysis/Help97_Rafael330_registered_build_20261105/`. Latest checked at3571 seconds: process present, collector errors empty, peak private memory about2.20GB. Do not restart a quiet build or mutate its registry/core/drivers/configs. Poll this exact session or confirm authoritative terminal status; a missing observation is not failure.

Own planned startup is already terminal: `work/analysis/Help97_Rafael330_identity_coldboot_20261105/`. Its4001-frame cold boot used ordinary New Game inputs, no savestate/battery/RAM override. `identity_RGB_qualification.json` binds all10 exact previously viewed RGB pairs, unchanged opening B44/EV0/COMMON/font/code, only SC0B81–84 plus the ordered Help resource changes, and all103 new Help pages to their reviewed bytes. Do not repeat that capture after the build if final identity is exact. Final registered manifest/stages, clean-input patch reconstruction, own RAM/captain0/route0/context and Fernan getters still need final binding. The composite release verifier and own-startup adapter have not yet been prepared. Credit427 only after those checks pass.

## Next Rafael261 — substantive contextual progress

`work/analysis/Rafael_B85_B100_clean_drafts_20261105/261_source_meanings_andindependent_drafts_v1.json` seals255 speech meanings/independent drafts plus six choices before current-English extraction. Eleven complete exchanges span16 inventoried blocks; B89/B94/B96/B98/B99 are control-only. Source/current speech binding: `work/analysis/Rafael_B85_B100_current_20261105/current_effective.json` (255 native pre-macro catalogue lookups with exact complete preambles/command kinds). The three original two-choice objects are B85@80, B88@814 and B91@110. Raw current references and all six source/current caption bytes are in `current_choice_andglyph_findings_v1.json`.

`translations/rafael_B85_B100_contextual_prose_review_v1.json` records **261 complete-exchange decisions:108 proposed revisions/153 justified retentions**, with229 four-gate passes and32 explicit name/term holds. Every fifth formatting gate remains false. `translations/rafael_B85_B100_contextual_decision_data_v1.py` saves the individual selection reasons, targeted findings and overrides, so do not reread and rechoose all261 from scratch. Earlier source draft v1/v2 data are preserved; v2 only makes the initial145 glosses readable, with all255 English draft strings unchanged.

Coverage includes Gerhard’s conditional return, the full Charles explosion/factory/science recruitment, the complete Zipang extortion/Yukihisa intervention, both Julian crown branches, Janus’s Mediterranean wish, both miracle-belief branches, tomato seedling and banana scenes, Gerhard’s lost sword, the ninja-garb discussion/quarrel and the amber rumor. Retain the scientist’s fluent educated voice, clipped genuine reactions and comic exchanges that already work; do not rewrite them merely because independent drafts differ. Four retained action-choice captions are natural in their selectable context; miracle Trust/Doubt is revised to I do/I don’t.

Concrete corrections include:

- Ten current B91 speeches are still Japanese (R5/14/28/35/43/51/59/62/70/77).
- Julian’s current B88R65 reverses who cannot face whom. Source Julian cannot face Meihua.
- Emilio’s B93R73 My treat? reverses the payer; it must ask Your treat? before Rafael answers My treat.
- B97R28 makes witnesses die, while the source passive clause concerns a ninja whose identity is exposed.
- B100R38 loses the rumor qualification, and R45’s Nobody knows improperly expands the worker’s own uncertainty.
- Fernando’s FE notices91/112 lose his explicit name, and Janus’s future conditional regional-fleet promise becomes an impersonal assignment.
- Charles’s retained Good to see you greeting needs a reply to that greeting, rather than Do not thank me.

Four full-width I characters occur in B85R25 (one), B87R213 (two) and B88R39 (one). The first/last records retain their already-good words after documented ASCII normalization; B87’s welcome is a prose revision. Six full-width question marks occur in three English confusion lines. Two additional marks belong to the ten untranslated Japanese speeches and are not mislabeled as English glyph defects. The initial count-scope assertion failure and original producer source are preserved; it was a report preflight mistake, not a native display failure.

Twenty source/current speaker-field metadata bindings are saved under the clean-draft root. They are **metadata only**, not getter/header approval. Current raw Retainer fields do not prove visible labels: actor151 already has a prior actual Sailor getter, actor152 is the former sailor in B91, and actor158 is Kurushima’s henchman. Check actual consumers and other uses before changing generic-role owners; unused ethnic/geographic secondary fields must not become spoken labels. Cesare’s トーニ/Tony surname needs an explicit retention/correction decision. Bind Zipang/Meihua/Silla Gold Crown/bullet pendant/tomato seedling/Katzbalger/rogue-ninja garb against native approved terms. A quick reference search found golden Zipangu in the registered Mystery Hunt description source; current story uses Zipang, so qualify the actual current native term before finalizing it. Do not infer name approvals or personal relationships from raw metadata.

Next: finish those32 linguistic name/term bindings, use qualified name/macro/consumer proofs where dependencies match, then format the complete261 as one substantial batch. Every changed/retained reformatted text needs fresh bounds, complete glyph, allocation and pagination checks and all new pages viewed. Sample distinct native behaviors, new generic-role headers and useful town/random scenes; no exhaustive natural playthrough is needed. This batch is not integrated and has no completion credit.

## Preserved release and full scope

Integrated completions remain11418 =6645 revisions+4773 retentions. Verified experimental candidate remains `out/all_routes_combined_sea22_fleet66_20261105_malloc_candidate.nds`, SHA-256 `81511dde6bc4cd81dee799e8ce893ba06f1fa44d96bbd541ac86ca67ae2d9635`. Main stays `out/raphael_natural_v2_accepted_base.nds`, SHA-256 `3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe`. Do not promote the running build. All202 Help source topics retain completed research, with97 still awaiting this integration. Keep deferred graphics artwork and the later older-record technical re-audit separate. Full goal active.
'''
    protected={
        'translations/release_stack.json':prep['registry_sha256'],
        'dk4tool/rom/nds.py':'27ce07965815b1c71ce39ce166406507fab621631b2373a96733eccd75dc2963',
        'out/all_routes_combined_sea22_fleet66_20261105_malloc_candidate.nds':'81511dde6bc4cd81dee799e8ce893ba06f1fa44d96bbd541ac86ca67ae2d9635',
        'out/raphael_natural_v2_accepted_base.nds':'3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe',
        **{str(p):sha(p.read_bytes()) for p in [prep_path,qualification,startup,review_path,sealed]}}
    checkpoint(mutation='work/analysis/Help97_Rafael330_build_Rafael261_checkpoint_20261105',completed=11418,protected=protected,
        batch_key='Rafael_SC0_B81_B100_clean_20261105',summary=summary,
        document='docs/editorial_Help97_Rafael330_build_Rafael261_comparisons_20261105.md',document_text=text,
        batch_updates=dict(new_credit=0,source_draft_speeches=580,source_draft_choices=11,contextual_comparisons=591,
            proposed_revisions=282,justified_retentions=309,four_gate_passes=559,remaining_packet_speech_drafts=0,
            next261_review=str(review_path),next261_review_sha256=sha(review_path.read_bytes()),
            next261_proposed_revisions=108,next261_justified_retentions=153,next261_four_gate_passes=229,
            next261_name_term_holds=32,next261_all_fifth_gates_pending=True,
            previous330_five_gate_research_complete=True,previous330_registered_build_live=True),
        additional_updates={'editorial_execution_priority_20261104':dict(new_credit=0,
            current_batch='Rafael_SC0_B85_B100_contextual_20261105',
            next_batch='Help97_Rafael330_registered_cumulative_20261105',
            registered_cumulative_build_live=True,registered_build_live=True,build_live=True,
            registered_build_session=24565,registered_build_PID=98840,build_session=24565,build_PID=98840,
            registered_integration_pending=True,current261_contextual_comparisons=261,current261_four_gate_passes=229,
            current261_name_term_holds=32,
            next_focus='Preserve live678 build;finish32 Rafael261 name/term bindings andbatch-format all261. Onterminal0 verify fullrelease/patch/ownRAM andcredit427 once.')},
        new_entries={
            'Help97_Rafael330_registered_cumulative_20261105':dict(new_credit=0,profile=prep['profile'],
                preparation=str(prep_path),preparation_sha256=sha(prep_path.read_bytes()),
                qualification=str(qualification),qualification_sha256=sha(qualification.read_bytes()),
                build_live=True,build_session=24565,build_PID=98840,expected_manifest_entries=678,accepted_layers=114,
                all_eight_final_stages_preserved=True,expected_candidate_sha256=prep['target_ROM_sha256'],
                expected_new_source_objects=427,expected_new_revisions=191,expected_new_retentions=236,
                previously_credited_amendments=[33],own_planned4001_frames_terminal=True,
                own_planned_RGB_qualification=str(startup),own_planned_RGB_qualification_sha256=sha(startup.read_bytes()),
                registered_manifest_patch_RAM_binding_andonce_only_credit_pending=True),
            'Rafael_SC0_B85_B100_contextual_20261105':dict(new_credit=0,source_speeches=255,source_choice_labels=6,
                independent_meanings_anddrafts=str(sealed),independent_meanings_anddrafts_sha256=sha(sealed.read_bytes()),
                current_effective='work/analysis/Rafael_B85_B100_current_20261105/current_effective.json',
                contextual_review=str(review_path),contextual_review_sha256=sha(review_path.read_bytes()),
                contextual_comparisons=261,proposed_revisions=108,justified_retentions=153,four_gate_passes=229,
                pending_name_term_IDs=review['pending_name_term_IDs'],all_fifth_formatting_gates_pending=True,
                untranslated_current_speeches=10,fullwidth_I_letters=4,fullwidth_I_records=3,
                six_fullwidth_English_questionmarks_inthree_records=True,native_visual_stored_actual_andintegration_pending=True,
                actual_gameplay=False,guide_photos=False),
        })
    print('Saved live678 build and261 new contextual comparisons;11418 integrated unchanged;all scope/ROMs preserved.')
