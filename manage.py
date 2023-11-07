#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys

try:
    from django.core.management import execute_from_command_line
except ImportError as exc:
    raise ImportError(
        "Couldn't import Django. Are you sure it's installed and "
        "available on your PYTHONPATH environment variable? Did you "
        "forget to activate a virtual environment?"
    ) from exc


def main():
    """Run administrative tasks."""
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "wrap_gpt.settings")
    my_settings = sys.argv[1].split(',')
    for my_setting in my_settings:
        os.environ[my_setting.split(':')[0]] = my_setting.split(':')[1]
    execute_from_command_line(sys.argv[1:])


if __name__ == "__main__":
    main()
