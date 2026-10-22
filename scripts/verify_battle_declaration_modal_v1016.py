"""Bind complete actual modal glyphs to source selection and reviewed native canvases."""
import argparse
import struct
import unicodedata
from pathlib import Path
from PIL import Image
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.battle_declaration_editorial import current_entries
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from scripts.battle_declaration_layout_v996 import compiled
from scripts.verify_personal_gameplay_v841 import get_machine
from scripts.verify_port_gameplay_v762 import cstring
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/battle_declaration_v1016')
ROM=Path('out/all_routes_combined_v997_candidate.nds')
SPECS={'UnknownJanus':(4,1904,'unknown'), 'KnownJanus':(4,1897,'named'),
       'UnknownEmilio':(14,1909,'unknown'), 'ReadyEmilio':(14,1895,'ready')}


def verify(folder,label,frame):
    folder=Path(folder);rom=NdsImage.open(ROM);arm=rom.read_file('/__arm9__.bin')
    digest=sha(ROM.read_bytes());assert digest==read(ROM.with_suffix('.manifest.json'))['candidate_sha256']
    actor,n,family=SPECS[label]
    rawp=folder/f'frame_{frame:06d}_arm9_ram.bin';raw=rawp.read_bytes();assert len(raw)==0x400000
    shot=folder/f'frame_{frame:06d}_navigation.png';image=Image.open(shot).convert('RGB');assert image.size==(256,384)
    row=next(r for r in read('translations/battle_declaration_editorial_manuscript_v3.json')['records'] if r['message_id']==n)
    entries=current_entries(rom.read_file('/COMMON/MESFILE.DK4'),arm)
    assert entries[n].text==compiled(row)
    owner,wrapped=[struct.unpack_from('<I',arm,k)[0] for k in (0x552A0,0x54450)]
    assert cstring(raw,owner+0x2030)==compiled(row)
    value=cstring(raw,wrapped)
    fontproof=read('work/analysis/battle_declaration_v995b/native_font_proof.json')
    cases=[c for c in fontproof['cases'] if c['message_id']==n and
           (c['faction_name_case'] is None if family!='named' else c['faction_name_case']['company_ID']==9)]
    assert len(cases)==1;case=cases[0]
    assert value==bytes.fromhex(case['native_formatted_hex'])
    assert compiled(row)==bytes.fromhex(case['compiled_template_hex'])
    path=Path(case['preview']);assert sha(path.read_bytes())==case['preview_sha256']
    plane=Image.open(path).convert('L');assert plane.size==(228,64)
    expected={(16+x,296+y) for y in range(64) for x in range(228) if plane.getpixel((x,y))==0}
    actual={(x,y) for y in range(294,366) for x in range(16,244) if image.getpixel((x,y))==(0,8,0)}
    assert expected==actual,(label,frame,'complete glyph plane mismatch',len(expected-actual),len(actual-expected))
    cpu,get=get_machine(arm,raw);actors=get(0xCB184);obj=actors+4+actor*32
    assert get(0x82478,get(0xCB1A8)+0x2090,1)==actor
    table={'unknown':0x02117400,'named':0x02117420,'ready':0x02117440}[family]
    assert get(0x53F4C,obj,table)==n
    vt=struct.unpack('<I',cpu.mem_read(obj,4))[0]
    fn=struct.unpack('<I',cpu.mem_read(vt+0x20,4))[0]
    pointer=get(fn-0x02000000,obj)
    name=unicodedata.normalize('NFKC',bytes(cpu.mem_read(pointer,128)).split(b'\0')[0].decode('cp932'))
    blocks=IlnkContainer.parse(rom.read_file('/COMMON/MESFILE.DK4')).blocks
    assert raw.count(blocks[entries[n].block])==1
    if n==1909:
        assert case['generated_native_lines'][0].endswith(' I')
        assert b'\x96\x6c' not in value.lower()
    return {'label':label,'frame':frame,'message_ID':n,'source_family':family,
        'actor_ID':actor,'native_actor_name':name,'source_table':table,
        'original_First_Mate_role_and_voice_selector_pass':True,
        'source_resident_bytes_and_complete_native_wrapping_exact':True,
        'single_complete_current_native_block_resident':True,
        'generated_native_lines':case['generated_native_lines'],
        'all228x64_reviewed_native_independent_font_pixels_match_actual_RGB':True,
        'complete_leading_trailing_letters_uniform_cell_origins_bounds_and_blank_ink_region_pass':True,
        'capture':str(shot),'capture_sha256':sha(shot.read_bytes()),'RAM':str(rawp),'RAM_sha256':sha(raw),
        'font_reference':str(path),'font_reference_sha256':sha(path.read_bytes()),
        'candidate_sha256':digest,'producer_sha256':sha(Path(__file__).read_bytes()),
        'portrait_name_choices_and_transition_verification_required_separately':True,
        'goal_complete':False}


def main():
    p=argparse.ArgumentParser();p.add_argument('--folder',required=True);p.add_argument('--case',choices=SPECS,required=True)
    p.add_argument('--frame',required=True,type=int);a=p.parse_args()
    proof=verify(a.folder,a.case,a.frame);ROOT.mkdir(exist_ok=True)
    out=ROOT/f'{a.case}_{a.frame:06d}_complete_modal.json';assert not out.exists();save(out,proof)
    print(a.case,a.frame,proof['generated_native_lines'],'complete actual glyphs/source pass',flush=True)


if __name__=='__main__':main()
