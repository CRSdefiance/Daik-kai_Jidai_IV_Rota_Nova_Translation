"""Save the verified research checkpoint and clean intake for the next Rafael batch."""
from pathlib import Path

from scripts.assemble_rafael_B241_B260_offline_v2 import ROOT, digest
from scripts.audit_story_glyph_consistency import load
from scripts.checkpoint_rafael_B168_B169_research_v1 import link
from scripts.save_editorial_progress_checkpoint_v6 import checkpoint
from scripts.save_rafael3222_weekend_checkpoint_v1 import BATCH, LEDGER, PACKAGE, RELEASE


READY = ROOT / 'research_final_v1/research_completion.json'
ACTUAL = READY.with_name('actual_review.json')
NEXT = Path('work/Rafael_B261_B280_clean_20261106')
NEXT_FILES = (NEXT/'clean_source_packet.json/clean_source_packet.json',
              NEXT/'clean_style_objects.json', NEXT/'clean_choice_objects.json')


def main():
    ready, actual, release, package, ledger = map(load, (READY, ACTUAL, RELEASE, PACKAGE, LEDGER))
    assert ready['all_individual_five_gates_pass'] and ready['registered_integration_pending']
    assert (ready['records'], ready['revisions'], ready['retentions'], ready['new_credit']) == (292, 244, 48, 0)
    assert (ready['body_pages'], ready['typed_labels'], ready['scoped_public_names']) == (294, 6, 20)
    assert (ready['actual_source_variants'], ready['actual_pages'], ready['actual_menus'], ready['actual_name_headers']) == (132, 135, 3, 13)
    assert actual['offline_only_speech_variants'] == 154 and len(actual['observed_FE_source_IDs']) == 7
    assert all(digest(path) == checksum for path, checksum in ready['evidence'].items())
    packet, styles, choices = map(load, NEXT_FILES)
    assert packet['clean_only_no_prior_English_ornew_editorial_credit']
    assert styles['source_packet_sha256'] == choices['source_packet_sha256'] == digest(NEXT_FILES[0])
    assert [group['block'] for group in packet['groups']] == list(range(261, 281))
    ordinary = [row for group in packet['groups'] for row in group['records']]
    next_records = ordinary + styles['records'] + choices['records']
    key = lambda row: (row['file_path'], row['id'])
    integrated = ledger['contextual_story_natural_dialogue_pass_v1871']['integrated_record_keys']
    current = load(ready['manuscript'])['records']
    next_keys = {key(row) for row in next_records}
    assert len(next_keys) == len(next_records) == 135
    assert next_keys.isdisjoint(map(key, integrated)) and next_keys.isdisjoint(map(key, current))
    assert (len(ordinary), len(styles['records']), len(choices['records'])) == (114, 16, 5)

    summary = (
        'Rafael B241–B260 passed all five research gates for 292 records, with 244 revisions and 48 justified retentions. '
        'The final 294 pages passed offline and stored checks. Three initialized emulator sequences displayed 135 pages '
        'and all three menus. Registered integration remains pending. Integrated coverage is 15,067.'
    )
    doc = f"""# Rafael B241–B260 research verification

{summary}

The review restored geographic references and the uncertainty around the Frozen Rose, corrected Jam Jack Ludwyan's signature and normalized Hatra's full-width I while preserving Rafael's name substitution. Sixteen wrap refinements removed four page turns while preserving every word. The stored script passed all 286 pre-substitution catalogue lookups, 120 relative branch cases and 343 archive loads. All 294 final pages, six captions and twenty scoped public names passed direct visual review. {link('Five-gate manuscript', ready['manuscript'])}. {link('Research completion evidence', READY)}.

The initialized fixtures displayed 132 speech variants and 13 distinct speaker headers, including the previously reviewed Sailor role. They showed both letter signatures, all seven system panels, the six captions at default cursor and ordinary A returns. Francisca's corrected F rendered in the progressive header. The full name getter passed offline. Both retained ellipses matched all black and shadow pixels when checked against their native palette. The other 154 speech variants are offline-only. Natural event activation, alternate selections and physical hardware remain unobserved. {link('Focused emulator evidence', ACTUAL)}.

Register the dialogue transaction and the independently verified exclusive actor 186 field correction. Carry forward all eight existing final stages, including the ASCII right-bound repair, plus the qualified B146 percent-relocation proof. Require clean-input reconstruction and candidate startup before credit. {link('Rafael3222 weekend package', package['zip'])}.

The next clean intake has 135 eligible objects across B261–B280, including 114 speeches, 16 style variants and five captions. It has zero overlap with the integrated or just-reviewed keys. Draft from clean Japanese before opening current English. {link('Clean source packet', NEXT_FILES[0])}.
"""
    evidence = {**ledger[BATCH]['evidence'], **{str(path): digest(path) for path in (READY, ACTUAL, Path(__file__))}}
    checkpoint(mutation=READY.parent/'verified_checkpoint_v1', batch_key=BATCH,
        batch_updates=dict(new_credit=0, all_individual_five_research_gates_pass=True, fifth_formatting_gate_pending=False,
            stored_checks_pending=False, focused_gameplay_pending=False, registered_integration_pending=True,
            full_intake_not_complete=True, source_speech_variants=286, typed_captions=6, complete_body_pages=294,
            scoped_public_names=20, observed_speeches=132, observed_pages=135, observed_menus=3, observed_headers=13,
            offline_only_speeches=154, offline_only_captions=0, final_review=ready['manuscript'],
            final_review_sha256=ready['manuscript_sha256'], research_completion=str(READY),
            research_completion_sha256=digest(READY), evidence=evidence),
        additional_updates={'editorial_execution_priority_20261104': dict(new_credit=0,
            current_batch='Rafael B241–B260 registered integration and B261–B280 clean drafts.',
            next_action='Register the verified dialogue transaction and Francisca field with exact reconstruction and startup. '
                        'Draft the next complete exchanges from clean Japanese.',
            current_batch_not_yet_integrated=True, native_job_live=False, registered_build_live=False, guide_photos=False)},
        new_entries={'Rafael_SC0_B261_B280_clean_20261106': dict(new_credit=0, source_only=True,
            source_records=135, ordinary_speeches=114, physical_style_alternatives=16, typed_captions=5,
            remaining_clean_meanings_anddrafts=135, remaining_current_comparisons=135, no_duplicate_credit=True,
            evidence={str(p): digest(p) for p in NEXT_FILES})},
        summary=summary, document='docs/editorial_Rafael_B241_B260_research_ready_20261106.md', document_text=doc,
        completed=15067, protected={'translations/release_stack.json':release['registry_sha256'],
            release['canonical_base']:release['canonical_sha256'], release['candidate']:release['candidate_sha256'],
            release['patch']:release['patch_sha256'], package['zip']:package['zip_sha256']})
    print('Saved 292 research completions and 135 clean source objects with zero new registered credit.')


if __name__ == '__main__':
    main()
