"""Resolve concrete visual phrase findings and the observed FE input-consumption failure."""
from copy import deepcopy
from hashlib import sha256
from scripts.meaning_maria328_clean_v1 import ROOT
from scripts.audit_story_glyph_consistency import load, save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest

def main():
    before=ROOT/'formatting_FE_v1/preferences_continuity_v2.json'
    out=ROOT/'formatting_FE_v1/preferences_visual_v3.json'
    assert not out.exists()
    pref=deepcopy(load(before))
    doc=ROOT/'formatting_FE_v1/physical_manuscript.json'
    rows={r['id']:r for r in load(doc)['records']}
    additions={
        'DK4_MES_B74_R0070':dict(required_pairs=[['old',"man's"]],reason="Keep old man's together in Julio's self-deprecating farewell; no wording change."),
        'DK4_MES_B75_R0012':dict(required_pairs=[['want','to'],['to','see'],['see','one']],reason='Keep the complete short Want to see one? question on one row.'),
        'DK4_MES_B76_R0012':dict(required_pairs=[['jaguar',"god's"],["god's",'vest']],reason="Keep the approved Jaguar God's Vest item name together; the complete sentence cannot fit one native row."),
        'DK4_MES_B76_R0038':dict(page_clause="Of course, if I happen to hear anything, I'll tell you.",reason='Trial the complete closing offer at the second-panel start, avoiding an A wait inside its conditional clause.'),
        'DK4_MES_B87_R0139_FE_PAGE_1':dict(FE_planning_cells=36,reason='The fresh native painter stops before the complete FE riddle input. Apply the existing source-bound 36-cell guard reserve, preserving the physical228px view and every word; repeat all native assertions.'),
        'DK4_MES_B87_R0139_FE_PAGE_2':dict(FE_planning_cells=36,reason='Same riddle continuation consumer has a37-visible-cell row; scope the existing guard reserve to this exact companion and verify it afresh.'),
    }
    for ident, fields in additions.items():
        row=rows[ident]
        rule=pref['records'].setdefault(ident,{})
        if 'reason' in rule: fields['reason']=rule['reason']+' '+fields['reason']
        rule.update(fields,bindings={k:sha256(row[k].encode()).hexdigest() for k in ['source_hex','current_hex','english']})
    pref.update(previous_preferences=str(before),previous_preferences_sha256=digest(before),
        concrete_native_failure_log=str(ROOT/'native_resume_v1.log'),
        concrete_native_failure_log_sha256=digest(ROOT/'native_resume_v1.log'),
        all_native_assertions_unchanged=True,new_credit=0)
    save(out,pref)
    print('Saved six source-bound visual/native refinements; no prose, native code or physical widths changed.')

if __name__=='__main__':main()
