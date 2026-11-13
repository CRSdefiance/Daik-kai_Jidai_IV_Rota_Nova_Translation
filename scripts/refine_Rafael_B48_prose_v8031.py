"""Keep Rafael's repeated request puzzled andpolite after a fresh complete-exchange reading."""
from copy import deepcopy
from pathlib import Path
from scripts.verify_village_wrap_v608 import read,save
from dk4tool.patch.grand_race_menu_release import sha
OLD=Path('translations/rafael_B48_editorial_manuscript_v1.json')
OUT=Path('translations/rafael_B48_editorial_manuscript_v2.json')
ROOT=Path('work/analysis/Rafael_B48_prose_refinement_v8031')
if __name__=='__main__':
    assert not OUT.exists() and not ROOT.exists()
    old=read(OLD);doc=deepcopy(old)
    row=next(r for r in doc['records'] if r['source_record_index']==331)
    assert row['english']=="Interested? I don't even know what the Proof of Conquest is!"
    before=deepcopy(row)
    target="Interested? What exactly is the Proof of Conquest, anyway?"
    row.update(english=target,logical_English=target,
        localization_note="Preserve the rhetorical response to interest andthe genuine question aboutthe term. Avoid false disinterest andavoid making Rafael's polite confusion into an emphatic declaration;the direct question naturally shows that he still needs the explanation.",
        editorial_finding="The full exchange calls for a puzzled question,not the predecessor's false disinterest or an unnecessarily emphatic statement ofignorance. Retain the same source meaning andrevision classification.")
    for p in doc['all32_complete_English_exchange_reviews']:
        r=next(r for r in p['complete_English_exchange'] if r['id']==row['id'])
        assert r['english']==before['english'];r['english']=target
    assert doc['revisions']==42 and doc['retentions']==49
    doc.update(prior_manuscript=str(OLD),prior_manuscript_sha256=sha(OLD.read_bytes()),
        fresh_complete_exchange_readback_R331_question_tone_refined=True)
    doc['evidence']=dict(doc['evidence'])|{str(OLD):sha(OLD.read_bytes()),str(Path(__file__)):sha(Path(__file__).read_bytes())}
    save(OUT,doc);ROOT.mkdir(parents=True)
    save(ROOT/'R331_source_question_tone_refined_no_count_orcontrol_change.json',dict(
        manuscript=str(OUT),manuscript_sha256=sha(OUT.read_bytes()),prior_manuscript=str(OLD),prior_manuscript_sha256=sha(OLD.read_bytes()),
        id=row['id'],source_reference=row['source_reference'],current_reference=row['current_reference'],
        before=before,after=row,all32_path_reviews_updated=True,revisions=42,retentions=49,
        formatting_gates_still_false=True,no_ROM_registry_ledger_orcredit_change=True,new_credit=0,full_goal_complete=False))
    print('R331 readback refined to a puzzled direct question;all32 paths updated. 42revisions/49retentions unchanged;formatting pending.')
