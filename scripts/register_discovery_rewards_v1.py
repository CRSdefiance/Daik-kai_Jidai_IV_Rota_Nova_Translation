"""Register the verified discovery and reward notices over Shipyard and Fleet Setup."""

import argparse
import inspect
import json
from pathlib import Path

from scripts import register_setup_save_equipment_v1 as previous
from scripts import stage_discovery_rewards_v1 as stage
from scripts.register_shipyard_fleet_setup_v1 import RELEASE as PARENT
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.verify_discovery_rewards_v1 import BOOT as STARTUP_VERIFICATION
from scripts.verify_discovery_rewards_v1 import CHECKPOINT, LIVE as LIVE_VERIFICATION, QA


base = previous.base
PROFILE = 'all-routes-discovery-rewards-editorial-v1-20261111'
FAMILY = 'discovery_rewards_contextual_20261111'
CHECK = 'registered_discovery_rewards_native_live_and_complete_parent_inverse'
PACKAGE = Path('releases/all_routes_editorial_20261111_discovery_rewards_candidate')
VERIFICATION = PACKAGE / 'verification'
RELEASE = VERIFICATION / 'registered_release_verification.json'
REVIEW = VERIFICATION / 'registered_review.json'
MUTATION_PLAN = VERIFICATION / 'registration_mutation_plan.json'
TEST = Path('out/discovery_rewards_registered_20261111_v1')
ROM = TEST / 'Translation_DS_All_Routes_Discovery_Rewards_20261111_candidate.nds'
MANIFEST = ROM.with_suffix('.manifest.json')
PATCH = PACKAGE / 'translation.xdelta'
DOC = Path('docs/editorial_discovery_rewards_registered_20261111.md')
PENDING_LEDGER = TEST / 'editorial_review_current.discovery_rewards.pending.json'
OUTPUT, EVIDENCE, RESEARCH = stage.MANUSCRIPT, stage.PROOF, stage.ROM
PREVIOUS_TOTAL, TOTAL, REVISED, RETAINED = 26357, 14, 12, 2


def rebuild(parent, evidence, source):
    code = checked_text(inspect.getsource(previous.rebuild), {
        "assert owner == evidence['ownership']": "assert json.loads(json.dumps(owner)) == evidence['ownership']",
        "rows = {row['message_ID']: row for row in source['records'] if row['message_ID'] != 318}":
            "rows = stage.active_rows(source)",
    })
    env = {**vars(previous), **globals()}
    exec(compile(code, __file__ + '::same-owned-payload-and-parent-inverse', 'exec'), env)
    return env['rebuild'](parent, evidence, source)


def verification_scope(approved, live):
    assert approved['observed_ids'] == live['observed_ids'] == [297, 298]
    assert approved['stored_records'] == 14 and approved['viewed_pages'] == 31
    assert len(live['selector_positive_and_negative_cases']) == 12
    assert live['original_auto_move']['native_automatic_flag_cleared']
    assert live['original_village']['fixture']['only_eight_ship_coordinate_bytes_owned']
    return dict(observed_notice_IDs=live['observed_ids'], stored_records=14, modal_variants=31,
        directly_viewed_modal_pages=31, original_auto_move_stop_yes_to_manual=True,
        original_discovery_docking_resupply_and_menu_return=True,
        fixture_scope='Ordinary Riga battery save with original controller and stylus inputs. Inuvik used a prior battery save and a verified eight-byte ship-position fixture before the original discovery.',
        startup_scope='Fresh emulator boot with the previously qualified system unlock fixture and 24 read-only protected name getters.',
        offline_only_notice_IDs=[288, 292, 299, 301, 302, 303, 305, 311, 313, 314, 340, 341],
        retained_raw_name_substitution_verified_offline=341,
        unbound_common_IDs=[287, 296, 300, 304], hardware=False)


def final_review(source, evidence, scope):
    assert evidence['editorial_amendments'] == json.loads(json.dumps(stage.AMENDMENTS))
    updated = source | {'records': list(stage.active_rows(source).values())}
    env = {**vars(previous), **globals()}
    exec(compile(inspect.getsource(previous.final_review), __file__ + '::exact-natural-dialogue-review', 'exec'), env)
    return env['final_review'](updated, evidence, scope)


