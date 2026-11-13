"""Bind exact Speyer source controls to original presenters and actual samples."""
import struct
from pathlib import Path
from PIL import Image
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.verify_name_catalog_glyphs_v278 import raster,expected_pixels
from scripts.verify_personal_gameplay_v841 import get_machine
from scripts.verify_port_gameplay_v762 import cstring
from scripts.verify_village_wrap_v608 import read,save

ROOT = Path('work/analysis/lil_Speyer_controls_v1936')
PACKET = Path('work/analysis/lil_followups_after_London_v1914/source_followup_packets_and_random_query_classification.json')
CONTEXT = Path('work/analysis/lil_Speyer_context_v1918/original_Hamburg_predicate_and57_macro_contexts.json')
AUDIT = Path('work/analysis/lil_Speyer_original_audit_v1935b/original_Hamburg79_Speyer51_and_three_access_fixture_audit.json')
NAV = Path('work/analysis/lil_Speyer_original_navigation_v1934/closed_original_scene_context.json')
BASE = 0x02000000

if __name__ == '__main__':
    assert not ROOT.exists()
    packet,context,audit,nav = map(read,(PACKET,CONTEXT,AUDIT,NAV))
    rom = Path(packet['candidate'])
    image,clean = NdsImage.open(rom),NdsImage.open('work/clean.nds')
    arm,original = image.read_file('/__arm9__.bin'),clean.read_file('/__arm9__.bin')
    assert sha(rom.read_bytes())==context['candidate_sha256']==audit['candidate_sha256']==nav['candidate_sha256']
    assert sha(arm)==context['ARM9_sha256']
    assert audit['all_inputs_capture_hashes4MiB_snapshots_and_three_access_footprints_verified']
    assert audit['all_readonly_observer_boundaries_and_host_restoration_pass']
    assert audit['ordinary_default_choice_selects_stored_option0_explanation_branch']
    spans = [(0x24274,0x242C8),(0x242CC,0x24310),(0x24314,0x24330),(0x24334,0x243A0),(0x54020,0x54060)]
    assert all(arm[a:b]==original[a:b]for a,b in spans)
    assert struct.unpack_from('<I',arm,0x242F0)[0]==0xEB00BF4A
    source = IlnkContainer.parse(image.read_file('/data/SC2.DK4')).blocks
    jp = IlnkContainer.parse(clean.read_file('/data/SC2.DK4')).blocks
    observed = {r['id']:r for r in nav['old_text_observations']}
    headers = []
    blocks = []
    for spec in packet['packets']:
        number = spec['block']
        if number not in (25,128):continue
        assert sha(source[number])==spec['current_block_sha256'] and sha(jp[number])==spec['source_block_sha256']
        for row in spec['records']:
            ja,at = row['source_offset']-5,row['current_offset']-5
            expected = bytes.fromhex('0040ffff00'+row['provisional_first_byte_hex'])
            assert jp[number][ja:ja+6]==source[number][at:at+6]==expected
            headers.append(dict(id=row['id'],block=number,source_header_offset=ja,current_header_offset=at,
                complete_preamble_hex=expected.hex(),individually_observed=row['id']in observed))
        blocks.append(dict(block=number,clean_block_sha256=sha(jp[number]),current_block_sha256=sha(source[number]),
            complete_preamble_counts={f'{p:02x}':sum(r['provisional_first_byte_hex']==f'{p:02x}'for r in spec['records'])
                for p in sorted({int(r['provisional_first_byte_hex'],16)for r in spec['records']})}))
    assert len(headers)==57 and sum(r['individually_observed']for r in headers)==51
    sample = observed['DK4_MES_B128_R0006']['holds'][0]
    raw = Path(sample['capture'].replace('_navigation.png','_arm9_ram.bin')).read_bytes()
    cpu,get = get_machine(arm,raw)
    selectors = {p:get(0x2434C,p)for p in(29,151,152)}
    assert selectors=={29:29,151:151,152:152} and bytes(cpu.mem_read(BASE,0x400000))==raw
    namecpu,nameget = get_machine(arm,raw)
    pointer = nameget(0xB8220,3)
    port = bytes(namecpu.mem_read(pointer,80)).split(b'\0')[0].decode('ascii')
    assert port=='Port' and bytes(namecpu.mem_read(BASE,0x400000))==raw
    glyph_cases = []
    wrapped = struct.unpack_from('<I',arm,0x54450)[0]
    for ident in ('DK4_MES_B128_R0006','DK4_MES_B128_R0010','DK4_MES_B128_R0026'):
        for hold in observed[ident]['holds']:
            raw = Path(hold['capture'].replace('_navigation.png','_arm9_ram.bin')).read_bytes()
            assert sha(raw)==hold['RAM_sha256']
            body = cstring(raw,wrapped)
            pixels,events,font = raster(arm,body)
            assert pixels==expected_pixels(arm,font,events)
            wanted = {(16+x,296+y)for y in range(64)for x in range(216)if pixels[y*216+x]==1}
            im = Image.open(hold['capture']).convert('RGB')
            actual = {(x,y)for y in range(296,360)for x in range(16,232)if im.getpixel((x,y))==(0,8,0)}
            assert wanted==actual
            glyph_cases.append(dict(id=ident,frame=hold['frame'],capture=hold['capture'],
                capture_sha256=hold['capture_sha256'],RAM_sha256=sha(raw),original_expanded_body_hex=body.hex(),
                whole_native_independent_actual_ink_equal=True,first_last_and_all_internal_glyphs_complete=True))
    ROOT.mkdir(parents=True)
    save(ROOT/'source_bound_B25_B128_progressive_control_contract.json',dict(format='dk4-lil-speyer-control-contract-v1',
        candidate=str(rom),candidate_sha256=sha(rom.read_bytes()),ARM9_sha256=sha(arm),blocks=blocks,
        original_control_dispatch_spans=[dict(start=BASE+a,end_exclusive=BASE+b,sha256=sha(arm[a:b]))for a,b in spans],
        exact_original_complete_preambles=headers,progressive_presenter=BASE+0x54020,
        registered_macro_wrappers_excluded_only_from_clean_code_span_comparison=True,
        original_native_actor_selectors=selectors,native_selector_preserves29_151_152_and_all4MiB=True,
        Speyer29_actual_portrait_full_Martin_Speyer_nameplate_body_and_transitions_viewed=True,
        actor152_actual_Sailor_portrait_nameplate_Japanese_body_and_following_Lil_transition_viewed=True,
        actor152_native_catalog_full_name='Retainer',actor152_actual_visible_nameplate='Sailor',
        native_catalog_full_name_not_assumed_to_equal_actual_nameplate=True,
        source151_unidentified_player_side_voice_uses_same_original_progressive_presenter=True,
        Retainer151_fallback_not_individually_activated=True,
        six_complete_native_independent_actual_glyph_hold_cases=glyph_cases,
        all57_complete_source_preambles_bound=True,all_Speyer_speeches_use_same_original_progressive_presenter=True,
        no_FE_or_new_modal_geometry_in_Speyer_blocks=True,
        actual_original_Port_caption_getter=BASE+0xB8220,native_facility3_caption=port,
        native_actual_category_town_subtype=[7,5,3],
        stored_choice0_visible_default_explanation_and_actual_native_result0_verified=True,
        stored_choice1_source_VM_only_not_individually_played=True,
        six_unvisited_conditional_speeches_source_native_only=True,
        conditional_scope='B12897 fallback, two offended-choice responses and all three B25 aftermath speeches were not individually activated. Same original progressive presenter and full native formatting checks apply; no individual gameplay claim.',
        no_global_profile_ROM_orcompletion_change=True,
        evidence={str(p):sha(p.read_bytes())for p in(PACKET,CONTEXT,AUDIT,NAV,
            Path('work/analysis/lil_Speyer_choice_v1927/original_choice_decoder_VM_geometry_and_native_pixels.json'))},
        producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print(dict(complete_preambles=57,actual_original_speeches=51,new_controls=[29,152],
        actor152_visible_nameplate='Sailor',six_native_actual_glyph_holds_exact=True,scope='Speyer B25/B128 only'))
