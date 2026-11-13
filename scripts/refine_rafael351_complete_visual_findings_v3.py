"""Keep exact prose and refine eleven observed phrase/page breaks after viewing all344 pages."""
from copy import deepcopy
from pathlib import Path
from scripts.audit_story_glyph_consistency import load, save
from dk4tool.patch.grand_race_menu_release import sha

DOC=Path('translations/rafael_B121_B140_formatting_manuscript_v4.json')
PARENT=Path('translations/rafael_B121_B140_visual_preferences_v3.json')
OUT=Path('translations/rafael_B121_B140_visual_preferences_v4.json')
if __name__=='__main__':
    assert not OUT.exists()
    doc,prior=map(load,[DOC,PARENT]);out=deepcopy(prior);rows={r['id']:r for r in doc['records']}
    changes={
        'SC0_B125_STYLE_54_300':dict(line_phrases=['out of place'],reason='The viewed page splits out/of place. Keep the idiomatic unit together.'),
        'SC0_B125_STYLE_440_366':dict(line_phrases=['out of this'],reason='The viewed page splits figurehead out/of this;keep out of this together without changing the proposed-use meaning.'),
        'DK4_MES_B127_R0026':dict(line_phrases=['Touch the flagship to stop.'],reason='Keep the complete second instruction together instead of leaving Touch after automatically. on the preceding line.'),
        'DK4_MES_B128_R0023':dict(line_phrases=['sail handlers'],reason='The viewed page splits the relevant crew-role phrase sail/handlers. Keep the noun phrase together.'),
        'DK4_MES_B129_R0024':dict(page_clause='into Africa and the New World.',reason='The prior full-condition page cut produced short middle rows on page1. Keep both destination regions together on page2 after the complete company/expansion verb phrase;all source goods,qualified future importance andthe FO macro stay unchanged.'),
        'DK4_MES_B134_R0019':dict(line_phrases=['Of all the people'],reason='Keep Claudio\'s alarmed Of all the people idiom together rather than splitting Of all/the people.'),
        'DK4_MES_B135_R0005':dict(line_phrases=['all sorts of taverns'],reason='Keep the noun phrase all sorts of taverns together instead of splitting all sorts/of taverns.'),
        'DK4_MES_B136_R0023':dict(line_phrases=['Guiding Staff'],reason='Keep the exact newly bound item name together instead of splitting Guiding/Staff.'),
        'DK4_MES_B136_R0147':dict(line_phrases=["shouldn't have been",'I owe him an apology.'],reason='The viewed opening Oh... I shouldn\'t is sparse. Keep the auxiliary sequence and the full apology sentence together in the unchanged remorseful paragraph.'),
        'DK4_MES_B137_R0013':dict(line_phrases=['A long voyage'],reason='Keep A long voyage together rather than ending the first line with A long.'),
        'DK4_MES_B137_R0060':dict(line_phrases=['choose Finish','Now, give it a try.'],reason='Keep the exact command instruction and the following encouragement together instead of splitting choose/Finish and Now,/give it a try.'),
    }
    for ident,value in changes.items():
        row=rows[ident]
        value['bindings']={k:sha(row[k].encode('utf-8')) for k in ['source_hex','current_hex','english']}
        out['records'][ident]=value
    out.update(previous_preferences=str(PARENT),previous_preferences_sha256=sha(PARENT.read_bytes()),
        full_current344_body_pages_directly_viewed_before_these_refinements=True,
        eleven_observed_phrase_orpage_refinements=list(changes),
        fresh_native_andvisual_checks_required_for_changed_encoded_bytes=True)
    out['evidence'].update({str(p):sha(p.read_bytes()) for p in [DOC,PARENT,Path(__file__)]})
    save(OUT,out);print('Saved eleven observed phrase/page refinements;all344 current pages viewed. Exact prose,controls,macros,font andnative geometry unchanged.')
