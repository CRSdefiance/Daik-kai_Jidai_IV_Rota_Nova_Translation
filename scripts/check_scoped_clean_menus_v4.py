"""Use both complete menu arities on an explicit current captain and owning source bank."""
from scripts import check_scoped_clean_menus_v3 as previous
from scripts.source_locked_derivation_v5118 import checked_text
source=checked_text(previous.source, {
    '    assert args.captain==3 or set(counts)<={2}':'    assert set(counts)<={2,3}',
    '    source=checked_text(inspect.getsource(previous.main),{':
        "    source=checked_text(inspect.getsource(previous.main),{\n        \"'scripts.check_maria390_three_choice_v1'\":\"'scripts.check_editorial_three_choice_explicit_route_v1'\",",
    '"if count==2:sys.argv+=[\'--captain\',\'3\']":"if count==2:sys.argv+=[\'--captain\',str(CAPTAIN)]"':
        '"if count==2:sys.argv+=[\'--captain\',\'3\']":"sys.argv+=[\'--captain\',str(CAPTAIN)]"',
})
if __name__=='__main__':
    env={**previous.previous.previous.main.__globals__,'__file__':__file__}
    exec(compile(source,__file__+'::same-all-caption-native-controls-pixels-indices-andnegative-contract','exec'),env)
    env['main']()
