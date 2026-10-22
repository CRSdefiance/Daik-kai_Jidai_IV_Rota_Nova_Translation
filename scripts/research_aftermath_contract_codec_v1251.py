"""Capacity research for exact caller memberships; no ARM9/ROM mutation.

Eight owned rows retain parent/stack/high-word metadata. Payload bytes encode
sorted range gaps:low7bits0..126 are the gap,127 precedes a LE16 gap;bit7
means an additional byte gives range length minus1. The header counts payload
bytes. This accommodates numeric2192 while preserving every historical key.
Native decoder/ABI/reference/font/gameplay proof is still required.
"""
from pathlib import Path
import struct
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.escape_direct_runtime_v1183b import contract_rows,table,CONTRACTS,PACKED_PHRASES,END,GATE
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/aftermath_contract_codec_v1251')
ROLE_KEYS=(0x7640,0x76A0,0x76E0,0x7740,0x7760,0x7900,0x7D00,0x7F00)
DIRECT_KEYS=(0x7640,0x77E0,0x7840,0x78C0)


def rows():
    out=[]
    for parent,offset,high,values in contract_rows():
        keys=set(values)
        if parent==0x02054014:keys.add(2192)
        elif parent==0x02053DB8:keys.update(ROLE_KEYS)
        elif parent==0x02053F40:keys.update(DIRECT_KEYS)
        out.append((parent,offset,high,tuple(sorted(keys))))
    return out


def encode(logical):
    result=bytearray()
    for parent,offset,high,values in logical:
        shift=(4 if parent==0x02053C14 else 5) if high else 0
        bias=896 if high else 384
        keys=sorted((v>>shift)-bias for v in values)
        assert keys[0]>=0 and keys[-1]<65536
        ranges=[]
        for key in keys:
            if ranges and key==ranges[-1][1]+1 and key-ranges[-1][0]<256:
                ranges[-1]=(ranges[-1][0],key)
            else:ranges.append((key,key))
        payload=bytearray();previous_end=-1
        for low,high_key in ranges:
            gap=low-(previous_end+1);length=high_key-low
            assert 0<=gap<=65535 and 0<=length<=255
            payload.append((128 if length else 0)|(gap if gap<127 else 127))
            if gap>=127:payload.extend(struct.pack('<H',gap))
            if length:payload.append(length)
            previous_end=high_key
        field=(offset+24-0x180)//4
        assert 0<=field<128 and len(payload)<256
        result.extend(struct.pack('<HBB',parent&65535,field|(128 if high else 0),len(payload)))
        result.extend(payload)
    return bytes(result)


def decode(data,count):
    pos=0;logical=[]
    for _ in range(count):
        parent,field,size=struct.unpack_from('<HBB',data,pos);pos+=4
        end=pos+size;assert end<=len(data)
        high=0x0211 if field&128 else 0
        offset=(field&127)*4+0x180-24
        parent|=0x02050000
        shift=(4 if parent==0x02053C14 else 5) if high else 0
        bias=896 if high else 384
        previous_end=-1;values=[]
        while pos<end:
            code=data[pos];pos+=1
            gap=code&127
            if gap==127:
                assert pos+2<=end
                gap=data[pos]+(data[pos+1]<<8);pos+=2
            length=0
            if code&128:
                assert pos<end;length=data[pos];pos+=1
                assert length>0
            low=previous_end+1+gap;last=low+length
            values.extend((key+bias)<<shift for key in range(low,last+1))
            previous_end=last
        assert pos==end and values==sorted(set(values))
        logical.append((parent,offset,high,tuple(values)))
    assert pos==len(data)
    return logical


def main():
    assert not ROOT.exists()
    path=Path('out/all_routes_combined_v1224_candidate.nds');rom=NdsImage.open(path);arm=rom.read_file('/__arm9__.bin')
    old=contract_rows();assert len(old)==8
    assert arm[CONTRACTS-0x02000000:CONTRACTS-0x02000000+188]==table()
    assert PACKED_PHRASES>=CONTRACTS+188 and END>PACKED_PHRASES
    logical=rows();before=encode(old);after=encode(logical)
    assert decode(before,8)==old and decode(after,8)==logical
    assert len(after)<=188,(len(after),188)
    added=[];cases=0
    for (parent,offset,high,prior),(p,o,h,now) in zip(old,logical,strict=True):
        assert (parent,offset,high)==(p,o,h) and set(prior)<=set(now)
        added.append({'parent':parent,'stack_selector_offset':offset,'high_word':high,
            'old_key_count':len(prior),'new_keys':sorted(set(now)-set(prior))})
        decoded=next(v for pp,oo,hh,v in decode(after,8) if pp==parent)
        for key in range(65536):
            assert (key in set(now))==(key in set(decoded));cases+=1
    assert sum(len(r['new_keys']) for r in added)==13
    ROOT.mkdir(parents=True)
    output=ROOT/'prospective_contract_metadata_ONLY.bin';output.write_bytes(after)
    save(ROOT/'encoding_capacity_research.json',{'source_ROM':str(path),'source_ROM_sha256':sha(path.read_bytes()),
        'source_ARM9_sha256':sha(arm),'contracts_address':CONTRACTS,'owned_existing_contract_bytes':188,
        'public_bank_end':END,'protected_packed_status_phrases':PACKED_PHRASES,
        'owned_gate_address_and_bytes':[GATE,172],
        'old_logical_rows':old,'prospective_logical_rows':logical,'exact_added_memberships':added,
        'old_reencoded_bytes':len(before),'prospective_encoded_bytes':len(after),
        'prospective_metadata':str(output),'prospective_metadata_sha256':sha(after),
        'all524288_low_word_membership_comparisons_against_independent_logical_sets':cases,
        'no_existing_membership_removed_and_only13_proven_new_keys_added':True,
        'supports2192_without_10bit_truncation':True,
        'native_decoder_must_use_byte_loads_for_LE16_gaps_not_unaligned_halfwords':True,
        'native_decoder_parent_high_word_alignment_stack_ABI_reference_fonts_and_gameplay_UNIMPLEMENTED':True,
        'no_ARM9_ROM_registry_or_completion_change':True,'producer_sha256':sha(Path(__file__).read_bytes()),
        'full_goal_complete':False})
    print('Prospective metadata:',len(after),'/188 bytes;all historical memberships retained;13 new keys;native decoder still required.',flush=True)


if __name__=='__main__':main()
