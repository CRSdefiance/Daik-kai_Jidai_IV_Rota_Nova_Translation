"""Every original warm/cold native copy,including complete post-NUL payloads."""

import struct
from pathlib import Path

from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from scripts import verify_shipyard_native_copies_v760 as verifier
from scripts.native_machine_scoped_v764 import machine
from scripts.prepare_recruitment_common_v772 import local_entries
from scripts.verify_recruitment_owned_v772 import ROOT as SOURCE
from scripts.verify_village_wrap_v608 import read

ROOT=SOURCE/'native_copies'


def main():
    plan=read(SOURCE/'prospective_common_repack.json')
    common=(SOURCE/'COMMON_RESEARCH_ONLY.bin').read_bytes();arm=(SOURCE/'COMBINED_ARM9_RESEARCH_ONLY.bin').read_bytes()
    assert sha(common)==plan['target_COMMON_sha256'] and sha(arm)==plan['target_ARM9_sha256']
    ROOT.mkdir(parents=True,exist_ok=True)
    for name,data in(('research_COMMON.bin',common),('research_combined_ARM9.bin',arm)):
        p=ROOT/name
        if p.exists():assert p.read_bytes()==data
        else:p.write_bytes(data)
    reader=local_entries(plan['directory_sha256']);entries=reader(common,arm,clean=False)
    verifier.ROOT=ROOT;verifier.common_message_entries=reader;active=[]
    def capture(arm):
        cpu=machine(arm);active[:]=[cpu];return cpu
    verifier.arm946_machine=capture
    original=verifier.loader.warm_copy;blocks=IlnkContainer.parse(common).blocks
    def complete(arm,common,n,expected,*,cold_cache=False):
        result=original(arm,common,n,expected,cold_cache=cold_cache)
        entry=entries[n];payload=blocks[entry.block][entry.block_offset:entry.copy_end]
        owner=struct.unpack_from('<I',arm,0x552A0)[0]
        assert bytes(active[0].mem_read(owner+0x2030,len(payload)))==payload
        result['entire_native_span_including_post_NUL_payload_exact']=True
        result['complete_span_sha256']=sha(payload)
        return result
    verifier.loader.warm_copy=complete;verifier.main()


if __name__=='__main__':main()
