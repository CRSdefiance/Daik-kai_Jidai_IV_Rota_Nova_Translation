"""Record reviewed nameplate masks and bind the chooser's independent text owners."""

from hashlib import sha256
from pathlib import Path
from struct import unpack_from

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.script.common_message_table import common_message_entries
from scripts import reconcile_shared_speaker_labels_20261111 as names
from scripts import register_captain_biographies_v1 as bios
from scripts import verify_captain_biographies_v1 as chooser
from scripts.registered_editorial_runtime_v2 import RegisteredRuntime
from scripts.review_sound_bgm_titles_v1 import DIRECTORY_OFFSET, TABLE_OFFSET, owned_entries, reference


base, current = names.base, names.current
NAME_REVIEW = names.CHECKPOINT / 'shared_occupational_nameplates_reviewed_v1.json'
CHOOSER_REVIEW = names.CHECKPOINT / 'common_104_107_chooser_owner_comparison_v1.json'
VIEWED_SHEET = '7760d0bd82fa4de770aaed71ca5574e025cda51e5c21136580fa13edcf2906a6'


def review_names():
    draft = base.load(names.MANUSCRIPT)
    native_path = names.BINDINGS / 'native/native_name_planes.json'
    native = base.load(native_path)
    assert draft['runtime'] == native['runtime'] and len(draft['records']) == 24
    assert native['all_name_strings_ASCII_complete_andfit_style11_216px']
    assert len(native['review_sheets']) == 1
    sheet, = native['review_sheets']
    assert base.digest(sheet['path']) == sheet['sha256'] == VIEWED_SHEET
    planes = {row['text']: row for row in native['planes']}
    assert set(planes) == {'Barkeep', 'Port Worker', 'Retainer', 'Sailor', 'Trader'}
    for plane in planes.values():
        assert plane['complete_first_internal_final_codes_bounds_andindependent_font_pixels_pass']
        assert base.digest(plane['native_plane']) == plane['native_plane_sha256']
        assert base.digest(plane['preview']) == plane['preview_sha256']
    records = [row | dict(context=draft['contexts'][row['context']]['file_path'] + ' reviewed exchange: ' + row['context'].replace('_', ' '),
        context_reference=row['context'], review=row['review'] | {'formatting': True},
        progressive_nameplate_plane=planes[row['english']]['native_plane_sha256'],
        catalogue_getter_verified=True, catalogue_UI_layout_observed=False) for row in draft['records']]
    result = draft | dict(records=records, native_nameplane_verification=native_path.as_posix(),
        native_nameplane_verification_sha256=base.digest(native_path), viewed_sheet=sheet,
        reviewed_progressive_nameplates=24, distinct_viewed_strings=5, revision_count=0,
        scope='Formatting approval covers current original progressive style 11. The catalog getter bytes are verified. Catalog UI layout remains open.',
        new_emulator_gameplay=False, hardware=False)
    validate_natural_dialogue_batch(result)
    return result


