"""Route the remaining Power and received-gold calls through the regular digits."""

from inspect import getsource
from pathlib import Path

from ndspy.code import MainCodeFile

from scripts import register_victory_reward_wrap_20261121 as parent
from scripts import stage_victory_reward_digits_20261121 as rewards
from scripts.source_locked_derivation_v5118 import checked_text


base, native, number = parent.base, parent.native, rewards.number
ROOT = Path("work/power_and_gold_digits_20261121")
ROM, PROOF = ROOT / "Power_And_Gold_Digits_STAGED.nds", ROOT / "staged.json"
POWER, GOLD = 288, 311
ORIGINAL = rewards.ORIGINAL
OWNED = {
    POWER: (0x020397B8, 0x0204A348, 0x020BC148),
    GOLD: (0x020791F8,),
}
RUINS_POWER = 0x020610DC
SAMPLES = {
    POWER: tuple((v,) for v in (1, 9, 10, 105, 999, 1000, 999999999, 2147483647)),
    GOLD: tuple((v,) for v in (100, 110, 130, 190, 990, 1000, 999999999, 2147483647)),
}
REASONS = {
    POWER: "The game names the Power statistic and reports the amount gained. Preserve the same wording on every branch, including ruins discovery.",
    GOLD: "This Search result announces gold received. Keep the direct system wording and use the amount the game actually credited.",
}


def patch(arm, clean):
    reviewed = {r["message_ID"]: r for r in base.load(ORIGINAL)["records"] if r["message_ID"] in OWNED}
    assert reviewed.keys() == OWNED.keys()
    itcm = next(s for s in MainCodeFile(arm, number.BASE).sections if s.ramAddress == number.ITCM)
    helper = bytes(itcm.data[number.HELPER - number.ITCM:number.END - number.ITCM])
    assert helper.hex() == base.load(rewards.HELPER_PROOF)["helper_hex"]
    output, bindings = bytearray(arm), []
    for message, addresses in OWNED.items():
        native_calls = reviewed[message]["native_callers"]
        assert {r["call"] - 12 for r in native_calls} == set(addresses) | ({RUINS_POWER} if message == POWER else set())
        for call in native_calls:
            modal = call["call"]
            pc = modal - 12
            at = pc - number.BASE
            start = call["code_start"] - number.BASE
            span = bytes.fromhex(call["exact_hex"])
            assert clean[start:start + len(span)] == span
            assert number.target(arm, modal - number.BASE) == rewards.prior.WRAPPER
            if pc == RUINS_POWER:
                assert number.target(arm, at) == number.HELPER
                assert arm[start:at] == clean[start:at] and arm[at + 4:start + len(span)] == clean[at + 4:start + len(span)]
                continue
            assert arm[start:start + len(span)] == span and number.target(arm, at) == number.NUMBER
            previous = arm[at:at + 4]
            revised = number.assemble(f"bl {number.HELPER:#x}", pc)
            assert len(revised) == 4
            output[at:at + 4] = revised
            bindings.append(dict(message_ID=message, number_call=pc, modal_call=modal, original_hex=previous.hex(),
                                 revised_hex=revised.hex(), original_caller_span_sha256=native.digest(span)))
    result = bytes(output)
    for binding in bindings:
        offset = binding["number_call"] - number.BASE
        assert number.target(result, offset) == number.HELPER
        output[offset:offset + 4] = bytes.fromhex(binding["original_hex"])
    assert bytes(output) == arm and number.cache_plan(result) == number.cache_plan(arm)
    assert len(bindings) == 4
    return result, bindings


def main():
    source = checked_text(getsource(rewards.main), {
        'if n == 303:\n                assert formatted.count(b"\\n") == 2':
            'assert len(formatted.splitlines()) == 1',
        'original_call_bindings=calls, exact_parent_inverse=True, native_number_checks=allocations,':
            'original_call_bindings=calls, previously_fixed_ruins_call=RUINS_POWER, exact_parent_inverse=True, native_number_checks=allocations,',
        'complete victory reward pages.': 'complete Power and received-gold pages.',
    })
    env = vars(rewards) | globals()
    exec(compile(source, __file__ + "::power-and-gold-digit-check", "exec"), env)
    env["main"]()


if __name__ == "__main__":
    main()
