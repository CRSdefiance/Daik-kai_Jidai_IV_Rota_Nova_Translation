"""Record the completed332-page visual pass and exact scoped phrase/page refinements."""
from copy import deepcopy
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load,save

ROOT=Path('work/analysis/Rafael_B81_B84_formatting_20261105')
DOC=ROOT/'native_ready_subset_v1/manuscript.json'
NATIVE=ROOT/'native_subset_v2/compiled_native_pages.json'

if __name__=='__main__':
    output=ROOT/'preferences_v3.json';assert not output.exists()
    doc,native=map(load,[DOC,NATIVE]);byid={r['id']:r for r in doc['records']}
    assert native['pages']==332 and len(native['records'])==323 and len(native['review_sheets'])==30
    assert native['all_first_internal_final_glyph_codes_pixels_input_canaries_andbounds_pass']
    assert native['complete_consumption_andpagination_exact'] and native['fresh_compiled_alignments']==1292
    for sheet in native['review_sheets']:assert sha(Path(sheet['path']).read_bytes())==sheet['sha256']
    preferences=deepcopy(load(ROOT/'native_ready_subset_v1/preferences.json'))
    line_phrases={
        (81,90):['most popular'],(81,220):['count me in'],(81,228):['Nice to meet you.'],
        (82,183):["don't get it"],(83,23):['power of love'],(83,199):['save you'],
        (84,53):['Where does Gerhard Adernkatz live?'],(84,60):['Hurry up'],
        (84,160):['took him in'],(84,167):['After that'],(84,206):["old man's advice"],
        (84,257):['next time'],(84,361):['next time'],
    }
    page_clauses={
        (82,18):'I have no intention of getting married!',
        (82,140):"Traveling the world to train with your sword wouldn't be such a bad idea, would it?",
        (84,140):'His fleet was the reason.',
        (84,458):'then turn your own broadside toward them and fire.',
        (84,527):'then turn your own broadside toward them and fire.',
        (84,466):'Assigning an officer with high Aim to a Gun Battery will make their fire more effective.',
        (84,535):'Assigning an officer with high Aim to a Gun Battery will make their fire more effective.',
    }
    findings=[]
    for pair in sorted(line_phrases.keys()|page_clauses.keys()):
        ident=f'DK4_MES_B{pair[0]}_R{pair[1]:04d}';row=byid[ident]
        entry=preferences['records'].setdefault(ident,dict(bindings={k:sha(row[k].encode('utf-8')) for k in ['source_hex','current_hex','english']}))
        if pair in line_phrases:
            entry['line_phrases']=line_phrases[pair]
            reason='Keep the viewed phrasal verb,complete name question,idiom or short phrase together;ordinary breaks remain formatter-owned.'
        else:
            entry['page_clause']=page_clauses[pair]
            reason='The viewed page turn splits a complete closing sentence or tightly connected imperative. Keep this exact source-complete clause on the next page;allow only formatter-owned unused native rows at that semantic boundary,never a blank page.'
        findings.append(dict(id=ident,source_reference=row['source_reference'],current_reference=row['current_reference'],finding=reason,preference=entry))
    assert len(findings)==20
    preferences.update(native_visual_findings=findings,visual_basis=str(NATIVE),visual_basis_sha256=sha(NATIVE.read_bytes()),
        preserve_every_prose_character_source_macro_andcomplete_speaker_preamble=True)
    save(output,preferences)
    save(ROOT/'native_subset_v2/direct_visual_review_with_findings.json',dict(native_proof=str(NATIVE),native_proof_sha256=sha(NATIVE.read_bytes()),
        all30_readable_sheets_directly_viewed=True,all332_complete_native_pages_directly_viewed=True,sheets=native['review_sheets'],
        all323_native_glyph_bounds_consumption_checks_pass=True,all_layouts_finally_approved=False,
        layout_findings=findings,four_scoped_fullwidth_Latin_letters_now_normal_ASCII_in_complete_native_planes=True,
        silent_reaction_brief_complete_utterance_andcomplete_sentence_endings_retained=True,
        narrow_opening_retention_examples=['DK4_MES_B82_R0103','DK4_MES_B84_R0089'],
        retention_reason='Opening rows end at a complete expressive unit,or keep the following company name/causal clause intact;no lost glyphs,forced prose shortening or copied legacy padding.',
        offline_only_not_new_gameplay=True,menu_name_plane_stored_actual_andregistered_integration_pending=True,
        two_long_FE_tutorial_paragraphs_remain_excluded_not_passed=True,new_credit=0,guide_photos=False))
    print('Viewed332 pages/30 sheets;20 exact layout findings recorded,all words retained;four Latin artifacts render normally. Final layouts remain pending.')
