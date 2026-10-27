"""Keep the photographed shop676/677 fix intact under the new byte decoder."""
import inspect
from dk4tool.patch.battle_aftermath_editorial import current_entries
from scripts import recheck_shop_formatting_v1168 as previous


if __name__ == '__main__':
    source = inspect.getsource(previous.main)
    replacements = {
        'work/analysis/duel_release_v1165/photographed_shop_formatting.json':
        'work/analysis/battle_aftermath_release_v1265/photographed_shop_formatting.json',
        'out/all_routes_combined_v1166_candidate.nds':'out/all_routes_combined_v1266_candidate.nds',
        '19109464a37c8acfe7ccf802fed712cc0bd413600b304546668fb5475801ac26':
        'cac04b66961829b42b3d54bd69d901926434ff1ed24d1be0b2f96665020e8da5',
        'new_V1166_shop_scene_activation_claimed':'new_V1266_shop_scene_activation_claimed',
        'V1166:':'V1266:',
    }
    for old,new in replacements.items():
        assert source.count(old) == 1
        source = source.replace(old,new)
    env = {**previous.__dict__,'__file__':__file__,'current_entries':current_entries}
    exec(compile(source,__file__,'exec'),env)
    env['main']()
