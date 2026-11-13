"""Record all32 B175 contextual decisions; native/display/release gates stay open."""
from collections import Counter
from copy import deepcopy
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts import lil_B175_prose_v4513 as prose
from scripts.verify_village_wrap_v608 import read, save

ROOT=Path('work/analysis/lil_B175_author_v4514')
COMPARISON=Path('work/analysis/lil_B175_comparison_v4511/all32_current_effective_comparison_packet.json')
GLOSS=Path('work/analysis/lil_B175_clean_context_v4502/all32_complete_B175_exchange_and_fresh_glosses.json')
OUTPUT=Path('translations/lil_B175_editorial_manuscript_v1.json')

if __name__=='__main__':
    assert not ROOT.exists() and not OUTPUT.exists()
    comparison,gloss=map(read,[COMPARISON,GLOSS]);source=read(comparison['source_context'])
    assert gloss['all32_clean_source_read_and_individually_glossed_before_predecessor_English']
    assert comparison['source_context_sha256']==sha(Path(comparison['source_context']).read_bytes())
    assert len(prose.REVISIONS)==19 and len(prose.RETAIN_NOTES)==13
    assert not set(prose.REVISIONS)&set(prose.RETAIN_NOTES)
    assert set(prose.REVISIONS)|set(prose.RETAIN_NOTES)=={r['source_record_index'] for r in source['records']}
    doc=dict(format='dk4-editorial-source-prose-draft-v1',translation_policy='natural-dialogue-v2',target_locale='en-US',
        encoder='dialogue-relocatable-v1',review_gates=['source','context','localization','naturalness','formatting'],
        file_path='/data/SC2.DK4',current_ROM=source['current_ROM'],current_ROM_sha256=source['current_ROM_sha256'],
        source_ROM_sha256=source['source_ROM_sha256'],required_runtime_ARM9_sha256=source['current_ARM9_sha256'],
        source_prose_or_completion_credit_added=0,formatting_review_pending=True,
        status='source-context-localization-naturalness-reviewed;formatting-native-references-representative-release-pending',
        whole_exchange_context=gloss['whole_exchange_context'],clean_first_notes_are_historical_and_precede_current_native_bindings=True)
    dependencies={
        'source_context':comparison['source_context'],'control_contract':comparison['control_proof'],
        'whole_exchange_context_notes':str(GLOSS),
        'actor_voice_contract':'work/analysis/lil_B175_voices_v4504/current5_static_names_voices_and207_catalog_rebind.json',
        'branch_proof':'work/analysis/lil_B175_branches_v4506/original_relative_skip_operand_proof.json',
        'source_entry_proof':'work/analysis/lil_B175_entry_v4507/source_EV2_B175_action_dependency_and_native_getter_binding.json',
        'source_effect_and_predicate_contract':'work/analysis/lil_B175_controls_v4509/one_resource_three_presentations_C200_two_ends_and7_source_leaves.json',
        'actor_terminology_reconciliation':comparison['terms_binding'],
        'source_nameplate_consumer_proof':'work/analysis/lil_B175_names_v4508/ten_original_name_consumers_owned_and_readonly_paths.json',
        'effective_current_comparison':str(COMPARISON),
    }
    for key,path in dependencies.items():
        doc[key],doc[key+'_sha256']=path,sha(Path(path).read_bytes())
    speakers={2:'Lil',9:'Camille',183:'Angel',184:'Snake',185:'Dandy',254:'Woman pirate (anonymous)'}
    rows=[]
    for original in comparison['records']:
        row=deepcopy(original);old=row['current_effective_paragraph']
        for macro in ['FI','FA','FO']:
            old=old.replace(macro,'{MACRO:'+macro+'}')
        index=row['source_record_index']
        body,note=prose.REVISIONS[index] if index in prose.REVISIONS else (old,prose.RETAIN_NOTES[index])
        assert body==body.strip() and '\n' not in body and '  ' not in body and all(ord(c)<128 for c in body)
        assert '%' not in body and not any(tag in body for tag in ['{LB','{PAD','{SPEAKER:'])
        for macro in ['FI','FA','FO']:
            assert bytes.fromhex(row['source_hex']).count(macro.encode())==body.count('{MACRO:'+macro+'}')
        decision='retain-wording' if body==old else 'revise'
        assert (decision=='revise')==(index in prose.REVISIONS)
        row.update(source_meaning=row['fresh_source_gloss'],english='{SPEAKER:'+format(row['source_selector'],'02X')+'}'+body,
            localization_note=note,editorial_decision=decision,current_stored_English=row['current_raw_storage_English'],
            effective_predecessor_paragraph=old,
            comparison_basis='Original native macro template;NFKC presentation forms and collapsed legacy whitespace;raw/effective provenance remains distinct.',
            review=dict(source=True,context=True,localization=True,naturalness=True,formatting=False),
            context=gloss['whole_exchange_context'],speaker=speakers[row['source_selector']],prose_author_module=str(Path(prose.__file__)),
            status=doc['status'],editorial_predecessor_English_comparison_pending=False,full_clean_context_precedes_comparison=True,
            current_macro_dispatch_bound=True,current_complete_native_display_pending=True,current_native_UI_body_explicit_unexecuted_boundary=True,
            current_effective_native_dispatch_proof=comparison['control_proof'],
            original_native_display_consumer='original_null_actor_24310_then5473C_FE' if row['kind']=='system-FE' else 'original_progressive_54020')
        if decision=='retain-wording':row['fresh_retained_wording_justification']=note
        rows.append(row)
    counts=Counter(r['editorial_decision'] for r in rows)
    assert counts=={'revise':19,'retain-wording':13}
    assert sum(r['kind']=='system-FE' for r in rows)==9 and len(rows)==32
    doc.update(manuscript_kind='speech',prose_companions=[],records=rows,revised=19,retained=13)
    ROOT.mkdir(parents=True);save(OUTPUT,doc)
    save(ROOT/'all32_clean_first_contextual_decisions.json',dict(manuscript=str(OUTPUT),manuscript_sha256=sha(OUTPUT.read_bytes()),
        decision_counts=dict(counts),source_context=comparison['source_context'],source_context_sha256=comparison['source_context_sha256'],
        all32_clean_then_current_whole_exchange_read=True,all13_retentions_individually_justified=True,
        source_context_localization_naturalness_gates_true_formatting_false=True,
        five_static_names_bound_and_FE_woman_and_sword_unnamed=True,
        source_FI4_FA1_FO0_preserved=True,admiral_source_rank_preserved_without_new_commission=True,
        recognition_danger_pirate_pride_defiance_sword_mystery_relief_teasing_and_worry_progression_preserved=True,
        no_boss_Captain_relationship_sword_power_or_earned_pursuit_added=True,
        evidence={str(p):sha(p.read_bytes()) for p in [COMPARISON,GLOSS,Path(prose.__file__),Path(__file__)]},
        new_emulator_runs=0,source_prose_or_completion_credit_added=0,no_ROM_registry_ledger_change=True,full_goal_complete=False))
    print(dict(objects=32,progressive=23,FE=9,decisions=dict(counts),FI=4,FA=1,FO=0,formatting_pending=True,credit=0))
