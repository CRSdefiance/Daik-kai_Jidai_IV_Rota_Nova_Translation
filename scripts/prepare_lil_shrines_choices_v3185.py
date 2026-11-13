"""Create a source-bound three-option successor from the two-option proof."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import save

OLD=Path('scripts/prove_lil_crew_items_choices_v3130.py')
NEW=Path('scripts/prove_lil_shrines_choices_v3185b.py')
ROOT=Path('work/analysis/lil_Shrines_Temples_menu_tools_v3185')

if __name__=='__main__':
    assert not NEW.exists() and not ROOT.exists()
    text=OLD.read_text(encoding='utf-8')
    replacements={
        'Original two-choice':'Original three-choice',
        'lil_Crew_Items_choices_v3130':'lil_Shrines_Temples_choices_v3185b',
        'work/analysis/lil_Crew_Items_source_v3112/complete200_clean_current_native_context.json':
        'work/analysis/lil_Shrines_Temples_source_v3163/complete235_clean_current_native_context.json',
        'translations/lil_crew_items_choice_manuscript_v1.json':'translations/lil_shrines_temples_choice_manuscript_v1.json',
        "if r['word']==0x2100":"if r['word']==0x2200 and r['offset']==offset",
        '== 2':'== 3',
        'for index in (0,1):':'for index in range(3):',
        "expected = 6+struct.unpack_from":"expected = 8+struct.unpack_from",
        'vm = prior.choice_vm(arm,value)':'vm = choice_vm(arm,value)',
        'all_four_style_label_planes':'all_six_style_label_planes',
        'Image.new(\'RGB\',(1000,300)':'Image.new(\'RGB\',(1000,440)',
        'typed_two_choice_RESEARCH_ONLY.bin':'typed_three_choice_RESEARCH_ONLY.bin',
        'six_original_VM_selection_and_cancel_cases_pass':'eight_original_VM_selection_and_cancel_cases_pass',
        'eight_complete_native_style_label_planes_pass':'twelve_complete_native_style_label_planes_pass',
        'source_derived_Crew_Items_choice_painter_v3130':'source_derived_Shrines_Temples_choice_painter_v3185b',
        'native_VM_selection_cancel_cases=6,native_label_planes=8':'native_VM_selection_cancel_cases=8,native_label_planes=12',
        '[(82,114)]':'[(105,186),(105,424),(105,842),(109,384),(110,336)]',
        'assert len(cases)==1':'assert len(cases)==5',
        'all1_typed_menu_native_proof.json':'all5_typed_menu_native_proof.json',
        'native_selection_cancel_cases=6,complete_current_and_reviewed_style_label_planes=8,clean_current_reviewed_native_decoder_cases=3':
        'native_selection_cancel_cases=40,complete_current_and_reviewed_style_label_planes=60,clean_current_reviewed_native_decoder_cases=15',
        'all2_labels_source_order_pointers_counts_and_original_selection_results_preserved':
        'all15_labels_source_order_pointers_counts_and_original_selection_results_preserved',
    }
    import re
    text=re.sub('|'.join(re.escape(k) for k in sorted(replacements,key=len,reverse=True)),
        lambda m:replacements[m.group()],text)
    begin=text.index('    first = values[0]')
    end=text.index("    objects = ",begin)
    text=text[:begin]+"""    assert len(values)==3
    chunks=[];offsets=[];cursor=0
    for value in values:
        assert value and value.strip()==value and b'\\n' not in value
        assert all(32<=v<127 for v in value)
        offsets.append(cursor)
        chunk=value+b'\\0';chunk+=b'\\0'*(-len(chunk)%2)
        chunks.append(chunk);cursor+=len(chunk)
    target=struct.pack('<4H',0x2200,*offsets)+b''.join(chunks)
""" + text[end:]
    # The original VM harness is adapted only for this source count. Original
    # getters, dispatch, geometry and returns execute; the modal loop is bridged.
    anchor="    painter = inspect.getsource(prior.paint)"
    assert text.count(anchor)==1
    text=text.replace(anchor,"""    vm_source=inspect.getsource(prior.choice_vm)
    vm_changes={
        '== 2':'== 3',
        'for index in (0, 1):':'for index in range(3):',
        'for selected in (0, 1, -1):':'for selected in (0, 1, 2, -1):',
        '(rect, provider, maximum, 2)':'(rect, provider, maximum, 3)',
        "pointer, 32":"pointer, len(object_bytes)",
        "96":"VM_GUARD_BYTES",
    }
    for old,new in vm_changes.items():
        assert old in vm_source,old
        vm_source=vm_source.replace(old,new)
    vm_env={**prior.__dict__,'VM_GUARD_BYTES':max(256,len(target)+32,len(objects[1][1])+32)}
    exec(compile(vm_source,'source_derived_three_choice_VM_v3185b','exec'),vm_env)
    choice_vm=vm_env['choice_vm']
""" + anchor)
    # Preserve all generated native evidence, including the exact VM adapter.
    anchor='        typed_target_object_hex=target.hex(),source_derived_painter_adapter=painter,'
    assert text.count(anchor)==1
    text=text.replace(anchor,anchor+"\n        source_derived_three_option_VM_adapter=vm_source,source_count3_and_result2_and_cancel_explicit=True,")
    NEW.write_text(text,encoding='utf-8')
    compile(text,str(NEW),'exec')
    ROOT.mkdir(parents=True)
    save(ROOT/'three_option_producer_provenance.json',dict(previous=str(OLD),previous_sha256=sha(OLD.read_bytes()),
        successor=str(NEW),successor_sha256=sha(NEW.read_bytes()),native_count3_textbase8_indices012_cancel_minus1_explicit=True,
        no_predecessor_or_ROM_change=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
