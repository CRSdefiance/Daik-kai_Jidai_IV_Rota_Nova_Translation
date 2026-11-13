"""Localize the original shark choices and scope portrait wrapping to this exchange."""

import inspect

from dk4tool.patch import mutiny_choice_labels_v1 as labels
from dk4tool.patch import mutiny_static_wrap_v1 as layout
from scripts.source_locked_derivation_v5118 import checked_text


SOURCE = '0a51098307e549ff3101a11ba04ab003e1f7b671cefe77f09b71ed26808e07fe'
TABLE = 0x119114
PRIOR = 0x01FFD814
SCOPE = {
    (0x02053C14, 0x270): (0x021164D0, 0x02116520, 0x02116660, 0x021167A0),
    (0x02054014, 0x274): (2425, 2430, 2435, 2436, 2441, 2442, 2443, 2448, 2449, 2450, 2451, 2452, 2453),
}
HOOK, LITERAL_COPY, MAXIMUM_TEMPLATE = layout.HOOK, layout.LITERAL_COPY, layout.MAXIMUM_TEMPLATE


def transform(source, choices):
    label_source = checked_text(inspect.getsource(labels.transform), {
        'Exact registered sailing-alert ARM9 required': 'Exact registered faction and epilogue ARM9 required',
        'assert len(labels) == 3': 'assert len(labels) == 2',
    })
    label_env = vars(labels) | {'SOURCE': SOURCE, 'TABLE': TABLE}
    exec(compile(label_source, __file__ + '::two-original-choice-pointers', 'exec'), label_env)
    env = vars(layout) | {'PRIOR': PRIOR, 'SCOPE': SCOPE, 'localize_labels': label_env['transform']}
    exec(compile(inspect.getsource(layout.assembly), __file__ + '::scoped-shark-portraits', 'exec'), env)
    source_code = checked_text(inspect.getsource(layout.transform), {'mutiny_selector=start': 'shark_selector=start'})
    exec(compile(source_code, __file__ + '::same-exact-layout-inverse', 'exec'), env)
    return env['transform'](source, choices)
