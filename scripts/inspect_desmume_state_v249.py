"""Read-only state export: CPU registers and TCM absent from the RAM API."""

import ctypes as ct
import json
import struct
import zlib
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha


def parse(raw):
    if raw[:16]!=b"DeSmuME SState\0\0":
        raise ValueError("Unknown native state header")
    version,emu,size,compressed=struct.unpack_from("<4I",raw,16)
    if version!=12:
        raise ValueError("Pinned native state version differs")
    if compressed==0xFFFFFFFF:
        if not 32<=size<=len(raw):
            raise ValueError("Declared state extent escapes export")
        body=raw[32:size]
    else:
        if compressed>len(raw)-32:
            raise ValueError("Compressed state extent escapes export")
        body=zlib.decompress(raw[32:32+compressed])
        if len(body)!=size:
            raise ValueError("State decompression extent differs")
    chunks={};pos=0
    while pos<len(body):
        if pos+4>len(body):
            raise ValueError("Truncated state chunk ID")
        kind=struct.unpack_from("<I",body,pos)[0];pos+=4
        if kind==0xFFFFFFFF:
            if pos!=len(body):
                raise ValueError("State has unparsed bytes after terminator")
            break
        if pos+4>len(body):
            raise ValueError("Truncated state chunk length")
        length=struct.unpack_from("<I",body,pos)[0];pos+=4
        if kind in chunks or pos+length>len(body):
            raise ValueError("State chunk extent or ID differs")
        chunks[kind]=body[pos:pos+length];pos+=length
    else:
        raise ValueError("Native state terminator missing")
    fields={}
    for kind in (1,4,60):
        source=chunks[kind];offset=0;rows={}
        while offset<len(source):
            if offset+12>len(source):
                raise ValueError("Truncated tagged state header")
            name=source[offset:offset+4].decode("ascii")
            item,count=struct.unpack_from("<2I",source,offset+4);offset+=12
            length=item*count
            if name in rows or offset+length>len(source):
                raise ValueError("Tagged state field extent differs")
            rows[name]=source[offset:offset+length];offset+=length
        fields[kind]=rows
    return fields,{"state_version":version,"emulator_version":emu,"chunk_ids":list(chunks),
                   "all_declared_chunks_and_selected_tag_fields_bounded":True}


def export(core,directory,expected_ram):
    core.retro_serialize_size.argtypes=[];core.retro_serialize_size.restype=ct.c_size_t
    size=core.retro_serialize_size()
    if not 0<size<=32*1024*1024:
        raise ValueError("Unexpected serialized state allocation")
    data=(ct.c_ubyte*size)()
    core.retro_serialize.argtypes=[ct.c_void_p,ct.c_size_t];core.retro_serialize.restype=ct.c_bool
    if not core.retro_serialize(data,size):
        raise ValueError("Native read-only state export failed")
    fields,proof=parse(bytes(data))
    if fields[4]["WRAM"]!=expected_ram:
        raise ValueError("Serialized main RAM differs from same-frame direct export")
    if ct.string_at(core.retro_get_memory_data(2),len(expected_ram))!=expected_ram:
        raise ValueError("State export changed main RAM")
    directory=Path(directory);directory.mkdir(parents=True,exist_ok=True)
    regions={}
    proof['MMU_serialized_field_extents'] = {tag: len(value) for tag, value in fields[4].items()}
    for tag,name,expected in [("ITCM","arm9_itcm.bin",0x8000),("DTCM","arm9_dtcm.bin",0x4000),
                              ("WRAX","arm9_extra_ram.bin",0x400000),("9REG","arm9_io.bin",0x2000),
                              ("OAMS","arm9_oam.bin",0x800),
                              ("LCDM","arm9_lcdc_vram.bin",0xA4000)]:
        raw=fields[4][tag]
        if len(raw)!=expected:
            raise ValueError("Native region extent differs: "+tag)
        path=directory/name;path.write_bytes(raw)
        regions[tag]={"path":str(path),"bytes":len(raw),"sha256":sha(raw)}
    if 'VMEM' in fields[4]:
        palette = fields[4]['VMEM']
        if len(palette) != 0x800:
            raise ValueError('Serialized standard palette extent differs')
        path = directory / 'arm9_standard_palettes.bin'
        path.write_bytes(palette)
        regions['VMEM'] = {'path':str(path),'bytes':len(palette),'sha256':sha(palette)}
    registers=list(struct.unpack("<16I",fields[1]["9REG"]))
    proof.update({"regions":regions,"ARM9_registers":registers,
                  "ARM9_instruction_address":struct.unpack("<I",fields[1]["9INA"])[0],
                  "DTCM_region":struct.unpack("<I",fields[60]["MDTC"])[0],
                  "ITCM_region":struct.unpack("<I",fields[60]["MITC"])[0],
                  "serialized_RAM_matches_same_frame_direct_export":True,
                  "main_RAM_unchanged_by_export":True,"state_loaded":False,"read_only_export":True,
                  "source_commit":"95b4d798731caa809125b6c3c11d17cc332ff6ef"})
    path=directory/"native_state.json";path.write_text(json.dumps(proof,indent=2)+"\n",encoding="utf-8")
    return {"path":str(path),"sha256":sha(path.read_bytes()),**proof}
