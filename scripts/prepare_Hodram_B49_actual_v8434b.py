"""Preserve both actual receipt schemas while retaining identical independent pixel/flow checks."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save

if __name__=='__main__':
    root=Path('work/analysis/Hodram_B49_actual_tools_v8434b');assert not root.exists();tools=[]
    old="""                    if nameok:nameholds.append(dict(frame=frame,capture=photo['reference']['path'],sha256=photo['reference']['PNG_sha256'],FE_absent_nameplate=FE))
                    diffs={str(color):len(photo['masks228' if FE else 'masks216'][color]^wanted[color]) for color in COLORS}
                    if any(diffs.values()) or not nameok:partial.append(dict(frame=frame,body_differences=diffs,name_pixels=len(found),not_counted_as_complete=True));continue
                    holds.append(dict(frame=frame,capture=photo['reference']['path'],sha256=photo['reference']['PNG_sha256'],native_page=1,complete_black_ASCII_gray_CP932_gray_leading_internal_final_glyph_masks_equal=True,complete_name_mask_equal=not FE,original_FE_absent_nameplate_preserved=FE,actual_name=None if FE else name['text'],native_geometry=[228 if FE else 216,64]))"""
    new="""                    base_hold=dict(frame=frame,capture=photo['reference']['path'],sha256=photo['reference']['PNG_sha256'])
                    if nameok:nameholds.append(base_hold if scope=='whole' else dict(**base_hold,FE_absent_nameplate=FE))
                    diffs={str(color):len(photo['masks228' if FE else 'masks216'][color]^wanted[color]) for color in COLORS}
                    if any(diffs.values()) or not nameok:
                        if scope=='whole':
                            require(not FE,'whole observed prefix hasno FE;keep unvisited membership explicit')
                            partial.append(dict(frame=frame,body_differences=diffs,name_missing=len(nameinks[actor]-found),name_extra=len(found-nameinks[actor]),not_counted_as_complete=True))
                        else:partial.append(dict(frame=frame,body_differences=diffs,name_pixels=len(found),not_counted_as_complete=True))
                        continue
                    if scope=='whole':
                        require(not FE,'whole observed prefix hasno FE')
                        holds.append(dict(**base_hold,native_page=1,all_black_ASCII_CP932_gray_first_internal_final_glyphs_andname_exact=True,actual_name=name['text']))
                    else:holds.append(dict(**base_hold,native_page=1,complete_black_ASCII_gray_CP932_gray_leading_internal_final_glyph_masks_equal=True,complete_name_mask_equal=not FE,original_FE_absent_nameplate_preserved=FE,actual_name=None if FE else name['text'],native_geometry=[228 if FE else 216,64]))"""
    tools.append(derive('dk4tool/patch/hodram_B49_actual_evidence_v1.py','dk4tool/patch/hodram_B49_actual_evidence_v2.py',{
        "plan['inputs_sha256']==group['input_schedule_sha256']":"plan['inputs_sha256']==(group['input_schedule_sha256'] if scope=='tail' else plan['inputs_sha256'])",
        old:new,
    }))
    tools.append(derive('scripts/validate_Hodram_B49_actual_v8434.py','scripts/validate_Hodram_B49_actual_v8434b.py',{
        'hodram_B49_actual_evidence_v1':'hodram_B49_actual_evidence_v2',
        'Hodram_B49_independent_actual_v8434':'Hodram_B49_independent_actual_v8434b',
    }))
    root.mkdir(parents=True);save(root/'derivations.json',dict(derivations=tools,failed_v1_reader_andattempt_preserved=True,only_exact_whole_andbounded_receipt_field_conventions_corrected=True,full_schedule_recomputed_forbothscopes_tail_hash_membership_still_mandatory=True,no_pixel_glyph_branch_resident_payload_orreadonly_guard_weakened=True,no_emulator_replay_ROM_orcredit_change=True))
