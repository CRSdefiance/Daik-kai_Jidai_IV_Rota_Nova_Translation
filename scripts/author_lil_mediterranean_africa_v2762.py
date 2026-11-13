"""Fresh complete-exchange source/prose pass for152 Mediterranean/Africa objects."""
from pathlib import Path
from copy import deepcopy
from collections import Counter
from scripts.lil_mediterranean_silveira_prose_v2762 import REVIEWS as WEST
from scripts.lil_sofala_prose_v2762 import REVIEWS as EAST
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/lil_Mediterranean_Africa_author_v2762')
SOURCE=Path('work/analysis/lil_Mediterranean_Africa_source_v2759/complete152_clean_current_native_context.json')
CONTROL=Path('work/analysis/lil_Mediterranean_Africa_controls_v2761/source_bound146_preambles_FE_and_original_conditional_predicates.json')
BRANCH=Path('work/analysis/lil_Mediterranean_Africa_branches_v2760/original_relative_skip_operand_proof.json')
DOC=Path('translations/lil_mediterranean_africa_editorial_manuscript_v1.json')
CHOICE=Path('translations/lil_mediterranean_africa_choices_editorial_draft_v1.json')
CONTEXT={
20:'Complete first Hayreddin confrontation. Original alliance,recognition andcrew alternatives stay distinct. Original choice0prepares for battle andleads tothe explicit lethal order/reluctant Gerhard response;choice1flees andleads tothe reputation/ Africa strategy advice. No actual choice oroutcome is claimed.',
32:'Complete later port-worker decision,whose source event requires20. Denial is original option0andwillingness toface the Hayreddin faction is1. The hurry-away response andthe reckless/optional crew responses must not be flattened into one unconditional conversation.',
33:'Complete three-line Silveira aftermath. Native event33requires134,andthe condemned everything-in-trading-lands ownership claim is explicit inB134. This is not established bystorage adjacency toHayreddin. Keep Camille unusually-wise joke andLil personal retort coherent.',
34:'Complete first Sofala drug-discovery exchange. Medicine ambiguity precedes the named narcotic reveal. The distressed man andshopkeeper are original NPCclasses,not invented named people. Preserve the sellers exploitation,the changing prices,Lil realization andmoral resolve,andall conditional crew responses. The shopkeeper drug/fate assertions remain character speech withtheir source qualifications.',
35:'Complete Espinosa-company defeat andreward alternatives. First-customer andearlier-visit recognition paths are distinct. Do not assume the merchant died orgrant two objects byreading both alternatives consecutively. Preserve reported recovery withtime,the source philosophy andthe shopkeeper personal warm assurance,without inventing a treatment orobjective guaranteed ending.',
36:'Complete Espinosa surrender/subordination andreward alternatives. Generic crew andCamille powder reports are distinct;the latter explicitly names the warehouse. Preserve Lil personal drug-sale prohibition andthe live Espinosa reply,not a death. Repeated ban/acknowledgment anddifferent shopkeeper paths are separately reviewed source objects,not duplicate unconditional speeches orgifts.',
134:'Complete first West-African Silveira confrontation. Keep the legitimate town-contract argument andSilveira absurd ownership claim,whichB33later condemns. Withdrawal is original option0;defiance is1. The withdrawal branch has extorted small market-share loss inSaoJorge,one anonymous FEsystem report andLil private vow. The defiant branch has Camille spoken agreement/private concern andthe final threat. Never invent kinship fromojisan/oyaji orshift the limited loss tothe whole town.'
}

