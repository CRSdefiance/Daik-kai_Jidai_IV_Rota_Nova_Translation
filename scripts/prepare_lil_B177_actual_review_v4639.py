"""Prepare measured B177 review without inheriting B176 timing or PRNG equality claims."""
from pathlib import Path
from scripts.prepare_lil_B156_layout_v3705 import derive
from scripts.verify_village_wrap_v608 import save

root=Path('work/analysis/lil_B177_actual_review_tools_v4639')
assert not root.exists()
tool=derive('scripts/review_lil_B176_actual_v4589.py','scripts/review_lil_B177_actual_v4639.py',{
    'B176':'B177','lil_B176':'lil_B177','actual_review_v4589':'actual_review_v4639',
    'actual_v4588':'actual_v4638','display_fixture_v4585':'display_fixture_v4635','display_v4587':'display_v4637',
    'whole_RGB_equal=a.tobytes()==b.tobytes()':'whole_frame_difference_bbox=ImageChops.difference(a,b).getbbox(),whole_RGB_equal=a.tobytes()==b.tobytes()',
    "    assert all(r['whole_RGB_equal'] for r in comparisons if r['frame']>=5290)":
    """    differences=[r for r in comparisons if r['frame']>=5290 and not r['whole_RGB_equal']]
    assert {r['frame'] for r in differences}=={6010,6190,7210,7390,7450,7630,7690,7870,8170,8350,8410,8590,8770,8950}
    assert len(differences)==14
    for row in differences:
        x0,y0,x1,y1=row['whole_frame_difference_bbox']
        assert 224<=x0<x1<=240 and 360<=y0<y1<=376
        row.update(scope='Following town/tutorial original A-button indicator animation only;full unmasked RGB difference box retained. Text glyphs and upper/portrait/name regions remain equal. No screenshot retiming or PRNG-causality claim.')
    assert all(r['whole_RGB_equal'] for r in comparisons if 5290<=r['frame']<=5950 or r['frame']==9001)""",
    '    assert not timings':
        "    assert len(timings)==11 and sum(r['source']['word']==0x4000 for r in timings)==9 and sum(r['source']['word']!=0x4000 for r in timings)==2",
    "    for v in actual['versions']:":"    for version_index,v in enumerate(actual['versions']):",
    "v['single_source_end386_actually_reached'] and v['fixture_exit_frame']==5256":
        "v['single_source_end482_actually_reached'] and v['fixture_exit_frame']==[5255,5257][version_index]",
    'start=8373,original_payload_exact_ROM=True':'start=[8375,8373][version_index],original_payload_exact_ROM=True',
    '[[2950,5050],[5290,9001]]':'[[3370,5050],[5290,9001],[6010,7210]]',
    'source_A0008_C200384_single_end386_actually_executed':'source_A0008_C200480_single_end482_actually_executed',
    'all_sampled_whole_RGB_from5290_through9001_equal=True':'whole_RGB_town5290_through5950_and_final9001_equal=True',
    'actual_timing_differences=timings,':
        "actual_timing_differences=timings,exact_timing_difference_counts=dict(total=11,speech=9,control_or_end=2),\n        fourteen_following_A_button_indicator_animation_differences_retained_unmasked=differences,",
    'source_event176_natural_eligibility_earned_state_earlier_location_full_route_or_hardware_not_proved':
        'source_event177_natural_eligibility_earned_state_earlier_location_full_route_or_hardware_not_proved',
    'session_id=18439':'session_id=78874','session_id=27916':'session_id=84991',
    'timing_differences=0,visual_review_pending=True':'timing_differences=11,following_indicator_RGB_differences=14,visual_review_pending=True',
})
root.mkdir(parents=True)
save(root/'source_derivation.json',dict(tool=tool,measured_fixture_exit_frames=[5255,5257],
    all115_sampled_upper_portrait_name_regions_equal=True,full_RGB_differences_after5290=14,
    full_RGB_differences_bounded_to_original_A_indicator=[224,360,240,376],
    nine_speech_two_control_or_end_timing_differences_preserved=True,
    PRNG_equality_not_assumed=True,no_new_boot_retiming_masking_or_editorial_credit=True,full_goal_complete=False))
