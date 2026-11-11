"""Register the reviewed Sound Setup track titles on the cumulative release."""

import argparse
from collections import Counter
from inspect import getsource
from json import dumps, loads
from pathlib import Path

from dk4tool.dialogue.review import validate_natural_dialogue_batch
from scripts import register_ancient_map_text_v2 as previous
from scripts import verify_sound_bgm_titles_v1 as verification
from scripts.source_locked_derivation_v5118 import checked_text


parent, transaction, base = previous.parent, previous.transaction, previous.base
stage = verification.stage
PARENT = previous.RELEASE
PROFILE = 'all-routes-sound-bgm-titles-editorial-v1-20261111'
FAMILY = 'sound_bgm_titles_contextual_20261111'
CHECK = 'registered_sound_bgm_titles_and_complete_parent_inverse'
PACKAGE = Path('releases/all_routes_editorial_20261111_sound_bgm_titles_candidate')
VERIFICATION = PACKAGE / 'verification'
RELEASE = VERIFICATION / 'registered_release_verification.json'
REVIEW = VERIFICATION / 'registered_review.json'
MUTATION_PLAN = VERIFICATION / 'registration_mutation_plan.json'
TEST = Path('out/sound_bgm_titles_registered_20261111_v1')
ROM = TEST / 'Translation_DS_All_Routes_Sound_Setup_20261111_candidate.nds'
MANIFEST = ROM.with_suffix('.manifest.json')
PATCH = PACKAGE / 'translation.xdelta'
DOC = Path('docs/editorial_sound_bgm_titles_registered_20261111.md')
PENDING_LEDGER = TEST / 'editorial_review_current.sound_bgm_titles.pending.json'
OUTPUT, EVIDENCE, RESEARCH = stage.review.OUTPUT, verification.REGISTRATION, stage.ROM
STARTUP_VERIFICATION, CHECKPOINT = verification.BOOT, verification.CHECKPOINT
LIVE_VERIFICATION, QA = verification.LIVE, verification.QA
PREVIOUS_TOTAL, TOTAL, REVISED, RETAINED = 27658, 38, 4, 34


def rebuild(release, evidence, source):
    image = base.NdsImage.open(release['candidate'])
    old_arm, old_common = (image.read_file(path) for path in (stage.ARM, stage.COMMON))
    rows = {row['message_ID']: row for row in source['records']}
    assert base.digest(OUTPUT) == evidence['manuscript_sha256']
    assert release['candidate_sha256'] == source['current_ROM_sha256']
    arm, common, entries, allocation = stage.stage(old_arm, old_common, rows)
    assert loads(dumps(allocation)) == evidence['allocation']
    assert evidence['original_selector_and_painter_exact'] and evidence['complete_parent_inverse']
    for row in evidence['records']:
        n = row['message_ID']
        assert row['reference'] == stage.review.reference(entries[n])
        assert row['complete_text'] == rows[n]['english'] == entries[n].text.decode('ascii')
    previous.verify_runtime(arm, release)
    image.replace_file(stage.ARM, arm)
    image.replace_file(stage.COMMON, common)
    assert bytes(image.rom.save()) == RESEARCH.read_bytes()
    image.replace_file(stage.ARM, old_arm)
    image.replace_file(stage.COMMON, old_common)
    assert bytes(image.rom.save()) == Path(release['candidate']).read_bytes()
    return arm, common


def verification_scope(approved, live):
    observed = list(verification.OBSERVED.values())
    assert approved['live_messages'] == live['observed_ids'] == observed
    assert approved['stored_cases'] == approved['viewed_pages'] == TOTAL
    assert live['actual_emulator'] and live['original_return_frames_exact'] and not live['gameplay_fixture']
    assert [row['message_ID'] for row in live['observations']] == observed
    return dict(observed_notice_IDs=observed, stored_cases=TOTAL, viewed_pages=TOTAL, actual_emulator=True,
        original_return_frames_exact=True, ordinary_gameplay=True, hardware=False, audio_output_assessed=False)


def final_review(source, evidence, scope):
    records = []
    for row, stored in zip(source['records'], evidence['records'], strict=True):
        n = stored['message_ID']
        assert row['id'] == f'COMMON_MESSAGE_{n}' and row['english'] == stored['complete_text']
        records.append(row | dict(review=row['review'] | {'formatting': True}, new_credit=1,
            registered_reference=stored['reference'] | {'ROM_sha256': evidence['research_ROM_sha256'],
                'exact_stored_hex': row['english'].encode('ascii').hex()}, native_center=stored['original_center'],
            gameplay_observed=n in scope['observed_notice_IDs']))
    assert len(records) == TOTAL and Counter(row['decision'] for row in records) == {
        'revision': REVISED, 'retention': RETAINED}
    review = dict(translation_policy=source['translation_policy'], target_locale=source['target_locale'],
        encoder=source['encoder'], review_gates=source['review_gates'], records=records,
        actual_verification_scope=scope, full_goal_complete=False)
    validate_natural_dialogue_batch(review)
    return review


