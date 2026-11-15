"""Explicit-filename engine compatibility for four unresolved standalone resources.

Original scene consumers are not inferred from these supplied resource contracts.
"""
import json
import struct
from pathlib import Path

from unicorn import UC_HOOK_CODE
from unicorn.arm_const import (
    UC_ARM_REG_LR,
    UC_ARM_REG_PC,
    UC_ARM_REG_R0,
    UC_ARM_REG_R1,
    UC_ARM_REG_R2,
)

from dk4tool.graphics.pxl import PxlImage
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.probe_button_prompt_native import STACK, call, machine
from scripts.research_online_loader_v190 import resource_call

ROM = Path('out/all_routes_combined_v546_candidate.nds')
ROOT = Path('work/analysis/standalone_resource_compatibility_v550')
VIEW = 0x02470020
OPEN, READ, SEEK, CLOSE = 0x020DED50, 0x020DEBDC, 0x020DEB70, 0x020DED08
PATHS = ('/_pxl/copyright.pxl','/_pxl/logo.pxl','/_pxl/ship_eurL.pxl','/_pxl/startmenu0.pxl')


def native_compatibility(image):
    arm = image.read_file('/__arm9__.bin')
    clean = NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    for lo,hi in [(0x5310,0x5340),(0x10FB1C,0x10FB40),(0xD3D30,0xD42AC),(0xD6524,0xD6C90)]:
        assert arm[lo:hi] == clean[lo:hi]
    u = machine(arm)
    resource_call(u,0x5310,())
    manager = struct.unpack_from('<I',arm,0x5D24)[0]
    call(u,0xD6C0C,(manager,))
    # Derive the class tag from an actual originally initialized registered owner.
    actual_fields = struct.unpack('<5I',u.mem_read(0x02313344,20))
    assert actual_fields[0] == 0x02160538 and actual_fields[4] == 0xFFFFFFFF
    owners = {}
    for n,path in enumerate(PATHS):
        owner = 0x02460020+n*0x100
        name = owner+0x40
        u.mem_write(owner-16,b'\xA5'*68)
        u.mem_write(name,path.lstrip('/').encode('ascii')+b'\0')
        call(u,0xD6C74,(owner,))
        assert struct.unpack('<3I',u.mem_read(owner,12))[1:] == (owner+4,owner+4)
        # Filename and derived class fields are explicit diagnostic inputs,
        # following the source-exact registered class layout. No PXL bytes or
        # native file/cache result is invented or preloaded.
        u.mem_write(owner,struct.pack('<I',actual_fields[0]))
        u.mem_write(owner+12,struct.pack('<2I',name,0xFFFFFFFF))
        assert bytes(u.mem_read(owner-16,16)) == b'\xA5'*16
        assert bytes(u.mem_read(owner+20,32)) == b'\xA5'*32
        owners[path] = owner
    handles, events = {}, []

    def bridge(uc, address, size, _):
        if address not in (OPEN, READ, SEEK, CLOSE):
            return
        obj = uc.reg_read(UC_ARM_REG_R0)
        if address == OPEN:
            name = bytes(uc.mem_read(uc.reg_read(UC_ARM_REG_R1), 96)).split(b"\0", 1)[0].decode("ascii")
            path = "/" + name.replace("\\", "/").lstrip("/")
            if path not in owners or obj in handles:
                raise ValueError("Native title file contract differs")
            data = image.read_file(path)
            handles[obj] = [path, data, 0]
            uc.mem_write(obj + 0x20, struct.pack("<2I", 0, len(data)))
            events.append({"operation": "open", "path": path, "sha256": sha(data)})
            result = 1
        elif address == SEEK:
            state = handles[obj]
            offset = uc.reg_read(UC_ARM_REG_R1)
            if uc.reg_read(UC_ARM_REG_R2) != 0 or not 0 <= offset <= len(state[1]):
                raise ValueError("Native title seek leaves source")
            state[2] = offset
            result = 1
        elif address == READ:
            state = handles[obj]
            target, count = uc.reg_read(UC_ARM_REG_R1), uc.reg_read(UC_ARM_REG_R2)
            if state[2] + count > len(state[1]):
                raise ValueError("Native title read leaves source")
            uc.mem_write(target, state[1][state[2]:state[2] + count])
            state[2] += count
            events.append({"operation": "read", "path": state[0], "count": count})
            result = count
        else:
            events.append({"operation": "close", "path": handles.pop(obj)[0]})
            result = 1
        uc.reg_write(UC_ARM_REG_R0, result)
        uc.reg_write(UC_ARM_REG_PC, uc.reg_read(UC_ARM_REG_LR))

    hook = u.hook_add(UC_HOOK_CODE, bridge)
    cases = []
    try:
        for path, owner in sorted(owners.items()):
            data = image.read_file(path)
            pxl = PxlImage.from_bytes(data)
            u.mem_write(VIEW - 16, b"\xa5" * 80)
            u.mem_write(VIEW, bytes(48))
            # Same whole-image constructor arguments as original scene setup
            # 0203DEE0 -> 020D4018; zero width/height asks for native full extent.
            u.mem_write(STACK, bytes(8))
            trace = resource_call(u, 0xD4018, (VIEW, owner, 0, 0))
            fields = struct.unpack("<12I", u.mem_read(VIEW, 48))
            # Reproduce original scene 0203DEE0's virtual source-to-destination
            # copy. Zero optional crop dimensions are a lazy full-image view;
            # do not invent explicit bounds in the source or call slot +8 a
            # size getter (it is another view constructor).
            destination, point = VIEW + 0x100, VIEW + 0x200
            u.mem_write(destination - 16, b"\xa5" * 80)
            u.mem_write(destination, bytes(48))
            u.mem_write(point, bytes(8))
            resource_call(u, 0xD3D80, (destination,))
            destination_vtable = struct.unpack("<I", u.mem_read(destination, 4))[0]
            copy_method = struct.unpack("<I", u.mem_read(destination_vtable + 12, 4))[0]
            resource_call(u, copy_method - 0x02000000, (destination, point, VIEW))
            copied_fields = struct.unpack("<12I", u.mem_read(destination, 48))
            resource_call(u, 0xD4170, (destination,))
            pointer = u.reg_read(UC_ARM_REG_R0)
            if (fields[3] != owner or copied_fields[1:] != fields[1:]
                    or bytes(u.mem_read(pointer, len(data))) != data or handles
                    or bytes(u.mem_read(VIEW - 16, 16)) != b"\xa5" * 16
                    or bytes(u.mem_read(VIEW + 48, 16)) != b"\xa5" * 16
                    or bytes(u.mem_read(destination - 16, 16)) != b"\xa5" * 16
                    or bytes(u.mem_read(destination + 48, 16)) != b"\xa5" * 16
                    or 0x020D4018 not in trace):
                raise ValueError(f"Native title view/header/palette/pixels/guards differ: {path}, pointer={pointer:#x}")
            assert bytes(u.mem_read(owner - 16,16)) == b"\xa5"*16
            assert bytes(u.mem_read(owner + 20,32)) == b"\xa5"*32
            assert bytes(u.mem_read(owner+12,4)) == struct.pack("<I",owner+0x40)
            cases.append({"path": path, "owner": owner, "data_pointer": pointer,
                          "owner_canaries_and_supplied_filename_pointer_retained": True,
                          "source_sha256": sha(data), "complete_resource_bytes": len(data),
                          "native_view": list(fields), "destination_view": list(copied_fields),
                          "source_header_extent": [pxl.width, pxl.height],
                          "native_virtual_copy_method": copy_method,
                          "native_optional_crop_parameters": list(fields[7:12]),
                          "complete_header_palette_indices_exact": True,
                          "constructor_virtual_copy_return_stack_and_view_guards_verified": True,
                          "unobserved_physical_crop_not_claimed": path != "/_pxl/title/title03.pxl"})
    finally:
        u.hook_del(hook)
    return {"cases": cases, "SDK_file_contract_events": events}



def main():
    ROOT.mkdir(parents=True,exist_ok=True)
    assert sha(ROM.read_bytes()) == '499e0ad767b1badf899ab6873ad787f171651035c7d6316012af2b8afc8c77d3'
    image = NdsImage.open(ROM)
    result = native_compatibility(image)
    assert len(result['cases']) == 4
    result.update({'candidate':str(ROM),'candidate_sha256':sha(ROM.read_bytes()),
                   'source_original_engine_routines_executed_with_explicit_filename_contracts':True,
                   'original_base_resource_constructor_and_native_class_tag_from_registered_owner':True,
                   'all4_unregistered_file_headers_palettes_and_full_indices_native_loaded_exact':True,
                   'zero_optional_crop_arguments_are_lazy_full_image_views_not_actual_scene_bounds':True,
                   'source_original_startup_registration_still_does_not_register_these4_paths':True,
                   'original_scene_consumers_or_GPU_composition_not_proven':True,
                   'production_ROM_changed':False,'full_goal_complete':False,
                   'all22_requirements_and18_incomplete_plaques_retained':True})
    (ROOT/'compatibility_proof.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print('All4 standalone files load/copy exact through original engine with explicit filename contracts; original scenes and GPU remain open.')


if __name__ == '__main__':
    main()
