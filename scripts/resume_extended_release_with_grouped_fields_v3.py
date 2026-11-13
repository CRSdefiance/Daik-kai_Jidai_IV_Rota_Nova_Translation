"""Registered prefix-extension successor retaining the original grouped_fields stage."""
from scripts.registered_canonical_extension_resume_v3 import run_driver


def main():
    run_driver('grouped_fields', __file__)


if __name__ == '__main__':
    main()
