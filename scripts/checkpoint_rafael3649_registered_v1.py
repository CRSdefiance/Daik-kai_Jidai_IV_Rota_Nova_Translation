"""Save the registered handoff and the next clean-only Rafael intake."""
from pathlib import Path
import os

from scripts.audit_story_glyph_consistency import load, save
from scripts.build_registered_rafael3649_v1 import CANDIDATE, INVERSE_PATCH, PARENT_REGISTRY, RELEASE
from scripts.checkpoint_rafael_B168_B169_research_v1 import link
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.save_editorial_progress_checkpoint_v6 import checkpoint
from scripts.save_rafael3222_weekend_checkpoint_v1 import LEDGER, PACKAGE
from scripts.seal_rafael_B281_B286_clean_v1 import OUTPUT, PACKET, ROOT, STYLES, MENUS


NEXT = 'Rafael_SC0_B281_B300_clean_20261106'
PRIOR_BATCH = 'Rafael_SC0_B261_B280_clean_20261106'
INTEGRATED = Path('translations/rafael_B261_B280_integrated_final_review_v1.json')
REGISTRY = Path('translations/release_stack.json')
PINS = Path('translations/rom_retention_pins.json')


def pin_release():
    before = PINS.read_bytes()
    pins = load(PINS)
    existing = {Path(row['path']).resolve() for row in pins}
    rows = (
        (CANDIDATE, 'Registered experimental Rafael3649, exact cumulative editorial successor.'),
        (INVERSE_PATCH, 'Exact reconstruction of Rafael3649 from the clean Japanese input and registered patch.'),
    )
    additions = [dict(path=str(path.resolve()), reason=f'{reason} SHA-256 {digest(path)}')
                 for path, reason in rows if path.resolve() not in existing]
    if additions:
        pending = PINS.with_name('rom_retention_pins.Rafael3649.pending.json')
        assert not pending.exists()
        save(pending, pins + additions)
        assert PINS.read_bytes() == before
        os.replace(pending, PINS)
        assert load(PINS) == pins + additions


def main():
    release, ledger, package, packet, styles, menus, first = map(load, (RELEASE, LEDGER, PACKAGE, PACKET, STYLES, MENUS, OUTPUT))
    assert ledger[PRIOR_BATCH]['new_credit'] == ledger[PRIOR_BATCH]['completion_credit_added'] == 135
    assert ledger['records_editorially_completed'] == 15494
    assert ledger['current_integrated_candidate']['sha256'] == release['candidate_sha256']
    assert release['all_nine_registered_final_stages_preserved'] and release['owned_Plett_Jacob_surnames_verified']
    assert release['clean_input_patch_byte_exact'] and not release['own_registered_startup_pending']
    assert load(REGISTRY)['latest_promoted_build'] == load(PARENT_REGISTRY)['latest_promoted_build']
    assert packet['clean_only_no_prior_English_ornew_editorial_credit']
    assert styles['source_packet_sha256'] == menus['source_packet_sha256'] == digest(PACKET)
    assert [group['block'] for group in packet['groups']] == list(range(281, 301))
    ordinary = [row for group in packet['groups'] for row in group['records']]
    source = ordinary + styles['records'] + menus['records']
    assert (len(ordinary), len(styles['records']), len(menus['records']), len(source)) == (164, 76, 5, 245)
    key = lambda row: (row['file_path'], row['id'])
    assert len(set(map(key, source))) == 245
    integrated = ledger['contextual_story_natural_dialogue_pass_v1871']['integrated_record_keys']
    assert set(map(key, source)).isdisjoint(map(key, integrated))
    assert first['records_count'] == 32 and first['complete_blocks'] == list(range(281, 287))
    assert first['no_current_English_extracted_for_this_intake_before_drafts']
    assert all(digest(path) == checksum for path, checksum in first['evidence'].items())
    summary = (
        'Rafael B261–B280 is registered in Rafael3649 and credited once, with 118 revisions and 17 justified retentions. '
        'The candidate preserves the nine prior final stages and adds both surname corrections. The exact clean-input patch, '
        '4001-frame startup and own name getters passed. Integrated coverage is 15,494. The next clean intake has 245 objects and 32 drafts.'
    )
    doc = f"""# Rafael B261–B280 registered checkpoint

{summary}

The manifest has 694 entries, 114 accepted layers and 29 passing release checks. Only the 20 reviewed SC0 blocks and the two independently qualified ARM9 surname corrections differ from Rafael3514. The final format check ran across all four story archives, including the existing B146 relocation proof. The candidate's own startup matched the ten verified opening frames. Both original getters returned Plett Perrault and Jacob Portunto, along with the preserved Fernan Silveira, Francisca and Sakura. {link('Registered candidate', CANDIDATE)}. {link('Exact clean-input patch', release['patch'])}. {link('Registered verification', RELEASE)}. {link('Integrated review ledger', INTEGRATED)}.

The initialized B261–B280 research sequence displayed 43 pages, both menus and Jacob's nameplate. The other 88 speech variants and the original branch destinations passed offline checks. Plett's nameplate and natural event activation were outside the sampled emulator sequences. The existing Rafael3222 weekend package remains available. {link('Research checkpoint', 'docs/editorial_Rafael_B261_B280_research_20261106.md')}. {link('Weekend package', package['zip'])}.

Continue B281–B300 from the clean Japanese intake. It contains 164 speeches, 76 alternate voices in 11 style tables, and five captions across two menus. Thirty-two independent drafts cover B281–B286. Finish the remaining 213 drafts in full exchanges before comparing with the registered English. The wider review, separate artwork work and later older-record technical audit remain in scope. {link('Clean source packet', PACKET)}. {link('First six drafted exchanges', OUTPUT)}.
"""
    evidence = {str(path): digest(path) for path in (PACKET, STYLES, MENUS, OUTPUT, RELEASE, INTEGRATED, Path(__file__))}
    pin_release()
    checkpoint(mutation=CANDIDATE.parent/'registered_documentation_v1', batch_key='editorial_execution_priority_20261104',
        batch_updates=dict(new_credit=0, current_batch='Rafael B287–B300 clean first.',
            next_action='Finish the 213 remaining independent drafts before reading Rafael3649 English.',
            current_batch_not_yet_integrated=True, native_job_live=False, registered_build_live=False, guide_photos=False),
        new_entries={NEXT: dict(new_credit=0, source_only=True, source_records=245, ordinary_speeches=164,
            physical_style_alternatives=76, typed_captions=5, independently_drafted_records=32,
            independent_draft_blocks=list(range(281,287)), remaining_clean_meanings_anddrafts=213,
            remaining_current_comparisons=245, no_duplicate_credit=True, evidence=evidence)},
        summary=summary, document='docs/editorial_Rafael_B261_B280_registered_20261106.md',
        document_text=doc, completed=15494, protected={
            str(REGISTRY):release['registry_sha256'], release['canonical_base']:release['canonical_sha256'],
            release['candidate']:release['candidate_sha256'], release['patch']:release['patch_sha256'],
            package['zip']:package['zip_sha256']})
    print('Saved the registered handoff and 32 of 245 clean first drafts.')


if __name__ == '__main__':
    main()
