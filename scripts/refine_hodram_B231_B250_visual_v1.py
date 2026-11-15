"""Record the direct visual pass and bind scoped, prose-preserving wrap trials."""
from pathlib import Path
from scripts.audit_story_glyph_consistency import load,save
from dk4tool.patch.grand_race_menu_release import sha

ROOT=Path('work/Hodram_B231_B250_clean_20261107')
DOC=ROOT/'formatting_v1/formatting_input_v2.json'
INITIAL=ROOT/'formatting_v1/initial_plan_v2/automatic_plans.json'
VIEW=ROOT/'initial_visual_review_v1.json'
PREFERENCES=ROOT/'formatting_v1/visual_preferences_v1.json'

def main():
    assert not VIEW.exists() and not PREFERENCES.exists()
    doc,plan,index=map(load,(DOC,INITIAL,ROOT/'initial_body_sheets_v1/sheet_index.json'))
    rows={r['id']:r for r in doc['records']}
    findings={}
    def prefer(block,record,reason,**options):
        key=f'DK4_MES_B{block}_R{record:04d}'
        row=rows[key]
        findings[key]=dict(reason=reason,bindings={k:sha(row[k].encode('utf-8')) for k in ['source_hex','current_hex','english']},**options)
    prefer(231,28,'Keep the idiom help in a fight together where native width allows.',required_pairs=[['help','in']])
    prefer(232,13,'Avoid splitting the short question know it?',required_pairs=[['know','it']])
    prefer(232,20,'Keep the three-word item name Giant Tortoise Shield intact.',required_pairs=[['giant','tortoise'],['tortoise','shield']])
    prefer(232,23,'Keep the conversational callback like this continuous.',required_pairs=[['like','this']])
    prefer(232,34,'Keep help in a fight continuous in the repeated pitch.',required_pairs=[['help','in']])
    prefer(233,49,'Avoid separating knew from its following content clause.',required_pairs=[['knew','was']])
    prefer(234,35,'Keep far reaches continuous in the uncertain geographic clue.',required_pairs=[['far','reaches']])
    prefer(236,30,'Avoid a new page containing only precise location; test full-width one-page fit.',one_page=True)
    prefer(236,37,'Keep sounds wonderfully continuous in the comic comparison.',required_pairs=[['sounds','wonderfully']])
    prefer(238,35,'If two pages are needed, keep the complete looming-destruction sentence on one page.',page_clause='It seemed only a matter of time before the entire convoy was destroyed.')
    prefer(238,44,'Avoid a second page containing only the danger; test one-page fit.',one_page=True)
    prefer(239,30,'Keep explain it all continuous in the spoken letter.',required_pairs=[['explain','it'],['it','all']])
    prefer(239,42,'Keep find it continuous rather than detaching the object.',required_pairs=[['find','it']])
    prefer(239,46,'Replace very early rows and the stranded in handy tail with a full-width one-page layout.',one_page=True,required_pairs=[['look','for'],['come','in'],['in','handy']])
    prefer(239,70,'Test one-page fit for the short complete response; preserve all sentences.',one_page=True)
    prefer(240,18,'Avoid splitting Such a grand name across pages; test one-page fit without shortening the rant.',one_page=True,required_pairs=[['such','a'],['a','grand'],['grand','name']])
    prefer(240,28,'Keep the complete cannon-versus-maintenance complaint on one page of the required two-page speech.',page_clause='The men are wondering whether it helps with cannon fire, too, instead of maintaining the ship!',required_pairs=[['instead','of']])
    prefer(241,44,'Keep give me a moment continuous in the search for the gloves.',required_pairs=[['give','me']])
    prefer(241,74,'Keep how well they work continuous in the reassurance.',required_pairs=[['well','they']])
    prefer(242,53,'Keep the short reward enough conclusion continuous.',required_pairs=[["that's",'reward']])
    prefer(243,64,'Keep considering it continuous in the anxious question.',required_pairs=[['considering','it']])
    prefer(248,28,'Keep Take a little extra continuous at the sentence boundary.',required_pairs=[['take','a']])
    sheets=index['sheets']
    assert len(sheets)==10 and sum(len(s['included']) for s in sheets)==230
    for sheet in sheets:
        assert sha(Path(sheet['path']).read_bytes())==sheet['sha256']
    save(VIEW,dict(initial_plan=str(INITIAL),all230_initial_body_pages_directly_viewed=True,
        body_sheets=sheets,all_initial_name_andmenu_sheets_directly_viewed=True,
        scoped_name_sheets=2,choice_menu_sheets=1,body_glyph_findings=0,
        observed_layout_candidates=[dict(id=k,**v) for k,v in findings.items()],
        justification_for_other_initial_layout_retentions='Complete glyphs, readable ordinary phrase flow and native bounds; short replies and source hesitations remain appropriately short. No extra dramatic break is invented.',
        scope='Offline original-native pixels only; B231-B250 scene gameplay remains unvisited.',new_credit=0,
        evidence={str(p):sha(p.read_bytes()) for p in [DOC,INITIAL,ROOT/'native_initial_v1/compiled_native_pages.json',ROOT/'initial_body_sheets_v1/sheet_index.json',Path(__file__)]}))
    save(PREFERENCES,dict(records=findings,no_prose_shortened=True,no_geometry_or_font_change=True,new_credit=0))
    print('230 pages directly reviewed; 22 scoped layout trials saved.')

if __name__=='__main__':main()
