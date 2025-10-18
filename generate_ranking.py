import requests
import json
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
from collections import defaultdict

now_jst = datetime.now(ZoneInfo("Asia/Tokyo"))
timestamp = now_jst.strftime('%Y年%m月%d日 %H:%M:%S')

# User-Agent（Wikimediaのポリシーに準拠）
HEADERS = {
    'User-Agent': 'YukiBot/1.0 (https://github.com/yimam)'  # ご自身のURLや連絡先に変更してください
}

# 除外する記事名
EXCLUDE_TITLES = ['Main_Page', 'メインページ', '特別:検索']

# 日本語の曜日を表示する関数
def format_date_with_weekday(date):
    weekdays = ['月', '火', '水', '木', '金', '土', '日']
    return date.strftime('%Y/%m/%d') + f'（{weekdays[date.weekday()]}）'

def format_period_with_weekday(start_date):
    weekdays = ['月', '火', '水', '木', '金', '土', '日']
    start_jst = datetime.combine(start_date, datetime.min.time()) + timedelta(hours=9)
    end_jst = start_jst + timedelta(days=1) - timedelta(minutes=1)
    start_label = f"{start_jst.strftime('%Y年%m月%d日')}（{weekdays[start_jst.weekday()]}）"
    end_label = f"{end_jst.strftime('%Y年%m月%d日')}（{weekdays[end_jst.weekday()]}）"
    return f"{start_label}9時00分から{end_label}8時59分"

def format_period(start_date):
    start_jst = datetime.combine(start_date, datetime.min.time()) + timedelta(hours=9)
    end_jst = start_jst + timedelta(days=1) - timedelta(minutes=1)
    return f"{start_jst.strftime('%Y年%m月%d日')}9時00分から{end_jst.strftime('%Y年%m月%d日')}8時59分"

def get_topviews(date_str, project='ja.wikipedia.org'):
    url = f'https://wikimedia.org/api/rest_v1/metrics/pageviews/top/{project}/all-access/{date_str}'
    response = requests.get(url, headers=HEADERS)
    if response.status_code != 200:
        print(f'Error: {response.status_code} on {date_str}')
        return []
    data = response.json()
    articles = data.get('items', [])[0].get('articles', [])
    return [a for a in articles if a['article'] not in EXCLUDE_TITLES]

def accumulate_views(start_date, end_date):
    view_counts = defaultdict(int)
    delta = (end_date - start_date).days + 1
    for i in range(delta):
        date = start_date + timedelta(days=i)
        date_str = date.strftime('%Y/%m/%d')
        articles = get_topviews(date_str)
        for a in articles:
            view_counts[a['article']] += a['views']
    return sorted(view_counts.items(), key=lambda x: x[1], reverse=True)[:10]

# 日本時間で今日の日付を取得
today = datetime.now(ZoneInfo("Asia/Tokyo")).date()

# 📅 一昨日（取得可能な最新日）
latest_date = today - timedelta(days=2)
latest_str = format_date_with_weekday(latest_date)

# 📅 一昨日
latest_articles = get_topviews(latest_date.strftime('%Y/%m/%d'))
yesterday_ranking = [
    {'title': a['article'], 'views': a['views']}
    for a in latest_articles[:10]
]
print(f"\n📅 {format_period_with_weekday(latest_date)} のトップ記事:")
for i, a in enumerate(yesterday_ranking, 1):
    print(f"{i}. {a['title']} - {a['views']} views")

# 📅 3日前
day_before_yesterday = latest_date - timedelta(days=1)
day_before_yesterday_str = format_date_with_weekday(day_before_yesterday)
articles_day_before_yesterday = get_topviews(day_before_yesterday.strftime('%Y/%m/%d'))
ranking_day_before_yesterday = [
    {'title': a['article'], 'views': a['views']}
    for a in articles_day_before_yesterday[:10]
]
print(f"\n📅 {format_period_with_weekday(day_before_yesterday)} のトップ記事:")
for i, a in enumerate(ranking_day_before_yesterday, 1):
    print(f"{i}. {a['title']} - {a['views']} views")

