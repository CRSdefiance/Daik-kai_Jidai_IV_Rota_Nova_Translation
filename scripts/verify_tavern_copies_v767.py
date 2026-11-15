"""All3668 complete cold/warm native selections for the Tavern component."""

from pathlib import Path
import struct

from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.script.common_message_table import DIRECTORY_OFFSET, TABLE_OFFSET
import scripts.verify_shipyard_native_copies_v760 as verifier


if __name__ == '__main__':
    verifier.ROOT = Path('work/analysis/tavern_release_v767')
    factory = verifier.arm946_machine
    active = []
    def capture_machine(arm):
        cpu = factory(arm); active[:] = [cpu]; return cpu
    verifier.arm946_machine = capture_machine
    original_copy = verifier.loader.warm_copy
    def complete_copy(arm, common, number, expected, *, cold_cache=False):
        report = original_copy(arm, common, number, expected, cold_cache=cold_cache)
        block = report['block']; start, following = struct.unpack_from('<2H', arm, TABLE_OFFSET + number * 2)
        size = struct.unpack_from('<HH', arm, DIRECTORY_OFFSET + block * 4)[1]
        end = following if following >= start else size
        payload = IlnkContainer.parse(common).blocks[block][start:end]
        owner = struct.unpack_from('<I', arm, 0x552A0)[0]
        assert bytes(active[0].mem_read(owner + 0x2030, len(payload))) == payload
        report['entire_native_span_including_post_NUL_payload_exact'] = True
        report['complete_span_sha256'] = sha(payload)
        return report
    verifier.loader.warm_copy = complete_copy
    verifier.main()
