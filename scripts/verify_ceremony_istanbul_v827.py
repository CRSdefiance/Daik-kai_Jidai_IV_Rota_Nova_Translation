"""Actual preparation reactions for three captains; site chant remains pending."""

import json
import struct
from pathlib import Path

from PIL import Image

from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.levelup_stat_format import current_entries
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import common_message_entries
from scripts.native_ceremony_istanbul_fixture_v827 import set_condition, relocate
from scripts.verify_arrival_native_v792 import prepared
from scripts.verify_ceremony_consumers_v808 import production_functions
from scripts.verify_ceremony_heroes_v825 import cstring, identity
from scripts.verify_ceremony_prayer_gameplay_v814 import calendar
from scripts.verify_common_alignment_native_v257 import raster
from scripts.verify_levelup_gameplay_v819 import glyphs
from scripts.verify_shipyard_gameplay_v760 import independent_font
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/ceremony_istanbul_v827')
CAP = Path('E:/Rota Nova translations/Generated/work/emulation_v193')
SCENES = [
    dict(hero='Maria', captain=3, folder='ceremony_Maria_Istanbul_v827', base=12800,
         IDs=[1201,1210,1214,1215,1216,291], end=15200, ticks=48),
    dict(hero='Rafael', captain=0, folder='ceremony_Rafael_final_variants_v827', base=4600,
         IDs=[1201,1210,1211,1215,1216,291], end=7800, ticks=48),
    dict(hero='Lil', captain=2, folder='ceremony_Lil_final_variants_v827', base=4600,
         IDs=[1201,1210,1213,1215,1217,291], end=7000, ticks=48),
]


