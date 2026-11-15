"""Bind B26 controls to original shared presenters and representative gameplay."""
import struct
from pathlib import Path
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.verify_personal_gameplay_v841 import get_machine
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/lil_London_controls_v1893')
PACKET=Path('work/analysis/lil_London_source_v1879b/all111_clean_current_native_source_context.json')
AUDIT=Path('work/analysis/lil_London_context_audit_v1892/original_London105_branch_and_three_fixture_audit.json')
NAV=Path('work/analysis/lil_London_context_navigation_v1891/closed_original_B26_context.json')
GERHARD=Path('work/analysis/Gerhard_story_control_proof_v1857/original4000_prefix10_Gerhard_live_mapping.json')
BASE=0x02000000

if __name__=='__main__':
    assert not ROOT.exists()
    packet,audit,nav,gerhard=map(read,(PACKET,AUDIT,NAV,GERHARD))
    rom=Path(packet['candidate'])
    image,clean=NdsImage.open(rom),NdsImage.open('work/clean.nds')
    arm,original=image.read_file('/__arm9__.bin'),clean.read_file('/__arm9__.bin')
    assert sha(arm)==gerhard['ARM9_sha256']==packet['ARM9_sha256']
    assert sha(rom.read_bytes())==audit['candidate_sha256']==nav['candidate_sha256']
    assert audit['all_inputs_capture_hashes4MiB_snapshots_and_three_coordinate_footprints_verified']
    assert audit['all_readonly_observer_boundaries_and_host_restoration_pass']
    assert gerhard['actual_Gerhard_portrait_full_nameplate_body_and_normal_next_Hodram_portrait_viewed']
    # Current native macro calls are an accepted guarded wrapper; bind their
    # exact runtime, and compare the unchanged original presenter/selector logic.
    spans=[(0x24274,0x242C8),(0x242CC,0x24310),(0x24314,0x243A0),(0x54020,0x54060),(0x5473C,0x54784)]
    assert all(arm[a:b]==original[a:b] for a,b in spans)
    assert struct.unpack_from('<I',arm,0x242F0)[0]==0xEB00B346
    assert struct.unpack_from('<I',arm,0x24318)[0]==0xEB00C108
    source=IlnkContainer.parse(image.read_file('/data/SC2.DK4')).blocks[26]
    japanese=IlnkContainer.parse(clean.read_file('/data/SC2.DK4')).blocks[26]
    assert sha(source)==packet['current_block_sha256'] and sha(japanese)==packet['clean_block_sha256']
    observations={r['id']:r for r in nav['old_text_observations']}
    selected=[r for r in packet['records'] if r['source_presentation_prefix_hex'] in ('97','10','1c','fe')]
    assert len(selected)==43
    headers=[]
    for r in selected:
        ja=r['source_reference']['header_offset']
        at=r['current_reference']['header_offset']
        expected=bytes.fromhex('0040ffff00'+r['source_presentation_prefix_hex'])
        assert japanese[ja:ja+6]==source[at:at+6]==expected
        headers.append(dict(id=r['id'],source_header_offset=ja,current_header_offset=at,
            complete_preamble_hex=expected.hex(),individually_observed=r['id'] in observations))
    first=observations['DK4_MES_B26_R0137']
    raw=Path(first['holds'][1]['capture'].replace('_navigation.png','_arm9_ram.bin')).read_bytes()
    cpu,get=get_machine(arm,raw)
    actor_ids={p:get(0x2434C,p) for p in (16,28,151)}
    assert actor_ids=={16:16,28:28,151:151}
    assert bytes(cpu.mem_read(BASE,0x400000))==raw
    actors=get(0xCB184)
    names={}
    for prefix in actor_ids:
        cp,q=get_machine(arm,raw)
        actor=actors+4+prefix*32
        vt=struct.unpack('<I',cp.mem_read(actor,4))[0]
        fn=struct.unpack('<I',cp.mem_read(vt+8,4))[0]
        assert fn==0x0207EDD4
        p=q(fn-BASE,actor)
        name=bytes(cp.mem_read(p,100)).split(b'\0')[0].decode('cp932')
        after=bytes(cp.mem_read(BASE,0x400000))
        delta=[dict(address=BASE+i,before=a,after=b) for i,(a,b) in enumerate(zip(raw,after,strict=True)) if a!=b]
        names[str(prefix)]=dict(native_name=name,actor=actor,name_getter=fn,
            cache_changes_on_separate_disposable_copy=delta,name_getter_not_claimed_pure=True)
    assert names['28']['native_name']=='James Clifford'
    assert names['16']['native_name']=='Gerhard Ardelknatts'
    assert names['151']['native_name']=='Retainer'
    fe=[observations[r['id']] for r in selected if r['source_presentation_prefix_hex']=='fe']
    assert len(fe)==3
    # Prefix FE is tested before fallback actor resolution in original242FC..
    # 24320 and uses5473C. Never reinterpret it through2434C as actor208.
    assert all(r['prefix_hex']=='fe' for r in fe)
    seen={r['id'] for r in selected if r['id'] in observations}
    unseen={r['id'] for r in selected if r['id'] not in observations}
    assert len(seen)==37 and len(unseen)==6
    ROOT.mkdir(parents=True)
    save(ROOT/'source_bound_B26_presenter_and_control_contract.json',dict(
        format='dk4-lil-london-control-contract-v1',candidate=str(rom),candidate_sha256=sha(rom.read_bytes()),
        ARM9_sha256=sha(arm),clean_B26_sha256=sha(japanese),current_B26_sha256=sha(source),
        original_control_dispatch_spans=[dict(start=BASE+a,end=BASE+b,sha256=sha(arm[a:b])) for a,b in spans],
        progressive_presenter=0x02054020,FE_modal_presenter=0x0205473C,
        exact_original_preambles=headers,native_actor_catalog=names,
        native_selector_preserves16_28_and151_and_all4MiB=True,
        Clifford28_actual_portrait_full_nameplate_body_and_following_Camille_transition_viewed=True,
        three_FE_actual_anonymous_portrait_free_paper_panels_viewed=True,
        original_outfit_pan_and_normal_London_town_return_actually_viewed=True,
        Gerhard10_shared_preamble_matches_actual_SC1B42_proof=True,
        Retainer97_uses_same_original_progressive_presenter_and_actor151_catalog=True,
        Retainer97_not_individually_activated_no_portrait_or_nameplate_live_claim=True,
        no_distinct_unresolved_new_renderer_for_six_conditional_records=True,
        conditional_scope='Five Gerhard10 andone97Retainer fallback areoffline/source-native only. Their original shared progressive presenter isrepresentatively tested;no individual visits claimed.',
        FE_consumer_geometry_and_new_font_planes_still_require_separate_native_proof=True,
        no_global_profile_or_ROM_orcompletion_change=True,
        evidence={str(p):sha(p.read_bytes()) for p in (PACKET,AUDIT,NAV,GERHARD,
            Path('work/analysis/lil_London_control_sheet_v1890b/contact_sheet_provenance.json'),
            Path('work/analysis/lil_London_context_navigation_v1891/inherited_observations_and_automatic_art_pan.json'))},
        producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print(dict(progressive_new_controls=[16,28,151],FE_anonymous_objects=3,conditional_offline_only=6,all43_preambles_bound=True))
