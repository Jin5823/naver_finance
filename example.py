import datetime
import pandas as pd
from finance_naver.naver_finance import naver_sise_day_url, get_naver_sise_day, get_naver_sise_high_down


data = get_naver_sise_high_down(1)
data.to_csv('sise_high_down.csv', mode='w', encoding='utf-8-sig', index=False)
