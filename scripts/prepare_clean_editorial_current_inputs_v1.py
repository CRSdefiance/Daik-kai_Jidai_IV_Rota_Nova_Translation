"""Project sealed clean-first drafts for guarded speech/style/two-or-three-menu binders."""
import argparse
from collections import Counter
from copy import deepcopy
from pathlib import Path
import re
import struct
from scripts.audit_story_glyph_consistency import load, save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from dk4tool.patch.grand_race_menu_release import sha


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    for name in ['drafts','packet','out']: parser.add_argument('--'+name,type=Path,required=True)
    args=parser.parse_args(); assert not args.out.exists()
    drafts,source=map(load,[args.drafts,args.packet]); count=source['records']
    assert len(drafts['records'])==count and drafts['current_English_not_consulted']
    assert drafts['whole_clean_exchanges_read_before_drafting']
    assert all(not any(r['review'].values()) and r['current_English_comparison_pending'] for r in drafts['records'])
    assert {r['id'] for r in drafts['records']}=={r['id'] for g in source['groups'] for r in g['records']}
    args.out.mkdir(); source=deepcopy(source)
    source.update(original_selected_packet=str(args.packet),original_selected_packet_sha256=digest(args.packet))
    groups={g['block']:g for g in source['groups']}
    for g in groups.values():g['clean_block_sha256']=sha(bytes.fromhex(g['clean_block_hex']))
    source_path=args.out/'source_packet.json'; save(source_path,source)
    sealed=args.out/'sealed_drafts.json'
    save(sealed,dict(source_meanings_andlogical_drafts_sealed_before_current_ROM_English_extraction_in_this_intake=True,
        source_meanings=drafts['source_meanings'],source_meanings_sha256=drafts['source_meanings_sha256'],
        independent_drafts=str(args.drafts),independent_drafts_sha256=digest(args.drafts),
        no_blanket_historical_English_exposure_claim=True,no_new_gates_orcredit=True,new_credit=0))
    grouped={'speech':[],'styles':[],'choices':[]}
    for original in drafts['records']:
        row=deepcopy(original); group=groups[row['block']]; block=bytes.fromhex(group['clean_block_hex'])
        ref=row['source_reference']; at=ref['offset']; raw=bytes.fromhex(row['source_hex'])
        assert block[at:at+len(raw)]==raw
        command=next(c for c in group['all_source_commands'] if c['offset']==ref['command_offset'])
        whole=bytes.fromhex(command['whole_command_hex']); assert block[command['offset']:command['offset']+len(whole)]==whole
        row.update(source_record_index=block[:at].count(b'\0'),
            source_macros={t:len(re.findall(t,row['source_Japanese'])) for t in ['FI','FA','FO','FU']},
            source_command_offset=command['offset'],source_word=command['word'],
            earlier_English_unconsulted=True,current_ROM_English_unconsulted=True)
        if row['kind']=='ordinary-speech':
            assert command['word']==0x4000 and whole[:6].hex()==row['source_complete_preamble_hex']; name='speech'
        elif row['kind']=='physical-style-alternative':
            assert command['word']==0x4100; offsets=list(struct.unpack_from('<8H',whole,2))
            indices=[i for i,v in enumerate(offsets) if command['offset']+20+v==at]; assert indices
            assert all(whole[20+offsets[i]:whole.index(0,20+offsets[i])]==raw for i in indices)
            row.update(source_header_hex=whole[:20].hex(),source_style_indices=indices,source_style_offsets=offsets,source_selector=whole[19]);name='styles'
        else:
            assert row['kind']=='typed-menu-caption' and command['word'] in (0x2100,0x2200)
            n={0x2100:2,0x2200:3}[command['word']]; base=2+2*n; offsets=struct.unpack_from(f'<{n}H',whole,2)
            i=int(row['id'].rsplit('_',1)[1]); assert i in range(n) and command['offset']+base+offsets[i]==at
            assert whole[base+offsets[i]:whole.index(0,base+offsets[i])]==raw
            row.update(source_index=i,source_count=n,source_choice_object_hex=whole.hex()); name='choices'
        grouped[name].append(row)
    assert sum(map(len,grouped.values()))==count
    for name,rows in grouped.items():
        save(args.out/(name+'_meanings.json'),dict(records=rows,meanings=len(rows),source_packet=str(source_path),
            source_packet_sha256=digest(source_path),all_drafts_sealed=str(sealed),all_drafts_sha256=digest(sealed),
            no_blanket_prior_English_exposure_claim=True,source_only_not_current_story_English=True,all_review_gates_pending=True,new_credit=0))
    counts={k:len(v) for k,v in grouped.items()}
    save(args.out/'projection.json',dict(source_objects=count,groups=counts,all_source_glosses_drafts_controls_andreferences_unchanged=True,
        dynamic_source_selectors=Counter(r['source_selector'] for r in grouped['speech'] if r['source_selector'] in range(207,224)),
        FE_source_panels=sum(r['source_selector']==254 for r in grouped['speech']),
        source_meanings_preceded_drafts_andcurrent_intake=True,no_new_gates_orcredit=True,new_credit=0,
        evidence={str(p):digest(p) for p in [args.drafts,args.packet,sealed,Path(__file__)]}))
    print(dict(source_objects=count,groups=counts,new_credit=0))

if __name__=='__main__': main()
