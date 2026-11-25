"""Check the registered guide candidate and carry forward the closed wrap and open shared scopes."""

from types import FunctionType

from scripts import prepare_pending_shared_text_20261118 as shared
from scripts import register_sailing_mode_prose_20261118 as registered


base, native = registered.base, registered.native
ROOT = registered.stage.ROOT
QUEUE = ROOT / "followup_wrap_queue.json"
PENDING = ROOT / "shared_text_current_binding.json"


def main():
    release = base.load(registered.RELEASE)
    registry, ledger, manifest = map(base.load, (base.REGISTRY, base.LEDGER, registered.MANIFEST))
    assert release["candidate_sha256"] == base.digest(registered.ROM) == ledger["current_integrated_candidate"]["sha256"]
    assert base.digest(registered.MANIFEST) == release["manifest_sha256"]
    assert base.digest(registered.PATCH) == release["patch_sha256"] == base.digest(ROOT / "clean_input.xdelta")
    assert registered.ROM.read_bytes() == (ROOT / "clean_rebuilt.nds").read_bytes()
    assert base.digest(base.REGISTRY) == release["registry_sha256"] == manifest["release_stack_sha256"]
    assert len(manifest["batches"]) == 887 and len(manifest["checks"]) == 222 and all(manifest["checks"].values())
    previous_registry = base.load(release["predecessor"]["registry"])
    assert len(registry["accepted_layers"]) == 114 and registry["accepted_layers"] == previous_registry["accepted_layers"]
    assert "ascii_glyph_right_bounds" in registry["profiles"][registered.PROFILE]
    assert ledger["records_editorially_completed"] == 27700
    assert base.digest(base.PROMOTED) == base.load(registered.VERIFY / "registration_mutation_plan.json")["main_sha256"]

    earlier, current = map(base.NdsImage.open, (registered.parent.ROM, registered.ROM))
    assert native.digest(current.read_file(native.ARM)) == release["target_ARM9_sha256"]
    assert release["target_ARM9_sha256"] == ledger["current_integrated_candidate"]["ARM9_sha256"]
    archived = registered.parent.stage.ROOT / "followup_wrap_queue.json"
    queue = base.load(archived)
    assert queue["candidate_sha256"] == release["predecessor"]["candidate_sha256"]
    assert queue["counts"]["open editorial lead"] == 0
    dependencies = {}
    for route in range(4):
        path = f"/data/SC{route}.DK4"
        old, new = (im.read_file(path) for im in (earlier, current))
        assert old == new
        dependencies[path] = native.digest(new)
    queue.update(candidate_sha256=release["candidate_sha256"], checked_story_archives=dependencies,
        predecessor_queue=dict(path=str(archived), sha256=base.digest(archived)))
    if QUEUE.exists():
        assert base.load(QUEUE) == queue
    else:
        base.save(QUEUE, queue)

    FunctionType(shared.main.__code__, vars(shared) | {"registered":registered, "OUTPUT":PENDING})()
    note = ("\nThe closed wrap queue carries forward on the same four story archives. "
            "The 276 shared-text drafts are bound to the current registered ROM. "
            "[Shared text bindings](../work/sailing_mode_prose_20261118/research_v1/shared_text_current_binding.json)\n")
    doc = registered.DOC.read_text(encoding="utf-8")
    if note not in doc:
        registered.DOC.write_text(doc + note, encoding="utf-8", newline="\n")
    print("Verified the guide candidate and clean patch. Carried forward all four story archives and the closed wrap queue.")


if __name__ == "__main__":
    main()
