"""Record all four viewed sheets, original Sailor alias, C283 harbor and paired return."""
from pathlib import Path
from PIL import Image
from scripts.verify_village_wrap_v608 import read,save
from dk4tool.patch.grand_race_menu_release import sha
ROOT=Path('work/analysis/lil_B160_transition_review_v3900')
ACTUAL=Path('work/analysis/lil_B160_actual_v3899/actual_source_English_all22_panels_six_actors_missing_ship_C283_C200_and_return.json')
BASE=Path('E:/Rota Nova translations/Generated/work/emulation_v193')
if __name__=='__main__':
    assert not ROOT.exists();a=read(ACTUAL);assert not a['failures'] and a['complete_matching_panels']==22;views=[]
    notes={2950:'Original151 Sailor nameplate/portrait and complete opening alarm over initialized fixture city.',3850:'Complete urgent harbor summons before C283, with Sailor alias intact.',4090:'After source C283, original harbor upper scene and complete Lil confirmation;no claim of natural earned ship loss or that every ship in the art is absent.',8170:'Normal C200/first-end return to initialized town menu, both displays intact. Fixture town is Amsterdam;this is not a source B160 location claim.'}
    for frame,note in notes.items():
        p=BASE/'lil_B160_display_v3897_reviewed_English'/f'frame_{frame:06d}_cold_boot.png';assert Image.open(p).size==(256,384);views.append(dict(path=str(p),sha256=sha(p.read_bytes()),frame=frame,review='Viewed full-screen capture. '+note))
    jp=BASE/'lil_B160_display_v3897_clean_Japanese/frame_008170_cold_boot.png';en=Path(views[-1]['path']);assert Image.open(jp).convert('RGB').tobytes()==Image.open(en).convert('RGB').tobytes();pairs=[]
    for v in a['versions']:
        controls=[c for c in v['selected_B22_command_pairs'] if c.get('original_source_block')==160 and c['word']!=0x4000];assert len(controls)==6 and [c['word'] for c in controls]==[0x632C,0x632A,0xC283,0x632B,0xC200,0];pairs.append(dict(case=v['case'],fixture_exit_frame=v['fixture_exit_frame'],source_presentation_command_pairs=controls))
    assert [v['fixture_exit_frame'] for v in a['versions']]==[8137,8135];sheets=[]
    for s in a['review_sheets']:assert sha(Path(s['path']).read_bytes())==s['sha256'];sheets.append({**s,'review':'Viewed actual dialogue sheet. Complete native text, all six original actors and nameplates, Sailor151 alias, beauty-sleep/Mamma mia reversal, optional food joke, four-row eyewitness account and practical search plan are intact. No visual finding.'})
    assert len(sheets)==4;ROOT.mkdir(parents=True);save(ROOT/'full_screen_transition_and_all4_sheet_review.json',dict(actual_audit=str(ACTUAL),actual_audit_sha256=sha(ACTUAL.read_bytes()),viewed_full_screens=views,paired_town_source=dict(path=str(jp),sha256=sha(jp.read_bytes()),review='Viewed Japanese town return alongside English;all RGB pixels equal.'),full_town_return_RGB_identical=True,viewed_actual_sheets=sheets,source_presentation_pairs=pairs,all22_panels_and37_observed_commands_pass=True,actual_Sailor151_original_progressive_nameplate_and_portrait_observed=True,source_C283_C200_three_resources_and_normal_return_visually_reviewed=True,phase_timings_recorded_not_asserted_identical=True,actual_natural_event160_eligibility_or_earned_ship_loss_claim=False,fixture_town_not_source_event_location=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False));print('Viewed4 sheets and5 full screens;6 source control returns per image;Sailor151 original alias,C283 harbor,C200 andpaired town RGB pass.')
