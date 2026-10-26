"""Bind historical qualified family samples without inventing current visits."""
from pathlib import Path
from PIL import Image,ImageDraw
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import common_message_entries
from dk4tool.patch.town_trade_port_contextual_reference_v1 import current_entries
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/guild_courier_history_v2246')
INPUTS=[Path('work/analysis/item_transactions_v789/qualified_transactions_gameplay.json'),Path('work/analysis/letter_eligibility_v790/actual_letter_dialogs.json'),Path('work/analysis/arrival_notices_v792/gameplay_verification.json')]
if __name__=='__main__':
    assert not ROOT.exists();ROOT.mkdir(parents=True)
    rom=NdsImage.open('out/all_routes_combined_v2171_candidate.nds');entries=current_entries(rom.read_file('/COMMON/MESFILE.DK4'),rom.read_file('/__arm9__.bin'))
    proofs=[];holds=[];sheets=[];roms={}
    for group,path in enumerate(INPUTS):
        d=read(path);reports=d.get('source_reports',d.get('reports'));hashes=d.get('source_report_sha256',d.get('report_sha256'))
        for i,p in enumerate(reports):
            digest=sha(Path(p).read_bytes());assert digest==(hashes[p]if isinstance(hashes,dict)else hashes[i]);report=read(p)
            if report['ROM_sha256']!=d['candidate_sha256']:continue
            rp=Path(report['ROM']);assert sha(rp.read_bytes())==report['ROM_sha256'];roms[str(rp)]=report['ROM_sha256']
            prior=NdsImage.open(rp);old=common_message_entries(prior.read_file('/COMMON/MESFILE.DK4'),prior.read_file('/__arm9__.bin'),clean=False)
            selected=list(range(1070,1146))if group<2 else [346,347,348]
            assert all(old[n].text==entries[n].text for n in selected)
        local=[]
        for h in d['holds']:
            c=h['capture'];assert sha(Path(c['path']).read_bytes())==c['PNG_sha256']
            assert h['complete_independent_font_and_blank_paper_exact']and h['all_other_pixels_exact']
            row=dict(message_ID=h['message_id'],frame=h['frame'],lines=h['lines'],capture=c['path'],capture_sha256=c['PNG_sha256'],source_proof=str(path),source_proof_sha256=sha(path.read_bytes()),historical_qualified_not_current_visit=True)
            local.append(row);holds.append(row)
        for start in range(0,len(local),12):
            subset=local[start:start+12];sheet=Image.new('RGB',(1024,410*((len(subset)+3)//4)),'#263238');draw=ImageDraw.Draw(sheet)
            for i,r in enumerate(subset):
                x,y=i%4*256,i//4*410;draw.text((x+3,y+3),f"HISTORICAL g{group} ID{r['message_ID']} f{r['frame']}",fill='white');sheet.paste(Image.open(r['capture']).convert('RGB'),(x,y+22))
            sp=ROOT/f'historical_group{group}_sheet{start//12}.png';sheet.save(sp);sheets.append(dict(path=str(sp),sha256=sha(sp.read_bytes()),scope='historical-qualified-family-only;not-new-current-gameplay'))
        proofs.append(dict(path=str(path),sha256=sha(path.read_bytes()),holds=len(local),IDs=sorted({r['message_ID']for r in local}),inherited_source_metadata=d))
    matrix=read('work/analysis/guild_courier_layouts_v2241/all79_current_native_layouts.json')
    old=read('work/analysis/item_diplomacy_integration_v788/production_layout/verification.json')['cases']+read('work/analysis/arrival_notices_v792/native_verification.json')['layouts']
    assert len(old)==len(matrix['cases'])==2823
    assert all(a['formatted_hex']==b['formatted_hex']for a,b in zip(old,matrix['cases']))
    assert len(holds)==35 and len(sheets)==5 and roms
    save(ROOT/'historical_family_binding.json',dict(candidate_sha256=sha(Path('out/all_routes_combined_v2171_candidate.nds').read_bytes()),historical_proofs=proofs,historical_holds=holds,historical_IDs=sorted({r['message_ID']for r in holds}),sampled_ROMs=roms,all_sampled_complete_paragraphs_identical_current=True,all2823_current_formatted_bytes_identical_historical=True,review_sheets=sheets,source_qualification_and_PRNG_controls_inherited_not_earned_or_current=True,arrival_daily_world_object_outputs_not_globally_approved=True,entry346_not_individually_activated=True,old791_broken_arrival_format_not_used_for_visual_approval=True,current_GPU_visits_separately_in2244=True,visual_review_pending=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print(dict(historical_holds=35,IDs=sorted({r['message_ID']for r in holds}),sheets=5))
