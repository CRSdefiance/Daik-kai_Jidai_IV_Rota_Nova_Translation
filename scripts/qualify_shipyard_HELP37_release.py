"""Qualify37 direct/shared plans,four coverage andtwo new native-control rejection cases."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import checked_text

source=checked_text(Path('scripts/qualify_town_HELP23_release.py').read_text(encoding='utf-8'),{
 'dk4tool.patch.town_help23_release_v1':'dk4tool.patch.shipyard_help37_release_v1',
 'Town_HELP23_release_qualification_20261104':'Shipyard_HELP37_release_qualification_20261104',
 'Town_HELP23_release_20261104':'Shipyard_HELP37_release_20261104',
 "len(proof['changed_records'])==23":"len(proof['changed_records'])==37",
 "('missing-offline-native-page','native'),('missing-observed-page','actual')]:":
 "('missing-offline-native-page','native'),('missing-observed-page','actual'),('wrong-Refit51-runtime','manuscript'),('wrong-Refit51-original-map','manuscript')]:",
 "r['topic_id']!=23":"r['topic_id']!=46",
 "        else:doc['actual_HELP_cases'].pop()":
 """        elif kind.startswith('wrong-Refit51'):
            row=next(r for r in doc['records'] if r['topic_id']==51);control=load(row['native_control_binding'])
            if kind=='wrong-Refit51-runtime':control['current_ARM9_sha256']='0'*64
            else:control['source51_symbol_mapping']['triangle']='Y'
            control_path=ROOT/(kind+'_control.json');save(control_path,control)
            row.update(native_control_binding=str(control_path),native_control_binding_sha256=sha(control_path.read_bytes()))
            config['dependencies'][str(control_path)]=sha(control_path.read_bytes())
        else:doc['actual_HELP_cases'].pop()""",
 'assert len(rejected)==4':
 "assert len(rejected)==6\n    assert 'same native control runtime' in rejected[-2]['error'] and 'original controls mapping' in rejected[-1]['error']",
 'Shared_HELP_T21_T43_formatting_20261104/preview_qualification_v2/qualification.json':
 'Shared_HELP_T44_T80_formatting_20261104/preview_qualification_v1/qualification.json',
 "len(load(formatter)['new_semantic_rejections'])==4":"len(load(formatter)['new_formatter_andindividual_gate_rejections'])==6",
 'Town23 direct/shared plans/four changed coverage guards pass;four formatter guards andten unchanged guards reused;all eight stages preserved.':
 'Help37 direct/shared plans/six changed coverage-control guards pass;six formatter guards andten unchanged source guards reused;all eight stages preserved.',
})
exec(compile(source,__file__+'::same-partial-coverage-source-contract-andnew-concrete-control-guard-qualification','exec'),globals())
