"""Stage the source-bound title for the two 祭主 actors."""

from hashlib import sha256
from pathlib import Path
from struct import pack_into, unpack_from

from ndspy.code import MainCodeFile

from dk4tool.graphics.pxl import PxlImage
from dk4tool.patch.main_pool_cache_visibility import BASE, POOL, STAGE, cache_plan
from scripts import register_forces_relationships_20261115 as parent
from scripts.prepare_all_routes_promotion_20261111 import verify_runtime
from scripts.qualify_rafael_plett_relocation_v1 import raw_hits
from scripts.verify_release_baseline import files


base = parent.base
ARM, CLEAN = parent.stage.ARM, parent.stage.CLEAN
ROOT = Path('work/ritual_officiant_labels_20261115_v1')
ROM = ROOT / 'Ritual_Officiant_Labels_RESEARCH_ONLY.nds'
STORED = ROOT / 'staged.json'
LABEL = b'Officiant\0'
ACTORS = (132, 135)
TABLE = 0x120B80
OLD = 0x2387E2C
PADDING_START, WRAPPER = 123176, 123200
START = 123188
END = START + len(LABEL)


def digest(data):
    return sha256(data).hexdigest()


def stage_arm(old, clean, release):
    assert digest(old) == release['target_ARM9_sha256']
    section = MainCodeFile(old, BASE).sections[3]
    staged = bytes(section.data)
    cache = cache_plan(old)
    assert section.ramAddress == STAGE and cache['entry'] - STAGE == WRAPPER
    assert cache['payload_bytes'] == len(staged) - 48 == 123264
    assert staged[PADDING_START:WRAPPER] == b'Perrault\0' + bytes(15)
    assert unpack_from('<I', old, TABLE + 65 * 32 + 4)[0] == POOL + PADDING_START
    address = POOL + START
    assert START % 4 == 0 and PADDING_START + 9 <= START < END < WRAPPER
    assert raw_hits(old, POOL + PADDING_START, POOL + WRAPPER) == [(TABLE + 65 * 32 + 4, POOL + PADDING_START)]
    assert staged[OLD - POOL:OLD - POOL + 8] == b'Priest\0\0'
    old_owners = [(TABLE + ident * 32, OLD) for ident in (*ACTORS, 139)]
    assert raw_hits(old, OLD, OLD + 8) == old_owners
    base_at = old.index(staged)
    assert old.count(staged) == 1
    physical = base_at + START
    fields = []
    edited = bytearray(old)
    for ident in ACTORS:
        field = TABLE + ident * 32
        source_pointer = unpack_from('<I', clean, field)[0]
        original = '祭主'.encode('cp932') + b'\0'
        assert clean[source_pointer - BASE:source_pointer - BASE + len(original)] == original
        assert unpack_from('<I', old, field)[0] == OLD
        pack_into('<I', edited, field, address)
        fields.append(dict(actor_ID=ident, field_offset=field, clean_pointer=source_pointer,
                           clean_hex=original.hex(), old_pointer=OLD, target_pointer=address))
    edited[physical:physical + len(LABEL)] = LABEL
    after = bytes(edited)
    parsed = MainCodeFile(after, BASE)
    assert cache_plan(after) == cache and len(after) == len(old)
    assert bytes(parsed.sections[3].data) == staged[:START] + LABEL + staged[END:]
    assert raw_hits(after, address, POOL + WRAPPER) == [(row['field_offset'], address) for row in fields]
    assert raw_hits(after, OLD, OLD + 8) == old_owners[-1:]
    inverse = bytearray(after)
    for offset, size in [(physical, len(LABEL)), *((row['field_offset'], 4) for row in fields)]:
        inverse[offset:offset + size] = old[offset:offset + size]
    assert bytes(inverse) == old
    verify_runtime(after, release)
    return after, dict(fields=fields, old_Priest_preserved_for_actor=139, new_label=LABEL[:-1].decode('ascii'),
                       new_label_span=[physical, physical + len(LABEL)], staged_alignment_range=[START, END],
                       clean_ARM9_sha256=digest(clean), previous_ARM9_sha256=digest(old), target_ARM9_sha256=digest(after),
                       same_section_extent_and_cache_plan=True, complete_ARM9_inverse_exact=True)


def main():
    assert not ROM.exists()
    release = base.load(parent.RELEASE)
    assert base.digest(base.REGISTRY) == release['registry_sha256']
    assert base.digest(parent.ROM) == release['candidate_sha256']
    assert base.digest(parent.MANIFEST) == release['manifest_sha256']
    assert base.digest(CLEAN) == release['clean_input_sha256']
    clean, image = [base.NdsImage.open(path) for path in (CLEAN, parent.ROM)]
    old = files(image)
    arm, proof = stage_arm(old[ARM], clean.read_file(ARM), release)
    # Test literal interior aliases across every owned component before staging.
    pixel_matches = []
    for path, raw in old.items():
        if path != ARM:
            hits = raw_hits(raw, POOL + START, POOL + WRAPPER)
            if hits:
                assert path == '/evstill/evstill172.pxl' and hits == [(37957, 37378901)], (path, hits)
                picture = PxlImage.from_bytes(raw)
                assert picture.pixels_offset <= hits[0][0] < len(raw) - 3 and picture.to_bytes() == raw
                pixel_matches.append(dict(path=path, matches=hits, pixel_start=picture.pixels_offset, sha256=digest(raw)))
    assert len(pixel_matches) == 1
    ROOT.mkdir(parents=True, exist_ok=True)
    image.replace_file(ARM, arm)
    assert {path for path, value in files(image).items() if value != old[path]} == {ARM}
    image.save(ROM)
    image.replace_file(ARM, old[ARM])
    assert bytes(image.rom.save()) == parent.ROM.read_bytes()
    base.save(STORED, proof | dict(candidate_sha256=base.digest(ROM), previous_sha256=release['candidate_sha256'],
                                  complete_ROM_inverse_exact=True, research_only=True, unrelated_pixel_matches=pixel_matches))
    print('Staged both Officiant labels. Priest for actor 139, Perrault, startup copy and right bound passed.')


if __name__ == '__main__':
    main()
