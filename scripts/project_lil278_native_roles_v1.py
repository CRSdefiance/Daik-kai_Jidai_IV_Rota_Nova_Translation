"""Bind the 141 saved Lil selector resolutions to their full clean headers."""

import inspect

from scripts import project_maria363_native_roles_v1 as previous
from scripts.source_locked_derivation_v5118 import checked_text


def main():
    source = checked_text(inspect.getsource(previous.main), {
        "'formatting_v1/role_bindings.json'": "'dynamic_roles_all_v1.json'",
        "{'ordinary-speech':6,'4100-style-alternative':85}":
            "{'ordinary-speech':2,'4100-style-alternative':139}",
        'Bound6 ordinary and85 virtual-style controls':
            'Bound 2 ordinary and 139 virtual-style controls',
    })
    from pathlib import Path

    env = {**vars(previous), 'ROOT': Path('work/Lil278_B299_B311_clean_20261110'), '__file__': __file__}
    exec(compile(source, __file__, 'exec'), env)
    env['main']()


if __name__ == '__main__':
    main()
