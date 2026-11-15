"""Approve only the new native grammar draft;archive without integration credit."""
from pathlib import Path
from shutil import copy2
from dk4tool.patch.grand_race_menu_release import sha
from scripts.sighting_layout_v1069 import compiled
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/sighting_grammar_review_v1100')
SOURCE=Path('translations/sighting_editorial_manuscript_v8.json')
MANUSCRIPT=Path('translations/sighting_editorial_manuscript_v9.json')
FONT=Path('work/analysis/sighting_fonts_v1099/native_font_proof.json')
ARCHIVE=Path('E:/Rota Nova translations/Editorial review/V1100 Sighting grammar native review')
GENERATED=Path('E:/Rota Nova translations/Generated')


def main():
    assert not ROOT.exists() and not MANUSCRIPT.exists() and not ARCHIVE.exists()
    font=read(FONT);matrix=read(font['matrix']);doc=read(SOURCE)
    assert font['complete_native_font_cases']==2700 and len(font['cases'])==2700
    assert sha(Path(font['matrix']).read_bytes())==font['matrix_sha256']
    assert matrix['manuscript_sha256']==sha(SOURCE.read_bytes()) and not matrix['findings_requiring_review']
    assert font['current_ROM_ARM9_sha256']==matrix['ARM9_sha256']==doc['current_ARM9_sha256']
    assert font['candidate_sha256']==doc['current_ROM_sha256']=='df958b7289743e8eca79c9a6a216e134c9a2590321597f7bead15111ee8d748f'
    rows={r['message_id']:r for r in doc['records']}
    assert set(rows)==set(range(614,629))
    for case in font['cases']:
        assert case['compiled_hex']==compiled(rows[case['message_ID']]).hex()
        assert case['whole228x64_native_and_independent_font_match']
        assert case['complete_leading_trailing_letters_and_uniform_native_margin']
        assert not case['weak_line_end_indices'] and not case['short_final_row']
    for sheet in font['review_sheets']:assert sha(Path(sheet['path']).read_bytes())==sheet['sha256']
    unsafe=[];exemplar=rows[614]
    for english in (' '+exemplar['english'],exemplar['english']+' ',exemplar['english'].replace(' ','  ',1),
        exemplar['english'].replace(' ','\n',1),exemplar['english'].replace(' ','\r',1),
        exemplar['english'].replace(' ','\t',1),exemplar['english']+'{PAD}',exemplar['english']+'é',
        exemplar['english'].replace('%s','%d',1),exemplar['english']+' %s',exemplar['english']+' %',
        exemplar['english'].replace('%s','IC',1)):
        try:compiled({**exemplar,'english':english})
        except ValueError:unsafe.append({'english':english,'rejected':True})
        else:raise AssertionError('Unsafe native paragraph accepted')
    for patch in ({'message_id':613},{'source_family':'fleet-sighting-under-attack'},{'native_argument_count':1}):
        try:compiled({**exemplar,**patch})
        except ValueError:unsafe.append({'invalid_fields':patch,'rejected':True})
        else:raise AssertionError('Wrong source contract accepted')
    assert len(unsafe)==15 and all(not r['review']['formatting'] for r in doc['records'])
    ROOT.mkdir(parents=True);visual=ROOT/'visual_and_compiler_review.json'
    save(visual,{'source_manuscript':str(SOURCE),'source_manuscript_sha256':sha(SOURCE.read_bytes()),
        'complete_native_font_proof':str(FONT),'complete_native_font_proof_sha256':sha(FONT.read_bytes()),
        'all_current_review_sheets_visually_inspected':font['review_sheets'],
        'all15_source_meaning_voice_and_complete20_faction_substitutions_read_aloud':True,
        'attributive_Clan_Fleet_company_and_personal_faction_names_reviewed':True,
        'complete_initial_I620_first_and_final_letters_uniform_margins_and_bounds_reviewed':True,
        '15_invalid_source_control_printf_and_alignment_inputs_rejected':unsafe,
        'no_registered_new_wording_or_actual_new_wording_scene_approval':True,
        'previous_V1086_614_actual_capture_contains_previous_wording':True,
        'global_uppercase_weak_word_case_sensitivity_still_open':True,'producer_sha256':sha(Path(__file__).read_bytes())})
    for row in doc['records']:
        row['review']['formatting']=True
        row['localization_note']+=' Current V8 wording now passes2700 current-ROM printf/wrap/full-font cases,all review sheets and15 invalid compiler controls. New registered insertion,exact patch and changed-wording gameplay are still required;V1086 actual captures contain the previous V7 wording.'
    doc.update(supersedes_manuscript=str(SOURCE),supersedes_manuscript_sha256=sha(SOURCE.read_bytes()),
        formatting_review_pending=False,status='15-faction-grammar-native-approved;new-registered-integration-and-actual-pending',
        native_font_proof=str(FONT),native_font_proof_sha256=sha(FONT.read_bytes()),
        visual_review=str(visual),visual_review_sha256=sha(visual.read_bytes()))
    save(MANUSCRIPT,doc)
    ledger_path=Path('translations/editorial_review_current_v1.json');ledger=read(ledger_path)
    assert ledger['records_editorially_completed']==1196 and ledger['records_with_source_and_prose_pass']==1234
    paths=ledger['active_source_prose_drafts']['manuscripts'];assert paths.count(str(SOURCE))==1
    paths[paths.index(str(SOURCE))]=str(MANUSCRIPT)
    ledger['newly_observed_sighting_followup'].update(manuscript=str(MANUSCRIPT),native_font_proof=str(FONT),
        visual_review=str(visual),pending_boundary_findings=0,status='V9-faction-grammar-native-approved;new-release-actual-pending',completed_entries_added=0)
    ledger['sighting_v1066']['current_manuscript']=str(MANUSCRIPT)
    ledger['sighting_faction_grammar_v1098'].update(manuscript=str(MANUSCRIPT),complete_native_font_proof=str(FONT),
        status='15-native-approved;registered-and-actual-new-wording-pending')
    ledger['active_source_prose_drafts']['status']='older750-752-context-pending;shot-pending;15-sighting-V9-native-approved-new-release-actual-pending'
    summary=('V1100 native-approves the15 faction-grammar sighting revisions after all2700 complete current-ROM printf/wrap/font cases,zero boundary findings,all review sheets and15 invalid compiler controls. Attributive faction ships preserves every approved name without awkward articleless Clan/Fleet phrases or adding flags/class/outcome facts. V9 is a draft for a new registered layer;V1086 remains the last combined candidate and its actual614 capture contains previous wording. V1097 integrated/startup/compass/negative-pilot evidence is preserved. The next33 duel alternatives have1040 original voice selections and explicit separate duel/speech consumers;no prose-review credit. Source literal ED6C proves alternate1973-1979 Admiral variants for captain IDs0..3;the V1101 guessed2512 table note is corrected by V1102.1196 complete,1234 source/prose;no new completion credit. Full shared/routes/raw-source review,close/incoming/name UI,successful-shot event,global formatting and separate graphics audit remain open.')
    ledger['latest_checkpoint']=summary
    ledger['sighting_grammar_v1100']={'manuscript':str(MANUSCRIPT),'native_font_proof':str(FONT),'visual_review':str(visual),
        'new_ROM_or_patch_built':False,'completed_entries_added':0,'full_goal_complete':False}
    save(ledger_path,ledger)
    doc_path=Path('docs/sighting_grammar_v1100_native_checkpoint.md')
    doc_path.write_text('# V1100: faction grammar native approval\n\n'+summary+
        '\n\nThe new paragraphs retain the fleet sighting,bearing,full faction identity and voice-specific battle readiness/already-attacked meaning. The clan,fleet and company names are unchanged. Every paragraph remains one logical input before macro expansion. Complete font planes include the leading ASCII I in620 and every trailing letter;all margins and35x4 bounds pass. No new prose is integrated into V1086 by this review.\n\nThe separate original duel consumer0200D458 selects its actor from controller side0/1 and formats through020CE898 before0200DA28. It must receive its own mapped display audit rather than inherit shared speech wrapping. Original post-duel actor predicate0207EF28 returns0 only for captain IDs0..3,which receive Admiral variants1973..1979 without a name argument;other IDs receive named1951..1956. The current33-entry inventory has no source/prose completion credit. Earlier source-table guesses remain preserved with an explicit correction.\n',encoding='utf-8')
    for filename in ('docs/translation_progress.md','docs/todo.md'):
        with Path(filename).open('a',encoding='utf-8') as stream:stream.write('\n\n## V1100: sighting grammar native review\n\n'+summary+'\n')
    with Path('docs/known_issues.md').open('a',encoding='utf-8') as stream:
        stream.write('\n\n## V1100: faction grammar and next duel consumers\n\nV1086 sighting substitutions such as belongs to Li Clan sound awkward. V9 drafts use unchanged faction names attributively and pass2700 complete native font/wrap cases;registered insertion and actual revised scenes remain pending. No generic article injection or name changes were made. Original duel1931-1950 uses0200D458/020CE898/0200DA28;post-defeat cover uses original53F0C speech. The V1101 note guessed2512 for an alternate table;V1102 reads literal0200ED6C and proves02117620 /1973-1979 Admiral alternatives for captain IDs0..3. No ROM was affected by the note. Source/prose review of33 duel alternatives remains pending. See sighting_grammar_v1100_native_checkpoint.md.\n')
    ARCHIVE.mkdir(parents=True);files=[]
    sources=[Path(__file__),SOURCE,MANUSCRIPT,ledger_path,doc_path,
        Path('scripts/review_sighting_faction_grammar_v1098.py'),Path('scripts/review_sighting_faction_grammar_v1098b.py'),
        Path('scripts/prepare_sighting_grammar_v1098b.py'),Path('scripts/prepare_sighting_font_recheck_v1099.py'),
        Path('scripts/probe_sighting_fonts_v1099.py'),Path('scripts/research_duel_voice_context_v1101.py'),
        Path('scripts/research_duel_escape_context_v1102.py'),Path('docs/translation_progress.md'),Path('docs/todo.md'),Path('docs/known_issues.md')]
    for folder in ('sighting_grammar_v1098b','sighting_fonts_v1099','duel_source_v1101','duel_source_v1102','sighting_grammar_review_v1100'):
        sources+=list(Path('work/analysis',folder).rglob('*'))
    seen=set()
    for source in sources:
        if not source.is_file() or source.absolute() in seen:continue
        seen.add(source.absolute());relative=(source.absolute().relative_to(Path.cwd()) if source.absolute().is_relative_to(Path.cwd()) else
            Path('Generated')/source.absolute().relative_to(GENERATED))
        target=ARCHIVE/relative;target.parent.mkdir(parents=True,exist_ok=True);copy2(source,target)
        assert sha(source.read_bytes())==sha(target.read_bytes())
        files.append({'source':str(source),'archived':str(target),'sha256':sha(target.read_bytes())})
    save(ARCHIVE/'archive_manifest.json',{'files':files,'all_hashes_verified':True,'no_ROM_or_new_completed_entry_credit':True,'full_goal_complete':False})
    save(ROOT/'archive_receipt.json',{'archive':str(ARCHIVE),'files':len(files),'manifest_sha256':sha((ARCHIVE/'archive_manifest.json').read_bytes())})
    print('V1100:15 grammar drafts native-approved;2700 fonts and next33 source inventory archived. No new ROM or completion credit;goal active.',flush=True)


if __name__=='__main__':main()
