"""Record the current scene-art associations and the checked movie texture scope."""

from pathlib import Path
from shutil import copyfile

from dk4tool.graphics.fls import FlsArchive
from scripts import checkpoint_story_still_commands_20261120 as scene
from scripts import inventory_shared_movie_textures_20261123 as atlas
from scripts import register_moonlit_violin_20261121 as violin


base, native, current = atlas.base, atlas.native, atlas.current
BOOK = Path("translations/editorial_checkpoints/SharedText_20261110_v1")
OUT = BOOK.parent / "shared_display_20261123/movie_label_scope_20261123.json"
HARBOR = BOOK / "rafael_harbor_shared_artwork_20261121_v1.json"
TITLE = BOOK / "shared_numeric_and_lil_artwork_20261121_v1.json"
STORED = OUT.with_name("current_shared_display_evidence_20261123.json")
CAPTIONS = BOOK / "opening_movie_caption_retentions_20261119_v1.json"
ASSOCIATIONS = {3394: ("/FLS/M20.fls", 26), 3397: ("/FLS/m21.fls", 0),
                3410: ("/FLS/M23.fls", 0), 3456: ("/FLS/M28.fls", 48)}


def preserved_image(reference):
    assert base.digest(Path(reference["path"])) == reference["PNG_sha256"]
    return reference


def movie_commands(walk, arm, image, chapter, block, movie_ids):
    data = native.IlnkContainer.parse(image.read_file(chapter)).blocks[block]
    trace = walk(arm, data)
    assert trace["error"] is None, (chapter, block, trace["error"])
    selected = []
    for call in trace["native_movie_requests"]:
        movie = call["args"][0]
        if movie not in movie_ids:
            continue
        offset = call["source_offset"]
        assert data[offset:offset + 2] == bytes([movie - 20, 0x49])
        assert call["args"] == [movie, 0, 1, 0]
        assert not any(row["source_offset"] == offset and row["PC"] in (scene.owners.GETTER, scene.owners.COPIER)
                       for row in trace["opaque_effect_bridges"])
        selected.append(dict(file_path=chapter, block=block, offset=offset, block_sha256=native.digest(data),
            command_hex=data[offset:offset + 2].hex(), arguments=call["args"]))
    assert {row["arguments"][0] for row in selected} == set(movie_ids)
    return selected


