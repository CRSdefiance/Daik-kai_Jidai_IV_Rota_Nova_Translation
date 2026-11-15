"""One prospective native example per draft; not production-selector coverage."""

from pathlib import Path

from PIL import Image,ImageDraw

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.context_tavern_schemes_v774 import ROOT
from scripts.native_machine_scoped_v764 import machine
from scripts.probe_button_prompt_native import BASE
from scripts.probe_tavern_continuation_layout_v768 import format_case
from scripts.review_tavern_schemes_v774 import MANUSCRIPT
from scripts.verify_common_alignment_native_v257 import raster
from scripts.verify_shipyard_gameplay_v760 import independent_font
from scripts.verify_village_wrap_v608 import read,save


def main():
    doc=read(MANUSCRIPT)
    rom=NdsImage.open('out/all_routes_combined_v773_candidate.nds')
    arm=rom.read_file('/__arm9__.bin')
    context=read(ROOT/'native_context.json')
    raw=Path(context['read_only_snapshot']['path']).read_bytes()
    assert sha(raw)==context['read_only_snapshot']['sha256']
    u=machine(arm)
    u.mem_write(BASE,raw)
    values={'scheme_label':b'Forge Papers','faction':b'Bergstrom Fleet','town':b'Amsterdam',
            'first_faction':b'Bergstrom Fleet','second_faction':b'Argot Co.'}
    cases=[]
    sheets=[]
    for i,row in enumerate(doc['records']):
        args=tuple(values[a] for a in row['source_native_arguments'])
        case=format_case(u,row,args)
        assert 'four_row_width_bound' not in case['findings'],case
        plane=raster(arm,bytes.fromhex(case['formatted_hex']),0x01FFCE40-BASE,
            size=(228,64),instruction_limit=1000000)
        assert plane==independent_font(arm,rom.read_file('/GRP/KANJI.FNT'),case['lines'])
        if i%14==0:
            sheet=Image.new('RGB',(940,1120),(235,230,208))
            draw=ImageDraw.Draw(sheet)
            sheets.append(sheet)
        x,y=10+(i%2)*466,8+((i%14)//2)*158
        draw.text((x,y),str(row['message_id'])+' '+', '.join(a.decode() for a in args),fill=(20,20,20))
        image=Image.new('RGB',(228,64),(250,244,216))
        image.putdata([(0,8,0) if v==1 else (250,244,216) for v in plane])
        sheet.paste(image.resize((456,128),Image.Resampling.NEAREST),(x,y+18))
        cases.append({**case,'complete_independent_native_font_plane_exact':True})
    paths=[]
    for i,sheet in enumerate(sheets):
        path=ROOT/f'prospective_examples_{i+1}.png'
        sheet.save(path)
        paths.append({'path':str(path),'sha256':sha(path.read_bytes())})
    save(ROOT/'prospective_example_verification.json',{
        'candidate_sha256':sha(Path('out/all_routes_combined_v773_candidate.nds').read_bytes()),
        'manuscript_sha256':sha(MANUSCRIPT.read_bytes()),'example_count':len(cases),'cases':cases,'sheets':paths,
        'scope':'One supplied representative argument set per56 drafts,original printf and existing literal wrapper,font/raster. Not exhaustive names,production-selector integration or gameplay.',
        'formatting_approval_pending':True,'full_goal_complete':False,
        'producer_sha256':sha(Path(__file__).read_bytes())})
    print('56 prospective native examples and independent font planes;full substitution matrix and integration remain pending.',flush=True)


if __name__=='__main__':main()
