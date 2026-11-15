"""Run the existing controlled native Refit font proof on the six revisions."""

from pathlib import Path

from scripts import stage_refit_help_wraps_20261115 as stage
from scripts.source_locked_derivation_v5118 import checked_text


def main():
    staged = stage.base.load(stage.STORED)
    assert stage.base.digest(stage.ROM) == staged['candidate_sha256']
    assert stage.base.digest(stage.REVIEW) == staged['manuscript_sha256']
    output = stage.ROOT / 'native_verified'
    assert not output.exists()
    producer = Path('scripts/verify_refit_editorial_v830.py')
    source = checked_text(producer.read_text(encoding='utf-8'), {
        'from scripts.prepare_refit_editorial_v830 import MANUSCRIPT, ROM, ROOT':
            'from scripts.stage_refit_help_wraps_20261115 import REVIEW as MANUSCRIPT, ROM, ROOT\n'
            "ROOT = ROOT / 'native_verified'",
        "    assert manuscript['current_candidate_sha256'] == sha(ROM.read_bytes())":
            "    from scripts.stage_refit_help_wraps_20261115 import REVISIONS, STORED\n"
            "    assert read(STORED)['candidate_sha256'] == sha(ROM.read_bytes())\n"
            "    manuscript['records'] = [row for row in manuscript['records'] if row['message_id'] in REVISIONS]\n"
            "    assert len(manuscript['records']) == len(REVISIONS)",
        "{record['editorial_decision']}": "{record['decision']}",
        'previews.mkdir(exist_ok=True)': 'previews.mkdir(parents=True)',
        '(line_index * 12 + y) * 168':
            '(line_index * 12 + y + 1) * 168',
        'assert actual == expected': 'assert actual == expected, (record["message_id"], lines)',
        'All31 current native fonts/independent complete planes/guards pass;four sheets await visual review.':
            'All six revised native font planes and guards passed.',
    })
    exec(compile(source, __file__ + '::native-refit-font-v830', 'exec'),
         {'__name__': '__main__', '__file__': __file__})


if __name__ == '__main__':
    main()
