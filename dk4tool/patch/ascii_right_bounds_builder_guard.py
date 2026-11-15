"""Qualify only the additive right-bound stage against the whole frozen builder.

Legacy layer configurations retain their exact dependency digest through an
immutable copy of the original builder. This guard separately proves that the
running builder is precisely the fully qualified V8865 builder plus this stage.
"""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.hodram_outcomes_builder_guard_v8 import validate_builder_bytes as validate_legacy

STAGE = '''    ascii_right_bounds_config = profile_config.get('ascii_glyph_right_bounds')
    if ascii_right_bounds_config:
        from dk4tool.patch.ascii_glyph_right_bounds import apply_release as apply_ascii_right_bounds

        ascii_right_bounds_source = candidate.read_file('/__arm9__.bin')
        ascii_right_bounds_target, ascii_right_bounds_proof = apply_ascii_right_bounds(
            ascii_right_bounds_source, ascii_right_bounds_config)
        candidate.replace_file('/__arm9__.bin', ascii_right_bounds_target)
        grouped.setdefault('/__arm9__.bin', [])
        changed_records.setdefault('/__arm9__.bin', []).extend(ascii_right_bounds_proof['changed_records'])
        relocation_checks.setdefault('/__arm9__.bin', {})['ascii_glyph_right_bounds'] = {
            'release_config': ascii_right_bounds_config,
            'release_config_sha256': sha256(Path(ascii_right_bounds_config).read_bytes()),
            'proof': ascii_right_bounds_proof}
        release_batches.append(Path(ascii_right_bounds_config))

'''.replace('\n', '\r\n')


def validate(raw, predecessor_digest):
    stage = STAGE.encode()
    boundary = b'    # Lexically valid "% o"'
    if raw.count(stage) != 1 or raw.count(boundary) != 1:
        raise ValueError('One exact glyph-bound stage required')
    if raw.index(stage) + len(stage) != raw.index(boundary):
        raise ValueError('Glyph bounds must immediately precede final safety gates')
    inverse = raw.replace(stage, b'', 1)
    if sha(inverse) != predecessor_digest:
        raise ValueError('Whole V8865 builder inverse changed')
    legacy = validate_legacy(inverse, '3becddbd3fb7f5da7ba68b7fde34532aa6e26eed911cc111df0c2a9912804d15')
    compile(raw, 'scripts/build_integrated_release.py', 'exec')
    return dict(whole_predecessor_builder_sha256=sha(inverse), legacy_contract=legacy,
                exact_single_right_bound_stage=True)


def validate_current(config):
    for path, digest in config['builder_dependencies'].items():
        if sha(Path(path).read_bytes()) != digest:
            raise ValueError('Glyph-bound builder dependency changed: ' + path)
    raw = Path('scripts/build_integrated_release.py').read_bytes()
    if sha(raw) != config['builder_predecessor_sha256']:
        raise ValueError('The complete canonical builder must remain byte-exact to V8865')
    return validate_legacy(raw, '3becddbd3fb7f5da7ba68b7fde34532aa6e26eed911cc111df0c2a9912804d15')
