"""Bind four source spans and extend the validated speech relocator with one complete typed menu."""
import struct
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/Rafael_B46_archive_tools_v7938')
CURRENT=Path('work/analysis/Rafael_B46_current_v7927/all24_speeches2_choices_source_current_refs_before_new_English_manuscript.json')
SOURCE=Path('work/analysis/Rafael_next_clean_v7918/complete_clean_SC0_B46_EV0_andcoverage_before_current_English.json')
CONTROLS=Path('work/analysis/Rafael_B46_source_controls_v7922/source_EV0_entry_four_relative_sites20_cases25_seeded_ends_menu_scope.json')
CHOICES=Path('work/analysis/Rafael_B46_choice_planes_v7934/two_labels8_native_style_planes_trimmed_native_width_andthree_returns.json')
if __name__=='__main__':
    assert not ROOT.exists();current,source,controls,choices=map(read,[CURRENT,SOURCE,CONTROLS,CHOICES])
    clean=bytes.fromhex(source['groups'][0]['clean_block_hex']);spec=current['groups'][0]
    old=bytes.fromhex(spec['current_block_hex']);boundaries={c['offset'] for c in spec['all_current_commands']}|{spec['current_logical_end']}
    edges=[]
    for a,b in zip(source['groups'][0]['commands'],spec['all_current_commands'],strict=True):
        assert (a['offset'],a['word'],a['native_extent'])==(b['offset'],b['word'],b['native_extent'])
        if a['word'] not in [0x100,0x200,0x300,0x400]:continue
        at=a['offset'];span=struct.unpack_from('<H',old,at+2)[0]
        assert clean[at:at+4]==old[at:at+4] and at+4 in boundaries and at+4+span in boundaries
        proof=next(r for r in controls['source_relative_cases'] if r['offset']==at)
        assert proof['word']==a['word'] and proof['span']==span and len(proof['cases'])==5
        assert all(r['next_offset']==at+4+(span if r['taken'] else 0) and r['all4MiB_ABI_owner_input_output_andcanary_guards_exact'] for r in proof['cases'])
        edges.append(dict(block=46,offset=at,word=a['word'],span_field_offset=at+2,source_span=span,
            unmatched_next_offset=at+4,matched_skip_target=at+4+span,ancestor_0100_offsets=b['ancestor_0100_offsets'],
            source_operand_hex=clean[at:at+4].hex(),current_operand_hex=old[at:at+4].hex()))
    assert len(edges)==4
    menu_insert="""        choiceproof=read('work/analysis/Rafael_B46_choice_planes_v7934/two_labels8_native_style_planes_trimmed_native_width_andthree_returns.json')
        choice_rows=doc['typed_choice_records'];assert len(choice_rows)==2 and [r['option_index'] for r in choice_rows]==[0,1]
        oldmenu=next(c for c in spec['all_current_commands'] if c['word']==0x2100)
        sourcemenu=next(c for c in clean_spec['commands'] if c['word']==0x2100)
        at=oldmenu['offset'];oldvalue=bytes.fromhex(oldmenu['whole_command_hex']);sourcevalue=bytes.fromhex(sourcemenu['whole_command_hex'])
        value=bytes.fromhex(choiceproof['target_menu_object_hex'])
        assert choiceproof['manuscript_sha256']==sha(Path(doc['prior_manuscript']).read_bytes())
        assert len(oldvalue)==len(sourcevalue)==36 and len(value)==30 and old[at:at+36]==oldvalue and clean[at:at+36]==sourcevalue
        assert value[:2]==oldvalue[:2]==bytes.fromhex('0021') and len(value)%2==0
        patches.append(dict(start=at,end=at+36,old=oldvalue,value=value,source=sourcevalue,id='B46_menu256',kind='typed-menu'))
        menu_record=dict(old_offset=at,old_length=36,new_length=30,word=0x2100,count=2,target_hex=value.hex(),old_hex=oldvalue.hex(),clean_hex=sourcevalue.hex(),
            labels=[r['english'] for r in choice_rows],record_IDs=[r['id'] for r in choice_rows],source_references=[r['source_reference'] for r in choice_rows])
        assert len(patches)==25
"""
    menu_refs="""        menu_record['new_offset']=mapped(menu_record['old_offset']);menu_record['label_references']=[]
        for row in choice_rows:
            at=menu_record['new_offset'];i=row['option_index'];relative=struct.unpack_from('<H',target,at+2+2*i)[0];start=at+6+relative
            value=row['english'].encode('ascii');assert target[start:start+len(value)+1]==value+b'\\0'
            menu_record['label_references'].append(dict(id=row['id'],option_index=i,old_reference=row['current_reference'],
                source_reference=row['source_reference'],new_offset=start,new_length=len(value),new_record_index=target[:start].count(b'\\0'),
                relative_table_field=at+2+2*i,relative_base=at+6,relative_offset=relative,target_hex=value.hex()))
"""
    row=derive('scripts/relocate_Rafael_B45_v7884.py','scripts/relocate_Rafael_B46_v7938.py',{
        'Research-only Rafael B45 reconstruction:five exact nested fixups,complete00 preambles andfull predecessor inverse.':'Research-only Rafael B46 reconstruction:24 speeches,two-choice object,four exact nested fixups andboth full inverses.',
        'Rafael_B45_relocation_v7884':'Rafael_B46_relocation_v7938',
        'Rafael_B45_current_v7871/all12_complete_source_current_refs_before_new_English_manuscript.json':str(CURRENT).replace('\\','/'),
        'Rafael_next_clean_v7864/complete_clean_SC0_B45_EV0_andcoverage_before_current_English.json':str(SOURCE).replace('\\','/'),
        'rafael_B45_editorial_manuscript_v3':'rafael_B46_editorial_manuscript_v2',
        'Rafael_B45_layout_v7881b/12_automatic_plans_full_native_width_zero_preamble_separate_body.json':'Rafael_B46_layout_v7932/24_automatic_plans_full_native_width_zero_preamble_separate_body.json',
        'Rafael_B45_native_review_v7883/12_exact_native_pages_rebound_with_individual_row_review.json':'Rafael_B46_native_review_v7935/24_pages2_choices_full_native_review_individual_wrap_reasons.json',
        'Rafael_B45_archive_tools_v7884/five_exact_source_current_relative_operands_bound_to25_native_cases.json':'Rafael_B46_archive_tools_v7938/four_exact_source_current_relative_operands_bound_to20_native_cases.json',
        'current_V7857_Rafael_native_v7868':'current_V7911_Rafael_native_v7914',
        "doc['prior_manuscript']['path']":"doc['prior_manuscript']",
        "        patches.sort(key=lambda p:p['start'])":menu_insert+"        patches.sort(key=lambda p:p['start'])",
        "            else:assert previous['whole_command_hex']==new['whole_command_hex']":"            elif word==0x2100:assert previous['whole_command_hex']==menu_record['old_hex'] and new['whole_command_hex']==menu_record['target_hex']\n            else:assert previous['whole_command_hex']==new['whole_command_hex']",
        '        def inverse(clean_version):':menu_refs+'        def inverse(clean_version):',
        'text_records=texts,relative_fixups=fixups':'text_records=texts,choice_commands=[menu_record],relative_fixups=fixups',
        "sum(len(g['text_records']) for g in groups)==12 and sum(len(g['relative_fixups']) for g in groups)==5":"sum(len(g['text_records']) for g in groups)==24 and sum(len(g['relative_fixups']) for g in groups)==4",
        'SC0_B45_RESEARCH_ONLY.DK4':'SC0_B46_RESEARCH_ONLY.DK4',
        "if a!=b]==[45]":"if a!=b]==[46]",
        'one_block12_speeches5_relative_fixups25_cases_exact_full_inverse.json':'one_block24_speeches2_choices4_fixups20_cases_exact_full_inverse.json',
        'source_relative_sites=5,relocated_native_skip_cases=25':'source_relative_sites=4,relocated_native_skip_cases=20',
        'all12_six_byte_preambles_macros_selectors_complete_terminal_andseparate_tails_preserved':'all24_six_byte_preambles_two_choices_macros_selectors_complete_terminal_andseparate_tails_preserved',
        'Research archive:12speeches/five relative sites/25guarded native cases;onlyB45 changes,342others exact;predecessor archive andclean block invert exactly.No ROM orcredit.':'Research archive:24 speeches/two choices/four relative sites/20 native cases;only B46 changes,342 others exact;both full block inverses andpredecessor archive exact. No ROM orcredit.',
    })
    ROOT.mkdir(parents=True)
    save(ROOT/'four_exact_source_current_relative_operands_bound_to20_native_cases.json',dict(
        operands_requiring_adjustment_when_resizing=edges,source_control_proof=str(CONTROLS),source_control_proof_sha256=sha(CONTROLS.read_bytes()),
        source_native_cases_reused_by_exact_operands_extent_andboundaries=20,source_current_relative_function_reads_identical_four_byte_operands=True,
        two_choice_object_proof=str(CHOICES),two_choice_object_proof_sha256=sha(CHOICES.read_bytes()),
        source_choice0_accept22_choice1_decline7_not_actual_gameplay=True,new_credit=0,
        evidence={str(p):sha(p.read_bytes()) for p in [CURRENT,SOURCE,CONTROLS,CHOICES,Path(__file__)]},full_goal_complete=False))
    save(ROOT/'provenance.json',dict(derivation=row,original_high_native_constants_bounds_preambles_inverses_andguards_preserved=True,
        source00_allowed_only_in_original_preamble_no_body_NUL_exception=True,complete_two_choice_object_andinternal_table_owned_explicitly=True,new_credit=0,full_goal_complete=False))
