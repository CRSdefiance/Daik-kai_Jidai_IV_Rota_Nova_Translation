"""Record viewed B174 dialogue, join notice, town return and scoped native state."""
import json
import struct
from pathlib import Path
from PIL import Image,ImageChops
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_market_gameplay_v753 import state
from scripts.verify_shipyard_gameplay_v760 import models
from scripts.verify_tavern_gameplay_v767 import persistent_objects
from scripts.verify_followup_gameplay_v778 import tasks
from scripts.verify_ceremony_prayer_gameplay_v814 import calendar
from scripts.verify_personal_gameplay_v841 import get_machine
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/lil_B174_actual_review_v4490b')
ACTUAL=Path('work/analysis/lil_B174_actual_v4489c/actual_all33_unforced_predicate_paths_effects_C200_and_end.json')
FIXTURE=Path('work/analysis/lil_B174_display_fixture_v4487/complete_effect_preserving_B22_fixtures.json')
BASE=Path('E:/Rota Nova translations/Generated/work/emulation_v193')

def native_json(value):
    assert isinstance(value,bytes),type(value)
    return {'native_byte_span_hex':value.hex()}

if __name__=='__main__':
    assert not ROOT.exists()
    actual,fixture=map(read,[ACTUAL,FIXTURE])
    assert actual['fresh_actual_unique_speech_panels']==actual['complete_matching_observations']==32
    assert not actual['failures'] and not actual['paired_region_differences']
    assert actual['offline_only_display_IDs']==['DK4_MES_B174_R0069']
    assert [v['fixture_exit_frame'] for v in actual['versions']]==[10776,10774]
    sheets=[]
    for sheet in actual['review_sheets']:
        assert sha(Path(sheet['path']).read_bytes())==sheet['sha256']
        sheets.append({**sheet,'viewed':True,'review':
            'Viewed every complete selected panel in exchange order. Lil Argot, Julian Lopes and Mihwa portraits/nameplates are intact. '
            'Read gratitude/first crown discovery and gift, dry response, adventure boast/flustered trading correction, ship-versus-running banter, '
            'collapse/rest, fate hyperbole, actual-grandfather aspiration, knowledge assurance/acceptance, renewed flirting/overboard retort, '
            'jealousy/employer explanation, conditional better-item return/date proposal and closing aside as one coherent exchange. '
            'All ten retentions work in context. First/internal/final glyphs, ordinary wraps and both proper titles are complete. '
            'Optional Emilio R69 was not selected under the original result0 and retains offline native coverage. No translation-specific display finding.'})
    assert len(sheets)==6
    reports=[];photos=[];snapshots=[];arms=[];paths=[ACTUAL,FIXTURE,Path(__file__)]
    for item in fixture['fixtures']:
        folder=BASE/('lil_B174_display_v4488_'+item['case'])
        reportpath=folder/'capture_report.json';report=read(reportpath)
        assert report['frames']==16001 and report['cold_boot'] and not report['savestate_loaded'] and not report['callback_errors']
        assert report['ROM_sha256']==item['research_ROM_sha256']==sha(Path(item['research_ROM']).read_bytes())
        snapshot=report['read_only_RAM_snapshot'];raw=Path(snapshot['path']).read_bytes()
        assert snapshot['read_only_export'] and len(raw)==4194304 and sha(raw)==snapshot['sha256']
        arm=NdsImage.open(item['research_ROM']).read_file('/__arm9__.bin')
        reports.append(report);photos.append({p['frame']:p for p in report['frames_captured']});snapshots.append((snapshot,raw));arms.append(arm)
        paths.extend([reportpath,Path(snapshot['path']),folder/'observer/commands.json'])
    assert arms[0]==arms[1] and photos[0].keys()==photos[1].keys()
    comparisons=[]
    for frame,source in sorted(photos[0].items()):
        english=photos[1][frame]
        for p in [source,english]:assert sha(Path(p['path']).read_bytes())==p['PNG_sha256']
        a,b=[Image.open(p['path']).convert('RGB') for p in [source,english]]
        assert ImageChops.difference(a.crop((0,0,256,294)),b.crop((0,0,256,294))).getbbox() is None,frame
        comparisons.append(dict(frame=frame,source=source,English=english,upper_portrait_name_regions_equal=True,whole_RGB_equal=a.tobytes()==b.tobytes()))
    assert len(comparisons)==232
    assert all(next(c for c in comparisons if c['frame']==f)['whole_RGB_equal'] for f in [10810,16001])
    notes={10570:'Viewed whole original screen during source A0002076: complete existing Julian Lopes joined! notice, including leading J and trailing exclamation, within original bounds. Both versions use current shared English assets; only B174 story bodies differ. The original A-button indicator is in a different blink phase, without a changed notice glyph.',
        10810:'Viewed whole-RGB-identical initialized Amsterdam town return after6240,both A000s,C200 and the single end. Amsterdam is the disclosed B22 fixture location, not an inferred B174 source location.',
        16001:'Viewed whole-RGB-identical following B120 Camille dialogue at the capture endpoint. No new B120 editorial credit or natural B174 eligibility is claimed.'}
    views=[]
    for version,photoset in zip(['clean_Japanese','reviewed_English'],photos,strict=True):
        for frame,note in notes.items():
            p=photoset[frame]
            views.append(dict(case=version,frame=frame,path=p['path'],sha256=p['PNG_sha256'],viewed=True,review=note))
    notice=[Image.open(p[10570]['path']).convert('RGB') for p in photos]
    assert notice[0].crop((16,296,232,360)).tobytes()==notice[1].crop((16,296,232,360)).tobytes()
    notice_difference=ImageChops.difference(*notice).getbbox()
    assert notice_difference==(224,360,240,376)
    native=[]
    for (snapshot,raw),arm in zip(snapshots,arms,strict=True):
        components={fn.__name__:fn(arm,raw) for fn in [state,models,persistent_objects,tasks,calendar]}
        cpu,get=get_machine(arm,raw);root,captain=get(0xCB184),get(0x7F244)
        assert captain==2 and 0x02000000<=root<=0x02400000-0x1A04
        actor=bytes(cpu.mem_read(root,0x1A04))
        native.append(dict(snapshot=snapshot,components=components,actor=actor,actor_root=root,captain_ID=captain,seed=struct.unpack_from('<I',raw,0x168EB8)[0]))
    component_equal={key:native[0]['components'][key]==native[1]['components'][key] for key in native[0]['components']}
    assert all(component_equal.values()) and native[0]['actor']==native[1]['actor']
    timings=[dict(source=a,English=b) for a,b in zip(actual['versions'][0]['selected_B22_command_pairs'],actual['versions'][1]['selected_B22_command_pairs'],strict=True)
        if (a['start'],a['returned'])!=(b['start'],b['returned'])]
    for version in actual['versions']:
        assert len(version['selected_B22_command_pairs'])==51 and version['unforced_predicate_result']==0
        assert version['actual_predicate']['result_words']==[2,0]
        assert [r['original_source_offset'] for r in version['actual_source_A000s']]==[2068,2076]
        assert [r['result_words'] for r in version['actual_source_A000s']]==[[3,0],[3,0]]
        assert [r['original_source_offset'] for r in version['actual_source_relative_commands']]==[882,890]
        assert all(r['result_words']==[3,0] and r['extent']==r['independently_verified_native_extent'] for r in version['actual_source_relative_commands'])
        assert version['actual_presentation_commands'][-1]['result_words']==[3,0]
        assert len(version['actual_source_C200'])==1 and version['actual_source_C200'][0]['result_words']==[3,0]
        assert version['selected_B22_command_pairs'][-1]['result_words']==[0,0]
        assert [r['source_offset'] for r in version['unvisited_declared_source_objects']]==[886,894,938]
        assert version['following_observed_blocks']==[120]
        held=version['actual_source_A000s'][1];assert held['start']<10570<held['returned']
    ROOT.mkdir(parents=True)
    save(ROOT/'all6_actual_sheets_optional_scope_join_notice_paired_return_and_final_state.json',dict(
        all6_actual_sheets_viewed=sheets,paired_full_screen_views=views,all232_sampled_nontext_region_checks=comparisons,
        all32_complete_held_planes_and_source_paired_regions_match=True,all232_sampled_nontext_regions_equal=True,
        offline_only_display_IDs=actual['offline_only_display_IDs'],whole_RGB_town10810_and_final16001_equal=True,
        source_and_English_unforced_predicate_result=0,both_source_A0002068_and2076_actually_executed=True,
        source_C2002084_actually_executed=True,source_relative_sites882890_actual_886894938_offline_native_only=True,
        original_VM_last_result0_preserved_through_type3_commands_C200_and_end=True,
        isolated_parser_output_and_actual_player_descriptor_are_distinct_scopes=True,
        source_single_end2086_actually_reached=True,source_packed_effect_and_predicate_semantics_not_inferred=True,
        source_45_structural_commands_and_original_nine_init_stored_no_omission_or_flattening=True,
        actual51_selected_commands_in_both_versions=True,actual_timing_differences=timings,
        exact_timing_difference_counts=dict(total=len(timings),speech=sum(r['source']['word']==0x4000 for r in timings),control_or_end=sum(r['source']['word']!=0x4000 for r in timings)),
        source_and_relocated_skip_extents_independently_bound=True,actual_source890_extent52_and_English_extent62_expected=True,
        join_notice10570_complete_shared_text_plane_equal=True,join_notice_full_RGB_difference_is_original_A_button_indicator=notice_difference,
        join_notice_leading_J_full_Julian_Lopes_and_trailing_exclamation_viewed=True,
        postscene16001_native_component_equality=component_equal,
        postscene16001_component_hashes=[{key:sha(json.dumps(value,sort_keys=True,default=native_json).encode('utf-8')) for key,value in row['components'].items()} for row in native],
        postscene16001_whole1A04_actor_models_and_captain2_equal=True,
        postscene16001_actor_samples=[dict(snapshot=row['snapshot'],actor_root=row['actor_root'],actor_bytes=len(row['actor']),actor_sha256=sha(row['actor']),captain_ID=row['captain_ID']) for row in native],
        postscene16001_PRNG_seeds=[row['seed'] for row in native],PRNG_equality_or_future_world_equivalence_not_claimed=True,
        full_RAM_equality_not_claimed_native_getters_run_on_exported_copies_only=True,
        no_open_translation_specific_display_or_control_finding=True,representative_actual_coverage_sufficient_for_this_distinct_display_scope=True,
        two16001_frame_content_boots_no_extra_repeats_needed_for_an_unobserved_later_outcome=True,
        no_natural_event_eligibility_earned_flags_full_route_or_hardware_claim=True,new_emulator_runs=2,
        evidence={str(p):sha(p.read_bytes()) for p in paths},producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print(dict(viewed_actual_sheets=6,complete_panels=32,offline_only=actual['offline_only_display_IDs'],
        sampled_nontext_regions=232,nontext_differences=0,paired_return10810=True,
        final16001_component_and_actor_equality=True,actual_predicate0_two_effects_and_C200=True,
        timing_differences=len(timings),new_boots=2,full_goal_active=True))
