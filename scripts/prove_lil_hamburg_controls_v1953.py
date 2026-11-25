"""Bind all B74 preambles to the exact runtime and closed original captures."""
import struct
from collections import Counter
from pathlib import Path
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.verify_personal_gameplay_v841 import get_machine
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/lil_Hamburg_controls_v1953')
PACKET = Path('work/analysis/lil_Hamburg_source_v1949/all79_source_native_context_and_two_choices.json')
NAV = Path('work/analysis/lil_Hamburg_arrival_navigation_v1933/closed_original_scene_context.json')
AUDIT = Path('work/analysis/lil_Speyer_original_audit_v1935b/original_Hamburg79_Speyer51_and_three_access_fixture_audit.json')
BASE = 0x02000000

if __name__ == '__main__':
    assert not ROOT.exists()
    packet, nav, audit = map(read, (PACKET, NAV, AUDIT))
    rom = Path(packet['candidate'])
    im, clean = NdsImage.open(rom), NdsImage.open('work/clean.nds')
    arm, original = im.read_file('/__arm9__.bin'), clean.read_file('/__arm9__.bin')
    assert sha(arm) == packet['ARM9_sha256'] == '500b7d6cea559d7252ae4e67f94540e67739428823a17cf26842b6827712a41e'
    assert sha(rom.read_bytes()) == packet['candidate_sha256']
    assert audit['all_inputs_capture_hashes4MiB_snapshots_and_three_access_footprints_verified']
    assert audit['all_readonly_observer_boundaries_and_host_restoration_pass']
    assert audit['B74_tutorial_choice0_Yes_please_observed_choice1_not_played']
    assert nav['original_process_closed']
    spans = [(0x24274,0x242C8),(0x242CC,0x24310),(0x24314,0x24330),
             (0x24334,0x243A0),(0x54020,0x54060),(0x5473C,0x54784)]
    assert all(arm[a:b] == original[a:b] for a,b in spans)
    assert struct.unpack_from('<I',arm,0x242F0)[0] == 0xEB00BF4A
    assert struct.unpack_from('<I',arm,0x24318)[0] == 0xEB00C107
    source = IlnkContainer.parse(im.read_file('/data/SC2.DK4')).blocks[74]
    jp = IlnkContainer.parse(clean.read_file('/data/SC2.DK4')).blocks[74]
    captured_im = NdsImage.open(nav['candidate'])
    assert sha(source) == packet['current_block_sha256']
    assert sha(jp) == packet['clean_block_sha256']
    assert captured_im.read_file('/__arm9__.bin') == arm
    assert IlnkContainer.parse(captured_im.read_file('/data/SC2.DK4')).blocks[74] == source
    # The original full capture ROM predates V1945: only these exact B74 and
    # runtime bytes are claimed equal, never the two entire ROMs.
    assert sha(Path(nav['candidate']).read_bytes()) == nav['candidate_sha256']
    observed = {r['id']:r for r in nav['old_text_observations']}
    assert len(observed) == 79
    headers = []
    for row in packet['records']:
        ja, at = row['source_reference']['header_offset'], row['current_reference']['header_offset']
        prefix = row['source_presentation_prefix_hex']
        expected = bytes.fromhex('0040ffff00'+prefix)
        assert jp[ja:ja+6] == source[at:at+6] == expected
        actual = observed[row['id']]
        assert actual['prefix_hex'] == prefix
        assert actual['source']['whole_resident_payload_exact_ROM']
        assert actual['source']['actual_sha256'] == sha(source)
        assert actual['source']['instruction_offset'] == at
        headers.append(dict(id=row['id'],source_header_offset=ja,current_header_offset=at,
            complete_preamble_hex=expected.hex(),individually_observed=True,
            original_hold_frames=[h['frame'] for h in actual['holds']]))
    counts = Counter(r['source_presentation_prefix_hex'] for r in packet['records'])
    assert counts == {'10':30,'09':23,'02':20,'fe':3,'0e':2,'14':1}
    for prefix, count in counts.items():
        assert source.count(bytes.fromhex('0040ffff00'+prefix)) == count
    sample = observed['DK4_MES_B74_R0056']['holds'][1]
    raw = Path(sample['capture'].replace('_navigation.png','_arm9_ram.bin')).read_bytes()
    assert sha(raw) == sample['RAM_sha256']
    cpu, get = get_machine(arm,raw)
    assert get(0x2434C,16) == 16
    assert bytes(cpu.mem_read(BASE,0x400000)) == raw
    actors = get(0xCB184)
    assert bytes(cpu.mem_read(BASE,0x400000)) == raw
    cp, q = get_machine(arm,raw)
    actor = actors+4+16*32
    vt = struct.unpack('<I',cp.mem_read(actor,4))[0]
    fn = struct.unpack('<I',cp.mem_read(vt+8,4))[0]
    assert fn == 0x0207EDD4
    p = q(fn-BASE,actor)
    name = bytes(cp.mem_read(p,100)).split(b'\0')[0].decode('cp932')
    assert name == 'Gerhard Ardelknatts'
    after = bytes(cp.mem_read(BASE,0x400000))
    delta = [dict(address=BASE+i,before=a,after=b) for i,(a,b) in enumerate(zip(raw,after,strict=True)) if a!=b]
    assert len([r for r in headers if r['complete_preamble_hex'].endswith('fe')]) == 3
    ROOT.mkdir(parents=True)
    save(ROOT/'source_bound_B74_presenter_and_control_contract.json',dict(
        format='dk4-lil-hamburg-control-contract-v1',candidate=str(rom),candidate_sha256=sha(rom.read_bytes()),
        ARM9_sha256=sha(arm),clean_B74_sha256=sha(jp),current_B74_sha256=sha(source),
        original_capture_candidate=nav['candidate'],original_capture_candidate_sha256=nav['candidate_sha256'],
        original_capture_B74_and_ARM9_exact_current=True,original_capture_not_claimed_whole_ROM_equal_current=True,
        original_control_dispatch_spans=[dict(start=BASE+a,end_exclusive=BASE+b,sha256=sha(arm[a:b])) for a,b in spans],
        registered_macro_wrappers_only_excluded_from_clean_code_spans=True,
        exact_original_complete_preambles=headers,complete_preamble_counts=dict(counts),
        progressive_presenter=0x02054020,FE_modal_presenter=0x0205473C,
        native_selector_preserves16_and_all4MiB=True,native_Gerhard_name=name,
        actor=actor,name_getter=fn,name_getter_cache_changes_on_separate_disposable_copy=delta,
        name_getter_not_claimed_pure=True,
        Gerhard10_actual_portrait_full_nameplate_and_following_dialogue_viewed=True,
        three_FE_actual_anonymous_portrait_free_paper_panels_viewed=True,
        FE_uses_original_separate_consumer_and_null_actor_macro_caller=True,
        FE_not_reinterpreted_via_fallback_actor_selector=True,
        all79_original_speeches_individually_observed=True,
        original_join_panel_tutorial_choice0_and_normal_Hamburg_return_captured=True,
        FE_geometry_glyphs_pagination_and_revised_actual_tests_still_pending=True,
        no_global_profile_ROM_orcompletion_change=True,
        evidence={str(p):sha(p.read_bytes()) for p in (PACKET,NAV,AUDIT)},
        producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print(dict(complete_preambles=79,counts=dict(counts),Gerhard_name=name,original_B74_runtime_exact_current=True))
