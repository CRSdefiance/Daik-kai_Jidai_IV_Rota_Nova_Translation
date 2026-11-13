"""Bind directly viewed phrase/page findings to unchanged logical English."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load,save

ROOT=Path('work/analysis/Rafael_B51_B60_formatting_20261104')
PHRASES={
    (51,75):["what country's"],
    (52,5):['Are you with {MACRO:FO}?'],
    (52,18):['home to Lisbon'],
    (53,6):['summoned us'],
    (55,8):["He's here"],(55,12):["I've already"],(55,47):['on giving me'],
    (55,115):['really got me fired up'],(55,142):['fellow Portuguese','backing down'],
    (55,168):['old bones','give it our all'],
    (56,21):['owe it'],(56,28):['how to trust'],(56,69):['What a vile scheme'],(56,77):['chipped in'],
    (57,33):["Ugh you're"],(57,64):['Come on let me have some'],(57,68):["I'm going"],
    (57,80):["That's why I'm visiting him"],(57,87):['Not sure about flowers',"you can't get them at sea"],
    (57,95):["crewmates aren't we"],(57,122):['Have plenty to eat all right'],
    (58,45):["Just what I'd expect"],(58,68):['Evergreen Lotus Leaf'],
    (60,44):['help you'],(60,57):["Can't we"],(60,111):['take on','their side you know'],
    (60,165):["Show me you're worthy of it"],(60,173):["Who's got","It's yours now"],
    (60,205):['yours truly'],(60,250):['last stronghold'],(60,309):['all our strength'],
    (60,335):['Free competition'],(60,370):['trade network'],(60,374):["who'd be"],
    (60,451):["there'll be"],(60,459):['caught up'],(60,470):["Spain's Invincible Armada"],
    (60,477):['give you'],
}
PAGES={
    (52,18):'He wants you to return home to Lisbon.',
    (60,140):"Throw in with men like that, and a dozen lives wouldn't last you.",
    (60,399):'If whoever controls them used that wealth to start conquering...',
    (60,486):"If you can't beat that little mustached bastard, you won't beat Kuhn in a hundred years!",
}

if __name__=='__main__':
    output=ROOT/'visual_preferences_v2.json';approval=ROOT/'initial253_pages_direct_visual_review.json'
    assert not output.exists() and not approval.exists()
    manuscript=ROOT/'formatting_input.json';native_path=ROOT/'speech_native_v1/compiled_native_pages.json'
    choices_path=ROOT/'two_choices_native_v1/complete_choice_objects.json'
    doc,native,choices=map(load,[manuscript,native_path,choices_path])
    assert native['pages']==253 and len(native['records'])==245 and native['fresh_compiled_alignments']==980
    assert native['all_first_internal_final_glyph_codes_pixels_input_canaries_andbounds_pass']
    assert len(native['review_sheets'])==25 and sum(s['pages'] for s in native['review_sheets'])==253
    for sheet in [*native['review_sheets'],*(o['review_sheet'] for o in choices['objects'])]:
        assert sha(Path(sheet['path']).read_bytes())==sheet['sha256']
    rows={(r['block'],r.get('source_record_index')):r for r in doc['records'] if r['kind']!='typed-choice-label'}
    records={}
    for key in PHRASES.keys()|PAGES.keys():
        row=rows[key]
        pref=dict(bindings={k:sha(row[k].encode('utf-8')) for k in ['source_hex','current_hex','english']},
            reason='Directly viewed complete page:keep the marked phrase orsuccessor-page clause together without changing prose.')
        if key in PHRASES:pref['line_phrases']=PHRASES[key]
        if key in PAGES:pref['page_clause']=PAGES[key]
        if key==(56,77):pref['ordinary_boundaries']=[['in','and']]
        records[row['id']]=pref
    save(output,dict(records=records,source_native_pages=str(native_path),source_native_pages_sha256=sha(native_path.read_bytes()),
        all_findings_directly_viewed=True,prose_unchanged=True,source_controls_font_geometry_andnative_code_unchanged=True))
    save(approval,dict(native=str(native_path),native_sha256=sha(native_path.read_bytes()),reviewed_sheets=native['review_sheets'],
        all253_initial_native_pages_directly_viewed=True,two_complete_menu_sheets_directly_viewed=True,
        menu_sheets=[o['review_sheet'] for o in choices['objects']],findings=records,
        retained_layouts=[
            dict(id='DK4_MES_B51_R0006',reason='The source thought deliberately trails off;the final since-I fragment belongs to that unfinished thought,not an omitted sentence.'),
            dict(id='DK4_MES_B54_R0031',reason='The complete governor’s-office object cannot join the introductory words within the validated width;keep the noun phrase intact.'),
            dict(id='DK4_MES_B55_R0044',reason='The second page already starts with the complete deduction-revelation sentence,preserving the joke.'),
            *[dict(id=f'DK4_MES_B60_R{n:04d}',reason='The second page contains a complete urgency sentence after the completed royal-succession hypothetical;no dangling clause.') for n in [208,293,474]],
            dict(id='DK4_MES_B60_R0277',reason='Keep Southeast Asia with at-once rather than fill the first row andstrand the short adverbial tail.')],
        native_checks_not_gameplay=True,formatting_approval_pending_updated_pages=True,new_credit=0,producer_sha256=sha(Path(__file__).read_bytes())))
    print('Recorded25 viewed speech sheets/253 pages and2 menu sheets;',len(records),'bound wrap findings;unchanged prose,updated pages pending.')
