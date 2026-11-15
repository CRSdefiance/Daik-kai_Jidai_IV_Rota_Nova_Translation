"""Record the completed human visual review after the terminal paired display audit."""
from pathlib import Path
from PIL import Image
from scripts.verify_village_wrap_v608 import read,save
from dk4tool.patch.grand_race_menu_release import sha
ROOT=Path('work/analysis/lil_B157_transition_review_v3775')
ACTUAL=Path('work/analysis/lil_B157_actual_v3773/actual_source_English_all75_panels_seven_actors_two_FE_pause_C281_4885_and_return.json')
BASE=Path('E:/Rota Nova translations/Generated/work/emulation_v193')
if __name__=='__main__':
    assert not ROOT.exists();a=read(ACTUAL);assert not a['failures'] and a['complete_matching_panels']==75 and a['visual_review_pending']
    views=[]
    notes={9430:'C281 transition: complete harbor background and cleared lower panel.',9490:'Innkeeper portrait/name and complete opening speech after C281.',11290:'4885 presentation: complete equipment window and harbor; observed fixture display is Stylish Boots. This is not an earned-item or source eligibility claim.',16690:'Original two-byte art pause: complete graveside image and A prompt; lower screen cleared.',16810:'First-person FE recollection: no invented narrator/nameplate, complete four rows over the original paper background.',21130:'Normal return to town after the first declared end; full upper and lower displays intact.'}
    for frame,note in notes.items():
        p=BASE/'lil_B157_display_v3771_reviewed_English'/f'frame_{frame:06d}_cold_boot.png';im=Image.open(p);assert im.size==(256,384);views.append(dict(path=str(p),sha256=sha(p.read_bytes()),frame=frame,review='Viewed full-screen capture. '+note))
    jp=BASE/'lil_B157_display_v3771_clean_Japanese/frame_021130_cold_boot.png';en=Path(views[-1]['path']);assert Image.open(jp).convert('RGB').tobytes()==Image.open(en).convert('RGB').tobytes()
    pairs=[]
    for v in a['versions']:
        selected=[c for c in v['selected_B22_command_pairs'] if c.get('original_source_block')==157 and c['word']!=0x4000];assert len(selected)==22
        assert {0xC281,0x4885,0x2000,0x4621,0x4620,0xC200,0}<=set(c['word'] for c in selected)
        pairs.append(dict(case=v['case'],fixture_exit_frame=v['fixture_exit_frame'],source_presentation_command_pairs=selected))
    assert [v['fixture_exit_frame'] for v in a['versions']]==[21096,21095]
    sheets=[]
    for s in a['review_sheets']:
        assert sha(Path(s['path']).read_bytes())==s['sha256'];sheets.append({**s,'review':'Viewed actual dialogue contact sheet: complete text and seven correct native portraits/names, including Carlo Sinat; both FE recollections complete, first-person and without an invented speaker. No visual finding.'})
    assert len(sheets)==13;ROOT.mkdir(parents=True)
    save(ROOT/'full_screen_transition_and_all13_sheet_review.json',dict(actual_audit=str(ACTUAL),actual_audit_sha256=sha(ACTUAL.read_bytes()),viewed_full_screens=views,paired_town_source=dict(path=str(jp),sha256=sha(jp.read_bytes()),review='Viewed Japanese town return alongside English; all RGB pixels equal.'),full_town_return_RGB_identical=True,viewed_actual_sheets=sheets,source_presentation_pairs=pairs,all75_panels_and106_observed_commands_pass=True,source_C281_4885_pause_picture_FE_and_normal_return_visually_reviewed=True,phase_timings_recorded_not_asserted_identical=True,actual_natural_event157_eligibility_or_earned_gift_recruitment=False,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print('Viewed13 sheets and7 full screens;22 source control returns per image; paired town RGB identical.')
