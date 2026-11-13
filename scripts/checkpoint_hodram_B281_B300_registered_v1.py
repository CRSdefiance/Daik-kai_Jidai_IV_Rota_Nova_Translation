"""Preserve registered deliverables and save the verified once-only editorial checkpoint."""
import os
from pathlib import Path
from scripts.audit_story_glyph_consistency import load,save
from scripts.build_registered_hodram_B281_B300_v1 import CANDIDATE,INVERSE_PATCH,RELEASE,REGISTRY,OUT,PARENT_REGISTRY
from scripts.approve_hodram_B281_B300_display_v5 import ROOT
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.save_editorial_progress_checkpoint_v7 import checkpoint
from scripts.save_rafael3222_weekend_checkpoint_v1 import PACKAGE

def main():
    release=load(RELEASE);completion=load(OUT/'completion_checkpoint.json')
    assert completion['new_credit']==384 and completion['counts']==dict(completed=18133,revised=11009,retained=7124)
    assert (release['registered_manifest_entries'],release['accepted_layers'],release['passing_release_checks'])==(704,114,39)
    assert release['clean_input_patch_byte_exact'] and not release['own_registered_startup_pending']
    for path in [CANDIDATE,INVERSE_PATCH]:assert digest(path)==release['candidate_sha256']
    registry,old=map(load,[REGISTRY,PARENT_REGISTRY])
    assert registry['latest_promoted_build']==old['latest_promoted_build'] and registry['accepted_layers']==old['accepted_layers']
    pins=Path('translations/rom_retention_pins.json');before=pins.read_bytes();values=load(pins)
    backup=OUT/'retention_pins_before_registered_checkpoint.json';assert not backup.exists();backup.write_bytes(before)
    for rom in [CANDIDATE,INVERSE_PATCH]:
        if not any(Path(v['path']).resolve()==rom.resolve() for v in values):
            values.append(dict(path=str(rom.resolve()),reason='Preserve registered cumulative Hodram B281-B300 and exact clean-input reconstruction. SHA256 '+digest(rom)))
    pending=pins.with_name('rom_retention_pins.Hodram_B281_B300.pending.json');assert not pending.exists()
    save(pending,values);assert pins.read_bytes()==before;os.replace(pending,pins)
    summary=('Hodram B281–B300 is registered and credited once: 384 reviews, 181 revisions and 203 justified retentions. '
        'Twenty-eight wraps, one native FE blank row and five punctuation glyph targets are corrected; two layouts retain the better originals. '
        'All 374 stored pages pass; representative emulator coverage observes 134 utterances/135 pages and all five menus. '
        'The cumulative candidate passes 704 manifest entries, 114 accepted layers, 39 release checks, exact clean-input reconstruction and its own startup. '
        'Integrated coverage is 18,133. Main is unchanged. Continue with a clean, overlap-checked next intake.')
    document=f'''# Hodram B281–B300 registered checkpoint

{summary}

- [Experimental cumulative ROM](../{CANDIDATE.as_posix()})
- [Manifest](../{Path(release['manifest']).as_posix()})
- [Clean-input patch](../{Path(release['patch']).as_posix()})
- [Registered verification](../{RELEASE.as_posix()})
- [384 integrated decisions with exact references](../translations/hodram_B281_B300_integrated_final_review_v1.json)
- [Research gates and gameplay scope](../{(ROOT/'research_final_v1/research_completion.json').as_posix()})

Candidate SHA-256: `{release['candidate_sha256']}`. Patch SHA-256: `{release['patch_sha256']}`. Clean Japanese input SHA-256: `{release['clean_input_sha256']}`. Canonical base remains `{release['canonical_base']}`, SHA-256 `{release['canonical_sha256']}`. The candidate preserves all 703 predecessor entries, all 114 accepted layers and the registered ASCII right-bound correction. Only the 20 reviewed SC1 blocks change. ARM9, names, font, artwork, all other files/components and every previous profile remain exact. Eight production rejection cases, complete parent inverse, all four story archive format guards and exact clean-input patch reconstruction pass. Its own 4,001-frame Rafael startup matches all ten previously viewed captures; both original getters verify all nine protected actors. The promoted main and weekend ZIP remain unchanged.

The [display/storage checkpoint](editorial_Hodram_B281_B300_stored_20261107.md) records the contextual findings, 18 retained source-qualified actors, term bindings, 28 wrap improvements, two justified layout retentions, the actual FE blank-row correction and five glyph fixes. All 384 individual gates now pass. No prose was shortened or manually wrapped; no QA waiver was used. All earlier translations, retentions, source/current references, failed trials and ROMs remain preserved.

Offline checks cover all 373 bodies/374 pages, all 131 physical voice alternatives/144 slots, 11 captions, 1,415 branch cases, 373 original catalogue lookups and 325 archive loads/cache hits. Eleven changed voice objects receive fresh native slot checks; seven exact objects reuse compatible proofs. Every initial and revised page and every name/menu sheet was directly viewed.

The disclosed 38,561-frame emulator sequence observes 134 variants/135 pages, 12 of 16 FE bodies, seven complete voice objects, FI/FA substitutions, dynamic source selectors207/208/211/215, all five menu occurrences, the royal continuation, one-page map response, gunpowder exchange/countdown and bog rescue. All 278 complete body and 254 header holds match native glyph planes and blank guards. All 135 lower-screen pages on 12 readable sheets and all five menus were directly viewed. Menu index0 was observed; other indices and cancellation retain separate offline proofs. The other239 speech variants and four FE bodies are offline-only. Original optional activation, locations, earned chronology, quest effects, full catalogue UI, complete routes and hardware remain unvisited. Concatenated optional/outcome commands test display and transitions, not original branch routing or party membership.

The first focused run stopped before emulator frames because its legacy capture junction was outside the writable workspace. Its plan is preserved. The successful run uses a workspace capture directory and the unchanged read-only observer. The registered successor startup uses a clean emulator subprocess, followed by the original RGB, current RAM/payload and getter verifiers. The first completion attempt stopped before any ledger mutation at one stale intake-status field; `completion_flag_binding_v2.json` binds its resolution to the completed source/current, scoped-name and five-gate evidence while preserving the research manuscript. Original event activation is still unvisited. Lossless NTFS compression preserved all logical ROM bytes and paths, with SHA-256 verification in `lossless_space_recovery_v1.json`; nothing was deleted or moved. These host/storage steps grant no extra gameplay or dialogue credit.

Integrated totals are18,133:11,009 revisions and7,124 justified retentions. Historical source/prose/draft counters are18,136; the existing difference of three remains. Credit is added once, preserving every earlier ledger family and record prefix. No process remains live. Continue with the clean remaining Hodram B301–B324 scope, checking actual inventory, neighboring conversation boundaries and overlap before choosing its batch. Do not assume all 24 blocks require edits or review credit. Preserve the full objective: all routes, shared town/shop/random exchanges, unfinished earlier contextual passes, speaker names and remaining player-facing prose, with Rafael/tutorial priority. Deferred graphics artwork and the later older-record technical re-audit stay separate. No guide photos or main promotion.
'''
    package=load(PACKAGE)
    checkpoint(mutation=OUT/'registered_documentation_checkpoint_v1',batch_key='editorial_execution_priority_20261104',
        batch_updates=dict(new_credit=0,current_batch='Hodram B281–B300 registered;384 disjoint reviews credited once.',
            next_action='Inventory clean remaining Hodram B301–B324, check neighboring context and reconcile all18,133 credited source keys.',
            current_batch_not_yet_integrated=False,all_current_batch_fifth_gates_pending=False,registered_integration_pending=False,
            native_job_live=False,registered_build_live=False,registered_cumulative_build_live=False,guide_photos=False),
        summary=summary,document='docs/editorial_Hodram_B281_B300_registered_20261107.md',document_text=document,completed=18133,
        protected={str(REGISTRY):release['registry_sha256'],release['canonical_base']:release['canonical_sha256'],
            release['candidate']:release['candidate_sha256'],release['patch']:release['patch_sha256'],package['zip']:package['zip_sha256']})
    save(OUT/'final_checkpoint_audit_v1.json',dict(release=str(RELEASE),release_sha256=digest(RELEASE),
        ledger_sha256=digest('translations/editorial_review_current_v1.json'),main_andaccepted_layers_exact_to_predecessor=True,
        counts=completion['counts'],all_prior_progress_andROMs_preserved=True,full_goal_complete=False,
        next_action='Clean source-first inventory and overlap check for the remaining Hodram tail.',new_credit=0))
    print('Saved registered checkpoint;18,133 integrated records. Full objective active; main unchanged.')

if __name__=='__main__':main()
