"""Qualify the existing Azores sentence alias for the developed-town docking prompt."""

from inspect import getsource
from pathlib import Path
from struct import pack, pack_into

from ndspy.code import MainCodeFile

from dk4tool.patch.main_pool_cache_visibility import POOL, STAGE, cache_plan
from scripts import stage_azores_wording_20261123 as prior
from scripts.observe_azores_return_20261123 import TOWN_NAME_CALL, VISIT
from scripts.reconcile_class_names_20261123 import word
from scripts.reconcile_queued_sailing_hints_20261123 import ARM, BASE, CLEAN, REGISTRY, RELEASE
from scripts.reconcile_queued_sailing_hints_20261123 import NdsImage, digest, read, reference, write
from scripts.source_locked_derivation_v5118 import checked_text
from scripts import verify_azores_wording_20261123 as native
from scripts.verify_lisbon_azores_voyage_20261123 import load_exact, text_at
from scripts.verify_personal_gameplay_v841 import get_machine


ROOT = Path(".codex-release-work/azores_return_20261123")
ROM = ROOT / "Azores_Return_STAGED.nds"
PROOF = ROOT / "stored_proof.json"
OFFSET = prior.RETIRED_CACHE_OFFSET
ENTRY = POOL + OFFSET
ALIAS = ENTRY + 52
SITE = TOWN_NAME_CALL - BASE
VILLAGE_SITES = tuple(BASE + site for _, site, _, _ in prior.NAME_CALLS)


def wrapper():
    instructions = pack("<11I", 0xE92D4070, 0xE12FFF31, 0xE10F5000,
        0xE59F4018, 0xE1500004, 0x159F4014, 0x11500004, 0x028F0010,
        0xE128F005, 0xE8BD4070, 0xE12FFF1E)
    return instructions + pack("<2I", prior.AZORES_VILLAGE, prior.AZORES_TOWN) + b"the Azores\0\0"


def patch(arm, clean):
    code = MainCodeFile(arm, BASE)
    assert bytes(code.save()) == arm
    main, staged = code.sections[0].data, code.sections[3]
    old_stage = bytes(staged.data)
    assert code.sections[0].ramAddress == BASE and staged.ramAddress == STAGE
    assert old_stage[OFFSET:OFFSET + 64] == prior.name_wrapper(ENTRY)
    assert arm[SITE - 0x18:SITE + 0x18] == clean[SITE - 0x18:SITE + 0x18]
    assert word(main, TOWN_NAME_CALL) == 0xE12FFF31
    for site in VILLAGE_SITES:
        assert word(main, site) == prior.branch_link(site, ENTRY)
    replacement = wrapper()
    assert len(replacement) == 64
    pack_into("<I", main, SITE, prior.branch_link(TOWN_NAME_CALL, ENTRY))
    staged.data[OFFSET:OFFSET + len(replacement)] = replacement
    result = bytes(code.save())
    assert cache_plan(result) == cache_plan(arm) and len(result) == len(arm)
    restored = MainCodeFile(result, BASE)
    pack_into("<I", restored.sections[0].data, SITE, 0xE12FFF31)
    restored.sections[3].data[OFFSET:OFFSET + 64] = old_stage[OFFSET:OFFSET + 64]
    assert bytes(restored.save()) == arm
    return result


