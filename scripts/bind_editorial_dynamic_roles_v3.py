"""Keep complete style/ordinary role guards when207 is only a captain control."""
import inspect
from scripts import bind_editorial_dynamic_roles_v2 as previous
from scripts.source_locked_derivation_v5118 import checked_text

source=checked_text(inspect.getsource(previous.main),{
    'assert selectors and 207 in selectors':'assert selectors and all(207<=v<224 for v in selectors)',
    "ctx.execute(env['dynamic'],selectors)":"ctx.execute(env['dynamic'],sorted(set([207,*selectors])))",
    'source_records=records,native_roles=result,source_owned_adapter=adapter,':
        'source_records=records,source_selectors=selectors,captain_control_selector=207,native_roles=result,source_owned_adapter=adapter,',
})
env={**vars(previous),'__file__':__file__}
exec(compile(source,__file__+'::same-native-roles-with-explicit-captain-control','exec'),env)

if __name__=='__main__':env['main']()
