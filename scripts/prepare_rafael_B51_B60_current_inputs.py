"""Seal245 clean-first drafts and select only their10 blocks for current comparison."""
import struct
from copy import deepcopy
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.audit_story_glyph_consistency import load, save
from scripts.gloss_rafael_B51_B59_clean import ROOT
from scripts.consolidate_rafael_B51_B60_source import RELEASE, cstring
from scripts.registered_editorial_runtime_v2 import RegisteredRuntime

if __name__ == '__main__':
    target = ROOT / 'B51_B60_current_binding_source_v1.json'; sealed = ROOT / 'B51_B60_all245_sealed_drafts_v1.json'
    selected = ROOT / 'B51_B60_selected_source_packet_v1.json'; terms_path = ROOT / 'B51_B60_exact_named_references_v1.json'
    assert not any(p.exists() for p in [target,sealed,selected,terms_path])
    paths = [ROOT / 'B51_B59_146_logical_English_drafts_v1.json',ROOT / 'B60_99_logical_English_drafts_v1.json']
    rows = [r for p in paths for r in load(p)['records']]
    assert len(rows)==245 and all(r['current_English_comparison_pending'] and not r['review']['formatting'] for r in rows)
    source = ROOT / 'B51_B60_source_identity_checkpoint_v1.json'; meaning = load(source)
    packet_path = ROOT / 'clean_source_packet.json'; packet = load(packet_path)
    subset = deepcopy(packet); subset['groups'] = [g for g in packet['groups'] if 51<=g['block']<=60]
    subset.update(records=245,selected_from=str(packet_path),selected_from_sha256=sha(packet_path.read_bytes()))
    ctx = RegisteredRuntime(RELEASE,RELEASE.with_name('own_registered_startup_verification.json'),captain=0)
    clean = NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    tables = [struct.unpack_from('<I',arm,0xCDAC0)[0]-33554432 for arm in [clean,ctx.arm]]
    references=[]
    for actor in [36,40]:
        fields=[]
        for col in [0,4,8]:
            source_field,current_field=tables[0]+32*actor+col,tables[1]+32*actor+col
            source_pointer,current_pointer=struct.unpack_from('<I',clean,source_field)[0],struct.unpack_from('<I',ctx.arm,current_field)[0]
            a,b=cstring(clean,source_pointer),cstring(ctx.raw,current_pointer)
            fields.append(dict(column=col,source_field=source_field,source_pointer=source_pointer,source_hex=a.hex(),source_text=a.decode('cp932'),
                current_field=current_field,current_pointer=current_pointer,current_hex=b.hex(),current_text=b.decode('cp932')))
        references.append(dict(actor_ID=actor,fields=fields,static_typed_name_fields_not_new_native_getter_orUI=True))
    assert [f['current_text'] for f in references[1]['fields'][:2]]==['Antony','Kuhn']
    save(terms_path,dict(runtime=ctx.receipt(),referenced_names=references,
        source_actor40_surname='クーン',established_progressive_reference='Antony Kuhn',
        separate_full_name_field_finding=dict(actor_ID=40,current_middle=references[1]['fields'][2]['current_text'],
            finding='Unintended full-width Latin F andpotential Fong/von name adaptation need a source-aware scoped full-name review. No automatic renaming.',
            no_change_ornew_credit=True),source_andcurrent_story_English_not_extracted=True,new_credit=0))
    save(sealed,dict(format='dk4-source-first-logical-English-drafts-v1',translation_policy='natural-dialogue-v2',target_locale='en-US',
        file_path='/data/SC0.DK4',blocks=list(range(51,61)),records=rows,
        source_meanings_andlogical_drafts_sealed_before_current_ROM_English_extraction_in_this_intake=True,
        constituent_drafts={str(p):sha(p.read_bytes()) for p in paths},exact_named_references=str(terms_path),
        exact_named_references_sha256=sha(terms_path.read_bytes()),all_fifth_formatting_gates_pending=True,new_credit=0,guide_photos=False))
    save(selected,subset)
    source_rows=deepcopy(meaning['records'])
    for r in source_rows:r['current_ROM_English_unconsulted']=True
    save(target,dict(source_packet=str(selected),source_packet_sha256=sha(selected.read_bytes()),records=source_rows,meanings=245,
        all_drafts_sealed=str(sealed),all_drafts_sha256=sha(sealed.read_bytes()),no_blanket_prior_English_exposure_claim=True,
        complete_gloss=str(source),complete_gloss_sha256=sha(source.read_bytes()),new_credit=0,guide_photos=False))
    print('Sealed245 source-first drafts,10 source blocks andexact Antony Kuhn fields;current comparison now permitted.')
