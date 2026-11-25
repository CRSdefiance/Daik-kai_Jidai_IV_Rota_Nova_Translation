"""Read the live FE bitmap through pinned DeSmuME bank-D ABG mapping, never a rebound RAM offset."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.inspect_committed_gpu_v646 import SOURCE

def read_bitmap(report,frame,header,descriptor):
    snapshots=[s for s in report['read_only_capture_native_states'] if s['frame']==frame];assert len(snapshots)==1;snapshot=snapshots[0]
    assert snapshot['read_only_export'] and snapshot['main_RAM_unchanged_by_export'] and snapshot['serialized_RAM_matches_same_frame_direct_export'] and not snapshot['state_loaded']
    regions={}
    for kind,size in [('LCDM',0xA4000),('9REG',0x2000)]:
        ref=snapshot['regions'][kind];raw=Path(ref['path']).read_bytes();assert len(raw)==ref['bytes']==size and sha(raw)==ref['sha256'];regions[kind]=raw
    # Pinned MMU.cpp maps D's physical pages24..31 to ABG pages0..7
    # for enabled MST1/OFS0. Other current banks do not overlap that map.
    cpp=SOURCE/'MMU.cpp';hdr=SOURCE/'MMU.h';text=cpp.read_text('utf8');head=hdr.read_text('utf8')
    assert '{24,8},' in text and 'MMU_vram_arm9(VRAMBANK,VRAM_PAGE_ABG+VRAMBankCnt.OFS*8);' in text and '#define VRAM_PAGE_ABG 0' in head and 'unsigned MST:3;' in head
    controls=regions['9REG'][0x240:0x24A];assert controls==bytes.fromhex('838b8481820083030082') and controls[3]==0x81
    pixels_address=(descriptor+header[4])&0xFFFFFFFF;relative=pixels_address-0x06000000;length=header[1]*2*header[2]
    assert header[:3]==[4,72,48] and 0<=relative and relative+length<=8*16384
    start=24*16384+relative;value=regions['LCDM'][start:start+length];assert len(value)==length
    return value,dict(frame=frame,original_descriptor_relative_pixel_word=header[4],actual_CPU_VRAM_bitmap_address=pixels_address,physical_LCDM_offset=start,bytes=length,VRAM_control_bytes=controls.hex(),
        original_bank_D_enabled_MST1_OFS0_ABG_mapping=True,physical_page_address=24,bank_pages=8,native_state_metadata=snapshot['path'],native_state_metadata_sha256=snapshot['sha256'],
        source_files={str(p):sha(p.read_bytes()) for p in [cpp,hdr,Path(__file__)]},regions={k:snapshot['regions'][k] for k in regions},read_only_live_VRAM_not_rebound_painter_RAM=True)
