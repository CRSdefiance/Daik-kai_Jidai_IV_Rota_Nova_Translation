"""Create/pin a reversible two-literal research image after the verified B221 release."""
import json,os,struct
from copy import deepcopy
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.square_shopkeeper_label_data_v1 import transform,OWNERS,OLD
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/square_shopkeeper_data_v7018')
PRIOR=Path('work/analysis/editorial_handoff_verification_v7017/verified_handoff.json')
SOURCE=Path('translations/square_shopkeeper_label_manuscript_v2.json')
DOC=Path('translations/square_shopkeeper_label_manuscript_v3.json')
ROM=Path('out/square_shopkeeper_v7018_RESEARCH_ONLY.nds')
if __name__=='__main__':
    assert not ROOT.exists() and not DOC.exists() and not ROM.exists()
    verified=read(PRIOR);assert verified['profile']=='all-routes-unified-v7011' and verified['completed']==6619
    assert sha(Path('translations/editorial_review_current_v1.json').read_bytes())==verified['ledger_sha256']
    parent_path=Path(verified['candidate']);assert sha(parent_path.read_bytes())==verified['candidate_sha256']
    original=read(SOURCE);parent=NdsImage.open(parent_path);clean=NdsImage.open('work/clean.nds');arm=parent.read_file('/__arm9__.bin')
    assert sha(arm)==original['current_ARM9_sha256']==verified['ARM9_sha256']
    assert arm==NdsImage.open(original['current_ROM']).read_file('/__arm9__.bin')
    assert sha(Path('work/clean.nds').read_bytes())=='f4f07c975cc293f5b2ba469747693d3dd37f2e6dfc408cf5910adf5e83d9177d'
    assert sha(Path(original['context_review']).read_bytes())==original['context_review_sha256']
    assert original['all_ten_four_prose_gates_true_formatting_false'] and all(not r['review']['formatting'] for r in original['records'])
    # Include every filesystem asset as well as ARM9/ARM7. This raw pointer census
    # does not claim that every dynamically calculated caller has been visited.
    entries=[('file:'+p,v) for _,p,v in parent.iter_files()]+[('component:'+p,v) for p,v in parent.iter_components()]
    needles={struct.pack('<I',pointer+delta):(pointer,delta) for pointer,_ in OWNERS for delta in range(len(OLD))}
    hits=[]
    for name,data in entries:
        for needle,(pointer,delta) in needles.items():
            at=data.find(needle)
            while at>=0:
                hits.append(dict(asset=name,offset=at,owner_pointer=pointer,interior_delta=delta));at=data.find(needle,at+1)
    assert len(hits)==10 and {h['asset'] for h in hits}=={'component:/__arm9__.bin'} and all(h['interior_delta']==0 for h in hits)
    assert sorted(h['offset'] for h in hits)==[0x120B80+i*32 for i in range(82,92)]
    target,plan=transform(arm,clean.read_file('/__arm9__.bin'),original['records'])
    ROOT.mkdir(parents=True);binary=ROOT/'ARM9_RESEARCH_ONLY.bin';binary.write_bytes(target)
    image=NdsImage.open(parent_path);image.replace_file('/__arm9__.bin',target);image.save(ROM);saved=NdsImage.open(ROM)
    assert saved.read_file('/__arm9__.bin')==target
    assert [p for _,p,v in parent.iter_files() if saved.read_file(p)!=v]==[]
    assert [p for p,v in parent.iter_components() if saved.read_file(p)!=v]==['/__arm9__.bin']
    doc=deepcopy(original);doc.update(previous_manuscript=str(SOURCE),previous_manuscript_sha256=sha(SOURCE.read_bytes()),
        historical_pre_B221_current_ROM=original['current_ROM'],historical_pre_B221_current_ROM_sha256=original['current_ROM_sha256'],
        current_ROM=str(parent_path),current_ROM_sha256=verified['candidate_sha256'],target_ARM9=str(binary),target_ARM9_sha256=sha(target),
        target_research_ROM=str(ROM),target_research_ROM_sha256=sha(ROM.read_bytes()),data_plan=plan,
        all36_pointer_values_scanned_unaligned_in_every_file_and_component=True,exact_pointer_hits=hits,
        complete_source_shared_dynamic_pair_macro_native_target_actual_and_registered_release_pending=True,
        new_name_completion_credit=0,new_dialogue_completion_credit=0,full_goal_complete=False)
    # The old no-change assertion remains in the frozen predecessor manuscript.
    doc['historical_v2_no_ROM_or_registry_or_ledger_change']=doc.pop('no_ROM_or_registry_or_ledger_change')
    doc['no_registry_or_ledger_change']=True;save(DOC,doc)
    pins=Path('translations/rom_retention_pins.json');raw=pins.read_bytes();values=json.loads(raw)
    assert not any(Path(r['path']).resolve()==ROM.resolve() for r in values)
    added=dict(path=str(ROM.resolve()),reason='Two owned Shopkeeper literal prefixes;ten reviewed source roles. Native/shared/display/release pending. Preserve every ROM. SHA256 '+sha(ROM.read_bytes()))
    encoded=(json.dumps(values+[added],ensure_ascii=False,indent=2)+'\n').replace('\n','\r\n').encode('utf-8')
    (ROOT/'pins.before.json').write_bytes(raw);assert json.loads(encoded)[:-1]==values and pins.read_bytes()==raw
    with pins.open('r+b') as stream:stream.write(encoded);stream.truncate();stream.flush();os.fsync(stream.fileno())
    assert pins.read_bytes()==encoded
    evidence={str(p):sha(p.read_bytes()) for p in [PRIOR,SOURCE,Path(original['context_review']),Path('dk4tool/patch/square_shopkeeper_label_data_v1.py'),Path(__file__)]}
    save(ROOT/'research_image_receipt.json',dict(parent=str(parent_path),parent_sha256=verified['candidate_sha256'],research_ROM=str(ROM),research_ROM_sha256=sha(ROM.read_bytes()),
        source_ARM9_sha256=sha(arm),target_ARM9_sha256=sha(target),COMMON_sha256=sha(parent.read_file('/COMMON/MESFILE.DK4')),
        manuscript=str(DOC),manuscript_sha256=sha(DOC.read_bytes()),data_plan=plan,exact_pointer_hits=hits,
        all_files_unchanged=True,only_two_owned_literal_prefixes_in_ARM9_change=True,all621_pointer_fields_all_other_names_and_unread_old_tails_exact=True,
        no_registered_candidate_or_new_parent_claim=True,source_four_prose_gates_only_formatting_not_approved=True,
        target_native_shared_dynamic_macro_pair_bounds_and_representative_captures_pending=True,evidence=evidence,
        new_emulator_runs=0,new_name_or_dialogue_credit=0,full_goal_complete=False))
    save(ROOT/'pin_receipt.json',dict(new_pins=[added],all_prior_pins_preserved=True,ROMs_deleted=0,before_sha256=sha(raw),after_sha256=sha(encoded),full_goal_complete=False))
    print(dict(research_ROM=str(ROM),target_ARM9_sha256=sha(target),changed_bytes=len(plan['changed_byte_offsets']),pointer_hits=len(hits),native_display_release_pending=True,new_credit=0),flush=True)
