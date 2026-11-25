"""Add original Town Commands navigation to the seven reviewed HELP articles."""

from pathlib import Path
from unittest.mock import patch

from scripts import prepare_general_help_v431 as general


def main():
    prose = dict(general.PROSE)
    prose[11] = (
        'Town Commands',
        "Select a building's sign to use its commands. Commands marked 'City only' are available only in a [[145|City]]. See [[12|Tavern]], [[21|Market]], [[26|Guild]], [[34|Inn]], [[35|Palace or Governor's Office]], [[42|Square]], [[44|Shipyard]], [[73|Port]], [[144|City Info]] and [[103|Shared Commands]]. You may also be able to visit local [[80|ruins]].",
        'City commands are selected through building signs. City-only commands require city classification. Preserve ten facility/data/shared-command links, the City-type link and the possible ruins visit.',
        'Restore the navigation prerequisite for Market21. City only distinguishes cities from ports; do not promise every city has ruins.')
    with patch.object(general, 'ROOT', Path('work/analysis/help_navigation_v433')), \
            patch.object(general, 'MANUSCRIPT', Path('translations/general_help_manuscript_v2.json')), \
            patch.object(general, 'PROSE', prose):
        general.main()


if __name__ == '__main__':
    main()
