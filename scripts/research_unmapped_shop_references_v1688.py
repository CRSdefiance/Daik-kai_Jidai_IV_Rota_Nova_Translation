"""Broader reference inventory for750-752;negative matches do not prove unused."""
import struct
from pathlib import Path
from capstone import Cs, CS_ARCH_ARM, CS_MODE_ARM
from capstone.arm import ARM_OP_IMM
from ndspy.code import loadOverlayTable
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read, save

ROOT=Path('work/analysis/unmapped_shop_references_v1688')
IDS=(750,751,752)

def occurrences(data,needle):
    found=[];at=0
    while (at:=data.find(needle,at))>=0:found.append(at);at+=1
    return found

if __name__=='__main__':
    assert not ROOT.exists()
    source=Path('work/clean.nds');rom=NdsImage.open(source);arm=rom.read_file('/__arm9__.bin')
    records=[]
    for number in IDS:
        for fmt in ['<H','<I']:
            hits=occurrences(arm,struct.pack(fmt,number))
            records.append({'component':'ARM9','ID_value':number,'packing':fmt,'offsets':hits,'not_inferred_to_be_message_references':True})
    cs=Cs(CS_ARCH_ARM,CS_MODE_ARM);cs.skipdata=True;cs.detail=True;instructions=[]
    for i in cs.disasm(arm[:0xE0000],0x02000000):
        if i.id and i.mnemonic.startswith(('mov','add','sub')) and any(o.type==ARM_OP_IMM and o.imm in IDS for o in i.operands):
            instructions.append({'address':i.address,'mnemonic':i.mnemonic,'operands':i.op_str})
    overlays=[]
    for number,overlay in loadOverlayTable(rom.rom.arm9OverlayTable,lambda overlayID,fileID:rom.rom.files[fileID]).items():
        overlays.append({'overlay':number,'load_address':overlay.ramAddress,'bytes':len(overlay.data),'sha256':sha(overlay.data),
                         'word_matches':{str(n):occurrences(overlay.data,struct.pack('<I',n)) for n in IDS}})
    containers=[]
    for _,path,data in rom.iter_files():
        if not path.startswith(('/data/SC','/data/EV','/testdata/SC','/testdata/EV')):continue
        if '/SC' in path:
            blocks=IlnkContainer.parse(data).blocks;kind='decompressed-ILNK'
        else:blocks=[data];kind='raw-event-file'
        hits=[]
        for n in IDS:
            for block,body in enumerate(blocks):
                for at in occurrences(body,struct.pack('<H',n)):
                    length_field=at==4 and body[:4]==b'CS\0\1'
                    hits.append({'value':n,'block':block,'offset':at,'context_hex':body[max(0,at-16):at+20].hex(),
                                 'CS_header_length_field_not_dialogue_call':length_field,
                                 'declared_CS_length':struct.unpack_from('<I',body,4)[0] if length_field else None,'block_bytes':len(body)})
        containers.append({'path':path,'sha256':sha(data),'kind':kind,'blocks':len(blocks),'packed_halfword_matches':hits})
    assert not instructions
    assert all(hit['CS_header_length_field_not_dialogue_call'] for c in containers for hit in c['packed_halfword_matches'])
    ROOT.mkdir(parents=True)
    save(ROOT/'broader_native_and_script_reference_inventory.json',{'source_ROM':str(source),'source_ROM_sha256':sha(source.read_bytes()),
        'IDs':list(IDS),'ARM9_raw_value_matches':records,'ARM9_mov_add_sub_exact_immediate_search_code_span':[0x02000000,0x020E0000],
        'exact_immediate_candidates':instructions,'original_overlays':overlays,'script_event_and_test_containers':containers,
        'observed_value750_fullword_at02120EAC_is_ship_metadata_not_a_bound_message_call':True,
        'all_route_and_test_script_short_matches_are_CS_header_lengths':True,
        'limitations':['No inference that the responses are unused. Computed IDs,other instruction forms,indirect dispatch and dynamic UI state remain unproven.',
                       'The earlier natural English drafts remain context-unmapped,unintegrated and incomplete. No speaker identity or screen geometry is invented.'],
        'next_action':'Trace original Market cancellation/restart controls or computed response dispatch;keep750-752 open meanwhile.',
        'source_prose_reviews_added':0,'completed_entries_added':0,'producer_sha256':sha(Path(__file__).read_bytes()),'full_goal_complete':False})
    print('750-752 wider reference inventory saved:route/test matches are CS lengths;overlay/main direct scans yield no bound caller. Context remains open;no unused or completion claim.')
