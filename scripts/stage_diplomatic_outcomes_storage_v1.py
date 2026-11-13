"""Verify the reviewed diplomacy notices through their stored native templates."""

import inspect
from hashlib import sha256
from pathlib import Path
from types import FunctionType

from dk4tool.patch.diplomatic_outcome_wrap_v1 import transform
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import DIRECTORY_OFFSET, TABLE_OFFSET
from scripts.audit_story_glyph_consistency import load, save
from scripts.checkpoint_diplomatic_outcomes_v1 import OUTPUT, RELEASE
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.preflight_diplomatic_outcome_wrap_v1 import PROOF
from scripts.preflight_literal_notice_formatting_v1 import run_case
from scripts.preflight_shared_crew_notices_v1 import with_components
from scripts.registered_editorial_runtime_v2 import RegisteredRuntime
from scripts.seal_shared_text_source_v1 import ARM, COMMON, reference
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.stage_shared_notices_storage_v1 import relocate


TARGET = Path('work/SharedText_20261110_v1/diplomatic_outcomes_wrap_v1')
ROM = TARGET / 'diplomatic_outcomes_RESEARCH_ONLY.nds'
RECEIPT = TARGET / 'stored_verification.json'


def stored_case_runner():
    source = checked_text(inspect.getsource(run_case), {
        '        u.reg_write(UC_ARM_REG_R1, test)':
            '        assert bytes(u.mem_read(ptr, len(template) + 1)) == template + b"\\0"',
        'original_storage_unmodified=True': 'actual_stored_template_pointer_used=True',
        'scratch_template_test_before_widget_creation=True': 'stopped_before_widget_creation=True',
    })
    env = dict(run_case.__globals__)
    exec(compile(source, __file__ + '::stored-template', 'exec'), env)
    return env['run_case']


def main():
    assert not ROM.exists() and not RECEIPT.exists()
    manuscript, preflight, release = load(OUTPUT), load(PROOF), load(RELEASE)
    assert digest(OUTPUT) == preflight['manuscript_sha256']
    runtime = RegisteredRuntime(RELEASE, release['own_registered_startup'], captain=3)
    assert runtime.receipt() == manuscript['registered_input'] == preflight['registered_input']
    wrapped, ownership = transform(runtime.arm)
    assert ownership == json_round_trip_ownership(preflight['research_ARM9'])
    rows = {row['message_ID']: row for row in manuscript['records']}
    storage = {n: row['english'].encode('ascii') for n, row in rows.items()}
    directory = sha256(runtime.arm[DIRECTORY_OFFSET:TABLE_OFFSET]).hexdigest()
    repack = FunctionType(relocate.__code__, {**relocate.__globals__, 'DIRECTORY': directory})
    common, arm, entries, packing = repack(runtime.common, wrapped, rows, storage)
    staged = with_components(runtime, arm, common)
    run_stored = stored_case_runner()
    checks = []
    for previous in preflight['cases']:
        n = previous['message_ID']
        row = rows[n] | {'current_hex': storage[n].hex()}
        actual = run_stored(staged, row, previous['arguments'])
        staged.calls.clear()
        assert actual['native_wrapper_output_hex'] == previous['native_wrapper_output_hex']
        assert actual['expanded_hex'] == previous['expanded_hex']
        checks.append(dict(message_ID=n, arguments=actual['arguments'],
            expanded_hex=actual['expanded_hex'], display_hex=actual['native_wrapper_output_hex'],
            exact_stored_template_and_original_wrapper=True))
    assert len(checks) == preflight['complete_cases']

    image = NdsImage.open(runtime.rompath)
    image.replace_file(ARM, arm)
    image.replace_file(COMMON, common)
    with ROM.open('xb') as stream:
        stream.write(image.rom.save())
    image.replace_file(ARM, runtime.arm)
    image.replace_file(COMMON, runtime.common)
    assert sha256(image.rom.save()).hexdigest() == release['candidate_sha256']
    staged_image = NdsImage.open(ROM)
    assert staged_image.read_file(COMMON) == common and staged_image.read_file(ARM) == arm
    references = [dict(message_ID=n, source=rows[n]['source_reference'],
        previous=rows[n]['current_reference'], staged=reference(entries[n]),
        staged_hex=storage[n].hex()) for n in rows]
    save(RECEIPT, dict(
        registered_input=runtime.receipt(), research_ROM=str(ROM), research_ROM_sha256=digest(ROM),
        target_ARM9_sha256=sha256(arm).hexdigest(), target_COMMON_sha256=sha256(common).hexdigest(),
        storage=packing, wrapper=ownership, complete_serialized_ROM_parent_inverse=True,
        stored_cases=checks, exact_record_references=references,
        display_bytes_match_reviewed_contact_sheets=True, gameplay_observed=False,
        native_confirmation_widget_and_final_formatting_gate_pending=True,
        new_credit=0, evidence={str(p): digest(p) for p in (OUTPUT, PROOF, Path(__file__))},
    ))
    print(f'{len(rows)} stored notices and {len(checks)} native expansion checks pass. Research ROM only.')


def json_round_trip_ownership(proof):
    return proof | {key: tuple(proof[key]) for key in ('notice_IDs', 'yes_no_IDs')}


if __name__ == '__main__':
    main()
