"""Register the reviewed Shipyard and fleet setup notices and their exact patch."""

import argparse
import inspect
import json
from pathlib import Path

from scripts import register_setup_save_equipment_v1 as previous
from scripts import stage_shipyard_fleet_setup_v2 as stage
from scripts.register_setup_save_equipment_v1 import RELEASE as PARENT
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.verify_shipyard_fleet_setup_v1 import BOOT as STARTUP_VERIFICATION
from scripts.verify_shipyard_fleet_setup_v1 import CATALOGUES
from scripts.verify_shipyard_fleet_setup_v1 import CHECKPOINT, LIVE as LIVE_VERIFICATION, QA


base = previous.base
PROFILE = 'all-routes-shipyard-fleet-setup-editorial-v1-20261111'
FAMILY = 'shipyard_fleet_setup_contextual_20261111'
CHECK = 'registered_shipyard_fleet_setup_native_live_and_complete_parent_inverse'
PACKAGE = Path('releases/all_routes_editorial_20261111_shipyard_fleet_setup_candidate')
VERIFICATION = PACKAGE / 'verification'
RELEASE = VERIFICATION / 'registered_release_verification.json'
REVIEW = VERIFICATION / 'registered_review.json'
MUTATION_PLAN = VERIFICATION / 'registration_mutation_plan.json'
TEST = Path('out/shipyard_fleet_setup_registered_20261111_v1')
ROM = TEST / 'Translation_DS_All_Routes_Shipyard_Fleet_Setup_20261111_candidate.nds'
MANIFEST = ROM.with_suffix('.manifest.json')
PATCH = PACKAGE / 'translation.xdelta'
DOC = Path('docs/editorial_shipyard_fleet_setup_registered_20261111.md')
PENDING_LEDGER = TEST / 'editorial_review_current.shipyard_fleet_setup.pending.json'
OUTPUT, EVIDENCE, RESEARCH = stage.MANUSCRIPT, stage.PROOF, stage.ROM
PREVIOUS_TOTAL, TOTAL, REVISED, RETAINED = 26333, 24, 17, 7


def rebuild(parent, evidence, source):
    source_code = checked_text(inspect.getsource(previous.rebuild), {
        "assert owner == evidence['ownership']": "assert json.loads(json.dumps(owner)) == evidence['ownership']",
        "rows = {row['message_ID']: row for row in source['records'] if row['message_ID'] != 318}":
            "rows = {row['message_ID']: row | stage.AMENDMENTS.get(row['message_ID'], {}) for row in source['records']}",
        'stage.relocate': 'stage.first.previous.relocate',
        'stage.reference': 'stage.first.previous.reference',
    })
    env = {**vars(previous), **globals()}
    exec(compile(source_code, __file__ + '::same-owned-payload-and-parent-inverse', 'exec'), env)
    return env['rebuild'](parent, evidence, source)


def verification_scope(approved, live):
    assert approved['observed_ids'] == live['observed_ids'] == [265, 280, 281, 285, 286]
    assert approved['stored_records'] == 24 and approved['viewed_pages'] == 28
    assert len(live['native_selector_controls']['dispatch_scope']) == 10
    catalogue = base.load(CATALOGUES)
    assert catalogue['candidate_sha256'] == live['candidate_sha256'] and catalogue['towns'] == 90
    return dict(observed_notice_IDs=live['observed_ids'], stored_records=24, modal_variants=28,
        directly_viewed_modal_pages=28, original_yard_confirmation_and_name_entry=True,
        original_fleet_setup_and_disband_choices=True, original_disband_dock_return=True,
        fixture_scope='Read-only native request observation over ordinary inputs and isolated existing battery saves. The fleet save inherits previously documented formation prerequisites.',
        offline_dynamic_notice_ids=[261, 279], offline_catalogue_expansions=len(catalogue['rows']),
        unbound_debt_warning=284, hardware=False)


def final_review(source, evidence, scope):
    assert evidence['editorial_amendments'] == json.loads(json.dumps(stage.AMENDMENTS))
    updated = source | {'records': [row | stage.AMENDMENTS.get(row['message_ID'], {}) for row in source['records']]}
    env = {**vars(previous), **globals()}
    exec(compile(inspect.getsource(previous.final_review), __file__ + '::exact-natural-dialogue-review', 'exec'), env)
    return env['final_review'](updated, evidence, scope)


