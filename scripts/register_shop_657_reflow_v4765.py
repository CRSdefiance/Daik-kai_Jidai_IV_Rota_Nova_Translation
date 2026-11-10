"""Review and register a single in-allocation formatting correction cumulatively."""
from copy import deepcopy
from pathlib import Path
import json
import os

from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch import shop_657_reflow as owned
from dk4tool.patch.duel_editorial import owned_entries
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.probe_common_single_cache_v862 import Loader
from scripts.review_early_shop_breaks_v4763e import CURRENT, CURRENT_SHA, reference
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/shop657_registration_v4765')
DOC = Path('translations/shop657_full_width_reflow_manuscript_v1.json')
CONFIG = Path('translations/shop657_full_width_reflow_release_v1.json')
PROFILE = 'all-routes-unified-v4766'
PARENT_PROFILE = 'font-v2-square-scratch-fix-20261027'
PROOF = Path('work/analysis/early_shop_breaks_v4763e/source_current_findings_and_native_proposal.json')


if __name__ == '__main__':
    assert not ROOT.exists() and not DOC.exists() and not CONFIG.exists()
    proof = read(PROOF)
    assert len(proof['native_cases']) == 6 and all(r['independent_full_plane_equal'] for r in proof['native_cases'])
    assert sha(Path(proof['sheet']).read_bytes()) == proof['sheet_sha256']
    assert sha(CURRENT.read_bytes()) == CURRENT_SHA
    parent, baseline = NdsImage.open(CURRENT), NdsImage.open('out/raphael_natural_v2_accepted_base.nds')
    common, arm = parent.read_file('/COMMON/MESFILE.DK4'), parent.read_file('/__arm9__.bin')
    before = owned_entries(common, arm, proof['directory_sha256'])
    row = deepcopy(next(r for r in read('translations/square_contextual_final_review_v1.json')['records'] if r['message_id'] == 657))
    selected = proof['records'][0]
    row.update(current_reference=reference(before[657]), current_hex=before[657].text.hex(),
        english=owned.PARAGRAPH+'{PAD}', editorial_decision='retain-wording-reflow',
        proposed_compiled_hex=proof['proposed_657_hex'],
        fresh_retained_wording_justification=selected['current_reason'],
        native_soft_wrap_reason=proof['weak_ending_disposition'],
        formatting_gate_scope='Complete six native planes viewed: existing657 parent, original and current fonts, exact first/internal/final glyphs, blanks, guards, padding and bounds. Three generated trailing spaces stay inside35 final cells. No consumer hook or geometry change.',
        source_meaning=selected['source_meaning'],
        localization_note='Retain the natural tag question and trade-house recommendation. Generate full-width ordinary soft wrapping without splitting the tag question. The complete-word For boundary is a scoped reviewed soft-wrap decision; no global weak-ending policy changes.',
        status='offline-approved-actual-and-registered-release-pending')
    doc = dict(format='dk4-shop657-full-width-reflow-manuscript-v1', translation_policy='natural-dialogue-v2',
        target_locale='en-US', encoder='dialogue-fixed-v1',
        review_gates=['source','context','localization','naturalness','formatting'],
        source_ROM_sha256='f4f07c975cc293f5b2ba469747693d3dd37f2e6dfc408cf5910adf5e83d9177d',
        current_ROM=str(CURRENT), current_ROM_sha256=CURRENT_SHA, records=[row],
        added_editorial_credit=0, formatting_reopened_from='translations/square_contextual_final_review_v1.json',
        actual_new_gameplay_pending=True, full_goal_complete=False)
    blocks = list(IlnkContainer.parse(common).blocks)
    e = before[657]
    body = bytearray(blocks[e.block]); target = bytes.fromhex(row['proposed_compiled_hex'])
    assert len(target) == len(e.text) == 72
    body[e.block_offset:e.block_offset+len(target)] = target
    blocks[e.block] = bytes(body)
    target_common = IlnkContainer(blocks).to_bytes()
    assert len(target_common) == len(common)
    ROOT.mkdir(parents=True)
    save(DOC, doc)
    conf = dict(format='dk4-shop657-full-width-reflow-v1', manuscript=str(DOC),
        source_COMMON_sha256=sha(common), source_ARM9_sha256=sha(arm),
        target_COMMON_sha256=sha(target_common), directory_sha256=proof['directory_sha256'],
        source_text_hex=e.text.hex(), target_text_hex=target.hex(),
        canonical_COMMON_sha256=sha(baseline.read_file('/COMMON/MESFILE.DK4')))
    rebuilt, positive = owned.propose(common, arm, conf)
    assert rebuilt == target_common
    save(ROOT/'positive_reconstruction.json', positive)
    (ROOT/'target_COMMON.bin').write_bytes(target_common)
    after = owned_entries(target_common, arm, proof['directory_sha256'])
    loader, copies = Loader(arm,target_common), []
    for mode in ['warm','cold']:
        for index,entry in enumerate(after):
            copies.append(loader.copy(entry.message_id,entry.text,mode))
            if (index+1)%1000 == 0:
                print(mode,index+1,'native copies',flush=True)
    loader.reset(); sequence=[]
    for n in [656,657,658,689,657,658,657,3667,657]:
        sequence.append(loader.copy(n,after[n].text,'sequence'))
    copy_path = ROOT/'all7336_native_copies.json'
    save(copy_path,dict(ARM9_sha256=sha(arm), COMMON_sha256=sha(target_common), complete_native_copies=len(copies),
        cases=copies, sequenced_cache_cases=sequence, original_ABI_full_spans_NUL_canaries_and_cache_bounds_pass=True,
        native_file_reads_are_host_contracts=True, actual_new_gameplay_frames=0))
    files = [str(DOC),str(PROOF),str(copy_path),'dk4tool/patch/shop_657_reflow.py',
        'dk4tool/patch/shop_business_editorial.py','dk4tool/dialogue/layout.py','dk4tool/dialogue/review.py']
    conf['dependencies'] = {p:sha(Path(p).read_bytes()) for p in files}
    save(CONFIG,conf)
    check = NdsImage.open(CURRENT)
    owned.apply_release(check,baseline,CONFIG)
    assert check.read_file('/COMMON/MESFILE.DK4') == target_common and check.read_file('/__arm9__.bin') == arm
    negatives=[]
    def reject(label,change):
        c=deepcopy(conf);d=deepcopy(doc);image=NdsImage.open(CURRENT);change(c,d,image)
        if d != doc:
            path=ROOT/(label+'_manuscript.json');save(path,d);c['manuscript']=str(path);c['dependencies'][str(path)]=sha(path.read_bytes())
        p=ROOT/(label+'_config.json');save(p,c)
        old_files=(image.read_file('/COMMON/MESFILE.DK4'),image.read_file('/__arm9__.bin'))
        try:owned.apply_release(image,baseline,p)
        except (ValueError,AssertionError):
            assert old_files==(image.read_file('/COMMON/MESFILE.DK4'),image.read_file('/__arm9__.bin'))
            negatives.append(label)
        else:raise AssertionError('Unexpected acceptance: '+label)
    for gate in ['source','context','localization','naturalness','formatting']:
        reject('unreviewed_'+gate,lambda c,d,i,g=gate:d['records'][0]['review'].update({g:False}))
    for field,value in [('english','Different words.{PAD}'),('source_hex','00'),('current_hex','00'),
                        ('message_id',658),('proposed_compiled_hex','00'),('native_soft_wrap_reason','')]:
        reject('wrong_'+field,lambda c,d,i,k=field,v=value:d['records'][0].update({k:v}))
    reject('wrong_reference',lambda c,d,i:d['records'][0]['current_reference'].update(offset=0))
    reject('wrong_target',lambda c,d,i:c.update(target_COMMON_sha256='0'*64))
    reject('wrong_dependency',lambda c,d,i:c['dependencies'].update({str(PROOF):'0'*64}))
    reject('wrong_runtime',lambda c,d,i:i.replace_file('/__arm9__.bin',b'X'+arm[1:]))
    reject('repeat_application',lambda c,d,i:i.replace_file('/COMMON/MESFILE.DK4',target_common))
    assert len(negatives)==16
    save(ROOT/'negative_cases.json',dict(cases=negatives,all_rejected_before_image_mutation=True))
    registry,builder=Path('translations/release_stack.json'),Path('scripts/build_integrated_release.py')
    rb,bb=registry.read_bytes(),builder.read_bytes();stack=json.loads(rb)
    assert PROFILE not in stack['profiles'] and len(stack['accepted_layers'])==114
    stage=b'''    shop657_reflow = profile_config.get('shop657_full_width_reflow')
    if shop657_reflow:
        from dk4tool.patch.shop_657_reflow import apply_release as apply_shop657_reflow

        shop657_report = apply_shop657_reflow(candidate, baseline, shop657_reflow)
        shop657_path = '/COMMON/MESFILE.DK4'
        grouped.setdefault(shop657_path, [])
        changed_records.setdefault(shop657_path, []).append('COMMON_MESSAGE_657')
        relocation_checks.setdefault(shop657_path, {})['shop657_full_width_reflow'] = {
            'release_config': shop657_reflow,
            'release_config_sha256': sha256(Path(shop657_reflow).read_bytes()),
            'proof': shop657_report}
        release_batches.append(Path(shop657_report['manuscript']))

'''
    anchor=b'    # Lexically valid "% o"'
    assert bb.count(anchor)==1 and b"profile_config.get('shop657_full_width_reflow')" not in bb
    updated_builder=bb.replace(anchor,stage+anchor,1);compile(updated_builder,str(builder),'exec')
    profile=deepcopy(stack['profiles'][PARENT_PROFILE])
    profile.update(status='experimental',shop657_full_width_reflow=CONFIG.as_posix(),
        description='Complete current560-entry translation/font/Square-repair stack plus full-width657 reflow; no promotion.',
        note='Retains every word and all display/code/substitution rules. One source-locked COMMON message; no graphics or runtime changes. Actual screen verification pending.')
    stack['profiles'][PROFILE]=profile
    newline='\r\n' if b'\r\n' in rb else '\n'
    encoded=(json.dumps(stack,ensure_ascii=False,indent=2)+'\n').replace('\n',newline).encode('utf-8')
    (ROOT/'registry_before.json').write_bytes(rb);(ROOT/'builder_before.py').write_bytes(bb)
    (ROOT/'registry_after.json').write_bytes(encoded);(ROOT/'builder_after.py').write_bytes(updated_builder)
    assert registry.read_bytes()==rb and builder.read_bytes()==bb
    builder.write_bytes(updated_builder);registry.write_bytes(encoded)
    restored=json.loads(registry.read_bytes());restored['profiles'].pop(PROFILE)
    assert restored==json.loads(rb) and builder.read_bytes().replace(stage,b'',1)==bb
    save(ROOT/'registration_receipt.json',dict(profile=PROFILE,parent_profile=PARENT_PROFILE,
        registry_before_sha256=sha(rb),registry_after_sha256=sha(encoded),builder_before_sha256=sha(bb),builder_after_sha256=sha(updated_builder),
        config=str(CONFIG),config_sha256=sha(CONFIG.read_bytes()),native_copies=7336,negative_cases=16,
        accepted_layers_and_promoted_main_preserved=True,no_ROM_created_here=True,
        viewed_six_native_preview_tiles=True,full_goal_complete=False,producer_sha256=sha(Path(__file__).read_bytes())))
    print(dict(profile=PROFILE,native_copies=7336,negatives=16,registered=True),flush=True)
