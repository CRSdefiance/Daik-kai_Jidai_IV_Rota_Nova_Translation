"""Qualify the exact relocated-context result and reject wrong ownership/source/macros."""
from copy import deepcopy
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.script.reviewed_credited_context_rebuild_v1 import rebuild_credited_context
from scripts.audit_story_glyph_consistency import load, save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.inventory_lil_after_crew_items_complete_v3152 import scoped_inventory

ROOT = Path('work/Lil382_residual_A_clean_20261110')


def main():
    out = ROOT/'credited_context_rebuild_qualification_v1.json'
    assert not out.exists()
    reconstruction = ROOT/'reconstruction_v2/reconstruction.json'
    rebuilt = load(reconstruction)
    doc = load(rebuilt['manuscript'])
    packetpath = ROOT/'current_inputs_v1/source_packet.json'
    group = next(g for g in load(packetpath)['groups'] if g['block']==115)
    currentpath = ROOT/'current_v1/current_effective.json'
    currentgroup = next(g for g in load(currentpath)['groups'] if g['block']==115)
    clean, current = bytes.fromhex(group['clean_block_hex']),bytes.fromhex(currentgroup['current_block_hex'])
    arm = NdsImage.open(rebuilt['parent']).read_file('/__arm9__.bin')
    records = [r for r in doc['records'] if r['block']==115]
    compiled = {r['id']:r for r in load(rebuilt['plan'])['records']}
    ledgerpath = Path('translations/editorial_review_current_v1.json')
    credited = {(r['file_path'],r['id']) for r in load(ledgerpath)['contextual_story_natural_dialogue_pass_v1871']['integrated_record_keys']}
    inventory,_,_ = scoped_inventory()
    def run(a,b,rows,plans,context,keys):
        return rebuild_credited_context(arm,a,b,rows,plans,inventory,context,keys,
            expected_context_objects=9,expected_context_speeches=4)
    target,proof = run(clean,current,records,compiled,group,credited)
    saved = next(g for g in rebuilt['groups'] if g['block']==115)
    assert target==Path(saved['target_block']).read_bytes()
    assert proof['actual_clean_block_inverse_exact'] and proof['current_parent_inverse_executed_by_original_complete_allocator']
    cases = []
    for kind in ['missing-credited-key','missing-owned-line','changed-source-coordinate','changed-source-byte','lost-faction-macro']:
        source=clean;rows=deepcopy(records);plans=deepcopy(compiled);keys=set(credited)
        if kind=='missing-credited-key':
            context=next(r for r in group['complete_clean_context_records'] if r['covered'])
            keys.remove((context['file_path'],context['exact_credited_source_bindings'][0]['id']))
        elif kind=='missing-owned-line':
            rows.pop()
        elif kind=='changed-source-coordinate':
            rows[0]['source_reference']['offset']+=1
        elif kind=='changed-source-byte':
            altered=bytearray(clean);altered[records[0]['source_reference']['offset']+1]^=1;source=bytes(altered)
        else:
            row=next(r for r in rows if r['source_macros'].get('FO'))
            raw=bytes.fromhex(plans[row['id']]['encoded_hex']);assert b'FO' in raw
            plans[row['id']]['encoded_hex']=raw.replace(b'FO',b'XX').hex()
        try:
            run(source,current,rows,plans,group,keys)
        except (AssertionError,ValueError) as error:
            cases.append(dict(case=kind,rejected=True,error_type=type(error).__name__))
        else:
            raise AssertionError('Accepted invalid relocated-context input: '+kind)
    assert len(cases)==5 and len(proof['preserved_credited_context_speeches'])==4
    save(out,dict(reconstruction=str(reconstruction),reconstruction_sha256=digest(reconstruction),
        actual_clean_current_andtarget_inverses_pass=True,positive_B115_target_byte_exact=True,
        preserved_context_objects=9,preserved_context_speeches=4,new_owned_speeches=32,
        selected_source_coordinates=proof['actual_source_to_current_selected_coordinates'],rejected_cases=cases,
        no_new_review_credit_orROM_changes=True,new_credit=0,
        evidence={str(p):digest(p) for p in [reconstruction,packetpath,currentpath,ledgerpath,Path(__file__),Path('dk4tool/script/reviewed_credited_context_rebuild_v1.py')]}))
    print('PASS B115 exact target/actual clean andparent inverses;five ownership/source/macro mutations rejected.')


if __name__=='__main__':
    main()
