"""Account only for observed zero-ink native ASCII-run flushes at exact source boundaries."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B207_name_phase_tools_v6354c')
HELPER='''def original_name_events(events,raw):
    cursor=0;at=0;x=0;ascii_run=0;visible=[];flushes=[]
    while at<len(raw):
        wide=raw[at]>=128;code=int.from_bytes(raw[at:at+2],'big') if wide else raw[at]
        if wide and ascii_run%2:
            flush=events[cursor];following=events[cursor+1]
            assert flush['kind']=='ascii' and flush['code']==32 and (flush['x'],flush['y'])==(x,0)==(following['x'],following['y']) and following['kind']=='cp932' and following['code']==code
            flushes.append(dict(source_byte_offset=at,event_index=cursor,kind='zero-ink-odd-ASCII-run-flush-before-source-CP932',x=x));cursor+=1
        event=events[cursor];assert (event['kind'],event['code'],event['x'],event['y'])==('cp932' if wide else 'ascii',code,x,0)
        visible.append(code);cursor+=1;at+=2 if wide else 1;x+=12 if wide else 6;ascii_run=0 if wide else ascii_run+1
    if ascii_run%2:
        event=events[cursor];assert (event['kind'],event['code'],event['x'],event['y'])==('ascii',32,x,0)
        flushes.append(dict(source_byte_offset=at,event_index=cursor,kind='zero-ink-odd-final-ASCII-run-flush',x=x));cursor+=1
    assert cursor==len(events)
    return visible,flushes

'''
if __name__=='__main__':
    assert not ROOT.exists();row=derive('scripts/prove_lil_B207_name_planes_v6354.py','scripts/prove_lil_B207_name_planes_v6354c.py',{
      "lil_B207_name_planes_v6354'":"lil_B207_name_planes_v6354c'",
      "if __name__=='__main__':":HELPER+"if __name__=='__main__':",
      "emitted=[e['code'] for e in events];original=codes(raw);assert emitted in [original,original+[32]]":"original=codes(raw);emitted,flushes=original_name_events(events,raw);assert emitted==original",
      'only_original_implicit_trailing_space_allowed=True':'only_exact_source_phase_flush_and_final_zero_ink_spaces_allowed=True,source_owned_native_flush_events=flushes'})
    ROOT.mkdir(parents=True);save(ROOT/'observed_source_phase_flush_correction.json',dict(tool=row,big_endian_source_CP932_codes_match_native8265=True,observed_ASCII_run_flush_space_at_x42_overlaps_only_empty_space_before_same_x_source_fullwidth_F=True,visible_source_characters_order_origins_bounds_pixels_and_actual_header_checks_unchanged=True,first_two_failed_event_list_models_preserved=True,no_ROM_font_name_metric_or_guard_changed=True,full_goal_complete=False))
