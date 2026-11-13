"""Author82 complete-exchange reviews; no coverage credit or ROM changes."""
from pathlib import Path
from copy import deepcopy
from collections import Counter
from scripts.lil_kuhn_invitation_report_prose_v2849 import REVIEWS as A
from scripts.lil_kuhn_negotiation_prose_v2849 import REVIEWS as B
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/lil_Kuhn_Alliance_author_v2850')
SOURCE=Path('work/analysis/lil_Kuhn_Alliance_source_v2846/complete82_clean_current_native_context.json')
CONTROL=Path('work/analysis/lil_Kuhn_Alliance_controls_v2848/source_bound82_preambles_and_original_conditional_predicates.json')
BRANCH=Path('work/analysis/lil_Kuhn_Alliance_branches_v2847/original_relative_skip_operand_proof.json')
DOC=Path('translations/lil_kuhn_alliance_editorial_manuscript_v1.json')
CONTEXT={47: 'Complete invitation to Batavia tavern with Jam optional self-important joke and separate pain reaction, Lil confirmation and private consultation with Camille. Preserve both FI and FA, curiosity, suspicion, his reluctance and leaving the decision to Lil. Native56 is Georg, Kuhn envoy, not a new unnamed rank. Do not disclose the later alliance terms or invent who hits Jam.', 48: 'Complete public alliance negotiation with all stored crew alternatives. Event48 requires47. Georg courteous business pitch,5000 currency-gold offer and anti-Pereira allegations are character claims, not independently verified fact or earned benefits. Preserve the change from Lil skepticism to interest, Camille private shock at Kuhn, his shaking hands and repeated failed explanations, allegations and crew disbelief/uncertainty, his hurt that even Lil doubts him, departure, unwanted restraint and pressured signature. Do not invent Pereira ties, disclose the father relationship here, make private thoughts audible, diagnose distress, name an attacker or explain the unspecified later scheme. Approved Camille and every runtime substitution remain exact.', 49: 'Complete private report to Antony Kuhn after event48. Event49 requires48. Georg reports the pact, suspects identity upon hearing Camille and then recognizes Marinus face; Kuhn complains about the feminine nickname and asks his condition. Preserve Marinus opposition, Georg repeated anxiety, unspecified prior arrangements and confident prediction of no return, and Kuhn trailing reservation. These are private statements, not knowledge granted to Lil or proof of a death. Polite sama does not confer a Lord rank. The feminine-name remark remains Kuhn source characterization; add no slur or modern identity explanation, and keep approved Camille.', 50: 'Complete later alliance approach. Event50 requires48 and must not follow54/121/55/56; preserve the stored alternative rather than treating it as an unconditional second simultaneous pact. Keep the elapsed-time greeting, recognition of Kuhn envoy, request, hesitant assent and courteous expectation of continued cooperation. No unspoken new payment, terms, earned company change or tested future outcome is supplied.'}
if __name__=='__main__':
    assert not ROOT.exists() and not DOC.exists()
    source,control,branch=map(read,[SOURCE,CONTROL,BRANCH]);reviews={**A,**B}
    assert len(A)==26 and len(B)==56 and not set(A)&set(B) and len(reviews)==82
    assert set(reviews)=={r['id'] for r in source['records']} and source['typed_choice_records']==[]
    assert control['all82_complete_preambles_and164_historical_dispatch_contexts_pass'] and len(control['current_original_predicate_cases'])==15
    assert [(q['block'],q['offset'],q['event']) for q in control['original_event_queries']]==[]
    assert len(branch['cases'])==600 and len(branch['operands_requiring_adjustment_when_resizing'])==60
    records=[]
    for original in source['records']:
        row=deepcopy(original);decision,gloss,english,note=reviews[row['id']]
        assert decision in ['V','R'] and gloss and english and note and english.isascii() and english==english.strip()
        assert not any(tag in english for tag in ['\n','{LB','{PAD','{ALIGN'])
        for macro in ['FI','FA','FO']:assert bytes.fromhex(row['source_hex'])[1:].count(macro.encode())==english.count('{MACRO:'+macro+'}'),row['id']
        row.update(source_meaning=gloss,english='{SPEAKER:'+row['source_presentation_prefix_hex'].upper()+'}'+english,localization_note=note,context=CONTEXT[row['block']]+' Every stored speech in the complete source block is reviewed; storage order alone does not establish branch reachability.',editorial_decision='revise' if decision=='V' else 'retain-wording',review=dict(source=True,context=True,localization=True,naturalness=True,formatting=False),status='source-context-prose-approved;current-native-format-reference-representative-release-pending')
        if decision=='R':
            previous=' '.join(row['current_English'].split())
            for macro in ['FI','FA','FO']:previous=previous.replace(macro,'{MACRO:'+macro+'}')
            assert english==previous,(row['id'],english,previous);row['fresh_retained_wording_justification']=note
        records.append(row)
    counts=Counter(r['editorial_decision'] for r in records);rev=counts['revise'];ret=counts['retain-wording']
    doc=dict(format='dk4-ilnk-editorial-source-prose-draft-v1',translation_policy='natural-dialogue-v2',target_locale='en-US',file_path='/data/SC2.DK4',review_gates=['source','context','localization','naturalness','formatting'],source_ROM_sha256=source['source_ROM_sha256'],current_ROM=source['current_ROM'],current_ROM_sha256=source['current_ROM_sha256'],required_runtime_ARM9_sha256=source['current_ARM9_sha256'],source_context=str(SOURCE),source_context_sha256=sha(SOURCE.read_bytes()),control_contract=str(CONTROL),control_contract_sha256=sha(CONTROL.read_bytes()),branch_proof=str(BRANCH),branch_proof_sha256=sha(BRANCH.read_bytes()),records=records,revised=rev,retained=ret,formatting_review_pending=True,no_authored_line_breaks_or_padding=True,source_prose_credit_added=0,completion_credit_added=0,actual_selected_Kuhn_Alliance_IDs=[],new_emulator_runs=0,full_goal_complete=False)
    ROOT.mkdir(parents=True);save(DOC,doc)
    assert (rev,ret)==(63,19)
    save(ROOT/'source_prose_review_receipt.json',dict(manuscript=str(DOC),manuscript_sha256=sha(DOC.read_bytes()),total=82,progressive=82,FE_panels=0,typed_labels=0,revised=rev,retained=ret,all82_clean_Japanese_and_complete_exchanges_reviewed=True,all195_commands60_relative_sites600_cases15_predicates_and164_historical_dispatch_contexts_bound=True,no_8100_event_queries_in_selected_commands=True,original_EV2_dependency47_48_and_forbidden54_121_55_56_bound=True,Georg_and_Antony_Kuhn_catalog_identity_bound_without_new_nameplate_claim=True,public_negotiation_private_report_and_later_approach_distinct=True,private_shock_and_allegations_not_new_fact=True,all_63_revisions19_retentions_source_macro_and_ASCII_preflight_pass=True,formatting_reference_representative_registered_release_pending=True,author_files={str(p):sha(p.read_bytes()) for p in [Path(__file__),Path('scripts/lil_kuhn_invitation_report_prose_v2849.py'),Path('scripts/lil_kuhn_negotiation_prose_v2849.py')]},source_prose_credit_added=0,completion_credit_added=0,full_goal_complete=False))
    print(f'82 fresh source/prose reviews: {rev} revisions/{ret} justified retentions. Native format/reference/representative/release pending; zero ledger credit.')
