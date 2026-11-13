"""Keep source battle-readiness statements as full English; recheck native wrapping."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.sighting_layout_v1069 import compiled
from scripts.probe_sighting_layout_v1070 import native_layout
from scripts.verify_arrival_native_v792 import prepared
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/sighting_layout_v1074')
SOURCE=Path('translations/sighting_editorial_manuscript_v3.json')
MANUSCRIPT=Path('translations/sighting_editorial_manuscript_v4.json')
TEXT={618:"We've got company in the %s! It's a fleet from %s! Let's get ready for a fight!"}


def main():
    assert not ROOT.exists() and not MANUSCRIPT.exists()
    doc=read(SOURCE);source_matrix=Path('work/analysis/sighting_layout_v1073/native_layout_matrix.json')
    matrix=read(source_matrix);assert matrix['manuscript_sha256']==sha(SOURCE.read_bytes())
    for row in doc['records']:
        if row['message_id'] in TEXT:
            row['english']=TEXT[row['message_id']]
            row['localization_note']+=' Use the complete spoken sentence Its a fleet from the named faction rather than a detached noun fragment. The unwelcome-company reaction and call to readiness preserve the original rough voice. This lengthens the prose without adding facts. Native weak-word scanning was separately found to treat uppercase A differently;keep that general formatter issue in the open watchlist rather than claiming a global repair.'
    doc['supersedes_manuscript']=str(SOURCE);doc['supersedes_manuscript_sha256']=sha(SOURCE.read_bytes())
    arm_path=Path(matrix['research_ARM9']);arm=arm_path.read_bytes();assert sha(arm)==matrix['research_ARM9_sha256']
    cpu=prepared(arm);rows={r['message_id']:r for r in doc['records']};cases=[];findings=[]
    for i,old in enumerate(matrix['cases']):
        text=compiled(rows[old['message_ID']])
        value,lines=native_layout(cpu,text,old['message_ID'],bytes.fromhex(old['bearing']['hex']),bytes.fromhex(old['faction_hex']))
        weak=[i for i,line in enumerate(lines[:-1]) if line.split()[-1].strip('.,!?;:').lower() in {'a','an','the','to','of','with','for','from','on','in','as','at'}]
        short=len(lines)>1 and (len(lines[-1])<=8 or len(lines[-1].split())==1)
        case={**old,'compiled_hex':text.hex(),'formatted_hex':value.hex(),'lines':lines,
            'native_cell_widths':[len(s.encode('cp932')) for s in lines],
            'weak_line_end_indices':weak,'short_final_row':short}
        cases.append(case)
        if weak or short:findings.append({'case_index':i,**case})
    assert len(cases)==2700 and all(not r['review']['formatting'] for r in doc['records'])
    ROOT.mkdir(parents=True);save(MANUSCRIPT,doc)
    save(ROOT/'native_layout_matrix.json',{'candidate':matrix['candidate'],'candidate_sha256':matrix['candidate_sha256'],
        'research_ARM9':str(arm_path),'research_ARM9_sha256':sha(arm),'runtime_plan':matrix['runtime_plan'],
        'source_matrix':str(source_matrix),'source_matrix_sha256':sha(source_matrix.read_bytes()),
        'manuscript':str(MANUSCRIPT),'manuscript_sha256':sha(MANUSCRIPT.read_bytes()),'cases':cases,
        'findings_requiring_review':findings,'all15_full_native_fonts_and_registered_provider_integration_actual_pending':True,
        'no_new_ROM_or_live_RAM_change':True,'completed_entries_added':0,'producer_sha256':sha(Path(__file__).read_bytes()),'full_goal_complete':False})
    ledger_path=Path('translations/editorial_review_current_v1.json');ledger=read(ledger_path)
    assert ledger['records_editorially_completed']==1196 and ledger['records_with_source_and_prose_pass']==1234
    paths=ledger['active_source_prose_drafts']['manuscripts'];assert paths.count(str(SOURCE))==1
    paths[paths.index(str(SOURCE))]=str(MANUSCRIPT)
    ledger['newly_observed_sighting_followup'].update(manuscript=str(MANUSCRIPT),native_layout_matrix=str(ROOT/'native_layout_matrix.json'),
        pending_boundary_findings=len(findings),status='source-prose-and2700-research-balanced-layout-cases;runtime-regressions-fonts-provider-release-actual-pending')
    ledger['sighting_v1066']['current_manuscript']=str(MANUSCRIPT)
    ledger['formatting_watchlist']['native_uppercase_weak_word_followup']={'evidence':'work/analysis/sighting_layout_v1073/native_layout_matrix.json','example_ID':618,'finding':'Original weak-word hash comparison is case-sensitive;uppercase A may remain at a line end. Current draft uses a complete natural sentence,but the general formatter audit stays open.','status':'open-source-bound-high-level-formatter-followup;not-globally-fixed'}
    save(ledger_path,ledger)
    print('2700 full readiness/sighting native cases;',len(findings),'boundary findings. All formatting gates remain open.',flush=True)


if __name__=='__main__':main()
