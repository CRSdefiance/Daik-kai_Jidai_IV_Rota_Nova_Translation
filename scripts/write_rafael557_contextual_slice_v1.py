"""Bind individual editorial decisions to exact clean/current exchanges andexisting identity data."""
from copy import deepcopy
from pathlib import Path
import re
from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load,save

DRAFTS=Path('work/analysis/Rafael_B141_B160_clean_20261105/all557_meanings_andindependent_drafts_v2.json')
CURRENT=Path('work/analysis/Rafael_B141_B160_current867_20261105/current_effective.json')
CAPTIONS=CURRENT.with_name('current_captions_andglyph_findings_v1.json')
IDENTITY=Path('work/analysis/Rafael557_names_terms_v1_20261105/names_terms_andconsumer_dependency_qualification.json')


def write_slice(out,decisions,overrides,producer,expected):
    out=Path(out);assert not out.exists()
    drafts,current,captions,identity=map(load,[DRAFTS,CURRENT,CAPTIONS,IDENTITY])
    source={r['id']:r for r in drafts['records']}
    existing={r['id']:r for g in current['groups'] for r in g['records']}
    existing.update({r['id']:r for r in captions['choices']})
    names={r['actor_ID']:next(x['text'] for x in r['current_consumers'] if x['consumer']=='progressive-nameplate') for r in identity['name_bindings']}
    assert set(existing)==set(source) and len(existing)==557
    assert set(overrides)<=set(decisions) and len(decisions)==expected
    rows=[]
    for ident,(decision,finding) in decisions.items():
        draft,old=source[ident],existing[ident]
        assert all(draft[k]==old[k] for k in ['file_path','block','source_reference','source_hex'])
        assert decision in ['revision','retention'] and finding
        previous=old.get('current_comparison_paragraph',old.get('current_English','')).strip()
        assert previous
        english=overrides.get(ident,previous if decision=='retention' else draft['independent_English'])
        if decision=='retention':assert english==previous
        else:assert english!=previous,ident
        assert english and '\n' not in english and not any(t in english for t in ['{LB','{ALIGN','{PAD}','%'])
        raw=bytes.fromhex(draft['source_hex']);body=raw[1:] if 'source_selector' in draft else raw
        tokens={t.decode():body.count(t) for t in set(re.findall(rb'F[A-Z]',body))}
        assert all(english.count(t)==n for t,n in tokens.items()),ident
        row=deepcopy(draft)
        row.update({k:deepcopy(v) for k,v in old.items() if k.startswith('current_') or k in ['selected_native_pointer']})
        row.update(english=english,decision=decision,finding=finding,localization_note=finding,
            source_meaning=draft['source_meaning'],context=draft['context'],
            speaker=names[draft['source_selector']] if 'source_selector' in draft and draft['source_selector']!=254 else
                ('System panel' if 'source_selector' in draft else 'Player choice'),
            kind=('system-FE' if draft['source_selector']==254 else 'progressive') if 'source_selector' in draft else 'typed-choice-label',
            current_English_comparison_pending=False,current_ROM_English_unconsulted=False,earlier_English_unconsulted=False,
            approved_names_terms_titles_andruntime_substitutions_pending=False,
            source_context_localization_formatting_gates_pending=False,all_five_review_gates_pending=False,
            complete_native_menu_binding_andformatting_pending=False,
            review=dict(source=True,context=True,localization=True,naturalness=True,formatting=False),
            fresh_formatting_binding_pending=True,registered_release_andcompletion_credit_pending=True,
            source_draft=str(DRAFTS),source_draft_sha256=sha(DRAFTS.read_bytes()),
            scoped_name_term_binding=str(IDENTITY),scoped_name_term_binding_sha256=sha(IDENTITY.read_bytes()),new_credit=0)
        if 'record_index' in row['source_reference']:
            row['source_record_index']=row['source_reference']['record_index']
        if decision=='retention':row['retention_reason']=finding
        row['native_literal_token_counts']=tokens
        if not english.isascii():
            assert decision=='retention' and set(english)<=set('…！？!? .'),ident
            row['deliberate_source_punctuation_retention']=True
        if previous.replace('Ｉ','I').replace('Ｆ','F')==english and previous!=english:
            row['glyph_only_revision_with_wording_retained']=True
        if 'FU' in tokens:row['FU_current_expansion_width_anddisplay_pending']=True
        rows.append(row)
    rows.sort(key=lambda r:(r['block'],r['source_reference']['offset']))
    blocks=sorted({r['block'] for r in rows})
    assert all({r['id'] for r in rows if r['block']==b}=={r['id'] for r in drafts['records'] if r['block']==b} for b in blocks)
    doc=dict(format='dk4-contextual-dialogue-review-v2',translation_policy='natural-dialogue-v2',target_locale='en-US',
        encoder='dialogue-relocatable-v1',review_gates=['source','context','localization','naturalness','formatting'],
        file_path='/data/SC0.DK4',blocks=blocks,records=rows,current_ROM=current['current_ROM'],
        current_ROM_sha256=current['current_ROM_sha256'],current_archive_sha256=current['current_archive_sha256'],
        source_objects=len(rows),proposed_revisions=sum(r['decision']=='revision' for r in rows),
        justified_retentions=sum(r['decision']=='retention' for r in rows),all_individual_four_prose_gates_pass=True,
        all_fifth_formatting_gates_pending=True,native_macro_tokens_still_require_formatter_marking=True,
        no_new_formatting_rendering_gameplay_orregistered_integration_claim=True,new_credit=0,guide_photos=False,
        evidence={str(p):sha(p.read_bytes()) for p in [DRAFTS,CURRENT,CAPTIONS,IDENTITY,Path(producer),Path(__file__)]})
    # The release validator deliberately requires all five gates. This manuscript
    # has only the four prose gates; never fabricate a formatting pass to save it.
    # Check the shared structural rules through the v1 policy projection, then
    # explicitly check the v2 prose fields. The unchanged v2 release validator
    # must reject this pending-formatting manuscript.
    projected=deepcopy(doc);projected['translation_policy']='natural-dialogue-v1'
    validate_natural_dialogue_batch(projected)
    assert all(r['source_meaning'].strip() and r['localization_note'].strip()
        and all(r['review'][g] is True for g in ['source','context','localization','naturalness'])
        and r['review']['formatting'] is False for r in rows)
    try:validate_natural_dialogue_batch(doc)
    except ValueError as error:
        assert 'requires per-record source, context, localization, naturalness, and formatting review' in str(error)
    else:raise AssertionError('Unformatted manuscript unexpectedly passed the release gate')
    doc['validation_scope']='Shared record structure and four prose gates only; unchanged v2 release gate correctly rejects pending formatting.'
    save(out,doc)
    print(f"Saved{len(rows)} contextual reviews:{doc['proposed_revisions']} revisions/{doc['justified_retentions']} retentions. Four prose gates pass;formatting/display/integration pending;no credit.")
