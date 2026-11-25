"""Derive actual-changing source/prose/waiver/profile policy challenges for B49."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/Rafael_B49_policy_tools_v8113')
SEMANTIC=[
 ('wrong-trade-house',5,'trade house','Guild'),
 ('reversed-Camille-rebuke',20,'Camille, stay out of it.','Camille, you make a good point.'),
 ('invented-final-warning',74,"I'm only going to say this once.",'This is your final warning.'),
 ('invented-established-trust',122,'you seem decent','you are our most trusted friend'),
 ('lost-unfinished-name-joke',142,'Hodram Ber... something','Hodram Bergstrom'),
 ('invented-given-name',158,'Clifford','James Clifford'),
 ('invented-Hanseatic-rank',175,'Martin Speyer','Admiral Martin Speyer'),
 ('lost-prospective-claim',183,"we're hoping to claim",'we already own'),
 ('wrong-contract-mechanic',187,'sign a contract with a city','conquer a city'),
 ('invented-permanent-trade-ban',192,'for a while','forever'),
 ('wrong-African-destination',238,'Africa','India'),
 ('wrong-western-New-World',244,'Head west to the New World','Head east to the New World'),
 ('invented-guaranteed-attack',259,"We've got plans of our own",'We will certainly attack you'),
 ('invented-completed-alliance',266,"You're asking us to form a pact","We've already signed a formal alliance"),
 ('reversed-pride',271,"we're asking you for a favor","you owe us your obedience"),
 ('invented-romance',275,'You really hate to lose',"You're obviously in love with me"),
 ('changed-first-FI',311,'{MACRO:FI}','{MACRO:FA}'),
 ('wrong-Valdes-country',328,'Valdes of Spain','Valdes of Portugal'),
 ('lost-prospective-Spanish-threat',331,'has its eye on','has already conquered'),
 ('invented-common-enemy-assent-on-all-paths',343,'Uh...','Yes, Valdes is our common enemy.'),
 ('invented-kinship',367,'Lil, wait!','My sister Lil, wait!'),
 ('literalized-storm-joke',381,"The storm's passed...",'The weather forecast is clear.'),
 ('reversed-grudging-loyalty',388,"I don't like it",'I approve completely'),
 ('changed-second-FI',388,'{MACRO:FI}','{MACRO:FO}'),
 ('lost-qualified-impression',392,"I bet she's scary","I know she's always violent"),
 ('lost-North-Sea-condition',405,"as long as the North Sea isn't all we have left",'because we already rule the North Sea'),
 ('lost-temporary-decision',409,'for now','forever'),
]
if __name__=='__main__':
    assert not ROOT.exists()
    source=Path('scripts/validate_Rafael_B48_policy_v8059.py').read_text('utf8')
    semantic=source[source.index('SEMANTIC='):source.index("\n\nif __name__",source.index('SEMANTIC='))]
    result=derive('scripts/validate_Rafael_B48_policy_v8059.py','scripts/validate_Rafael_B49_policy_v8113.py',{
        semantic:'SEMANTIC='+repr(SEMANTIC),
        'Rafael_B48_policy_validation_v8059':'Rafael_B49_policy_validation_v8113',
        'rafael_B48_editorial_manuscript_v4.json':'rafael_B49_editorial_manuscript_v3.json',
        'Rafael_B48_relocation_v8041/SC0_block48_RESEARCH_ONLY.bin':'Rafael_B49_relocation_v8096/SC0_block49_RESEARCH_ONLY.bin',
        'B48':'B49','blocks[48]':'blocks[49]',
        "p.max_lines==(8 if ident=='DK4_MES_B48_R0347' else 4)":"p.max_lines==4",
        "next(r for r in doc['records'] if r['id']=='DK4_MES_B48_R0347')":"next(r for r in doc['records'] if r['source_record_index']==15)",
        'len(positive)==91':'len(positive)==61',
        "sum(x['qa']['native_page_count'] for x in positive)==92":"sum(x['qa']['native_page_count'] for x in positive)==61",
        "sum(i['severity']=='warning' for x in positive for i in x['qa']['issues'])==2":"sum(i['severity']=='warning' for x in positive for i in x['qa']['issues'])==3",
        "sum(i['code']=='line-break-count' for x in positive for i in x['qa']['issues'])==37":"sum(i['code']=='line-break-count' for x in positive for i in x['qa']['issues'])==22",
        '91_speech92_page_positives_actual_changing_expected_guard_rejections.json':'61_speech61_page_positives_actual_changing_expected_guard_rejections.json',
        'all_original_QA_diagnostics_preserved_37_infos_two_exact_warning_exceptions':'all_original_QA_diagnostics_preserved_22_infos_three_exact_warning_exceptions',
        'R347_only_second_page_andsource00_body_guard_preserved':'all61_single_pages_andallseven_source_selectors_source00_body_guard_preserved',
        'thirteen_native_only_speeches_andall_actual_measured_limits_retained':'eleven_native_only_speeches_andall_actual_measured_limits_retained',
        'B48:91 exact speech positives/92 pages;':'B49:61 exact speech positives/61 pages;',
        '37 infos/2 narrow warning exceptions unchanged.':'22 infos/3 narrow warning exceptions unchanged.',
    })
    ROOT.mkdir(parents=True);save(ROOT/'source_locked_derivation.json',result)
    print('Prepared B49 policy positives and actual-changing semantic/source/profile/waiver challenges.')
