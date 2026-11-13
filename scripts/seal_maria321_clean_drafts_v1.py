"""Seal all321 exact clean meanings/drafts before any existing story-English comparison."""
from copy import deepcopy
from pathlib import Path
from scripts.audit_story_glyph_consistency import load, save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest

ROOT=Path('work/Maria_B196_B215_clean_20261110')


def main():
    meaning_path=ROOT/'all321_clean_meanings_v1.json'
    draft_path=ROOT/'all321_independent_drafts_v1.json'
    seal_path=ROOT/'clean_draft_seal_v1.json'
    assert not any(p.exists() for p in [meaning_path,draft_path,seal_path])
    packet_path=ROOT/'clean_source_packet.json'
    packet=load(packet_path)
    selected=[r for g in packet['groups'] for r in g['records']]
    meanings,drafts,evidence=[],[],{str(packet_path):digest(packet_path),str(Path(__file__)):digest(Path(__file__))}
    for part in ['B196_B201','B202_B209','B210_B215']:
        mp,dp=[ROOT/f'clean_part_{part}_v1/{name}.json' for name in ['clean_meanings','independent_drafts']]
        m,d=map(load,[mp,dp])
        assert m['current_English_not_consulted'] and d['current_English_not_consulted']
        assert d['source_meanings_sha256']==digest(mp)
        assert len(m['records'])==len(d['records'])
        for a,b in zip(m['records'],d['records'],strict=True):
            assert all(a[k]==b[k] for k in ['id','source_hex','source_reference','source_Japanese','source_meaning','whole_exchange_context'])
            assert b['english']==b['independent_English_draft'] and not any(b['review'].values())
        meanings.extend(deepcopy(m['records']))
        drafts.extend(deepcopy(d['records']))
        for p in [mp,dp,Path(d['authored'])]:evidence[str(p)]=digest(p)
    assert len(meanings)==len(drafts)==len(selected)==321
    assert len({r['id'] for r in drafts})==321
    for original,meaning,draft in zip(selected,meanings,drafts,strict=True):
        assert all(original[k]==meaning[k]==draft[k] for k in ['id','source_hex','source_reference','source_Japanese'])
        assert meaning['source_meaning_reviewed_from_complete_clean_exchange']
        assert draft['current_English_not_consulted'] and draft['logical_paragraph_without_authored_wraps']
        assert draft['english'].isascii() and '\n' not in draft['english']
    shared=dict(source_packet=str(packet_path),source_packet_sha256=digest(packet_path),blocks=packet['selected_blocks'],
        complete_exchanges=18,source_objects=321,current_English_not_consulted=True,new_credit=0,
        full_goal_complete=False,evidence=evidence)
    save(meaning_path,dict(shared,records=meanings,all321_clean_meanings_saved=True,
        source_gloss_precedes_independent_draft_in_each_authored_entry=True,
        each_part_meanings_file_written_before_its_draft_file=True,
        independent_draft_parts_already_saved=True))
    save(draft_path,dict(shared,records=drafts,all321_independent_drafts_saved=True,
        source_meanings=str(meaning_path),source_meanings_sha256=digest(meaning_path),
        translation_policy='natural-dialogue-v2',target_locale='en-US',
        current_English_comparison_names_terms_consumers_andall_five_gates_pending=True))
    save(seal_path,dict(source_objects=321,complete_exchanges=18,source_meanings=str(meaning_path),
        source_meanings_sha256=digest(meaning_path),independent_drafts=str(draft_path),independent_drafts_sha256=digest(draft_path),
        source_glosses_andindependent_drafts_all_saved_before_first_current_story_English_exposure=True,
        all_five_review_gates_pending=True,no_current_story_English_read=True,new_credit=0,full_goal_complete=False,
        evidence={**evidence,str(meaning_path):digest(meaning_path),str(draft_path):digest(draft_path)}))
    print('Sealed321 clean meanings andindependent drafts;18 exchanges; currentEnglish/allgates pending;zero credit.')


if __name__=='__main__':main()
