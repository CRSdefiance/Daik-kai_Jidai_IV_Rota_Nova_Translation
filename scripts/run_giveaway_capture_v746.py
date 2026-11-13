"""Run the unchanged headless frontend with the explicit current role adapter."""

import runpy

from scripts import native_missionary_fixture_v623 as legacy
from scripts.native_missionary_fixture_v746 import assign

if __name__ == '__main__':
    legacy.assign = assign
    runpy.run_path('scripts/headless_desmume_v193.py', run_name='__main__')
