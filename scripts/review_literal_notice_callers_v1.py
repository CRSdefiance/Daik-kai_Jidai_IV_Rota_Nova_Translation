"""Review the exact shared notice and fleet-order callers in the registered runtime."""

import re
from collections import Counter
from pathlib import Path

from unicorn.arm_const import UC_ARM_REG_LR, UC_ARM_REG_PC, UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3, UC_ARM_REG_SP

from dk4tool.rom.nds import NdsImage
from scripts.audit_story_glyph_consistency import load, save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.probe_button_prompt_native import BASE, STACK, STOP
from scripts.registered_editorial_runtime_v2 import RegisteredRuntime


ARCHIVE = Path('translations/editorial_checkpoints/SharedText_20261110_v1')
OUTPUT = ARCHIVE / 'literal_notice_context_and_runtime.json'
CALLS = Path('work/analysis/native_common_arm_calls_wrappers_clean.json')
RELEASE = Path('work/lil261_B323_B335_release_v1/registered_release_verification.json')
STARTUP = RELEASE.with_name('own_registered_startup_verification.json')
WRAPPERS = {BASE+0x546B8: 'notice', BASE+0x5466C: 'yes-no', BASE+0x54624: 'yes-no-with-extra-control'}
DECISIONS = [
    [
        85,
        "We can sail for about %s days.",
        "The current fragment can read as time already spent at sea. The native call formats a computed estimate. Use a clear future-tense range notice."
    ],
    [
        86,
        None,
        "Keep the established month/day, separate status row and departure message. The original fourth port argument is passed on the stack and stays last."
    ],
    [
        87,
        "Not enough %s.",
        "The caller supplies the named requirement. The Japanese reports insufficient quantity. Missing incorrectly suggests it is entirely absent."
    ],
    [
        88,
        None,
        "The concise status keeps the destruction of the whole enemy fleet and the source's emphatic tone."
    ],
    [
        89,
        None,
        "The current line accurately conveys enemy retreat and distinguishes it from fleet destruction."
    ],
    [
        90,
        None,
        "Keep the source's subdued ellipsis and the named town as the target of defeat. The current status reads naturally."
    ],
    [
        91,
        None,
        "The short surrender notice keeps the different outcome and subdued tone. Its trailing blank line belongs to display review."
    ],
    [
        92,
        None,
        "The speakerless yes/no offer is polite and fluent. The native flow searches affiliated fleets before asking and can handle more than one report. Keep the plural phrasing."
    ],
    [
        93,
        "The city of %s is firing on %s's fleet.",
        "The city is the attacker, and the second value is the fleet's owner. The source describes ongoing fire, with no claim it has just begun."
    ],
    [
        94,
        "%s is under attack by the pirate %s!",
        "The original call passes the city first and the pirate second. Replace the disconnected fragments with one clear sentence in the same order."
    ],
    [
        95,
        "In %s, %s sold large amounts of %s and expanded their market share!",
        "Preserve the established trade wording and order of place, seller and commodity. Normalize the initial full-width I."
    ],
    [
        96,
        None,
        "The original call reads the player company object and passes its name. The possessive correctly names whose share fell. Do not reinterpret it as a city argument."
    ],
    [
        112,
        None,
        "The existing notice accurately reports missing system data. Its extra newline and padding are separate from the wording. Two direct native routes are present, including a lookup and a modal."
    ],
    [
        118,
        None,
        "The current wording accurately identifies corrupted system data. The original failure branch also invokes the separate fallback explanation in 122."
    ],
    [
        120,
        None,
        "Everything correct? is a natural short confirmation. The original setup branch invokes a yes/no modal and preserves the prior selection state on the negative route."
    ],
    [
        121,
        "Start the game?",
        "The source asks whether to start. The current native copy returns a fragment from the unrelated save warning. Restore the confirmation at the original yes/no call."
    ],
    [
        122,
        "Couldn't load the system data. The game will start with default system data.",
        "The current native copy starts in the middle of the same save warning. Restore the source's load failure and subsequent initialization. The caller continues startup after the notice."
    ],
    [
        123,
        None,
        "The current standalone load failure preserves the source. Keep it distinct from missing or corrupted data and from the notice that also says startup will continue."
    ],
    [
        125,
        None,
        "The sentence preserves both the substantial investment and the resulting economic recovery."
    ],
    [
        126,
        None,
        "The existing economic boom notice naturally conveys the stronger outcome and retains its investment cause."
    ],
    [
        127,
        None,
        "The existing command clearly asks the player to choose a base city. The native selection route keeps this distinct from patrol and docking."
    ],
    [
        128,
        None,
        "The refusal clearly identifies the missing contract with the selected city. Its negative predicate is distinct from the already-contracted refusal."
    ],
    [
        129,
        None,
        "The two natural sentences give the patrol target and the requirement for a contract. Keep the city terminology shared by the fleet orders."
    ],
    [
        130,
        "Choose a city where you have a contract. The fleet will dock there.",
        "State clearly that the contract is with the city and the fleet will dock there. The native branch is the port-call order."
    ],
    [
        131,
        None,
        "The short command names the city as the attack target and fits the related selection prompts."
    ],
    [
        132,
        None,
        "The existing sentence accurately distinguishes an already signed contract from the absence of a contract."
    ],
    [
        133,
        None,
        "The existing line correctly attributes the city's contract to a faction the player is not at war with. Keep that distinction."
    ],
    [
        134,
        None,
        "The current wording clearly describes a city with no contract with a faction at war with the player."
    ],
    [
        135,
        "The people here are furious. There's no way in or out right now.",
        "The source says public anger makes entering or leaving impossible. The current warning softens the restriction and drops the exit sense. Keep the temporal situation implicit in right now."
    ],
    [
        136,
        "Choose a shop sign to ask about trends and other local news.",
        "Restore the shop-sign instruction and the source's broader information about trends. Use the native formatter for ordinary line breaks."
    ]
]