def main():
    assert not OUT.exists()
    release, installed_review = map(base.load, (current.RELEASE, current.REVIEW))
    candidate = base.digest(current.ROM)
    assert release["candidate_sha256"] == installed_review["candidate_sha256"] == candidate
    assert base.digest(base.REGISTRY) == release["registry_sha256"]
    assert base.digest(native.CLEAN) == release["clean_input_sha256"]
    clean, installed = map(base.NdsImage.open, (native.CLEAN, current.ROM))
    arms = [image.read_file(current.ARM) for image in (clean, installed)]
    assert native.digest(arms[1]) == release["target_ARM9_sha256"]
    frames = {row["message_ID"]: row for row in base.load(HARBOR)["records"]}
    title = base.load(TITLE)["title_artwork_association"]["3456"]
    violin_proof = base.load(violin.REVIEW)["artwork"]
    texture_inventory = base.load(atlas.ROOT / "texture_inventory.json")
    assert texture_inventory["candidate_sha256"] == candidate
    previous = base.load(STORED)
    wanted = set(previous["literal_scan_keys"])
    assert len(wanted) == 35 and ASSOCIATIONS.keys() <= wanted
    available = set(ASSOCIATIONS) | {3401, 3490, 3500, 3515}
    share = {row["message_ID"]: row for row in installed_review["shared_consumer_binding"]["records"]}
    reader = current.stage.observed.prior.shared.paired.prior.entries
    stored = reader(installed)
    rows = []
    for row in previous["records"]:
        key = row["message_ID"]
        if key not in available:
            continue
        assert row["installed_reference"] == share[key]["installed"] == current.stage.town.reference(stored[key])
        assert row["source_hex"] == row["installed_hex"] == stored[key].text.hex()
        result = dict(message_ID=key, clean_Japanese=bytes.fromhex(row["source_hex"]).decode("cp932"),
            clean_reference=row["source_reference"], installed_reference=row["installed_reference"],
            exact_stored_hex=row["installed_hex"], draft=row["earlier_draft"], other_stored_text_consumer_open=True)
        if key in ASSOCIATIONS:
            path, index = ASSOCIATIONS[key]
            blobs = [image.read_file(path) for image in (clean, installed)]
            hashes = [native.digest(blob) for blob in blobs]
            left, right = (FlsArchive(blob).texture(index) for blob in blobs)
            assert left == right
            parts = dict(file_path=path, texture_index=index, clean_sha256=hashes[0], current_sha256=hashes[1],
                         exact_visible_texture_sha256=native.digest(left.render().tobytes()))
            if key in frames:
                historical = frames[key]
                assert hashes == [historical["art"]["clean_sha256"], historical["art"]["installed_sha256"]]
                assert historical["English"] == row["earlier_draft"]["english"]
                assert native.digest(left.indices) == historical["art"]["unchanged_texture_sha256"]
                parts["earlier_ordinary_New_Game_hold"] = preserved_image(historical["observed"])
            elif key == 3410:
                assert hashes[0] == hashes[1] == violin_proof["sha256"]
                parts["moonlit_scene_context"] = "Rafael appears with his violin before the close-ups and reply."
            else:
                assert hashes == [title["clean_asset_sha256"], title["installed_asset_sha256"]]
                assert title["english_draft"] == row["earlier_draft"]["english"]
                parts["earlier_ordinary_title_hold"] = preserved_image(title["held_frame"])
                parts["complete_approved_names"] = preserved_image(title["complete_animated_names"]["frame"])
            result["separate_artwork_path"] = parts
        rows.append(result)
    assert {row["message_ID"] for row in rows} == available
    walk = scene.explicit_walk()
    chapters = {
        ("/data/SC0.DK4", 44): (20, 21),
        ("/data/SC0.DK4", 51): (23,),
        ("/data/SC1.DK4", 143): (23,),
    }
    commands = {label: [record for (path, block), ids in chapters.items()
        for record in movie_commands(walk, arm, image, path, block, ids)]
        for label, arm, image in zip(("clean", "current"), arms, (clean, installed), strict=True)}
    assert len(commands["clean"]) == len(commands["current"]) == 4
    carried = []
    for row in base.load(CAPTIONS)["records"]:
        path, index = row["file_path"], row["texture_index"]
        blobs = [image.read_file(path) for image in (clean, installed)]
        for data, ref in zip(blobs, (row["source_reference"], row["current_reference"]), strict=True):
            assert native.digest(data) == ref["file_sha256"]
            assert native.digest(FlsArchive(data).texture(index).indices) == ref["texture_index_sha256"]
        carried.append({key: row[key] for key in ("id", "file_path", "texture_index", "english",
            "localization_note", "source_reference", "current_reference", "previous_render_evidence")})
    assert len(carried) == 5
    for movie in texture_inventory["movie_archives"].values():
        sheet = movie["sheet"]
        path = Path(sheet["path"])
        assert base.digest(path) == sheet["sha256"]
        target = OUT.parent / f"shared_scene_{path.name}"
        copyfile(path, target)
        assert base.digest(target) == sheet["sha256"]
        sheet["path"] = str(target)
    base.save(OUT, dict(candidate_sha256=candidate, clean_sha256=release["clean_input_sha256"],
        records=rows, checked_movie_commands=commands, carried_opening_captions=carried,
        visual_comparison_of_57_texture_pairs=texture_inventory["movie_archives"],
        still_unlinked_scene_label_ids=sorted(available - ASSOCIATIONS.keys()),
        shared_storage_open_total=len(share), other_least_understood_scope=sorted(wanted - ASSOCIATIONS.keys()),
        earlier_evidence={str(p):base.digest(p) for p in (HARBOR, TITLE, violin.REVIEW, CAPTIONS, STORED)},
        new_gameplay_runs=0, new_editorial_credit=0, assets_changed=False,
        scope="Selected story commands and independent movie art. Archived COMMON labels retain their own open display gate."))
    print("Verified four separate movie associations on the current ROM and scoped the four unmatched label descriptions.")


if __name__ == "__main__":
    main()
