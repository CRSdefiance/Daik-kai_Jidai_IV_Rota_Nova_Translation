"""Execute the unchanged scoped-reuse binder exactly once."""
from scripts import extract_editorial_current_scope_reuse_v1 as previous

# v1 preserved the original module's __main__ footer, then called main again.
# Importing it under its module name is safe; use a non-main compilation context
# here and make the single explicit entry-point call below.
env={**previous.env,'__name__':'qualified_scoped_current_binding','__file__':__file__}
exec(compile(previous.source,__file__+'::same-native-guards-single-entry-point','exec'),env)

if __name__=='__main__':
    env['main']()
