"""Prepare complete-block negative testing and one cumulative B169 registration."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import save

ROOT = Path('work/analysis/lil_B169_registration_tools_v4250')
OLD = Path('scripts/register_lil_B168_v4203.py')
NEW = Path('scripts/register_lil_B169_v4250.py')

if __name__ == '__main__':
    assert not ROOT.exists() and not NEW.exists()
    text = OLD.read_text(encoding='utf-8')
    removed = ['FE_wrong_consumer','FE_wrong_selector','FE_geometry','FE_pagination','generic_name_written']
    lines = text.splitlines(keepends=True)
    for label in removed:
        matched = [line for line in lines if "('"+label+"'," in line]
        assert len(matched)==1
        lines.remove(matched[0])
    text = ''.join(lines)
    changes = {
        'B168':'B169','lil_B168_editorial_v1':'lil_B169_editorial_v2',
        'lil_B168_registration_v4203':'lil_B169_registration_v4250',
        'all-routes-unified-v4204':'all-routes-unified-v4251',
        'all_routes_combined_v4160':'all_routes_combined_v4204',
        'lil_B168_editorial_manuscript_v8':'lil_B169_editorial_manuscript_v5',
        'lil_B168_editorial_relocation_map':'lil_B169_editorial_relocation_map',
        'lil_B168_checkpoint_v4188':'lil_B169_reference_checkpoint_v4247',
        'all-routes-unified-v4160':'all-routes-unified-v4204',
        'lil_B168_layout_v3':'lil_B169_layout_v2','lil_B168_profile':'lil_B169_profile',
        'lil_B168_reference_approval_v4202':'lil_B169_reference_approval_v4246',
        'lil_B168_loader_v4194/whole_SC2_and_B168_initial_entry_proof':'lil_B169_loader_v4237/whole_SC2_and_B169_initial_entry_proof',
        'lil_B168_transition_review_v4201/all9_sheets_contact_FE_source_effect_and_paired_return_review':'lil_B169_transition_review_v4245/all6_sheets_source_effect_and_paired_return_review',
        'dk4-lil-B168-editorial-release-v1':'dk4-lil-B169-editorial-release-v1',
        "== 54":"== 36",
        "english='WHere to see old Mikhail too?'":"english='LWhat is this Proof?'",
        'all16_source_current_target_nonrelative_nonspeech_leaves':'all5_source_current_target_nonrelative_nonspeech_leaves',
        'native_sixteen_consumer_cases':'native_twelve_consumer_cases',
        'all4_declared_end_decodes_return_type0_extent4_without_post_payload_read':'all2_declared_end_decodes_return_type0_extent4_without_post_payload_read',
        "for macro in ['FI', 'FA', 'FO']:":"for macro in ['FI', 'FO']:",
        'actual_progressive_FE_three_predicates_full_effect_and_return':'actual_progressive_three_predicates_full_effect_and_return',
        'actual_source_recruitment_effect':'actual_source_hex0029_0001_effect',
        "['source_end_offset'] = 2910":"['source_end_offset'] = 2584",
        'lil_mikhail':'lil_proof',
        'lil_B168_editorial':'lil_B169_editorial',
        'V4160':'V4204','v4203.tmp':'v4250.tmp',
        'expected_manifest_batches=544':'expected_manifest_batches=545',
        'expected_batches=544':'expected_batches=545',
        'positive_records=54':'positive_records=36',
    }
    import re
    for old in changes:
        assert old in text,old
    text = re.sub('|'.join(re.escape(k) for k in sorted(changes,key=len,reverse=True)),lambda m:changes[m.group()],text)
    a = text.index("        description='Full V4204 cumulative stack")
    b = text.index("\n    registry['profiles'][PROFILE]",a)
    text = text[:a]+"        description='Full V4204 cumulative stack plus36 complete B169 Proof explanation reviews:19 revisions/17 retentions,36 progressive speeches,53 commands,twelve spans,three predicates,five leaves,one later hex0029/0001 effect and one tail end. Two complete-condition B22 boots cover33 speeches and normal return;Julio/Ian/Fernando remarks remain offline. No natural eligibility,earned flag,full-route orhardware claim.')"+text[b:]
    anchor = "    for macro in ['FI', 'FO']:\n"
    assert text.count(anchor)==1
    extra = """    mutations.extend([
        ('lost_owned_scratch', 'source_nameplate_consumer_proof', lambda value: value['native_twelve_consumer_cases']['rows'][0].update(original_scratch_rings=[])),
        ('wrong_decimal_operand', 'reference_map', lambda value: value.update(source_effect_operand_decimal_values=[29,1])),
        ('wrong_operand_amendment', 'source_effect_operand_notation_amendment', lambda value: value.update(operand_hex_values=['0028','0001'])),
        ('lost_native_bounds', 'native_font_proof', lambda value: value['cases'][0].update(all_visible_origins_zero_and16px_rows_within4rows=False)),
    ])
"""
    text = text.replace(anchor,extra+anchor)
    anchor = "    deps.update(mapping[key] for key in ['source_plan', 'source_census'])\n"
    assert text.count(anchor)==1
    text = text.replace(anchor,anchor+"    deps.add(doc['source_effect_operand_notation_amendment'])\n")
    assert text.count('    save(rp, registry)')==1
    text = text.replace('    save(rp, registry)',
        "    import json\n    registry_bytes=(json.dumps(registry,ensure_ascii=False,indent=2)+'\\n').replace('\\n','\\r\\n').encode('utf-8')\n    assert len(registry_bytes)>len(raw)\n    with rp.open('r+b') as stream:\n        stream.write(registry_bytes)\n        stream.flush()\n        os.fsync(stream.fileno())")
    assert 'B168' not in text and 'lil_B168' not in text
    compile(text,str(NEW),'exec')
    NEW.write_text(text,encoding='utf-8',newline='\n')
    ROOT.mkdir(parents=True)
    save(ROOT/'source_derivation.json',dict(previous=str(OLD),previous_sha256=sha(OLD.read_bytes()),successor=str(NEW),successor_sha256=sha(NEW.read_bytes()),
        removed_unrelated_FE_or_generic_role_cases=removed,added_scratch_operand_and_bounds_negatives=4,
        expected_manifest_batches=545,source_parent_profile='all-routes-unified-v4204',
        new_profile='all-routes-unified-v4251',no_registration_build_orcredit_change_yet=True,
        producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print('B169 atomic registration producer prepared;complete V4204 inherited,545 batches expected. Main promotion preserved.')
