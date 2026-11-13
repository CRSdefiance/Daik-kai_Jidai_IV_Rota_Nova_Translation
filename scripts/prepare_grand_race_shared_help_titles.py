"""Prepare the reviewed help variant required by the full race UI allocation."""

import json
from pathlib import Path

from dk4tool.patch.grand_race_help_shared_titles import (
    HELP,
    MENU,
    compile_records,
    sha,
    validate_release_batch,
)
from dk4tool.rom.nds import NdsImage


def main():
    source = NdsImage.open('out/raphael_natural_v2_accepted_base.nds').read_file('/__arm9__.bin')
    batch = {'format': 'dk4-arm9-fixed-text-batch-v1', 'file_path': '/__arm9__.bin',
             'source_file_sha256': sha(source), 'target_locale': 'en-US',
             'scope': 'All nine complete reviewed help pages; About/Basic Rules share identical menu labels',
             'status': 'prepared-experimental-unregistered-runtime-pending',
             'native_shared_help_titles': {'help_batch': HELP, 'help_batch_sha256': sha(Path(HELP).read_bytes()),
                                           'menu_batch': MENU, 'menu_batch_sha256': sha(Path(MENU).read_bytes())},
             'records': compile_records(source)}
    validate_release_batch(batch, source)
    Path('translations/grand_race_help_shared_menu_titles_v2.json').write_text(json.dumps(batch, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print('Complete help variant prepared; two shared title pointers; 28 source-owned bytes available for full UI allocation.')


if __name__ == '__main__':
    main()
