"""Independent production glyph evidence with semantic negative cases; no emulator replay."""
from copy import deepcopy
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.dialogue.hodram_B31_B53_profile_v1 import contract,validate_runtime,validate_approved_batch
from dk4tool.dialogue.hodram_B31_B53_names_v1 import validate_scoped_names
from dk4tool.patch.hodram_B31_B53_native_evidence_v1 import check_native_models
from scripts.review_Hodram_B31_B53_actual_v8744 import PROOFS
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/Hodram_B31_B53_native_validation_v8754')
DOC=Path('translations/hodram_B31_B53_editorial_manuscript_v5.json')
NAMES=Path('translations/hodram_B31_B53_speaker_name_review_v3.json')
def require(value,label):
    if not value:raise ValueError('B31/B53 native evidence: '+label)
if __name__=='__main__':
    assert not ROOT.exists();data={k:read(p) for k,p in PROOFS.items()};doc,names=map(read,[DOC,NAMES]);data.update(manuscript=doc,names=names)
    frozen=contract();validate_approved_batch(doc);validate_scoped_names(names);image=NdsImage.open(doc['current_ROM']);validate_runtime(image)
    modules=[Path('dk4tool/patch/hodram_B31_B53_native_guards_v1.py'),Path('dk4tool/patch/hodram_B31_B53_native_evidence_v1.py')]
    protected={Path(p) for p in frozen['dependencies']}|{DOC,NAMES,Path(__file__),*modules,Path('translations/release_stack.json'),Path('translations/editorial_review_current_v1.json'),Path('translations/rom_retention_pins.json'),Path(doc['current_ROM']),Path('work/clean.nds')}
    before={str(p):sha(p.read_bytes()) for p in protected}
    result=check_native_models(data,doc['records'],image,read,require)
    assert result['summary']['native_body_pages_recomputed']==6 and result['summary']['scoped_style11_nameplanes_recomputed']==2
    assert set(result['names'])=={34,113} and set(result['bodies'])=={'clean_Japanese','revised_English'}
    cases=[]
    def reject(label,mutate):
        changed=deepcopy(data);mutate(changed);assert changed!=data,label
        try:check_native_models(changed,doc['records'],image,read,require)
        except ValueError as error:
            text=str(error);assert 'Native dependency changed' not in text and 'Frozen Hodram-B31-B53 contract changed' not in text,(label,text)
            cases.append(dict(label=label,actual_changed_input=True,rejected=True,diagnostic=text))
        else:raise AssertionError('Changed native evidence accepted:'+label)
    reject('untrusted-page-adapter',lambda d:d['pages'].__setitem__('source_owned_target_page_adapter',d['pages']['source_owned_target_page_adapter']+'\n# untrusted'))
    reject('wrong-ARM9-binding',lambda d:d['models'].__setitem__('ARM9_sha256','0'*64))
    reject('wrong-font-binding',lambda d:d['models'].__setitem__('font_sha256','0'*64))
    reject('missing-source-model',lambda d:d['models']['native_models']['clean_Japanese'].pop())
    reject('missing-stored-model',lambda d:d['models']['native_models']['revised_English'].pop())
    reject('source-selector',lambda d:d['models']['native_models']['clean_Japanese'][0].__setitem__('source_selector',113))
    reject('stored-final-glyph-code',lambda d:d['models']['native_models']['revised_English'][0]['pages'][0]['events'][-1].__setitem__('code',d['models']['native_models']['revised_English'][0]['pages'][0]['events'][-1]['code']^1))
    reject('complete-plane-digest',lambda d:d['models']['native_models']['revised_English'][0]['pages'][0].__setitem__('native_plane_sha256','0'*64))
    reject('stored-body-byte',lambda d:d['models']['native_models']['revised_English'][0].__setitem__('input_hex',d['models']['native_models']['revised_English'][0]['input_hex'][:-2]))
    reject('unapproved-short-name',lambda d:d['models']['name_planes'][0].__setitem__('text','Hayreddin'))
    reject('name-width',lambda d:d['models']['name_planes'][0].__setitem__('original_pair_flush_width',d['models']['name_planes'][0]['original_pair_flush_width']+6))
    reject('extra-full-catalogue-nameplane',lambda d:d['models']['name_planes'].append(deepcopy(d['models']['name_planes'][0])))
    assert len(cases)==12 and {str(p):sha(p.read_bytes()) for p in protected}==before
    ROOT.mkdir(parents=True);save(ROOT/'independent_native_validation.json',dict(manuscript=str(DOC),manuscript_sha256=sha(DOC.read_bytes()),
        contract='translations/hodram_B31_B53_native_contract_v1.json',native_summary=result['summary'],
        six_complete_source_andstored_native_pages_two_current_progressive_names_andall_independent_pixels_exact=True,
        negative_cases=cases,negative_count=len(cases),every_negative_actual_input_changed_andsemantic_guard_rejected=True,
        all_frozen_dependency_andtrusted_adapter_guards_remained_enabled=True,all_protected_files_ROMs_registry_ledger_andsource_inputs_hash_exact=True,protected_hashes=before,
        disposable_native_CPU_checks_not_new_gameplay_andno_producer_replay=True,production_actual_control_references_loaders_readers_atomic_andregistered_work_pending=True,
        new_emulator_runs=0,new_credit=0,full_goal_complete=False,
        evidence={str(p):sha(p.read_bytes()) for p in [DOC,NAMES,*modules,Path(__file__)]}))
    print('Independent production native:6complete source/stored pages+2names match;12semantic defects reject withfrozen/trusted guardsactive. No emulator/ROMcommit orcredit.',flush=True)
