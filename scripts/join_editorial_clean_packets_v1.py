"""Join disjoint source-only packets without re-extracting their completed inventories."""
import argparse
from copy import deepcopy
from pathlib import Path
from scripts.audit_story_glyph_consistency import load,save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--packets',type=Path,nargs='+',required=True)
    parser.add_argument('--out',type=Path,required=True)
    args=parser.parse_args();assert not args.out.exists()
    docs=[load(p) for p in args.packets];result=deepcopy(docs[0]);groups=[]
    for doc in docs:
        for key in ['source_ROM','source_ROM_sha256','source_archive_sha256','source_ARM9_sha256','route','file_path']:
            assert doc[key]==result[key]
        assert doc['clean_only_no_prior_English_ornew_editorial_credit'] and doc['new_credit']==0
        assert sum(len(g['records']) for g in doc['groups'])==doc['records']
        groups.extend(doc['groups'])
    assert len({g['block'] for g in groups})==len(groups)
    groups.sort(key=lambda r:r['block'])
    assert digest(result['source_ROM'])==result['source_ROM_sha256']
    result.update(groups=groups,records=sum(len(g['records']) for g in groups),
        exact_disjoint_clean_packet_join=True,source_inventories_reused_not_rerun=True,
        packet_inputs={str(p):digest(p) for p in args.packets},join_producer_sha256=digest(__file__))
    save(args.out,result);print('Joined',result['records'],'source speeches in',len(groups),'complete blocks.')

if __name__=='__main__':main()
