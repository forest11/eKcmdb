#import optparse
import sys
import os


if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")
    import django
    django.setup()

    from backend.jumpserver import main
    main.ManagementUtily(sys.argv[0:])
