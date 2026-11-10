"""Archive the registered361-review successor without changing earlier credit or evidence."""
import re
from pathlib import Path
from scripts.source_locked_derivation_v5118 import checked_text

parent = Path('scripts/checkpoint_lil269_registered_v1.py').read_text(encoding='utf-8')
source = checked_text(parent, {
    'Lil269_offline_20261110_v3': 'Lil361_stored_actual_partial_20261110_v1',
    'lil269': 'lil361',
    'Lil269': 'Lil361',
    'B243_B282': 'B283_B298',
    'all269_individual_five_gates_pass': 'all361_individual_five_gates_pass',
    'work/story_source_coverage_20261110_SC2_v4/coverage.json': 'work/story_source_coverage_20261110_SC2_v5/coverage.json',
    '(139, 141, 64563)': '(199, 200, 86324)',
    "assert before.startswith(b'Lil382 residual A is registered')": "assert before.startswith(b'Lil269 B243')",
    'final_formatting_bodies=262, final_formatting_pages=264, source_bound_layout_changes=16, pages_reclaimed=1':
        'final_formatting_bodies=352, final_formatting_pages=353, source_bound_layout_changes=9, pages_reclaimed=0',
    'native_rendering_pending=False, direct_visual_review_pending=False, stored_checks_pending=False, gameplay_pending=False,':
        'native_rendering_pending=False, direct_visual_review_pending=False, stored_checks_pending=False, gameplay_pending=False, actual_direct_visual_review_pending=False, actual_menu_transition_approval_pending=False,',
    "Path('scripts/analyze_rafael_B201_B220_menu_actual_v1.py')":
        "Path('scripts/analyze_rafael_B201_B220_menu_actual_v1.py'),Path('scripts/check_reviewed_lil_actual_menus_v1.py')",
    "next_action='Continue remaining1154 native Lil positions from complete B283 source context; retain B294 earlier credited context. Full shared/player-facing/name scope remains active; main acceptance is separate.'":
        "next_action='Continue remaining793 native Lil positions from complete B299 clean source context. Preserve source-first seals and prior credit. Full shared/player-facing/name scope stays active; main acceptance remains separate.'",
})
counts = {'269': '361', '104': '178', '165': '183', '727': '728', '62': '63',
    '24744': '25105', '14704': '14882', '10040': '10223', '1154': '793'}
