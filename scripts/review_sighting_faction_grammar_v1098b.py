"""Faithful attributive faction names;source/prose draft and complete wrap matrix."""
from dataclasses import asdict
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import common_message_entries
from dk4tool.patch.sighting_editorial import current_entries
from dk4tool.patch.grand_race_menu_release import sha
from scripts.sighting_layout_v1069 import compiled
from scripts.probe_sighting_layout_v1070 import native_layout
from scripts.verify_arrival_native_v792 import prepared
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/sighting_grammar_v1098b')
SOURCE=Path('translations/sighting_editorial_manuscript_v7.json')
MANUSCRIPT=Path('translations/sighting_editorial_manuscript_v8.json')
ROM=Path('out/all_routes_combined_v1086_candidate.nds')
TEXT={
614:"Fleet spotted in the %s! Those are %s ships! We're getting ready for battle!",
615:"Spotted a fleet in the %s! Those are %s ships! We're getting ready to fight!",
616:"There's a fleet in the %s! Those are %s ships! Get ready for battle!",
617:"There's a fleet in the %s! Those are %s ships! We're getting ready for battle!",
618:"We've got company in the %s! Those are %s ships! Let's get ready for a fight!",
619:"Spotted a fleet in the %s! Those are %s ships! Prepare for battle!",
620:"I found a fleet in the %s! Those are %s ships! Time to fight!",
621:"Fleet spotted in the %s! Those are %s ships! We're getting ready for battle!",
622:"Fleet spotted in the %s! Those are %s ships, and they're attacking us!",
623:"There's a fleet in the %s! Those are %s ships, and they're attacking us!",
624:"Look! A fleet in the %s! Those are %s ships, and they're attacking us!",
625:"Fleet in the %s! Those are %s ships, and they've picked a fight with us!",
626:"A fleet in the %s! Those are %s ships, and they've launched an attack!",
627:"Whoa! A fleet in the %s is attacking us! Those are %s ships!",
628:"A fleet in the %s! Those are %s ships, and they've launched an attack!"}


