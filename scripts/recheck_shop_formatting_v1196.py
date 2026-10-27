"""Recheck the user's photographed shop formatting in the exact V1189 build."""
import inspect
from scripts import recheck_shop_formatting_v1168 as previous


def main():
    source=inspect.getsource(previous.main)
    replacements={
        'work/analysis/duel_release_v1165/photographed_shop_formatting.json':'work/analysis/escape_direct_release_v1188/photographed_shop_formatting.json',
        'out/all_routes_combined_v1166_candidate.nds':'out/all_routes_combined_v1189_candidate.nds',
        '19109464a37c8acfe7ccf802fed712cc0bd413600b304546668fb5475801ac26':'a7b7799052a83703dc5a2bf84e946e43b31d5e1f795f9f3371417412f60c7df4',
        'new_V1166_shop_scene_activation_claimed':'new_V1189_shop_scene_activation_claimed',
        'V1166:':'V1189:',
    }
    for old,new in replacements.items():
        assert source.count(old)==1;source=source.replace(old,new)
    from dk4tool.patch.escape_direct_entries import current_entries
    env={**previous.__dict__,'__file__':__file__,'current_entries':current_entries}
    exec(compile(source,__file__,'exec'),env);env['main']()


if __name__=='__main__':main()
