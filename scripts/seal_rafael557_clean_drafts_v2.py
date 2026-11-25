"""Combine the complete clean-first intake,correct source nuances andpreserve exact runtime tokens."""
from copy import deepcopy
from pathlib import Path
import re
from scripts.audit_story_glyph_consistency import load,save
from dk4tool.patch.grand_race_menu_release import sha

ROOT=Path('work/analysis/Rafael_B141_B160_clean_20261105')
INPUTS=[ROOT/p for p in ['B141_B145_meanings_andindependent_drafts_v1.json',
    'B146_B151_meanings_andindependent_drafts_v1.json','B152_B156_meanings_andindependent_drafts_v1.json',
    'B157_B160_meanings_andindependent_drafts_v2.json']]


def main():
    output=ROOT/'all557_meanings_andindependent_drafts_v2.json'
    census_path=ROOT/'source_census_anddraft_qualification_v2.json'
    assert not output.exists() and not census_path.exists()
    packet_path,style_path,choice_path=[ROOT/p for p in ['clean_source_packet.json','clean_style_objects.json','clean_choice_objects.json']]
    packet,styles,choices=map(load,[packet_path,style_path,choice_path])
    source=[r for g in packet['groups'] for r in g['records']]+styles['records']+choices['records']
    assert (len(source),packet['records'],len(styles['records']),len(choices['records']))==(557,549,0,8)
    docs=list(map(load,INPUTS));rows=[deepcopy(r) for d in docs for r in d['records']]
    indexed={(r['file_path'],r['id']):r for r in rows}
    assert len(rows)==len(indexed)==557 and set(indexed)=={(r['file_path'],r['id']) for r in source}
    for original in source:
        row=indexed[(original['file_path'],original['id'])]
        assert all(row[k]==v for k,v in original.items()),original['id']
        assert not any(row['review'].values()) and len(row['review'])==5
    contexts={k:v for d in docs for k,v in d['source_contexts'].items()}
    changes=[]
    def amend(ident,text,reason):
        row=indexed[('/data/SC0.DK4',ident)];before=row['independent_English'];assert before!=text
        row['independent_English']=text
        changes.append(dict(id=ident,source_reference=row['source_reference'],source_hex=row['source_hex'],
            before=before,after=text,source_fidelity_orlocalization_reason=reason))
    amend('DK4_MES_B141_R0038',"I suspect defeating Spain isn't what he has in mind...",
        'というよりは introduces an alternative target,not Spain plus an additional target;retain Julio’s qualification.')
    amend('DK4_MES_B141_R0065',"B-but...! I mean...",
        'Preserve Rafael’s unfinished shocked objection without adding an explicit prohibition orclaim that Hayreddin cannot act.')
    amend('DK4_MES_B145_R0114',"Well, we saw... I mean...",
        'Keep Claudio’s awkward incomplete evasion without inventing a polished depends-what-you-mean wordplay.')
    amend('DK4_MES_B145_R0122',"Eir... I mean, A-Arcadius!",
        'Retain the interrupted real name andalias correction using ASCII punctuation;do not globallyrename actor8.')
    row=indexed[('/data/SC0.DK4','DK4_MES_B148_R0224')]
    amend(row['id'],row['independent_English'].replace('be rivals','be enemies'),
        '敵同士 explicitly makes them enemies;courteous delivery mustnot soften that toordinary friendly rivalry.')
    amend('DK4_MES_B152_R0050',"The Estado, your trading sphere here in Southeast Asia...",
        'Retain Estado andits sourcegloss withASCII apposition punctuation,not an unqualified em-dash glyph.')
    for row in rows:
        if row['block']==155 and 'Lord Escante' in row['independent_English']:
            amend(row['id'],row['independent_English'].replace('Lord Escante','Governor Escante'),
                '様 alone doesnot establish nobility. The whole exchange explicitly identifies Escante asthe governor ofMexico.')
    amend('DK4_MES_B155_R0029',"Either way, Governor Escante will rule the New World. And as for the homeland... Oops. Better stop there.",
        '本国からの is interrupted:do not supply independence,freedom fromrule,conquest ofthe homeland oranyother unstated secret.')
    amend('DK4_MES_B155_R0117',"Then look at it the other way: Escante's in our way!",
        'Keep Claudio’s reversal intact withASCII punctuation;no native font approval is inferred.')
    token_cases=[];new_FU=[]
    for row in rows:
        draft=row['independent_English'];raw=bytes.fromhex(row['source_hex'])
        body=raw[1:] if 'source_selector' in row else raw
        tokens={t.decode():body.count(t) for t in sorted(set(re.findall(rb'F[A-Z]',body)))}
        assert all(draft.count(t)==n for t,n in tokens.items()),row['id']
        assert not any(ord(c)>127 for c in draft),row['id']
        assert '\n' not in draft and not any(t in draft for t in ['{LB','{ALIGN','{PAD}'])
        row['native_literal_token_counts']=tokens
        if tokens:token_cases.append(dict(id=row['id'],tokens=tokens))
        if 'FU' in tokens:new_FU.append(dict(id=row['id'],source_reference=row['source_reference'],source_hex=row['source_hex'],count=tokens['FU']))
    assert len(new_FU)==2
    ledger_path=Path('translations/editorial_review_current_v1.json');ledger=load(ledger_path)
    completed={(r['file_path'],r['id']) for r in ledger['contextual_story_natural_dialogue_pass_v1871']['record_keys']}
    assert len(completed)==ledger['records_editorially_completed']==12712
    assert not completed & set(indexed)
    save(output,dict(records=rows,records_count=557,ordinary_speeches=549,typed_captions=8,physical_style_variants=0,
        complete_blocks=list(range(141,161)),source_contexts=contexts,
        all_individual_clean_meanings_andindependent_drafts_saved=True,all_current_comparisons_andapproved_bindings_pending=True,
        all_five_gates_pending=True,no_current_English_extracted_for_this_intake_before_drafts=True,
        no_blanket_claim_of_historical_unexposure=True,all_source_controls_andliteral_F_tokens_preserved=True,
        FU_native_consumer_andapproved_names_terms_titles_pending=True,draft_amendments=changes,
        provisional_spellings_are_not_approved_name_changes=True,no_ROM_or_registry_changes=True,new_credit=0,guide_photos=False,
        evidence={str(p):sha(p.read_bytes()) for p in [packet_path,style_path,choice_path,*INPUTS,Path(__file__)]}))
    save(census_path,dict(source_packet=str(packet_path),source_packet_sha256=sha(packet_path.read_bytes()),
        meanings_anddrafts=str(output),meanings_anddrafts_sha256=sha(output.read_bytes()),
        source_objects=557,ordinary_speeches=549,typed_captions=8,choice_objects=4,physical_style_variants=0,
        complete_blocks=list(range(141,161)),all_source_objects_exactly_once=True,complete_source_headers_objects_andreferences_exact=True,
        source_macro_literal_cases=token_cases,distinct_FU_source_records=new_FU,FU_native_display_behavior_unqualified=True,
        ASCII_only_logical_drafts=True,no_new_native_execution_formatting_orvisual_approval=True,
        completed_source_key_overlap=[],integrated_completed=12712,ledger_before_sha256=sha(ledger_path.read_bytes()),
        four_pronoun_replacements_in_failed_last_draft_restored_to_original_FI_count=True,
        failed_draft_producer='scripts/draft_rafael_B157_B160_clean_v1.py',
        corrected_draft_producer='scripts/draft_rafael_B157_B160_clean_v2.py',
        draft_amendments=changes,new_credit=0,guide_photos=False,full_goal_complete=False))
    print(f'Qualified557 clean meanings/drafts:549 speeches/8 labels,zero completed overlap,{len(changes)} source/localization refinements,all literal tokens exact. FU/display/current comparison/all gates pending. No credit.')


if __name__=='__main__':main()
