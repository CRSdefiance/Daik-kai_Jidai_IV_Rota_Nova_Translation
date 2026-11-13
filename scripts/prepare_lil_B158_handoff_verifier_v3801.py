"""Derive an independent exact-reference, native-plane and coverage audit for B158."""
from pathlib import Path
import re
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import save
if __name__=='__main__':
    p=Path('scripts/verify_editorial_handoff_v3760.py');q=Path('scripts/verify_editorial_handoff_v3801.py');assert not q.exists();t=p.read_text(encoding='utf-8')
    changes={'B157':'B158','editorial_handoff_verification_v3760':'editorial_handoff_verification_v3801','lil_B157_checkpoint_v3759':'lil_B158_checkpoint_v3800','lil_B157_editorial_manuscript_v5':'lil_B158_editorial_manuscript_v4','v3759':'v3800','V3759':'V3800','unfinished_editorial_scope_v3742':'unfinished_editorial_scope_v3782',
        "{'revise':31,'retain-wording':44}":"{'revise':14,'retain-wording':5}",
        "sum(r['kind']=='system-FE' for r in rows)==2":"sum(r['kind']=='system-FE' for r in rows)==4",
        "sum(bytes.fromhex(r['source_hex']).count(b'FI') for r in rows)==2":"sum(bytes.fromhex(r['source_hex']).count(b'FI') for r in rows)==1",
        '{2,9,14,19,20,105,142,254}':'{2,7,9,14,254}',
        '(5329,5254,75)':'(5348,5329,19)',
        '5329':'5348','5254':'5329','5332':'5351','3476':'3495','3388':'3419','1866':'1910',
        '(3730,3655)':'(3749,3730)',
        "['incomplete_route_source_prose_groups','incomplete_route_source_prose_count','next_focus']":"['incomplete_route_source_prose_groups','incomplete_route_source_prose_count','next_focus','broader_coverage_units']",
        'next_B157_B160_source_scope_v3759':'next_B158_B160_source_scope_v3800','other82_B158_B160_not_yet_fully_read_or_gloss_approved':'other63_B159_B160_not_yet_fully_read_or_gloss_approved','other82_B158_B160_unread_or_gloss_pending':'other63_B159_B160_unread_or_gloss_pending','all75_exact_source_current_effective_gloss_decision_macro_and_complete_native_references_verified':'all19_exact_source_current_effective_gloss_decision_macro_and_complete_native_references_verified',
        'manifest_batches=531':'manifest_batches=532','integrated=5254':'integrated=5329','pending=75':'pending=19',
        'V3759 independently verified:5329 reread/5254 integrated/75 pending;5332 source-prose;V3738/531 unchanged.':'V3800 independently verified:5348 reread/5329 integrated/19 pending;5351 source/prose;V3778/532 unchanged.'}
    for a in changes:assert a in t,a
    t=re.sub('|'.join(re.escape(a) for a in sorted(changes,key=len,reverse=True)),lambda m:changes[m.group()],t)
    t=re.sub(r'(?<![\w])(?:75|600|24|10|25|531)(?![\w])',lambda m:{'75':'19','600':'152','24':'18','10':'3','25':'5','531':'532'}[m.group()],t)
    # Case-sensitive generic substitutions keep historical B157 inventories intact; fix the new scope lookup explicitly.
    t=t.replace('next_B158_B160_source_scope_v3800','next_B158_B160_source_scope_v3800')
    a="    ROOT.mkdir(parents=True);save(ROOT/'verified_handoff.json'";assert t.count(a)==1;extra="    assert fresh['integrated_record_keys']==old['integrated_record_keys'] and len(fresh['integrated_record_keys'])==5329\n    assert [x for x in inv['broader_coverage_units'] if x['id']!='all-route-scenes']==[x for x in oldinv['broader_coverage_units'] if x['id']!='all-route-scenes']\n    assert sum(ledger['source_prose_reviewed_counts_by_file'].values())==5351 and ledger['completed_editorial_record_counts_by_file']['/data/SC2.DK4']==3476\n";t=t.replace(a,extra+a)
    compile(t,str(q),'exec');q.write_text(t,encoding='utf-8',newline='\n');root=Path('work/analysis/lil_B158_handoff_verifier_tools_v3801');assert not root.exists();root.mkdir(parents=True);save(root/'source_derivation.json',dict(source=str(p),source_sha256=sha(p.read_bytes()),successor=str(q),successor_sha256=sha(q.read_bytes()),no_ledger_or_docs_mutation=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
