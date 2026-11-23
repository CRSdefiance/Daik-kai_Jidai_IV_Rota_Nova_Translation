"""Verify the revised lookout page in the original focused bubbles voyage."""

from inspect import getsource
from struct import pack, unpack
from types import FunctionType

from scripts import run_sea_event_bubbles_focused_v2 as prior
from scripts import stage_bubble_portrait_wraps_20261120 as stage
from scripts.source_locked_derivation_v5118 import checked_text


base = stage.base
LIVE = stage.ROOT / 'focused_bubbles'
TABLE = 0x118840
ORIGINAL_LINE, REVISED_LINE = 457, 461
old_setter = FunctionType(prior.set_condition.__code__, vars(prior) | {'ROM': stage.ROM})


def set_condition(arm, raw, request):
    edited, provenance = old_setter(arm, raw, request)
    original = arm[TABLE:TABLE + 32]
    slots = unpack('<8I', original)
    assert ORIGINAL_LINE in slots and REVISED_LINE in slots
    alternate = pack('<8I', *(REVISED_LINE if key == ORIGINAL_LINE else key for key in slots))
    selecting = request['mode'] == 'choose-bubbles'
    before, after = (original, alternate) if selecting else (alternate, original)
    assert raw[TABLE:TABLE + len(before)] == before
    result = edited[:TABLE] + after + edited[TABLE + len(after):]
    zone = range(TABLE, TABLE + len(before))
    changes = [dict(address=prior.BASE + at, before=raw[at], after=result[at])
               for at in zone if raw[at] != result[at]]
    assert changes
    return result, provenance | dict(
        changes=provenance['changes'] + changes, shared_lookout_table=prior.BASE + TABLE,
        original_lookout_message=ORIGINAL_LINE, supplied_message=REVISED_LINE,
        voice_variant_forced=True, restored_table=not selecting)


def run(output, setter_reference, *, rom=stage.ROM, proof=stage.PROOF):
    source = checked_text(getsource(prior.main), {
        "staged['research_ROM_sha256']": "staged['candidate_sha256']",
        "    first = dict(until=8727, condition_fixture={'mode': 'choose-bubbles'}, buttons=['UP'], duration=400)\n"
        "    navigation.write_text(json.dumps(first) + '\\n', encoding='utf-8')":
            "    navigation.write_bytes(HISTORICAL_COMMANDS.read_bytes())",
        'from scripts.run_sea_event_bubbles_focused_v2 import set_condition':
            setter_reference,
    })
    env = vars(prior) | dict(OUT=output, ROM=rom, EVIDENCE=proof,
                              HISTORICAL_COMMANDS=prior.OUT / 'commands.jsonl')
    exec(compile(source, __file__ + '::focused-lookout', 'exec'), env)
    env['main']()


if __name__ == '__main__':
    run(LIVE, 'from scripts.replay_bubble_portrait_wraps_20261120 import set_condition')
