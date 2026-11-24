"""Install only COMMON 863 and check the stored caller, format and release inputs."""

from argparse import ArgumentParser
from inspect import getsource
from pathlib import Path
from types import FunctionType, SimpleNamespace

from scripts import preflight_tavern_sighting_rumor_20261124 as review
from scripts import stage_tunis_shop_advice_20261124 as shared
from scripts.probe_battle_aftermath_fonts_v1256 import consumer
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.stage_cartridge_title_20261123 import NdsImage, digest, read, reference, write


trend, panels, KEY = shared.trend, review.panels, review.KEY
played = SimpleNamespace(RELEASE=review.RELEASE)
ROOT = Path("E:/Rota Nova translations/Generated/work/editorial_20261124_tavern_sighting_rumor")
ROM = ROOT / "Tavern_Sighting_Rumor_STAGED.nds"
STORED, NATIVE = ROOT / "stored_proof.json", ROOT / "installed_native.json"
PATCH, REBUILT, PATCH_PROOF = [ROOT / name for name in ("translation.xdelta", "clean_rebuilt.nds", "clean_patch_proof.json")]
STARTUP_CAPTURE = ROOT / "startup/capture/capture_report.json"


def stage():
    source = checked_text(getsource(shared.stage), {
        'sum(len(sheet["messages"]) for sheet in proof["proposed_sheets"]) == 124':
            'sum(len(sheet["messages"]) for sheet in proof["proposed_sheets"]) == 7',
    })
    scope = vars(shared) | globals()
    exec(compile(source, __file__ + "::source-locked-common-deployment", "exec"), scope)
    scope["stage"]()


def installed():
    parent, proof, stored = map(read, (review.RELEASE, review.OUT, STORED))
    assert stored["candidate_sha256"] == digest(ROM)
    assert stored["predecessor_sha256"] == proof["candidate_sha256"] == parent["candidate_sha256"]
    assert stored["source_preflight"] == reference(review.OUT)
    ctx = review.earlier.RegisteredRuntime(review.RELEASE, parent["own_registered_startup"], captain=3)
    image = NdsImage.open(ROM)
    arm, common = image.read_file(review.ARM), image.read_file(review.COMMON)
    assert arm == ctx.arm
    assert trend.digest(common) == stored["target_COMMON_sha256"] == proof["proposed_COMMON_sha256"]
    old, new = [review.earlier.athens.common_rows(blob, arm) for blob in (ctx.common, common)]
    assert [b.message_id for a, b in zip(old, new, strict=True) if a != b] == [KEY]
    assert new[870] == old[870] and new[review.REPLY] == old[review.REPLY]
    source = checked_text(getsource(consumer), {
        "pointer = 0x02470000": "pointers = (0x02470000, SECOND_ARGUMENT)",
        '''    if argument is not None:
        assert len(argument) < 64 and b'\0' not in argument
        cpu.mem_write(pointer,argument+b'\0')
'''.replace(chr(0), r"\0"): '''    for pointer, value in zip(pointers, argument):
        assert len(value) < 64 and bytes(1) not in value
        cpu.mem_write(pointer, value + bytes(1))
''',
        "(actor_or_role,key,pointer if argument is not None else 0,0)":
            "(actor_or_role, key, *(pointers if argument else (0, 0)))",
    })
    scope = dict(consumer.__globals__, SECOND_ARGUMENT=0x02470100)
    exec(compile(source, __file__ + "::two-argument-tavern-wrapper", "exec"), scope)
    native = scope["consumer"]
    results = []
    samples = [case for case in proof["native_cases"] if case["arguments"][0] in review.SAMPLES]
    for case in samples:
        args = tuple(value.encode("ascii") for value in case["arguments"])
        output = native(arm, common, ctx.raw, ctx.plan, 0x53FE4, case["speaker_object"], KEY, args)
        assert output["formatted_hex"] == case["proposed"]["formatted_hex"]
        assert output["file_reads"]
        results.append(dict(original_arguments=case["arguments"], native=output))
    reply = proof["optional_same_speaker_followup"]
    retained = native(arm, common, ctx.raw, ctx.plan, 0x53FE4, reply["same_original_speaker_object"], review.REPLY, ())
    assert retained["formatted_hex"] == reply["layout"]["formatted_hex"]
    write(NATIVE, dict(candidate_sha256=stored["candidate_sha256"], predecessor_sha256=parent["candidate_sha256"],
        installed_loader_and_formatter=results, retained_followup=retained,
        ordinary_representative_consumer=reference(review.parent.REVIEW),
        ordinary_representative_paired_gameplay=reference(review.parent.build.PAIRED),
        exact_reused_consumer_dependencies=dict(ARM9_sha256=trend.digest(arm), message_870_hex=new[870].text.hex(),
            same_portrait_wrapper=0x02053FE4, unchanged_870_archived_record=True),
        coverage="Focused native loader, substitution and wrap checks on the staged archive. The ordinary representative replay is inherited by exact dependencies."))
    print("Stored loader and formatter match all three sampled layouts and the retained patron follow-up.")


if __name__ == "__main__":
    cli = ArgumentParser(description=__doc__)
    cli.add_argument("action", choices=("stage", "installed", "patch", "startup"))
    action = cli.parse_args().action
    if action in ("stage", "installed"):
        globals()[action]()
    else:
        FunctionType(shared.release_check.__code__, vars(shared) | globals())(read(STORED), action)
