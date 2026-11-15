"""Keep complete menu guards while binding an explicit final formatting manuscript."""
import inspect
from scripts import check_scoped_clean_menus_v1 as previous
from scripts.source_locked_derivation_v5118 import checked_text

source=checked_text(inspect.getsource(previous.main),{
    "args=ap.parse_args();doc=load(args.root/'formatting_v1/formatting_input.json')":
        "ap.add_argument('--manuscript',type=Path,required=True)\n    args=ap.parse_args();doc=load(args.manuscript)",
    "        'assert len(groups)==8 and sum(map(len,groups.values()))==17':":
        "        \"docpath = ROOT/'formatting_v1/formatting_input.json'\":'docpath = MANUSCRIPT',\n        'assert len(groups)==8 and sum(map(len,groups.values()))==17':",
    "env={**vars(previous),'ROOT':args.root,'__file__':__file__}":
        "env={**vars(previous),'ROOT':args.root,'MANUSCRIPT':args.manuscript,'__file__':__file__}",
})
if __name__=='__main__':
    env={**previous.main.__globals__,'__file__':__file__}
    exec(compile(source,__file__+'::same-complete-menu-provider-alias-pixel-andnegative-guards-explicit-input','exec'),env)
    env['main']()
