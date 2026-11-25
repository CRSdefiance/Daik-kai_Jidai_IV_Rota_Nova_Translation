"""Only exact known six-outcome stages plus the exact additive B49 stage may surround the frozen builder."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.hodram_outcomes_builder_guard_v2 import (
    BUILDER,STAGE as STAGE_V3,LEGACY_STAGE,validate_builder_bytes as previous_validate,
)
from scripts.source_locked_derivation_v5118 import checked_text

STAGE_V4=checked_text(STAGE_V3,{'hodram_outcomes_editorial_v3':'hodram_outcomes_editorial_v4'})
STAGE_B49='''    hodram_B49_editorial_config = profile_config.get('hodram_B49_editorial')
    if hodram_B49_editorial_config:
        from dk4tool.patch.hodram_B49_editorial_v1 import apply_release as apply_hodram_B49_editorial

        hodram_B49_editorial_report = apply_hodram_B49_editorial(candidate, baseline, hodram_B49_editorial_config)
        for hodram_B49_file in hodram_B49_editorial_report['files']:
            hodram_B49_path = hodram_B49_file['file_path']
            grouped.setdefault(hodram_B49_path, [])
            changed_records.setdefault(hodram_B49_path, []).extend(row['id'] for row in hodram_B49_file['changed_records'])
            relocation_checks.setdefault(hodram_B49_path, {})['hodram_B49_editorial'] = {
                'release_config': hodram_B49_editorial_config,
                'release_config_sha256': sha256(Path(hodram_B49_editorial_config).read_bytes()),
                'proof': hodram_B49_editorial_report}
        for hodram_B49_manuscript in hodram_B49_editorial_report['manuscripts']:
            more_batch = Path(hodram_B49_manuscript)
            if more_batch in release_batches:
                raise ValueError('Hodram B49 stage must run once after the complete V8377 stack')
            release_batches.append(more_batch)

'''
ANCHOR=b'    # Lexically valid "% o"'

def validate_builder_bytes(raw,digest):
    if not isinstance(raw,bytes):raise ValueError('Hodram builder guard: complete builder bytes required')
    variants=[('preserved-v2',LEGACY_STAGE.encode()),('preserved-v3',STAGE_V3.encode()),('compatible-v4',STAGE_V4.encode())]
    b49=STAGE_B49.encode();marker=b"profile_config.get('hodram_B49_editorial')"
    if sha(raw)==digest:
        previous=previous_validate(raw,digest)
        return dict(**previous,exact_B49_owned_stage_inverse=False,compatible_stage_version=None)
    present=[(name,stage) for name,stage in variants if raw.count(stage)==1]
    if len(present)!=1 or sum(raw.count(stage) for _,stage in variants)!=1:
        raise ValueError('Hodram builder guard: exactly one complete known outcome stage required')
    name,stage=present[0]
    if raw.count(ANCHOR)!=1 or raw.count(b49)>1 or raw.count(marker)!=raw.count(b49):
        raise ValueError('Hodram builder guard: exact single B49 stage required')
    if raw.count(b49):
        if name!='compatible-v4' or raw.index(stage)+len(stage)!=raw.index(b49) or raw.index(b49)+len(b49)!=raw.index(ANCHOR):
            raise ValueError('Hodram builder guard: B49 must follow compatible complete V8377 andprecede safety exactly')
        normalized=raw.replace(b49,b'',1)
    else:
        normalized=raw
    if name=='compatible-v4':normalized=normalized.replace(stage,STAGE_V3.encode(),1)
    previous=previous_validate(normalized,digest)
    inverse=raw.replace(stage,b'',1)
    if b49 in inverse:inverse=inverse.replace(b49,b'',1)
    if sha(inverse)!=digest:
        raise ValueError('Hodram builder guard: every unowned frozen builder byte must invert exactly')
    compile(raw,str(BUILDER),'exec')
    return dict(**previous,exact_B49_owned_stage_inverse=b49 in raw,compatible_stage_version=name,whole_original_builder_inverse_sha256=sha(inverse))

def checked_dependency(path,digest):
    path=Path(path)
    if path.resolve()==BUILDER:validate_builder_bytes(path.read_bytes(),digest)
    elif sha(path.read_bytes())!=digest:raise ValueError('Native dependency changed:'+str(path))
    return True
