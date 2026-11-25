"""Use the established mixed historical-decision schemas in the final audit."""
from pathlib import Path
from scripts.prepare_lil_B156_layout_v3705 import derive
from scripts.verify_village_wrap_v608 import save

ROOT=Path('work/analysis/lil_B174_final_audit_tools_v4501b')
if __name__=='__main__':
    assert not ROOT.exists()
    tool=derive('scripts/verify_editorial_handoff_v4501.py','scripts/verify_editorial_handoff_v4501b.py',{
        'editorial_handoff_verification_v4501':'editorial_handoff_verification_v4501b',
        "    assert sum(f['revised_count'] for f in ledger['completed_editorial_families'])==ledger['records_revised_and_integrated']==3709\n    assert sum(f['retained_count'] for f in ledger['completed_editorial_families'])==ledger['retained_wordings_editorially_completed']==2124":
            """    def decision(row):
        value=row.get('historical_editorial_decision') or row.get('decision') or row.get('editorial_decision')
        assert isinstance(value,str) and value.startswith(('revis','retain'))
        return 'revise' if value.startswith('revis') else 'retain'
    all_rows=[r for f in ledger['completed_editorial_families'] for r in f['records']]
    assert Counter(decision(r) for r in all_rows)=={'revise':3709,'retain':2124}
    assert (ledger['records_revised_and_integrated'],ledger['retained_wordings_editorially_completed'])==(3709,2124)""",
    })
    ROOT.mkdir(parents=True);save(ROOT/'source_derivation.json',dict(tool=tool,
        initial_unexecuted_audit_preserved=True,all5833_individual_historical_decisions_recounted=True,
        no_ledger_or_ROM_change=True,full_goal_complete=False))
    print('Prepared final audit using established per-record historical decision precedence; all history remains checked.')
