"""Automatic native compilation for distinct embedded and argument-free modal consumers."""
from functools import lru_cache
from pathlib import Path
from types import FunctionType
from unicorn.arm_const import UC_ARM_REG_R0
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts import mood_comments_layout_v980 as base
from scripts.native_call_abi_v764 import call
from scripts.verify_arrival_native_v792 import prepared

ROM=Path('out/all_routes_combined_v981_candidate.nds')
ROM_SHA='fa5656c1d0a234d5626c2eb917d9f29a1d4a48cfdaeba5900cff3a71c3def01b'
ARM_SHA='a446afb0ea754456351b9257b34edc8526d9c437bd2af7fe0f9cb2fe3e0ddadb'
WIDTH=36
MAX_LINES=3
PHRASES=[('get','angry'),('come','on'),('got','hungry'),('do','it','again'),('now','now'),('change','of','pace'),
    ('getting','angry'),('bad','for'),('your','health'),('no','rush'),('take','our','time'),('with','the','work'),
    ('one','drink'),('lift','my','spirits'),('free','moment'),('i','train'),('pickup','line'),('thought','of'),
    ('get','into','mischief'),('come','here'),('put','my','training'),('to','the','test'),('real','war'),('let','me','fight'),('stay','hidden')]
KEEP_TOGETHER=base.KEEP_TOGETHER|{tuple(w.strip('.,!?;:').lower() for w in pair) for p in PHRASES for pair in zip(p,p[1:])}
WEAK=base.WEAK
layout=FunctionType(base.layout.__code__,{**base.layout.__globals__,'KEEP_TOGETHER':KEEP_TOGETHER})
serialize=base.serialize

@lru_cache(maxsize=1)
def source_arm():
    assert sha(ROM.read_bytes())==ROM_SHA
    arm=NdsImage.open(ROM).read_file('/__arm9__.bin');assert sha(arm)==ARM_SHA
    return arm

@lru_cache(maxsize=3)
def modal_compile(english):
    assert english and english==' '.join(english.split()) and english.isascii()
    assert len(english)<220 and all(32<=ord(c)<127 and c not in '%{}' for c in english)
    assert not any(t in english for t in ('FI','FA','FO','FU','IC'))
    arm=source_arm();cpu=prepared(arm);text=b' '+english.encode('ascii');src,dest=0x02450020,0x02451020
    cpu.mem_write(src-16,b'\xa5'*16+text+b'\0'+b'\xa5'*16)
    cpu.mem_write(dest-16,b'\xa5'*288)
    # Execute the existing balanced formatter as an offline compiler. No runtime
    # membership,code,allocation or authored paragraph changes are required.
    call(cpu,0x147AE5,(src,dest),instruction_limit=2000000);length=cpu.reg_read(UC_ARM_REG_R0)
    assert 0<length<240
    result=bytes(cpu.mem_read(dest,length));assert bytes(cpu.mem_read(dest+length,1))==b'\0'
    assert bytes(cpu.mem_read(src,len(text)+1))==text+b'\0'
    assert bytes(cpu.mem_read(src-16,16))==bytes(cpu.mem_read(src+len(text)+1,16))==b'\xa5'*16
    assert bytes(cpu.mem_read(dest-16,16))==bytes(cpu.mem_read(dest+256,16))==b'\xa5'*16
    assert b' '.join(result.split())==english.encode('ascii')
    lines=[s.strip().decode('ascii') for s in result.split(b'\n')]
    assert 1<=len(lines)<=4 and max(map(len,lines))<=35
    return result

def compiled(row):
    assert 1872<=row['message_id']<=1888
    if row['consumer']=='assignment-refusal-modal':
        assert row['message_id'] in (1878,1879,1880)
        return modal_compile(row['english'])
    assert row['consumer']=='Deck-CabinInfoView' and row['message_id'] not in (1878,1879,1880)
    return serialize(layout(row['english']))

def visible_lines(row):
    return [s.strip().decode('ascii') for s in compiled(row).split(b'\n')] if row['consumer']=='assignment-refusal-modal' else layout(row['english'])
