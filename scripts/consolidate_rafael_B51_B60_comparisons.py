"""Save four caption decisions and249 contextual reviews, leaving display gates pending."""
import struct
from copy import deepcopy
from pathlib import Path
from dk4tool.dialogue.reviewed_choice_object_v2 import labels
from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load, save
from scripts.gloss_rafael_B51_B59_clean import ROOT

CURRENT=Path('work/analysis/Rafael_B51_B60_current_20261104/current_effective.json')

if __name__=='__main__':
    output=ROOT/'B51_B60_249_contextual_prose_review_v1.json'
    captions_path=ROOT/'B60_four_choice_comparisons_v1.json'
    assert not output.exists() and not captions_path.exists()
    source_path=ROOT/'B60_four_choice_drafts_v1.json';source=load(source_path)
    current=load(CURRENT);group=next(g for g in current['groups'] if g['block']==60)
    maps={c['source_offset']:c for c in group['command_map'] if c['word']==8448}
    captions=[]
    for draft in source['records']:
        mapping=maps[draft['source_command_offset']];raw=bytes.fromhex(mapping['current_hex'])
        index=draft['source_index'];values=labels(raw);value=values[index]
        relative=6+struct.unpack_from('<HH',raw,2)[index]
        assert raw[relative:relative+len(value)+1]==value+b'\0'
        text=' '.join(value.decode('cp932').split())
        revision=draft['source_command_offset']==1852
        reason=('Correct Koon to the established Kuhn name andmake the first proposal a natural Let’s answer.' if index==0 else
            'Correct only Koon to Kuhn;retain the natural collective promise to leave this enemy to Pereira.') if revision else (
            'Spain,which seized Portugal naturally answers the true-enemy question andpreserves the source’s stated grievance.' if index==0 else
            'The hesitant We don’t know naturally admits the group’s uncertainty in answer to Pereira’s question;no extra motive isneeded.')
        english=("Let's defeat Kuhn first." if index==0 else "We'll leave Kuhn to you.") if revision else text
        row=deepcopy(draft);row.update(english=english,logical_English=english,current_hex=value.hex(),
            current_choice_object_hex=raw.hex(),current_stored_text=value.decode('cp932'),current_comparison_paragraph=text,
            current_reference=dict(file_path='/data/SC0.DK4',block=60,command_offset=mapping['current_offset'],
                source_index=index,offset=mapping['current_offset']+relative,length=len(value)),
            decision='revision' if revision else 'retention',finding=reason,retention_reason=None if revision else reason,
            source_first_draft_English=draft['english'],source_first_draft_reference=dict(path=str(source_path),sha256=sha(source_path.read_bytes()),id=draft['id']),
            current_English_comparison_pending=False,earlier_English_unconsulted=False,current_English_now_exposed=True,
            source_andcurrent_typed_choice_indices_preserved=True,current_ROM=current['current_ROM'],current_ROM_sha256=current['current_ROM_sha256'])
        captions.append(row)
    save(captions_path,dict(records=captions,compared=4,proposed_revisions=2,justified_retentions=2,
        whole_paired_alternatives_reviewed=True,all_four_prose_gates_pass=True,all_fifth_formatting_gates_pending=True,
        source=str(source_path),source_sha256=sha(source_path.read_bytes()),current=str(CURRENT),current_sha256=sha(CURRENT.read_bytes()),new_credit=0))
    parts=[ROOT/'B51_B59_146_whole_exchange_comparison_v1.json',ROOT/'B60_99_whole_exchange_comparison_v1.json']
    rows=[deepcopy(r) for p in parts for r in load(p)['records']]
    refinements={
        'DK4_MES_B57_R0095':('Of course. We’re crewmates, aren’t we?',
            'Use crewmates for 仲間 in this reassurance,preserving warmth without implying a relationship beyond their shared crew.'),
        'DK4_MES_B60_R0041':("All right. Come on.",
            'Keep Pereira’s blunt invitation without adding a specific instruction to follow him somewhere.'),
    }
    for row in rows:
        if row['id'] in refinements:
            english,reason=refinements[row['id']];english=english.replace('’',"'")
            assert row['decision']=='revision'
            row['contextual_refinement']=dict(previous_proposal=row['english'],reason=reason)
            row.update(english=english,logical_English=english,localization_note=reason,finding=reason)
    rows+=captions
    assert len(rows)==249 and len({r['id'] for r in rows})==249
    assert all(r['review']==dict(source=True,context=True,localization=True,naturalness=True,formatting=False) for r in rows)
    assert (sum(r['decision']=='revision' for r in rows),sum(r['decision']=='retention' for r in rows))==(102,147)
    assert sum(r.get('glyph_finding',{}).get('count',0) for r in rows)==3
    save(output,dict(format='dk4-contextual-prose-review-v1',translation_policy='natural-dialogue-v2',target_locale='en-US',
        file_path='/data/SC0.DK4',blocks=list(range(51,61)),records=rows,compared=249,
        speeches=245,typed_choice_captions=4,proposed_revisions=102,justified_retentions=147,
        wording_retentions_with_scoped_glyph_corrections=2,full_width_I_glyphs_to_correct=3,
        all_four_individual_prose_gates_pass=True,all_fifth_formatting_gates_pending=True,
        full_source_preamble_native_context_stored_display_visual_gameplay_andregistered_integration_pending=True,
        completed_coverage_credit=0,guide_photos=False,full_goal_complete=False,
        separate_name_field_findings=[dict(actor_ID=35,field='given name',finding='Full-width F in Fernan;exclusive field/glyph correction pending.'),
            dict(actor_ID=40,field='middle name',finding='Full-width F andFong/von adaptation require scoped review;not an automatic name change.')],
        important_source_corrections=['Military summons affiliation','Albuquerque Lord invention','Silveira reward/purchased-gift joke',
            'Untranslated Rafael reaction','Future Africa conquest presented as already complete','Emilio confined indoors,not stuck in town',
            'Uddin first-person introductions','Registered Evergreen Lotus Leaf/Rigveda/Kuhn terms',
            'Spain-king hypotheticals andpermanent succession rights','Mediterranean Proof misidentified as this sea'],
        current_ROM=current['current_ROM'],current_ROM_sha256=current['current_ROM_sha256'],new_credit=0,
        evidence={str(p):sha(p.read_bytes()) for p in [*parts,source_path,captions_path,CURRENT,
            ROOT/'B51_B60_source_identity_checkpoint_v1.json',ROOT/'B51_B60_exact_named_references_v1.json',Path(__file__)]}))
    print('249 contextual prose reviews saved:102 revisions/147 retentions;three I glyph fixes/two separate name findings;display pending,zero credit.')
