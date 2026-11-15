"""Resolve the seven source role selectors on Rafael3894's own startup."""
from scripts.bind_rafael_B281_B300_roles_v1 import source as previous
from scripts.source_locked_derivation_v5118 import checked_text


source = checked_text(previous, {
    'assert len(records)==79 and selectors==[207,208,211,215,216]':
        'assert len(records)==148 and selectors==[207,208,211,214,215,216,222]',
})

if __name__ == '__main__':
    exec(compile(source, __file__ + '::fresh-148-role-record-bindings', 'exec'), globals())
