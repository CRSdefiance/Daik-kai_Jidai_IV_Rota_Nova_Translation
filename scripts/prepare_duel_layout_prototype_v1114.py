"""Refine one formal line from source and define automatic post-macro layout."""
from pathlib import Path
from collections import Counter
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save


def main():
    source=Path('translations/duel_editorial_manuscript_v2.json')
    target=Path('translations/duel_editorial_manuscript_v3.json')
    root=Path('work/analysis/duel_layout_v1114')
    assert not target.exists() and not root.exists()
    doc=read(source);row=next(r for r in doc['records'] if r['message_id']==1938)
    assert row['english']=="...You're %s! We shall settle this with a duel!" and row['editorial_decision']=='retain'
    row['english']="...%s! Let us settle this with a duel!"
    row['editorial_decision']='revise'
    row['localization_note']+=(
        ' Source refinement:the paused call of the opponents name conveys recognition in spoken English;formal Let us preserves the original proposal 勝負をつけようぞ. '
        'An explicit You are is unnecessary here,and a new question would invent uncertainty. Keep the full duel-resolution intent,ellipsis and formal voice. '
        'This complete phrasing also supports the legal16-character name without reducing the name,font size or source meaning. Native formatting and release gates remain pending.')
    assert Counter(r['editorial_decision'] for r in doc['records'])=={'revise':23,'retain':10}
    doc.update(supersedes_manuscript=str(source),supersedes_manuscript_sha256=sha(source.read_bytes()),
        status='33-source-prose-reviewed;duel24x3-postmacro-layout-prototype-pending-runtime-and-actual')
    root.mkdir(parents=True);save(target,doc)
    save(root/'source_refinement1938.json',{'source_manuscript':str(source),'source_manuscript_sha256':sha(source.read_bytes()),
        'target_manuscript':str(target),'source_Japanese':row['source_Japanese'],'source_meaning':row['source_meaning'],
        'previous_English':"...You're %s! We shall settle this with a duel!",'current_draft_English':row['english'],
        'recognition_formality_and_full_duel_resolution_meaning_preserved':True,
        'no_authored_linebreak_font_name_or_panel_dimension_change':True,'formatting_and_release_not_approved':True})
    ledger_path=Path('translations/editorial_review_current_v1.json');ledger=read(ledger_path)
    assert ledger['records_editorially_completed']==1196 and ledger['records_with_source_and_prose_pass']==1267
    paths=ledger['active_source_prose_drafts']['manuscripts'];assert paths.count(str(source))==1
    paths[paths.index(str(source))]=str(target)
    ledger['duel_prose_v1103'].update(manuscript=str(target),revisions=23,retained_wordings=10,
        source_refinement1938=str(root/'source_refinement1938.json'))
    save(ledger_path,ledger)
    print('Formal1938 proposal refined from source;33 drafts now23 revisions10 retentions. No new credit;original panel/font/name dimensions preserved.')


if __name__=='__main__':main()
