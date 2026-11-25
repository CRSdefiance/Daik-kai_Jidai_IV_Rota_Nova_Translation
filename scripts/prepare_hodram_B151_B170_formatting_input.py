"""Bind selected prose to the existing formatter; defer only the unqualified cinematic FE bodies."""
from copy import deepcopy
from pathlib import Path
from scripts.audit_story_glyph_consistency import load,save
from dk4tool.patch.grand_race_menu_release import sha

ROOT=Path('work/analysis/Hodram_B151_B170_formatting_20261102')
SOURCE=Path('translations/hodram_B151_B170_contextual_editorial_manuscript_v3.json')


if __name__=='__main__':
    assert not ROOT.exists();doc=load(SOURCE)
    assert len(doc['records'])==642 and doc['complete_four_gate_comparisons']==642
    rows=[];deferred=[]
    for source in doc['records']:
        row=deepcopy(source)
        if row.get('source_selector')==254 and row['block']==156:
            deferred.append(row);continue
        if row['kind']!='typed-choice-label':
            row['kind']='system-FE' if row['source_selector']==254 else 'progressive'
            row['source_record_index']=row['source_reference']['record_index']
            row['planned_English_markup']='{SPEAKER:'+f'{row["source_selector"]:02X}'+'}'+row['english']
            row['source_meaning_gloss']=row['source_meaning']
            row['complete_clean_exchange_context']=row['context']
        assert all(row['review'][k] for k in ['source','context','localization','naturalness']) and not row['review']['formatting']
        rows.append(row)
    assert len(deferred)==23 and len(rows)==619
    assert sum(r['kind']=='progressive' for r in rows)==602 and sum(r['kind']=='system-FE' for r in rows)==9
    assert sum(r['kind']=='typed-choice-label' for r in rows)==8
    result={**doc,'records':rows,'physical_speech_objects':611,'ordinary_speech_objects':611,'typed_choice_objects':8,'typed_choice_commands':4,
        'source_full_manuscript':str(SOURCE),'source_full_manuscript_sha256':sha(SOURCE.read_bytes()),
        'deferred_cinematic_records':[r['id'] for r in deferred],
        'only_native_formatting_schedule_split_no_editorial_scope_orprose_reduction':True,
        'new_credit':0,'producer_sha256':sha(Path(__file__).read_bytes())}
    ROOT.mkdir(parents=True);save(ROOT/'ordinary_formatting_input.json',result)
    save(ROOT/'deferred_cinematic_records.json',dict(records=deferred,source_manuscript=str(SOURCE),source_manuscript_sha256=sha(SOURCE.read_bytes()),
        original_source_staging_preserved_until_native_geometry_qualification=True,no_prose_removed_from_goal=True,new_credit=0))
    print('611 speeches ready for fresh ordinary formatting;8 captions retained separately;23 cinematic FE records explicitly scheduled after source geometry. All642 prose preserved.')
