"""Register the verified arrival-month label correction over the cumulative ROM."""

import argparse
from copy import deepcopy
from gzip import compress, decompress
from hashlib import sha256
from json import dumps, loads
from pathlib import Path
from shutil import copyfile

from dk4tool.patch.xdelta import apply_xdelta, make_xdelta
from scripts import stage_arrival_month_labels_v1 as stage
from scripts import verify_arrival_month_labels_v1 as verification
from scripts.editorial_ledger_storage_v1 import encode_ledger
from scripts.prepare_all_routes_promotion_20261111 import package_checksums, verify_runtime


parent, base = stage.parent, stage.base
ARM, COMMON, CLEAN = stage.ARM, stage.COMMON, stage.CLEAN
PROFILE = 'all-routes-arrival-month-labels-v1-20261111'
CHECK = 'registered_arrival_month_label_terminators_and_complete_parent_inverse'
PACKAGE = Path('releases/all_routes_editorial_20261111_arrival_month_labels_candidate')
VERIFICATION = PACKAGE / 'verification'
REVIEW = VERIFICATION / 'registered_label_review.json'
RELEASE = VERIFICATION / 'registered_release_verification.json'
MUTATION_PLAN = VERIFICATION / 'registration_mutation_plan.json'
TEST = Path('out/arrival_month_labels_registered_20261111_v1')
ROM = TEST / 'Translation_DS_All_Routes_Arrival_Month_Labels_20261111_candidate.nds'
MANIFEST, PATCH = ROM.with_suffix('.manifest.json'), PACKAGE / 'translation.xdelta'
DOC = Path('docs/editorial_arrival_month_labels_registered_20261111.md')
REGISTRY_PENDING = base.REGISTRY.with_name('release_stack.arrival_month_labels.pending.json')
LEDGER_PENDING = base.LEDGER.with_name('editorial_review_current.arrival_month_labels.pending.json')


def digest(raw):
    return sha256(raw).hexdigest()


def archive(raw, path):
    path.write_bytes(compress(raw, compresslevel=1, mtime=0))
    assert decompress(path.read_bytes()) == raw


