"""Register Inn23 after the complete V799 inherited stack; actual scenes pending."""

from copy import deepcopy
from pathlib import Path

from dk4tool.patch import inn_editorial as owned
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import common_message_entries
from scripts.verify_village_wrap_v608 import read,save

ROOT=owned.ROOT
CONFIG=Path('translations/inn_editorial_release_v1.json')
MANUSCRIPT=Path('translations/inn_editorial_manuscript_v3.json')
DRAFT=Path('translations/inn_editorial_manuscript_v2.json')
TIME=Path('translations/inn_time_phrases_manuscript_v2.json')


def main():
    assert 'all-routes-unified-v803' not in read('translations/release_stack.json')['profiles']
    if any(p.exists() for p in (CONFIG,MANUSCRIPT,TIME)):
        # A failed validation never registered this draft. Preserve that exact
        # attempt before repairing its header; registered artifacts stay frozen.
        backup=ROOT/'unregistered_header_attempt_1';assert not backup.exists()
        backup.mkdir();archived={}
        for path in (CONFIG,MANUSCRIPT,TIME):
            if path.exists():
                raw=path.read_bytes();(backup/path.name).write_bytes(raw);archived[str(path)]=sha(raw)
        save(backup/'archive.json',dict(registered=False,files=archived,reason='Time-phrase draft omitted supported encoder/review_gates declarations;no ROM build or registry profile existed.'))
    production=deepcopy(read(DRAFT));native=read(ROOT/'production_layout.json')
    assert native['manuscript_sha256']==sha(DRAFT.read_bytes()) and native['native_layouts']==1169
    canonical=NdsImage.open('out/raphael_natural_v2_accepted_base.nds')
    accepted=common_message_entries(canonical.read_file('/COMMON/MESFILE.DK4'),canonical.read_file('/__arm9__.bin'),clean=False)
    for row in production['records']:
        assert all(row['review'][g] for g in ('source','context','localization','naturalness')) and not row['review']['formatting']
        row['canonical_source_hex']=accepted[row['message_id']].text.hex()
        row['review']['formatting']=True
        row['status']='source-native-production-reviewed;experimental-actual-revised-playback-pending'
        row['context']+=' V803 verifies the stored paragraph through the original trampoline and exact caller contract. Complete native copies and96 font planes pass;actual revised playback remains required.'
    production.update(reviewed_research_manuscript=str(DRAFT),reviewed_research_manuscript_sha256=sha(DRAFT.read_bytes()),
        status='registered-experimental-actual-gameplay-pending',production_approval=True,ROM_changed=False,whole_batch_completion_credit=False)
    save(MANUSCRIPT,production)
    time=deepcopy(read('translations/inn_time_phrases_manuscript_v1.json'))
    for row in time['records']:
        row['review']['formatting']=True
        row['localization_note']='Full prose uses the source-owned40-byte time allocation and the freshly proven unreferenced12-byte former Military Investment slot. The complete luxury-goods phrase is rebound within those allocations. Native provider144 cases and complete paragraph fonts pass;actual revised rumors pending.'
    time.update(encoder='dialogue-relocatable-v1',review_gates=['source','context','localization','naturalness','formatting'],
        native_format='owned-Cstrings;exact four-literal source map plus indexed luxury-goods phrase',
        production_approval=True,production_ownership_proof='work/analysis/inn_runtime_v802/bounded_runtime_plan.json',actual_revised_gameplay_pending=True)
    save(TIME,time)
    rom=NdsImage.open('out/all_routes_combined_v799_candidate.nds')
    c,a,proof=owned.plan(rom.read_file('/COMMON/MESFILE.DK4'),rom.read_file('/__arm9__.bin'),production['records'])
    assert c==(ROOT/'COMMON_RESEARCH_ONLY.bin').read_bytes() and a==(ROOT/'COMBINED_ARM9_RESEARCH_ONLY.bin').read_bytes()
    registry=read('translations/release_stack.json');assert 'all-routes-unified-v803' not in registry['profiles'] and len(registry['accepted_layers'])==114
    inherited=deepcopy(registry['profiles']['all-routes-unified-v799']);frozen={}
    for value in inherited.values():
        if isinstance(value,str) and value.endswith('.json') and Path(value).exists():
            cfg=read(value);frozen[value]=sha(Path(value).read_bytes())
            for p,h in cfg.get('dependencies',{}).items():assert sha(Path(p).read_bytes())==h,p;frozen[p]=h
    save(ROOT/'frozen_prior_dependencies.json',frozen);save(ROOT/'release_stack_before_v803.json',registry)
    files=[Path(p) for p in ('dk4tool/patch/inn_editorial.py','dk4tool/patch/inn_editorial_runtime.py',
        'dk4tool/patch/palace_label_boundaries.py','dk4tool/patch/palace_editorial_runtime.py',
        'dk4tool/script/common_message_table.py','scripts/prepare_item_common_v788.py',
        'scripts/prepare_recruitment_common_v772.py','scripts/context_inn_v801.py','scripts/verify_inn_baseline_v801.py',
        'scripts/prepare_inn_editorial_v801.py','scripts/verify_inn_runtime_v802.py','scripts/probe_inn_layout_v802.py',
        'scripts/refine_inn_stay_v802.py','scripts/prepare_inn_v803.py','scripts/verify_inn_copies_v803.py',
        'scripts/native_call_abi_v764.py','scripts/native_machine_scoped_v764.py',str(DRAFT),str(TIME))]
    files += [ROOT/p for p in ('production_layout.json','prospective_common_repack.json')]
    files += [Path('work/analysis/inn_context_v801')/p for p in ('native_context.json','baseline_and_time_ownership.json')]
    files += [Path('work/analysis/inn_runtime_v802')/p for p in ('bounded_runtime_plan.json','scope_proof.json','status_contracts.json',
        'complete_month_phrases.json','layout/verification.json','layout/visual_review.json','layout_v2_delta/verification.json','layout_v2_delta/visual_review.json')]
    first,last=proof['repacked_block_range'];files += [ROOT/f'native_copies/native_copies_block_{b:02d}.json' for b in range(first,last+1)]
    save(CONFIG,dict(format='dk4-inn-editorial-v1',source_common_sha256=owned.SOURCE_COMMON,source_arm9_sha256=owned.SOURCE_ARM,
        target_common_sha256=sha(c),target_arm9_sha256=sha(a),directory_sha256=proof['directory_sha256'],
        manuscript=str(MANUSCRIPT),manuscript_sha256=sha(MANUSCRIPT.read_bytes()),
        time_manuscript=str(TIME),time_manuscript_sha256=sha(TIME.read_bytes()),dependencies={str(p):sha(p.read_bytes()) for p in files}))
    assert owned.apply_release(rom.read_file('/COMMON/MESFILE.DK4'),rom.read_file('/__arm9__.bin'),CONFIG)[:2]==(c,a)
    registry['profiles']['all-routes-unified-v803']={**inherited,'inn_editorial':str(CONFIG),'status':'experimental',
        'description':'Complete V799 stack plus23 source-reviewed Inn paragraphs and full relative-month prose in existing owned storage. Actual revised Inn gameplay pending.'}
    save('translations/release_stack.json',registry)
    assert all(sha(Path(p).read_bytes())==h for p,h in frozen.items())
    print('V803 registered;all older profiles,470 batches,114 accepted layers and frozen dependencies retained;actual revised Inn scenes pending.',flush=True)


if __name__=='__main__':main()
