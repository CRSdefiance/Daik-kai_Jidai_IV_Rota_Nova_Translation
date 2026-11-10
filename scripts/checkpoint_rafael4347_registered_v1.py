"""Record the registered Rafael4347 handoff and verify the next clean intake."""
import inspect
import os
from pathlib import Path

from scripts.audit_story_glyph_consistency import load, save
from scripts.build_registered_rafael4347_v1 import CANDIDATE, INVERSE_PATCH, PARENT_REGISTRY, RELEASE
from scripts.checkpoint_rafael_B168_B169_research_v1 import link
from scripts.checkpoint_rafael3649_registered_v1 import pin_release as previous_pins
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.save_editorial_progress_checkpoint_v6 import checkpoint
from scripts.save_rafael3222_weekend_checkpoint_v1 import LEDGER, PACKAGE
from scripts.source_locked_derivation_v5118 import checked_text


BATCH = 'Rafael_SC0_B301_B320_clean_20261106'
NEXT = 'Rafael_SC0_B321_B342_clean_20261106'
INTEGRATED = Path('translations/rafael_B301_B320_integrated_final_review_v1.json')
REGISTRY = Path('translations/release_stack.json')
PINS = Path('translations/rom_retention_pins.json')
ROOT = Path('work/Rafael_B321_B342_clean_20261106')
PACKET = ROOT / 'clean_source_packet.json'
STYLES = ROOT / 'clean_style_objects.json'
MENUS = ROOT / 'clean_choice_objects.json'
pin_source = checked_text(inspect.getsource(previous_pins), {'Rafael3649': 'Rafael4347'})
exec(compile(pin_source, __file__ + '::registered-ROM-pins', 'exec'), globals())


def main():
    release, ledger, package, packet, styles, menus = map(load, (RELEASE, LEDGER, PACKAGE, PACKET, STYLES, MENUS))
    assert ledger[BATCH]['new_credit'] == ledger[BATCH]['completion_credit_added'] == 453
    assert ledger['records_editorially_completed'] == 16192
    assert ledger['current_integrated_candidate']['sha256'] == release['candidate_sha256']
    assert release['all_other_files_components_graphics_names_andruntime_exact_to_parent']
    assert release['clean_input_patch_byte_exact'] and not release['own_registered_startup_pending']
    current, parent = map(load, (REGISTRY, PARENT_REGISTRY))
    assert current['latest_promoted_build'] == parent['latest_promoted_build']
    assert current['accepted_layers'] == parent['accepted_layers']
    profile = current['profiles'][release['profile']]
    assert profile['ascii_glyph_right_bounds'] == parent['profiles'][release['predecessor_profile']]['ascii_glyph_right_bounds']
    assert packet['clean_only_no_prior_English_ornew_editorial_credit']
    assert styles['source_packet_sha256'] == menus['source_packet_sha256'] == digest(PACKET)
    assert [group['block'] for group in packet['groups']] == list(range(321, 343))
    ordinary = [row for group in packet['groups'] for row in group['records']]
    source = ordinary + styles['records'] + menus['records']
    assert (len(ordinary), len(styles['records']), len(menus['records']), len(source)) == (242, 298, 16, 556)
    assert (len(styles['objects']), styles['style_alias_slots'], len(menus['objects']), len(menus['label_free2000_controls'])) == (48, 384, 7, 1)
    key = lambda row: (row['file_path'], row['id'])
    assert len(set(map(key, source))) == 556
    integrated = ledger['contextual_story_natural_dialogue_pass_v1871']['integrated_record_keys']
    assert set(map(key, source)).isdisjoint(map(key, integrated))

    summary = (
        'Rafael B301–B320 is registered in Rafael4347 and credited once, with 397 revisions and 56 justified retentions. '
        'The exact clean-input patch, candidate startup and six inherited names passed. '
        'Integrated coverage is 16,192. The next clean Rafael intake has 556 records.'
    )
    doc = f"""# Rafael B301–B320 registered checkpoint

{summary}

The experimental candidate preserves the prior manifest entries, 114 accepted layers and the ASCII right-bound correction. The 32 passing release checks include a fresh format check across all four story archives. Changes from Rafael3894 are confined to the 20 reviewed SC0 blocks. The patch reconstructs the exact candidate from the clean Japanese input. The candidate’s own 4,001-frame startup matched the ten reviewed opening captures. Both original name getters returned Fernan Silveira, Plett Perrault, Jacob Portunto, Zaganos Bey, Francisca and Sakura. {link('Registered candidate', CANDIDATE)}. {link('Exact clean-input patch', release['patch'])}. {link('Release verification', RELEASE)}. {link('Integrated review ledger', INTEGRATED)}.

The focused emulator sequence used initialized events. It displayed 47 pages across 45 utterances, both two-page turns, all 11 labels across five menus, dialogue after the default choice in each menu, and ten nameplates including Al Shin and Safia. All 444 stored pages and 630 relocated branch cases passed offline. The other 397 speech variants were checked offline. Natural quest activation, other choice outcomes and hardware remain untested for this batch. {link('Focused evidence', 'work/Rafael_B301_B320_clean_20261106/research_final_v2/actual_review.json')}. {link('Stored checks', 'work/Rafael_B301_B320_clean_20261106/stored_v1/stored_native_verification.json')}. {link('Qualification checkpoint', 'docs/editorial_Rafael_B301_B320_research_20261106.md')}.

Continue with complete exchanges in Rafael B321–B342 from the clean Japanese. The intake contains 242 ordinary speeches, 298 physical alternate voices in 48 tables and 16 captions across seven menus. A separate label-free control is preserved outside the count. All 556 source keys are outside the credited set. Artwork and the older-record technical audit remain separate. {link('Clean speech and command packet', PACKET)}. {link('Alternate voices', STYLES)}. {link('Menu captions', MENUS)}.
"""
    evidence = {str(path): digest(path) for path in (PACKET, STYLES, MENUS, RELEASE, INTEGRATED, Path(__file__))}
    pin_release()
    checkpoint(
        mutation=CANDIDATE.parent/'registered_documentation_v1', batch_key='editorial_execution_priority_20261104',
        batch_updates=dict(new_credit=0, current_batch='Rafael B321–B342 clean first.',
                           next_action='Draft complete exchanges from the clean intake, then compare with Rafael4347.',
                           current_batch_not_yet_integrated=True, native_job_live=False,
                           registered_build_live=False, guide_photos=False),
        new_entries={NEXT: dict(new_credit=0, source_only=True, source_records=556, ordinary_speeches=242,
            physical_style_alternatives=298, typed_captions=16, independently_drafted_records=0,
            independent_draft_blocks=[], remaining_clean_meanings_anddrafts=556,
            remaining_current_comparisons=556, no_duplicate_credit=True, evidence=evidence)},
        summary=summary, document='docs/editorial_Rafael_B301_B320_registered_20261106.md',
        document_text=doc, completed=16192, protected={
            str(REGISTRY): release['registry_sha256'], release['canonical_base']: release['canonical_sha256'],
            release['candidate']: release['candidate_sha256'], release['patch']: release['patch_sha256'],
            package['zip']: package['zip_sha256'],
        },
    )
    print('Saved Rafael4347 and the 556-record clean intake. Integrated coverage is 16,192.')


if __name__ == '__main__':
    main()
