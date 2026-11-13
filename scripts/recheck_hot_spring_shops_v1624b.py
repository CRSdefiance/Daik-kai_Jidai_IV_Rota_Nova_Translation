"""Keep the two photographed shop-formatting repairs intact in V1622."""
import inspect
from dk4tool.patch.hot_spring_editorial import current_entries
from scripts import recheck_shop_formatting_v1168 as previous
from scripts.verify_village_wrap_v608 import read
if __name__=='__main__':
    release=read('work/analysis/hot_spring_release_v1621/registered_release_verification.json');source=inspect.getsource(previous.main)
    for old,new in [('work/analysis/duel_release_v1165/photographed_shop_formatting.json','work/analysis/hot_spring_release_v1621/photographed_shop_formatting.json'),
        ('out/all_routes_combined_v1166_candidate.nds','out/all_routes_combined_v1622_candidate.nds'),
        ('19109464a37c8acfe7ccf802fed712cc0bd413600b304546668fb5475801ac26',release['candidate_sha256']),
        ('new_V1166_shop_scene_activation_claimed','new_V1622_shop_scene_activation_claimed'),('V1166:','V1622:')]:
        assert source.count(old)==1;source=source.replace(old,new)
    env={**previous.__dict__,'__file__':__file__,'current_entries':current_entries};exec(compile(source,__file__,'exec'),env);env['main']()
