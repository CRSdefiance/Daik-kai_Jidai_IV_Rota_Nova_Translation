"""Correct the caught description-versus-item-table distinction;preserve the failed proof."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B207_item_binding_tools_v6349b')
if __name__=='__main__':
    assert not ROOT.exists()
    original="    assert terms and any(t['source_Japanese']=='ミノタウロスの斧' and t['current_English']==\"Minotaur's Axe\" for t in terms) and not ctx.machines"
    replacement='''    # COMMON owns the item description;the218-row ARM9 table owns its title.
    field=ITEM_TABLE+41*24;title_fields=[]
    for label,code in [('clean',clean.read_file('/__arm9__.bin')),('current',ctx.arm)]:
        pointer=struct.unpack_from('<I',code,field)[0];value=c_string(code,pointer-BASE)
        title_fields.append(dict(version=label,pointer_field=field,pointer=pointer,file_offset=pointer-BASE,whole24byte_row_hex=code[field:field+24].hex(),terminated_hex=(value+b'\\0').hex(),text=value.decode('cp932')))
    item=dict(item_ID=41,file_path='/__arm9__.bin',fields=title_fields,source_Japanese=title_fields[0]['text'],current_English=title_fields[1]['text'])
    assert item['source_Japanese']=='ミノタウロスの斧' and item['current_English']=='Minotaur Axe'
    assert len(terms)==1 and terms[0]['message_ID']==2856 and 'ミノタウロス' in terms[0]['source_Japanese'] and 'Minotaur' in terms[0]['current_English'] and not ctx.machines'''
    row=derive('scripts/compare_lil_B207_effective_v6349.py','scripts/compare_lil_B207_effective_v6349b.py',{
      "from pathlib import Path":"from pathlib import Path\nimport struct\nfrom scripts.materialize_all_item_names_v1 import TABLE as ITEM_TABLE,c_string\nfrom scripts.current_build_native_context_v6261b import BASE",
      'lil_B207_effective_v6349\'':'lil_B207_effective_v6349b\'',original:replacement,
      'existing_source_current_Minotaur_terms=terms':'item_name_binding=item,existing_source_current_Minotaur_descriptions=terms',
      'existing_item_name_Minos_genitive_and_axe_retained_without_new_item_credit':'existing_item_title_and_description_bound_without_new_item_credit',
      "print('All13 current runtime paragraphs equal stored bodies;no catalogue overrides. Existing Minotaur item terms:',[(t['message_ID'],t['source_Japanese'],t['current_English']) for t in terms])":"print('All13 runtime paragraphs equal stored bodies;no overrides. ARM9 item41:',item['source_Japanese'],'->',item['current_English'],';COMMON description2856 bound separately. No new item or prose credit.')"})
    ROOT.mkdir(parents=True);save(ROOT/'corrected_table_ownership_derivation.json',dict(tool=row,failed_description_equals_title_assumption_preserved=True,source_spoken_Minotaur_genitive_and_canonical_UI_Minotaur_Axe_need_individual_prose_reconciliation=True,no_guard_or_native_address_weakened=True,no_ROM_name_item_or_review_credit_change=True,full_goal_complete=False))