def bindings(clean, current, inventory, number):
    candidates = [r for r in inventory['calls'] if r['message_id'] == number]
    assert candidates
    result = []
    for row in candidates:
        assert row['component'] == 'arm9' and row['argument_register'] == 'r0'
        start = row['file_offset'] - 24
        end = row['file_offset'] + 4
        assert current[start:end] == clean[start:end]
        result.append(dict(call_PC=row['runtime_address'], target=row['target'],
            reference_start=BASE+start, source_andcurrent_hex=clean[start:end].hex(),
            source_context=row['context'], presentation=WRAPPERS.get(row['target'], 'direct-original-COMMON-lookup')))
    return result


def current_copy(ctx, row, target):
    cpu, get, provider = ctx.machine(ctx.arm, ctx.common, ctx.raw, ctx.plan)
    number = row['message_ID']
    cpu.reg_write(UC_ARM_REG_SP, STACK)
    cpu.reg_write(UC_ARM_REG_LR, STOP)
    cpu.reg_write(UC_ARM_REG_R0, number)
    for index, reg in enumerate([UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3]):
        at = 0x02660000 + index*32
        cpu.mem_write(at, f'test-argument-{index+1}'.encode('ascii')+b'\0')
        cpu.reg_write(reg, 1 if target == BASE+0x54624 and index == 0 else at)
    if number == 86:
        at = 0x02660060
        cpu.mem_write(at, b'test-argument-4\0')
        cpu.mem_write(STACK, at.to_bytes(4, 'little'))
    stop = BASE+0x54774 if target in WRAPPERS else STOP
    cpu.emu_start(target, stop, count=1000000)
    assert cpu.reg_read(UC_ARM_REG_PC) == stop
    pointer = cpu.reg_read(UC_ARM_REG_R1 if target in WRAPPERS else UC_ARM_REG_R0)
    raw = bytes.fromhex(row['current_hex'])
    assert bytes(cpu.mem_read(pointer, len(raw)+1)) == raw+b'\0', number
    assert bytes(cpu.mem_read(ctx.actor_root, 0x1A04)) == ctx.actor_bytes
    return dict(wrapper=target, terminal_PC=stop, buffer_pointer=pointer, copied_hex=raw.hex(),
        mode=cpu.reg_read(UC_ARM_REG_R0) if target in WRAPPERS else None,
        file_reads=provider.reads, exact_instruction_count=len(provider.executed_current),
        original_loader_and_wrapper_to_native_format_entry=True)


