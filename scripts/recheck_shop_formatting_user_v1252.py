"""Fresh V1224 native check of the user's photographed shop formatting case."""
import inspect

from dk4tool.patch.duel_special_editorial import current_entries
from scripts import recheck_shop_formatting_v1168 as previous


def main():
    source = inspect.getsource(previous.main)
    replacements = {
        'work/analysis/duel_release_v1165/photographed_shop_formatting.json':
        'work/analysis/user_shop_formatting_v1252/photographed_shop_formatting.json',
        'out/all_routes_combined_v1166_candidate.nds':
        'out/all_routes_combined_v1224_candidate.nds',
        '19109464a37c8acfe7ccf802fed712cc0bd413600b304546668fb5475801ac26':
        'cdc860e53267dbef64ac9d40a1832b00fda6a4da6adbde2b61be830345d55dbd',
        'new_V1166_shop_scene_activation_claimed':
        'new_V1224_shop_scene_activation_claimed',
        'V1166:': 'V1224:',
    }
    for old, new in replacements.items():
        assert source.count(old) == 1
        source = source.replace(old, new)
    env = {**previous.__dict__, '__file__': __file__, 'current_entries': current_entries}
    exec(compile(source, __file__, 'exec'), env)
    env['main']()


if __name__ == '__main__':
    main()
