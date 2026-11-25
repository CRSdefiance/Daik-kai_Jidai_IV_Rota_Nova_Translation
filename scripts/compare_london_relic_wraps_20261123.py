"""Compare native formatting of the London relic rumor across runtime arguments."""

from argparse import ArgumentParser
from collections import Counter
from itertools import product
from struct import unpack

from scripts import verify_london_tavern_20261123 as london
from scripts.probe_tavern_conversations_v764 import format_case
from scripts.registered_editorial_runtime import original_machine
from scripts.registered_editorial_runtime_v2 import RegisteredRuntime


OUT = london.OUT.with_name("london_relic_tip_wrap_comparison_20261123.json")
DRAFTS = (
    "Oh, %s? Try %s %s and %s %s from here.",
    "%s? You might find it %s %s and %s %s of here.",
    "%s? I know it. Look %s %s and %s %s from here.",
    "%s? From here, try going %s %s and %s %s.",
    "Oh, %s? It may be %s %s and %s %s from here.",
)
FOLLOWUP_DRAFTS = (
    "%s? Try going %s %s and %s %s from here.",
    "%s? From here, try heading %s %s and %s %s.",
    "%s? I know it. Try heading %s %s and %s %s.",
    "%s? I know it. From here, go %s %s and %s %s.",
    "%s? You could try %s %s and %s %s from here.",
    "%s? You might find it %s %s, %s %s from here.",
    "%s? I know it. Look %s %s, %s %s from here.",
    "%s? Oh, yes. Try heading %s %s and %s %s.",
    "%s? Try looking %s %s, %s %s from here.",
    "%s? Try %s %s and %s %s from here.",
)
FOLLOWUP = OUT.with_name("london_relic_tip_wrap_comparison_followup_20261123.json")
KEY = 843
BASE = 0x02000000


def providers(cpu, call):
    def pointer(address):
        return unpack("<I", bytes(cpu.mem_read(address, 4)))[0]

    def string(address):
        window = bytes(cpu.mem_read(address, 256))
        value, _, _ = window.partition(b"\0")
        assert value and value.isascii() and len(value) < 32
        return value.decode("ascii")

    root = call(0xCB190)
    objects = []
    for index in range(218):
        obj = root + 4 + 20 * index
        getter = pointer(pointer(obj) + 8)
        objects.append(dict(index=index, getter=getter, name=string(call(getter - BASE, obj))))
    tables = {}
    for field, literal, expected in (
        ("north_south", 0x02058F08, ("north", "south")),
        ("east_west", 0x02058F10, ("east", "west")),
        ("distance", 0x02058F0C, ("a little", "far", "very far")),
    ):
        address = pointer(literal)
        values = tuple(string(pointer(address + 4 * i)) for i in range(len(expected)))
        assert values == expected
        tables[field] = dict(literal=literal, pointer=address, strings=values)
    return objects, tables


def measure(lines):
    result = Counter()
    for first, second in zip(lines, lines[1:]):
        end = first.split()[-1].lower()
        start = second.split()[0].lower().rstrip(".,!?")
        if end in ("little", "far") and start in ("north", "south", "east", "west"):
            result["split_qualifier_direction"] += 1
        if (end, start) in (("a", "little"), ("very", "far")):
            result["split_distance_qualifier"] += 1
    if len(lines) > 1 and len(lines[-1]) <= 12:
        result["short_final_row"] += 1
    return result


def case(cpu, template, args):
    return format_case(cpu, dict(message_id=KEY, english=template),
                       [arg.encode("ascii") for arg in args])


def main(drafts=DRAFTS, output=OUT):
    archive = london.read(london.OUT)
    receipt = london.observed.current.RELEASE
    release = london.read(receipt)
    assert archive["candidate_sha256"] == release["candidate_sha256"]
    ctx = RegisteredRuntime(receipt, release["own_registered_startup"], captain=3)
    exact, exact_call, _ = ctx.machine(ctx.arm, ctx.common, ctx.raw, ctx.plan)
    names, stock = providers(exact, exact_call)
    domain = [stock[field]["strings"] for field in ("distance", "north_south", "distance", "east_west")]
    original = london.common_rows(ctx.common, ctx.arm)[KEY].text.decode("ascii")
    assert original.startswith(" ") and original.count("%s") == 5
    candidates = (original[1:], *(s.ljust(len(original) - 1) for s in drafts))
    assert all(s.count("%s") == 5 and len(s) == len(original) - 1 for s in candidates)
    assert london.ITEM_ARGS[0] in {row["name"] for row in names}

    # Right-bound and staged overlay bytes are verified by RegisteredRuntime.
    # The full argument sweep uses the same captured machine without the per-instruction audit hook.
    cpu, _, _ = original_machine(ctx.arm, ctx.common, ctx.raw, ctx.plan)
    results = []
    for template in candidates:
        sample = case(exact, template, london.ITEM_ARGS)
        assert sample == case(cpu, template, london.ITEM_ARGS)
        counts = Counter()
        by_name = {}
        longest = None
        for row in names:
            name = row["name"]
            findings = Counter()
            for args in product((name,), *domain):
                result = case(cpu, template, args)
                lines = result["lines"]
                assert 1 <= len(lines) <= 4 and all(0 < len(line) <= 35 for line in lines)
                assert "four_row_width_bound" not in result["findings"]
                findings.update(measure(lines))
                findings[f"{len(lines)}_rows"] += 1
                if longest is None or sum(map(len, lines)) > sum(map(len, longest["lines"])):
                    longest = dict(arguments=args, lines=lines, formatted_hex=result["formatted_hex"])
            counts.update(findings)
            by_name[name] = dict(findings)
        assert longest is not None
        for args in (tuple(longest["arguments"]), ("Blue Oak Shield", "very far", "south", "very far", "west")):
            assert case(exact, template, args) == case(cpu, template, args)
        results.append(dict(template=template.rstrip(), displayed_london=sample, longest=longest,
                            counts=counts, counts_by_name=by_name))
        print(template.rstrip(), dict(counts), sample["lines"], flush=True)

    assert results[0]["displayed_london"]["lines"] == list(london.HOLDS[KEY][2])
    london.write(output, dict(registered_build=ctx.receipt(), source_gameplay=london.reference(london.OUT),
        native_item_names=names, stock_direction_arguments=stock, rendered_layouts_per_template=len(names) * 36,
        comparisons=results, candidate_changed=False, new_gameplay=False))


if __name__ == "__main__":
    cli = ArgumentParser(description=__doc__)
    cli.add_argument("--followup", action="store_true")
    main(FOLLOWUP_DRAFTS, FOLLOWUP) if cli.parse_args().followup else main()
