"""Source-reviewed successor: avoid fleet-from-Fleet with complete faction labels."""
from copy import deepcopy
from pathlib import Path
from PIL import Image,ImageDraw
from types import FunctionType
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.search_reports_editorial import current_entries
from dk4tool.script.common_message_table import common_message_entries
from dk4tool.dialogue.review import validate_natural_dialogue_batch
from scripts.prepare_work_comments_v842 import reference
from scripts.reinforcement_sniping_layout_v1024 import compiled
from scripts.probe_reinforcement_sniping_layout_v1030 import native_layout,TABLES
from scripts.verify_arrival_native_v792 import prepared
from scripts.verify_common_alignment_native_v257 import raster as original_raster
from scripts.verify_shipyard_gameplay_v760 import independent_font
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/reinforcement_faction_prose_v1802')
ROM=Path('out/all_routes_combined_v1775_candidate.nds')
OLD=Path('translations/reinforcement_sniping_editorial_manuscript_v2.json')
NEW=Path('translations/reinforcement_sniping_editorial_manuscript_v3.json')
TEXT={1911:"Admiral! It looks like ships from %s will help us!",
    1912:"Admiral! Ships from %s are coming to help us!",
    1913:"Admiral! Looks like ships from %s are joining our side!",
    1914:"Admiral! It seems ships from %s will lend us a hand!",
    1915:"I hear ships from %s will fight alongside us too!",
    1916:"Admiral! It seems ships from %s are coming to our aid!"}

if __name__=='__main__':
    assert not ROOT.exists()and not NEW.exists();ROOT.mkdir(parents=True)
    image=NdsImage.open(ROM);arm=image.read_file('/__arm9__.bin');common=image.read_file('/COMMON/MESFILE.DK4')
    font=image.read_file('/GRP/KANJI.FNT');current=current_entries(common,arm)
    clean=NdsImage.open('work/clean.nds');jp=common_message_entries(clean.read_file('/COMMON/MESFILE.DK4'),clean.read_file('/__arm9__.bin'))
    before=read(OLD);doc=deepcopy(before)
    for key in('native_font_proof','native_font_proof_sha256','visual_review_proof','visual_review_proof_sha256',
               'reviewed_research_manuscript','reviewed_research_manuscript_sha256'):
        doc.pop(key,None)
    doc.update(status='successor-six-faction-paragraphs-source-prose-and-native-checked-not-integrated',
        current_ROM=str(ROM),current_ROM_sha256=sha(ROM.read_bytes()),current_COMMON_sha256=sha(common),current_ARM9_sha256=sha(arm),
        predecessor_manuscript=str(OLD),predecessor_manuscript_sha256=sha(OLD.read_bytes()),
        formatting_review_pending=True,registered_integration_pending=True,
        source_and_prose_coverage_added=0,completed_entries_added=0)
    for row in doc['records']:
        n=row['message_id'];assert row['source_hex']==jp[n].text.hex()
        row['current_reference']=reference(current[n]);row['current_text_hex']=current[n].text.hex()
        row['current_English']=current[n].text.decode('cp932')
        if n in TEXT:
            row['english']=TEXT[n]
            row['localization_note']=('The native faction substitution includes complete labels such as Bergstrom Fleet and Argot Co. '
                'Render the source fleet as ships from the named faction so English does not repeat a fleet from a Fleet. '
                'The original assistance,uncertainty or reported-speech tone and naval participants are preserved;no faction label is shortened. '
                'This is a collective reference to the original supporting fleet,not a change to its size or role.')
            row['review']['formatting']=False
        row['compiled_hex']=compiled(row).hex()
    class CurrentFont:
        @staticmethod
        def open(path):
            assert str(path)=='out/all_routes_combined_v255_candidate.nds'
            return image
    raster=FunctionType(original_raster.__code__,{**original_raster.__globals__,'NdsImage':CurrentFont},argdefs=original_raster.__defaults__)
    old_cases=read(before['native_font_proof'])['cases'];cpu=prepared(arm);cases=[];findings=[]
    for prior in old_cases:
        n=prior['message_ID']
        if n not in TEXT:continue
        row=next(r for r in doc['records']if r['message_id']==n);arg=bytes.fromhex(prior['argument_case']['hex'])
        value,lines=native_layout(cpu,compiled(row),n,arg,TABLES['reinforcement'])
        pixels=bytes(raster(arm,value,0x01FFCE40-0x02000000,size=(228,64),instruction_limit=2000000))
        assert pixels==bytes(independent_font(arm,font,lines))
        weak=[i for i,line in enumerate(lines[:-1])if line.split()[-1].strip('.,!?;:').lower()in{'a','an','the','to','of','with','for','from','on','in','as','at'}]
        short=len(lines)>1 and(len(lines[-1])<=8 or len(lines[-1].split())==1)
        path=ROOT/f'ID{n}_faction{prior["variant"]:02d}_complete_native.png'
        Image.frombytes('L',(228,64),bytes(0 if p else 255 for p in pixels)).save(path)
        case={'message_ID':n,'argument_case':prior['argument_case'],'formatted_hex':value.hex(),'lines':lines,
            'current_native_printf_wrap_ABI_guards_and_complete_native_independent_font_pass':True,
            'preview':str(path),'preview_sha256':sha(path.read_bytes()),'weak_line_end_indices':weak,'short_final_row':short}
        cases.append(case)
        if weak or short:findings.append(case)
    assert len(cases)==120
    selected=[]
    for n in TEXT:
        candidates=[r for r in cases if r['message_ID']==n]
        for c in(max(candidates,key=lambda r:len(r['formatted_hex'])),next(r for r in candidates if r['argument_case']['label']=='Argot Co.')):
            if c not in selected:selected.append(c)
    sheets=[]
    for start in range(0,len(selected),10):
        sheet=Image.new('RGB',(936,760),'#263238');draw=ImageDraw.Draw(sheet)
        for k,r in enumerate(selected[start:start+10]):
            x,y=468*(k%2),152*(k//2);draw.text((x+5,y+3),f"Draft ID{r['message_ID']} / {r['argument_case']['label']}",fill='white')
            sheet.paste(Image.open(r['preview']).resize((456,128),Image.Resampling.NEAREST),(x+5,y+22))
        path=ROOT/f'draft_review_sheet{start//10+1}.png';sheet.save(path);sheets.append({'path':str(path),'sha256':sha(path.read_bytes())})
    proof=ROOT/'six_paragraphs120_complete_native_cases.json'
    save(proof,{'candidate':str(ROM),'candidate_sha256':sha(ROM.read_bytes()),'old_manuscript_sha256':sha(OLD.read_bytes()),
        'changed_native_IDs':sorted(TEXT),'all120_cases':cases,'boundary_findings':findings,'review_sheets':sheets,
        'new_prose_not_integrated_or_gameplay_verified':True,'visual_review_pending':True,'full_goal_complete':False,
        'producer_sha256':sha(Path(__file__).read_bytes())})
    doc['successor_native_format_proof']=str(proof);doc['successor_native_format_proof_sha256']=sha(proof.read_bytes())
    save(NEW,doc)
    print({'six_successor_paragraphs':6,'complete_native_cases':120,'boundary_findings':len(findings),
        'not_integrated':True,'visual_review_pending':True},flush=True)
