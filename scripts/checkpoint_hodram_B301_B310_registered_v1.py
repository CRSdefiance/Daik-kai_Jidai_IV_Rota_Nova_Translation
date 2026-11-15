"""Save registered deliverables, conserved credit and the overlap-checked remaining tail."""
import os
from pathlib import Path
from scripts.audit_story_glyph_consistency import load,save
from scripts.build_registered_hodram_B301_B310_v1 import CANDIDATE,INVERSE_PATCH,RELEASE,REGISTRY,OUT,PARENT_REGISTRY
from scripts.approve_hodram_B301_B310_display_v6 import ROOT
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.save_editorial_progress_checkpoint_v7 import checkpoint
from scripts.save_rafael3222_weekend_checkpoint_v1 import PACKAGE

def main():
    release=load(RELEASE);completion=load(OUT/'completion_checkpoint.json')
    assert completion['new_credit']==234 and completion['counts']==dict(completed=18367,revised=11136,retained=7231)
    assert (release['registered_manifest_entries'],release['accepted_layers'],release['passing_release_checks'])==(705,114,40)
    assert release['clean_input_patch_byte_exact'] and not release['own_registered_startup_pending']
    for path in [CANDIDATE,INVERSE_PATCH]:assert digest(path)==release['candidate_sha256']
    registry,old=map(load,[REGISTRY,PARENT_REGISTRY])
    assert registry['latest_promoted_build']==old['latest_promoted_build'] and registry['accepted_layers']==old['accepted_layers']
    assert all(registry['profiles'][k]==v for k,v in old['profiles'].items())
    assert set(registry['profiles'])-set(old['profiles'])=={release['profile']}
    pins=Path('translations/rom_retention_pins.json');before=pins.read_bytes();values=load(pins)
    backup=OUT/'retention_pins_before_registered_checkpoint.json';assert not backup.exists();backup.write_bytes(before)
    for rom in [CANDIDATE,INVERSE_PATCH]:
        if not any(Path(v['path']).resolve()==rom.resolve() for v in values):
            values.append(dict(path=str(rom.resolve()),reason='Preserve registered cumulative Hodram B301-B310 and exact clean-input reconstruction. SHA256 '+digest(rom)))
    pending=pins.with_name('rom_retention_pins.Hodram_B301_B310.pending.json');assert not pending.exists()
    save(pending,values);assert pins.read_bytes()==before;os.replace(pending,pins)
    nextroot=Path('work/Hodram_B311_B324_clean_20261107')
    packet,styles,choices,scope=map(load,[nextroot/'clean_source_packet.json',nextroot/'clean_style_objects.json',nextroot/'clean_choice_objects.json',nextroot/'clean_intake_scope_v1.json'])
    rows=[r for g in packet['groups'] for r in g['records']]+styles['records']+choices['records']
    keys={(r['file_path'],r['id']) for r in rows}
    ledgerpath=Path('translations/editorial_review_current_v1.json');ledger=load(ledgerpath)
    credited={(r['file_path'],r['id']) for r in ledger['contextual_story_natural_dialogue_pass_v1871']['record_keys']}
    assert len(credited)==ledger['records_editorially_completed']==18367 and len(keys)==len(rows)==400 and not keys&credited
    assert (scope['ordinary_speeches'],scope['physical_personality_alternatives'],scope['typed_caption_records'],scope['physical_style_objects'],scope['typed_choice_objects'])==(151,236,13,38,6)
    assert scope['reviewed_block_numbers']==list(range(311,325)) and not scope['control_only_blocks']
    assert ledger['Hodram_B301_B310_clean_next_20261107']['long_QA_return_risk_unresolved'] is False
    reconciled=nextroot/'credited_reconciliation_after_B301_B310_v1.json';assert not reconciled.exists()
    save(reconciled,dict(eligible_next_objects=400,ordinary_speeches=151,physical_voice_alternatives=236,typed_captions=13,
        all18367_current_credited_keys_checked=True,credited_overlap=0,original_intake_epoch_completed_keys=scope['all_completed_exclusion_keys_checked'],
        source_meanings_drafts_comparisons_andall_five_gates_still_pending=True,no_new_current_English_dialogue_extracted=True,
        source_only_boundary_read_of_B311_does_not_grant_review_credit=True,new_credit=0,
        evidence={str(p):digest(p) for p in [ledgerpath,nextroot/'clean_source_packet.json',nextroot/'clean_style_objects.json',nextroot/'clean_choice_objects.json',nextroot/'clean_intake_scope_v1.json']}))
    summary=('Hodram B301–B310 is registered and credited once:234 reviews,127 revisions and107 justified retentions. '
        'Eighteen layouts, one native FE split word and one glyph target improve; one better layout is retained. '
        'All228 stored pages pass; two bounded emulator runs observe96 utterances/97 pages andfour menus, with both returns verified. '
        'The cumulative candidate passes705 manifest entries,114 accepted layers,40 release checks, exact clean-input reconstruction and its own startup. '
        'Integrated coverage is18,367. Main is unchanged. Next:400 clean, disjoint B311–B324 objects; meanings/drafts/comparisons remain.')
    document=f'''# Hodram B301–B310 registered checkpoint

{summary}

- [Experimental cumulative ROM](../{CANDIDATE.as_posix()})
- [Manifest](../{Path(release['manifest']).as_posix()})
- [Clean-input patch](../{Path(release['patch']).as_posix()})
- [Registered verification](../{RELEASE.as_posix()})
- [234 integrated decisions and exact source/current references](../translations/hodram_B301_B310_integrated_final_review_v1.json)
- [Research gates and actual/offline scope](../{(ROOT/'research_final_v1/research_completion.json').as_posix()})

Candidate SHA-256: `{release['candidate_sha256']}`. Patch SHA-256: `{release['patch_sha256']}`. Clean Japanese input SHA-256: `{release['clean_input_sha256']}`. Canonical base remains `{release['canonical_base']}`, SHA-256 `{release['canonical_sha256']}`. All704 predecessor entries,114 accepted layers and the ASCII right-bound correction remain. Only ten reviewed SC1 blocks301–310 change. ARM9, font, names, artwork, all other files/components and previous profiles are exact. Eight malformed-input rejection cases, whole parent inverse, all four story-archive format guards and byte-exact clean-input reconstruction pass. The candidate's own4,001-frame Rafael startup matches all ten previously reviewed captures; both original getters verify nine protected actors. Main and the weekend ZIP are unchanged.

The [contextual checkpoint](editorial_Hodram_B301_B310_contextual_20261107.md) contains the source findings: invented water-shortage/hours/departure details, wrong mosque/vault claims, two untranslated monk turns, corrected far-northeast-of-China directions, vocalized breath sounds and the discreet offer. All234 individual gates now pass;127 prose revisions and107 retentions retain their individual reasons. The [offline checkpoint](editorial_Hodram_B301_B310_stored_20261107.md) supplies eight justified name retentions, scoped terms,18 layout improvements, one justified layout retention, the repaired appear split and ASCII silence punctuation. No prose is shortened or manually wrapped and no QA waiver is used.

Offline checks cover225 bodies/228 pages,152 physical voice alternatives/184 slots in23 objects, nine captions in four menus,190 relocated branch cases,225 complete native catalogue lookups and325 archive loads/cache hits. Five changed voice objects receive fresh target-slot checks;18 byte-identical objects reuse qualified proofs. All initial and changed pages and scoped name/menu sheets were directly viewed. The eight scoped name decisions and16 original getters remain separate from the wider207-entry name review and unvisited full-catalogue UI.

The [bounded gameplay join](../work/Hodram_B301_B310_clean_20261107/bounded_combined_v1/bounded_return_checks.json) covers two independent initialized sequences/34,162 frames. They preserve all100 planned native commands,96 utterances/97 pages and all four menus. All210 complete body holds and194 header holds match native planes and blank guards. All97 actual pages on nine readable sheets, the menu sheet and both final return screens were directly viewed. All eight FE notices, captain FI injury,23 complete voice commands at original startup assignments, Senior Monk/Mihwa headers, Kinkaku-ji, wolf treatment and the two-page offer are observed. Menu index0 is observed; nondefault/cancel behavior retains distinct offline proofs. The other129 physical voice variants remain offline-only. Frame numbers remain local to each run. These samples do not activate original optional scenes, branches, party assignments, rewards or chronology, or establish full-route/hardware coverage.

The prior [return-risk checkpoint](editorial_Hodram_B301_B310_gameplay_risk_20261107.md) is superseded by the [source/RAM capacity proof](../work/Hodram_B301_B310_clean_20261107/native_QA_capacity_v1.json) and [bounded return approval](../work/Hodram_B301_B310_clean_20261107/fixture_exit_resolution_bounded_v1.json). The artificial10,540-byte B42 sequence overflowed the original native stack frame; runtime RAM contains its prose over all nine saved caller-register words, including saved LR. Trace proves the cleanup and exit commands were reached. Cleanup/end-operand changes did not remove this overflow and are preserved as failed tests. All ten production target blocks are at most3,276 bytes. A conservative9,216-byte QA-block guard rejects the known oversized fixture before any ROM write; complete-block splitting produces6,140/4,448-byte fixtures, and both return to the following native resupply dialogue without undefined instructions. Production scene controls, engine and font are not altered by this QA repair. Preserve all failed experiments; do not repeat the disproven terminal-operand theory or restart completed editorial/display checks.

There were seven initialized QA runs/156,887 total frames including the preserved failed/diagnostic experiments; the qualified representative scope is the two passing bounded runs above. The separate three-utterance/four-page Mihwa test also passes its return. These are repeated evidence for96 unique observed variants, not additional dialogue credit. Read-only native observers preserve CPU/RAM/TCM and restore host filters; registered startup uses a clean subprocess. In-place NTFS compression preserves every ROM path and logical SHA-256. No ROM is deleted or moved. All earlier translations, retentions, evidence and generated ROMs remain.

Integrated totals are18,367:11,136 revisions and7,231 justified retentions. Historical source/prose/draft counters are18,370, preserving the earlier difference of three. Once-only credit preserves every prior family and record prefix. No process remains live. The [next source-only scope](../work/Hodram_B311_B324_clean_20261107/clean_intake_scope_v1.json) contains400 disjoint objects across14 complete blocks:151 ordinary speeches,236 physical alternatives/304 slots in38 objects and13 captions in six menus. [Fresh reconciliation](../work/Hodram_B311_B324_clean_20261107/credited_reconciliation_after_B301_B310_v1.json) checks all18,367 credited keys with no overlap. All next meanings, localized drafts, current-English comparisons, scoped names and display gates remain. The old B311 boundary-only Japanese read grants no credit. Begin clean source and whole-exchange meanings; do not consult eligible current English before meanings and drafts are sealed.

The full objective stays active across all storylines, unfinished earlier contextual passes, shared town/shop/random dialogue, names and remaining player-facing prose, with Rafael/tutorial priority. Unresolved graphics artwork and the later older-record technical re-audit remain separate. No guide photos or main promotion.
'''
    package=load(PACKAGE)
    checkpoint(mutation=OUT/'registered_documentation_checkpoint_v1',batch_key='editorial_execution_priority_20261104',
        batch_updates=dict(new_credit=0,current_batch='Hodram B301–B310 registered;234 disjoint reviews credited once. Next400 B311–B324 objects are source-only.',
            next_action='Read complete clean B311–B324 exchanges; save400 meanings and natural logical drafts before eligible current-English comparison. Reuse resolved native QA capacity guard and all completed proofs.',
            current_batch_not_yet_integrated=False,all_current_batch_fifth_gates_pending=False,registered_integration_pending=False,
            native_job_live=False,registered_build_live=False,registered_cumulative_build_live=False,guide_photos=False),
        new_entries={'Hodram_B311_B324_clean_next_20261107':dict(new_credit=0,total_editorial_objects=400,ordinary_speeches=151,
            physical_personality_alternatives=236,physical_style_objects=38,personality_alias_slots=304,typed_caption_records=13,typed_choice_objects=6,
            clean_source_scope=str(nextroot/'clean_intake_scope_v1.json'),source_meanings_saved=0,localized_drafts_saved=0,current_English_comparisons=0,
            source_meanings_pending=True,localized_drafts_pending=True,all_five_review_gates_pending=True,scoped_names_pending=True,
            fresh_native_body_pages_pending=True,stored_reconstruction_pending=True,representative_gameplay_pending=True,registered_integration_pending=True,
            all18367_completed_keys_checked=True,source_key_overlap_with_completed_credit=0,no_current_English_dialogue_extracted=True,
            reconciliation=str(reconciled),reconciliation_sha256=digest(reconciled),native_job_live=False,registered_build_live=False)},
        summary=summary,document='docs/editorial_Hodram_B301_B310_registered_20261107.md',document_text=document,completed=18367,
        protected={str(REGISTRY):release['registry_sha256'],release['canonical_base']:release['canonical_sha256'],
            release['candidate']:release['candidate_sha256'],release['patch']:release['patch_sha256'],package['zip']:package['zip_sha256']})
    save(OUT/'final_checkpoint_audit_v1.json',dict(release=str(RELEASE),release_sha256=digest(RELEASE),
        ledger_sha256=digest(ledgerpath),main_accepted_layers_andall_prior_profiles_exact=True,counts=completion['counts'],
        next400_keys_disjoint=True,all_prior_progress_translations_evidence_andROMs_preserved=True,full_goal_complete=False,
        next_action='Clean-source meanings and drafts for B311–B324; no restart of completed proofs.',new_credit=0))
    print('Saved registered checkpoint;18,367 integrated records and400 source-only next objects. Full objective active; main unchanged.')

if __name__=='__main__':main()
