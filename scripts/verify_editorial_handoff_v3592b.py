"""Make the inventory-count assertion unconditional;prior-audit state is already exact-bound."""
from pathlib import Path
if __name__=='__main__':
    a=Path('scripts/verify_editorial_handoff_v3592.py');t=a.read_text(encoding='utf-8');old="assert inventory['incomplete_route_source_prose_count']==38 and inventory['older_record_reaudit_after_full_editorial_goal'] if 'older_record_reaudit_after_full_editorial_goal' in inventory else True";assert old in t;t=t.replace(old,"assert inventory['incomplete_route_source_prose_count']==38").replace('editorial_handoff_verification_v3592','editorial_handoff_verification_v3592b');exec(compile(t,str(Path(__file__))+'::unconditional_inventory_count','exec'),dict(__name__='__main__',__file__=__file__))
