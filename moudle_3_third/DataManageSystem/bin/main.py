import os
import sys
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

from core import log_function, crawler, image, office, user_manage

def main():
    user_manage.main()

if __name__ == "__main__":
    main()