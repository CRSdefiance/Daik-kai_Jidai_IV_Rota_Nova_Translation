"""Inn selector extension in existing allocations; research until registered."""

import struct

from dk4tool.patch import palace_editorial_runtime as previous

bank=previous.bank
BASE=bank.BASE
CONTRACTS=previous.LUXURY_GOODS
TABLE_USED=142
TABLE_BYTES=144
PACKED_PHRASES=CONTRACTS+TABLE_BYTES
END=previous.END
TIME_START=0x02143DCC
TIME_END=0x02143DF4
LAST_MONTH=0x02143E04
THIS_MONTH=TIME_START
LUXURY_GOODS=TIME_START+12
MONTHS_AGO=TIME_START+25
ORDINARY=(1178,1179,*range(1181,1186),*range(1194,1199))
YES_NO=(1177,1180,1199)


def contract_rows():
    rows=[]
    for parent,offset,high,values in previous.contract_rows():
        selected=set(values)
        if parent==0x02054014:selected.update(ORDINARY)
        elif parent==0x02053FCC:selected.update(YES_NO)
        elif parent==0x02053DB8:selected.add(0x80E0)
        rows.append((parent,offset,high,tuple(sorted(selected))))
    return rows


def table():
    data=bytearray()
    for parent,offset,high,values in contract_rows():
        shift=(4 if parent==0x02053C14 else 5) if high else 0
        assert all(not n&((1<<shift)-1) for n in values)
        keys=sorted((n>>shift)-512 if high else n for n in values)
        ranges=[]
        for key in keys:
            if ranges and key==ranges[-1][1]+1:ranges[-1]=(ranges[-1][0],key)
            else:ranges.append((key,key))
        encoded=[]
        for lo,hi in ranges:
            while lo<=hi:
                end=min(lo+31,hi)
                assert 0<=lo<=end<2048
                encoded.append(lo|((end-lo)<<11));lo=end+1
        field=(offset+24-0x180)//4
        data.extend(struct.pack('<HBB',parent&65535,field|(128 if high else 0),len(encoded)))
        data.extend(struct.pack('<'+'H'*len(encoded),*encoded))
    assert len(data)==TABLE_USED
    return bytes(data)+bytes(TABLE_BYTES-len(data))


def patches(arm):
    assert PACKED_PHRASES==previous.PACKED_PHRASES
    assert arm[previous.LUXURY_GOODS-BASE:previous.CONTRACTS-BASE]==b'luxury goods\0\0'
    assert arm[previous.CONTRACTS-BASE:previous.PACKED_PHRASES-BASE]==previous.table()
    words=list(struct.unpack_from('<12H',arm,PACKED_PHRASES-BASE))
    assert words[7]*4+bank.DATA_BASE==previous.LUXURY_GOODS
    words[7]=(LUXURY_GOODS-bank.DATA_BASE)//4
    assert bank.DATA_BASE+words[7]*4==LUXURY_GOODS
    data=table()+struct.pack('<12H',*words)
    assert CONTRACTS+len(data)==END and len(data)==168
    blob=b'This month\0\0luxury goods\0%s months ago\0\0'
    assert len(blob)==40 and blob[12:25]==b'luxury goods\0' and blob[25:39]==b'%s months ago\0'
    assert arm[TIME_END-BASE:TIME_END-BASE+8]==b'Reclaim\0'
    assert arm[LAST_MONTH-BASE:LAST_MONTH-BASE+12]==b'Mil Invest\0\0'
    result={CONTRACTS:data,TIME_START:blob,LAST_MONTH:b'Last month\0\0'}
    for at,old,new in ((0x5CB2C,0x02143DCC,LAST_MONTH),(0x5CB30,0x02143DD4,THIS_MONTH),
                        (0x5CB34,0x02143DDC,MONTHS_AGO),(0x5CB38,0x02143DE8,MONTHS_AGO)):
        assert struct.unpack_from('<I',arm,at)[0]==old
        result[BASE+at]=struct.pack('<I',new)
    gate=arm[bank.GATE-BASE:bank.GATE-BASE+164]
    needle=struct.pack('<I',previous.CONTRACTS)
    assert gate.count(needle)==1
    result[bank.GATE+gate.index(needle)]=struct.pack('<I',CONTRACTS)
    return result


def apply(arm):
    out=bytearray(arm)
    for at,raw in patches(arm).items():out[at-BASE:at-BASE+len(raw)]=raw
    assert len(out)==len(arm)
    return bytes(out)
