"""Registered prefix-extension successor retaining the original runtime_bounds stage."""
from scripts.registered_canonical_extension_resume_v3 import run_driver


def main():
    run_driver('runtime_bounds', __file__)


if __name__ == '__main__':
    main()
