"""Clear redundant non-ROM staging only after release and Drive verification."""
from scripts import cleanup_fernando_parallel_routes_20261121 as template
from scripts import register_refit_sailing_parallel_routes_20261121 as release
from scripts.source_locked_derivation_v5118 import checked_text


main_source = checked_text(template.main_source, {
    '"release_stack_with_fernando_parallel_routes.json"': '"release_stack_with_refit_sailing_parallel_routes.json"',
})
scope = template.scope | {"release": release, "base": release.base, "stage": release.stage}
exec(compile(main_source, __file__, "exec"), scope)


if __name__ == "__main__":
    scope["main"]()
