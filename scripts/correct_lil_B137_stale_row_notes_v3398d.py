"""Remove only two obsolete row-count waivers in theapproval successor."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import save
if __name__=='__main__':
    old=Path('scripts/approve_lil_B137_native_v3398b.py');new=Path('scripts/approve_lil_B137_native_v3398c.py');assert not new.exists();t=old.read_text(encoding='utf-8')
    a="    for row in doc['records']:\n";assert t.count(a)==1;t=t.replace(a,"    obsolete_notes=[]\n"+a)
    a="        row['review']['formatting']=True;";assert a in t;t=t.replace(a,"""        if row.get('qa_waivers') and not any(d.code=='line-break-count' for d in encoded.diagnostics):
            assert row['qa_waivers']==['line-break-count']
            reason=row['qa_waiver_reason'];obsolete_notes.append(dict(id=row['id'],old_waivers=row['qa_waivers'],old_reason=reason,reason='Final encoder reports no row-count difference.'))
            row['obsolete_row_count_note_removed']=obsolete_notes[-1]
            row['localization_note']=row['localization_note'].replace(reason,'').rstrip();row.pop('qa_waivers');row.pop('qa_waiver_reason')
"""+a)
    a='    ROOT.mkdir(parents=True);merged=';assert a in t;t=t.replace(a,"    assert {r['id'] for r in obsolete_notes}=={'DK4_MES_B137_R0181','DK4_MES_B137_R0252'}\n"+a)
    a='source_English_macro_control_invariants=invariants,';assert a in t;t=t.replace(a,a+'obsolete_row_count_notes_removed=obsolete_notes,')
    compile(t,str(new),'exec');new.write_text(t,encoding='utf-8');root=Path('work/analysis/lil_B137_stale_row_notes_v3398d');root.mkdir(parents=True);save(root/'provenance.json',dict(previous=str(old),previous_sha256=sha(old.read_bytes()),successor=str(new),successor_sha256=sha(new.read_bytes()),finding='Two inherited row-count waivers are obsolete after current encoding. Remove only those exact waivers;retain all real current QA gates and18actual row-count notes.',no_prose_or_encoded_bytes_changed=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
