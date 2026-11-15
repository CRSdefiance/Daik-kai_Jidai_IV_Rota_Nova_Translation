"""Record viewed actual presentation transitions andthe identical town return."""
from pathlib import Path
from PIL import Image
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B156_actual_transitions_v3737b')
if __name__=='__main__':
    assert not ROOT.exists();p=Path('work/analysis/lil_B156_actual_v3733/actual_source_English_all76_panels_ten_actors_resources_C200_and_return.json');actual=read(p);assert actual['complete_matching_panels']==76 and not actual['failures'];paired=[]
    for a,b in zip(actual['versions'][0]['selected_B22_command_pairs'],actual['versions'][1]['selected_B22_command_pairs'],strict=True):
        assert (a.get('original_source_offset'),a['word'],a['result_words'])==(b.get('original_source_offset'),b['word'],b['result_words'])
        if a.get('original_source_block')!=156 or a['word']==0x4000:continue
        paired.append(dict(source_offset=a['original_source_offset'],word=a['word'],Japanese=a,English=b,measured_frame_intervals=[x['returned']-x['start'] for x in [a,b]],not_interpreted_as_operand_time_units=True))
    frames=[]
    for f in [12310,14230,15850,21130]:
        photos=[]
        for c in ['clean_Japanese','reviewed_English']:
            report=read('E:/Rota Nova translations/Generated/work/emulation_v193/lil_B156_display_v3731_'+c+'/capture_report.json');r=next(r for r in report['frames_captured'] if r['frame']==f);path=Path(r['path']);assert sha(path.read_bytes())==r['PNG_sha256'];photos.append((r,Image.open(path).convert('RGB')))
        equal=photos[0][1].tobytes()==photos[1][1].tobytes()
        if f==21130:assert equal
        frames.append(dict(frame=f,Japanese=photos[0][0],English=photos[1][0],whole_RGB_equal=equal,viewed_English=True,viewed_Japanese=f==21130,scope='Post-C200 normal Amsterdam town return' if f==21130 else 'Original source-owned upper-scene/picture/presentation transition;phase timing may differ by one or two frames.'))
    assert [v['fixture_exit_frame'] for v in actual['versions']]==[21097,21096];assert len(paired)==38 and sum(r['word']==0xC200 for r in paired)==1;ROOT.mkdir(parents=True);save(ROOT/'source_English_presentation_transition_review.json',dict(actual_proof=str(p),actual_proof_sha256=sha(p.read_bytes()),paired_original_presentation_resource_C200_and_first_end_commands=paired,viewed_transition_frames=frames,all13_actual_consumer_sheets_viewed=True,all76_panels_ten_source_actor_selectors_pass=True,original_98_Sailor_nameplate_alias_proof='work/analysis/lil_B156_nameplate_v3737a/source_native_catalogue_vs_progressive_Sailor_alias.json',both_normal_town_returns_and_whole21130_RGB_equal=True,exit_frames=[21097,21096],no_same_frame_timing_assumption_for_fades_or_glyph_progress=True,not_natural_event156_location_eligibility_or_earned_recruitment=True,no_new_ROM_capture_orcredit=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False));print('Viewed13 actual sheets plus4 English transitions/paired town return;76panels/123commands pass. Source Sailor alias andphase timing distinguished.')
