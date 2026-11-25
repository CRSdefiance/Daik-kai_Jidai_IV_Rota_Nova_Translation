"""Preserve2633 pre-write refusal;match the literal unconverted print count."""
from pathlib import Path
if __name__=='__main__':
 source=Path('scripts/reconcile_search_reports_retentions_v2633.py').read_text();old='changes["print(\'V2627:16retentions reconciled;fresh2114;';new='changes["print(\'V2627:16retentions reconciled;fresh2103;';assert source.count(old)==1;source=source.replace(old,new)
 source=source.replace("search_reports_completion_v2633'","search_reports_completion_v2633b'").replace("CHECKPOINT='V2633'","CHECKPOINT='V2633b'")
 source=source.replace("'contextual_retention_v2633'","'contextual_retention_v2633b'").replace("'next_remaining_historical_inventory_v2633'","'next_remaining_historical_inventory_v2633b'")
 source=source.replace('V2633 reconciles','V2633b reconciles').replace('## V2633:','## V2633b:').replace('# Current editorial handoff - V2633\\n','# Current editorial handoff - V2633b\\n').replace('V2633:11retentions','V2633b:11retentions')
 exec(compile(source,__file__,'exec'),{'__name__':'__main__','__file__':__file__})
