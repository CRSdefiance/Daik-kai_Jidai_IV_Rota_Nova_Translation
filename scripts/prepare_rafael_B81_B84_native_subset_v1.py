"""Advance323 complete speech objects;retain two explicit FE overflow risks andfive menu objects."""
from copy import deepcopy
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load,save

ROOT=Path('work/analysis/Rafael_B81_B84_formatting_20261105')
PARENT=ROOT/'formatting_input.json'

if __name__=='__main__':
    out=ROOT/'native_ready_subset_v1';assert not out.exists()
    doc=load(PARENT);failed=load(ROOT/'automatic_v1/automatic_plans.json')
    held={'DK4_MES_B84_R0470','DK4_MES_B84_R0539'}
    assert {r['id'] for r in failed['failures']}==held and len(failed['records'])==323
    subset=deepcopy(doc);subset['records']=[r for r in doc['records'] if r['kind']!='typed-choice-label' and r['id'] not in held]
    assert len(subset['records'])==323
    subset.update(physical_speech_objects=323,ordinary_speech_objects=311,FE_speech_objects=12,typed_choice_objects=0,typed_choice_commands=0,
        subset_of=str(PARENT),subset_of_sha256=sha(PARENT.read_bytes()),
        held_source_IDs=sorted(held),held_typed_choice_objects=5,whole_batch_display_complete=False)
    prefs={};plans={r['id']:r for r in failed['records']}
    for ident,index,reason in [
        ('DK4_MES_B82_R0089',0,"Cristina deliberately trails off after engaged to... before insulting her would-be fiance. The source has an interrupted pause;this is a complete intentional ellipsis,not an auxiliary/preposition stranded by wrapping."),
        ('DK4_MES_B82_R0103',1,"Mivor's complete shouted protest ends told me to! before his declaration of sincere feelings. To is the grammatical elliptical infinitive at a sentence boundary,not a broken phrase;retain the natural complete sentence.")]:
        row=next(r for r in subset['records'] if r['id']==ident)
        prefs[ident]=dict(bindings={k:sha(row[k].encode('utf-8')) for k in ['source_hex','current_hex','english']},
            QA_line_ending_retention=dict(exact_line=plans[ident]['lines'][index],line_index=index,reason=reason))
    out.mkdir();save(out/'manuscript.json',subset);save(out/'preferences.json',dict(records=prefs))
    save(out/'held_FE_risk.json',dict(source_IDs=sorted(held),unchanged_logical_English={r['id']:r['english'] for r in doc['records'] if r['id'] in held},
        finding='Two identical146-character source-complete tutorial paragraphs have no guarded four-row plan at native228px FE geometry. Do not shrink fonts,widen geometry,drop words,shorten good prose merely to fit,or mark them passed. Need source-preserving consumer pagination with focused transition proof.',
        original_failure=str(ROOT/'automatic_v1/automatic_plans.json'),original_failure_sha256=sha((ROOT/'automatic_v1/automatic_plans.json').read_bytes()),
        untouched_source_control_ownership_andall_other_record_checks_still_required=True,new_credit=0))
    print('Prepared323 fresh native candidates;two FE paragraphs andfive typed captions remain separately tracked;two exact grammatical endings documented.')
