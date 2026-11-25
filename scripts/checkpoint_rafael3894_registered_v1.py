"""Save the integrated checkpoint and the next complete clean-source intake."""
import inspect
import os
from pathlib import Path

from scripts.audit_story_glyph_consistency import load, save
from scripts.build_registered_rafael3894_v1 import CANDIDATE, INVERSE_PATCH, PARENT_REGISTRY, RELEASE
from scripts.checkpoint_rafael_B168_B169_research_v1 import link
from scripts.checkpoint_rafael3649_registered_v1 import pin_release as previous_pins
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.save_editorial_progress_checkpoint_v6 import checkpoint
from scripts.save_rafael3222_weekend_checkpoint_v1 import LEDGER, PACKAGE
from scripts.source_locked_derivation_v5118 import checked_text


BATCH = 'Rafael_SC0_B281_B300_clean_20261106'
NEXT = 'Rafael_SC0_B301_B320_clean_20261106'
INTEGRATED = Path('translations/rafael_B281_B300_integrated_final_review_v1.json')
REGISTRY = Path('translations/release_stack.json')
PINS = Path('translations/rom_retention_pins.json')
ROOT = Path('work/Rafael_B301_B320_clean_20261106')
PACKET = ROOT / 'clean_source_packet.json/clean_source_packet.json'
STYLES = ROOT / 'clean_style_objects.json'
MENUS = ROOT / 'clean_choice_objects.json'
pin_source = checked_text(inspect.getsource(previous_pins), {'Rafael3649': 'Rafael3894'})
exec(compile(pin_source, __file__ + '::registered-ROM-pins', 'exec'), globals())


def main():
    release, ledger, package, packet, styles, menus = map(load, (RELEASE, LEDGER, PACKAGE, PACKET, STYLES, MENUS))
    assert ledger[BATCH]['new_credit'] == ledger[BATCH]['completion_credit_added'] == 245
    assert ledger['records_editorially_completed'] == 15739
    assert ledger['current_integrated_candidate']['sha256'] == release['candidate_sha256']
    assert release['all_predecessor_stage_dependencies_preserved'] and release['owned_Zaganos_surname_verified']
    assert release['clean_input_patch_byte_exact'] and not release['own_registered_startup_pending']
    current, parent = map(load, (REGISTRY, PARENT_REGISTRY))
    assert current['latest_promoted_build'] == parent['latest_promoted_build']
    assert current['accepted_layers'] == parent['accepted_layers']
    profile = current['profiles'][release['profile']]
    assert profile['ascii_glyph_right_bounds'] == parent['profiles'][release['predecessor_profile']]['ascii_glyph_right_bounds']
    assert packet['clean_only_no_prior_English_ornew_editorial_credit']
    assert styles['source_packet_sha256'] == menus['source_packet_sha256'] == digest(PACKET)
    assert [group['block'] for group in packet['groups']] == list(range(301, 321))
    ordinary = [row for group in packet['groups'] for row in group['records']]
    source = ordinary + styles['records'] + menus['records']
    assert (len(ordinary), len(styles['records']), len(menus['records']), len(source)) == (297, 145, 11, 453)
    key = lambda row: (row['file_path'], row['id'])
    assert len(set(map(key, source))) == 453
    integrated = ledger['contextual_story_natural_dialogue_pass_v1871']['integrated_record_keys']
    assert set(map(key, source)).isdisjoint(map(key, integrated))

    summary = (
        'Rafael B281–B300 is registered in Rafael3894 and credited once, with 202 revisions and 43 justified retentions. '
        'The exact clean-input patch, candidate startup and Zaganos Bey name getters passed. '
        'Integrated coverage is 15,739. The next clean Rafael intake has 453 objects.'
    )
    doc = f"""# Rafael B281–B300 registered checkpoint

{summary}

The experimental candidate preserves the prior manifest entries, 114 accepted layers and the ASCII right-bound correction. The 31 passing release checks include a fresh format-safety check across all four story archives. The only owned differences from Rafael3649 are the 20 reviewed SC0 blocks and one byte in Zaganos’s ARM9 surname field. The exact clean-input reconstruction matches the candidate. The candidate’s own 4,001-frame startup matched the ten verified opening frames and both original getters returned Zaganos Bey, Plett Perrault, Jacob Portunto, Fernan Silveira, Francisca and Sakura. {link('Registered candidate', CANDIDATE)}. {link('Exact clean-input patch', release['patch'])}. {link('Release verification', RELEASE)}. {link('Integrated review ledger', INTEGRATED)}.

The focused initialized emulator sequence displayed 31 pages across 27 utterances, all five bear captions with the default cursor and the following dialogue after pressing A, the Plett and Zaganos nameplates, and the corrected 10,000-gold notice. All 248 stored pages and 800 relocated branch cases passed offline. The other 213 speech variants, original quest activation and gameplay outcomes remain outside the initialized sequence. {link('Focused evidence', 'work/Rafael_B281_B300_clean_20261106/research_final_v1/actual_review.json')}. {link('Stored checks', 'work/Rafael_B281_B300_clean_20261106/stored_v2/stored_native_verification.json')}. {link('Offline display checkpoint', 'docs/editorial_Rafael_B281_B300_display_20261106.md')}.

Continue with complete exchanges in Rafael B301–B320 from the clean Japanese. The intake has 297 ordinary speeches, 145 physical alternate voices in 19 tables and 11 captions across five menus. Each source key is outside the credited set. Preserve the wider goal, separate artwork work and later older-record technical audit. {link('Clean speech and command packet', PACKET)}. {link('Alternate voices', STYLES)}. {link('Menu captions', MENUS)}.
"""
    evidence = {str(path): digest(path) for path in (PACKET, STYLES, MENUS, RELEASE, INTEGRATED, Path(__file__))}
    pin_release()
    checkpoint(
        mutation=CANDIDATE.parent/'registered_documentation_v1', batch_key='editorial_execution_priority_20261104',
        batch_updates=dict(new_credit=0, current_batch='Rafael B301–B320 clean first.',
                           next_action='Draft complete exchanges from the clean intake, then compare with Rafael3894.',
                           current_batch_not_yet_integrated=True, native_job_live=False,
                           registered_build_live=False, guide_photos=False),
        new_entries={NEXT: dict(new_credit=0, source_only=True, source_records=453, ordinary_speeches=297,
            physical_style_alternatives=145, typed_captions=11, independently_drafted_records=0,
            independent_draft_blocks=[], remaining_clean_meanings_anddrafts=453,
            remaining_current_comparisons=453, no_duplicate_credit=True, evidence=evidence)},
        summary=summary, document='docs/editorial_Rafael_B281_B300_registered_20261106.md',
        document_text=doc, completed=15739, protected={
            str(REGISTRY): release['registry_sha256'], release['canonical_base']: release['canonical_sha256'],
            release['candidate']: release['candidate_sha256'], release['patch']: release['patch_sha256'],
            package['zip']: package['zip_sha256'],
        },
    )
    print('Saved Rafael3894 and the 453-record clean intake. Integrated coverage is 15,739.')


if __name__ == '__main__':
    main()