def register():
    assert not any(path.exists() for path in (TEST, PACKAGE, DOC, REGISTRY_PENDING, LEDGER_PENDING))
    old, proof, boot, live = map(base.load, (parent.RELEASE, stage.PROOF, verification.BOOT, verification.LIVE))
    sha = base.digest(stage.ROM)
    assert sha == proof['research_ROM_sha256'] == boot['candidate_sha256'] == live['candidate_sha256']
    assert proof['parent_inverse_exact'] and old['candidate_sha256'] == live['parent_sha256'] == proof['parent_sha256']
    assert all(base.digest(path) == expected for path, expected in live['evidence'].items())
    assert boot['cold_boot'] and len(boot['original_protected_name_getters']) == 24
    assert len(live['observed_changes']) == 12 and len(live['whole_frame_equal']) == 28
    assert live['calendars_and_other_pixels_unchanged'] and live['repository_tests'] == 34
    assert base.digest(CLEAN) == old['clean_input_sha256']
    assert base.digest(parent.ROM) == old['candidate_sha256'] and base.digest(parent.MANIFEST) == old['manifest_sha256']
    before_registry, before_ledger = base.REGISTRY.read_bytes(), base.LEDGER.read_bytes()
    assert digest(before_registry) == old['registry_sha256']
    registry, ledger = loads(before_registry), loads(before_ledger)
    assert PROFILE not in registry['profiles'] and len(registry['accepted_layers']) == 114
    assert ledger['records_editorially_completed'] == 27597 and not ledger['full_goal_complete']
    assert ledger['current_integrated_candidate']['sha256'] == old['candidate_sha256']
    manifest = base.load(parent.MANIFEST)
    assert len(manifest['batches']) == 774 and len(manifest['checks']) == 109 and all(manifest['checks'].values())
    parent_image = base.NdsImage.open(parent.ROM)
    original = parent_image.read_file(ARM)
    arm, records = stage.transform(original, base.NdsImage.open(CLEAN).read_file(ARM))
    assert records == proof['records'] and digest(arm) == proof['research_ARM9_sha256']
    assert digest(parent_image.read_file(COMMON)) == proof['research_COMMON_sha256'] == old['target_COMMON_sha256']
    verify_runtime(arm, old)
    parent_image.replace_file(ARM, arm)
    assert bytes(parent_image.rom.save()) == stage.ROM.read_bytes()
    parent_image.replace_file(ARM, original)
    assert bytes(parent_image.rom.save()) == parent.ROM.read_bytes()
    TEST.mkdir()
    VERIFICATION.mkdir(parents=True)
    make_xdelta(CLEAN, stage.ROM, PATCH)
    apply_xdelta(CLEAN, PATCH, ROM)
    assert ROM.read_bytes() == stage.ROM.read_bytes() and base.digest(ROM) == sha
    for path in (stage.PROOF, verification.BOOT, verification.LIVE, verification.QA):
        copyfile(path, VERIFICATION / path.name)
        assert base.digest(VERIFICATION / path.name) == base.digest(path)
    scope = dict(actual_emulator=True, hardware=False, Trade_holds=11, Golden_Route_Found_holds=1,
        other_whole_frames_exact=28, original_calendar_and_Guild_return_exact=True,
        fixture_scope='One temporary purchase-cost word to reach the original Golden Route screen.')
    base.save(REVIEW, dict(translation_policy='natural-dialogue-v2', target_locale='en-US',
        records=[row | dict(review=dict.fromkeys(('source', 'context', 'localization', 'naturalness', 'formatting'), True),
                            new_dialogue_credit=0) for row in records],
        actual_verification_scope=scope, current_ROM_sha256=sha))
    previous = TEST / 'release_stack_before_arrival_month_labels.json'
    previous.write_bytes(before_registry)
    predecessor = {key: old[key] for key in ('profile', 'candidate', 'candidate_sha256', 'manifest', 'manifest_sha256', 'registry_sha256')}
    predecessor['registry'] = str(previous)
    profile = deepcopy(registry['profiles'][old['profile']])
    profile.update(verified_golden_route_exchanges_predecessor=predecessor, arrival_month_labels_release=str(REVIEW),
                   note='Terminated the original Trade and Golden Route arrival-month labels in their owned slots.')
    registry['profiles'][PROFILE] = profile
    base.save(REGISTRY_PENDING, registry)
    manifest.update(profile=PROFILE, candidate_rom=str(ROM), candidate_sha256=sha,
                    release_stack_sha256=base.digest(REGISTRY_PENDING))
    manifest['batches'].append(str(REVIEW))
    manifest['checks'][CHECK] = True
    manifest['changed_records'][ARM].extend(row['id'] for row in records)
    manifest['relocations'][ARM]['arrival_month_labels'] = records
    manifest['arrival_month_labels_registered_successor_pipeline'] = dict(predecessor=predecessor,
        driver=str(Path(__file__)), driver_sha256=base.digest(__file__), review=str(REVIEW), review_sha256=base.digest(REVIEW),
        exact_rebuild_and_reconstruction=True, scope=scope)
    assert len(manifest['batches']) == 775 and len(manifest['checks']) == 110
    base.save(MANIFEST, manifest)
    startup = VERIFICATION / verification.BOOT.name
    release = old | dict(profile=PROFILE, candidate=str(ROM), candidate_sha256=sha, patch=str(PATCH),
        patch_sha256=base.digest(PATCH), manifest=str(MANIFEST), manifest_sha256=base.digest(MANIFEST),
        registry_sha256=base.digest(REGISTRY_PENDING), target_ARM9_sha256=digest(arm), predecessor=predecessor,
        registered_manifest_entries=775, passing_release_checks=110, repository_tests=34,
        own_registered_startup=str(startup), own_registered_startup_sha256=base.digest(startup),
        actual_verification_scope=scope, changed_components=[ARM], changed_internal_files=[],
        new_contextual_records=0, prose_revisions=0, justified_retentions=0, reviewed_UI_labels=2)
    base.save(RELEASE, release)
    base.save(PACKAGE / 'release_manifest.json', release | {'user_acceptance_pending': True})
    archive(MANIFEST.read_bytes(), PACKAGE / 'build_manifest.json.gz')
    archive(REGISTRY_PENDING.read_bytes(), PACKAGE / 'build_release_stack.json.gz')
    archive(before_ledger, TEST / 'editorial_ledger_before.json.gz')
    ledger['current_integrated_candidate'].update(path=str(ROM), sha256=sha, profile=PROFILE,
        ARM9_sha256=release['target_ARM9_sha256'], patch=str(PATCH), patch_sha256=release['patch_sha256'],
        manifest=str(MANIFEST), manifest_sha256=release['manifest_sha256'], registered_release_verification=str(RELEASE))
    ledger['latest_checkpoint'] = 'The two arrival-month label corrections are registered.'
    ledger['arrival_month_labels_20261111'] = dict(review=str(REVIEW), release=str(RELEASE), new_dialogue_credit=0)
    LEDGER_PENDING.write_bytes(encode_ledger(ledger))
    base.save(MUTATION_PLAN, dict(registry_before=digest(before_registry), registry_after=base.digest(REGISTRY_PENDING),
        ledger_before=digest(before_ledger), ledger_after=base.digest(LEDGER_PENDING), main=base.digest(base.PROMOTED)))
    print('Staged the exact cumulative arrival-month release for publication.')


