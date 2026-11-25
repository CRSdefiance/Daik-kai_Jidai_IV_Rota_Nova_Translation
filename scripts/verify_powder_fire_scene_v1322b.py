"""Check deferred original fire cleanup after dismissing the follow-up notice.

The predecessor expected cleanup while Fire extinguished was still on screen.
Both source and target retain bit0 then clear it after that original UI returns.
"""
import inspect
from pathlib import Path
from scripts import verify_powder_fire_scene_v1322 as previous

if __name__ == '__main__':
    source = inspect.getsource(previous.main)
    old = "assert all(not state['original_mobile_flag0E'] & 1 for state in states if state['frame'] >= 7350)"
    assert source.count(old) == 1
    source = source.replace(old,"assert all(not state['original_mobile_flag0E'] & 1 for state in states if state['frame'] >= 7490)")
    anchor = '    ROOT.mkdir(parents=True)'
    assert source.count(anchor) == 1
    source = source.replace(anchor,"""    assert all(state['original_mobile_flag0E'] & 1 for state in states if state['frame'] in [7350,7390])
    source_cleanup = []
    for frame in [7210,7310,7510]:
        old_raw = Path(f'E:/Rota Nova translations/Generated/work/emulation_v193/town_gunnery_v1300_1266/frame_{frame:06d}_arm9_ram.bin').read_bytes()
        old_cpu,old_get = get_machine(arm,old_raw)
        old_mobile = old_get(0x36C70,old_get(0xCB1A8)+4+132+12)
        source_cleanup.append({'frame':frame,'flag0E':bytes(old_cpu.mem_read(old_mobile+14,1))[0],
            'Hull_Crew':[old_get(0x5543C,old_mobile),old_get(0x55444,old_mobile)]})
    assert source_cleanup[0]['flag0E'] == source_cleanup[1]['flag0E'] == 5
    assert source_cleanup[-1]['flag0E'] == states[-1]['original_mobile_flag0E'] == 4
    assert source_cleanup[-1]['Hull_Crew'] == states[-1]['own_Hull_Crew'] == [56,112]
    ROOT.mkdir(parents=True)""")
    source = source.replace("'normal_A_dismissals_preserve_extinguished_response_clear_fire_and_return_to_original_sea_battle':True,",
        "'normal_A_dismissals_preserve_extinguished_response_clear_fire_and_return_to_original_sea_battle':True,'original_source_cleanup_phase_states':source_cleanup,'cleanup_is_deferred_until_original_extinguished_notice_is_dismissed_in_both_versions':True,'predecessor_1322_early_cleanup_assumption_corrected':True,")
    env = {**previous.__dict__,'__file__':__file__,'ROOT':Path('work/analysis/powder_fire_verified_v1322b')}
    exec(compile(source,__file__,'exec'),env)
    env['main']()