def review_chooser(ctx, release):
    inventory = base.load(chooser.INVENTORY)
    historic, registered = map(base.load, (bios.RELEASE, bios.REVIEW))
    assert base.digest(bios.ROM) == historic['candidate_sha256']
    assert base.digest(current.CLEAN) == release['clean_input_sha256'] == inventory['clean_ROM_sha256']
    historical_arm = base.NdsImage.open(bios.ROM).read_file(current.ARM)
    clean = base.NdsImage.open(current.CLEAN)
    clean_arm = clean.read_file(current.ARM)
    sources = common_message_entries(clean.read_file(current.COMMON), clean_arm)
    arm = ctx.arm
    stored = owned_entries(ctx.common, arm, sha256(arm[DIRECTORY_OFFSET:TABLE_OFFSET]).hexdigest())
    spans = ((chooser.CALLER[0], 0x9E770), (chooser.TABLE, chooser.TABLE+16), chooser.STORAGE)
    assert all(arm[lo:hi] == historical_arm[lo:hi] == ctx.raw[lo:hi] for lo, hi in spans)
    font = GameAsciiFont.from_arm9(arm)
    assert font.glyphs == GameAsciiFont.from_arm9(historical_arm).glyphs
    prior_live = bios.VERIFICATION / 'captain_chooser_gameplay_verification.json'
    live = base.load(prior_live)
    assert len(live['live_cases']) == 7 and live['reverse_switch_verified']
    boot = base.load(release['own_registered_startup'])
    maria_frame = next(row for row in boot['exact_matching_frames'] if row['frame'] == 3340)
    legacy_path = names.CHECKPOINT / 'legacy_common_35_checkpoint_v1.json'
    legacy = {row['message_ID']: row for row in base.load(legacy_path)['records']}
    results = []
    for original, reviewed in zip(inventory['records'], registered['records'], strict=True):
        assert all(reviewed['review'].values()) and original['actor'] == reviewed['actor']
        index = original['chooser_index']
        ident = 104 + index
        japan = sources[ident].text.decode('cp932')
        assert sources[ident].text.hex() == legacy[ident]['clean_hex'] and stored[ident].text.hex() == legacy[ident]['current_hex']
        lines = original['existing_source_rows']
        chooser.stage.previous.references(clean_arm, lines, True)
        assert japan.replace('\n', '').replace('。', '') == ''.join(row['Japanese'] for row in lines)
        own = reviewed['registered_reference']
        assert unpack_from('<I', arm, chooser.TABLE + index * 4)[0] == own['runtime_address']
        assert arm[own['ARM9_offset']:own['ARM9_offset']+own['byte_count']].hex() == own['exact_hex']
        selection = chooser.native_selector(arm, ctx.raw, reviewed)
        original_cases = [row for row in live['live_cases'] if row['actor'] == original['actor']]
        assert original_cases
        glyphs = chooser.mask(font, reviewed['staged_rows'], chooser.captured(maria_frame)) if index == 3 else None
        results.append(dict(id=f'COMMON_MESSAGE_{ident}', actor=original['actor'], clean_COMMON_reference=reference(sources[ident]),
            current_COMMON_reference=reference(stored[ident]), clean_COMMON_text=japan,
            current_COMMON_text=stored[ident].text.decode('cp932'), clean_chooser_rows=lines,
            current_chooser_reference=own | {'ROM_sha256': release['candidate_sha256']},
            current_chooser_English=reviewed['english'], current_native_selection=selection,
            current_Maria_gameplay_glyphs=glyphs, historical_gameplay=original_cases,
            other_COMMON_consumers_unresolved=True, new_credit=0))
    return dict(candidate_sha256=release['candidate_sha256'], records=results,
        clean_prose_matches_after_display_newlines_and_sentence_stops_removed=True,
        chooser_uses_independent_ARM9_text_for_all_four_native_indices=True,
        scope='Four offline selector cases and one current Maria hold from the existing cold-boot capture. Earlier gameplay visited all four. Other callers of the COMMON records remain open.',
        evidence={str(path): base.digest(path) for path in (chooser.INVENTORY, bios.REVIEW, prior_live, legacy_path,
                 release['own_registered_startup'], Path(__file__))}, new_editorial_credit=0, full_goal_complete=False)


def main():
    assert not NAME_REVIEW.exists() and not CHOOSER_REVIEW.exists()
    release = base.load(current.RELEASE)
    ctx = RegisteredRuntime(current.RELEASE, release['own_registered_startup'], captain=3)
    name_review, chooser_review = review_names(), review_chooser(ctx, release)
    base.save(NAME_REVIEW, name_review)
    base.save(CHOOSER_REVIEW, chooser_review)
    print('Sealed 24 progressive-nameplate retentions and four independently owned chooser biographies.')


if __name__ == '__main__':
    main()
