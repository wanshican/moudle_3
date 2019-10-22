import os
import sys
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

from core import memo, log_function


def main():
    # try:
    #     ma = memo.MemoAdmin()
    #     # ma.login()
    #     if sys.argv[1] in {'-a', '--add'}:
    #         ma.add()
    #     elif sys.argv[1] in {'-d', '--delete'}:
    #         ma.dele()
    #     elif sys.argv[1] in {'-m', '--modify'}:
    #         ma.modify()
    #     elif sys.argv[1] in {'-q', '--query'}:
    #         ma.query()
    #     elif sys.argv[1] in {'-s', '--save'}:
    #         ma.save()
    #     elif sys.argv[1] in {'-e', '--export'}:
    #         ma.export_pdf()
    #     elif sys.argv[1] in {'-qm', '--query_memo'}:
    #         ma.query_memo()
    #     elif sys.argv[1] in {'-se', '--send_email'}:
    #         ma.send_email()
    # except Exception as e:
    #     print(e)
    memo.main()
    

if __name__ == "__main__":
    main()



