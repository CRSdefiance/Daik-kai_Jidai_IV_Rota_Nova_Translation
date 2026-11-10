"""Save427 once-only completions and261 new body/menu/reconstruction progress."""
from pathlib import Path
from scripts.audit_story_glyph_consistency import load
from scripts.save_editorial_progress_checkpoint_v5 import checkpoint
from dk4tool.patch.grand_race_menu_release import sha

ROOT = Path('work/analysis/Help97_Rafael330_release_verified_20261105')
DOC = Path('translations/rafael_B85_B100_contextual_editorial_manuscript_v2.json')
NATIVE = Path('work/analysis/Rafael261_native_final_v4_20261105/compiled_native_pages.json')
MENU = Path('work/analysis/Rafael261_choices_20261105/complete_native_visual_approval_v1.json')
REBUILD = Path('work/analysis/Rafael_B85_B100_rebuilt_v1_20261105/reconstruction.json')

if __name__ == '__main__':
    release, completion, doc, native, menu, rebuild = map(load, [ROOT/'registered_release_verification.json', ROOT/'completion_checkpoint.json', DOC, NATIVE, MENU, REBUILD])
    assert completion['new_credit'] == 427 and completion['counts']['completed'] == 11845
    assert not release['own_registered_startup_pending'] and release['clean_input_patch_byte_exact']
    assert (doc['proposed_revisions'], doc['justified_retentions'], doc['four_gate_passes']) == (111, 150, 261)
    assert not doc['pending_name_term_IDs'] and not any(r['review']['formatting'] for r in doc['records'])
    assert len(native['records']) == 255 and native['pages'] == 256 and native['all256_complete_pages_directly_viewed']
    assert menu['typed_labels'] == 6 and menu['all_three_native_caption_sheets_directly_viewed']
    assert (rebuild['speech_count'], rebuild['typed_choice_count'], rebuild['command_count'], rebuild['relative_sites']) == (255, 6, 453, 60)
    summary = ('Rafael/tutorial priority continues. Help97 plusRafael330 integrated once:11845 completions '
        '(6836 revisions/5009 retentions),678 entries/114 layers/eight stages/26 checks,exact clean patch,own4001-frame '
        'startup/RAM/Fernan getters pass. Experimental cc71ec06;main unchanged. Coerce33 is a zero-credit amendment. '
        'Next Rafael261 nowallfour prose gates:111 revisions/150 retentions,no name/term holds. '
        '255 speeches/256 native-viewed pages andsix captions/three native menus pass;ten wrap refinements,245 exact body reuses. '
        'All16 blocks reconstructed with453 commands/60 relative sites andfive control-only blocks preserved. '
        'Stored consumers/loaders,native nameplate views,focused gameplay andregistered integration remain;all261 fifth gates false. '
        'No guide photos;all routes,earlier translations,town-shop/random scenes,names/glyphs,ROMs andevidence remain in scope.')
    text = '''# Help97/Rafael330 integrated; next Rafael261 native pages — November 5, 2026

Rafael’s early storyline and all tutorials remain first. Preserve the full all-route editorial objective, earlier translations, justified retentions, coverage credit, ROMs and evidence. No guide photos, promotion, pruning or commit/push. The main ROM is unchanged.

## Verified cumulative release and once-only credit

`out/all_routes_combined_help97_rafael330_20261105_candidate.nds` is the new verified **experimental** cumulative candidate, SHA-256 `cc71ec06ce5345dcc71f8b631232f4d8d501152f6989374741616260fa0ca448`. Its adjacent `.xdelta` reconstructs this exact image from clean input `f4f07c975cc293f5b2ba469747693d3dd37f2e6dfc408cf5910adf5e83d9177d`. The original nine-driver build completed; all678 manifest entries,114 accepted layers,26 checks and eight final stages pass, including ASCII right bounds and Fernan’s ordinary F. Registry remains `86770091eb469009f039c35185a51e7731478fa21b6869527b7d2042d601d5b8`; original ROM core remains `27ce0796`.

`work/analysis/Help97_Rafael330_release_verified_20261105/` holds release verification, exact integrated references, patch reconstruction, composite coverage, the final ROM’s own4001-frame/captain0/route0/RAM/payload/startup proof, both Fernan getters and the once-only completion receipt. The previously captured exact-identity startup and10 exact reviewed RGB pairs were reused without another emulator run. All generated ROMs remain preserved.

`translations/Help97_Rafael330_integrated_final_review_v1.json` retains all428 individual decisions with final references:97 new Help articles,330 Rafael objects and the already-credited Coerce33 amendment. Exactly427 new objects were credited (191 revisions/236 retentions);33 earns no duplicate credit. Integrated totals: **11845 =6836 revisions+5009 retentions**. Historical source/prose totals retain their existing three-record offset:11848. All202 Help source topics now have integrated contextual review; later gameplay discoveries can still amend them.

Gameplay scope remains honest. The103 Help pages have56 observed pages/51 articles and47 offline-only pages, with22 exact older page observations reused and33 included in the amendment count. Rafael330 has336 native body pages;75 source speeches/77 commands/86 body pages andfive choices were observed in disclosed initialized fixtures, while250 speeches are offline-only. These composite observations are not one complete final-ROM playthrough, natural event activation, earned chronology or hardware verification. Existing full source/control/native/menu/name/branch proofs were reused where dependencies match.

## Next Rafael261: all four prose gates; native body/menu review complete

`translations/rafael_B85_B100_contextual_editorial_manuscript_v2.json` covers255 speeches andsix captions in11 complete exchanges across B85–B100. It records **111 revisions/150 justified retentions**, all261 four-gate passes andzero name/term holds. Preserve earlier independent drafts and comparisons; do not rereview/rechoose these261 from scratch. Every fifth formatting gate remains false until stored checks and representative gameplay are finished. See the preceding checkpoint for the source-complete initial comparisons, ten untranslated speeches and substantive participant/payer/identity-exposure/rumor corrections.

`work/analysis/Rafael261_names_terms_20261105/names_macros_andconsumer_dependency_qualification_v1.json` binds20 scoped actors:12 fresh clean/current two-getter executions andeight exact dependency-qualified reuses. Public role getters return Sailor for actors151/152/158; do not copy raw full-catalogue Retainer or unused nationality metadata into dialogue headers. Cesare Tony is a specifically justified retention, consistent with its earlier individual review, without a new canonical-Latin claim. Preserve Clau’s explicit source nickname. Spoken Mihwa nowmatches the native name field; Zipangu follows registered current text data. Five item labels are bound through actual pointer fields and verified own RAM, including the relocated Sweeping Katzbalger pool pointer. Generic source Katzbalger does not acquire its unspoken epithet; Ninja Garb keeps the source black/rogue context. This is lexical/getter evidence, not new item-card/location-UI or20-header gameplay approval. Global207/full-catalogue review remains open.

Final plan: `work/analysis/Rafael261_sparse_row_refinement_v4_20261105/full_plan/automatic_plans.json`. Final native proof: `work/analysis/Rafael261_native_final_v4_20261105/compiled_native_pages.json`, with `direct_visual_approval.json`. All255 speeches/256 pages pass complete leading/internal/trailing glyph codes and independent pixels, four native macro alignments each, bounds/canaries, complete consumption and pagination. Every base page, twelve delta pages andone final sparse-opening replacement were directly viewed on readable sheets. Four full-width I characters andsix English question marks nowuse normal ASCII.

Ten exact wrap refinements preserve every prose character: a complete closing sentence across B86R75’s page turn, a quoted question, a connected thinking-about phrase, a welcome, greeting, help-out/come-on imperatives, a short question tag, Let’s get moving and Some of these seeds.245 unchanged body records reuse exact native proofs. A35-character whole-sentence constraint failed the validated guard budget and is preserved as a failed plan; geometry was not relaxed. One attempted fleet-of-my-own constraint stranded I’d like on a sparse middle row, so retain its better-balanced original layout with an explicit reason. A sparse Just opening was replaced by the full Just thinking about it phrase. No prose shortened, engine/font enlarged, or ordinary manual breaks added.

`work/analysis/Rafael261_choices_20261105/complete_native_visual_approval_v1.json` approves six captions inthree original two-choice objects (B85@80,B88@814,B91@110); allthree sheets were viewed. All native provider alignments, original selection/cancel response paths, caption planes/styles, centering/bounds and compiler negatives pass. Modal loops are bridged offline; actual controller highlight/A-response coverage remains pending. B88 initially exposed a host diagnostic’s32-byte sample truncating a34-byte clean Japanese label. `B88_provider_failure_v1.json` preserves that finding. `check_rafael_two_choice_display_v2.py` reads through the NUL within the supplied object’s exact bounds; original getter/width/instructions/canaries remain unchanged. The complete label then passes. This was a harness limitation, not a discovered in-game truncation.

## Reconstructed research batch; next work

`work/analysis/Rafael_B85_B100_rebuilt_v1_20261105/reconstruction.json` binds all16 blocks,453 commands,60 branch-relative sites,255 speeches andsix captions inthree compound menus. The11 dialogue blocks change; B89/B94/B96/B98/B99 remain byte-identical control-only blocks. Complete clean/current block/archive/serialized-ROM inverses pass, and all unowned files/components match parent675. Research image `reviewed_RESEARCH_ONLY.nds`, SHA-256 `39f7e6fa3a2759f66cddaee9262aa84a4b34f7210d475aa0b55318c3b1e96e1a`, is preserved. It is not a registered successor and earns no completion credit.

Next: qualify all stored native lookups/pages, branch cases andloaders; render/reuse exact scoped nameplate planes; then run representative initialized story/menu/pagination/transition samples, including distinct generic-role headers, the miracle choice/FE notices and Charles’s two-page speech. Actual natural route/conditional activation is not required. Reuse the exact native/menu/macro proofs already completed.

**Rebase only owned B85–B100 blocks onto the new678 cumulative parent before registration.** The research reconstruction uses parent675; copying its whole SC0 archive into678 would lose the just-integrated B81–B84 revision. Preserve new Help andB81–B84, refresh global archive references andqualify unchanged renderer/name/macro dependencies. Reuse the exact owned block reconstructions andpage bytes; do not repeat prose/native work solely for the new cumulative identity. Registered integration remains pending for these261 objects.

Main remains `out/raphael_natural_v2_accepted_base.nds`, SHA-256 `3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe`. All other routes, prior unfinished contextual passes, shared town/shop exchanges, random scenes, remaining player-facing prose andname/glyph consistency stay in scope. Keep graphics artwork andthe later older-record technical re-audit separate. Full goal active.
'''
    protected = {str(p): sha(p.read_bytes()) for p in [DOC, NATIVE, MENU, REBUILD, ROOT/'completion_checkpoint.json', ROOT/'registered_release_verification.json',
        Path('translations/release_stack.json'), Path('dk4tool/rom/nds.py'), Path(release['candidate']), Path('out/raphael_natural_v2_accepted_base.nds')]}
    checkpoint(mutation='work/analysis/Help427_integrated_Rafael261_native_checkpoint_20261105', completed=11845, protected=protected,
        batch_key='Rafael_SC0_B81_B100_clean_20261105', summary=summary,
        document='docs/editorial_Help427_integrated_Rafael261_native_20261105.md', document_text=text,
        batch_updates=dict(new_credit=0, contextual_comparisons=591, proposed_revisions=285, justified_retentions=306, four_gate_passes=591,
            previous330_integrated_andcredited=True, previous330_registered_build_live=False,
            next261_review=str(DOC), next261_review_sha256=sha(DOC.read_bytes()), next261_proposed_revisions=111, next261_justified_retentions=150,
            next261_four_gate_passes=261, next261_name_term_holds=0, next261_all_fifth_gates_pending=True,
            next261_native_proof=str(NATIVE), next261_native_proof_sha256=sha(NATIVE.read_bytes())),
        additional_updates={
            'Rafael_SC0_B85_B100_contextual_20261105': dict(new_credit=0, contextual_review=str(DOC), contextual_review_sha256=sha(DOC.read_bytes()),
                proposed_revisions=111, justified_retentions=150, four_gate_passes=261, pending_name_term_IDs=[],
                native_speeches=255, native_body_pages=256, all_native_body_pages_directly_viewed=True, native_proof=str(NATIVE), native_proof_sha256=sha(NATIVE.read_bytes()),
                menu_visual=str(MENU), menu_visual_sha256=sha(MENU.read_bytes()), reconstruction=str(REBUILD), reconstruction_sha256=sha(REBUILD.read_bytes()),
                all_fifth_formatting_gates_pending=True, actual_gameplay=False, stored_consumers_loaders_actual_andregistered_integration_pending=True,
                native_visual_stored_actual_andintegration_pending=True, needs_owned_block_rebase_to678_not_whole675_archive=True),
            'editorial_execution_priority_20261104': dict(new_credit=0, current_batch='Rafael_SC0_B85_B100_contextual_20261105',
                next_batch='Rafael_SC0_B85_B100_contextual_20261105', registered_cumulative_build_live=False, registered_build_live=False, build_live=False,
                registered_build_terminal=True, registered_build_exit_code=0, registered_integration_pending=False,
                current261_four_gate_passes=261, current261_name_term_holds=0,
                next_focus='Complete Rafael261 stored native/branch/loader/nameplane checks andrepresentative gameplay;rebase owned blocks only onto678 andintegrate when gates pass. All202 Help topics integrated;full all-route objective remains.')})
    print('Checkpoint saved:11845 integrated;next261 allfour prose gates/256 viewed body pages/six menus/reconstruction,zero newcredit. Fullgoalactive/main unchanged.')
