import datetime
import os
import pickle

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

with open(os.path.join(BASE_DIR, 'db', 'wanshican_memo.pkl'), 'rb') as f:
    print(os.path.join(BASE_DIR, 'db', 'wanshican_memo.pkl'))
    memo_list = pickle.loads(f.read())
    print(memo_list)
