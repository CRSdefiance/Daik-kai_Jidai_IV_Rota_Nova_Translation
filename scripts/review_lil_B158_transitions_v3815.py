"""Record the completed visual review of19 panels, both source art pauses and normal town return."""
from pathlib import Path
from PIL import Image
from scripts.verify_village_wrap_v608 import read,save
from dk4tool.patch.grand_race_menu_release import sha
ROOT=Path('work/analysis/lil_B158_transition_review_v3815')
ACTUAL=Path('work/analysis/lil_B158_actual_v3814/actual_source_English_all19_panels_four_actors_four_FE_two_pauses_music_picture_and_return.json')
BASE=Path('E:/Rota Nova translations/Generated/work/emulation_v193')
if __name__=='__main__':
    assert not ROOT.exists();a=read(ACTUAL);assert not a['failures'] and a['complete_matching_panels']==19;views=[]
    notes={2950:'4650 tavern presentation and complete opening Lil panel; original portrait/name and complete text intact.',5170:'First two-byte source art pause: full dance scene and original A prompt; lower panel cleared.',5890:'Second two-byte source art pause: full close-up dance picture and A prompt; lower panel cleared.',6010:'Complete Lil admiration over the original dance picture, with correct portrait/name and all text.',7030:'4670 return to the tavern and Cristina portrait/name; the complete I love this song clause stays together.',7930:'Normal town return after the single declared end; upper and lower displays intact.'}
    for frame,note in notes.items():
        p=BASE/'lil_B158_display_v3812_reviewed_English'/f'frame_{frame:06d}_cold_boot.png';assert Image.open(p).size==(256,384);views.append(dict(path=str(p),sha256=sha(p.read_bytes()),frame=frame,review='Viewed full-screen capture. '+note))
    jp=BASE/'lil_B158_display_v3812_clean_Japanese/frame_007930_cold_boot.png';en=Path(views[-1]['path']);assert Image.open(jp).convert('RGB').tobytes()==Image.open(en).convert('RGB').tobytes();pairs=[]
    for v in a['versions']:
        selected=[c for c in v['selected_B22_command_pairs'] if c.get('original_source_block')==158 and c['word']!=0x4000];assert len(selected)==16 and sum(c['word']==0x2000 for c in selected)==2;assert {0x4650,0x4660,0x4670,0x4621,0}<=set(c['word'] for c in selected);pairs.append(dict(case=v['case'],fixture_exit_frame=v['fixture_exit_frame'],source_presentation_command_pairs=selected))
    assert [v['fixture_exit_frame'] for v in a['versions']]==[7895,7893];sheets=[]
    for s in a['review_sheets']:assert sha(Path(s['path']).read_bytes())==s['sha256'];sheets.append({**s,'review':'Viewed actual dialogue contact sheet: all complete text and four original native portraits/names, including Cristina Erneco. All four FE panels retain anonymous patron labels, shared exaggerated cheers or applause without invented static actors. No visual finding.'})
    assert len(sheets)==4;ROOT.mkdir(parents=True);save(ROOT/'full_screen_transition_and_all4_sheet_review.json',dict(actual_audit=str(ACTUAL),actual_audit_sha256=sha(ACTUAL.read_bytes()),viewed_full_screens=views,paired_town_source=dict(path=str(jp),sha256=sha(jp.read_bytes()),review='Viewed Japanese town return alongside English; all RGB pixels equal.'),full_town_return_RGB_identical=True,viewed_actual_sheets=sheets,source_presentation_pairs=pairs,all19_panels_and44_observed_commands_pass=True,source_4650_4660_4670_two_pauses_picture_music_FE_and_normal_return_visually_reviewed=True,phase_timings_recorded_not_asserted_identical=True,actual_natural_event158_eligibility_or_full_route_claim=False,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False));print('Viewed4 sheets and7 full screens;16 source control returns per image; both pauses and paired town RGB pass.')
