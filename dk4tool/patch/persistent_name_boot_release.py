"""Stage persistent names outside ARM7's initial image before the final copy."""

import json
import struct
from pathlib import Path

from ndspy.code import MainCodeFile

from dk4tool.patch.grand_race_menu_release import sha

SOURCE = 'dde53bd0a3832dc4c01437f119ba10faaaab47b053234fb27bbcab545710862a'
BASE, POOL, STAGE = 0x02000000, 0x02387A20, 0x023A7200
ARM7 = 'cf22688a539b0923e2027c27f3b150beb5b65ee9f5d7380b8150e51d70d198ec'


def transform(source, arm7, arm7_base):
    if sha(source) != SOURCE or sha(arm7) != ARM7 or arm7_base != 0x02380000:
        raise ValueError('Exact V150 ARM9 and ARM7 boot identity required')
    if STAGE < arm7_base + len(arm7):
        raise ValueError('Staging overlaps ARM7 initial load')
    code = MainCodeFile(source, BASE)
    if len(code.sections) != 4 or code.sections[3].ramAddress != POOL:
        raise ValueError('Original persistent section ownership differs')
    payload = bytes(code.sections[3].data)
    if (len(payload) != 1504 or struct.unpack_from('<I', source, 0x8E4)[0] != 0xEB000BD9
            or struct.unpack_from('<I', source, 0xE45DC)[0] != POOL + len(payload)):
        raise ValueError('Startup hook or final heap reservation differs')
    main = bytes(code.sections[0].data)
    entry = STAGE + len(payload)
    stub = struct.pack('<12I', 0xE92D400F, 0xE59F0018, 0xE59F1018, 0xE59F2018,
                       0xE4903004, 0xE4813004, 0xE2522004, 0x1AFFFFFB,
                       0xE8BD800F, STAGE, POOL, len(payload))
    struct.pack_into('<I', code.sections[0].data, 0x8E4,
                     0xEB000000 | (((entry - (BASE + 0x8E4 + 8)) // 4) & 0xFFFFFF))
    code.sections[3].ramAddress = STAGE
    code.sections[3].data = bytearray(payload + stub)
    saved = bytes(code.save())
    check = MainCodeFile(saved, BASE)
    restored = bytearray(check.sections[0].data)
    restored[0x8E4:0x8E8] = main[0x8E4:0x8E8]
    off = code.codeSettingsOffs
    restored[off:off + 12] = main[off:off + 12]
    if (bytes(restored) != main or any(bytes(check.sections[n].data) != bytes(code.sections[n].data)
                                      for n in (1, 2))
            or check.sections[3].ramAddress != STAGE
            or bytes(check.sections[3].data) != payload + stub):
        raise ValueError('Boot repair changes unrelated main/ITCM/DTCM/payload bytes')
    return saved


def apply_release(source, config_path, arm7, arm7_base):
    config = json.loads(Path(config_path).read_text(encoding='utf-8'))
    if (config.get('format') != 'dk4-persistent-name-boot-release-v1'
            or config['source_arm9_sha256'] != SOURCE or config['source_arm7_sha256'] != ARM7):
        raise ValueError('Boot repair release configuration differs')
    saved = transform(source, arm7, arm7_base)
    if sha(saved) != config['target_arm9_sha256']:
        raise ValueError('Boot repair target identity differs')
    return saved, {'status': 'staged-persistent-name-boot-repair-cold-boot-pending',
                   'arm9_sha256': sha(saved), 'arm7_source_sha256': sha(arm7),
                   'staging_span': [STAGE, STAGE + 1552],
                   'final_pool_span': [POOL, POOL + 1504],
                   'copy_entry': STAGE + 1504, 'full_boot_verified': False}
