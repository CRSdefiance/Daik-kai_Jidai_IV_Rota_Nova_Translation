"""Bind new V820 ceremony replay to verified complete glyphs and unchanged state."""

import struct
from pathlib import Path

from PIL import Image,ImageChops

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.levelup_stat_format import current_entries
from dk4tool.rom.nds import NdsImage
from scripts.native_ceremony_rand_trace_v822 import ROOT
from scripts.verify_ceremony_random_cause_v823 import load,ram,fingerprint
from scripts.verify_levelup_gameplay_v819 import glyphs
from scripts.verify_village_wrap_v608 import read,save


def main():
    old,of,orr=load('ceremony_v809_Athens_climb_frame_probe')
    new,nf,nrr=load('ceremony_v820_uncontrolled_Athens_v823')
    assert old['scripted_input_schedule']==new['scripted_input_schedule'] and old['core_options']==new['core_options']
    assert not any(r.get('synthetic_discarded_yield_RAND_control') for r in new['synthetic_condition_fixtures'])
    before=NdsImage.open(old['ROM']);after=NdsImage.open(new['ROM'])
    a,b=[r.read_file('/__arm9__.bin') for r in (before,after)]
    assert sha(b)=='c27c2b01ea689ef6cc15bffabb30138aaadecb1d8a14e8a2d85a0f4c09d643eb'
    assert before.read_file('/COMMON/MESFILE.DK4')==after.read_file('/COMMON/MESFILE.DK4')
    assert before.read_file('/GRP/KANJI.FNT')==after.read_file('/GRP/KANJI.FNT')
    entries=current_entries(after.read_file('/COMMON/MESFILE.DK4'),b)
    wrapped=struct.unpack_from('<I',b,0x54450)[0]
    states=[];controls=[];stat_holds=[]
    for f in sorted(nrr):
        x,y=ram(orr[f]),ram(nrr[f])
        assert fingerprint(a,x)==fingerprint(b,y),(f,'uncontrolled V820 world differs from V809')
        assert x[0x168EB8:0x168EBC]==y[0x168EB8:0x168EBC]
        states.append(dict(frame=f,all_original_persistent_state_models_tasks_funds_time_and_PRNG_equal_V809=True))
        oldpic,newpic=[Image.open(d[f]['path']).convert('RGB') for d in (of,nf)]
        diff=ImageChops.difference(oldpic,newpic)
        if f in (9000,9800):
            at=wrapped-0x02000000
            encoded=y[at:at+256].split(b'\0')[0]
            original=x[at:at+256].split(b'\0')[0]
            assert b' '.join(encoded.split())==b' '.join(original.split())
            lines=[s.strip().decode('cp932') for s in encoded.split(b'\n')]
            glyphs(b,after.read_file('/GRP/KANJI.FNT'),newpic,encoded,lines)
            diff.paste((0,0,0),(16,294,244,366));assert diff.getbbox() is None
            stat_holds.append(dict(frame=f,lines=lines,capture=nf[f],
                complete_native_and_independent_font_actual_pixel_plane_exact=True,
                no_words_numbers_or_leading_trailing_letters_changed=True,
                outside_text_body_all_pixels_equal=True))
        else:
            assert diff.getbbox() is None,(f,diff.getbbox())
            controls.append(dict(frame=f,entire_two_screen_frame_equal_V809=True))
    prior_path=Path('work/analysis/ceremony_Athens_v816/Athens_site_glyph_stage_only_v817.json')
    prior=read(prior_path);transferred=[]
    assert prior['all_complete_native_and_independent_font_planes_and_captured_buffers_pass']
    assert len(prior['complete_scene_holds'])==26
    for hold in prior['complete_scene_holds']:
        f=hold['frame'];source=hold['capture'];target=nf[f]
        assert sha(Path(source['path']).read_bytes())==source['PNG_sha256']
        assert ImageChops.difference(Image.open(source['path']).convert('RGB'),Image.open(target['path']).convert('RGB')).getbbox() is None
        assert hold['complete_native_and_independent_font_exact']
        transferred.append(dict(frame=f,message_id=hold['message_id'],lines=hold['lines'],capture=target,
            whole_frame_exact_to_previously_verified_full_glyph_and_blank_plane=True,
            COMMON_template_font_and_native_formatter_unchanged=True))
    proof=dict(candidate=new['ROM'],candidate_sha256=new['ROM_sha256'],complete_state_and_PRNG_pairs=states,
        whole_screen_controls=controls,two_additional_complete_stat_holds=stat_holds,
        complete_ceremony_holds=transferred,full_goal_complete=False,new_editorial_completion_credit=0,
        ordinary_V820_random_stream_and_world_results_match_V809_at_every46_observed_checkpoint=True,
        no_post_acknowledgment_generator_trace_or_entropy_control_in_this_run=True,
        isolated_calendar_access_inputs_only_not_earned_campaign_access=True,
        prior_native_glyph_proof=str(prior_path),prior_native_glyph_proof_sha256=sha(prior_path.read_bytes()),
        other_protagonist_reactions_and_final_family_review_remain=True,
        producer_sha256=sha(Path(__file__).read_bytes()))
    assert len(states)==46 and len(controls)==44 and len(stat_holds)==2 and len(transferred)==26
    save(ROOT/'V820_uncontrolled_ceremony_display_and_state_v824.json',proof)
    print('V820 ordinary replay:46 unchanged state/PRNG pairs,44 complete-screen controls,26 complete ceremony holds and2 repaired stat holds pass.',flush=True)


if __name__=='__main__':main()
