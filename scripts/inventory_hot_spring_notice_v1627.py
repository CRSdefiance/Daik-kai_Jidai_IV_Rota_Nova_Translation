"""Keep the original optional Experience notice in the broader prose audit."""
from dataclasses import asdict
from pathlib import Path
import struct
from capstone import Cs,CS_ARCH_ARM,CS_MODE_ARM
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import common_message_entries
from dk4tool.patch.hot_spring_editorial import current_entries
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/hot_spring_notice_source_v1627')
ROM=Path('out/all_routes_combined_v1622_candidate.nds')
if __name__=='__main__':
    assert not ROOT.exists()
    clean,current=NdsImage.open('work/clean.nds'),NdsImage.open(ROM)
    original,arm=clean.read_file('/__arm9__.bin'),current.read_file('/__arm9__.bin')
    jp=common_message_entries(clean.read_file('/COMMON/MESFILE.DK4'),original);en=current_entries(current.read_file('/COMMON/MESFILE.DK4'),arm)
    assert original[0x79344:0x793B4]==arm[0x79344:0x793B4]
    assert struct.unpack_from('<I',arm,0x793B0)[0]==310
    md=Cs(CS_ARCH_ARM,CS_MODE_ARM);records=[]
    for n in [309,310,311]:
        records.append({'message_id':n,'source_reference':{k:v for k,v in asdict(jp[n]).items() if k!='text'},
            'source_hex':jp[n].text.hex(),'source_Japanese':jp[n].text.decode('cp932'),
            'current_reference':{k:v for k,v in asdict(en[n]).items() if k!='text'},'current_text_hex':en[n].text.hex(),'current_English':en[n].text.decode('cp932')})
    ROOT.mkdir(parents=True);save(ROOT/'optional_hot_spring_Experience_notice310_source.json',{'candidate':str(ROM),'candidate_sha256':sha(ROM.read_bytes()),
        'records_and_neighbors':records,'original_call':0x02079390,'original_entry':0x020546B8,'original_message_ID_literal':0x020793B0,
        'original_no_runtime_argument_in310_source':b'%' not in jp[310].text,
        'code':[{'address':i.address,'mnemonic':i.mnemonic,'operands':i.op_str} for i in md.disasm(original[0x79344:0x793A4],0x02079344)],
        'context':'The original optional hot-spring skill/RNG branch speaks through role1/table2116D60,executes6624C(10,10),then calls546B8(310) with no printf argument. Japanese says the benefits of the hot spring increased the stat quoted as Experience. Do not invent an affected party,total,guaranteed full-fatigue recovery or numeric experience amount in this no-argument notice.',
        'findings':['Current Hot spring raised Experience is awkward system prose.','Current authored leading spaces and LF require the speakerless native literal-modal review.'],
        'no_edit_no_new_source_prose_or_completion_credit':True,'prose_native_release_and_actual_optional_notice_review_pending':True,
        'producer_sha256':sha(Path(__file__).read_bytes()),'full_goal_complete':False})
    print('Optional original Experience notice310 inventoried with clean/current references and actual caller;prose/native/release/actual gates still open,no counts changed.')
