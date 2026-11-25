"""Compile the guild dialogue over the relocated registered forest candidate."""

from collections import defaultdict
from types import FunctionType

from dk4tool.script.format_safety_relocated_v2 import bind_registered_story_percent_guard
from scripts import review_london_guild_assignments_20261118 as review


paired = review.paired
base, native, stage, parent = paired.base, paired.native, paired.stage, paired.parent
ROOT = paired.ROOT / "research_v4"
ROM = ROOT / "London_And_Malacca_Guild_Assignments_RESEARCH_ONLY.nds"
PROOF = ROOT / "stored_proof.json"
PLANNER = stage.progressive.layout.PLANNER
VIRTUAL_SPEAKER = b"\x02"


def plan_progressive(row, selector, current, original):
    logical = row["english"]
    norm = stage.progressive.layout.prior.layout.norm

    def markup(text):
        return review.TOKEN.sub(lambda match: "{MACRO:" + match[0] + "}", text)

    def longest(text):
        return text.replace("{MACRO:FA}", "W" * 16).replace("{MACRO:FI}", "W" * 16)

    def pairs(phrases):
        return [(norm(a), norm(b)) for term in phrases for a, b in zip(term.split(), term.split()[1:])]

    # Rebuilding the native owner allows ordinary wrapping to use the full
    # available width. The virtual field supplies a planning budget, not ROM padding.
    template = markup(logical)
    budget = b" " * (len(template) + 32)
    record = dict(id=row["id"], kind="progressive", source_selector=2,
        source_hex=(VIRTUAL_SPEAKER + original).hex(), current_hex=(VIRTUAL_SPEAKER + budget).hex(),
        english="{SPEAKER:02}" + template, protected_pairs=pairs(map(markup, row["protected_phrases"])))
    planner = FunctionType(PLANNER.__code__, PLANNER.__globals__ | {"display": longest})
    plan = planner(record)
    encoded = bytes.fromhex(plan["encoded_hex"])
    assert encoded[:1] == VIRTUAL_SPEAKER
    body = encoded[1:]
    assert review.logical(body.decode("ascii")) == logical
    assert not any(d["severity"] == "error" for d in plan["diagnostics"])
    assert all(any(markup(p).casefold() in line.casefold() for line in plan["lines"])
               for p in row["protected_phrases"])
    assert plan["expected_native_pages"] == 1 and all(len(longest(line)) <= 36 for line in plan["lines"])
    return body, plan | dict(logical_English=logical, source_selector=selector,
        planning_record=dict(source_hex=(bytes([selector]) + original).hex()),
        encoded_hex=(bytes([selector]) + body).hex(),
        maximum_expanded_FI_FA_length=16)


def rebuild_function():
    env = vars(stage) | {"plan_progressive": plan_progressive}
    for function in (stage.changed_speech, stage.changed_styles, stage.rebuild):
        env[function.__name__] = FunctionType(function.__code__, env)
    return env["rebuild"]


def main():
    assert not ROOT.exists()
    manuscript, packet, release = map(base.load, (review.OUTPUT, review.SOURCE, parent.RELEASE))
    assert manuscript["source_packet_sha256"] == base.digest(review.SOURCE)
    assert manuscript["previous_sha256"] == packet["candidate_sha256"] == base.digest(parent.ROM)
    assert manuscript["previous_registry_sha256"] == release["registry_sha256"] == base.digest(base.REGISTRY)
    ctx = native.RegisteredRuntime(parent.RELEASE, release["own_registered_startup"], captain=3)
    clean = base.NdsImage.open(native.CLEAN)
    target = base.NdsImage.open(parent.ROM)
    assert base.digest(native.CLEAN) == release["clean_input_sha256"]
    inventory, _, _ = native.scoped_inventory()
    clean_arm = clean.read_file(native.ARM)
    painter = stage.system.native_painter(ctx)
    rebuild = rebuild_function()
    groups = defaultdict(list)
    packet_groups = {(g["file_path"], g["block"]): g for g in packet["groups"]}
    for row in manuscript["records"]:
        groups[row["file_path"], row["block"]].append(row)
    assert groups.keys() == packet_groups.keys()
    initial = native.files(target)
    verified, changed = [], defaultdict(list)
    for route in range(4):
        file = f"/data/SC{route}.DK4"
        source_bank = native.IlnkContainer.parse(clean.read_file(file))
        archive = native.IlnkContainer.parse(initial[file])
        original_blocks = list(archive.blocks)
        for n in paired.BLOCKS[route]:
            current, source = archive.blocks[n], source_bank.blocks[n]
            item = packet_groups[file, n]
            assert native.digest(source) == item["source_block_sha256"]
            assert native.digest(current) == item["current_block_sha256"]
            rows = groups[file, n]
            value, receipts, plans = rebuild(rows, source, current, inventory, clean_arm, ctx.arm, painter)
            assert bool(value != current) == any(r["decision"] == "revision" for r in rows)
            if current != value:
                archive.blocks[n] = value
                changed[file].append(n)
            verified.append(dict(route=route, file_path=file, block=n, before=native.digest(current),
                after=native.digest(value), source=native.digest(source), commands=receipts, plans=plans))
        packed = archive.to_bytes()
        archive.blocks[:] = original_blocks
        assert archive.to_bytes() == initial[file]
        target.replace_file(file, packed)

    final = native.files(target)
    assert initial.keys() == final.keys()
    assert {p for p in initial if initial[p] != final[p]} == changed.keys()
    guard = base.load(base.REGISTRY)["profiles"][release["profile"]]["source25_multiarchive_guard"]
    controls = bind_registered_story_percent_guard(guard)(native.files(clean), final)
    assert controls["total_exact_source_bound_relocated_leading25_count"] == 7
    assert not any(controls["source_bound_new_command_counts"].values())
    payload = bytes(target.rom.save())
    for file in changed:
        target.replace_file(file, initial[file])
    assert bytes(target.rom.save()) == parent.ROM.read_bytes()
    ROOT.mkdir()
    ROM.write_bytes(payload)
    base.save(PROOF, dict(candidate_sha256=base.digest(ROM), predecessor_sha256=release["candidate_sha256"],
        manuscript_sha256=base.digest(review.OUTPUT), clean_sha256=release["clean_input_sha256"], groups=verified,
        changed_blocks=changed, whole_parent_inverse=True, source25=controls, stored_check_only=True))
    print("Assembled all revised guild exchanges with exact relative branches and whole-ROM inverse.", flush=True)


if __name__ == "__main__":
    main()
