"""Preserve the registered candidate and save concise authoritative progress."""
import os
from pathlib import Path
from scripts.audit_story_glyph_consistency import load,save
from scripts.build_registered_hodram_B251_B280_v1 import CANDIDATE,INVERSE_PATCH,RELEASE,REGISTRY,OUT
from scripts.approve_hodram_B251_B280_display_v5 import ROOT
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.save_editorial_progress_checkpoint_v7 import checkpoint
from scripts.save_rafael3222_weekend_checkpoint_v1 import PACKAGE


def main():
    release=load(RELEASE);completion=load(OUT/'completion_checkpoint.json')
    assert completion['new_credit']==216 and completion['counts']==dict(completed=17749,revised=10828,retained=6921)
    assert (release['registered_manifest_entries'],release['accepted_layers'],release['passing_release_checks'])==(703,114,38)
    assert release['clean_input_patch_byte_exact'] and not release['own_registered_startup_pending']
    for path in (CANDIDATE,INVERSE_PATCH):assert digest(path)==release['candidate_sha256']
    pins=Path('translations/rom_retention_pins.json');before=pins.read_bytes();values=load(pins)
    backup=OUT/'retention_pins_before_registered_checkpoint.json';assert not backup.exists();backup.write_bytes(before)
    for rom in (CANDIDATE,INVERSE_PATCH):
        if not any(Path(v['path']).resolve()==rom.resolve() for v in values):
            values.append(dict(path=str(rom.resolve()),reason='Preserve registered cumulative Hodram B251-B280 candidate and exact clean-input reconstruction. SHA256 '+digest(rom)))
    pending=pins.with_name('rom_retention_pins.Hodram_B251_B280.pending.json');assert not pending.exists()
    save(pending,values);assert pins.read_bytes()==before;os.replace(pending,pins)
    summary=('Hodram B251–B280 is registered and credited once: 216 reviews, 129 revisions and 87 justified retentions. '
        'Thirteen visual wrap changes, one FE warning wrap and two glyph corrections pass; three layout candidates retain originals. '
        'All 212 stored pages pass; representative emulator coverage observes 86 utterances/88 pages and all three menus. '
        'The cumulative candidate passes 703 manifest entries, 114 accepted layers, 38 release checks, exact clean-input reconstruction and its own startup. '
        'Integrated coverage is 17,749. Main is unchanged; continue with a clean, overlap-checked next intake.')
    doc=f'''# Hodram B251–B280 registered checkpoint

{summary}

- [Experimental cumulative ROM](../{CANDIDATE.as_posix()})
- [Manifest](../{Path(release['manifest']).as_posix()})
- [Clean-input patch](../{Path(release['patch']).as_posix()})
- [Registered verification](../{RELEASE.as_posix()})
- [216 integrated decisions and exact references](../translations/hodram_B251_B280_integrated_final_review_v1.json)
- [Five-gate research and honest gameplay scope](../{(ROOT/'research_final_v1/research_completion.json').as_posix()})

Candidate SHA-256: `{release['candidate_sha256']}`. Patch SHA-256: `{release['patch_sha256']}`. Clean Japanese input SHA-256: `{release['clean_input_sha256']}`. Canonical base remains `{release['canonical_base']}`, SHA-256 `{release['canonical_sha256']}`. This experimental candidate preserves all 702 predecessor entries and 114 accepted layers, adds one SC1 transaction/check, and changes only the 30 reviewed SC1 blocks. ARM9, font, artwork, names, other files/components and registered ASCII right bounds remain exact to the predecessor. Eight production rejection cases, complete parent inverse, four-archive format guard and exact clean-input reconstruction pass. The candidate's own 4,001-frame ordinary Rafael startup matches all ten previously viewed captures; both original getters pass for all nine protected actors. Main and the Rafael3222 weekend ZIP are unchanged. All generated ROMs are preserved.

The [previous display/storage checkpoint](editorial_Hodram_B251_B280_stored_20261107.md) records the substantive prose findings, 21 retained source-qualified names, term bindings, 13 wrap refinements, FE36 warning fix and two glyph corrections. All 216 individual gates are now complete. Revised/retained prose and every original reference/reason are preserved; no guide photos are collected.

Offline checks cover all 209 bodies/212 pages, 16 style alternatives, seven captions, 660 relocated branch cases, 209 original catalogue lookups and 325 archive loads/cache hits. Gameplay is one disclosed 26,801-frame cold boot showing 86 source variants/88 pages, 18 of 31 FE bodies, FI/FA substitutions, selectors207/208, both voice objects, both selected two-page passages and all three source-bound menus. Complete masks pass for 184 body holds and 148 name/header holds. All 88 lower-screen pages in eight readable sheets and all three menus were directly viewed. The 123 other speech variants and 13 FE bodies remain offline-only. Menu index0 was observed; other indices/cancellation have offline consumer proofs. Original optional activation, locations, earned chronology, quest effects, full catalogue UI, full routes and hardware are unvisited. Concatenated B252 outcomes are a display test, not original branch routing.

B277 R66 still has a short final continuation, hidden inside. Its original one-page alternatives fail QA. A fresh attempt to keep the whole predicate on page2 also has no passing plan under unchanged guards; evidence is retained at `formatting_v1/actual_boundary_trial_v7/automatic_plans.json`. Keep the complete prose and passing layout rather than claim the tail disappeared. This is a justified retention, not a new correction. No heuristic waiver is used.

The first scene run completed all frames, but its observer stopped after a disk-full RAM-file write; it receives no complete observation credit. All failed artifacts are preserved. The successful v3 observer keeps every boundary memory read/hash/nonmutation check while omitting redundant per-page RAM files; complete compatible native proofs remain bound. Lossless NTFS compression recovered space without deleting/moving ROMs, and every compressed ROM's SHA-256 was checked. The first startup host invocation failed before frames; its folder is preserved. The successful direct harness run uses the established malloc environment. Do not infer a ROM defect or an unproven failure cause from that host exception.

Integrated totals are 17,749: 10,828 revisions and 6,921 justified retentions. Historical source/prose/draft counters are 17,752; the existing difference of three remains. Credit is added exactly once with prior keys, families and record prefixes preserved. No live process remains. Continue the full objective with clean next-scope inventory and overlap checks, without reopening completed checks. Keep Rafael/tutorial priority, every remaining route/shared town/shop/random exchange, unfinished earlier contextual passes, speaker names and player-facing prose in scope. Deferred graphics artwork, the untranslated city alias and later older-record technical re-audit remain separate. No main promotion without user acceptance.
'''
    package=load(PACKAGE)
    checkpoint(mutation=OUT/'registered_documentation_checkpoint_v1',batch_key='editorial_execution_priority_20261104',
        batch_updates=dict(new_credit=0,current_batch='Hodram B251–B280 registered; 216 reviews credited once.',
            next_action='Prepare the next clean complete-exchange intake and reconcile all 17,749 credited source keys.',
            current_batch_not_yet_integrated=False,all_current_batch_fifth_gates_pending=False,
            registered_integration_pending=False,native_job_live=False,registered_build_live=False,
            registered_cumulative_build_live=False,guide_photos=False),
        summary=summary,document='docs/editorial_Hodram_B251_B280_registered_20261107.md',document_text=doc,
        completed=17749,protected={str(REGISTRY):release['registry_sha256'],release['canonical_base']:release['canonical_sha256'],
            release['candidate']:release['candidate_sha256'],release['patch']:release['patch_sha256'],package['zip']:package['zip_sha256']})
    print('Saved registered checkpoint; 17,749 integrated records. Full objective active; main unchanged.')


if __name__=='__main__':main()