def publish_prepared():
    release, plan = map(base.load, (RELEASE, MUTATION_PLAN))
    assert not DOC.exists()
    assert base.digest(base.PROMOTED) == plan['main']
    for path, key in ((base.REGISTRY, 'registry_before'), (base.LEDGER, 'ledger_before'),
                      (REGISTRY_PENDING, 'registry_after'), (LEDGER_PENDING, 'ledger_after')):
        assert base.digest(path) == plan[key]
    for path, key in ((ROM, 'candidate_sha256'), (MANIFEST, 'manifest_sha256'), (PATCH, 'patch_sha256')):
        assert base.digest(path) == release[key]
    pins_path = Path('translations/rom_retention_pins.json')
    pins = base.load(pins_path)
    for path in (stage.ROM, ROM):
        resolved = str(path.resolve())
        assert path.is_file() and not any(row['path'] == resolved for row in pins)
        pins.append(dict(path=resolved, reason=f'Preserve the arrival-month build. SHA256 {base.digest(path)}'))
    notes = f"""# Arrival-month labels candidate

Use [{ROM.name}](../../{ROM.as_posix()}) with its build manifest. The [clean-input patch](translation.xdelta) reconstructs the candidate byte for byte from Japanese SHA-256 `{release['clean_input_sha256']}`. Candidate SHA-256 `{release['candidate_sha256']}`. Patch SHA-256 `{release['patch_sha256']}`.

Trade shows “Arr.” and Golden Route Found shows “Arrival.” Both labels terminate before the following string in ARM9. The 40-frame Lisbon comparison found 12 label-only differences and 28 exact frames. Both complete glyph masks, the month grids, the Guild return, cold boot, 24 protected getters, 34 targeted tests and 110 release checks passed. [Review](verification/{REVIEW.name}) · [Gameplay](verification/{verification.LIVE.name})
"""
    document = """# Arrival-month labels registered

The Trade and Golden Route Found calendars now display complete terminated labels. The eight-byte fields at `0215A000` and `0216AFB0` hold “Arr.” and “Arrival.” The original callers and the strings that follow both slots are byte-exact. The replay verified the new labels and preserved all other screen pixels in the 40 sampled frames.

The [registered candidate and patch](../releases/all_routes_editorial_20261111_arrival_month_labels_candidate/README.md) preserve all previous layers. The dialogue ledger remains at 27,597 reviews, with 379 native shared keys to review or classify. Continue with the [Ancient Map manuscript](../translations/editorial_checkpoints/SharedText_20261110_v1/treasure_map_documents_context_v1.json). It records 51 contextual decisions and the 20 original region and direction pairs. The native document layout and representative replay are pending.
"""
    (PACKAGE / 'README.md').write_text(notes, encoding='utf-8', newline='\n')
    base.save(PACKAGE / 'checksums.json', package_checksums(PACKAGE))
    old_registry = base.REGISTRY.read_bytes()
    REGISTRY_PENDING.replace(base.REGISTRY)
    try:
        LEDGER_PENDING.replace(base.LEDGER)
    except OSError:
        base.replace_checked(base.REGISTRY, old_registry)
        raise
    assert base.digest(base.REGISTRY) == plan['registry_after'] and base.digest(base.LEDGER) == plan['ledger_after']
    base.replace_checked(pins_path, (dumps(pins, ensure_ascii=False, indent=2) + '\n').replace('\n', '\r\n').encode())
    base.replace_checked(DOC, document.encode())
    lead = '# Current editorial checkpoint - 2026-11-11\n\n'
    lead += f'The two arrival-month labels are registered. [Checkpoint]({DOC.name})\n\n'
    for name in ('editorial_handoff_current.md', 'editorial_efficiency_workflow.md', 'translation_progress.md',
                 'build_continuity_protocol.md'):
        path = Path('docs') / name
        base.replace_checked(path, lead.encode() + path.read_bytes())
    print('Registered 775 entries, 114 accepted layers and 110 checks. Dialogue credit remains 27,597.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    action = parser.add_mutually_exclusive_group(required=True)
    action.add_argument('--register', action='store_true')
    action.add_argument('--publish-prepared', action='store_true')
    (publish_prepared if parser.parse_args().publish_prepared else register)()