def publish(release):
    summary = 'The 14 discovery and reward notices are registered. The ledger now credits 26,371 reviews.'
    notes = f"""# All Routes Discovery and Rewards candidate

Use the local ROM `{ROM.as_posix()}` beside its build manifest. The [clean-input patch](translation.xdelta) applies to clean Japanese SHA-256 `{release['clean_input_sha256']}` and reconstructs SHA-256 `{release['candidate_sha256']}` byte for byte. Patch SHA-256 is `{release['patch_sha256']}`.

{summary} Twelve revisions and two justified retentions cover discoveries, the Auto Move confirmation, captured gold and supplies, and acquisitions. The food and water notice preserves both native amounts and the barrel unit for each. The original discovery and crew-recruitment wording earned retention.

The original Riga replay verified the complete “Stop Auto Move?” prompt and return to manual sailing. At Inuvik, the ship-position fixture led into the original discovery, docking, resupply, and village menu return. All 31 stored display variants were visually reviewed. The remaining notices passed offline checks, including the original composed-name substitution. All 81 release checks, 30 targeted tests, cold startup, and 24 protected name getters passed. [Gameplay proof](verification/discovery_rewards_gameplay_verification.json) · [Exact record review](verification/registered_review.json)
"""
    (PACKAGE / 'README.md').write_text(notes, encoding='utf-8', newline='\n')
    base.save(PACKAGE / 'checksums.json', {p.relative_to(PACKAGE).as_posix(): base.digest(p)
        for p in sorted(PACKAGE.rglob('*')) if p.is_file() and p.name != 'checksums.json'})
    pin_path = Path('translations/rom_retention_pins.json')
    pins = base.load(pin_path)
    assert any(row['path'] == str(RESEARCH.resolve()) for row in pins)
    assert not any(row['path'] == str(ROM.resolve()) for row in pins)
    pins.append(dict(path=str(ROM.resolve()), reason=f"Preserve registered discovery and reward ROM. SHA256 {release['candidate_sha256']}"))
    base.replace_checked(pin_path, (json.dumps(pins, ensure_ascii=False, indent=2) + '\n').replace('\n', '\r\n').encode('utf-8'))
    doc = f"""# Discovery and reward notices registered

{summary} The original discovery and recruitment wording earned retention. The revised notices distinguish recovered gold, a national reward, and generic receipts. Both supply quantities survive in the original order, and the shark sound and acquisition messages were reviewed in the context of the complete exchange. [Release and patch](../{PACKAGE.as_posix()}/README.md) · [Registered review](../{REVIEW.as_posix()})

The Riga Auto Move replay confirmed the complete question and manual sailing state. Inuvik discovery and the subsequent docking and resupply were observed in the original emulator flow with an eight-byte ship-position fixture. All 31 stored variants passed automated and visual checks. The recruitment notice passed offline with original composed names. Hardware testing and the other reward triggers remain unobserved.

The [source review](../{OUTPUT.as_posix()}) preserves the unbound records 287, 296, 300 and 304 and the surrounding shark exchange. Continue the remaining shared notices from the clean source, including 334–335, 337, and 342–345. Keep 284, 318, the legacy setup and Options records, and Market replies 750–752 open. Keep deferred artwork and the older-record technical re-audit separate.
"""
    base.replace_checked(DOC, doc.encode('utf-8'))
    lead = f'# Current editorial checkpoint - 2026-11-11\n\n{summary}\n\nContinue from [the registered discovery and reward notices]({DOC.name}).\n\n'.encode('utf-8')
    for name in ('editorial_handoff_current.md', 'editorial_efficiency_workflow.md', 'translation_progress.md'):
        path = Path('docs') / name
        base.replace_checked(path, lead + path.read_bytes())
    continuity = Path('docs/build_continuity_protocol.md')
    lead = f"""The 14 discovery and reward notices are registered over Shipyard and Fleet Setup with 746 entries, 114 accepted layers and 81 checks. Use `scripts/register_discovery_rewards_v1.py --register` to stage and `--publish-prepared` to publish. Preserve the original raw recruitment formatter and route the five reward paragraphs only through their original notice parent. The exact reconstruction, live Auto Move and village transitions, and cold startup pass. [Registered checkpoint]({DOC.name})

"""
    base.replace_checked(continuity, lead.encode('utf-8') + continuity.read_bytes())
    print('Registered 746 entries and credited 14 discovery and reward notices once.')


def register():
    source = checked_text(inspect.getsource(previous.register), {
        "'equipment-and-system-notices'": "'discovery-and-reward-notices'",
        'Fourteen system and equipment notices are registered.': 'Fourteen discovery and reward notices are registered.',
        "'== 25985': '== 26333', '== 15438': '== 15699', '== 10547': '== 10634'":
            "'== 25985': '== 26371', '== 15438': '== 15728', '== 10547': '== 10643'",
        '"len(manifest[\'batches\']) == 743 and len(manifest[\'checks\']) == 78"':
            '"len(manifest[\'batches\']) == 745 and len(manifest[\'checks\']) == 80"',
        '"len(manifest[\'batches\']) == 744 and len(manifest[\'checks\']) == 79"':
            '"len(manifest[\'batches\']) == 746 and len(manifest[\'checks\']) == 81"',
        'release_stack_before_equipment_system.json': 'release_stack_before_discovery_rewards.json',
        'verified_captain_biographies_predecessor=predecessor, equipment_system_release=str(REVIEW)':
            'verified_shipyard_fleet_setup_predecessor=predecessor, discovery_rewards_release=str(REVIEW)',
        'Reviewed system and equipment notices, including the original removal result.':
            'Reviewed discovery and reward notices with scoped native paragraph wrapping.',
        'release_stack.equipment_system.pending.json': 'release_stack.discovery_rewards.pending.json',
        'COMMON_329_EQUIPMENT_REMOVAL_WORD_WRAP': 'COMMON_DISCOVERY_REWARD_WORD_WRAP',
        'equipment_system_registered_successor_pipeline': 'discovery_rewards_registered_successor_pipeline',
        'registered_manifest_entries=744, accepted_layers=114, passing_release_checks=79, repository_tests=30':
            'registered_manifest_entries=746, accepted_layers=114, passing_release_checks=81, repository_tests=30',
        'Equipment/system registration staged and ready to publish.':
            'Discovery and reward registration staged and ready to publish.',
    })
    env = {**vars(previous), **globals()}
    exec(compile(source, __file__ + '::same-registered-release-transaction', 'exec'), env)
    env['register']()


def publish_prepared():
    source = checked_text(inspect.getsource(previous.publish_prepared), {
        'release_stack.equipment_system.pending.json': 'release_stack.discovery_rewards.pending.json',
    })
    env = {**vars(previous), **globals()}
    exec(compile(source, __file__ + '::same-registered-publication', 'exec'), env)
    env['publish_prepared']()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    action = parser.add_mutually_exclusive_group(required=True)
    action.add_argument('--register', action='store_true')
    action.add_argument('--publish-prepared', action='store_true')
    (publish_prepared if parser.parse_args().publish_prepared else register)()
