"""Register the verified faction and epilogue notices over Discovery and Rewards."""

import argparse
import inspect
import json
from pathlib import Path

from scripts import register_setup_save_equipment_v1 as previous
from scripts import stage_faction_and_epilogue_v2 as stage
from scripts.register_discovery_rewards_v1 import RELEASE as PARENT
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.verify_faction_and_epilogue_v1 import BOOT as STARTUP_VERIFICATION
from scripts.verify_faction_and_epilogue_v1 import CHECKPOINT, LIVE as LIVE_VERIFICATION, QA


base = previous.base
PROFILE = 'all-routes-faction-epilogue-editorial-v1-20261111'
FAMILY = 'faction_and_epilogue_contextual_20261111'
CHECK = 'registered_faction_and_epilogue_native_live_and_complete_parent_inverse'
PACKAGE = Path('releases/all_routes_editorial_20261111_faction_and_epilogue_candidate')
VERIFICATION = PACKAGE / 'verification'
RELEASE = VERIFICATION / 'registered_release_verification.json'
REVIEW = VERIFICATION / 'registered_review.json'
MUTATION_PLAN = VERIFICATION / 'registration_mutation_plan.json'
TEST = Path('out/faction_and_epilogue_registered_20261111_v1')
ROM = TEST / 'Translation_DS_All_Routes_Faction_and_Epilogue_20261111_candidate.nds'
MANIFEST = ROM.with_suffix('.manifest.json')
PATCH = PACKAGE / 'translation.xdelta'
DOC = Path('docs/editorial_faction_and_epilogue_registered_20261111.md')
PENDING_LEDGER = TEST / 'editorial_review_current.faction_and_epilogue.pending.json'
OUTPUT, EVIDENCE, RESEARCH = stage.previous.MANUSCRIPT, stage.PROOF, stage.ROM
PREVIOUS_TOTAL, TOTAL, REVISED, RETAINED = 26371, 7, 6, 1


def rebuild(parent, evidence, source):
    code = checked_text(inspect.getsource(previous.rebuild), {
        "assert owner == evidence['ownership']": "assert json.loads(json.dumps(owner)) == evidence['ownership']",
        "rows = {row['message_ID']: row for row in source['records'] if row['message_ID'] != 318}":
            "rows = stage.active_rows(source)",
        'stage.transform': 'stage.previous.transform',
        'stage.relocate': 'stage.previous.previous.relocate',
        'stage.reference': 'stage.previous.previous.reference',
    })
    env = {**vars(previous), **globals()}
    exec(compile(code, __file__ + '::same-owned-payload-and-parent-inverse', 'exec'), env)
    return env['rebuild'](parent, evidence, source)


def verification_scope(approved, live):
    assert approved['observed_ids'] == live['observed_ids'] == [342, 343, 344, 345]
    assert approved['stored_records'] == 7 and approved['viewed_pages'] == 16
    assert len(live['selector_positive_and_negative_cases']) == 12
    assert len(live['original_panel_holds']) == len(live['original_A_dismissals']) == 4
    assert len(live['original_game_over_return']) == 3
    assert live['fixture']['only_two_state_bytes_changed']
    return dict(observed_notice_IDs=live['observed_ids'], stored_records=7, modal_variants=16,
        directly_viewed_modal_pages=16, original_four_panels_and_game_over=True,
        fixture_scope='The active Hodram save was booted normally. Two isolated state bytes selected the original epilogue before the original display and A transitions.',
        earned_ending=False, offline_only_notice_IDs=[334, 335, 337],
        retained_wording_wrap_repaired=343, unbound_common_IDs=[330, 331, 332, 333, 336], hardware=False)

def final_review(source, evidence, scope):
    assert evidence['editorial_amendments'] == json.loads(json.dumps(stage.AMENDMENTS))
    updated = source | {'records': list(stage.active_rows(source).values())}
    env = {**vars(previous), **globals()}
    exec(compile(inspect.getsource(previous.final_review), __file__ + '::exact-natural-dialogue-review', 'exec'), env)
    result = env['final_review'](updated, evidence, scope)
    retained, = [row for row in result['records'] if row['decision'] == 'retention']
    assert retained['message_ID'] == 343
    case, = [row for row in evidence['rendered_variants'] if row['message_ID'] == 343]
    assert case['retained_prose_layout_changed'] and len(case['previous_native_lines']) == 1
    retained['layout_revised_without_prose_revision'] = True
    retained['original_native_pre_widget_lines'] = case['previous_native_lines']
    retained['registered_native_lines'] = case['lines']
    return result


