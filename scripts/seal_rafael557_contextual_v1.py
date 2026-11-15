"""Seal the complete prose decisions; retain all unformatted originals and zero credit."""
from copy import deepcopy
from collections import Counter
from pathlib import Path
import re,struct
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load,save
from scripts.qualify_rafael351_item_and_UI_terms_v1 import string

ROOT=Path('work/analysis/Rafael557_contextual_comparison_v1_20261105')
PARTS=[Path('translations/rafael_B141_B145_B150_contextual_review_v1.json'),
    Path('translations/rafael_B146_B149_B151_B160_contextual_review_v1.json')]
OUT=Path('translations/rafael_B141_B160_contextual_review_v1.json')
IDENTITY=Path('work/analysis/Rafael557_names_terms_v1_20261105/names_terms_andconsumer_dependency_qualification.json')
PRIOR=Path('translations/rafael_B61_B80_scoped_names_actual_final_v1.json')

def main():
    assert not ROOT.exists() and not OUT.exists()
    documents=list(map(load,PARTS));identity=load(IDENTITY)
    rows=sorted([deepcopy(r) for d in documents for r in d['records']],key=lambda r:(r['block'],r['source_reference']['offset']))
    drafts_path=Path('work/analysis/Rafael_B141_B160_clean_20261105/all557_meanings_andindependent_drafts_v2.json')
    drafts=load(drafts_path);source={r['id']:r for r in drafts['records']}
    assert len(rows)==len({r['id'] for r in rows})==557 and {r['id'] for r in rows}==set(source)
    assert all(d['current_ROM_sha256']==identity['runtime']['candidate_sha256'] for d in documents)
    # Reuse the established spoken spelling only after checking its exact current
    # source/first/last fields. No new getter, font or catalogue-UI claim is made.
    prior=next(r for r in load(PRIOR)['records'] if r.get('actor_ID')==40)
    assert prior['english']=='Antony Kuhn' and all(prior['review'][g] for g in ['source','context','localization','naturalness'])
    arm=NdsImage.open(identity['runtime']['candidate']).read_file('/__arm9__.bin')
    jp=NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    assert sha(arm)==identity['runtime']['ARM9_sha256']
    snapshot=identity['runtime']['snapshot'];raw=Path(snapshot['path']).read_bytes()
    assert sha(raw)==snapshot['sha256']
    fields=[]
    for old in prior['source_reference']['clean_fields']:
        pos=old['source_field'];sp,cp=[struct.unpack_from('<I',a,pos)[0] for a in [jp,arm]]
        s,c=string(jp,sp),string(raw,cp)
        assert s['text']==old['source_text'] and s['hex']==old['source_hex']
        fields.append(dict(column=old['column'],field_offset=pos,source=s,current=c))
    spoken=fields[0]['current']['text']+' '+fields[1]['current']['text']
    assert spoken==prior['english']
    for row in rows:
        original=source[row['id']]
        assert all(row[k]==original[k] for k in ['source_reference','source_hex','source_complete_preamble_hex'] if k in original)
        assert all(row['review'][g] is True for g in ['source','context','localization','naturalness']) and row['review']['formatting'] is False
        # Resolve draft-only terminology in explanatory metadata; preserve the
        # independent English and exact original draft as immutable provenance.
        for key in ['source_meaning','context']:
            row[key]=row[key].replace('Coen','Kuhn').replace('Ihwa','Yifa')
        if row['block']==160:
            row['context']='Two alternative participants disassemble the Tang Bamboo Craft using the Bamboo Assembly Plan. Janus or Yifa discovers a drawing inside/on the back of a bamboo piece. Preserve the Tang cultural context, alternate speakers and their different levels of certainty; approved names and item titles are bound separately.'
        if row['id']=='DK4_MES_B160_R0025':
            row['source_meaning']='On the alternate participant branch, Yifa experiments with taking the craft apart.'
        if row['id']=='DK4_MES_B143_R0372':
            row['source_meaning']='Fernan gives two ways to declare war: attack the other faction at sea, or have the assigned First Mate prepare the document at the Guild. The First Mate is the player\'s officer, not a guild employee.'
        row['non_speaking_Kuhn_spelling_qualification']=str(ROOT/'current_Kuhn_spelling_binding.json') if row['block']==152 else None
        row['logical_paragraph_with_no_authored_wraps']=True
        assert not any(t in row['english'] for t in ['Coen','Koon','Ihwa','Ｉ','Ｆ','惨','\n','{LB','{ALIGN','{PAD}'])
        if row['decision']=='retention':
            assert row['retention_reason'] and row['english']==row.get('current_comparison_paragraph',row.get('current_English','')).strip()
    counts=Counter(r['decision'] for r in rows);assert counts=={'revision':235,'retention':322}
    token_counts=Counter()
    for row in rows:token_counts.update(row['native_literal_token_counts'])
    assert token_counts=={'FI':41,'FA':8,'FO':10,'FU':2}
    glyphs=[r for r in rows if any(c in r.get('current_comparison_paragraph',r.get('current_English','')) for c in ['Ｉ','Ｆ','惨'])]
    assert len(glyphs)==13 and all(r['decision']=='revision' for r in glyphs)
    assert sum(r.get('glyph_only_revision_with_wording_retained',False) for r in rows)==9
    ROOT.mkdir(parents=True)
    save(ROOT/'current_Kuhn_spelling_binding.json',dict(actor_ID=40,approved_spoken_name=spoken,
        original_source_andcurrent_fields=fields,approved_review=str(PRIOR),approved_review_sha256=sha(PRIOR.read_bytes()),
        current_runtime=identity['runtime'],no_new_native_getter_font_display_orcatalogue_UI_execution=True,
        full_middle_component_andcatalogue_UI_not_approved=True,no_name_data_changes=True))
    combined={k:deepcopy(v) for k,v in documents[0].items() if k not in ['records','blocks','source_objects','proposed_revisions','justified_retentions','evidence']}
    combined.update(blocks=list(range(141,161)),records=rows,source_objects=557,ordinary_speeches=549,choice_captions=8,
        proposed_revisions=235,justified_retentions=322,completed_current_comparisons=557,remaining_current_comparisons=0,
        scoped_public_name_retentions=20,source_literal_substitution_counts=dict(token_counts),
        glyph_defect_records=13,glyph_only_revisions=9,source_only_punctuation_not_blanket_flagged=True,
        evidence={str(p):sha(p.read_bytes()) for p in [*PARTS,IDENTITY,PRIOR,drafts_path,ROOT/'current_Kuhn_spelling_binding.json',Path(__file__)]})
    save(OUT,combined)
    save(ROOT/'comparison_qualification.json',dict(manuscript=str(OUT),manuscript_sha256=sha(OUT.read_bytes()),
        source_objects=557,whole_blocks=20,ordinary_speeches=549,choice_captions=8,
        revisions=235,retentions=322,scoped_name_retentions=20,all_individual_four_prose_gates=True,
        fifth_gate_pending_for_all557=True,new_credit=0,current_ROM_sha256=combined['current_ROM_sha256'],
        exact_source_current_bindings_and_independent_source_draft_provenance=True,
        all61_literal_substitutions_preserved=True,glyph_findings=[dict(id=r['id'],previous=r['current_comparison_paragraph'],english=r['english'],
            wording_retained=r.get('glyph_only_revision_with_wording_retained',False)) for r in glyphs],
        fresh_formatting_all_pages_andrepresentative_distinct_behavior_tests_pending=True,
        registered_integration_clean_input_patch_andcredit_pending=True,no_new_gameplay_orvisual_claim=True,guide_photos=False))
    print('Sealed557 complete contextual comparisons:235 revisions/322 retentions;20 names retained;13 glyph defects corrected in prose,9 with wording retained. Formatting/integration pending;no credit.')

if __name__=='__main__':main()
