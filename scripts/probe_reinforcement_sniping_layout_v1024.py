"""Full native argument and wrap matrix with exact CP932 commander bytes."""
import struct
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.native_call_abi_v764 import call
from scripts.probe_button_prompt_native import BASE,STACK
from scripts.verify_arrival_native_v792 import prepared
from scripts.reinforcement_sniping_layout_v1024 import compiled
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/reinforcement_sniping_v1024')
ROM=Path('out/all_routes_combined_v997_candidate.nds')
MANUSCRIPT=Path('translations/reinforcement_sniping_editorial_manuscript_v1.json')
TABLES={'reinforcement':0x021173E0,'covering_fire':0x021173C0,'admiral_shot':0x02117300}


def native_layout(cpu,text,n,argument,table):
    output,template,arg,wrapped=0x02420020,0x02420400,0x02420800,0x02420C20
    cpu.mem_write(output-16,b'\xA5'*288);cpu.mem_write(template,text+b'\0')
    if argument is not None:cpu.mem_write(arg,argument+b'\0')
    call(cpu,0xD7720,(output,template,arg,0),instruction_limit=2000000)
    expected=text.replace(b'%s',argument,1) if argument is not None else text
    assert bytes(cpu.mem_read(output,len(expected)+1))==expected+b'\0'
    assert bytes(cpu.mem_read(output-16,16))==b'\xA5'*16
    assert bytes(cpu.mem_read(output+len(expected)+1,271-len(expected)))==b'\xA5'*(271-len(expected))
    cpu.mem_write(wrapped-16,b'\xA5'*288)
    cpu.mem_write(STACK+0x264,struct.pack('<I',0x02053DB8))
    cpu.mem_write(STACK+0x274,struct.pack('<I',n))
    cpu.mem_write(STACK+0x27C,struct.pack('<I',table))
    call(cpu,0x01FFCF3C-BASE,(wrapped,output,0),instruction_limit=2000000)
    result=bytes(cpu.mem_read(wrapped,256)).split(b'\0')[0]
    assert bytes(cpu.mem_read(wrapped-16,16))==bytes(cpu.mem_read(wrapped+256,16))==b'\xA5'*16
    assert b' '.join(result.split())==b' '.join(expected.split())
    lines=[s.strip().decode('cp932') for s in result.split(b'\n')]
    assert 1<=len(lines)<=4 and all(len(s.encode('cp932'))<=35 for s in lines),(n,argument,lines)
    return result,lines


def arguments():
    context=read('work/analysis/reinforcement_sniping_v1022b/source_context_packet.json')
    supplement=read('work/analysis/reinforcement_sniping_v1023/compact_name_and_source_meaning_supplement.json')
    faction=[{'kind':'native-faction-label','company_ID':r['company_ID'],'label':r['name'],'hex':r['name_hex']}
             for r in context['all20_native_complete_company_labels']]
    names={}
    for r in context['all_nonnull63_fleet_commander_labels']:
        entry=names.setdefault(r['name_hex'],{'kind':'native-commander-label-or-regular-officer-stress','hex':r['name_hex'],
            'label':bytes.fromhex(r['name_hex']).decode('cp932'),'source_fleet_IDs':[],'additional_regular_officer_IDs':[]})
        entry['source_fleet_IDs'].append(r['fleet_ID'])
    for r in supplement['all208_native_compact_actor_labels'][:28]:
        entry=names.setdefault(r['name_hex'],{'kind':'native-commander-label-or-regular-officer-stress','hex':r['name_hex'],
            'label':r['native_compact_label'],'source_fleet_IDs':[],'additional_regular_officer_IDs':[]})
        entry['additional_regular_officer_IDs'].append(r['actor_ID'])
    variants=list(names.values())
    for value in ('A','ABCDEFGHIJKLMNOPQRSTUVW','Northern Compass Co.'):
        variants.append({'kind':'synthetic-short-long-parity-stress-not-real-name','label':value,'hex':value.encode('ascii').hex()})
    return faction,variants


def main():
    assert not ROOT.exists();ROOT.mkdir(parents=True)
    rom=NdsImage.open(ROM);arm=rom.read_file('/__arm9__.bin');doc=read(MANUSCRIPT)
    assert sha(ROM.read_bytes())==doc['current_ROM_sha256']
    faction,names=arguments();cases=[];findings=[]
    for row in doc['records']:
        n=row['message_id'];family=row['source_family'];values=faction if family=='reinforcement' else names if family=='covering_fire' else [None]
        for i,value in enumerate(values):
            cpu=prepared(arm);text=compiled(row)
            result,lines=native_layout(cpu,text,n,bytes.fromhex(value['hex']) if value else None,TABLES[family])
            weak=[j for j,line in enumerate(lines[:-1]) if line.split()[-1].strip('.,!?;:').lower() in {'a','an','the','to','of','with','for','from','on','in','as','at'}]
            short_tail=len(lines)>1 and (len(lines[-1])<=8 or len(lines[-1].split())==1)
            case={'message_ID':n,'source_family':family,'argument_case':value,'variant':i,
                'compiled_hex':text.hex(),'formatted_hex':result.hex(),'lines':lines,
                'native_cell_widths':[len(s.encode('cp932')) for s in lines],
                'complete_original_printf_wrap_ABI_and_scratch_guards_pass':True,
                'exact_original_argument_bytes_and_complete_words_preserved':True,
                'weak_line_end_indices':weak,'short_final_row':short_tail}
            cases.append(case)
            if weak or short_tail:findings.append({'case_index':len(cases)-1,**case})
        print(n,len(values),'original argument/wrap cases pass',flush=True)
    save(ROOT/'native_layout_matrix.json',{'candidate_sha256':sha(ROM.read_bytes()),'ARM9_sha256':sha(arm),
        'manuscript':str(MANUSCRIPT),'manuscript_sha256':sha(MANUSCRIPT.read_bytes()),
        'cases':cases,'all20_faction_variants':len(faction),'unique_commander_regular_officer_and_stress_variants':len(names),
        'findings_requiring_review':findings,'all_full_native_font_canvases_not_yet_proven':True,
        'native_runtime_not_modified':True,'source_prose_or_completion_credit_added':0,
        'producer_sha256':sha(Path(__file__).read_bytes()),'full_goal_complete':False})
    print(len(cases),'complete native layout cases;',len(findings),'boundary findings;full font and actual scenes pending.',flush=True)


if __name__=='__main__':main()
