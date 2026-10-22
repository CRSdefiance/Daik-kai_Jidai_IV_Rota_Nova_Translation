"""Keep the user's photographed shop fix exact in the registered fire candidate."""
import inspect
from dk4tool.patch.powder_fire_editorial import current_entries
from scripts import recheck_shop_formatting_v1168 as previous

if __name__ == '__main__':
    source = inspect.getsource(previous.main)
    changes = [
        ('work/analysis/duel_release_v1165/photographed_shop_formatting.json','work/analysis/powder_fire_release_v1315/photographed_shop_formatting.json'),
        ('out/all_routes_combined_v1166_candidate.nds','out/all_routes_combined_v1316_candidate.nds'),
        ('19109464a37c8acfe7ccf802fed712cc0bd413600b304546668fb5475801ac26','f27f98ab3c2d6fb56623e916c12da85355585a5d64622f9637f7c08ff9ddf8aa'),
        ('new_V1166_shop_scene_activation_claimed','new_V1316_shop_scene_activation_claimed'),
        ('V1166:','V1316:')]
    for old,new in changes:
        assert source.count(old) == 1
        source = source.replace(old,new)
    env = {**previous.__dict__,'__file__':__file__,'current_entries':current_entries}
    exec(compile(source,__file__,'exec'),env)
    env['main']()