pattern = re.compile(r'(?<![A-Za-z0-9_])(?:' + '|'.join(sorted(counts, key=len, reverse=True)) + r')(?![A-Za-z0-9_])')
source = pattern.sub(lambda m: counts[m[0]], source)
start = source.index("    partial = next(g for g in residual['groups']")
end = source.index("    assert actual['all_actual_body_menu_andtransition_sheets_directly_viewed']", start)
source = checked_text(source, {source[start:end]: """    assert not any(g['block'] == 294 for g in residual['groups'])
    context = load(ROOT/'credited_context_rebuild_qualification_v1.json')
    assert context['preserved_context_objects'] == 1 and context['new_owned_speeches'] == 15
    assert context['actual_clean_current_andtarget_inverses_pass'] and context['positive_B294_target_byte_exact']
"""})
start = source.index('    lead = ')
end = source.index('    assert before.startswith', start)
source = checked_text(source, {source[start:end]: """    lead = '''Lil361 B283–B298 is registered over Lil269:728 entries,114 accepted layers and63 release checks. Use `scripts/build_registered_lil361_v1.py` and `--register`; pure transaction:`dk4tool/patch/lil361_release_v1.py`. All361 source reviews,353 body pages,nine captions,exact clean-input patch,own startup and24 protected getters pass. Preserve all727 predecessor entries,Market format/both pointers,six-section ARM9,ASCII right bounds,source25v2 andB164R99. B294 uses the frozen preintegration credit witness and credited-context helper to preserve R73 without duplicate credit. Native Lil remainder793;next complete clean groupB299. Full goal active;main requires acceptance. Continue from [the registered checkpoint](editorial_Lil361_registered_20261110.md);earlier entries are history.

'''
"""})
start = source.index('    summary = ')
end = source.index('    protected = ', start)
source = checked_text(source, {source[start:end]: """    summary = ('Lil B283–B298 is registered and credited once:361 contextual reviews,178 revisions,183 justified retentions and15 scoped names. '
        'All353 body pages,nine captions and19 name strings pass; nine layouts improve,including one FE extra blank row,without changing prose. '
        'Three primary emulator samples observe199 bodies/200 unique pages,one page turn,15 FE returns andfour menus;153 personality alternatives remain offline-only. '
        'One focused longer-tail replay verifies the unchanged host exit; four runs total86,324 frames/242 page occurrences/22 viewed sheets. '
        'The728-entry/114-layer candidate passes63 release checks,exact clean-input reconstruction,own startup,24 protected getters and27 fresh tests. '
        'Integrated25,105;native Lil remainder793. Testing ROM/patch ready;main awaits acceptance;full goal active;no worker live.')
    document = Path('docs/editorial_Lil361_registered_20261110.md')
    text = f'''# Lil361 registered cumulative candidate — November 10, 2026

{summary}

Use [the testing ROM](../out/promotion_ready_20261110_lil361_v1/Translation_DS_All_Routes_Lil361_20261110_candidate.nds) with its adjacent manifest. SHA-256:`{release['candidate_sha256']}`. [Standalone clean-input patch and notes](../{package.as_posix()}/README.md), patch SHA-256:`{release['patch_sha256']}`. This includes the newly registered361 records, unlike v5. All727 predecessor entries and114 accepted layers remain: Rafael/tutorial work, Market format/both pointers, six-section ARM9, ASCII right bounds, source25v2 andB164R99. Only `/data/SC2.DK4` changes relative to registered Lil269; other files/components are byte-exact. Canonical base:`{release['canonical_base']}` (`{release['canonical_sha256']}`). Main remains V4701 pending cold-boot acceptance. Earlier ROMs, translations and source-first seals are preserved. Both the previous packaging/checkpoint turn and this completed integration turn are progress; the full goal stays active.

The16 whole clean-source exchanges cover175 ordinary bodies,177 physical personality alternatives andnine captions. [Integrated review ledger](../translations/lil361_B283_B298_integrated_final_review_v1.json) preserves exact source/current/registered references, individual findings,178 revisions,183 justified retentions andallfive gates. Fifteen scoped actors retain19 qualified strings, with individual reasons. Full catalogue UI, future role assignments andbroader name localization remain open. Earlier clean meanings and independent drafts precede current-English exposure; no completed batch is restarted.

The reviewed conversations preserve the forest bear's play-dead joke, Emilio actually falling asleep, uncertain injuries andpossible man-eater; the London job's approximately200 barrels/two cargo holds,8,000 gold andsmall share gain; Mikhail's mistaken contact joke without inventing a body part/romance; cramped-cave gunfire risking friends andinferred hunger during escape; Angkor's pure-new-star riddle,Alchemy Book andold coin without inventing a deity title/gender; the foggy mountain route andcrew separation without invented deaths; the hidden Christian settlement anduncertain Mediterranean map lead; andthe emperor's vassal-king guest,Heavenly Wristband,one-day loan,25,000 gold andsmall Istanbul share gain. Three stale Constantinople mentions become Istanbul. FA is the Argot surname,not invented company membership. Good reactions,humor andcharacter voices remain for individual reasons. See [the prose checkpoint](editorial_Lil361_prose_plan_20261110.md) for detailed source findings.

Final plan:`plan_v6/automatic_plans.json`,352 bodies/353 pages,zero errors/warnings/failures. Nine layouts improve relative to the first plan:seven phrase wraps,one cliff page boundary andone FE reserve/phrase correction. All logical prose andthe353-page count remain unchanged. The observed B292R50 defect was an extra space-only row; non-space glyphs were not lost. The qualified FE36 reserve removes it at unchanged228px physical width,font,controls andruntime. The final three lines andordinary A return are directly seen. All353 final pages,allnine captions andall19 name strings were viewed andbound to native pixels; old failed/superseded trials remain preserved. No good prose was shortened for fit.

Stored reconstruction verifies all16 groups/579 commands/175 relative sites andactual clean/current/block/whole-archive/serialized-NDS inverses. B294 retains one earlier credited R73 as context alongside15 new reviews; the frozen24,744-key witness andfive deliberate context-helper negatives prevent losing orrecrediting it. Stored checks pass353 pages (91 fresh parity-dependent/262 exact native reuses),875 relocated native relative cases,352 complete-buffer lookups,336 SC2 loads/cache hits and672 parent handoffs. All192 personality slots across24 objects and216 compiler negatives pass. Controls,macros,complete leading/internal/trailing glyphs,consumption,canaries,bounds,allocation andpagination pass. These are offline checks.

Three initialized B22-host samples observe199 bodies/200 unique pages:all175 ordinary bodies and24 current personality selections. The153 other physical personality alternatives remain offline-only. Allfour menus/nine captions pass exact pixels,centering,cursor bands/backgrounds andfollowing A returns. Observed cursor indices:Other1/2 progression,Run away0/1,Run0/1 andWait0. The cliff explanation turns normally to its second page;15 FE panels return normally. All18 body sheets andthree menu sheets were directly viewed andtheir exact original capture tiles verified.

The first host-transition check correctly stopped because the original captures had not reached resupply/tutorial. One unchanged-ROM longer-tail run adds6,000 frames andordinary A presses, preserving the entire original input prefix andevery scene command. Its42 selected-page PNGs match the earlier directly viewed captures byte for byte. It reaches native crew joining,resupply andthe following steering tutorial; its transition sheet is directly viewed andbound to original full-screen captures. The timing shortfall required no ROM correction. Only this focused fourth run claims the complete host exit. Total:86,324 frames,242 body-page occurrences,200 unique source-body pages and22 viewed sheets. Original expeditions/conditions,locations,chronology,quest outcomes,rewards/stats,numeric menu registers/cancellation,full-route playthroughs,catalogue UI andhardware remain unvisited; native numeric-return/cancellation checks remain separate offline evidence. No savestate,battery,RAM,roster,RNG orcondition-result override was used for these Lil samples. No free-sailing ororiginal quest progression credit is inferred from the QA host.

The exact cumulative candidate separately passes its own31,000-frame Maria/Hangzhou cold boot,six directly viewed captures and24 original protected-name getter cases. Its existing isolated system unlock is disclosed andunearned. All63 registered release checks,27 fresh repository tests andeight production-scope negatives pass. Both independent clean-input reconstructions are byte-exact andallpackage checksums pass. Accepted layers,allprevious profiles,main andcanonical base remain unchanged. The testing ROM and reconstruction are explicitly pinned.

Integrated:25,105 =14,882 revisions +10,223 retentions. Native Lil census:5,927 of6,720 exact positions covered,793 remaining; native Maria remains5,129/5,129. All6,720 clean-source positions were rechecked against the reused native inventory,with zero duplicated credit. Remaining complete groups begin atB299. B294 is fully covered,including its earlier credited context; its earlier packet stays archived.

[Lossless registered evidence archive](../{archive.as_posix()}) preserves current JSON/TXT/XML receipts,failed/superseded plans,source/current prose,individual comparisons,source census andrelease proofs,with exact earlier artifact reuses. Raw ROM/RAM/captures/planes remain local. Resume the full remaining contextual storyline/shared/shop/town/random/player-facing/name review from B299 without repeating completed checks. Keep early Rafael/tutorial priorities,guide-photo collection discontinued,deferred graphics artwork andthe later older-record technical re-audit separate. Main acceptance is independent of ongoing editorial work. No worker is live.
'''
"""})

if __name__ == '__main__':
    exec(compile(source, __file__ + '::same-earned-credit-preserving-atomic-checkpoint-andlossless-archive', 'exec'), globals())
