"""Bind unchanged historical Palace/Inn families; do not invent current visits."""
from pathlib import Path
from PIL import Image,ImageDraw
from dk4tool.rom.nds import NdsImage
from dk4tool.patch import palace_editorial,inn_editorial
from dk4tool.patch.town_trade_port_contextual_reference_v1 import current_entries
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/palace_inn_history_v2260')
INPUTS=[('work/analysis/palace_integration_v797/contract_gameplay_verification.json','actual_repaired_holds'),('work/analysis/palace_gameplay_v798/treasure_gameplay_verification.json','five_repaired_holds'),('work/analysis/palace_label_boundaries_v799/actual_family_verification.json','sixteen_actual_holds'),('work/analysis/inn_integration_v803/stay_gameplay_verification.json','actual_holds'),('work/analysis/inn_integration_v803/news_report_refusal_gameplay.json','actual_holds'),('work/analysis/inn_history_v804/history_gameplay_verification.json','cases'),('work/analysis/inn_history_v804/departure_gameplay_verification.json','actual_holds')]
if __name__=='__main__':
    assert not ROOT.exists();ROOT.mkdir(parents=True);current=NdsImage.open('out/all_routes_combined_v2171_candidate.nds');arm=current.read_file('/__arm9__.bin');entries=current_entries(current.read_file('/COMMON/MESFILE.DK4'),arm)
    holds=[];proofs=[];roms={};reports={}
    for group,(path,key)in enumerate(INPUTS):
        path=Path(path);d=read(path);report_paths=[]
        if group==0:report_paths=d['report_paths']
        elif group==1:report_paths=[d['capture_report']]
        elif group==2:
            for row in d['reports']:assert sha(Path(row['path']).read_bytes())==row['sha256']
            report_paths=[r['path']for r in d['reports']]
        elif group==3:report_paths=d['reports']
        elif group==4:
            for row in d['scenarios']:assert sha(Path(row['report']).read_bytes())==row['report_sha256']
            report_paths=[r['report']for r in d['scenarios']]
        elif group==5:
            for row in d['cases']:assert sha(Path(row['report']).read_bytes())==row['report_sha256']
            report_paths=[r['report']for r in d['cases']]
        else:assert sha(Path(d['report']).read_bytes())==d['report_sha256'];report_paths=[d['report']]
        for p in report_paths:
            report=read(p);reports[p]=sha(Path(p).read_bytes())
            if report['ROM_sha256']!=d['candidate_sha256']:continue
            rp=Path(report['ROM']);assert sha(rp.read_bytes())==report['ROM_sha256'];roms[str(rp)]=report['ROM_sha256'];prior=NdsImage.open(rp);owned=palace_editorial if group<3 else inn_editorial
            old=owned.current_entries(prior.read_file('/COMMON/MESFILE.DK4'),prior.read_file('/__arm9__.bin'));ids=range(1146,1177)if group<3 else range(1177,1200)
            assert all(old[n].text==entries[n].text for n in ids)
            assert prior.read_file('/GRP/KANJI.FNT')==current.read_file('/GRP/KANJI.FNT')
        for h in d[key]:
            capture=h.get('capture',h.get('hold'));assert sha(Path(capture['path']).read_bytes())==capture['PNG_sha256']
            holds.append(dict(message_ID=h.get('id',h.get('message_id')),frame=capture['frame'],lines=h['lines'],capture=capture['path'],capture_sha256=capture['PNG_sha256'],source_proof=str(path),source_proof_sha256=sha(path.read_bytes()),historical_only_not_current_visit=True,inherited_complete_renderer_comparison_fields={k:v for k,v in h.items()if isinstance(v,bool)}))
        proofs.append(dict(path=str(path),sha256=sha(path.read_bytes()),holds=len(d[key]),historical_provenance_and_fixtures=d))
    geometry_path=Path('work/analysis/palace_label_boundaries_v799/actual_menu_geometry_verification.json');geometry=read(geometry_path);assert geometry['all_six_labels_complete_in_actual_menus']and geometry['total_actual_rows']==12
    oldarm=NdsImage.open('out/all_routes_combined_v799_candidate.nds').read_file('/__arm9__.bin');doc=read('translations/palace_inn_contextual_editorial_manuscript_v1.json')
    for row in doc['auxiliary_labels'][:6]:
        field=row['current_reference']['field'];assert arm[field:field+4]==oldarm[field:field+4];p=row['current_reference']['pointer']-0x02000000;assert arm[p:p+len(row['english'])+1]==oldarm[p:p+len(row['english'])+1]
    for lo,hi in geometry['source_geometry_code_exact_to_clean']:assert arm[lo:hi]==oldarm[lo:hi]
    menu=[];cap=Path('E:/Rota Nova translations/Generated/work/emulation_v193/palace_v799_expanded_menu')
    for row in geometry['frames']:
        p=cap/f"frame_{row['frame']:06d}_navigation.png";assert sha(p.read_bytes())==row['PNG_sha256'];menu.append(dict(frame=row['frame'],capture=str(p),capture_sha256=row['PNG_sha256'],source_original_geometry=row,historical_only_not_current_visit=True))
    sheets=[]
    for name,rows in [('historical_dialogue',holds),('historical_six_label_menu',menu)]:
        for start in range(0,len(rows),12):
            selected=rows[start:start+12];sheet=Image.new('RGB',(1024,410*((len(selected)+3)//4)),'#263238');draw=ImageDraw.Draw(sheet)
            for i,r in enumerate(selected):
                x,y=i%4*256,i//4*410;draw.text((x+3,y+3),f"HISTORICAL ID{r.get('message_ID','menu')} f{r['frame']}",fill='white');sheet.paste(Image.open(r['capture']).convert('RGB'),(x,y+22))
            p=ROOT/f'{name}_{start//12:02d}.png';sheet.save(p);sheets.append(dict(path=str(p),sha256=sha(p.read_bytes()),scope='historical-family-or-menu-only;not-current-gameplay'))
    assert len(holds)==44
    save(ROOT/'historical_family_binding.json',dict(candidate_sha256=sha(Path('out/all_routes_combined_v2171_candidate.nds').read_bytes()),historical_proofs=proofs,historical_holds=holds,historical_IDs=sorted({r['message_ID']for r in holds}),sampled_ROMs=roms,source_reports=reports,all_sampled_complete_Palace31_or_Inn23_paragraphs_and_font_exact_current=True,current1492_formatted_bytes_identical_historical=True,historical_menu_geometry_proof=str(geometry_path),historical_menu_geometry_proof_sha256=sha(geometry_path.read_bytes()),current_six_labels_pointers_strings_and_original_geometry_code_exact_historical=True,historical_menu_frames=menu,review_sheets=sheets,historical_declared_headquarters_letter_money_item_qualification_and_history_market_inputs_not_earned=True,no_actual_monthly_payment_or_naturally_generated_battle_raid_claim=True,current_actual_Inn5_IDs_separate_in2258b=True,visual_review_pending=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False));print(dict(historical_holds=len(holds),historical_IDs=len({r['message_ID']for r in holds}),menu_frames=len(menu),sheets=len(sheets)))
