"""Every eligible condition in both rumor voices,not gameplay screenshots."""

from pathlib import Path

from PIL import Image,ImageDraw

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.context_tavern_recruitment_v771 import CURRENT,ROOT,RAM_REPORT
from scripts.native_machine_scoped_v764 import machine
from scripts.native_call_abi_v764 import call
from scripts.probe_button_prompt_native import BASE
from scripts.verify_common_alignment_native_v257 import raster
from scripts.verify_shipyard_gameplay_v760 import independent_font
from scripts.verify_market_gameplay_v753 import snapshot
from scripts.verify_village_wrap_v608 import read,save
from unicorn.arm_const import UC_ARM_REG_R0


def main():
    folder=ROOT/'native_layout_phrases_v2';matrix=read(folder/'matrix.json');native=read(folder/'verification.json')
    context=read(ROOT/'native_context.json');rom=NdsImage.open(CURRENT);arm=rom.read_file('/__arm9__.bin')
    previews=[]
    for n in(905,906):
        for status in context['all13_source_status_names_and_UI_labels'][:12]:
            row=next(r for r in matrix['cases'] if r['id']==n and r['source_values_hex']==[b'Rio de Janeiro'.hex(),status['current_UI_label'].encode().hex()])
            pixels=raster(arm,bytes.fromhex(row['formatted_hex']),0x01FFCE40-BASE,size=(228,64),instruction_limit=1000000)
            assert pixels==independent_font(arm,rom.read_file('/GRP/KANJI.FNT'),row['lines'])
            path=folder/f'status_ID{n}_{status["index"]:02d}.png'
            Image.frombytes('L',(228,64),bytes(0 if v else 255 for v in pixels)).save(path)
            previews.append({**row,'status_index':status['index'],'path':str(path),'sha256':sha(path.read_bytes())})
    sheets=[]
    for start in(0,12):
        sheet=Image.new('RGB',(1428,720),'#30343c');draw=ImageDraw.Draw(sheet)
        for i,row in enumerate(previews[start:start+12]):
            x,y=i%3*476,i//3*180;draw.text((x+5,y+4),f'RESEARCH ID{row["id"]} / status{row["status_index"]}',fill='white')
            sheet.paste(Image.open(row['path']).convert('RGB').resize((456,128),Image.Resampling.NEAREST),(x+5,y+24))
        path=folder/f'all12_statuses_ID{905 if start==0 else 906}_2x.png';sheet.save(path);sheets.append({'path':str(path),'sha256':sha(path.read_bytes())})
    # Original lookup returns concrete culture/role NPCs for every main city in
    # this captured world. Null-mode UI coverage is not inferred from this fact.
    u=machine(arm);u.mem_write(BASE,snapshot(read(RAM_REPORT),3200));actors=[]
    for place in context['actual114_native_town_objects'][:90]:
        call(u,0xB2CD8,(place['object'],13));pointer=u.reg_read(UC_ARM_REG_R0)
        assert pointer
        actors.append({'city_index':place['index'],'original_role13_pointer':pointer})
    save(folder/'all_status_font_review.json',{'all24_independent_native_status_planes':previews,'two_full_status_sheets':sheets,
        'primary_font_plane_count':len(native['independent_full_font_planes']),
        'primary_font_proof_sha256':sha((folder/'verification.json').read_bytes()),
        'native_role13_nonnull_for_all90_main_cities_in_current_capture':actors,
        'scope':'Additional full-condition prose/font review and captured NPC inventory;not new gameplay or earned conditions',
        'producer_sha256':sha(Path(__file__).read_bytes()),'full_goal_complete':False})
    print('All12 eligible statuses in both rumor voices rendered;90 captured main-city role13 lookups are non-null.',flush=True)


if __name__=='__main__':main()
