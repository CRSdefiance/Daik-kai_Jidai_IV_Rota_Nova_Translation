"""Register the51 ceremony paragraphs after the complete V803 stack."""

from copy import deepcopy
from pathlib import Path

from dk4tool.patch import ceremony_editorial as owned
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import common_message_entries
from scripts.ceremony_runtime_v808 import ROOT as RUNTIME_ROOT
from scripts.verify_village_wrap_v608 import read,save

ROOT=owned.ROOT
CONFIG=Path('translations/ceremony_editorial_release_v1.json')
MANUSCRIPT=Path('translations/ceremony_editorial_manuscript_v3.json')
DRAFT=Path('translations/ceremony_editorial_manuscript_v2.json')


def main():
    registry=read('translations/release_stack.json')
    assert 'all-routes-unified-v809' not in registry['profiles'] and not CONFIG.exists() and not MANUSCRIPT.exists()
    inherited=deepcopy(registry['profiles']['all-routes-unified-v803']);frozen={}
    for value in inherited.values():
        if isinstance(value,str) and value.endswith('.json') and Path(value).exists():
            cfg=read(value);frozen[value]=sha(Path(value).read_bytes())
            for p,h in cfg.get('dependencies',{}).items():assert sha(Path(p).read_bytes())==h,p;frozen[p]=h
    assert len(registry['accepted_layers'])==114
    save(ROOT/'frozen_prior_dependencies.json',frozen);save(ROOT/'release_stack_before_v809.json',registry)
    production=deepcopy(read(DRAFT));native=read(ROOT/'production_layout.json')
    assert native['manuscript_sha256']==sha(DRAFT.read_bytes()) and native['native_layouts']==201
    canonical=NdsImage.open('out/raphael_natural_v2_accepted_base.nds')
    accepted=common_message_entries(canonical.read_file('/COMMON/MESFILE.DK4'),canonical.read_file('/__arm9__.bin'),clean=False)
    production['records']=[r for r in production['records'] if r['message_id']!=64]
    for row in production['records']:
        assert all(row['review'][g] for g in ('source','context','localization','naturalness')) and not row['review']['formatting']
        row['canonical_source_hex']=accepted[row['message_id']].text.hex()
        row['review']['formatting']=True
        row['context']+=' V809 verifies the stored paragraph through its exact native parent and complete independent font plane. Actual ceremony playback and outcomes remain pending.'
        row['status']='source-native-production-reviewed;experimental-actual-revised-playback-pending'
    production.update(reviewed_research_manuscript=str(DRAFT),reviewed_research_manuscript_sha256=sha(DRAFT.read_bytes()),
        retained_shared64_not_changed_or_newly_formatting_approved=True,
        status='registered-experimental-actual-gameplay-pending',production_approval=True,
        whole_batch_completion_credit=False,ROM_changed=False)
    save(MANUSCRIPT,production)
    rom=NdsImage.open('out/all_routes_combined_v803_candidate.nds')
    c,a,proof=owned.plan(rom.read_file('/COMMON/MESFILE.DK4'),rom.read_file('/__arm9__.bin'),production['records'])
    assert c==(ROOT/'COMMON_RESEARCH_ONLY.bin').read_bytes() and a==(ROOT/'COMBINED_ARM9_RESEARCH_ONLY.bin').read_bytes()
    files=[Path(p) for p in ('dk4tool/patch/ceremony_editorial.py','scripts/ceremony_runtime_v808.py',
        'scripts/prepare_ceremony_common_v809.py','scripts/verify_ceremony_runtime_v808.py',
        'scripts/verify_ceremony_consumers_v808.py','scripts/verify_ceremony_production_v809.py',
        'scripts/verify_ceremony_copies_v809.py','scripts/prepare_item_common_v788.py',
        'scripts/prepare_recruitment_common_v772.py','scripts/context_ceremony_v806.py',
        'scripts/native_machine_scoped_v764.py','scripts/native_call_abi_v764.py',str(DRAFT),
        'work/analysis/ceremony_context_v806/native_context.json',
        'work/analysis/ceremony_layout_v807_name_bounds/runtime_size_measurement.json',
        'work/analysis/ceremony_layout_v807_name_bounds/research_report.json',
        'work/analysis/ceremony_layout_v807_name_bounds/visual_review.json')]
    files += [RUNTIME_ROOT/p for p in ('prospective_runtime_plan.json','bounded_storage_proof.json','scope_proof.json',
        'status_contracts.json','literal_equivalence.json','native_runtime_verification.json','modal_scope.json','effective_consumer_formats.json')]
    files += [ROOT/p for p in ('production_layout.json','prospective_common_repack.json','complete_native_copies.json')]
    files += [ROOT/f'native_copies/native_copies_block_{n:02d}.json' for n in range(41)]
    save(CONFIG,dict(format='dk4-ceremony-editorial-v1',source_common_sha256=owned.SOURCE_COMMON,source_arm9_sha256=owned.SOURCE_ARM,
        target_common_sha256=sha(c),target_arm9_sha256=sha(a),directory_sha256=proof['directory_sha256'],
        manuscript=str(MANUSCRIPT),manuscript_sha256=sha(MANUSCRIPT.read_bytes()),dependencies={str(p):sha(p.read_bytes()) for p in files}))
    assert owned.apply_release(rom.read_file('/COMMON/MESFILE.DK4'),rom.read_file('/__arm9__.bin'),CONFIG)[:2]==(c,a)
    registry['profiles']['all-routes-unified-v809']={**inherited,'ceremony_editorial':str(CONFIG),'status':'experimental',
        'description':'Complete V803 stack plus51 source-reviewed ceremony paragraphs,exact protagonist selectors and six result notices in existing384-byte banks and128-byte modal wrapper. Actual ceremony gameplay pending.'}
    save('translations/release_stack.json',registry)
    assert all(sha(Path(p).read_bytes())==h for p,h in frozen.items())
    print('V809 registered after complete V803;all prior profiles,470 batches,114 accepted layers and frozen dependencies retained. Actual ceremony scenes pending.',flush=True)


if __name__=='__main__':main()
