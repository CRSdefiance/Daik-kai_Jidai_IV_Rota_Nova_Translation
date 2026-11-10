"""Registered canonical-prefix extension followed by the original owned_names stage."""
from scripts.registered_canonical_extension_resume_v2 import run_driver


def main():
    run_driver('owned_names', __file__)


if __name__ == '__main__':
    main()
