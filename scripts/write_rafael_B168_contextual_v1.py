"""Record both complete B168 exchanges against their exact clean and current records."""
from copy import deepcopy
from pathlib import Path
from types import FunctionType

from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.patch.grand_race_menu_release import sha
from scripts import write_rafael_B177_B180_contextual_v1 as previous
from scripts.audit_story_glyph_consistency import load, save

A=Path('work/analysis')
CURRENT=A/'Rafael_B168_current1674_20261105/current_effective.json'
DRAFTS=A/'Rafael_B161_B180_clean_20261105/B168_clean_first_v1/sealed_drafts.json'
IDENTITY=A/'Rafael_B166_B167_current1674_20261105/names_and_terms_v1.json'
DECISIONS=Path('translations/rafael_B168_contextual_decisions_v1.txt')
OUT=Path('translations/rafael_B168_contextual_review_v1.json')
GATES=previous.GATES


def main():
    assert not OUT.exists()
    drafts,current,identity=map(load,(DRAFTS,CURRENT,IDENTITY))
    assert identity['runtime']==current['runtime']
    assert drafts['complete_blocks']==[168]
    source=current['groups'][0]['records']
    assert len(source)==len(drafts['records'])==47
    ids={r['id']:r for r in source}
    actors={r['source_selector'] for r in source}
    assert actors=={0,5,6,15}
    names={r['actor_ID']:next(c['text'] for c in r['current_consumers'] if c['consumer']=='progressive-nameplate')
        for r in identity['name_bindings'] if r['actor_ID'] in actors}
    assert names=={0:'Rafael Castor',5:'Claudio Manaus',6:'Julio Erneco',15:'Angelo Puccini'}
    env={**previous.review_record.__globals__,'DECISIONS':DECISIONS,'CONTEXTS':{168:drafts['source_contexts']['168']}}
    read=FunctionType(previous.read_decisions.__code__,env)
    compare=FunctionType(previous.review_record.__code__,env)
    decisions=read()
    rows=[compare(r,ids[r['id']],names,decisions) for r in drafts['records']]
    assert not decisions
    for r in rows:
        if r['source_record_index'] in (89,174):
            r['current_width_punctuation_normalized']=True
    doc=dict(format='dk4-contextual-dialogue-review-v2',translation_policy='natural-dialogue-v2',target_locale='en-US',
        encoder='dialogue-relocatable-v1',review_gates=GATES,file_path='/data/SC0.DK4',blocks=[168],records=rows,
        source_objects=47,current_ROM=current['current_ROM'],current_ROM_sha256=current['current_ROM_sha256'],
        current_archive_sha256=current['current_archive_sha256'],runtime=current['runtime'],
        proposed_revisions=sum(r['decision']=='revision' for r in rows),justified_retentions=sum(r['decision']=='retention' for r in rows),
        current_glyph_defect_records=[r['id'] for r in rows if r.get('current_unintended_glyphs')],
        current_width_punctuation_records=[r['id'] for r in rows if r.get('current_width_punctuation_normalized')],
        all_individual_four_prose_gates_pass=True,all_fifth_formatting_gates_pending=True,
        native_macro_tokens_still_require_formatter_marking=True,
        scoped_unchanged_name_binding=str(IDENTITY),new_credit=0,
        evidence={str(p):sha(p.read_bytes()) for p in (DRAFTS,CURRENT,IDENTITY,DECISIONS,Path(previous.__file__),Path(__file__))})
    projected=deepcopy(doc);projected['translation_policy']='natural-dialogue-v1'
    validate_natural_dialogue_batch(projected)
    assert all(not row['review']['formatting'] for row in rows)
    save(OUT,doc)
    print(f"47 contextual comparisons, {doc['proposed_revisions']} revisions and {doc['justified_retentions']} retentions. Fresh display gates pending.")


if __name__=='__main__':
    main()
