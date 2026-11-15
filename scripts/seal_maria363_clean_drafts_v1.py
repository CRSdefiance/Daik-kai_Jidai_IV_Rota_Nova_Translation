"""Seal all363 clean meanings and independent drafts before current story extraction."""
from collections import Counter
from copy import deepcopy
from pathlib import Path
from scripts.audit_story_glyph_consistency import load, save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest

ROOT=Path('work/Maria_B216_B252_clean_20261110')


def main():
    mp,dp,sp=[ROOT/n for n in ['all363_clean_meanings_v1.json','all363_independent_drafts_v1.json','clean_draft_seal_v1.json']]
    assert not any(p.exists() for p in [mp,dp,sp])
    pp=ROOT/'clean_source_packet.json';packet=load(pp)
    selected=[r for g in packet['groups'] for r in g['records']]
    meanings=[];drafts=[];evidence={str(p):digest(p) for p in [pp,Path(__file__)]}
    parts=['B216_B226_v2','B227_B243_v1','B244_B251_v1','B252_v1']
    for part in parts:
        a,b=[ROOT/f'clean_part_{part}/{n}.json' for n in ['clean_meanings','independent_drafts']]
        m,d=map(load,[a,b])
        assert m['current_English_not_consulted'] and d['current_English_not_consulted']
        assert d['source_meanings_sha256']==digest(a) and a.stat().st_mtime_ns<=b.stat().st_mtime_ns
        assert len(m['records'])==len(d['records'])
        for x,y in zip(m['records'],d['records'],strict=True):
            assert all(x[k]==y[k] for k in ['id','source_hex','source_reference','source_Japanese','source_meaning','whole_exchange_context'])
            assert y['english']==y['independent_English_draft'] and not any(y['review'].values())
        meanings.extend(deepcopy(m['records']));drafts.extend(deepcopy(d['records']))
        for p in [a,b,Path(d['authored'])]:evidence[str(p)]=digest(p)
    assert len(selected)==len(meanings)==len(drafts)==len({r['id'] for r in drafts})==363
    for x,y,z in zip(selected,meanings,drafts,strict=True):
        assert all(x[k]==y[k]==z[k] for k in ['id','source_hex','source_reference','source_Japanese'])
        assert y['source_meaning_reviewed_from_complete_clean_exchange'] and z['current_English_not_consulted']
        assert z['english'].isascii() and '\n' not in z['english'] and z['logical_paragraph_without_authored_wraps']
        assert all(z['english'].count(t)==z['source_Japanese'].count(t) for t in ['FI','FA','FO','FU'])
    assert Counter(r['kind'] for r in drafts)=={'ordinary-speech':266,'physical-style-alternative':85,'typed-menu-caption':12}
    amendment=ROOT/'authored_B216_B226_v2.json';before=ROOT/'authored_B216_B226_v1.json'
    a,b=map(load,[before,amendment]);changes=[]
    for x,y in zip(a['records'],b['records'],strict=True):
        assert x[0]==y[0]
        if x!=y:changes.append(dict(id=x[0],before=x[1:],after=y[1:]))
    assert {r['id'] for r in changes}=={'DK4_MES_B221_R0104','DK4_MES_B226_R0042'}
    evidence[str(before)]=digest(before)
    common=dict(source_packet=str(pp),source_packet_sha256=digest(pp),blocks=packet['selected_blocks'],complete_exchanges=37,
        source_objects=363,current_English_not_consulted=True,new_credit=0,full_goal_complete=False,evidence=evidence,
        clean_only_amendments=changes,all_original_part_outputs_preserved=True,
        unresolved_native_source_controls=[dict(id='DK4_MES_B252_R0095',selector=215,
            source_hex='d78aeb82c882a282c18149',native_identity_andconsumer_approval_pending=True)])
    save(mp,dict(common,records=meanings,all363_clean_meanings_saved=True,
        source_gloss_precedes_independent_draft_in_each_authored_entry=True,each_part_meanings_file_written_before_its_draft_file=True))
    save(dp,dict(common,records=drafts,all363_independent_drafts_saved=True,source_meanings=str(mp),source_meanings_sha256=digest(mp),
        translation_policy='natural-dialogue-v2',target_locale='en-US',
        current_English_comparison_names_terms_consumers_andall_five_gates_pending=True))
    save(sp,dict(source_objects=363,complete_exchanges=37,source_meanings=str(mp),source_meanings_sha256=digest(mp),
        independent_drafts=str(dp),independent_drafts_sha256=digest(dp),
        source_glosses_andindependent_drafts_all_saved_before_first_current_story_English_exposure=True,
        all_five_review_gates_pending=True,no_current_story_English_read=True,new_credit=0,full_goal_complete=False,
        evidence={**evidence,str(mp):digest(mp),str(dp):digest(dp)}))
    print('Sealed363 clean meanings and independent drafts;37 groups; all gates pending; zero credit.')


if __name__=='__main__':main()
