"""Native two-argument expansion/wrapping matrix; no ROM or approved font gate."""
from copy import deepcopy
from pathlib import Path
import struct
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.native_call_abi_v764 import call
from scripts.probe_button_prompt_native import BASE,STACK
from scripts.verify_arrival_native_v792 import prepared
from scripts.sighting_layout_v1069 import compiled,PROFILE
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/sighting_layout_v1070')
SOURCE=Path('translations/sighting_editorial_manuscript_v1.json')
MANUSCRIPT=Path('translations/sighting_editorial_manuscript_v2.json')
ROM=Path('out/all_routes_combined_v1034_candidate.nds')


def native_layout(cpu,text,n,direction,faction):
    out,t,a,b,w=0x02420020,0x02420400,0x02420800,0x02420900,0x02420C20
    cpu.mem_write(out-16,b'\xA5'*288);cpu.mem_write(w-16,b'\xA5'*288)
    for at,value in ((t,text),(a,direction),(b,faction)):cpu.mem_write(at,value+b'\0')
    call(cpu,0xD7720,(out,t,a,b),instruction_limit=2000000)
    expected=text.replace(b'%s',direction,1).replace(b'%s',faction,1)
    assert len(expected)<256 and bytes(cpu.mem_read(out,len(expected)+1))==expected+b'\0'
    assert bytes(cpu.mem_read(out-16,16))==b'\xA5'*16
    assert bytes(cpu.mem_read(out+len(expected)+1,271-len(expected)))==b'\xA5'*(271-len(expected))
    assert b'..' not in expected
    cpu.mem_write(STACK+0x264,struct.pack('<I',0x02053DB8))
    cpu.mem_write(STACK+0x274,struct.pack('<I',n))
    table=0x02118560 if n<622 else 0x02118540
    cpu.mem_write(STACK+0x27C,struct.pack('<I',table))
    call(cpu,0x01FFCF3C-BASE,(w,out,0),instruction_limit=2000000)
    result=bytes(cpu.mem_read(w,256)).split(b'\0')[0]
    assert bytes(cpu.mem_read(w-16,16))==bytes(cpu.mem_read(w+256,16))==b'\xA5'*16
    assert b' '.join(result.split())==b' '.join(expected.split())
    lines=[s.strip().decode('cp932') for s in result.split(b'\n')]
    assert 1<=len(lines)<=4 and all(len(s.encode('cp932'))<=35 for s in lines)
    return result,lines


def main():
    assert not ROOT.exists() and not MANUSCRIPT.exists()
    doc=read(SOURCE);assert len(doc['records'])==15
    before=deepcopy(doc);row=next(r for r in doc['records'] if r['message_id']==614)
    assert row['english']=="Fleet spotted in the %s! It belongs to %s. Battle stations!"
    row['english']="Fleet spotted in the %s! It belongs to %s! Battle stations!"
    row['localization_note']+=' Native complete-faction substitution caught a doubled period after labels ending in Co.;use the already appropriate exclamation instead,without altering the name bytes or the source meaning.'
    doc['consumer_layout_profile']=PROFILE
    doc['supersedes_manuscript']=str(SOURCE);doc['supersedes_manuscript_sha256']=sha(SOURCE.read_bytes())
    rom=NdsImage.open(ROM);arm=rom.read_file('/__arm9__.bin')
    assert sha(ROM.read_bytes())==doc['current_ROM_sha256']
    context=read('work/analysis/sighting_editorial_v1065/source_context_packet.json')
    provider=read('work/analysis/sighting_provider_v1068/provider_native_proof.json')
    assert sha(arm)==provider['source_ARM9_sha256']
    directions=[{'label':'vicinity','hex':b'vicinity'.hex(),'kind':'source-reviewed-unintegrated-close-range-provider'}]
    directions += [{'label':r['text'],'hex':r['hex'],'kind':'native-compass-label'} for r in context['original_bearing_getter_cases'][1:]]
    factions=read('work/analysis/reinforcement_sniping_v1022b/source_context_packet.json')['all20_native_complete_company_labels']
    cpu=prepared(arm);cases=[];findings=[]
    for row in doc['records']:
        n=row['message_id'];text=compiled(row)
        for direction in directions:
            for faction in factions:
                result,lines=native_layout(cpu,text,n,bytes.fromhex(direction['hex']),bytes.fromhex(faction['name_hex']))
                weak=[i for i,line in enumerate(lines[:-1]) if line.split()[-1].strip('.,!?;:').lower() in {'a','an','the','to','of','with','for','from','on','in','as','at'}]
                short=len(lines)>1 and (len(lines[-1])<=8 or len(lines[-1].split())==1)
                case={'message_ID':n,'compiled_hex':text.hex(),'bearing':direction,'faction_ID':faction['company_ID'],
                    'faction_hex':faction['name_hex'],'formatted_hex':result.hex(),'lines':lines,
                    'native_cell_widths':[len(s.encode('cp932')) for s in lines],
                    'original_printf_and_current_native_wrapper_ABI_and_guards_pass':True,
                    'weak_line_end_indices':weak,'short_final_row':short}
                cases.append(case)
                if weak or short:findings.append({'case_index':len(cases)-1,**case})
        print(n,'180 native two-argument wrap cases pass',flush=True)
    assert len(cases)==2700 and all(not r['review']['formatting'] for r in doc['records'])
    ROOT.mkdir(parents=True);save(MANUSCRIPT,doc)
    save(ROOT/'native_layout_matrix.json',{'candidate':str(ROM),'candidate_sha256':sha(ROM.read_bytes()),
        'ARM9_sha256':sha(arm),'manuscript':str(MANUSCRIPT),'manuscript_sha256':sha(MANUSCRIPT.read_bytes()),
        'cases':cases,'all_nine_relative_bearing_classes_and20_native_faction_labels':True,
        'findings_requiring_review':findings,'complete_native_fonts_and_actual_display_pending':True,
        'provider_not_integrated':True,'no_ROM_or_live_RAM_change':True,'completed_entries_added':0,
        'producer_sha256':sha(Path(__file__).read_bytes()),'full_goal_complete':False})
    ledger_path=Path('translations/editorial_review_current_v1.json');ledger=read(ledger_path)
    assert ledger['records_editorially_completed']==1196 and ledger['records_with_source_and_prose_pass']==1234
    paths=ledger['active_source_prose_drafts']['manuscripts'];assert paths.count(str(SOURCE))==1
    paths[paths.index(str(SOURCE))]=str(MANUSCRIPT)
    ledger['newly_observed_sighting_followup'].update(manuscript=str(MANUSCRIPT),native_layout_matrix=str(ROOT/'native_layout_matrix.json'),
        pending_boundary_findings=len(findings),status='source-prose-and2700-native-expansion-wrap-cases;boundary-fonts-provider-integration-actual-pending')
    ledger['sighting_v1066']['current_manuscript']=str(MANUSCRIPT)
    save(ledger_path,ledger)
    print('2700 native expansion/wrap cases;',len(findings),'boundary findings. Complete fonts/provider integration/actual scenes still pending.',flush=True)


if __name__=='__main__':main()
