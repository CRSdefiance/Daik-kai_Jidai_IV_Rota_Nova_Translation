"""Stage exact viewed sea-event layouts while preserving other portrait dispatch."""

from hashlib import sha256
import inspect
from itertools import product
from pathlib import Path
import re
from types import FunctionType

from dk4tool.patch import sea_event_static_wrap_v1 as wrap
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import DIRECTORY_OFFSET, TABLE_OFFSET
from scripts.audit_story_glyph_consistency import load, save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.preflight_shared_crew_notices_v1 import with_components
from scripts.probe_button_prompt_native import machine
from scripts.registered_editorial_runtime_v2 import RegisteredRuntime
from scripts.review_sea_event_wrap_plan_v1 import PROOF
from scripts.seal_shared_text_source_v1 import ARM, COMMON, reference
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.stage_sea_event_review_v1 import EVIDENCE as PREVIOUS, OUTPUT, RELEASE, native_stored
from scripts.stage_shared_notices_storage_v1 import relocate
from scripts.verify_shared_crew_selector_v1 import ARGS, dispatch


ROOT = Path('out/sea_events_20261110_v2')
ROM = ROOT / 'sea_events_balanced_RESEARCH_ONLY.nds'
EVIDENCE = ROOT / 'stored_balanced_verification.json'


def verify_scope(arm):
    cpu = machine(arm)
    source = checked_text(inspect.getsource(dispatch), {'count=128': 'count=1024'})
    env = dict(dispatch.__globals__)
    exec(compile(source, __file__ + '::longer-selector-bound', 'exec'), env)
    run_dispatch = env['dispatch']
    candidate_parents = (*wrap.TABLES, 0x02053C5C, 0x02053D24, 0x02053F40, 0x02053EF4, 0x02054014)
    candidates = {0x02116730, 0x02116EE0, 0x02117000, 0x021187E0, 0x02118980, 469}
    for table in (*wrap.TABLES[wrap.QUEUED], *wrap.TABLES[wrap.CAPTAIN]):
        candidates.update((table - 4, table, table + 4))
    texts = (b' Ordinary paragraph', b' Exact break\n  Second row',
             b'No leading space\n  Second row', b' Unprotected break\nSecond row')
    selected = tested = 0
    for parent, table, text in product(candidate_parents, sorted(candidates), texts):
        cpu.mem_write(ARGS[1], text + b'\0')
        stack = {0x264: parent, 0x270: table, 0x274: table, 0x27C: table}
        active = table in wrap.TABLES.get(parent, ()) and text == texts[1]
        target, registers = run_dispatch(cpu, wrap.HOOK, stack, (wrap.PRIOR, wrap.LITERAL_COPY))
        assert target == (wrap.LITERAL_COPY if active else wrap.PRIOR), (parent, table, text)
        assert registers == ARGS
        tested += 1
        selected += active
    assert selected == 13
    return dict(tested=tested, selected=selected, other_dispatches_rejoin_earlier_selector=True,
        original_registers_stack_and_LR_preserved=True)


def main():
    assert not ROOT.exists()
    source, previous, plan, release = map(load, (OUTPUT, PREVIOUS, PROOF, RELEASE))
    runtime = RegisteredRuntime(RELEASE, release['own_registered_startup'], captain=3)
    assert source['registered_input'] == previous['registered_input'] == runtime.receipt()
    assert digest(previous['research_ROM']) == plan['candidate_sha256'] == previous['research_ROM_sha256']
    assert plan['evidence'][str(OUTPUT)] == digest(OUTPUT) and plan['evidence'][str(PREVIOUS)] == digest(PREVIOUS)
    for sheet in (*previous['contact_sheets'], *plan['contact_sheets']):
        assert digest(sheet['path']) == sheet['sha256']
    old = {case['message_ID']: case for case in previous['cases']}
    balanced = {case['message_ID']: case for case in plan['records']}
    assert len(old) == 98 and len(balanced) == 26 and set(balanced) <= set(old)
    storage = {n: bytes.fromhex(balanced[n]['proposed_display_hex'] if n in balanced else case['staged_hex'])
               for n, case in old.items()}
    assert all(not re.search(rb'%|F[AIOU]|IC', storage[n]) for n in balanced)
    target_arm, owner = wrap.transform(runtime.arm)
    scope = verify_scope(target_arm)
    directory = sha256(runtime.arm[DIRECTORY_OFFSET:TABLE_OFFSET]).hexdigest()
    rows = {row['message_ID']: row for row in source['records']}
    groups = {row['first_ID']: row for row in source['exact_native_event_groups']}
    repack = FunctionType(relocate.__code__, {**relocate.__globals__, 'DIRECTORY': directory})
    common, arm, entries, packing = repack(runtime.common, target_arm, rows, storage)
    target = with_components(runtime, arm, common)
    tracked_case = checked_text(inspect.getsource(native_stored), {
        '0x02132020}': '0x02132020, scoped_literal_address}',
    })
    env = {**native_stored.__globals__, 'scoped_literal_address': wrap.LITERAL_COPY}
    exec(compile(tracked_case, __file__ + '::existing-literal-copy-path', 'exec'), env)
    check_stored = env['native_stored']
    cases = []
    for n, row in rows.items():
        before = old[n]
        assert row['source_reference'] == before['source_reference'] and row['current_reference'] == before['current_reference']
        case = check_stored(target, row, groups[row['native_group_first_ID']], storage[n])
        final_hex = case.pop('display').hex()
        expected = balanced[n]['proposed_display_hex'] if n in balanced else before['display_hex']
        assert final_hex == expected, (n, bytes.fromhex(final_hex), bytes.fromhex(expected), case)
        if n in balanced:
            assert case['native_formatter_addresses'] == [wrap.LITERAL_COPY]
        cases.append(case | dict(display_hex=final_hex, staged_hex=storage[n].hex(),
            source_reference=row['source_reference'], current_reference=row['current_reference'],
            staged_reference=reference(entries[n]), exact_viewed_ink_sha256=(
                balanced[n]['ink_sha256'] if n in balanced else before['native_ink_sha256'])))

    image = NdsImage.open(runtime.rompath)
    image.replace_file(ARM, arm)
    image.replace_file(COMMON, common)
    ROOT.mkdir()
    with ROM.open('xb') as stream:
        stream.write(image.rom.save())
    image.replace_file(ARM, runtime.arm)
    image.replace_file(COMMON, runtime.common)
    assert sha256(image.rom.save()).hexdigest() == release['candidate_sha256']
    reopened = NdsImage.open(ROM)
    assert reopened.read_file(ARM) == arm and reopened.read_file(COMMON) == common
    save(EVIDENCE, dict(
        registered_input=runtime.receipt(), research_ROM=str(ROM), research_ROM_sha256=digest(ROM),
        target_ARM9_sha256=sha256(arm).hexdigest(), target_COMMON_sha256=sha256(common).hexdigest(),
        storage=packing, selector=owner, selector_scope=scope, complete_serialized_ROM_parent_inverse=True,
        cases=cases, ordinary_boundaries_retained=plan['ordinary_boundaries_retained'],
        exact_viewed_original_pages=72, exact_viewed_balanced_pages=26, logical_text_unchanged_from_review=True,
        actual_gameplay=False, staged_no_release_credit=True,
        evidence={str(path): digest(path) for path in (OUTPUT, PREVIOUS, PROOF, Path(__file__))}))
    print(f"{len(cases)} stored cases match their viewed layouts; {scope['tested']} native selector cases pass.")


if __name__ == '__main__':
    main()
