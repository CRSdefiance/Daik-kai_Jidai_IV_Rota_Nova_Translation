"""Allow only the exact owned additive builder stage, with a byte-exact inverse to the frozen builder."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha

BUILDER=Path('scripts/build_integrated_release.py').resolve()
STAGE='''    hodram_outcomes_editorial_config = profile_config.get('hodram_outcomes_editorial')
    if hodram_outcomes_editorial_config:
        from dk4tool.patch.hodram_outcomes_editorial_v2 import apply_release as apply_hodram_outcomes_editorial

        hodram_outcomes_editorial_report = apply_hodram_outcomes_editorial(candidate, baseline, hodram_outcomes_editorial_config)
        for hodram_outcomes_file in hodram_outcomes_editorial_report['files']:
            hodram_outcomes_path = hodram_outcomes_file['file_path']
            grouped.setdefault(hodram_outcomes_path, [])
            changed_records.setdefault(hodram_outcomes_path, []).extend(row['id'] for row in hodram_outcomes_file['changed_records'])
            relocation_checks.setdefault(hodram_outcomes_path, {})['hodram_outcomes_editorial'] = {
                'release_config': hodram_outcomes_editorial_config,
                'release_config_sha256': sha256(Path(hodram_outcomes_editorial_config).read_bytes()),
                'proof': hodram_outcomes_editorial_report}
        for hodram_outcomes_manuscript in hodram_outcomes_editorial_report['manuscripts']:
            more_batch = Path(hodram_outcomes_manuscript)
            if more_batch in release_batches:
                raise ValueError('Hodram B47/B48 stage must run once after the complete V8300 stack')
            release_batches.append(more_batch)

'''

def validate_builder_bytes(raw,digest):
    if sha(raw)==digest:return dict(original_frozen_builder=True,exact_owned_stage_inverse=False)
    stage=STAGE.encode('utf8');anchor=b'    # Lexically valid "% o"'
    if raw.count(stage)!=1 or raw.count(anchor)!=1 or sha(raw.replace(stage,b'',1))!=digest:
        raise ValueError('Hodram builder guard: exact single owned stage andwhole frozen builder inverse required')
    if not raw.index(b"profile_config.get('hodram_three_blocks_editorial')")<raw.index(stage)<raw.index(anchor):
        raise ValueError('Hodram builder guard: owned stage must follow full V8300 andprecede literal-percent safety')
    if raw.index(stage)+len(stage)!=raw.index(anchor):
        raise ValueError('Hodram builder guard: exact approved insertion boundary required')
    compile(raw,str(BUILDER),'exec')
    return dict(original_frozen_builder=False,exact_owned_stage_inverse=True)

def checked_dependency(path,digest):
    path=Path(path)
    if path.resolve()==BUILDER:validate_builder_bytes(path.read_bytes(),digest)
    elif sha(path.read_bytes())!=digest:raise ValueError('Native dependency changed:'+str(path))
    return True
