"""Use the original Square selection with a supplied sample-pitch voice."""

from argparse import ArgumentParser
from types import FunctionType, SimpleNamespace

from unicorn.arm_const import UC_ARM_REG_R0

from scripts import replay_square_samples_wraps_20261115 as earlier
from scripts import stage_square_and_market_reward_wraps_20261123 as stage


def replay(version):
    previous = stage.base.load(stage.parent.RELEASE)
    arm_sha = previous["target_ARM9_sha256"]
    stock_assign = FunctionType(earlier.missionary.assign.__code__,
        vars(earlier.missionary) | {"ARMS": (arm_sha,)})
    clean = stage.base.NdsImage.open(stage.CLEAN).read_file(stage.ARM)

    def assignment(arm, raw, request):
        assigned, receipt = stock_assign(arm, raw, request)
        spans = ((0x7E988, 0x7E9A0), (0x7EB24, 0x7EB64), (0x53F4C, 0x53F9C))
        assert all(arm[lo:hi] == clean[lo:hi] for lo, hi in spans)
        cpu = earlier.machine(arm)
        cpu.mem_write(earlier.BASE, assigned)
        actor = receipt["actor"]

        def get(fn, args):
            earlier.call(cpu, fn, args)
            return cpu.reg_read(UC_ARM_REG_R0)

        source = get(0x7EB24, (actor,))
        assert earlier.BASE <= source < earlier.BASE + len(assigned) - 0x1C
        addr = source + 0x1C
        off = addr - earlier.BASE
        assert get(0x7E988, (actor,)) == assigned[off] == 7
        assert get(0x53F4C, (actor, 0x021184A0)) == 673
        changed = assigned[:off] + b"\x05" + assigned[off+1:]
        assert sum(a != b for a, b in zip(raw, changed, strict=True)) == 4
        cpu.mem_write(earlier.BASE, changed)
        assert get(0x7E988, (actor,)) == 5
        assert get(0x53F4C, (actor, 0x021184C0)) == 663
        assert get(0x53F4C, (actor, 0x021184A0)) == 671
        receipt.update(after_RAM_sha256=earlier.sha256(changed).hexdigest(),
            only_three_declared_room_type_and_assignment_bytes_changed=False,
            only_four_declared_room_assignment_and_voice_bytes_changed=True,
            changes=[*receipt["changes"], dict(address=addr, before=7, after=5)],
            supplied_voice_style=5, original_confirmation=663, original_announcement=671)
        return changed, receipt

    root = stage.ROOT / f"{version}_square"
    root.mkdir()
    body = stage.base.load(stage.PROOF) if version == "new" else previous
    contract = root / "replay_contract.json"
    stage.base.save(contract, {name: body[name] for name in ("candidate_sha256", "target_ARM9_sha256")})
    rom = stage.ROM if version == "new" else stage.parent.ROM
    settings = SimpleNamespace(ROOT=root, ROM=rom, STORED=contract)
    runner = FunctionType(earlier.main.__code__, vars(earlier) | dict(stage=settings, sample_fixture=lambda: assignment))
    runner("samples")


if __name__ == "__main__":
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("version", choices=("old", "new"))
    replay(parser.parse_args().version)
