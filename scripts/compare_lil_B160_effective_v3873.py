"""Expose the complete B160 older English only after fresh clean-source glosses."""
from pathlib import Path
import re
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import save

if __name__=='__main__':
    PRODUCER=Path(__file__);DRAFT=Path('scripts/compare_lil_B159_effective_v3831.py');t=DRAFT.read_text(encoding='utf-8')
    changes={'lil_B159_comparison_v3831':'lil_B160_comparison_v3873','lil_B159_source_v3828':'lil_B160_source_v3870','all41_clean_current_complete_context':'all22_clean_current_complete_context','subset82_dispatches_and23_source_exact_control_leaves':'subset44_dispatches_and12_source_exact_control_leaves','lil_B159_clean_context_v3826/all41_complete_B159_exchange_and_fresh_glosses':'lil_B160_clean_context_v3869/all22_complete_B160_exchange_and_fresh_glosses','five_names_distinct_Samwell_consumers_and_original_entry_binding':'six_names_original_Sailor151_alias_and_entry_binding','lil_B159_controls_v3830/six_predicates_four_resource_sites_one_effect_two_ends_and23_source_leaves':'lil_B160_controls_v3872/five_predicates_C283_C200_three_resource_sites_and12_source_leaves','all41_clean_source_speeches_and_optional_Emilio_Fernando_branches_read':'all22_clean_source_speeches_and_optional_Angelo_Emilio_branches_read','all41':'all22','fresh41':'fresh22','len(rows)==41':'len(rows)==22','block=159':'block=160','B159':'B160','All41':'All22','and41':'and22'}
    for a in changes:assert a in t,a
    t=re.sub('|'.join(re.escape(a) for a in sorted(changes,key=len,reverse=True)),lambda m:changes[m.group()],t)
    start=t.index('The full clean source and22 fresh glosses');end=t.index("']",start)
    t=t[:start]+'The full clean source and22 fresh glosses were read first. Six static actors and22 progressive speeches retain FI1, five predicates, three resource values/sites,20 relative sites, C283, C200 andtwo endwords. Sailor151 follows the original progressive alias, distinct from the full catalogue Retainer. No FE, pause or A000 is invented. Isolated probes do not establish full command effects, natural event eligibility, source location or an earned ship-loss state. No decisions or credit here.'+t[end:]
    t=t.replace('producer_sha256=sha(Path(__file__).read_bytes())','producer_sha256=sha(PRODUCER.read_bytes()),draft_producer=str(DRAFT),draft_producer_sha256=sha(DRAFT.read_bytes())')
    compile(t,str(PRODUCER),'exec');exec(compile(t,str(PRODUCER),'exec'),dict(__name__='__main__',__file__=str(PRODUCER),PRODUCER=PRODUCER,DRAFT=DRAFT))