def publish(release):
    summary = 'The seven faction and epilogue notices are registered. The ledger now credits 26,378 reviews.'
    notes = f"""# All Routes Faction and Epilogue candidate

Use the local ROM `{ROM.as_posix()}` beside its build manifest. The [clean-input patch](translation.xdelta) applies to clean Japanese SHA-256 `{release['clean_input_sha256']}` and reconstructs SHA-256 `{release['candidate_sha256']}` byte for byte. Patch SHA-256 is `{release['patch_sha256']}`.

{summary} The naval attack alert reads naturally with the sampled faction names. The modal level-up matches the floating notice’s wording, and the faction dissolution result keeps its original name getter. The epilogue preserves the four native panels, fixes mid-word wraps, and replaces the mismatched capital I.

An isolated Hodram emulator fixture set two state bytes to select the original epilogue. Its four complete panels, four A dismissals and Game Over screen passed. All 16 stored variants were visually reviewed, including the four stock captain and faction pairs. The naval attack, modal level-up and faction dissolution were checked offline. All 82 release checks, 30 targeted tests, cold startup and 24 protected name getters passed. [Gameplay proof](verification/faction_and_epilogue_gameplay_verification.json) · [Exact record review](verification/registered_review.json)
"""
    (PACKAGE / 'README.md').write_text(notes, encoding='utf-8', newline='\n')
    base.save(PACKAGE / 'checksums.json', {p.relative_to(PACKAGE).as_posix(): base.digest(p)
        for p in sorted(PACKAGE.rglob('*')) if p.is_file() and p.name != 'checksums.json'})
    pin_path = Path('translations/rom_retention_pins.json')
    pins = base.load(pin_path)
    for path, role in ((stage.previous.ROM, 'first epilogue research ROM'),
                       (RESEARCH, 'refined epilogue research ROM'), (ROM, 'registered epilogue ROM')):
        assert not any(row['path'] == str(path.resolve()) for row in pins)
        pins.append(dict(path=str(path.resolve()), reason=f'Preserve {role}. SHA256 {base.digest(path)}'))
    base.replace_checked(pin_path, (json.dumps(pins, ensure_ascii=False, indent=2) + '\n').replace('\n', '\r\n').encode('utf-8'))
    doc = f"""# Faction and epilogue notices registered

{summary} Six revisions improve the attack alert, level-up, dissolution and epilogue. One retention preserves “passed away after a full and eventful life.” The predecessor split “eventful” and “passed” between rows. The revised runtime wraps complete words and retains the original narrator pause after the first panel. [Release and patch](../{PACKAGE.as_posix()}/README.md) · [Registered review](../{REVIEW.as_posix()})

A two-byte fixture entered the original four-panel epilogue after an ordinary Hodram battery-save replay. All four live framebuffer and formatter-buffer checks passed, followed by the original Game Over screen. All 16 stored variants were reviewed visually. The three other notices and the alternate captains’ displays were checked offline. No earned ending or hardware verification is recorded.

The [source review](../{OUTPUT.as_posix()}) preserves the original callers and unbound Options records 330–333 and stat notice 336. Continue with the full shark exchange around COMMON 2425–2453 and bind its conditional groups and speakers. Keep the other unresolved notices, Market replies, later technical re-audit and artwork in their existing queues.
"""
    base.replace_checked(DOC, doc.encode('utf-8'))
    lead = f'# Current editorial checkpoint - 2026-11-11\n\n{summary}\n\nContinue from [the registered faction and epilogue notices]({DOC.name}).\n\n'.encode('utf-8')
    for name in ('editorial_handoff_current.md', 'editorial_efficiency_workflow.md', 'translation_progress.md'):
        path = Path('docs') / name
        base.replace_checked(path, lead + path.read_bytes())
    continuity = Path('docs/build_continuity_protocol.md')
    lead = f"""The seven faction and epilogue notices are registered over Discovery and Rewards with 747 entries, 114 accepted layers and 82 checks. Use `scripts/register_faction_and_epilogue_v1.py --register` to stage and `--publish-prepared` to publish. Keep the original raw dissolution wrapper and the four epilogue calls in order. The exact reconstruction, epilogue Game Over transition and cold startup pass. [Registered checkpoint]({DOC.name})

"""
    base.replace_checked(continuity, lead.encode('utf-8') + continuity.read_bytes())
    print('Registered 747 entries and credited seven faction and epilogue notices once.')

def register():
    source = checked_text(inspect.getsource(previous.register), {
        "'equipment-and-system-notices'": "'faction-and-epilogue-notices'",
        'Fourteen system and equipment notices are registered.': 'Seven faction and epilogue notices are registered.',
        "'== 25985': '== 26333', '== 15438': '== 15699', '== 10547': '== 10634'":
            "'== 25985': '== 26378', '== 15438': '== 15734', '== 10547': '== 10644'",
        '"len(manifest[\'batches\']) == 743 and len(manifest[\'checks\']) == 78"':
            '"len(manifest[\'batches\']) == 746 and len(manifest[\'checks\']) == 81"',
        '"len(manifest[\'batches\']) == 744 and len(manifest[\'checks\']) == 79"':
            '"len(manifest[\'batches\']) == 747 and len(manifest[\'checks\']) == 82"',
        'release_stack_before_equipment_system.json': 'release_stack_before_faction_and_epilogue.json',
        'verified_captain_biographies_predecessor=predecessor, equipment_system_release=str(REVIEW)':
            'verified_discovery_rewards_predecessor=predecessor, faction_and_epilogue_release=str(REVIEW)',
        'Reviewed system and equipment notices, including the original removal result.':
            'Reviewed faction and epilogue notices with scoped native paragraph wrapping.',
        'release_stack.equipment_system.pending.json': 'release_stack.faction_and_epilogue.pending.json',
        'COMMON_329_EQUIPMENT_REMOVAL_WORD_WRAP': 'COMMON_FACTION_AND_EPILOGUE_WORD_WRAP',
        'equipment_system_registered_successor_pipeline': 'faction_and_epilogue_registered_successor_pipeline',
        'registered_manifest_entries=744, accepted_layers=114, passing_release_checks=79, repository_tests=30':
            'registered_manifest_entries=747, accepted_layers=114, passing_release_checks=82, repository_tests=30',
        'Equipment/system registration staged and ready to publish.':
            'Faction and epilogue registration staged and ready to publish.',
    })
    env = {**vars(previous), **globals()}
    exec(compile(source, __file__ + '::same-registered-release-transaction', 'exec'), env)
    env['register']()


def publish_prepared():
    source = checked_text(inspect.getsource(previous.publish_prepared), {
        'release_stack.equipment_system.pending.json': 'release_stack.faction_and_epilogue.pending.json',
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
