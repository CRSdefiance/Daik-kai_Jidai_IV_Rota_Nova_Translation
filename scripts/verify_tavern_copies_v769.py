"""Full native research copies with an exact local directory digest only."""

import inspect
import struct
from pathlib import Path

from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.script import common_message_table as parser
from scripts import verify_shipyard_native_copies_v760 as verifier
from scripts.native_machine_scoped_v764 import machine
from scripts.verify_village_wrap_v608 import read

ROOT=Path('work/analysis/tavern_runtime_v769/native_copies')


def main():
    source=ROOT.parent
    plan=read(source/'prospective_common_repack.json')
    common=(source/'COMMON_RESEARCH_ONLY.bin').read_bytes()
    arm=(source/'COMBINED_ARM9_RESEARCH_ONLY.bin').read_bytes()
    assert sha(common)==plan['target_COMMON_sha256'] and sha(arm)==plan['target_ARM9_sha256']
    ROOT.mkdir(parents=True,exist_ok=True)
    for name,data in (('research_COMMON.bin',common),('research_combined_ARM9.bin',arm)):
        path=ROOT/name
        if path.exists():assert path.read_bytes()==data
        else:path.write_bytes(data)
    local=dict(parser.__dict__)
    local['RELOCATED_DIRECTORY_HASHES']=parser.RELOCATED_DIRECTORY_HASHES|{plan['directory_sha256']}
    exec(compile(inspect.getsource(parser.common_message_entries),str(Path(parser.__file__)),'exec'),local)
    entries=local['common_message_entries'](common,arm,clean=False)
    verifier.ROOT=ROOT;verifier.common_message_entries=local['common_message_entries']
    active=[]
    def capture(arm):
        cpu=machine(arm);active[:]=[cpu];return cpu
    verifier.arm946_machine=capture
    original=verifier.loader.warm_copy
    blocks=IlnkContainer.parse(common).blocks
    def complete(arm,common,n,expected,*,cold_cache=False):
        result=original(arm,common,n,expected,cold_cache=cold_cache)
        entry=entries[n];payload=blocks[entry.block][entry.block_offset:entry.copy_end]
        owner=struct.unpack_from('<I',arm,0x552A0)[0]
        assert bytes(active[0].mem_read(owner+0x2030,len(payload)))==payload
        result['entire_native_span_including_post_NUL_payload_exact']=True
        result['complete_span_sha256']=sha(payload)
        return result
    verifier.loader.warm_copy=complete
    verifier.main()


if __name__=='__main__':main()