def check_arguments(original, revised, snapshot):
    old_cpu, get = get_machine(original, snapshot)
    new_cpu, _ = get_machine(revised, snapshot)
    new_cpu.mem_write(ENTRY, wrapper())
    new_cpu.mem_write(TOWN_NAME_CALL, revised[SITE:SITE + 4])
    assert text_at(snapshot, ENTRY + 44) == b"the Azores"
    assert text_at(bytes(new_cpu.mem_read(BASE, len(snapshot))), ALIAS) == b"the Azores"
    villages, towns = get(0xCB118), get(0xCB178)
    groups = [dict(site=site, objects=[get(0xCACAC, villages, i) for i in range(24)],
                   previous_azores=ENTRY + 44, azores_index=13) for site in VILLAGE_SITES]
    groups.append(dict(site=TOWN_NAME_CALL, objects=[towns + 4 + i * 108 for i in range(114)],
                       previous_azores=prior.AZORES_TOWN, azores_index=103))
    # Some town virtual methods make nested calls. LR is volatile and the
    # docking function restores its own return address from its stack frame.
    abi_scope = vars(native).copy()
    abi_source = checked_text(getsource(native.native_call), {
        "    assert cpu.reg_read(registers.UC_ARM_REG_LR) == site + 4\n": "",
    })
    exec(compile(abi_source, __file__ + "::town-getter-abi", "exec"), abi_scope)
    native_call = abi_scope["native_call"]
    proof = []
    for group in groups:
        site = group["site"]
        for index, obj in enumerate(group["objects"]):
            getter = word(snapshot, word(snapshot, obj) + 8)
            natural = get(getter - BASE, obj)
            assert (natural in (prior.AZORES_TOWN, prior.AZORES_VILLAGE)) == (index == group["azores_index"])
            before = group["previous_azores"] if index == group["azores_index"] else natural
            after = ALIAS if index == group["azores_index"] else natural
            for flags in range(16):
                registers = 0x1F | flags << 28
                current, old_flags = native_call(old_cpu, site, obj, getter, registers)
                target, new_flags = native_call(new_cpu, site, obj, getter, registers)
                assert (current[0], target[0]) == (before, after)
                assert current[1:] == target[1:] and old_flags == new_flags
        proof.append(dict(site=site, checked_objects=len(group["objects"]), all_16_flag_states=True,
                          azores_index=group["azores_index"], other_name_pointers_exact=True))
    assert bytes(old_cpu.mem_read(BASE, len(snapshot))) == snapshot
    expected = bytearray(snapshot)
    expected[ENTRY - BASE:ENTRY - BASE + 64] = wrapper()
    expected[SITE:SITE + 4] = revised[SITE:SITE + 4]
    assert bytes(new_cpu.mem_read(BASE, len(snapshot))) == expected
    return proof


def main():
    assert not ROM.exists() and not PROOF.exists()
    receipt = read(RELEASE)
    assert digest(REGISTRY) == receipt["registry_sha256"]
    assert digest(receipt["candidate"]) == receipt["candidate_sha256"]
    assert digest(CLEAN) == receipt["clean_input_sha256"]
    candidate, clean = map(NdsImage.open, (receipt["candidate"], CLEAN))
    original = candidate.read_file(ARM)
    assert prior.digest_bytes(original) == receipt["target_ARM9_sha256"]
    revised = patch(original, clean.read_file(ARM))
    capture = read(VISIT)
    assert capture["ROM_sha256"] == receipt["candidate_sha256"]
    snapshot, = [row for row in capture["read_only_pause_RAM_snapshots"] if row["frame"] == 13600]
    states = check_arguments(original, revised, load_exact(snapshot))

    candidate.replace_file(ARM, revised)
    data = bytes(candidate.rom.save())
    candidate.replace_file(ARM, original)
    assert bytes(candidate.rom.save()) == Path(receipt["candidate"]).read_bytes()
    ROOT.mkdir(parents=True, exist_ok=True)
    ROM.write_bytes(data)
    write(PROOF, dict(candidate=str(ROM), candidate_sha256=digest(ROM),
        verified_predecessor_sha256=receipt["candidate_sha256"], parent=reference(RELEASE),
        only_internal_change=ARM, whole_parent_inverse=True, target_ARM9_sha256=prior.digest_bytes(revised),
        cache_plan_unchanged=True, wrapper_hex=wrapper().hex(), wrapper=ENTRY, alias_address=ALIAS,
        existing_calls=list(VILLAGE_SITES), added_call=TOWN_NAME_CALL, case_groups=states,
        native_case_count=sum(group["checked_objects"] for group in states) * 16, source_snapshot=snapshot,
        gameplay_pending=True, release_registration_pending=True))
    print(f"Staged and qualified {ROM}.")


if __name__ == "__main__":
    main()
