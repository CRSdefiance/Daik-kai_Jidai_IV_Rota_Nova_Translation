"""Bind all five original role selectors for the ruins encounters."""
from scripts.bind_rafael_B261_B280_roles_v1 import source as previous
from scripts.source_locked_derivation_v5118 import checked_text


source = checked_text(previous, {
    'assert len(records)==17 and selectors==[207,208]':
        'assert len(records)==79 and selectors==[207,208,211,215,216]',
})

if __name__ == '__main__':
    exec(compile(source, __file__ + '::all-five-current-role-selectors', 'exec'), globals())
