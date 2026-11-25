"""Verify stored violin-scene bodies in the original progressive display path."""

from types import FunctionType, SimpleNamespace

from scripts import stage_moonlit_violin_20261121 as build
from scripts import verify_all_routes_next_phrase_wraps_20261118 as display


base, native = build.base, build.native
ROOT = build.ROOT / "native_display"
PROOF = ROOT / "native_display.json"
NAMES = {"FI": "Hodram"}


def bytes_for(raw):
    return raw[6:raw.index(0, 6)]


def main():
    assert not ROOT.exists()
    stored, review = map(base.load, (build.PROOF, build.review.OUTPUT))
    assert base.digest(build.ROM) == stored["candidate_sha256"]
    assert base.digest(build.review.OUTPUT) == stored["manuscript_sha256"]
    old, target = map(base.NdsImage.open, (build.parent.ROM, build.ROM))
    assert all(old.read_file(asset) == target.read_file(asset) for asset in display.ASSETS)
    arm, font = (target.read_file(asset) for asset in (display.ASSETS[0], display.ASSETS[2]))
    runtime = SimpleNamespace(arm=arm)
    render = display.clipped_renderer(runtime)
    rows = {(r["file_path"], r["id"]): r for r in review["records"]}
    results, previews = [], []
    for group in stored["groups"]:
        path = group["file_path"]
        block = native.IlnkContainer.parse(target.read_file(path)).blocks[group["block"]]
        assert native.digest(block) == group["after"]
        for cmd in group["commands"]:
            if not cmd["record_ids"]:
                continue
            ident, = cmd["record_ids"]
            row = rows.pop((path, ident))
            command, before = (bytes.fromhex(cmd[k]) for k in ("stored", "current"))
            raw = bytes_for(command)
            offset = cmd["stored_offset"]
            assert command[:6] == before[:6] == b"\0\x40\xFF\xFF\0" + bytes([row["source_selector"]])
            assert raw.isascii() and block[offset:offset+len(command)] == command
            assert not any(command[6+len(raw):])
            assert build.review.TOKEN.findall(raw.decode()) == build.review.TOKEN.findall(bytes_for(before).decode())
            pages = []
            if row["source_selector"] == 254:
                assert command == before and raw.strip() == b"..."
            else:
                default = display.prior.default_text(raw, NAMES)
                if row["decision"] == "revision":
                    plan = group["plans"][ident]
                    compiled = bytes.fromhex(plan["encoded_hex"])
                    assert bytes([row["source_selector"]]) + raw in (compiled, compiled+b" ")
                    assert build.review.logical(raw.decode()) == row["english"]
                    assert plan["expected_native_pages"] == 1
                    pages = display.display.raster(runtime, font, render, default, plan["lines"], 1)
                    preview, = pages
                    previews.append((f"SC{group['route']} {ident}", bytes.fromhex(preview["native_plane_hex"])))
                else:
                    assert command == before and build.review.logical(raw.decode()) == row["english"]
                    result = render(arm, font, default)
                    assert result["complete_consumed_bytes"] == len(default)
                    pages = result["pages"]
                assert all(p["native_independent_plane_equal"] for p in pages)
            results.append(dict(id=ident, file_path=path, block=group["block"], decision=row["decision"],
                stored_offset=offset, stored_command_hex=command.hex(), native_pages=len(pages),
                native_page_hashes=[native.digest(bytes.fromhex(p["native_plane_hex"])) for p in pages],
                exact_speakerless_pause=not pages))
    assert not rows and len(previews) == 5 and len(results) == 37
    ROOT.mkdir()
    contact = display.display.inherited.early.contact_sheets
    sheets = FunctionType(contact.__code__, contact.__globals__ | {"ROOT": ROOT})(previews)
    base.save(PROOF, dict(candidate_sha256=stored["candidate_sha256"], stage_proof_sha256=base.digest(build.PROOF),
        records=results, sheets=sheets, actual_gameplay=False, newly_rendered_pages=len(previews)))
    print("Five revised native pages passed. The 32 retentions keep their original controls and text.")


if __name__ == "__main__":
    main()