def main():
    ROOT.mkdir(parents=True, exist_ok=True)
    rom = NdsImage.open('out/all_routes_combined_v820_candidate.nds')
    rom_hash = sha(rom.source.read_bytes())
    assert rom_hash == 'b8126bf14fd3aa0236c03ee48492a40eb0f2b50e77df5a16c3d6f92ea6bb2251'
    arm, common, font = [rom.read_file(p) for p in ('/__arm9__.bin','/COMMON/MESFILE.DK4','/GRP/KANJI.FNT')]
    clean = NdsImage.open('work/clean.nds')
    clean_arm = clean.read_file('/__arm9__.bin')
    original = common_message_entries(clean.read_file('/COMMON/MESFILE.DK4'), clean_arm)
    entries = current_entries(common, arm)
    blocks = IlnkContainer.parse(common).blocks
    rows = {r['message_id']:r for r in read('translations/ceremony_editorial_manuscript_v3.json')['records']}
    ordinary, modal, osource, msource = production_functions()
    printed, wrapped, owner = [struct.unpack_from('<I',arm,n)[0] for n in (0x5444C,0x54450,0x552A0)]
    loaded = {}

    def load(name):
        if name in loaded:
            return loaded[name]
        folder = CAP/name
        report = read(folder/'capture_report.json')
        assert report['ROM_sha256'] == rom_hash and report['cold_boot'] and not report['savestate_loaded']
        assert not report['callback_errors'] and not report['hardware_device_verification'] and not report['goal_complete']
        assert report['core_DLL_sha256'] == '42160dbfef89adfb3cfd975070a3047d8ad0979cead55607ebdfd3b931046c2b'
        assert report['Istanbul_fixture_adapter_v827']['no_captain_actor_dialogue_source_code_or_random_state_fixture_available']
        donor = report['battery_save_preloaded']
        assert 'disposable' in donor['source'].lower() and donor['source'] != donor['destination']
        assert donor['copied_byte_exact_before_cold_boot'] and sha(Path(donor['source']).read_bytes()) == donor['source_sha256']
        frames = {r['frame']:r for r in report['frames_captured']}
        snapshots = {r['frame']:r for r in report['read_only_pause_RAM_snapshots']}

        def raw_at(frame):
            row = snapshots[frame]
            raw = Path(row['path']).read_bytes()
            assert row['read_only_export'] and len(raw) == 0x400000 and sha(raw) == row['sha256']
            assert raw[0x610FC:0x61C18] == arm[0x610FC:0x61C18] == clean_arm[0x610FC:0x61C18]
            return raw

        # Recompute the exact executed receipts, including order of same-frame inputs.
        locations = {r['frame']:r for r in report.get('synthetic_location_fixtures',[])}
        for receipt in report.get('synthetic_condition_fixtures',[]):
            frame = receipt['frame']
            before = raw_at(frame)
            after, expected = set_condition(arm,before,dict(mode='ceremony-Istanbul',facility=receipt['facility_role'],day=receipt['target_day']))
            expected['frame'] = frame
            assert json.loads(json.dumps(expected)) == receipt
            assert identity(arm,before) == identity(arm,after)
            if frame in locations:
                moved, expected_location = relocate(arm,after,22)
                expected_location['frame'] = frame
                assert json.loads(json.dumps(expected_location)) == locations.pop(frame)
                assert identity(arm,before) == identity(arm,moved)
        assert not locations
        loaded[name] = report,frames,raw_at
        return loaded[name]

    holds, returns, reviews = [], [], {}
    for scene in SCENES:
        report,frames,raw_at = load(scene['folder'])
        who = identity(arm,raw_at(scene['base']))
        assert who['captain'] == scene['captain'] and who['notice_name'] == scene['hero']
        assert who['town'] == who['fleet_town'] == 22
        assert calendar(arm,raw_at(scene['base']))['original_zero_based_date'][1] == 23
        for i,number in enumerate(scene['IDs']):
            frame = scene['base']+400*i
            raw, row = raw_at(frame), rows[number]
            assert identity(arm,raw) == who
            assert original[number].text == bytes.fromhex(row['source_hex'])
            assert original[number].text.decode('cp932') == row['japanese']
            values = (who['notice_name'].encode(),) if number in (290,291) else (b'Cappadocia',) if number == 1219 else ()
            case = (modal if number in (290,291) else ordinary)(prepared(arm),row,values)
            assert not case['findings']
            encoded = bytes.fromhex(case['formatted_hex'])
            assert cstring(raw,wrapped) == encoded and cstring(raw,owner+0x2030) == entries[number].text
            assert raw.count(blocks[entries[number].block]) == 1
            for value in values:
                assert value in cstring(raw,printed) and value in encoded
            capture = frames[frame]
            assert sha(Path(capture['path']).read_bytes()) == capture['PNG_sha256']
            glyphs(arm,font,Image.open(capture['path']).convert('RGB'),encoded,case['lines'])
            holds.append(dict(hero=scene['hero'],captain=who['captain'],frame=frame,message_id=number,
                lines=case['lines'],capture=capture,folder=scene['folder'],
                complete_native_independent_and_actual_ink_blank_plane_exact=True,
                complete_first_last_letters_alignment_bounds_variables_template_and_resident_block=True,
                actual_original_portraits_and_captions_visually_reviewed=True))
            reviews[number] = dict(message_id=number,Japanese=row['japanese'],English=row['english'],
                source_reference=row['source_reference'],source_hex=row['source_hex'],current_entry_hex=entries[number].text.hex(),
                source_meaning=row['source_meaning'],localization_note=row['localization_note'],
                decision='retain frozen production wording after actual captain context review')
        end = raw_at(scene['end'])
        assert identity(arm,end) == who
        ticks = calendar(arm,end)['ticks']-calendar(arm,raw_at(scene['base']))['ticks']
        assert ticks == scene['ticks'], (scene['hero'],scene['base'],ticks)
        returns.append(dict(hero=scene['hero'],from_frame=scene['base'],town_return_frame=scene['end'],
            original_tick_increment=ticks,normal_return_visually_reviewed=True))
    # Additional real three-stat growth after Rafael's preparations.
    _,frames,raw_at = load('ceremony_Rafael_final_variants_v827')
    stats = cstring(raw_at(7400),wrapped)
    lines = [s.strip().decode('cp932') for s in stats.split(b'\n')]
    assert len(lines) == 3 and not stats.endswith(b'\n')
    assert lines == ['Stamina increased by ２!','Agility increased by １!','Charm increased by １!']
    glyphs(arm,font,Image.open(frames[7400]['path']).convert('RGB'),stats,lines)
    header = cstring(raw_at(7000),wrapped)
    assert header == b'Rafael leveled up!!'
    plane = raster(arm,header,0x01FFCE40-0x02000000,size=(228,64),instruction_limit=1000000)
    independent = independent_font(arm,font,[header.decode()])
    independent = b''.join(independent[y*228+6:(y+1)*228]+bytes(6) for y in range(64))
    assert plane == independent
    picture = Image.open(frames[7000]['path']).convert('RGB')
    assert {(16+i%228,296+i//228) for i,p in enumerate(plane) if p == 1} == {
        (x,y) for y in range(294,366) for x in range(16,244) if picture.getpixel((x,y)) == (0,8,0)}
    # The two original approach runs contain no counted ceremony holds, but their
    # executed fixtures and protected input hashes are also checked.
    for hero in ('Rafael','Lil'):
        load(f'ceremony_{hero}_Istanbul_v827')
    for catalog in ('work/analysis/ceremony_heroes_v825/after_fast_normal_save_provenance.json',
                    'work/analysis/ceremony_istanbul_v827/Rafael_Lil_normal_saves_pending_reload.json'):
        for row in read(catalog)['rows']:
            assert sha(Path(row['normal_save']).read_bytes()) == row['sha256']
            assert sha(Path(row['disposable_copy']).read_bytes()) == row['sha256']
    maria_save = read(ROOT/'Maria_normal_save_pending_reload.json')
    assert sha(Path(maria_save['normal_save']).read_bytes()) == maria_save['sha256']
    assert sha(Path(maria_save['disposable_copy']).read_bytes()) == maria_save['sha256']
    assert len(holds) == 18 and len(reviews) == 9
    known = set(read('translations/editorial_review_current_v1.json')['actual_ceremony_Lil_v826']['cumulative_distinct_actual_family_IDs'])
    new = set(reviews)-known
    assert new == {1211,1213,1214,1217} and len(known | set(reviews)) == 51
    save(ROOT/'four_preparation_variants_actual_verification.json',dict(
        candidate=str(rom.source),candidate_sha256=rom_hash,clean_source_sha256=sha(clean.source.read_bytes()),
        complete_scene_holds=holds,source_context_reviews=list(reviews.values()),time_and_return=returns,
        new_actual_variant_IDs=sorted(new),cumulative_distinct_actual_family_IDs=sorted(known | set(reviews)),
        remaining_actual_variant_IDs=[1224],
        site_access_attempt_not_credited='Lil Gate opens original rockfall/map quest before ceremony;9200-15400 are not ceremony holds.',
        extra_real_growth_holds=[dict(frame=7000,capture=frames[7000],lines=[header.decode()]),
                                 dict(frame=7400,capture=frames[7400],lines=lines)],
        all_executed_fixture_receipts_recomputed_exact=True,
        all_original_and_disposable_input_saves_hash_unchanged=True,
        ordinary_formatter_sha256=sha(osource.encode()),modal_formatter_sha256=sha(msource.encode()),
        no_paired_cross_captain_outcome_or_full_route_or_hardware_verification_claim=True,
        final_family_review_still_required=True,whole_family_completion_credit=0,full_goal_complete=False,
        producer_sha256=sha(Path(__file__).read_bytes())))
    print('PASS:18 preparation holds,9 clean-source records,4 new variants,3 original returns,2 extra growth holds;1224 remains.',flush=True)


if __name__ == '__main__':
    main()
