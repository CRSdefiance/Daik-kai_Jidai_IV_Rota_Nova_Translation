"""Publish the checked cumulative B50 release and preserve the next clean-first batch."""
import os
from pathlib import Path
from scripts.audit_story_glyph_consistency import load,save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.save_editorial_progress_checkpoint_v9 import checkpoint

ROOT=Path('work/maria_B50_release_v1')
NEXT=Path('work/Maria_B51_B57_clean_20261109')

def main():
    release=load(ROOT/'registered_release_verification.json');done=load(ROOT/'completion_checkpoint.json')
    census_path=Path('work/story_source_coverage_20261109_SC3_v4/coverage.json');census=load(census_path)
    assert done['new_credit']==16 and done['counts']==dict(completed=19748,revised=11880,retained=7868)
    assert (release['registered_manifest_entries'],release['accepted_layers'],release['passing_release_checks'])==(712,114,47)
    assert not release['own_registered_startup_pending'] and release['registered_market_format_andboth_data_pointers_preserved']
    assert release['source_owned_FE_continuation_andfull139_character_paragraph_preserved']
    assert len(census['missing'])==4345 and not census['inventory_failures'] and not census['legacy_source_bindings_not_exact']
    assert digest('translations/release_stack.json')==release['registry_sha256']
    drafts=load(NEXT/'B51_B52_independent_drafts_v1.json');packet=load(NEXT/'clean_source_packet.json')
    assert drafts['source_objects']==28 and drafts['current_English_not_consulted'] and packet['records']==310
    previous_packet=load('work/story_source_coverage_20261109_SC3_v4/residual_clean_source_packet.json')
    fresh={g['block']:g for g in previous_packet['groups'] if 51<=g['block']<=57}
    assert len(fresh)==7
    for group in packet['groups']:
        assert group['clean_block_hex']==fresh[group['block']]['clean_block_hex']
        assert [(r['id'],r['source_reference'],r['source_hex']) for r in group['records']]==[
            (r['id'],r['source_reference'],r['source_hex']) for r in fresh[group['block']]['records']]
        assert all(not r['covered'] and not r['exact_credited_source_bindings'] for r in fresh[group['block']]['records'])
    save(NEXT/'registered_parent_and_disjointness_v1.json',dict(registered_candidate=release['candidate'],
        registered_candidate_sha256=release['candidate_sha256'],source_objects=310,complete_exchanges=7,
        all310_still_missing_in_post_B50_exact_source_census=True,current_English_not_consulted=True,
        evidence={str(p):digest(p) for p in [census_path,NEXT/'clean_source_packet.json',NEXT/'B51_B52_independent_drafts_v1.json']},new_credit=0))
    pins_path=Path('translations/rom_retention_pins.json');before=pins_path.read_bytes();pins=load(pins_path)
    for value in [release['candidate'],release['exact_clean_reconstruction']]:
        path=Path(value);assert digest(path)==release['candidate_sha256']
        assert not any(Path(r['path']).resolve()==path.resolve() for r in pins)
        pins.append(dict(path=str(path.resolve()),reason='Preserve registered Maria B50 cumulative candidate/exact clean-input reconstruction. SHA256 '+release['candidate_sha256']))
    (ROOT/'retention_pins.before.json').write_bytes(before)
    pending=pins_path.with_name('rom_retention_pins.Maria_B50_registered.pending.json');assert not pending.exists()
    save(pending,pins);assert pins_path.read_bytes()==before;os.replace(pending,pins_path)
    save(ROOT/'retention_registration_v1.json',dict(candidate_sha256=release['candidate_sha256'],
        pinned_ROMs=[release['candidate'],release['exact_clean_reconstruction']],no_deletions=True,pins_sha256=digest(pins_path)))
    continuity=Path('docs/build_continuity_protocol.md');old=continuity.read_bytes()
    prefix='''Maria B50 uses `scripts/build_registered_maria_B50_v1.py` over the exact registered
Maria270 output. Its reviewed FE stage reuses the qualified source-owned native
continuation helper: 16 source reviews become 17 native panels, with exactly one
additional six-byte FE preamble under B50 R43. Preserve all 139 paragraph characters;
the ordinary paragraph space becomes a native page boundary. B50 has no relative
branch sites. Require complete source/current blocks, archive and serialized NDS
inverses, all 17 stored/effective bodies and native bounds, guarded alignment cases,
303 loads/606 handoffs, actual A/page/next-source transition and all generated-page
visual approvals. No renderer, viewport, font or prose shortening is authorized by
this scope. Retain the exact 711-entry predecessor, 114 accepted layers, market
autoload literal/pointers, six-section ARM9, ASCII right-bound correction and v2
multi-archive source25 guard. Require the byte-exact clean-input patch, candidate's
own Maria/Hangzhou startup and both getters for all 12 protected names before
registration/credit. The registered successor has 712 entries and 47 release checks.
Count 16 source reviews once, never 17 for the child panel. Main requires acceptance.
The preceding B50-held statements below are preserved history, now resolved.

'''
    (ROOT/'build_continuity.before.md').write_bytes(old)
    pending=continuity.with_name('build_continuity_protocol.Maria_B50.pending.md');assert not pending.exists()
    pending.write_bytes(prefix.encode('utf-8')+old);assert continuity.read_bytes()==old;os.replace(pending,continuity)
    save(ROOT/'build_continuity_update_v1.json',dict(before_sha256=digest(ROOT/'build_continuity.before.md'),
        after_sha256=digest(continuity),complete_old_document_preserved_as_suffix=True))
    summary=('Maria B50 is registered and credited once: 16 reviews/9 revisions/7 retentions, 17 directly viewed native panels, '
        'two wrap improvements, one blank-row repair and an exact-source FE continuation preserve the full paragraph. '
        'The cumulative candidate passes 47 checks with 712 entries/114 accepted layers, exact clean-input reconstruction, '
        'own startup and 24 protected getters; market/ASCII right-bound fixes remain exact. Integrated totals are 19,748; '
        '6,150 native story objects remain. Next B51–B57 has 310 disjoint clean objects; first28 meanings and independent '
        'drafts are sealed, all current comparisons/five gates remain pending. Main and full scope are unchanged.')
    text=f'''# Maria B50 registered checkpoint — November 9, 2026

**16 contextual source reviews are integrated exactly once: nine revisions and seven justified retentions.** All five individual gates pass. The full 139-character conditional paragraph is preserved with an exact-source native FE page continuation; the body now has 17 physical commands/panels without 17 source credits. A blank row and two awkward wraps are corrected, including continuity of “admiral like you.” No prose shortening or renderer/font/viewport change was needed.

Candidate: [all_routes_maria_B50_candidate.nds](../{release['candidate'].replace(chr(92),'/')}), SHA-256 `{release['candidate_sha256']}`.
Clean-input patch: [all_routes_maria_B50_candidate.xdelta](../{release['patch'].replace(chr(92),'/')}), SHA-256 `{release['patch_sha256']}`.
Manifest: `{release['manifest']}`, SHA-256 `{release['manifest_sha256']}`.
Registry SHA-256: `{release['registry_sha256']}`. Profile: `{release['profile']}`.

This cumulative test candidate retains all 711 preceding entries, all 114 accepted layers, the Trade/Goods Info terminator correction, ASCII right-bound fix and approved name/glyph work. Only SC3 B50 changes; ARM9, other internal files/components, artwork and names remain exact to registered Maria270. The complete source/current block, archive and serialized parent inverses pass. The clean-input patch reconstructs the whole candidate exactly from clean SHA-256 `{release['clean_input_sha256']}`. The new entry is712 and the release check is47. The v2 multi-archive source25 guard and all seven source-leading controls remain exact.

Reuse [the completed B50 research](editorial_Maria_B50_FE_research_20261109.md); do not redo its checks. All17 stored/effective bodies and final pages, eight fresh parity-dependent pages plus nine exact reused pages, 68 selected alignment cases, all17 catalogue bindings, 303 full loads/cache hits and606 parent handoffs pass. There are zero native relative branch sites in this block. Seven malformed FE insertions and eight malformed registered-transaction scopes reject. Every final body page and selected gameplay panel was directly viewed. The whole original paragraph stays one source-owned review while its native page child repeats only the exact source FE preamble.

The actual initialized display fixture observes all16 utterances/17 panels in13,001 frames: first R43 page at6185, A6400, second page6425, A6640 and next source R46 at6665, followed by resupply, departure and sailing. Eight complete headers were sampled. The candidate itself passes its own31,000-frame title/New Game/Maria opening/Hangzhou coldboot, six directly viewed captures, complete payload/RAM guards, captain3/route3 and both original getters for12 protected actors. These are emulator checks using the disclosed existing system-only unlock, not earned progression. B50's original cutscene activation, artwork/effects, conditional outcomes, full catalogue UI and hardware remain unvisited; the fixture does not claim a natural playthrough.

`translations/maria_B50_integrated_final_review_v1.json` and `exact_integrated_record_bindings.json` bind every reviewed source to its registered reference. R43 records both native page references. The ledger completion receipt proves once-only credit and exact unrelated keys/earlier record prefixes. All5129 clean SC3 source positions were rechecked:784 covered,4345 remaining, with no duplicate or legacy-binding failures. Earlier286 meaning/draft/source work is preserved and now all286 is integrated through separate270+16 credits. Historical held and failed producers remain evidence.

Integrated totals: **19,748 =11,880 revisions +7,868 retentions**. Native story objects remaining: **6,150 =Lil1,805 +Maria4,345**. Shared town/shop/random/UI and other prose remain separately tracked. The historical meaning/prose/draft counter is19,751; the extra three historical counts do not add integrated credit. All ROMs, earlier translations, evidence and prior registry profiles are preserved; the new candidate and clean reconstruction are pinned. Main `all-routes-unified-v4701` and the canonical baseline are unchanged. No promotion or Git push occurred.

**Continue with the seven complete B51–B57 source exchanges:310 disjoint objects.** `work/Maria_B51_B57_clean_20261109/clean_source_packet.json` binds every selected source position. Post-integration census reconciliation confirms all310 are still uncredited. The complete B51/B52 clean meanings and28 independent logical drafts are sealed before current-English comparison. Richard's colonial claims remain his own, Maria's assessments stay inferences, no attacker/weapon/rank/kinship is invented, and both town FA substitutions remain runtime values. These drafts supply no completed gates or review credit. The other282 meanings/drafts, all310 current comparisons, scoped names/roles, fresh display/storage/visual checks and representative gameplay remain pending. Do not restart the registered B50 checks. All unfinished storylines, earlier contextual passes, shared town/shop/random dialogue, names, wraps/glyphs and other prose remain in scope. Graphics artwork and the later older-record technical re-audit stay separate. No guide photos or live worker at this checkpoint.
'''
    testing=ROOT/'testing_handoff.md';assert not testing.exists()
    testing.write_text(f'''# Translation DS testing candidate

[ROM](all_routes_maria_B50_candidate.nds) · [manifest](all_routes_maria_B50_candidate.manifest.json) · [clean-input patch](all_routes_maria_B50_candidate.xdelta)

SHA-256 `{release['candidate_sha256']}`. Registered cumulative test candidate; main remains unchanged. Includes the Rafael2952 Trade/Goods Info repair, all earlier reviewed content and the completed Maria B50 dialogue/wrapping fix. Use a copy of your existing save with the new ROM basename and preserve the original save.

Clean-input reconstruction, native checks and representative emulator/startup checks pass. Hardware and naturally earned late source conditions remain unvisited. [Full evidence and continuation](../../docs/editorial_Maria_B50_registered_20261109.md).
''',encoding='utf-8',newline='\n')
    checkpoint(mutation=ROOT/'registered_progress_checkpoint_v1',batch_key='editorial_execution_priority_20261104',
        batch_updates=dict(new_credit=0,current_batch='Maria B51–B57 clean-first310;B50 fully registered.',
            current_batch_not_yet_integrated=True,all_current_batch_fifth_gates_pending=True,
            native_job_live=False,registered_build_live=False,guide_photos=False,
            next_action='Finish remaining282 clean meanings andindependent drafts,thencompare all310 current records as whole exchanges;fresh formatting follows.'),
        additional_updates={'Maria_SC3_B37_B50_clean_20261109':dict(new_credit=0,
            integrated_complete_exchange_subset=286,integrated_split_families=['Maria_SC3_B37_B49_contextual_integrated_20261109',done['family']],
            subset_registered_candidate=release['candidate'],subset_registered_candidate_sha256=release['candidate_sha256'],
            withheld_complete_exchange=None,withheld_records=0,registered_integration_pending=False,
            all_five_gates_pending=False,all_fifth_formatting_gates_pending=False,
            final_cumulative_integration_complete=True)},
        new_entries={'Maria_SC3_B51_B57_clean_20261109':dict(new_credit=0,source_objects=310,complete_exchanges=7,
            source_packet=str(NEXT/'clean_source_packet.json'),source_packet_sha256=digest(NEXT/'clean_source_packet.json'),
            clean_meanings_completed=28,independent_logical_drafts=28,current_comparisons=0,
            all_five_review_gates_pending=True,registered_integration_pending=True,
            current_English_not_consulted=True,current_registered_parent=release['candidate'],
            current_registered_parent_sha256=release['candidate_sha256'],
            source_progress=[str(NEXT/'B51_B52_clean_meanings_v1.json'),str(NEXT/'B51_B52_independent_drafts_v1.json')])},
        summary=summary,document='docs/editorial_Maria_B50_registered_20261109.md',document_text=text,completed=19748,
        protected={'translations/release_stack.json':release['registry_sha256'],release['candidate']:release['candidate_sha256'],
            release['manifest']:release['manifest_sha256'],release['patch']:release['patch_sha256'],
            release['canonical_base']:release['canonical_sha256'],str(continuity):digest(continuity)})
    print('Saved registered B50 checkpoint:19,748 integrated/6,150 native story objects remain;next310 active;main unchanged.')
if __name__=='__main__':main()