# 📅 過去7日間（昨日を含む）
start_7 = latest_date - timedelta(days=6)
end_7 = latest_date
views_7 = accumulate_views(start_7, end_7)
ranking_7 = [{'title': t, 'views': v} for t, v in views_7]
period_7 = f"{format_period_with_weekday(start_7).split('から')[0]}から{format_period_with_weekday(end_7).split('から')[1]}"
print(f"\n📅 {period_7} の累計ランキング:")
for i, a in enumerate(ranking_7, 1):
    print(f"{i}. {a['title']} - {a['views']} views")

# 📅 9日前〜15日前（過去7日間の開始日の前日から7日間）
end_8_14 = start_7 - timedelta(days=1)
start_8_14 = end_8_14 - timedelta(days=6)
views_8_14 = accumulate_views(start_8_14, end_8_14)
ranking_8_14 = [{'title': t, 'views': v} for t, v in views_8_14]
period_8_14 = f"{format_period_with_weekday(start_8_14).split('から')[0]}から{format_period_with_weekday(end_8_14).split('から')[1]}"
print(f"\n📅 {period_8_14} の累計ランキング:")
for i, a in enumerate(ranking_8_14, 1):
    print(f"{i}. {a['title']} - {a['views']} views")

# 📅 過去30日間（昨日を含む）
start_30 = latest_date - timedelta(days=29)
end_30 = latest_date
views_30 = accumulate_views(start_30, end_30)
ranking_30 = [{'title': t, 'views': v} for t, v in views_30]
period_30 = f"{format_period_with_weekday(start_30).split('から')[0]}から{format_period_with_weekday(end_30).split('から')[1]}"
print(f"\n📅 {period_30} の累計ランキング:")
for i, a in enumerate(ranking_30, 1):
    print(f"{i}. {a['title']} - {a['views']} views")

# JSON保存用データ構造（曜日付き）
output = {
    format_period_with_weekday(latest_date): {
        'ランキング': yesterday_ranking
    },
    format_period_with_weekday(day_before_yesterday): {
        'ランキング': ranking_day_before_yesterday
    },
    f"{format_period_with_weekday(start_7).split('から')[0]}から{format_period_with_weekday(end_7).split('から')[1]}": {
        'ランキング': ranking_7
    },
    f"{format_period_with_weekday(start_8_14).split('から')[0]}から{format_period_with_weekday(end_8_14).split('から')[1]}": {
        'ランキング': ranking_8_14
    },
    f"{format_period_with_weekday(start_30).split('から')[0]}から{format_period_with_weekday(end_30).split('から')[1]}": {
        'ランキング': ranking_30
    }
}

output['更新時刻'] = timestamp

print(f"\n📅 更新時刻（JST）: {timestamp}")

import os

# スクリプト自身の場所を取得（絶対パス）
script_dir = os.path.dirname(os.path.abspath(__file__))

# 保存先をスクリプトと同じ場所に固定
save_path = os.path.join(script_dir, 'docs', 'ranking.json')

# 保存処理
with open(save_path, 'w', encoding='utf-8') as f:
    json.dump(output, f, ensure_ascii=False, indent=2)

# script.js を docs にコピー
import shutil
source_js = os.path.join(script_dir, 'script.js')
target_js = os.path.join(script_dir, 'docs', 'script.js')
os.makedirs(os.path.dirname(target_js), exist_ok=True)
shutil.copy2(source_js, target_js)
print(f"✅ script.js を docs フォルダに保存しました：{target_js}")

# 保存後に確認
with open(save_path, 'r', encoding='utf-8') as f:
    preview = json.load(f)
    print("\n✅ 保存された更新時刻:", preview.get('更新時刻', '見つかりませんでした'))

# スクリプトと同じ階層にある script.js を削除
script_path_to_delete = os.path.join(script_dir, 'script.js')

if os.path.exists(script_path_to_delete):
    os.remove(script_path_to_delete)
    print(f"🗑️ script.js を削除しました：{script_path_to_delete}")
else:
    print("⚠️ 削除対象の script.js が見つかりませんでした（すでに削除済みか存在しない可能性）")


# 保存後に確認
with open(save_path, 'r', encoding='utf-8') as f:
    preview = json.load(f)
    print("\n✅ 保存された更新時刻:", preview.get('更新時刻', '見つかりませんでした'))