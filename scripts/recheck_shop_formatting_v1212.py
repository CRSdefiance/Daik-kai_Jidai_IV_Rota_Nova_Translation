"""Verify the photographed shop formatting remains correct in V1206."""
import inspect
from scripts import recheck_shop_formatting_v1168 as previous


def main():
    source=inspect.getsource(previous.main)
    replacements={
        'work/analysis/duel_release_v1165/photographed_shop_formatting.json':'work/analysis/duel_bark_release_v1205/photographed_shop_formatting.json',
        'out/all_routes_combined_v1166_candidate.nds':'out/all_routes_combined_v1206_candidate.nds',
        '19109464a37c8acfe7ccf802fed712cc0bd413600b304546668fb5475801ac26':'3ab79feca6d89fbb3cb4495b378f0a8d70cdeb15ecaf3085713940fc799dcd57',
        'new_V1166_shop_scene_activation_claimed':'new_V1206_shop_scene_activation_claimed','V1166:':'V1206:',
    }
    for old,new in replacements.items():assert source.count(old)==1;source=source.replace(old,new)
    from dk4tool.patch.duel_bark_editorial import current_entries
    env={**previous.__dict__,'__file__':__file__,'current_entries':current_entries}
    exec(compile(source,__file__,'exec'),env);env['main']()


if __name__=='__main__':main()
