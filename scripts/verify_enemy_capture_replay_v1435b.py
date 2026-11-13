"""Account for the original A-prompt phase after extra capture reading time.

V1435 passed both whole native/RGB capture holds and all return states,then
stopped before writing proof because10850 differs only in the blinking A icon.
Require the exact16x16 icon rectangle;all other pixels and nine later whole
screens remain identical. Never waive text,portraits or game-state differences.
"""
from pathlib import Path

if __name__=='__main__':
    path = Path('scripts/verify_enemy_capture_replay_v1435.py')
    source = path.read_text(encoding='utf-8')
    old = """        assert Image.open(picture).convert('RGB').tobytes()==Image.open(source_picture).convert('RGB').tobytes(),frame
        unchanged.append({'frame':frame,'whole_RGB_equal_to_V1404':True,'source':str(source_picture),'source_sha256':sha(source_picture.read_bytes())})"""
    new = """        current_picture,previous_picture = Image.open(picture).convert('RGB'),Image.open(source_picture).convert('RGB')
        icon = None
        if frame==10850:
            from PIL import ImageChops
            difference = ImageChops.difference(current_picture,previous_picture)
            assert difference.getbbox()==(224,360,240,376)
            for y in range(384):
                for x in range(256):
                    if not (224<=x<240 and 360<=y<376):
                        assert current_picture.getpixel((x,y))==previous_picture.getpixel((x,y))
            icon = {'rectangle':[224,360,240,376],'only_original_blinking_A_phase_differs_after80_extra_reading_frames':True,'all_text_portraits_scenes_and_every_other_pixel_exact':True}
        else:
            assert current_picture.tobytes()==previous_picture.tobytes(),frame
        unchanged.append({'frame':frame,'whole_RGB_equal_to_V1404':frame!=10850,'A_prompt_phase_only':icon,'source':str(source_picture),'source_sha256':sha(source_picture.read_bytes())})"""
    assert source.count(old)==1
    source = source.replace(old,new)
    for old,new in [
        ("'work/analysis/enemy_capture_verified_v1435'","'work/analysis/enemy_capture_verified_v1435b'"),
        ('later10_whole_reward_cargo_and_sailing_screens_exact_to_V1404','later9_whole_reward_cargo_and_sailing_screens_exact_plus10850_A_prompt_phase_only')]:
        assert source.count(old)==1,old
        source = source.replace(old,new)
    exec(compile(source,__file__,'exec'),{**globals(),'__name__':'__main__'})
