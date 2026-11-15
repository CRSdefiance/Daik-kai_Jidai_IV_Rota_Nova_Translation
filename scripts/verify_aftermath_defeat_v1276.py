"""Original crew-abandonment and flagship-loss glyphs and defeat-to-title flow."""
import inspect
import struct
from pathlib import Path
from shutil import copy2
from types import FunctionType
from PIL import Image

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.battle_aftermath_editorial import current_entries
from dk4tool.rom.nds import NdsImage
from scripts import verify_aftermath_victory_v1271 as previous
from scripts.native_aftermath_defeat_fixture_v1274 import ROM,apply_fixture
from scripts.verify_common_alignment_native_v257 import raster as original_raster
from scripts.verify_shipyard_gameplay_v760 import independent_font
from scripts.verify_personal_gameplay_v841 import get_machine
from scripts.verify_village_wrap_v608 import read,save

ROOT = Path('work/analysis/aftermath_defeat_verified_v1276')
RUN = Path('work/analysis/aftermath_defeat_v1275')
CAP = Path('E:/Rota Nova translations/Generated/work/emulation_v193/aftermath_defeat_v1275_1266')
GUIDE = Path('E:/Rota Nova translations/Guide screenshots/V1266 Defeat aftermath')
BASE = 0x02000000


def main():
    # Reuse every original31 fixture/full-RAM/identity/RNG/input assertion.
    # Only terminal frame,fixture request and input-free interval differ.
    source = inspect.getsource(previous.main)
    source = source[:source.index('    entries = current_entries(common,arm)')]+'    return locals()\n'
    replacements = {
        "report['frames'] == 11782":"report['frames'] == 7802",
        "else {'duel_context':'healthyContact'}":"else {'duel_context':'unarmoredContact'}",
        "5773 <= e['start'] <= 10982":"5773 <= e['start'] <= 6922",
    }
    for old,new in replacements.items():
        assert source.count(old) == 1
        source = source.replace(old,new)
    env = {**previous.__dict__,'__file__':__file__,'ROOT':ROOT,'RUN':RUN,'CAP':CAP,'GUIDE':GUIDE,
        'ROM':ROM,'apply_fixture':apply_fixture}
    exec(compile(source,__file__,'exec'),env)
    audit = env['main']()
    raw,arm,common,rom = (audit[k] for k in ('raw','arm','common','rom'))
    entries = current_entries(common,arm)
    font_path = Path('work/analysis/battle_aftermath_fonts_v1260/native_font_proof.json')
    font = read(font_path)
    escape_path = Path('work/analysis/battle_aftermath_escape_v1262/original_direct_escape_regression.json')
    escape = read(escape_path)
    assert font['ARM9_sha256'] == escape['ARM9_sha256'] == sha(arm)
    assert font['COMMON_sha256'] == escape['COMMON_sha256'] == sha(common)
    cases = {n:next(c for c in font['cases'] if c['message_id'] == n and c['name_case'] is None) for n in (2016,2138)}
    escape_case = next(c for c in escape['all13_original_direct_pipeline_cases'] if c['message_ID'] == 1973)
    class CurrentFont:
        @staticmethod
        def open(path):
            assert path == 'out/all_routes_combined_v255_candidate.nds'
            return rom
    raster = FunctionType(original_raster.__code__,{**original_raster.__globals__,'NdsImage':CurrentFont},argdefs=original_raster.__defaults__)
    owner,wrapped = [struct.unpack_from('<I',arm,o)[0] for o in (0x552A0,0x54450)]
    holds = []
    for n,frames,table in ((1973,(6902,6922),0x02117620),(2016,(7042,7052),0x02117760),(2138,(7162,7172),0x02117F00)):
        formatted = bytes.fromhex(escape_case['formatted_hex'] if n == 1973 else cases[n]['native_formatted_hex'])
        lines = [v.strip().decode('ascii') for v in formatted.split(b'\n')]
        pixels = raster(arm,formatted,0x01FFCE40-BASE,size=(228,64),instruction_limit=2000000)
        assert pixels == independent_font(arm,rom.read_file('/GRP/KANJI.FNT'),lines)
        for frame in frames:
            body = raw(frame)
            cpu,get = get_machine(arm,body)
            fleets,actors = get(0xCB1A8),get(0xCB184)
            identity = get(0x82478,fleets+0x2090,1)
            actor = actors+4+identity*32
            assert identity == 18 and get(0x7EE08,actor) == 18 and get(0x53F4C,actor,table) == n
            assert body[owner-BASE+0x2030:owner-BASE+0x2230].split(b'\0')[0] == entries[n].text
            assert body[wrapped-BASE:wrapped-BASE+512].split(b'\0')[0] == formatted
            image_path = CAP/f'frame_{frame:06d}_navigation.png'
            image = Image.open(image_path).convert('RGB')
            expected = {(16+x,296+y) for y in range(64) for x in range(228) if pixels[y*228+x]}
            actual = {(x,y) for y in range(294,366) for x in range(16,244) if image.getpixel((x,y)) == (0,8,0)}
            assert actual == expected,(n,frame,len(expected-actual),len(actual-expected))
            holds.append({'frame':frame,'message_ID':n,'actual_original_role_or_direct_source_actor_ID':18,
                'original_voice_table':table,'source_template_and_native_wrap_exact':True,'lines':lines,
                'whole228x64_native_font_and_independent_font_equal':True,
                'complete_foreground_and_blank_paper_RGB_mask_equal':True,'matching_pixels':len(expected),
                'missing_or_unexpected_foreground_pixels':0,'uniform_visible_margins_all_letters_and_bounds_pass':True,
                'capture':str(image_path),'capture_sha256':sha(image_path.read_bytes()),'RAM_sha256':sha(body)})
    states = []
    for frame,expected in ((5782,[31,117]),(6902,[0,45]),(6922,[0,45]),(7042,[0,45]),(7172,[0,45])):
        body = raw(frame)
        cpu,get = get_machine(arm,body)
        actors = get(0xCB184)
        hp = [get(0x7E19C,o) for o in (actors+0x19E4,actors+4+32*32)]
        assert hp == expected,(frame,hp,expected)
        states.append({'frame':frame,'own_enemy_HP':hp,'RAM_sha256':sha(body)})
    reference = Path('E:/Rota Nova translations/Generated/work/emulation_v193/escape_direct_v1190_1189/frame_007802_navigation.png')
    final_path = CAP/'frame_007802_navigation.png'
    assert Image.open(final_path).tobytes() == Image.open(reference).tobytes()
    ROOT.mkdir(parents=True)
    GUIDE.mkdir(parents=True)
    effective = ROOT/'effective_fixture_input_audit.py'
    effective.write_text(source,encoding='utf-8')
    screens = []
    for label,frame in (('abandon_ship_testing_fixture',7042),('flagship_defeated_testing_fixture',7162),
                         ('original_game_over',7382),('ordinary_title_return',7802)):
        image = CAP/f'frame_{frame:06d}_navigation.png'
        dest = GUIDE/(label+'.png')
        copy2(image,dest)
        assert image.read_bytes() == dest.read_bytes()
        screens.append({'path':str(dest),'source':str(image),'frame':frame,'sha256':sha(dest.read_bytes())})
    proof = {'candidate':str(ROM),'candidate_sha256':audit['digest'],'terminal_frame':7802,
        'report':str(audit['report_path']),'report_sha256':sha(audit['report_path'].read_bytes()),
        'all31_fixture_replays':audit['audits'],'last_fixture5770_before_duel5772':True,
        'all_actor_IDs_RNG_event_words_and_full4MiB_fixture_receipts_exact':True,
        'effective_fixture_and_input_audit':str(effective),'effective_fixture_and_input_audit_sha256':sha(effective.read_bytes()),
        'no_during_or_post_combat_health_ability_equipment_location_or_result_changes':True,
        'native_positive_HP31_and_shield_inventory_test_prerequisites_disclosed_not_earned_progression':True,
        'original_natural_HP_evolution':states,'complete_actual_holds':holds,
        'actual_1973_preserved_and2016_2138_new_native_fonts_RGB_and_source_speakers_verified':True,
        'ordinary_A_abandonment_flagship_defeat_GameOver_and_title_transition_visually_reviewed':True,
        'final_title_whole_screen_exact_to_prior_original_return':str(reference),'reference_sha256':sha(reference.read_bytes()),
        'source_and_disposable_saves_unchanged':True,'guide_screenshots':screens,
        'representative_original_family_evidence_for2016_2021_and2138_2145':True,
        'only2016_and2138_have_individual_actual_activations_in_new_families':True,
        'other_aftermath_source_families_still_pending':True,
        'targeted_headless_test_not_whole_route_or_hardware_verification':True,
        'producer_sha256':sha(Path(__file__).read_bytes()),'full_goal_complete':False}
    save(ROOT/'actual_abandonment_and_flagship_defeat.json',proof)
    save(GUIDE/'provenance.json',proof)
    print('31 exact pre-duel audits;six full font/RGB holds;original abandonment/loss/GameOver/title pass.',flush=True)


if __name__ == '__main__':
    main()
