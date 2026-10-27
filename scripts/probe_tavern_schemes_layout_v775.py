"""Full catalog substitutions through native printf and literal formatting."""

import argparse
from itertools import product
from pathlib import Path

from PIL import Image,ImageDraw

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.context_tavern_schemes_v774 import ROOT as SOURCE
from scripts.native_machine_scoped_v764 import machine
from scripts.probe_button_prompt_native import BASE
from scripts.probe_tavern_continuation_layout_v768 import format_case
from scripts.review_tavern_schemes_v774 import MANUSCRIPT
from scripts.verify_common_alignment_native_v257 import raster
from scripts.verify_shipyard_gameplay_v760 import independent_font
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/tavern_schemes_layout_v775')
CURRENT=Path('out/all_routes_combined_v773_candidate.nds')


def main(manuscript=MANUSCRIPT,root=ROOT):
    MANUSCRIPT,ROOT=Path(manuscript),Path(root)
    ROOT.mkdir(parents=True,exist_ok=True)
    rom=NdsImage.open(CURRENT)
    arm=rom.read_file('/__arm9__.bin')
    doc=read(MANUSCRIPT)
    context=read(SOURCE/'native_context.json')
    towns_context=read('work/analysis/tavern_recruitment_editorial_v771/native_context.json')
    factions=[bytes.fromhex(r['name_hex']) for r in context['all21_initialized_native_faction_names'] if r['name_hex']]
    towns=[bytes.fromhex(r['name_hex']) for r in towns_context['actual114_native_town_objects']]
    labels=[bytes.fromhex(r['label_hex']) for r in context['four_original_scheme_labels']]
    assert len(factions)==20 and len(towns)==114 and len(labels)==4
    assert sha(CURRENT.read_bytes())==context['candidate_sha256']
    boundary=b'ABCDEFGHIJKLMNOPQRSTUVW'
    raw=Path(context['read_only_snapshot']['path']).read_bytes()
    assert sha(raw)==context['read_only_snapshot']['sha256']
    def variants(n):
        if 915<=n<=920: yield from ((s,) for s in labels)
        elif 940<=n<=947:
            yield from product(factions,towns)
            yield from product((boundary,),towns)
        elif 948<=n<=955:
            yield from product(factions,factions)
            yield from product((boundary,),factions)
            yield from product(factions,(boundary,))
            yield (boundary,boundary)
        elif 956<=n<=963:
            yield from product(towns,factions)
            yield from product(towns,(boundary,))
        else: yield ()
    cases,findings,fonts=[],[],[]
    for row in doc['records']:
        family=[]
        for i,args in enumerate(variants(row['message_id'])):
            if i%64==0:
                u=machine(arm)
                u.mem_write(BASE,raw)
            case=format_case(u,row,args)
            case['synthetic_23_byte_faction_boundary']=boundary in args
            family.append(case)
            if case['findings']:findings.append(case)
        cases.extend(family)
        # Every record's maximal expanded length and maximal row/width case.
        choices=[max(family,key=lambda r:sum(len(x) for x in r['lines'])),
                 max(family,key=lambda r:(len(r['lines']),max(map(len,r['lines']))))]
        seen=set()
        for case in choices:
            if case['formatted_hex'] in seen:continue
            seen.add(case['formatted_hex'])
            plane=raster(arm,bytes.fromhex(case['formatted_hex']),0x01FFCE40-BASE,size=(228,64),instruction_limit=1000000)
            assert plane==independent_font(arm,rom.read_file('/GRP/KANJI.FNT'),case['lines'])
            path=ROOT/f'font_{len(fonts):03d}_ID{case["id"]}.png'
            Image.frombytes('L',(228,64),bytes(0 if v==1 else 255 for v in plane)).save(path)
            fonts.append({**case,'path':str(path),'sha256':sha(path.read_bytes()),'complete_independent_font_plane_exact':True})
        print(f'ID{row["message_id"]}: {len(family)} native layouts;{len(findings)} cumulative findings.',flush=True)
    save(ROOT/'native_layout_matrix.json',{'count':len(cases),'findings_count':len(findings),'cases':cases,
        'all20_named_factions_all114_town_names_and_four_scheme_labels':True,
        'synthetic23_byte_boundary_is_not_a_proven_input_limit_or_earned_state':True,
        'combinations_not_all_claimed_reachable':True})
    save(ROOT/'layout_findings.json',findings)
    sheets=[]
    for start in range(0,len(fonts),12):
        sheet=Image.new('RGB',(1428,720),'#30343c')
        draw=ImageDraw.Draw(sheet)
        for i,row in enumerate(fonts[start:start+12]):
            x,y=i%3*476,i//3*180
            draw.text((x+5,y+4),f'RESEARCH ID{row["id"]} / {start+i}',fill='white')
            sheet.paste(Image.open(row['path']).convert('RGB').resize((456,128),Image.Resampling.NEAREST),(x+5,y+24))
        path=ROOT/f'complete_fonts_{start//12:02d}_2x.png'
        sheet.save(path)
        sheets.append({'path':str(path),'sha256':sha(path.read_bytes())})
    save(ROOT/'verification.json',{'candidate':str(CURRENT),'candidate_sha256':sha(CURRENT.read_bytes()),
        'manuscript_sha256':sha(MANUSCRIPT.read_bytes()),'complete_native_layouts':len(cases),
        'findings_count':len(findings),'complete_font_planes':fonts,'preview_sheets':sheets,
        'all56_IDs_covered':sorted({r['id'] for r in cases}),
        'scope':'Original printf and existing literal formatter directly;not production selector,integration or gameplay.',
        'formatting_approval_pending':True,'full_goal_complete':False,
        'producer_sha256':sha(Path(__file__).read_bytes())})
    print(f'{len(cases)} layouts,{len(fonts)} fonts,{len(findings)} findings. Research only.',flush=True)


if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--manuscript',default=str(MANUSCRIPT))
    parser.add_argument('--out',default=str(ROOT))
    args=parser.parse_args()
    main(args.manuscript,args.out)
