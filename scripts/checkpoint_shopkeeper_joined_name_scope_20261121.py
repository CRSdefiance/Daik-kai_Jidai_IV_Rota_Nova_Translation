"""Bind joined shopkeeper name scope to the retail scripts and Forces view."""

from collections import Counter
from json import dumps, loads
from pathlib import Path
import re
from struct import unpack_from

from unicorn.arm_const import UC_ARM_REG_FP, UC_ARM_REG_PC, UC_ARM_REG_R7, UC_ARM_REG_SB

from scripts import checkpoint_joined_actor_names_20261119 as earlier
from scripts import reconcile_shared_display_20261121 as shared
from scripts import register_hodram_execution_20261121 as current
from scripts.registered_editorial_runtime_v2 import RegisteredRuntime


base, native = current.parent.base, current.parent.native
BASE = earlier.BASE
OUTPUT = earlier.OUTPUT.with_name("shopkeeper_joined_name_scope_20261121_v1.json")
ROLE = Path("translations/square_shopkeeper_labels_contextual_final_review_v1.json")
LEADER_CHART = Path("releases/all_routes_editorial_20261120_forces_chart_fields_candidate/verification/registered_review.json")
JOIN_ACTION = re.compile(rb"\x00\xA0\xFF\xFF")
JOIN_HANDLER = (0x2BB18, 0x2BDC8)
JOIN_DISPATCH = (0x2BE8C, 0x2BF84)
FORCE_LEADER_PATH = (0x8CECC, 0x8CF30)
JOINED_NAME = 0x7EA8C
SHOPKEEPERS = (82, 83)
JOIN_NOTICE = 341


def retail_actions(rom):
    arm = rom.read_file(shared.ARM)
    inventory, _, _ = native.scoped_inventory()
    groups = []
    for n in range(4):
        path = f"/data/SC{n}.DK4"
        archive = rom.read_file(path)
        blocks = native.IlnkContainer.parse(archive).blocks
        rows, scanned = [], 0
        for index, block in enumerate(blocks):
            candidates = {m.start() for m in JOIN_ACTION.finditer(block, 8)
                if m.start()+8 <= len(block) and unpack_from("<I", block, m.start()+4)[0] >> 28 == 2}
            if not candidates:
                continue
            scanned += 1
            commands, _ = inventory(arm, block)
            matches = [cmd for cmd in commands if cmd["offset"] in candidates and cmd["word"] == 0xA000]
            assert {cmd["offset"] for cmd in matches} == candidates
            block_sha = native.digest(block)
            for cmd in matches:
                at = cmd["offset"]
                packed, = unpack_from("<I", block, at + 4)
                assert cmd["native_extent"] == 8 and bytes.fromhex(cmd["whole_command_hex"]) == block[at:at+8]
                rows.append(dict(block=index, command_offset=at, byte_hex=cmd["whole_command_hex"],
                    block_sha256=block_sha, actor_ID=packed & 0xFF, joins_company=bool(packed & (1 << 16)),
                    enclosing_0100_controls=cmd["ancestor_0100_offsets"]))
        groups.append(dict(route=n, archive=path, sha256=native.digest(archive),
            blocks_total=len(blocks), blocks_with_action_candidates=scanned, actions=rows))
    return groups


def name_domains(runtime, originals, actors):
    cpu, get, provider = runtime.machine(runtime.arm, runtime.common, runtime.raw, runtime.plan)
    actor_root = get(0xCB184)
    force_root = get(0xCB160)
    captain = get(0x7F244)
    assert captain == 3 and actor_root == runtime.actor_root
    actor_memory = bytes(cpu.mem_read(actor_root, 0x1A04))
    force_memory = bytes(cpu.mem_read(force_root, 4+20*76))

    def actor(n):
        return actor_root + (0x19E4 if n == captain else 4+32*n)

    def read(pointer):
        return earlier.labels.read_text(cpu, pointer)

    recruits = []
    for n in sorted(actors):
        obj = actor(n)
        name = read(get(JOINED_NAME, obj))
        assert name == originals[n]["short_and_joined"]["joined_full"]["text"] and name.isascii()
        recruits.append(dict(actor_ID=n, actor_pointer=obj, getter=BASE+JOINED_NAME, exact_joined_name=name))
    stock = []
    start, stop = [BASE + v for v in FORCE_LEADER_PATH]
    for index in range(20):
        source_index = get(0x3CD78, force_root+4+index*76)
        assert 0 <= source_index < 207
        cpu.reg_write(UC_ARM_REG_SB, index)
        cpu.emu_start(start, stop, count=2000)
        assert cpu.reg_read(UC_ARM_REG_PC) == stop
        obj, pointer = [cpu.reg_read(reg) for reg in (UC_ARM_REG_R7, UC_ARM_REG_FP)]
        assert obj == actor(source_index)
        name = read(pointer)
        assert name.isascii()
        stock.append(dict(company_index=index, actor_ID=source_index, actor_object=obj,
            name_pointer=pointer, joined_leader_name=name))
    assert not set(SHOPKEEPERS) & {r["actor_ID"] for r in stock}
    shop_names = []
    for n in SHOPKEEPERS:
        entry = originals[n]
        obj = actor(n)
        views = {k: read(get(v, obj)) for k, v in earlier.GETTERS.items()}
        assert views == {k: item["text"] for k, item in entry["short_and_joined"].items()}
        assert views["dialogue"] == views["catalogue"] == "Shopkeeper"
        shop_names.append(dict(actor_ID=n, actor_pointer=obj, getter_results=views,
            original_company_ID=get(0x7E958, obj), original_availability=get(0x7DB14, obj)))
    assert [r["original_company_ID"] for r in shop_names] == [21, 21]
    assert bytes(cpu.mem_read(actor_root, len(actor_memory))) == actor_memory
    assert bytes(cpu.mem_read(force_root, len(force_memory))) == force_memory
    assert not provider.reads
    return recruits, stock, shop_names


