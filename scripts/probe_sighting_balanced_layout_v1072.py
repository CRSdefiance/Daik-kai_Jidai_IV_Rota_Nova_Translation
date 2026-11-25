"""Original substitution/wrapping matrix with two bounded research memberships."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.sighting_runtime_v1071 import apply
from scripts.sighting_layout_v1069 import compiled
from scripts.probe_sighting_layout_v1070 import native_layout
from scripts.verify_arrival_native_v792 import prepared
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/sighting_layout_v1072')
ROM=Path('out/all_routes_combined_v1034_candidate.nds')


def main():
    assert not ROOT.exists()
    rom=NdsImage.open(ROM);arm,plan=apply(rom.read_file('/__arm9__.bin'))
    original=read('work/analysis/sighting_layout_v1070/native_layout_matrix.json')
    doc=read(original['manuscript']);assert sha(Path(original['manuscript']).read_bytes())==original['manuscript_sha256']
    rows={r['message_id']:r for r in doc['records']};cpu=prepared(arm)
    cases=[];findings=[]
    for i,old in enumerate(original['cases']):
        text=compiled(rows[old['message_ID']]);assert text.hex()==old['compiled_hex']
        value,lines=native_layout(cpu,text,old['message_ID'],bytes.fromhex(old['bearing']['hex']),bytes.fromhex(old['faction_hex']))
        weak=[i for i,line in enumerate(lines[:-1]) if line.split()[-1].strip('.,!?;:').lower() in {'a','an','the','to','of','with','for','from','on','in','as','at'}]
        short=len(lines)>1 and (len(lines[-1])<=8 or len(lines[-1].split())==1)
        case={**old,'formatted_hex':value.hex(),'lines':lines,'native_cell_widths':[len(s.encode('cp932')) for s in lines],
            'weak_line_end_indices':weak,'short_final_row':short,'research_two_table_balancing_membership':True}
        cases.append(case)
        if weak or short:findings.append({'case_index':i,**case})
    assert len(cases)==2700
    ROOT.mkdir(parents=True);research=ROOT/'ARM9_RUNTIME_RESEARCH_ONLY.bin';research.write_bytes(arm)
    save(ROOT/'native_layout_matrix.json',{'candidate':str(ROM),'candidate_sha256':sha(ROM.read_bytes()),
        'research_ARM9':str(research),'research_ARM9_sha256':sha(arm),'runtime_plan':plan,
        'source_matrix':'work/analysis/sighting_layout_v1070/native_layout_matrix.json',
        'source_matrix_sha256':sha(Path('work/analysis/sighting_layout_v1070/native_layout_matrix.json').read_bytes()),
        'manuscript':original['manuscript'],'manuscript_sha256':original['manuscript_sha256'],
        'cases':cases,'findings_requiring_review':findings,'complete_native_fonts_actual_and_registered_integration_pending':True,
        'no_new_ROM_or_live_RAM_change':True,'completed_entries_added':0,'producer_sha256':sha(Path(__file__).read_bytes()),'full_goal_complete':False})
    print('2700 native balanced-layout cases;',len(findings),'boundary findings. Full runtime regressions and fonts remain pending.',flush=True)


if __name__=='__main__':main()
