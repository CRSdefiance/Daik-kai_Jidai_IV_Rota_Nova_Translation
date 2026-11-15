"""Author 90 complete-exchange reviews; no coverage credit or ROM changes."""
from pathlib import Path
from copy import deepcopy
from collections import Counter
from scripts.lil_polder_source_goods_prose_v2823 import REVIEWS as A
from scripts.lil_mediterranean_outcomes_prose_v2823 import REVIEWS as B
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/lil_Goods_Mediterranean_author_v2823')
SOURCE=Path('work/analysis/lil_Goods_Mediterranean_source_v2820/complete90_clean_current_native_context.json')
CONTROL=Path('work/analysis/lil_Goods_Mediterranean_controls_v2822/source_bound90_preambles_and_original_conditional_predicates.json')
BRANCH=Path('work/analysis/lil_Goods_Mediterranean_branches_v2821/original_relative_skip_operand_proof.json')
DOC=Path('translations/lil_goods_mediterranean_editorial_manuscript_v1.json')
CONTEXT={
41:"Complete governor's office completion, gift and continuing funding exchange, following B40. Event41 requires completed40. Preserve the 400,000 currency gold gift, student gratitude, further investment needs and mutual encouragement. Do not confuse this currency with the earlier three holds of commodity gold, name a new governor, infer town ownership or claim actual tested construction, payment or later development.",
43:"Complete source-item discovery and usage exchange with every stored companion alternative. Source items create new trade goods when given at a suitable Market; they are distinct from ordinary raw-material commodities. Preserve the merchant initiating the request, Lil choice whether to give it, several suitable towns, any faction access, and the strategic market-share and profit explanation. Julio old-fellow self-description is his voice, not an invented rank. Do not add the separate help topic five-specialty limit where unspoken. Existing reviewed help Source Items and Market terminology is bound by the ancillary source evidence; the older Local Product item-category wording remains an uncredited future reconciliation lead.",
44:"Complete alternative return plans after trade success in Africa and India, not Asia generally. Event44 requires43. Preserve the distinct proposals to introduce goods to the Mediterranean or challenge Hayreddin, crew alternatives and Lil private impression of Camille dependable/manly presence. Both original event queries are completion20 at offsets160 and476, not a father-reveal assumption. No romantic relationship, actual voyage, battle or earned territorial control is newly verified by this prose review.",
45:"Complete Hayreddin outcome exchange. Familiar and less-familiar fallen-faction reports retain their qualifications, distinct from the subordination and crew-praise branch. Preserve Lil confidence, Camille transition-of-trade reflection, Gerhard advice and later reassessment, Julio measured admonition, Fernando luck-versus-current-ability reasoning, Lil crew credit and their return credit to her leadership. Her parenthesized impression of Camille remains private, not an invented romance. Preserve the final port-object presentation and tentative map identification without supplying contents or a destination. Native151 is a crew reporter class, not an earned First Mate.",
46:"Complete Pasha outcome exchange. Keep familiar/rumored fallen-forces reactions separate from subordination under FO and object delivery by Pasha subordinates. Compare faction strength, not individual physical strength. Preserve this-object presentations, Lil question, tentative treasure identification, uncertainty and apparent armor value, and Fernando/Cesare alternatives. Remove invented male sir address to Lil; no named item, price, courier gender, new rank or actual gift receipt is inferred."
}
if __name__=='__main__':
    assert not ROOT.exists() and not DOC.exists()
    source,control,branch=map(read,[SOURCE,CONTROL,BRANCH]);reviews={**A,**B}
    assert len(A)==52 and len(B)==38 and not set(A)&set(B) and len(reviews)==90
    assert set(reviews)=={r['id'] for r in source['records']} and source['typed_choice_records']==[]
    assert control['all90_complete_preambles_and180_historical_dispatch_contexts_pass'] and len(control['current_original_predicate_cases'])==32
    assert [(q['block'],q['offset'],q['event']) for q in control['original_event_queries']]==[(44,160,20),(44,476,20)]
    assert len(branch['cases'])==1280 and len(branch['operands_requiring_adjustment_when_resizing'])==128
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
    doc=dict(format='dk4-ilnk-editorial-source-prose-draft-v1',translation_policy='natural-dialogue-v2',target_locale='en-US',file_path='/data/SC2.DK4',review_gates=['source','context','localization','naturalness','formatting'],source_ROM_sha256=source['source_ROM_sha256'],current_ROM=source['current_ROM'],current_ROM_sha256=source['current_ROM_sha256'],required_runtime_ARM9_sha256=source['current_ARM9_sha256'],source_context=str(SOURCE),source_context_sha256=sha(SOURCE.read_bytes()),control_contract=str(CONTROL),control_contract_sha256=sha(CONTROL.read_bytes()),branch_proof=str(BRANCH),branch_proof_sha256=sha(BRANCH.read_bytes()),records=records,revised=rev,retained=ret,formatting_review_pending=True,no_authored_line_breaks_or_padding=True,source_prose_credit_added=0,completion_credit_added=0,actual_selected_Goods_Mediterranean_IDs=[],new_emulator_runs=0,full_goal_complete=False)
    ROOT.mkdir(parents=True);save(DOC,doc)
    save(ROOT/'source_prose_review_receipt.json',dict(manuscript=str(DOC),manuscript_sha256=sha(DOC.read_bytes()),total=90,progressive=90,FE_panels=0,typed_labels=0,revised=rev,retained=ret,all90_clean_Japanese_and_complete_exchanges_reviewed=True,all128_relative_sites_and32_predicates_source_bound=True,original_completion20_queries_source_bound=True,India_not_general_Asia_and_source_items_not_raw_goods_preserved=True,fall_and_subordination_alternatives_distinct=True,qualified_reports_and_private_asides_preserved=True,older_Local_Product_UI_terminology_remains_uncredited_lead=True,formatting_reference_representative_registered_release_pending=True,author_files={str(p):sha(p.read_bytes()) for p in [Path(__file__),Path('scripts/lil_polder_source_goods_prose_v2823.py'),Path('scripts/lil_mediterranean_outcomes_prose_v2823.py')]},source_prose_credit_added=0,completion_credit_added=0,full_goal_complete=False))
    print(f'90 fresh source/prose reviews: {rev} revisions/{ret} justified retentions. Native format/reference/representative/release pending; zero ledger credit.')
