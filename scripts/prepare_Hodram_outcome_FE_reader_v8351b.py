"""Preserve the executed FE reader; correct CPU register indexing and JSON color representation."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save

if __name__=='__main__':
    root=Path('work/analysis/Hodram_outcome_FE_reader_tools_v8351b');assert not root.exists()
    changes={
        "row['context']==registers[5] and row['R1']==registers[6]":"row['context']==registers[4] and row['R1']==registers[5]",
        'palette15_RGB=colors[15],palette14_RGB=colors[14]':'palette15_RGB=list(colors[15]),palette14_RGB=list(colors[14])',
    }
    a=derive('dk4tool/patch/hodram_outcomes_FE_evidence_v1.py','dk4tool/patch/hodram_outcomes_FE_evidence_v2.py',changes)
    b=derive('scripts/validate_Hodram_outcome_FE_evidence_v8351.py','scripts/validate_Hodram_outcome_FE_evidence_v8351b.py',{
        'hodram_outcomes_FE_evidence_v1':'hodram_outcomes_FE_evidence_v2',
        'Hodram_outcome_FE_evidence_v8351':'Hodram_outcome_FE_evidence_v8351b',
    })
    root.mkdir(parents=True);save(root/'CPU_R0_offset4_R1_offset5_and_JSON_color_lists_source_locked.json',dict(derivations=[a,b],original_failed_reader_preserved=True,ROM_text_andcaptures_unchanged=True,new_credit=0,full_goal_complete=False))
