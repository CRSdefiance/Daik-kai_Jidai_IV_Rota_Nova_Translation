"""Keep complete menu guards with explicit captain/source-bank scope for two-choice menus."""
from scripts import check_scoped_clean_menus_v2 as previous
from scripts.source_locked_derivation_v5118 import checked_text

source = checked_text(previous.source, {
    "    args=ap.parse_args();doc=load(args.manuscript)":
        "    ap.add_argument('--captain',type=int,choices=range(4),required=True)\n"
        "    args=ap.parse_args();doc=load(args.manuscript)",
    "    assert doc['runtime']['captain']==3 and doc['file_path']=='/data/SC3.DK4'":
        "    assert doc['runtime']['captain']==args.captain and doc['file_path']==f'/data/SC{args.captain}.DK4'",
    "    source=checked_text(inspect.getsource(previous.main),{":
        """    assert args.captain==3 or set(counts)<={2}
    source=checked_text(inspect.getsource(previous.main),{
        \"doc['file_path']=='/data/SC3.DK4'\":\"doc['file_path']==FILE_PATH\",
        \"if count==2:sys.argv+=['--captain','3']\":\"if count==2:sys.argv+=['--captain',str(CAPTAIN)]\",""",
    "env={**vars(previous),'ROOT':args.root,'MANUSCRIPT':args.manuscript,'__file__':__file__}":
        "env={**vars(previous),'ROOT':args.root,'MANUSCRIPT':args.manuscript,'CAPTAIN':args.captain,'FILE_PATH':doc['file_path'],'__file__':__file__}",
})

if __name__ == '__main__':
    env = {**previous.previous.main.__globals__, '__file__': __file__}
    exec(compile(source,__file__+'::same-complete-menu-guards-explicit-captain-and-source-bank', 'exec'),env)
    env['main']()
