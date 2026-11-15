"""Save source-bound B166–B167 decisions and isolate staged FE and alias display leads."""
from collections import Counter
from copy import deepcopy
from pathlib import Path
from types import FunctionType

from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load, save
from scripts import write_rafael_B177_B180_contextual_v1 as previous
from scripts.qualify_rafael_B166_B167_names_v1 import A, CURRENT, IDENTITY

DRAFTS = A / 'Rafael_B161_B180_clean_20261105/B166_B167_clean_first_v1/sealed_drafts.json'
DECISIONS = Path('translations/rafael_B166_B167_contextual_decisions_v1.txt')
OUT = Path('translations/rafael_B166_B167_contextual_review_v1.json')
FE_SPEAKERS = {
    183:'Eirene',190:'Eirene',196:'Eirene',205:'Eirene',208:'Eirene',215:'Eirene',222:'Eirene',237:'Eirene',
    245:'Eirene',249:'Claudio Manaus',253:'Eirene',257:'Claudio Manaus',261:'Eirene',265:'Claudio Manaus',
    269:'Eirene',273:'Claudio Manaus',526:'Eirene',538:'Eirene',564:'Rafael Castor',572:'Rafael Castor',
    595:'Rafael Castor',610:'Rafael Castor',629:'Rafael Castor',787:'Charlotte Miller',791:'Charlotte Miller',
    794:'Charlotte Miller',797:'Charlotte Miller',908:'Rafael Castor',912:'Crew',
}
ACTOR8_IN_SCENE = {584,658,770,779}
LAYOUT_LEADS = {
    183:'Keep source heading above speech and preserve the hesitant reaction.',
    245:'Source uses a leading empty row and a separate initial address in this alternation.',
    249:'Restore source third-row right-side staging for Claudio.',
    253:'Restore source third-row left-side staging for Eirene.',
    257:'Restore source third-row right-side staging for Claudio.',
    261:'Restore source third-row left-side staging for Eirene.',
    265:'Preserve the original lower right silence with its complete ellipsis.',
    269:'Restore source third-row left-side staging for Eirene.',
    273:'Preserve the original lower right silence before the cut to the crew.',
    787:'Standalone letter salutation with the original FI substitution.',
    791:'Keep the original Portuguese and its phonetic aid in distinct row groups.',
    794:'Keep the Portuguese, phonetic aid and signature in distinct row groups.',
    797:'Keep the separate translated reading with FI and the distinct signature.',
    908:'Restore the source lower-row closing call.',
    912:'Restore the source lower-row crew response.',
}


def main():
    assert not OUT.exists()
    draft, current, identity = map(load, (DRAFTS,CURRENT,IDENTITY))
    assert identity['runtime']==current['runtime']
    originals = [r for group in current['groups'] for r in group['records']]
    by_id = {r['id']:r for r in originals}
    assert len(originals)==len(by_id)==len(draft['records'])==186
    names = {r['actor_ID']:next(x['text'] for x in r['current_consumers'] if x['consumer']=='progressive-nameplate')
        for r in identity['name_bindings']}
    env = {**previous.review_record.__globals__,'DECISIONS':DECISIONS,'CONTEXTS':{166:'B166',167:'B167'}}
    read = FunctionType(previous.read_decisions.__code__,env)
    review = FunctionType(previous.review_record.__code__,env)
    decisions = read()
    rows = [review(r,by_id[r['id']],names,decisions) for r in draft['records']]
    assert not decisions
    assert Counter(r['block'] for r in rows) == {166:136,167:50}
    assert {r['source_record_index'] for r in rows if r['source_selector']==254}==FE_SPEAKERS.keys()
    assert {r['source_record_index'] for r in rows if r['source_selector']==8}==ACTOR8_IN_SCENE
    for r, d in zip(rows,draft['records'],strict=True):
        r['context'] = d['context']
        idx = r['source_record_index']
        if r['source_selector']==254:
            r['speaker'] = FE_SPEAKERS[idx]
            r['FE_layout_finding'] = LAYOUT_LEADS.get(idx) or (
                'Preserve the separate explicit Eirene heading and wrap the body using native FE width.'
                if r['source_Japanese'].startswith('＜エイレネ＞') else 'Wrap logical prose using the established FE consumer.')
            r['FE_source_layout_native_requalification_pending'] = True
            if idx in (265,273):
                r['source_full_width_padding_is_staging_not_visible_glyph_defect'] = True
        elif r['source_selector']==8:
            r['speaker'] = 'Eirene'
            r['contextual_nameplate_vs_default_actor8_pending'] = True
        if (r['block'],idx) in {(166,568),(167,9)}:
            r['current_width_punctuation_normalized'] = True
    tokens = Counter(t for r in rows for t in r['native_literal_tokens'])
    assert tokens == {'FI':9,'FA':2,'FU':1}
    evidence = {str(p):sha(p.read_bytes()) for p in [DRAFTS,CURRENT,IDENTITY,DECISIONS,Path(previous.__file__),Path(__file__)]}
    doc = dict(format='dk4-contextual-dialogue-review-v2',translation_policy='natural-dialogue-v2',
        target_locale='en-US',encoder='dialogue-relocatable-v1',review_gates=previous.GATES,
        file_path='/data/SC0.DK4',blocks=[166,167],records=rows,source_objects=186,
        current_ROM=current['current_ROM'],current_ROM_sha256=current['current_ROM_sha256'],
        current_archive_sha256=current['current_archive_sha256'],runtime=current['runtime'],
        proposed_revisions=sum(r['decision']=='revision' for r in rows),
        justified_retentions=sum(r['decision']=='retention' for r in rows),
        current_glyph_defect_records=[r['id'] for r in rows if r.get('current_unintended_glyphs')],
        current_width_punctuation_records=[r['id'] for r in rows if r.get('current_width_punctuation_normalized')],
        glyph_only_revisions=[r['id'] for r in rows if r.get('glyph_only_revision_with_wording_retained')],
        contextual_alias_risk_records=[r['id'] for r in rows if r.get('contextual_nameplate_vs_default_actor8_pending')],
        all_individual_four_prose_gates_pass=True,all_fifth_formatting_gates_pending=True,
        native_macro_tokens_still_require_formatter_marking=True,
        no_new_formatting_rendering_gameplay_orregistered_integration_claim=True,new_credit=0,evidence=evidence)
    projected = deepcopy(doc)
    projected['translation_policy']='natural-dialogue-v1'
    validate_natural_dialogue_batch(projected)
    try:
        validate_natural_dialogue_batch(doc)
    except ValueError as error:
        assert 'requires per-record source, context, localization, naturalness, and formatting review' in str(error)
    else:
        raise AssertionError('Unformatted manuscript unexpectedly passed the release gate')
    save(OUT,doc)
    print(f"186 contextual reviews, {doc['proposed_revisions']} revisions and {doc['justified_retentions']} retentions. All display gates pending.")


if __name__ == '__main__':
    main()
