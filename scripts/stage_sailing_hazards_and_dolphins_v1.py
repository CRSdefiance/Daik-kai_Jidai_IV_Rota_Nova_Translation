"""Check the sailing exchange paragraphs through the original portrait consumers."""

from hashlib import sha256
from inspect import getsource
from pathlib import Path
from types import FunctionType

from keystone import KS_ARCH_ARM, KS_MODE_ARM, Ks
from ndspy.code import MainCodeFile

from dk4tool.patch import compact_portrait_selector_v1 as compact
from dk4tool.script.common_message_table import DIRECTORY_OFFSET, TABLE_END, TABLE_OFFSET
from scripts import review_sailing_hazards_and_dolphins_v1 as review
from scripts import stage_fleet_reports_v1 as prior
from scripts import stage_oasis_and_whale_reports_v1 as previous
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.stage_mutiny_review_v1 import PARENTS


ARM, COMMON, BASE, OUTPUT = review.ARM, review.COMMON, review.BASE, review.OUTPUT
ROOT = Path('out/sailing_hazards_and_dolphins_staged_20261111_v1')
ROM = ROOT / 'sailing_hazards_and_dolphins_RESEARCH_ONLY.nds'
PROOF = ROOT / 'stored_verification.json'
PHRASES = {
    2366: ("in our ship's log?",),
    2367: ('A pod of dolphins!', "in the ship's log?"),
    2368: ('a pod of dolphins over there!', "in the ship's log?"),
    2369: ('May I write about them', "in the ship's log?"),
    2370: ('Can we put it', "in the ship's log?"),
    2371: ('What a sight!', "in the ship's log?"),
    2372: ('So many dolphins!', "in the ship's log.", 'Can I, Admiral?'),
    2377: ("That was soothing, wasn't it?",),
    2380: ('a quiet moment', 'now and then.'),
    2385: ("I'm losing my mind!",),
    2386: ("What's that voice?", "I'm losing my mind!"),
    2387: ("I'm going mad!",),
    2388: ('H-help me!', "I'm going mad!"),
    2392: ('swallowing the ship!',),
    2393: ('swallow our ship!',),
    2395: ('swallowing the ship!',),
    2405: ("We're caught in the tornado!",),
    2407: ("The ship's being pulled in!",),
    2408: ("The tornado's swallowing us!",),
    2410: ("The whirlpool's got us!",),
    2411: ("We're being sucked", 'into a whirlpool!'),
    2419: ("We can't turn in time!",),
    2421: ("We won't turn in time!",),
}


def extend_owned_scopes(arm, additions, receipt):
    selector = receipt['selector']
    fallback = receipt['previous_selector']
    guard = receipt['shared_existing_static_guard']['address']
    original = {tuple(key): tuple(values) for key, values in receipt['literal_scopes']}
    dynamic = {tuple(key): tuple(values) for key, values in receipt['dynamic_scopes']}
    assert all(set(values).isdisjoint(original.get(key, ()) + dynamic.get(key, ()))
               for key, values in additions.items())
    extended = original | {key: original.get(key, ()) + tuple(values) for key, values in additions.items()}
    asm = Ks(KS_ARCH_ARM, KS_MODE_ARM)
    old = bytes(asm.asm(compact.assembly(original, dynamic, fallback, guard), selector)[0])
    new = bytes(asm.asm(compact.assembly(extended, dynamic, fallback, guard), selector)[0])
    code = MainCodeFile(arm, BASE)
    assert bytes(code.save()) == arm and len(code.sections) == 6
    itcm, tail = code.sections[-2:]
    assert not tail.bssSize and tail.ramAddress == 0x01FFD000
    at = selector - tail.ramAddress
    hook = receipt['hook'] - itcm.ramAddress
    assert bytes(itcm.data[hook:hook + 4]) == bytes(asm.asm(f'b {selector:#x}', receipt['hook'])[0])
    assert len(old) == receipt['selector_bytes'] and bytes(tail.data[at:]) == old
    assert selector + len(new) <= BASE and guard < selector and fallback < selector
    tail.data[at:] = new
    target = bytes(code.save())
    inverse = MainCodeFile(target, BASE)
    assert bytes(inverse.sections[-1].data[at:]) == new
    inverse.sections[-1].data[at:] = old
    assert bytes(inverse.save()) == arm
    return target, extended, dynamic, dict(selector=selector, old_bytes=len(old), selector_bytes=len(new),
        source_ARM9_sha256=sha256(arm).hexdigest(), target_ARM9_sha256=sha256(target).hexdigest(),
        previous_selector=fallback, hook=receipt['hook'], existing_guard=guard,
        complete_serialized_ARM9_parent_inverse=True)


def stage(runtime, release, rows, groups, verified=None):
    assert sha256(runtime.arm).hexdigest() == release['target_ARM9_sha256']
    assert all(row['original_substitution_count'] == 0 for row in rows.values())
    compile_layouts = prior.prior.prior.compile_layouts
    compiler = FunctionType(compile_layouts.__code__, compile_layouts.__globals__ | {
        'PHRASES': {number: phrases for number, phrases in PHRASES.items() if len(rows[number]['english']) > 36},
    })
    storage = compiler(rows)
    additions = {}
    for group in groups:
        if not any(b'\n' in storage[number] for number in range(group['first_ID'], group['last_ID'] + 1)):
            continue
        caller, = group['native_callers']
        key = PARENTS[caller['consumer'] - BASE]
        additions.setdefault(key, []).append(group['table'])
    receipt = review.prior.load(review.parent.VERIFICATION / 'stored_verification.json')['ownership']
    wrapped, static, dynamic, ownership = extend_owned_scopes(runtime.arm, additions, receipt)
    relocate = prior.prior.prior.relocate
    directory = sha256(runtime.arm[DIRECTORY_OFFSET:TABLE_OFFSET]).hexdigest()
    repack = FunctionType(relocate.__code__, relocate.__globals__ | {'DIRECTORY': directory})
    common, arm, rebound, allocation = repack(runtime.common, wrapped, rows, storage)
    assert allocation['all_41_blocks_fit_8KiB']
    assert arm[:DIRECTORY_OFFSET] == wrapped[:DIRECTORY_OFFSET] and arm[TABLE_END:] == wrapped[TABLE_END:]
    if verified is None:
        checks = previous.verify_scope(arm, static, dynamic, receipt['previous_selector'],
                                      receipt['shared_existing_static_guard']['original_failed_guard_target'])
    else:
        assert ownership['target_ARM9_sha256'] == verified['ownership']['target_ARM9_sha256']
        checks = verified['ownership']['selector_checks']
    return arm, common, storage, rebound, allocation, ownership | dict(
        added_literal_scopes=list(additions.items()), literal_scopes=list(static.items()),
        dynamic_scopes=list(dynamic.items()), selector_checks=checks)


def main():
    source = checked_text(getsource(prior.main), {
        'assert len(records) == 47 and len(pages) == 89': 'assert len(records) == 59 and len(pages) == 59',
    })
    environment = vars(prior) | globals()
    exec(compile(source, __file__ + '::sailing-portrait-checks', 'exec'), environment)
    environment['main']()


if __name__ == '__main__':
    main()
