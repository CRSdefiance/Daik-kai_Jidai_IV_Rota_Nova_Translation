"""Fresh whole-exchange clean-Japanese glosses before anycurrent B36 English exposure."""
from copy import deepcopy
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/maria_confrontation_gloss_v7787')
SOURCE=Path('work/analysis/maria_next_clean_v7786/complete_clean_SC3_B36_EV3_andcoverage_before_current_English.json')
PREVIOUS=Path('work/analysis/maria_story_chain_clean_v7725/complete_clean_34_108_35_67_refs_explicit_source_dependency_chain_before_current_English.json')
GLOSSES={
    5:"Actor02 asks everyone whether preparations for leaving port are ready. This is a question to the group,not a completed voyage orproof ofthe optional scene's current port.",
    9:"Actor0A recognizes the person asLil Argot,the head ofthe Argot Company. The source selector is0A,not Camille's09;do notinvent Camille attending orchanging his stated reluctance fromthe previous exchange. Preserve the recognition andleadership identification withoutadding a rank.",
    12:"Maria agrees thatthis appears tobe the person. Preserve the brief confirming response ratherthan adding a new introduction orproof.",
    16:"Maria politely interrupts andasks whether the person isAdmiral Lil Argot. Preserve the source-supported admiral title andthe direct identity question.",
    19:"Lil stammers in surprise atbeing addressed so abruptly,acknowledges sheis Lil,anddemands toknow the stranger's identity. Her casual,increasingly defensive voice contrasts withMaria's controlled manner.",
    23:"Maria identifies herself asFI ofFO andasserts thatLil cannot beunaware ofher. Retain both originalruntime tokens exactly andher confident rhetorical expectation ofrecognition;do notsubstitute a fixed personal orcompany name.",
    27:"Lil repeatsFI in startled recognition,thenasks whether that person really came directly herself. Directly coming/entering doesnot establish a naval invasion,attack orcompleted battle. Retain the same runtime FI token.",
    31:"Lil suddenly fears thatMaria mayintend tokill her. This isLil's alarmed suspicion,not a narrator's fact orMaria's intention.",
    34:"Maria denies that suspicion,says Lil seems deeply influenced byKuhn,andexplains shehascome totellLil thetruth:Kuhn isusing her. Preserve the tentative assessment ofthe influence andthe stated purpose ofthe visit. Poison imagery concerns misleading influence,not literal poisoning.",
    37:"Confused,Lil asks whatMaria means andpraisesKuhn asawonderful merchant whoistrying tosave thepeople ofSoutheastAsia. This isLil's belief inside theargument,not established truth orproof ofan actual rescue. Keep SoutheastAsia distinct fromEastAsia/China.",
    41:"Lil says sheisonlyhelpingKuhn,thenaccusesMaria ofbeing apirate whocontrolsChina's underworld. Preserve the accusation andcontempt asLil's words;do notturnit intoMaria's self-description,anarrator fact,oraclaim thatshe rulesallChina.",
    45:"Maria saysLildoesnotknowKuhn'struenature andwarns thatheintends touseherasfaraspossible andtheneliminateher. Preserve the planned future sequence andlethal context withoutinventing anassassination method,alreadyfulfilleddeath ormechanical guarantee.",
    49:"Lil callsMaria'sclaimalie,tellshernot tomakeupnonsense,anddemands proofthatKuhnisabadman,insisting shehasnone. Preserve both thedenial andthedefensive challenge;do notinvent documents,evidence possession orproof produced bythegame.",
    52:"Maria askswhetherLilstilldoesnotunderstand,stressesthatLil'slifeisatstake,andsaysthereisstilltime now. Preserve theurgency andcurrent opportunity withoutinventing adate,deadline,specific escape plan orguaranteed outcome.",
    56:"Lilsaysshecannotbelieve suchasuddenclaim,andendswitha dismissivesnort. This isrejection ofunproven accusations,not acceptance,aforgivenmisunderstanding orapromise toinvestigate.",
    60:"Maria responds withanexasperated aside callingLilayoungwoman/girlwhoisunwilling orslowtounderstand. 娘isnot Maria'sdaughter;do notinvent kinship,callLilachild,oraddromance,motives orachange ofmind.",
}
CONTEXT="""Lil ispreparing toleaveport;actor0A identifiesherasArgot's leader. Maria approaches politely butconfidently,introducesherself,andisrecognized. Lil'ssurpriseturns tofearofassassination. Maria deniesthat,thenwarnsthatshemisunderstandsKuhn. LilpraisesKuhn'ssupposedhelpforSoutheastAsia'speople andaccusesMariaofpiracyinChina. MariawarnsofKuhn'sintendeduseandeliminationofLil;Lildemandsproofandrejectsthesuddenclaim. Maria'sfinalasideisexasperation,notreconciliation. ThepriorB35 dialogueexplainsMaria'sdesireforadirectmeeting andtentativeBatavia whereabouts;theEV3prerequisite35->36 doesnotproveimmediatechronology,currenttown,naturalactivation,allotherconditionsorCamille'spresence."""
if __name__=='__main__':
    assert not ROOT.exists();source,previous=map(read,[SOURCE,PREVIOUS]);group=source['groups'][0]
    assert group['block']==36 and len(group['records'])==16 and not group['completed_coverage_overlap']
    event=group['source_event_records'][0]
    assert (event['event_ID'],event['action_index'],event['script_block'],event['must_be_completed'],event['must_not_be_completed'])==(36,37,36,[35],[])
    assert source['source_only_no_current_English_exposed_orused'] and not source['inventory_failures']
    rows=deepcopy(group['records']);assert {r['source_record_index'] for r in rows}==set(GLOSSES)
    for row in rows:
        row.update(source_gloss=GLOSSES[row['source_record_index']],full_clean_exchange_context=CONTEXT,
            source_gloss_mode='freshly authored fromcomplete clean Japanese before current English',
            source_gloss_not_current_English_derived=True,review=dict(source=True,context=True,localization=False,naturalness=False,formatting=False),
            native_name_macro_control_current_English_anddisplay_gates_pending=True,new_source_prose_orcompletion_credit=0)
    assert {r['source_selector'] for r in rows}=={2,3,10}
    assert sum(bytes.fromhex(r['source_hex'])[1:].count(b'FI') for r in rows)==2
    assert sum(bytes.fromhex(r['source_hex'])[1:].count(b'FO') for r in rows)==1
    assert not any(b'FA' in bytes.fromhex(r['source_hex'])[1:] for r in rows)
    ROOT.mkdir(parents=True);save(ROOT/'sixteen_clean_whole_exchange_glosses_before_current_English.json',dict(
        source_packet=str(SOURCE),source_packet_sha256=sha(SOURCE.read_bytes()),source_ROM=source['source_ROM'],source_ROM_sha256=source['source_ROM_sha256'],
        file_path=group['file_path'],block=36,clean_block_sha256=group['clean_block_sha256'],records=rows,complete_clean_exchange_context=CONTEXT,
        original_EV3_event=event,prior_source_context=str(PREVIOUS),prior_source_context_sha256=sha(PREVIOUS.read_bytes()),
        full_clean_Japanese_exchange_read_before_current_English=True,all16_fresh_source_glosses_written_before_localized_prose=True,
        source_0A_not_Camille09_identity_assumption=True,all_current_English_bodies_unread=True,
        no_fixed_substitution_for_two_FI_one_FO_tokens=True,no_ROM_ledger_registry_name_asset_orcredit_change=True,
        evidence={str(p):sha(p.read_bytes()) for p in [SOURCE,PREVIOUS,Path(__file__)]},new_credit=0,new_emulator_runs=0,full_goal_complete=False))
    print('Maria B36:16fresh whole-exchange clean glosses;actors02/03/0A;FI2/FO1;original35->36dependency.CurrentEnglish stillunread;zero credit.')
