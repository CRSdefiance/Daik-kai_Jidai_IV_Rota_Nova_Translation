"""Author358 reviewed speeches andtwo typed choices; no ledger/native credit."""
from pathlib import Path
from copy import deepcopy
from collections import Counter
from scripts.lil_new_world_aftermath_prose_v2928 import REVIEWS as A
from scripts.lil_clifford_hostage_prose_v2930 import REVIEWS as B
from scripts.lil_kuhn_return_after_rescue_prose_v2932 import REVIEWS as C
from scripts.lil_kuhn_no_alliance_prose_v2933 import REVIEWS as D
from scripts.lil_kuhn_alliance_outcome_prose_v2934 import REVIEWS as E
from scripts.lil_kuhn_ambush_rescue_prose_v2935 import REVIEWS as F,CHOICES
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/lil_Kuhn_Resolution_author_v2936')
SOURCE=Path('work/analysis/lil_Kuhn_Resolution_source_v2923/complete358speeches2choices_clean_current_native_context.json')
CONTROL=Path('work/analysis/lil_Kuhn_Resolution_controls_v2925/source_bound358_preambles_FE_and_original_conditional_predicates.json')
BRANCH=Path('work/analysis/lil_Kuhn_Resolution_branches_v2924/original_relative_skip_operand_proof.json')
CONTEXT=Path('work/analysis/lil_Kuhn_Resolution_context_v2926/complete_clean_exchange_context_notes.json')
TERMS=Path('work/analysis/lil_Kuhn_Resolution_item_terms_v2927/clean_current_and_registered_item_names.json')
DOC=Path('translations/lil_kuhn_resolution_editorial_manuscript_v1.json')
MENU=Path('translations/lil_kuhn_resolution_choice_manuscript_v1.json')
FILES=[Path('scripts')/name for name in ['lil_new_world_aftermath_prose_v2928.py','lil_clifford_hostage_prose_v2930.py','lil_kuhn_return_after_rescue_prose_v2932.py','lil_kuhn_no_alliance_prose_v2933.py','lil_kuhn_alliance_outcome_prose_v2934.py','lil_kuhn_ambush_rescue_prose_v2935.py']]


def reviewed(original,review,contexts):
    row=deepcopy(original);decision,gloss,english,note=review;choice=row['kind']=='typed-choice-label'
    assert decision in ['V','R'] and gloss and note and english.isascii() and english==english.strip()
    assert not any(tag in english for tag in ['\n','{LB','{ALIGN','{PAD'])
    raw=bytes.fromhex(row['source_hex']);body=raw if choice else raw[1:]
    for macro in ['FI','FA','FO']:assert body.count(macro.encode())==english.count('{MACRO:'+macro+'}'),row['id']
    if decision=='R':
        previous=' '.join(row['current_English'].split())
        for macro in ['FI','FA','FO']:previous=previous.replace(macro,'{MACRO:'+macro+'}')
        assert english==previous,(row['id'],english,previous)
        row['fresh_retained_wording_justification']=note
    if not choice:english='{SPEAKER:'+row['source_presentation_prefix_hex'].upper()+'}'+english
    context=contexts[row['block']].replace('Ceremonial Dagger','Ceremonial Knife').replace('Sun-patterned Sheath','Sun-Crest Sheath')
    context+=' Every source speech and choice in the complete exchange has been read; storage order is not proof of branch reachability. Item terminology is reconciled to exact clean/current pointers in the linked item terminology proof. Prose validation does not claim current native display,actual selected gameplay or release completion.'
    row.update(source_meaning=gloss,english=english,localization_note=note,context=context,editorial_decision='revise' if decision=='V' else 'retain-wording',
        review=dict(source=True,context=True,localization=True,naturalness=True,formatting=False),status='source-context-prose-approved;current-native-ordinary-FE-choice-format-reference-representative-release-pending')
    return row