def main():
    assert not OUTPUT.exists()
    release = base.load(current.RELEASE)
    assert base.digest(current.ROM) == release["candidate_sha256"]
    assert base.digest(shared.CLEAN) == release["clean_input_sha256"]
    assert base.digest(base.REGISTRY) == release["registry_sha256"]
    with current.parent.mapped(base.LEDGER) as ledger:
        assert current.parent.value(ledger, "current_integrated_candidate", 1)["sha256"] == release["candidate_sha256"]
    runtime = RegisteredRuntime(current.RELEASE, release["own_registered_startup"], captain=3)
    clean = base.NdsImage.open(shared.CLEAN)
    ja = clean.read_file(shared.ARM)
    spans = (JOIN_HANDLER, JOIN_DISPATCH, FORCE_LEADER_PATH, (0x7EA48, 0x7EB3C), (0x7ED88, 0x7EE08))
    assert all(ja[a:b] == runtime.arm[a:b] for a, b in spans)
    references = earlier.native_references(runtime.image, runtime.arm)
    old = base.load(earlier.OUTPUT)
    assert loads(dumps(references)) == old["caller_references"]
    clean_groups, installed_groups = map(retail_actions, (clean, runtime.image))
    unique_joiners = set()
    counts = Counter()
    for left, right in zip(clean_groups, installed_groups, strict=True):
        key = lambda r: (r["block"], r["byte_hex"], r["actor_ID"], r["joins_company"])
        assert [key(r) for r in left["actions"]] == [key(r) for r in right["actions"]]
        for row in right["actions"]:
            counts["join" if row["joins_company"] else "leave"] += 1
            if row["joins_company"]:
                unique_joiners.add(row["actor_ID"])
            assert row["actor_ID"] not in SHOPKEEPERS
    assert counts == {"join": 86, "leave": 2}
    originals = {r["actor_ID"]: r for r in old["actor_output_inventory"]}
    recruits, chart, shop_names = name_domains(runtime, originals, unique_joiners)
    source = shared.workflow.common_message_entries(clean.read_file(shared.COMMON), ja)[JOIN_NOTICE]
    installed = shared.entries(runtime.image)[JOIN_NOTICE]
    assert unpack_from("<I", runtime.arm, 0x2BDD0) == (JOIN_NOTICE,)
    assert source.text.decode("cp932") == "%sが\n仲間になりました！"
    assert installed.text.strip() == b"%s joined!" and installed.text.count(b"%s") == 1
    review = {r["actor_ID"]: r for r in base.load(ROLE)["records"]}
    for row in shop_names:
        ident = row["actor_ID"]
        previous = originals[ident]
        assert all(review[ident]["review"].values()) and review[ident]["english"] == "Shopkeeper"
        row.update(clean_role=previous["clean_role"], clean_secondary_metadata=previous["clean_and_current_regional_secondary_field"],
            english_nameplate="Shopkeeper", decision="retain the plain occupation",
            reason="The Square and the customer exchange establish the role. The scene does not introduce a personal name.")
    dependencies = (Path(__file__), ROLE, earlier.OUTPUT, LEADER_CHART, current.RELEASE, Path(release["own_registered_startup"]))
    base.save(OUTPUT, dict(candidate_sha256=release["candidate_sha256"], clean_sha256=release["clean_input_sha256"],
        caller_reference_census=references, checked_native_code_hashes=[dict(start=lo,end=hi,sha256=native.digest(ja[lo:hi])) for lo,hi in spans],
        source_retail_archive_actions=clean_groups, current_retail_archive_actions=installed_groups, scripted_counts=dict(counts),
        original_forces_chart_stock_leader_paths=chart, original_script_recruit_joined_names=recruits,
        retained_square_nameplates=shop_names, join_notice=dict(ID=JOIN_NOTICE, source_reference=shared.workflow.reference(source),
            current_reference=shared.workflow.reference(installed), source_hex=source.text.hex(), current_hex=installed.text.hex(),
            decision="retention", reason="The short system announcement names the recruit and confirms the change without adding rank or a personal relationship."),
        scope="Offline original command boundaries, original initialized stock Forces chart selector and original name getters. "
              "Other potential Deck or conditional receivers remain open.", new_gameplay_runs=0, new_editorial_credit=0,
        evidence={str(p): base.digest(p) for p in dependencies}))
    print(f"Bound {sum(counts.values())} authored crew effects, {len(recruits)} recruited names and {len(chart)} Forces chart leader paths.")


if __name__ == "__main__":
    main()