def main():
    assert not ROOT.exists() and not MANUSCRIPT.exists()
    rom=NdsImage.open(ROM);arm=rom.read_file('/__arm9__.bin');common=rom.read_file('/COMMON/MESFILE.DK4')
    assert sha(ROM.read_bytes())=='df958b7289743e8eca79c9a6a216e134c9a2590321597f7bead15111ee8d748f'
    clean_path=Path('work/clean.nds');clean=NdsImage.open(clean_path)
    assert sha(clean_path.read_bytes())=='f4f07c975cc293f5b2ba469747693d3dd37f2e6dfc408cf5910adf5e83d9177d'
    originals=common_message_entries(clean.read_file('/COMMON/MESFILE.DK4'),clean.read_file('/__arm9__.bin'))
    current=current_entries(common,arm);doc=read(SOURCE);reviews=[]
    for row in doc['records']:
        n=row['message_id'];assert originals[n].text.hex()==row['source_hex']
        assert current[n].text==compiled(row)
        old=row['english'];row['english']=TEXT[n]
        row['current_reference']={k:v for k,v in asdict(current[n]).items() if k!='text'}
        row['current_text_hex']=current[n].text.hex();row['current_English']=current[n].text.decode('ascii')
        row['localization_note']=row['localization_note'].split(' Native approval:')[0]+(
            ' Faction grammar review:use the unchanged faction name attributively in Those are %s ships. '
            'This is natural with Li Clan,Hayreddin Clan,Bergstrom Fleet,company names and surname faction labels. '
            'The first clause still explicitly reports a fleet;the follow-up identifies its ships without adding flags,colors,ship class or battle outcomes. '
            'Preserve the voice-specific readiness or already-attacked claim and bearing-first/faction-second source order. '
            'Read aloud against clean Japanese and all20 established complete labels. Earlier V7 font/gameplay evidence does not approve the changed wording;new complete font and integrated scene checks are required.')
        row['review']['formatting']=False
        row['compiled_hex']=compiled(row).hex()
        reviews.append({'message_ID':n,'source_Japanese':row['source_Japanese'],'source_meaning':row['source_meaning'],
            'previous_English':old,'proposed_English':row['english'],
            'source_context_faithfulness_voice_and_naturalness_reviewed':True,'formatting_and_release_not_approved':True})
    prior_evidence={}
    for key in ('native_font_proof','native_font_proof_sha256','native_runtime_proof','native_runtime_proof_sha256',
                'visual_review','visual_review_sha256','native_label_records','native_label_proof','native_label_proof_sha256'):
        if key in doc:prior_evidence[key]=doc.pop(key)
    doc.update(supersedes_manuscript=str(SOURCE),supersedes_manuscript_sha256=sha(SOURCE.read_bytes()),
        current_ROM=str(ROM),current_ROM_sha256=sha(ROM.read_bytes()),current_COMMON_sha256=sha(common),current_ARM9_sha256=sha(arm),
        previous_wording_native_and_label_evidence=prior_evidence,preserved_native_labels_not_to_reapply=['vicinity','Armed Latina'],
        formatting_review_pending=True,status='15-faction-grammar-source-prose-revised;new-fonts-registered-release-and-actual-pending')
    ROOT.mkdir(parents=True);save(MANUSCRIPT,doc)
    source_matrix_path=Path('work/analysis/sighting_layout_v1079/native_layout_matrix.json')
    source_matrix=read(source_matrix_path);rows={r['message_id']:r for r in doc['records']}
    cpu=prepared(arm);cases=[];findings=[]
    for index,old in enumerate(source_matrix['cases']):
        n=old['message_ID'];text=compiled(rows[n]);bearing=bytes.fromhex(old['bearing']['hex']);faction=bytes.fromhex(old['faction_hex'])
        value,lines=native_layout(cpu,text,n,bearing,faction)
        weak=[i for i,line in enumerate(lines[:-1]) if line.split()[-1].strip('.,!?;:').lower() in {'a','an','the','to','of','with','for','from','on','in','as','at'}]
        short=len(lines)>1 and (len(lines[-1])<=8 or len(lines[-1].split())==1)
        case={**old,'compiled_hex':text.hex(),'formatted_hex':value.hex(),'lines':lines,
            'native_cell_widths':[len(line.encode('cp932')) for line in lines],
            'weak_line_end_indices':weak,'short_final_row':short}
        cases.append(case)
        if weak or short:findings.append({'case_index':index,**case})
        if (index+1)%180==0:print(n,'all180 current-ROM native wrap cases checked',flush=True)
    assert len(cases)==2700
    matrix_path=ROOT/'native_layout_matrix.json'
    save(matrix_path,{'candidate':str(ROM),'candidate_sha256':sha(ROM.read_bytes()),'ARM9_sha256':sha(arm),
        'manuscript':str(MANUSCRIPT),'manuscript_sha256':sha(MANUSCRIPT.read_bytes()),
        'source_matrix':str(source_matrix_path),'source_matrix_sha256':sha(source_matrix_path.read_bytes()),
        'cases':cases,'findings_requiring_review':findings,
        'all15_current_original_printf_and_wrap_guards_and_complete_words_within35x4':True,
        'complete_font_visual_review_release_patch_and_actual_scenes_pending':True,'completed_entries_added':0,
        'producer_sha256':sha(Path(__file__).read_bytes()),'full_goal_complete':False})
    save(ROOT/'source_and_grammar_review.json',{'records':reviews,
        'all15_exact_source_records_rechecked_in_clean_ROM':True,'all20_complete_faction_names_retained':True,
        'prior_finding_examples':['It belongs to Li Clan','It is from Bergstrom Fleet'],
        'new_phrase_examples':['Those are Li Clan ships!','Those are Bergstrom Fleet ships!','Those are Centurione Co. ships!'],
        'no_runtime_article_injection_or_name_changes':True,'no_ROM_build_or_new_gameplay_credit':True})
    ledger_path=Path('translations/editorial_review_current_v1.json');ledger=read(ledger_path)
    assert ledger['records_editorially_completed']==1196 and ledger['records_with_source_and_prose_pass']==1234
    paths=ledger['active_source_prose_drafts']['manuscripts'];assert paths.count(str(SOURCE))==1
    paths[paths.index(str(SOURCE))]=str(MANUSCRIPT)
    ledger['newly_observed_sighting_followup'].update(manuscript=str(MANUSCRIPT),native_layout_matrix=str(matrix_path),
        pending_boundary_findings=len(findings),status='V8-faction-grammar-revision;2700-current-ROM-wrap-cases;new-fonts-release-actual-pending',completed_entries_added=0)
    ledger['sighting_v1066']['current_manuscript']=str(MANUSCRIPT)
    ledger['sighting_faction_grammar_v1098']={'manuscript':str(MANUSCRIPT),'source_review':str(ROOT/'source_and_grammar_review.json'),
        'native_layout_matrix':str(matrix_path),'boundary_findings':len(findings),
        'V1086_preserves_previous_wording_new_draft_not_integrated':True,'completed_entries_added':0,'full_goal_complete':False}
    ledger['active_source_prose_drafts']['status']='older750-752-context-pending;shot-pending;15-sighting-V8-grammar-fonts-release-actual-pending'
    checkpoint=('V1098 rechecks all15 exact clean sighting records and revises faction ownership clauses to attributive ships,avoiding awkward articleless clan/fleet substitutions while preserving all20 names,source meaning,voice and both argument positions. All2700 current-V1086 native printf/wrap cases preserve complete words and35x4 bounds;'+str(len(findings))+' boundary findings require review. The new V8 draft is not integrated;complete native fonts,visual review,registered exact patch and actual changed wording remain pending. V1097 build/gameplay checkpoint remains the latest integrated evidence.1196 complete,1234 source/prose;no completion credit and full goal active.')
    ledger['latest_checkpoint']=checkpoint;save(ledger_path,ledger)
    for filename in ('docs/translation_progress.md','docs/todo.md'):
        with Path(filename).open('a',encoding='utf-8') as stream:stream.write('\n\n## V1098: faction grammar review\n\n'+checkpoint+'\n')
    print(checkpoint,flush=True)


if __name__=='__main__':main()
