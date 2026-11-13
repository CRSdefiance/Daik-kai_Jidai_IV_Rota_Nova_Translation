"""Use the exact legacy source ID where the old schema has no block field."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import save
if __name__=='__main__':
    a=Path('scripts/reconcile_maria_B109_terms_v3504.py');b=Path('scripts/reconcile_maria_B109_terms_v3504b.py');assert not b.exists();t=a.read_text(encoding='utf-8');x="r.get('block')==109";assert t.count(x)==1;t=t.replace(x,"r.get('id')=='DK4_MES_B109_R0025'").replace('maria_B109_terms_v3504','maria_B109_terms_v3504b');compile(t,str(b),'exec');b.write_text(t,encoding='utf-8');root=Path('work/analysis/maria_B109_term_tools_v3504b');assert not root.exists();root.mkdir(parents=True)
    save(root/'provenance.json',dict(previous=str(a),previous_sha256=sha(a.read_bytes()),successor=str(b),successor_sha256=sha(b.read_bytes()),failure='The legacy91 record supplies block identity in its exact ID and has no block field. Bind DK4_MES_B109_R0025 explicitly. No terms receipt,ROM,ledger ortranslation was changed by the failed producer.',producer_sha256=sha(Path(__file__).read_bytes()),all_prior_artifacts_preserved=True,full_goal_complete=False))