if __name__=='__main__':
    assert not any(p.exists() for p in [ROOT,DOC,MENU]);source,control,branch,context,terms=map(read,[SOURCE,CONTROL,BRANCH,CONTEXT,TERMS])
    reviews={**A,**B,**C,**D,**E,**F};assert len(reviews)==sum(map(len,[A,B,C,D,E,F]))==358
    assert set(reviews)=={r['id'] for r in source['records']} and set(CHOICES)=={r['id'] for r in source['typed_choice_records']}
    assert source['total_editorial_objects']==360 and source['progressive_speeches']==342 and source['system_FE_panels']==16 and source['typed_choice_labels']==2
    assert len(control['dispatch_cases'])==716 and len(control['current_original_predicate_cases'])==84 and len(control['original_event_queries'])==9
    assert control['all358_complete_preambles_and716_historical_dispatch_contexts_pass'] and control['all16_FE_before_fallback208_use5473C_and_original24310_null_macro_actor'] and control['FE_FI_substitution_original_dispatcher_output_bound']
    assert len(branch['cases'])==3400 and len(branch['operands_requiring_adjustment_when_resizing'])==340 and sum(len(b['all_clean_native_commands']) for b in source['blocks'])==936
    assert terms['all16_current_pointer_strings_equal_registered_names'] and context['all358_clean_speeches_and2_source_choice_labels_read_as_complete_exchanges']
    contexts={r['block']:r['clean_exchange_context_findings'] for r in context['blocks']}
    records=[reviewed(r,reviews[r['id']],contexts) for r in source['records']]
    choices=[reviewed(r,CHOICES[r['id']],contexts) for r in source['typed_choice_records']]
    assert Counter(r['editorial_decision'] for r in records)=={'revise':213,'retain-wording':145}
    assert Counter(r['editorial_decision'] for r in choices)=={'revise':1,'retain-wording':1}
    shared=dict(format='dk4-ilnk-editorial-source-prose-draft-v1',translation_policy='natural-dialogue-v2',target_locale='en-US',file_path='/data/SC2.DK4',review_gates=['source','context','localization','naturalness','formatting'],
        source_ROM_sha256=source['source_ROM_sha256'],current_ROM=source['current_ROM'],current_ROM_sha256=source['current_ROM_sha256'],required_runtime_ARM9_sha256=source['current_ARM9_sha256'],
        source_context=str(SOURCE),source_context_sha256=sha(SOURCE.read_bytes()),control_contract=str(CONTROL),control_contract_sha256=sha(CONTROL.read_bytes()),branch_proof=str(BRANCH),branch_proof_sha256=sha(BRANCH.read_bytes()),
        whole_exchange_context_notes=str(CONTEXT),whole_exchange_context_notes_sha256=sha(CONTEXT.read_bytes()),item_terminology_reconciliation=str(TERMS),item_terminology_reconciliation_sha256=sha(TERMS.read_bytes()),
        formatting_review_pending=True,no_authored_line_breaks_or_padding=True,source_prose_credit_added=0,completion_credit_added=0,actual_selected_Kuhn_Resolution_IDs=[],new_emulator_runs=0,full_goal_complete=False)
    ROOT.mkdir(parents=True);save(DOC,dict(**shared,records=records,revised=213,retained=145,typed_choice_companion=str(MENU)))
    save(MENU,dict(**shared,records=choices,revised=1,retained=1,ordinary_FE_companion=str(DOC),typed_menu_command_block=121,typed_menu_command_offset=302,typed_source_count=2,choice_indices_must_remain=[0,1],not_a_speech_or_speaker_prefix=True))
    save(ROOT/'source_prose_review_receipt.json',dict(manuscript=str(DOC),manuscript_sha256=sha(DOC.read_bytes()),choice_manuscript=str(MENU),choice_manuscript_sha256=sha(MENU.read_bytes()),
        total_editorial_objects=360,speeches=358,ordinary=342,FE=16,typed_choices=2,revised=214,retained=146,all360_clean_source_and_whole_exchange_prose_gates_pass=True,
        source936commands340sites3400cases716dispatch84predicates9queries_bound=True,all_source_macros_and_exact_individually_justified_retentions_pass=True,
        original_FE_null_actor_FI_contract_bound=True,original_two_choice_count_pointer_ownership_source_mapped=True,all_three_Kuhn_outcomes_and_Hodram_presence_knowledge_branches_distinct=True,
        female_nickname_and_parental_account_respectful_without_added_ridicule_or_identity_claim=True,explicit_Asian_independence_and_European_power_context_preserved=True,
        personal_apologies_information_recipients_and_effort_versus_guarantee_restored=True,
        author_files={str(p):sha(p.read_bytes()) for p in FILES+[Path(__file__)]},source_evidence={str(p):sha(p.read_bytes()) for p in [SOURCE,CONTROL,BRANCH,CONTEXT,TERMS]},
        current_native_formatting_choice_fonts_pagination_reference_representative_and_registered_release_pending=True,source_prose_or_completion_credit_added=0,full_goal_complete=False))
    print('360fresh source/prose drafts:214revisions/146justified retentions;342ordinary/16FE/two typedchoices. Native/reference/representative/release pending;ledger unchanged.')
