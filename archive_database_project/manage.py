#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys

from magazine_archive import functions as fc


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'archive_database.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


def exportData():

    # deleta current file structure
    for file in os.listdir('magazine_archive/static/magazine/temp'):
        if file in ['temp_img', 'temp_file']:
            for img in os.listdir('magazine_archive/static/magazine/temp/temp_img'):
                os.remove(f'magazine_archive/static/magazine/temp/temp_img/{img}')
            continue
        os.remove(f'magazine_archive/static/magazine/temp/{file}')

    # recreate from database incase changes
    
    fc.exportAll()


if __name__ == '__main__':
    exportData()
    main()