"""Preserve all13 original direct escape pipelines under the special dispatch."""
import inspect
from pathlib import Path
from scripts import verify_duel_bark_escape_regression_v1203 as previous


def main():
    source = inspect.getsource(previous.main)
    replacements = {
        'work/analysis/duel_bark_native_v1201/native_payload_plan.json':
        'work/analysis/duel_special_native_v1218/native_payload_plan.json',
        'out/all_routes_combined_v1189_candidate.nds':
        'out/all_routes_combined_v1206_candidate.nds',
        'work/analysis/duel_bark_native_v1201/direct_escape_regression_plan.json':
        'work/analysis/duel_special_native_v1218/direct_escape_regression_plan_v1221.json',
        'E:/Rota Nova translations/Generated/work/emulation_v193/escape_direct_v1190_1189/frame_006902_arm9_ram.bin':
        'E:/Rota Nova translations/Generated/work/emulation_v193/duel_bark_v1207_1206/frame_007313_arm9_ram.bin',
    }
    for old, new in replacements.items():
        assert source.count(old) == 1
        source = source.replace(old, new)
    env = {**previous.__dict__, '__file__': __file__,
           'ROOT': Path('work/analysis/duel_special_escape_v1221')}
    exec(compile(source, __file__, 'exec'), env)
    env['main']()


if __name__ == '__main__':
    main()