def publish(release):
    summary = 'All 38 Sound Setup music titles are registered. The ledger now credits 27,696 reviews.'
    pin_path = Path('translations/rom_retention_pins.json')
    pins = base.load(pin_path)
    for path in (RESEARCH, ROM):
        assert path.is_file() and not any(row['path'] == str(path.resolve()) for row in pins)
        pins.append(dict(path=str(path.resolve()), reason=f'Preserve the Sound Setup title build. SHA256 {base.digest(path)}'))
    base.replace_checked(pin_path, (dumps(pins, ensure_ascii=False, indent=2) + '\n').replace('\n', '\r\n').encode())
    readme = f"""# All Routes Sound Setup candidate

Use [{ROM.name}](../../{ROM.as_posix()}) with its build manifest. The [clean-input patch](translation.xdelta) reconstructs the ROM byte for byte from Japanese SHA-256 `{release['clean_input_sha256']}`. Candidate SHA-256 `{release['candidate_sha256']}`. Patch SHA-256 `{release['patch_sha256']}`.

{summary} The four revisions include the approved Rafael and Camille spellings. The 34 retentions and four revisions all have complete native title and selector checks. An ordinary emulator replay observed all four revisions, the longest retained title and both original returns. It did not assess audio output. Cold startup, 24 protected name getters, 34 targeted tests and 112 release checks passed. [Gameplay](verification/{LIVE_VERIFICATION.name}) · [Exact records](verification/registered_review.json)
"""
    (PACKAGE / 'README.md').write_text(readme, encoding='utf-8', newline='\n')
    base.save(PACKAGE / 'checksums.json', previous.package_checksums(PACKAGE))
    doc = f"""# Sound Setup music titles registered

{summary} COMMON 3251–3288 supplies the original Sound Setup BGM selector. All 38 individual contextual decisions are in the [review ledger](../{REVIEW.as_posix()}). The [registered ROM and patch](../{PACKAGE.as_posix()}/README.md) preserve all 114 accepted layers, including the Market and ASCII right-bound corrections.

Northern and Southern European Town use parallel wording for the source locations. Rafael and Lil & Camille match the approved spellings used elsewhere. The original selection order, five-pixel tracking, and centered title panel are preserved. The original Sound Setup navigation displayed the four revised tracks and the full “Southeast Asian Village” title. That replay establishes the last letter’s presence where the synthetic narrow surface stopped one character early. Both return screens and all pixels outside the changed title region matched. Hardware and audio output remain unassessed.

280 native shared keys remain to review or classify. Continue with the Online copy, scene labels, and other legacy or shared keys. Other player-facing UI, speaker labels, earlier wraps and glyphs, and representative town and random-scene testing remain in scope. Deferred artwork and the older-record technical re-audit remain separate.
"""
    base.replace_checked(DOC, doc.encode('utf-8'))
    lead = f'# Current editorial checkpoint - 2026-11-11\n\n{summary}\n\nContinue from [the registered Sound Setup titles]({DOC.name}).\n\n'
    for name in ('editorial_handoff_current.md', 'editorial_efficiency_workflow.md', 'translation_progress.md'):
        path = Path('docs') / name
        base.replace_checked(path, lead.encode('utf-8') + path.read_bytes())
    continuity = Path('docs/build_continuity_protocol.md')
    protocol = ('Sound Setup music titles are registered with 777 entries, 114 accepted layers and 112 checks. '
                'Use scripts/register_sound_bgm_titles_v1.py with --register and --publish-prepared. '
                f'Exact patch, native title masks, ordinary Sound Setup and startup pass. [Checkpoint]({DOC.name})\n\n')
    base.replace_checked(continuity, protocol.encode('utf-8') + continuity.read_bytes())
    print('Registered 777 entries and credited the 38 Sound Setup titles once.')


def environment():
    return previous.environment() | globals()


def register():
    code = checked_text(getsource(previous.register), {
        'ancient-map-text': 'sound-bgm-titles',
        'All 61 Ancient Map records are registered.': 'All 38 Sound Setup music titles are registered.',
        "'== 27658'": "'== 27696'", "'== 16587'": "'== 16591'", "'== 11071'": "'== 11105'",
        "== 775 and len(manifest['checks']) == 110": "== 776 and len(manifest['checks']) == 111",
        "== 776 and len(manifest['checks']) == 111": "== 777 and len(manifest['checks']) == 112",
        'registered_manifest_entries=776, accepted_layers=114, passing_release_checks=111':
            'registered_manifest_entries=777, accepted_layers=114, passing_release_checks=112',
        'verified_arrival_month_labels_predecessor=predecessor, ancient_map_text_release=str(REVIEW)':
            'verified_ancient_map_text_predecessor=predecessor, sound_bgm_titles_release=str(REVIEW)',
        'Reviewed Ancient Map documents and rumors with the original painter and bounded word wraps.':
            'Reviewed Sound Setup music titles through the original selector and painter.',
        'release_stack_before_ancient_map_text': 'release_stack_before_sound_bgm_titles',
        'release_stack.ancient_map_text.pending': 'release_stack.sound_bgm_titles.pending',
        'COMMON_ANCIENT_MAP_TEXT_DIRECTORY_AND_POINTERS': 'COMMON_SOUND_BGM_TITLES_DIRECTORY_AND_POINTERS',
        'ancient_map_text_registered_successor_pipeline': 'sound_bgm_titles_registered_successor_pipeline',
        'Ancient Map registration staged and ready to publish.': 'Sound Setup registration staged and ready to publish.',
    })
    env = environment()
    exec(compile(code, __file__ + '::derive-sound-registration', 'exec'), env)
    env['register']()


def publish_prepared():
    code = checked_text(getsource(previous.publish_prepared), {
        'release_stack.ancient_map_text.pending': 'release_stack.sound_bgm_titles.pending',
    })
    env = environment()
    exec(compile(code, __file__ + '::derive-sound-publication', 'exec'), env)
    env['publish_prepared']()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    action = parser.add_mutually_exclusive_group(required=True)
    action.add_argument('--register', action='store_true')
    action.add_argument('--publish-prepared', action='store_true')
    (publish_prepared if parser.parse_args().publish_prepared else register)()