if __name__=='__main__':
    assert not ROOT.exists() and not DOC.exists() and not CHOICE.exists()
    source,control,branch=map(read,[SOURCE,CONTROL,BRANCH]);reviews={**WEST,**EAST}
    assert not set(WEST)&set(EAST) and len(WEST)==54 and len(EAST)==98 and len(reviews)==152
    originals=source['records']+source['typed_choice_records'];assert len(originals)==152 and set(reviews)=={r['id'] for r in originals}
    assert control['all146_complete_preambles_and292_historical_dispatch_contexts_pass'] and len(control['current_original_predicate_cases'])==28
    assert len(branch['cases'])==1240 and len(branch['operands_requiring_adjustment_when_resizing'])==124
    assert source['blocks'][1]['original_event_source']['must_be_completed']==[20] and source['blocks'][2]['original_event_source']['must_be_completed']==[134]
    speech=[];choices=[]
    for original in originals:
        row=deepcopy(original);decision,gloss,english,note=reviews[row['id']];typed=row['kind']=='typed-choice-label'
        assert decision in ['V','R'] and gloss and english and note
        assert english.isascii() and english==english.strip() and '\n' not in english and '{LB' not in english and '{PAD}' not in english and '{ALIGN' not in english
        authored=english if typed else '{SPEAKER:'+row['source_presentation_prefix_hex'].upper()+'}'+english
        row.update(source_meaning=gloss,english=authored,localization_note=note,
            context=CONTEXT[row['block']]+' Source packet includes every native speech/choice inthese seven linked exchanges;storage neighbors alone do not prove consecutive reachability.',
            editorial_decision='revise' if decision=='V' else 'retain-wording',
            review=dict(source=True,context=True,localization=True,naturalness=True,formatting=False),
            status='source-context-prose-approved;current-native-formatting-reference-representative-release-pending')
        if decision=='R':
            retained=' '.join(row['current_English'].split())
            for macro in ['FI','FA','FO']:retained=retained.replace(macro,'{MACRO:'+macro+'}')
            assert english==retained,(row['id'],english,retained)
            row['fresh_retained_wording_justification']=note
        for macro in ['FI','FA','FO']:
            raw=bytes.fromhex(row['source_hex']);raw=raw if typed else raw[1:]
            assert raw.count(macro.encode())==english.count('{MACRO:'+macro+'}'),(row['id'],macro)
        if typed:choices.append(row)
        else:speech.append(row)
    assert len(speech)==146 and len(choices)==6 and sum(r['kind']=='system-FE' for r in speech)==1
    base=dict(translation_policy='natural-dialogue-v2',target_locale='en-US',file_path='/data/SC2.DK4',
        review_gates=['source','context','localization','naturalness','formatting'],source_ROM_sha256=source['source_ROM_sha256'],
        current_ROM=source['current_ROM'],current_ROM_sha256=source['current_ROM_sha256'],required_runtime_ARM9_sha256=source['current_ARM9_sha256'],
        source_context=str(SOURCE),source_context_sha256=sha(SOURCE.read_bytes()),control_contract=str(CONTROL),control_contract_sha256=sha(CONTROL.read_bytes()),
        branch_proof=str(BRANCH),branch_proof_sha256=sha(BRANCH.read_bytes()),formatting_review_pending=True,source_prose_credit_added=0,completion_credit_added=0,
        no_authored_line_breaks_or_padding=True,actual_selected_Mediterranean_Africa_IDs=[],new_emulator_runs=0,full_goal_complete=False)
    ROOT.mkdir(parents=True)
    for path,records,format in [(DOC,speech,'dk4-ilnk-editorial-source-prose-draft-v1'),(CHOICE,choices,'dk4-native-typed-choice-source-prose-draft-v1')]:
        counts=Counter(r['editorial_decision'] for r in records)
        save(path,dict(**base,format=format,records=records,revised=counts['revise'],retained=counts['retain-wording']))
    counts=Counter(r['editorial_decision'] for r in speech+choices)
    sources=[Path(__file__),Path('scripts/lil_mediterranean_silveira_prose_v2762.py'),Path('scripts/lil_sofala_prose_v2762.py')]
    save(ROOT/'source_prose_review_receipt.json',dict(manuscript=str(DOC),manuscript_sha256=sha(DOC.read_bytes()),choices=str(CHOICE),choices_sha256=sha(CHOICE.read_bytes()),
        total=152,speeches=146,progressive=145,FE_panels=1,typed_labels=6,revised=counts['revise'],retained=counts['retain-wording'],
        all152_clean_Japanese_and_complete_exchanges_reviewed=True,event20_to32_and134_to33_context_source_bound=True,
        defeat_surrender_reward_and_crew_alternatives_not_flattened=True,formatting_reference_representative_registered_release_pending=True,
        source_prose_credit_added=0,completion_credit_added=0,author_files={str(p):sha(p.read_bytes()) for p in sources},full_goal_complete=False))
    print(f'152fresh source/prose reviews authored:{counts["revise"]}revisions/{counts["retain-wording"]}justified retentions;145progressive/1FE/six typed labels. Full native formatting/reference/release pending;no credit yet.')
