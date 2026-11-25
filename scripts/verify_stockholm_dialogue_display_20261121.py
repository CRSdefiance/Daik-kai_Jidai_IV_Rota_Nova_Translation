"""Verify and preview all three changed Stockholm native pages."""
from types import FunctionType, SimpleNamespace

from scripts import stage_stockholm_dialogue_followup_20261121 as build
from scripts import verify_all_routes_next_phrase_wraps_20261118 as display
from scripts import verify_stockholm_december_20261121 as previous


base, native, town = build.base, build.native, previous.town
ROOT = build.ROOT / "native_display"
PROOF = ROOT / "native_display.json"


def main():
    assert not ROOT.exists()
    stored, review = map(base.load,(build.PROOF,build.REBOUND))
    sha = base.digest(build.ROM)
    assert stored["candidate_sha256"] == sha and stored["manuscript_sha256"] == base.digest(build.REBOUND)
    before, after = map(base.NdsImage.open,(build.parent.ROM,build.ROM))
    assert all(before.read_file(p)==after.read_file(p) for p in display.ASSETS)
    original_arm, kanji = (after.read_file(path) for path in (native.ARM,"/GRP/KANJI.FNT"))
    runtime = SimpleNamespace(image=after,arm=original_arm)
    progressive = display.clipped_renderer(runtime)
    system = town.current_fe_painter(runtime)
    rows = {(row["file_path"],row["id"]):row for row in review["records"]}
    receipts, previews = [], []
    for group in stored["groups"]:
        path,number = group["file_path"],group["block"]
        data = native.IlnkContainer.parse(after.read_file(path)).blocks[number]
        assert native.digest(data) == group["after"]
        for command in group["commands"]:
            at = command["stored_offset"]
            original,compiled = (bytes.fromhex(command[key]) for key in ("current","stored"))
            assert data[at:at+len(compiled)] == compiled
            for ident in command["record_ids"]:
                row = rows.pop((path,ident))
                result = dict(id=ident,file_path=path,block=number,decision=row["decision"],
                              stored_offset=at,stored_command_hex=compiled.hex())
                if row["decision"] == "retention":
                    assert original == compiled
                    receipts.append(result)
                    continue
                selector = row["source_selector"]
                assert original[:6] == compiled[:6] == b"\0\x40\xff\xff\0"+bytes([selector])
                body = compiled[6:compiled.index(0,6)]
                assert body.isascii() and not any(compiled[6+len(body):])
                assert build.author.logical(body.decode("ascii")) == row["english"]
                plan = group["plans"][ident]
                assert plan["expected_native_pages"] == 1
                planned = bytes.fromhex(plan["encoded_hex"])
                assert compiled[5:6]+body in (planned, planned+b" ")
                if selector == 254:
                    fe = system(body)
                    build.stage.system.check_FE_rows(body,fe)
                    assert fe["complete_consumed_bytes"] == len(body)
                    physical = fe["physical"]
                    assert len(physical) == 228 * 64
                    assert all(not any(physical[y*228+216:(y+1)*228]) for y in range(64))
                    logical_plane = b"".join(physical[y*228:y*228+216] for y in range(64))
                else:
                    page, = display.display.raster(runtime,kanji,progressive,body,plan["lines"],1)
                    assert page["native_independent_plane_equal"]
                    physical = logical_plane = bytes.fromhex(page["native_plane_hex"])
                result.update(native_pages=1,lines=plan["lines"],full_consumption=True,no_runtime_substitutions=True,
                    plane_sha256=native.digest(physical),complete_first_last_glyphs=True)
                previews.append((ident,logical_plane))
                receipts.append(result)
    assert not rows and len(receipts) == 39 and len(previews) == 3
    ROOT.mkdir()
    contact = display.display.inherited.early.contact_sheets
    sheets = FunctionType(contact.__code__,contact.__globals__ | {"ROOT":ROOT})(previews)
    base.save(PROOF,dict(candidate_sha256=sha,stage_proof_sha256=base.digest(build.PROOF),records=receipts,
        sheets=sheets,offline_native_only=True,newly_rendered_pages=3))
    print("Three Stockholm pages passed native checks, and all 36 retained records are byte-exact.")


if __name__ == "__main__":
    main()