def main():
    assert not OUTPUT.exists()
    comparison = ARCHIVE / 'contextual_comparison_pending_consumers.json'
    prior, inventory = load(comparison), load(CALLS)
    ctx = RegisteredRuntime(RELEASE, STARTUP, captain=3)
    assert ctx.release['candidate_sha256'] == prior['candidate_sha256']
    clean_path = Path('work/clean.nds')
    assert digest(clean_path) == inventory['source_rom_sha256']
    source_arm = NdsImage.open(clean_path).read_file('/__arm9__.bin')
    input_rows = {r['message_ID']: r for r in prior['records']}
    records = []
    for number, replacement, finding in DECISIONS:
        row = input_rows[number]
        calls = bindings(source_arm, ctx.arm, inventory, number)
        results = [current_copy(ctx, row, entry) for entry in sorted({r['target'] for r in calls})]
        retained = replacement is None
        english = row['current_English'].strip() if retained else replacement
        if number == 86:
            english = '{LB}'.join(line.strip() for line in english.splitlines())
        assert english.count('%s') == bytes.fromhex(row['source_hex']).count(b'%s')
        assert english.isascii() and (number == 86 or '\n' not in english)
        records.append(dict(id=row['id'], message_ID=number, file_path=row['file_path'],
            source_reference=row['source_reference'], current_reference=row['current_reference'],
            source_hex=row['source_hex'], current_hex=row['current_hex'], source_Japanese=row['clean_Japanese'],
            current_English=row['current_English'], english=english, speaker='Speakerless system notice',
            decision='retention' if retained else 'revision', source_meaning=row['finding'],
            context=finding, localization_note=finding, manual_break_reason=(
                'The original date, status and departure details are separate display fields.' if number == 86 else ''),
            native_callers=calls, current_copies=results, native_substitution_count=english.count('%s'),
            review=dict(source=True, context=True, localization=True, naturalness=True, formatting=False),
            formatting_and_representative_display_pending=True, source_activation_or_actual_gameplay_not_claimed=True,
            new_credit=0))
    assert len(records) == 30
    assert len({r['message_ID'] for r in records}) == 30
    counts = dict(Counter(r['decision'] for r in records))
    remaining = sorted(set(input_rows)-{r['message_ID'] for r in records})
    save(OUTPUT, dict(records=records, counts=counts, original_native_copy_cases=sum(len(r['current_copies']) for r in records),
        remaining_compared_message_IDs=remaining, not_yet_classified_as_unused=remaining,
        separate_levelup_andpunctuation_3_source_leads_still_pending=True,
        source_and_registered_source_callers_bound=True, runtime=ctx.receipt(), current_source_andcomparison=str(comparison),
        translation_policy='natural-dialogue-v2', encoder='dialogue-relocatable-v1', target_locale='en-US',
        review_gates=['source','context','localization','naturalness','formatting'],
        review_status='four gates passed, native formatting, representative display and release pending',
        native_calls_stop_before_modal_layout_and_use_test_arguments=True, no_new_gameplay_or_review_credit=True,
        evidence={str(p):digest(p) for p in [comparison, CALLS, RELEASE, STARTUP, Path(__file__)]}, full_goal_complete=False))
    print(f'Bound and reviewed {len(records)} shared messages, {counts}, with all native source copies verified.')


if __name__ == '__main__':
    main()