def publish(release):
    summary = 'The 24 shipyard and fleet setup notices are registered. The ledger now credits 26,357 reviews.'
    notes = f"""# All Routes Shipyard and Fleet Setup candidate

Use the local ROM \x60{ROM.as_posix()}\x60 beside its build manifest. The [clean-input patch](translation.xdelta) applies to clean Japanese SHA-256 \x60{release['clean_input_sha256']}\x60 and reconstructs SHA-256 \x60{release['candidate_sha256']}\x60 byte for byte. Patch SHA-256 is \x60{release['patch_sha256']}\x60.

{summary} Seventeen revisions and seven justified retentions cover local news, ship buying, captain changes, regional fleet setup and disbandment. Distinct refusals and confirmations again select complete text. Long names retain both original substitutions and keep “as admiral?” together.

Syracuse replays verified the purchase prompt through ship naming, both original fleet pickers, and the disband choice through cancellation and the dock result. The fleet replay used an existing save with a documented regional fleet. All 28 stored modal variants, 80 release checks, 30 targeted tests, cold startup and 24 protected name getters passed. [Gameplay proof](verification/shipyard_fleet_gameplay_verification.json) · [Exact record review](verification/registered_review.json)
"""
    (PACKAGE / 'README.md').write_text(notes, encoding='utf-8', newline='\n')
    base.shutil.copyfile(CATALOGUES, VERIFICATION / CATALOGUES.name)
    assert base.digest(CATALOGUES) == base.digest(VERIFICATION / CATALOGUES.name)
    base.save(PACKAGE / 'checksums.json', {p.relative_to(PACKAGE).as_posix(): base.digest(p)
        for p in sorted(PACKAGE.rglob('*')) if p.is_file() and p.name != 'checksums.json'})
    pin_path = Path('translations/rom_retention_pins.json')
    pins = base.load(pin_path)
    for path, role in ((stage.first.ROM, 'first shipyard fleet prototype'),
                       (RESEARCH, 'phrase-safe shipyard fleet research ROM'), (ROM, 'registered shipyard fleet ROM')):
        assert not any(row['path'] == str(path.resolve()) for row in pins)
        pins.append(dict(path=str(path.resolve()), reason=f'Preserve {role}. SHA256 {base.digest(path)}'))
    base.replace_checked(pin_path, (json.dumps(pins, ensure_ascii=False, indent=2) + '\n').replace('\n', '\r\n').encode('utf-8'))
    doc = f"""# Shipyard and fleet setup notices registered

{summary} COMMON 261–286 includes the restored ship ownership and build availability messages, the flagship confirmation and the two fleet-selection instructions. The short captain choice is retained. The admiral question uses the original two name getters and wraps without splitting “as admiral?”. [Release and patch](../{PACKAGE.as_posix()}/README.md) · [Registered review](../{REVIEW.as_posix()})

Two original Syracuse paths verified Buy through ship naming and the Fleet Setup and Disband pickers. The disband replay covered both the original cancellation and the dock result on an isolated copy of an existing regional-fleet save. All 28 stored modal variants passed independent pixel checks and were viewed. Local news and the admiral appointment samples passed offline. Hardware testing remains pending.

COMMON 267 was already credited. The debt warning in 284 still lacks an original DS caller. The clean and current bytes, prior wording and exact call references are recorded in the [source review](../{OUTPUT.as_posix()}). Continue the next reachable discovery, reward and acquisition exchanges. Keep 318, 284, the unresolved legacy setup prompts and the three Market replies open, along with the remaining town, random and player-facing prose.
"""
    base.replace_checked(DOC, doc.encode('utf-8'))
    lead = f'# Current editorial checkpoint - 2026-11-11\n\n{summary}\n\nContinue from [the registered Shipyard and fleet setup notices]({DOC.name}).\n\n'.encode('utf-8')
    for name in ('editorial_handoff_current.md', 'editorial_efficiency_workflow.md', 'translation_progress.md'):
        path = Path('docs') / name
        base.replace_checked(path, lead + path.read_bytes())
    continuity = Path('docs/build_continuity_protocol.md')
    lead = f"""The 24 Shipyard and fleet setup notices are registered over Equipment and System with 745 entries, 114 accepted layers and 80 checks. Use \x60scripts/register_shipyard_fleet_setup_v1.py --register\x60 to stage and \x60--publish-prepared\x60 to publish. Preserve both original fleet list modes, the two name getters and separate modal parents, and the scoped local-news and admiral paragraph paths. The exact reconstruction, original purchase, fleet and dock transitions, and cold startup pass. [Registered checkpoint]({DOC.name})

"""
    base.replace_checked(continuity, lead.encode('utf-8') + continuity.read_bytes())
    print('Registered 745 entries and credited 24 Shipyard and fleet setup notices once.')


def register():
    source = checked_text(inspect.getsource(previous.register), {
        "'equipment-and-system-notices'": "'shipyard-and-regional-fleet-setup'",
        'Fourteen system and equipment notices are registered.': 'Twenty-four Shipyard and fleet setup notices are registered.',
        "'== 25985': '== 26333', '== 15438': '== 15699', '== 10547': '== 10634'":
            "'== 25985': '== 26357', '== 15438': '== 15716', '== 10547': '== 10641'",
        '"len(manifest[\'batches\']) == 743 and len(manifest[\'checks\']) == 78"':
            '"len(manifest[\'batches\']) == 744 and len(manifest[\'checks\']) == 79"',
        '"len(manifest[\'batches\']) == 744 and len(manifest[\'checks\']) == 79"':
            '"len(manifest[\'batches\']) == 745 and len(manifest[\'checks\']) == 80"',
        'release_stack_before_equipment_system.json': 'release_stack_before_shipyard_fleet_setup.json',
        'verified_captain_biographies_predecessor=predecessor, equipment_system_release=str(REVIEW)':
            'verified_equipment_system_predecessor=predecessor, shipyard_fleet_setup_release=str(REVIEW)',
        'Reviewed system and equipment notices, including the original removal result.':
            'Reviewed Shipyard and fleet setup notices with scoped name and town wrapping.',
        'release_stack.equipment_system.pending.json': 'release_stack.shipyard_fleet_setup.pending.json',
        'COMMON_329_EQUIPMENT_REMOVAL_WORD_WRAP': 'COMMON_261_279_SHIPYARD_FLEET_WORD_WRAP',
        'equipment_system_registered_successor_pipeline': 'shipyard_fleet_setup_registered_successor_pipeline',
        'registered_manifest_entries=744, accepted_layers=114, passing_release_checks=79, repository_tests=30':
            'registered_manifest_entries=745, accepted_layers=114, passing_release_checks=80, repository_tests=30',
        'Equipment/system registration staged and ready to publish.':
            'Shipyard and fleet setup registration staged and ready to publish.',
    })
    env = {**vars(previous), **globals()}
    exec(compile(source, __file__ + '::same-registered-release-transaction', 'exec'), env)
    env['register']()


def publish_prepared():
    source = checked_text(inspect.getsource(previous.publish_prepared), {
        'release_stack.equipment_system.pending.json': 'release_stack.shipyard_fleet_setup.pending.json',
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
