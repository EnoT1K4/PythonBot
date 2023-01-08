TOKEN = '5314760304:AAEFM60qOzXSlZj5GuIwH9nKX6uuiPE2CEo'
CHANELL_URL = 'https://t.me/lll1po_test'
CHANELL_ID = '@lll1po_test'
CHAT_ID = '@test_lll1po'
from db import Database
db = Database('Database.db')
a = db.get_admID()
ADMINS_ID = []
for i in range(len(a)):
    ADMINS_ID.append(a[i][0])
ADMIN_ID = '1531015280'
WORDS = []