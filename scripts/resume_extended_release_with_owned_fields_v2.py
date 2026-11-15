"""Registered canonical-prefix extension followed by the original owned_fields stage."""
from scripts.registered_canonical_extension_resume_v2 import run_driver


def main():
    run_driver('owned_fields', __file__)


if __name__ == '__main__':
    main()
