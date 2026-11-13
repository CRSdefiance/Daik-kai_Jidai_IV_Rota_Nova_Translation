"""Save individually authored meanings from whole clean exchanges without current-English intake."""
import argparse
import importlib
from copy import deepcopy
from pathlib import Path
from scripts.audit_story_glyph_consistency import load,save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest

def main():
    p=argparse.ArgumentParser(description=__doc__)
    for key in ['packet','module','out']:p.add_argument('--'+key,required=True)
    a=p.parse_args();packet_path=Path(a.packet);out=Path(a.out);assert not out.exists()
    packet=load(packet_path);data=importlib.import_module(a.module)
    assert packet['current_English_unconsulted'] and data.CONTEXT.keys()==data.GLOSSES.keys()
    groups={g['block']:g for g in packet['groups']};records=[]
    for block,meanings in data.GLOSSES.items():
        source=groups[block]['records'];indexed={r['source_record_index']:r for r in source}
        assert len(indexed)==len(source) and {i for i,_ in meanings}==set(indexed)
        assert len(meanings)==len(source) and data.CONTEXT[block].strip()
        for index,meaning in meanings:
            row=deepcopy(indexed[index]);assert meaning.strip() and row['current_English_unconsulted']
            row.update(source_meaning=meaning,whole_exchange_context=data.CONTEXT[block],
                source_meaning_pending=False,source_first_independent_meaning_saved=True,
                source_read_with_all_previous_andfollowing_speeches_in_block=True,
                source_meaning_not_final_context_name_orformat_approval=True)
            assert not any(row['review'].values());records.append(row)
    save(out,dict(records=records,records_count=len(records),blocks=list(data.GLOSSES),
        clean_source_packet=str(packet_path),clean_source_packet_sha256=digest(packet_path),
        current_English_unconsulted=True,all_individual_meanings_from_complete_clean_exchanges=True,
        approved_names_used_without_new_relationship_rank_orbiography=True,
        localized_drafts_current_comparison_andfive_gates_still_pending=True,new_credit=0,
        evidence={str(q):digest(q) for q in [packet_path,Path(data.__file__),Path(__file__)]}))
    print('Sealed',len(records),'individual clean meanings in',len(data.GLOSSES),'complete exchanges;current English unread,zero credit.')

if __name__=='__main__':main()
