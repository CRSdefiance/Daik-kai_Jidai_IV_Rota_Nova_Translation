"""Record direct inspection of all28 native body pages and two narrowly scoped ordinary boundaries."""
from pathlib import Path
from scripts.verify_village_wrap_v608 import read,save
from dk4tool.patch.grand_race_menu_release import sha
ROOT=Path('work/analysis/Hodram_B137_B45_B46_native_review_v8247')
PAGES=Path('work/analysis/Hodram_B137_B45_B46_pages_v8246/28_complete_native_paragraphs28_pages112_compiled_alignments.json')
if __name__=='__main__':
    assert not ROOT.exists();pages=read(PAGES);plan=read(pages['plan']);doc=read(pages['manuscript'])
    assert pages['manuscript_sha256']==sha(Path(pages['manuscript']).read_bytes()) and pages['plan_sha256']==sha(Path(pages['plan']).read_bytes())
    assert len(pages['records'])==pages['complete_progressive_pages']==28
    viewed=[]
    for sheet in pages['review_sheets']:
        assert sha(Path(sheet['path']).read_bytes())==sheet['sha256']
        viewed.append(dict(**sheet,directly_viewed=True,scope='Offline original native body renderer;not an emulator scene capture ornameheader proof.'))
    assert len(viewed)==3
    reasons={
      'DK4_MES_B137_R0089':"Retain the exact ordinary the / Mediterranean boundary. The complete36-cell clause the Mediterranean live by sea trade. does not fit a guarded continuation row;keeping all128 prose characters naturally in four rows leaves this complete article at a row end. The next row identifies the region immediately. No word or glyph is split,and the paragraph preserves bothcities anduncertain recruitment. Adding a page orrewriting the meaning solely toeliminate this article boundary would reduce readability. This exception isonlythis complete compiled paragraph,not aglobal weak-word exemption.",
      'DK4_MES_B137_R0092':"Retain the exact ordinary to / the towns boundary. This keeps the towns around the Mediterranean together on thefinal row andpreserves a natural complete three-row paragraph. To is a complete preposition;allfirst/internal/finalglyphs andpunctuation arepresent. It doesnot justify clipping,splitwords,extra pages orother future boundary changes. Bind onlythisexact source/prose/compiled record.",
    }
    warnings=[];infos=[]
    for row,p,n in zip(doc['records'],plan['records'],pages['records'],strict=True):
        assert row['id']==p['id']==n['id'] and row['english']==n['logical_English']==' '.join(p['lines'])
        assert len(n['pages'])==p['expected_native_pages']==1 and not row['review']['formatting']
        for page in n['pages']:
            assert sha(Path(page['native_plane']).read_bytes())==page['native_plane_sha256']
            assert sha(Path(page['preview']).read_bytes())==page['preview_sha256']
            assert page['native_independent_plane_equal'] and page['first_visible_origin']==[0,0]
        for issue in p['base_QA']['issues']:
            assert issue['severity']!='error'
            if issue['severity']=='warning':
                assert issue['code']=='weak-line-ending' and row['id'] in reasons
                warnings.append(dict(id=row['id'],issue=issue,reason=reasons[row['id']],source_hex=row['source_hex'],
                    logical_English=row['english'],compiled_hex=p['encoded_hex'],generated_lines=p['lines'],
                    manuscript_sha256=pages['manuscript_sha256'],proposed_later_scoped_qa_waivers=['weak-line-ending']))
            elif issue['severity']=='info':infos.append(dict(id=row['id'],issue=issue))
    assert len(warnings)==2 and {r['id'] for r in warnings}==set(reasons)
    ROOT.mkdir(parents=True)
    save(ROOT/'28_native_pages_directly_viewed_two_exact_boundary_reviews.json',dict(pages=str(PAGES),pages_sha256=sha(PAGES.read_bytes()),manuscript=pages['manuscript'],manuscript_sha256=pages['manuscript_sha256'],
        directly_viewed_sheets=viewed,all28_complete_bodies_visually_read=True,original_warnings=warnings,original_infos=infos,original_diagnostics_not_suppressed=True,
        three_source_silences_complete_original_ellipsis_glyphs=True,source_Camille_name_check_tag_andfinal_Hodram_question_coherent=True,
        all28_singlepages_original216px_fourrows_fullleading_internal_trailing_glyphs=True,
        no_manual_wraps_width_font_or_global_weak_rule_change=True,all28_formatting_gates_remain_false=True,
        body_preview_not_nameheader_stored_script_scene_transition_item_panel_ornatural_event_coverage=True,
        stored_controls_names_actual4800_layout0_hide4700_andregistered_release_pending=True,
        new_credit=0,new_emulator_runs=0,full_goal_complete=False,evidence={str(p):sha(p.read_bytes()) for p in [PAGES,Path(pages['plan']),Path(pages['manuscript']),Path(__file__)]}))
    print('28body pages directly viewed;two exact ordinary-boundary reviews;infos',len(infos),'allformatting gates remainfalse.')
