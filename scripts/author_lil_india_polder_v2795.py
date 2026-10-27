"""Author 119 fresh whole-exchange source/prose reviews; no ledger credit yet."""
from pathlib import Path
from copy import deepcopy
from collections import Counter
from scripts.lil_india_camille_prose_v2795 import REVIEWS as A
from scripts.lil_polder_gift_prose_v2795 import REVIEWS as B
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/lil_India_Polder_author_v2795')
SOURCE=Path('work/analysis/lil_India_Polder_source_v2792/complete119_clean_current_native_context.json')
CONTROL=Path('work/analysis/lil_India_Polder_controls_v2794/source_bound119_preambles_and_original_conditional_predicates.json')
BRANCH=Path('work/analysis/lil_India_Polder_branches_v2793/original_relative_skip_operand_proof.json')
DOC=Path('translations/lil_india_polder_editorial_manuscript_v1.json')
CONTEXT={
37:'Complete India poverty/caste exchange andall stored crew alternatives. Lil notices inequality,learns the character explanation ofbirth-assigned social standing,andwants tohelp. Her conditional recollection ofthe Amsterdam polder student is original completion129atnativeoffset820;do not assume she remembers anunencountered project. No modern caste group,rank,political prescription orhistorical generalization is invented.',
38:'Complete moral-doubt exchange withCamille. The two opening versions are alternatives;nativecompletion48is queriedat316and1270forfather-related material. Do not claim48is thefulltrue-name reveal. Inthat alternative the Japanese explicitly identifiesKuhn asCamille father;keep the apology andhis private reluctance without projectingthe relationship intothe other version. Preserve the progression fromprofit/conflict andpersonal responsibility totwo peace proposals,the MaritimeSilkRoad image,qualified speculation aboutthe Proofs,legitimate authority rather than military conquest,andLil explicitscary-dad/sibling analogy. Parenthesized aside remainsprivate. ApprovedCamille andestablishedProofofConquest terminology apply;no actualruler status orartifactagency isinvented.',
39:'Complete polder follow-up,gold request andLelystad destination. Raisedfunds/helpergrowth/smallsettlement already exist inthis storyreport,butthegovernoroffice andtradingtown remain futureplans. Government demands goldinreturnforaid;the quantity ofthreeholds isfirstspokenatR47,notintheearlierquotation. Lil promises toprocuregoods;this doesnotprove actualplayercargo ordelivery. Preserve sourcefirstperson,qualification andwarmconfidence.',
40:'Complete Lelystad arrival/delivery andfutureplans. Originalevent40requires39. Preserve Camille uncertainty atapparentlyemptyland,Lil falteringconfidence,studentcallout,personalpromisedgoldreport,gratitude/modesty andconditionalinvestment/tradingtown aspiration. Do notupgradefuturegovernoroffice orinvestment intoanearned outcome. Endingencouragement ismutualeffort,notajointcompany contract.',
129:'Complete earlierAmsterdam polderintroduction,all storedcompanions andpunctuation-only reaction. Thegift-searchpreface queries originalcompletion130at12;do notmakeitunconditional. Student explainsnationality,poor farmingfamily,larger/goodland goal,dikes/enclosure/pumping,namesapolder,andestimatesabout1000000currencygold. Governmentaid already sought isnot enough. Preserve hisdetermination andLil/Gerhardencouragement without inventingdonation,exactaidamount orfinishedproject. Originalevent129mustnotfollowcompleted37;B37laterqueries129before rememberingthisperson. ResearchStudent171is anoriginalclass,notaninventednamedprofessor.',
130:'Complete Cliffordgiftpickup withoriginalletter-reading andalready-heard alternatives. Nativecompletion26at68selects sourcebranches;previousreviewedCliffordalliance context is notcreditedagain. Keep the letterhand-off,recognition/wait/objecthandoff orpriorCliffordword as alternatives,notduplicategifts. The object isakeytodecipheringthemap;do notinventitscontents,a map-screenunlock ornewreward. Barkeep92isaclassandolder-manaddress isnotliteralUncle.'
}
if __name__=='__main__':
    assert not ROOT.exists() and not DOC.exists();source,control,branch=map(read,[SOURCE,CONTROL,BRANCH]);reviews={**A,**B}
    assert len(A)==56 and len(B)==63 and not set(A)&set(B) and len(reviews)==119
    assert set(reviews)=={r['id'] for r in source['records']} and source['typed_choice_records']==[]
    assert control['all119_complete_preambles_and238_historical_dispatch_contexts_pass'] and len(control['current_original_predicate_cases'])==10
    assert [(q['block'],q['event']) for q in control['original_event_queries']]==[(37,129),(38,48),(38,48),(129,130),(130,26)]
    assert len(branch['cases'])==400 and len(branch['operands_requiring_adjustment_when_resizing'])==40
    records=[]
    for original in source['records']:
        row=deepcopy(original);decision,gloss,english,note=reviews[row['id']]
        assert decision in ['V','R'] and gloss and english and note and english.isascii() and english==english.strip()
        assert not any(tag in english for tag in ['\n','{LB','{PAD','{ALIGN'])
        for macro in ['FI','FA','FO']:assert bytes.fromhex(row['source_hex'])[1:].count(macro.encode())==english.count('{MACRO:'+macro+'}')
        row.update(source_meaning=gloss,english='{SPEAKER:'+row['source_presentation_prefix_hex'].upper()+'}'+english,localization_note=note,context=CONTEXT[row['block']]+' Every native speech inthis complete source block is reviewed;storage order alone is notbranch reachability.',editorial_decision='revise' if decision=='V' else 'retain-wording',review=dict(source=True,context=True,localization=True,naturalness=True,formatting=False),status='source-context-prose-approved;current-native-format-reference-representative-release-pending')
        if decision=='R':
            previous=' '.join(row['current_English'].split())
            for macro in ['FI','FA','FO']:previous=previous.replace(macro,'{MACRO:'+macro+'}')
            assert english==previous,(row['id'],english,previous);row['fresh_retained_wording_justification']=note
        records.append(row)
    assert Counter(r['editorial_decision'] for r in records)=={'revise':84,'retain-wording':35}
    doc=dict(format='dk4-ilnk-editorial-source-prose-draft-v1',translation_policy='natural-dialogue-v2',target_locale='en-US',file_path='/data/SC2.DK4',review_gates=['source','context','localization','naturalness','formatting'],source_ROM_sha256=source['source_ROM_sha256'],current_ROM=source['current_ROM'],current_ROM_sha256=source['current_ROM_sha256'],required_runtime_ARM9_sha256=source['current_ARM9_sha256'],source_context=str(SOURCE),source_context_sha256=sha(SOURCE.read_bytes()),control_contract=str(CONTROL),control_contract_sha256=sha(CONTROL.read_bytes()),branch_proof=str(BRANCH),branch_proof_sha256=sha(BRANCH.read_bytes()),records=records,revised=84,retained=35,formatting_review_pending=True,no_authored_line_breaks_or_padding=True,source_prose_credit_added=0,completion_credit_added=0,actual_selected_India_Polder_IDs=[],new_emulator_runs=0,full_goal_complete=False)
    ROOT.mkdir(parents=True);save(DOC,doc)
    save(ROOT/'source_prose_review_receipt.json',dict(manuscript=str(DOC),manuscript_sha256=sha(DOC.read_bytes()),total=119,progressive=119,FE_panels=0,typed_labels=0,revised=84,retained=35,all119_clean_Japanese_and_complete_exchanges_reviewed=True,original_129_48_130_26_queries_source_bound=True,conditional_father_references_and_private_aside_preserved=True,initial_million_currency_and_later_three_hold_goods_distinct=True,formatting_reference_representative_registered_release_pending=True,author_files={str(p):sha(p.read_bytes()) for p in [Path(__file__),Path('scripts/lil_india_camille_prose_v2795.py'),Path('scripts/lil_polder_gift_prose_v2795.py')]},source_prose_credit_added=0,completion_credit_added=0,full_goal_complete=False))
    print('119fresh source/prose reviews:84revisions/35justifiedretentions. Nativeformat/reference/representative/release pending;zero ledgercredit.')
