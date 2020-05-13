import os
import sys

from simple_mailer.web import get_application

sys.path.insert(0, os.path.dirname(__file__))

application = get_application()
