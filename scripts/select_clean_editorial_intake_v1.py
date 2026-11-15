"""Select disjoint complete clean exchanges using the already-qualified native census."""
import argparse
from collections import Counter
from copy import deepcopy
from pathlib import Path
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load,save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    for arg in ['packet','out','release']:ap.add_argument('--'+arg,type=Path,required=True)
    ap.add_argument('--blocks',type=int,nargs='+',required=True);ap.add_argument('--expected-records',type=int,required=True)
    args=ap.parse_args();assert not args.out.exists() and args.blocks==sorted(set(args.blocks))
    packet,release=map(load,[args.packet,args.release])
    assert packet['source_only_not_current_English'] and packet['complete_native_inventory_reused_not_rerun']
    assert digest('translations/release_stack.json')==release['registry_sha256']
    assert digest(release['candidate'])==release['candidate_sha256']
    image=NdsImage.open(packet['source_ROM']);assert digest(packet['source_ROM'])==packet['source_ROM_sha256']
    resource=image.read_file(packet['file_path']);assert sha(resource)==packet['source_archive_sha256']
    blocks=IlnkContainer.parse(resource).blocks
    groups=deepcopy([g for g in packet['groups'] if g['block'] in args.blocks])
    assert [g['block'] for g in groups]==args.blocks
    ledger=load('translations/editorial_review_current_v1.json')
    credited={(r['file_path'],r['id']) for r in ledger['contextual_story_natural_dialogue_pass_v1871']['integrated_record_keys']}
    keys=[];ids=[]
    for group in groups:
        assert bytes.fromhex(group['clean_block_hex'])==blocks[group['block']]
        for row in group['records']:
            assert not row['covered'] and not row['exact_credited_source_bindings']
            raw=bytes.fromhex(row['source_hex']);at=row['source_reference']['offset']
            assert blocks[row['block']][at:at+len(raw)]==raw
            keys.append((row['block'],at,row['source_hex']));ids.append((row['file_path'],row['id']))
    assert len(keys)==len(set(keys))==len(set(ids))==args.expected_records and not set(ids)&credited
    args.out.mkdir()
    selected=args.out/'clean_source_packet.json'
    save(selected,dict(packet,groups=groups,records=len(keys),selected_blocks=args.blocks,complete_exchanges=len(groups),
        original_census=str(args.packet),original_census_sha256=digest(args.packet),new_credit=0))
    counts=Counter(r['kind'] for g in groups for r in g['records'])
    save(args.out/'source_selection_v1.json',dict(source_objects=len(keys),complete_exchanges=len(groups),consumer_counts=dict(counts),
        blocks=[dict(block=g['block'],records=len(g['records'])) for g in groups],
        all_exact_clean_source_positions_rechecked=True,complete_existing_native_inventory_reused_not_replayed=True,
        source_current_comparisons_andall_five_gates_pending=True,no_current_English_read_orapproval=True,
        no_meanings_drafts_orlocalization_approval_yet=True,exact_disjoint_credited_keys=True,
        registered_parent=release['candidate'],registered_parent_sha256=release['candidate_sha256'],new_credit=0,
        evidence={str(p):digest(p) for p in [args.packet,args.release,selected,Path(__file__)]}))
    print(dict(source_objects=len(keys),complete_exchanges=len(groups),consumers=dict(counts),new_credit=0,current_English_not_exposed=True))

if __name__=='__main__':main()
