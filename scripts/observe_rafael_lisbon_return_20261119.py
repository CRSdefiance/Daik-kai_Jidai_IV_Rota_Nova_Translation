"""Continue the verified Ceuta voyage on ordinary controls from the Port menu."""

from inspect import getsource
from pathlib import Path
from types import FunctionType

from scripts import observe_rafael_ceuta_arrival_20261119 as original
from scripts import register_rafael_ceuta_contract_routes_20261119 as active
from scripts import replay_rafael_ceuta_contract_routes_20261119 as prior
from scripts.source_locked_derivation_v5118 import checked_text

ROOT = Path('work/rafael_lisbon_return_20261119')
CAPTURE = ROOT/'capture'
JOURNAL = ROOT/'navigation.jsonl'
PREFIX = prior.CAPTURE/'capture_report.json'
START = 50165


def main():
    probe = checked_text(getsource(original.make_observer), {
        '    env = vars(story)': '''    code = checked_text(code, {
        '                assert len(self.rows) < 20000':
            '                if frame < START:\\n                    return\\n                assert len(self.rows) < 20000',
    })
    env = vars(story)''',
        'REQUESTS=common.REQUESTS, __file__=__file__': 'REQUESTS=common.REQUESTS, START=START, __file__=__file__',
    })
    bootstrap = checked_text(getsource(original.main), {
        "'29295', '33860', '34420'": "str(START)",
    })
    env = vars(original)|dict(active=active,ROOT=ROOT,CAPTURE=CAPTURE,JOURNAL=JOURNAL,PREFIX=PREFIX,START=START,__file__=__file__)
    exec(compile(probe,__file__+'::observer','exec'),env)
    exec(compile(bootstrap,__file__+'::ordinary-return','exec'),env)
    env['main']()


if __name__=='__main__':
    main()
