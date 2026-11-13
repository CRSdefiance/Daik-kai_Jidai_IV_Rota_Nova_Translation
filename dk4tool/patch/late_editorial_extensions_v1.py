"""Plan ordered source-qualified late editorial layers, then commit one NDS object.

Each adapter supplies its own frozen native/editorial/evidence contract. This
shared entry point preserves the complete predecessor and validates manifest
records and every unowned file/component before committing any extension.
"""
import importlib
import re
from copy import deepcopy
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha

BUILDER_STAGE = """    late_editorial_specs = profile_config.get('late_editorial_extensions', [])
    if late_editorial_specs:
        from dk4tool.patch.late_editorial_extensions_v1 import apply_extensions

        late_editorial_reports = apply_extensions(candidate, baseline, late_editorial_specs, release_batches)
        for late_editorial_report in late_editorial_reports:
            for late_editorial_file in late_editorial_report['files']:
                late_editorial_path = late_editorial_file['file_path']
                grouped.setdefault(late_editorial_path, [])
                changed_records.setdefault(late_editorial_path, []).extend(row['id'] for row in late_editorial_file['changed_records'])
                relocation_checks.setdefault(late_editorial_path, {})['late_editorial:' + late_editorial_report['extension_id']] = late_editorial_report
            release_batches.extend(Path(path) for path in late_editorial_report['manuscripts'])

"""


def require(value, message):
    if not value:
        raise ValueError('Late editorial extension: ' + message)


def plan_extensions(image, baseline, specs, existing_manuscripts=()):
    require(isinstance(specs, list) and bool(specs), 'nonempty ordered extension list required')
    keys = {'id', 'module', 'module_sha256', 'config', 'config_sha256', 'parent_ROM_sha256', 'target_ROM_sha256'}
    seen, modules, configs = set(), set(), set()
    manuscripts = {str(Path(p).resolve()) for p in existing_manuscripts}
    original, original_baseline = bytes(image.rom.save()), bytes(baseline.rom.save())
    working = deepcopy(image)
    reports = []
    for spec in specs:
        require(isinstance(spec, dict) and set(spec) == keys, 'exact extension schema required')
        ident, module_name = spec['id'], spec['module']
        require(isinstance(ident, str) and re.fullmatch(r'[a-z][a-z0-9_-]*', ident) and ident not in seen, 'unique extension identity required')
        require(isinstance(module_name, str) and re.fullmatch(r'dk4tool\.patch\.[a-z][a-z0-9_]*', module_name) and module_name not in modules, 'unique owned production adapter required')
        module_path = Path(*module_name.split('.')).with_suffix('.py')
        config_path = Path(spec['config'])
        require(config_path.resolve().is_relative_to(Path('translations').resolve()) and config_path.suffix == '.json' and str(config_path.resolve()) not in configs, 'unique registered local release configuration required')
        require(module_path.is_file() and sha(module_path.read_bytes()) == spec['module_sha256'], 'complete frozen production adapter identity')
        require(config_path.is_file() and sha(config_path.read_bytes()) == spec['config_sha256'], 'complete frozen release configuration identity')
        before = bytes(working.rom.save())
        require(sha(before) == spec['parent_ROM_sha256'], 'complete ordered predecessor identity')
        module = importlib.import_module(module_name)
        require(Path(module.__file__).resolve() == module_path.resolve() and callable(getattr(module, 'plan_release', None)), 'exact owned pure planning entry point required')
        planned_rom, report = module.plan_release(working, deepcopy(baseline), config_path)
        require(bytes(working.rom.save()) == before and bytes(image.rom.save()) == original and bytes(baseline.rom.save()) == original_baseline, 'planner must preserve all caller NDS objects')
        planned = deepcopy(working)
        planned.rom = planned_rom
        after = bytes(planned.rom.save())
        require(sha(after) == spec['target_ROM_sha256'] and after != before, 'complete tested target image identity')
        require(isinstance(report, dict) and report.get('one_complete_NDS_object_commit_after_all_gates') is True, 'complete guarded planner contract required')
        paths, record_keys = set(), set()
        require(isinstance(report.get('files'), list) and bool(report['files']), 'nonempty exact changed-file reports required')
        for file in report['files']:
            path = file['file_path']
            require(path not in paths and file['source_sha256'] == sha(working.read_file(path)) and file['target_sha256'] == sha(planned.read_file(path)) and file['source_sha256'] != file['target_sha256'], 'complete unique changed-file identity')
            require(isinstance(file['changed_records'], list) and bool(file['changed_records']), 'source-qualified changed records required')
            for row in file['changed_records']:
                key = path, row['id']
                require(key not in record_keys and row['file_path'] == path, 'unique file-qualified changed-record identity')
                record_keys.add(key)
            paths.add(path)
        changed = {p for _, p, value in working.iter_files() if planned.read_file(p) != value}
        require(changed == paths and all(planned.read_file(p) == value for p, value in working.iter_components()), 'every unowned file/component must remain exact')
        require(set((r['file_path'], r['id']) for r in report['changed_records']) == record_keys, 'complete manifest record membership required')
        listed = report.get('manuscripts')
        require(isinstance(listed, list) and bool(listed), 'source-qualified manuscripts required')
        for path in listed:
            resolved = str(Path(path).resolve())
            require(Path(path).is_file() and resolved not in manuscripts, 'each manuscript must run exactly once after its complete prefix')
            manuscripts.add(resolved)
        reports.append(dict(**report, extension_id=ident, module=module_name, module_sha256=spec['module_sha256'],
             release_config=str(config_path), release_config_sha256=spec['config_sha256'],
             parent_ROM_sha256=spec['parent_ROM_sha256'], target_ROM_sha256=spec['target_ROM_sha256']))
        seen.add(ident)
        modules.add(module_name)
        configs.add(str(config_path.resolve()))
        working = planned
    require(bytes(image.rom.save()) == original and bytes(baseline.rom.save()) == original_baseline, 'no caller mutation before complete extension chain passes')
    return working.rom, reports


def apply_extensions(image, baseline, specs, existing_manuscripts=()):
    planned, reports = plan_extensions(image, baseline, specs, existing_manuscripts)
    image.rom = planned
    return reports
