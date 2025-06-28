#!/usr/bin/env python3
# threat_analyzer.py — analyze replies to the latest tweet of a given user via Twitter API v2

import os
import sys
import json
import argparse
import logging
import requests

# Map numeric severity to human-readable color
COLOR_LEVELS = {
    1: 'Blue',    # baseline, no threat keywords
    2: 'Green',
    3: 'Yellow',
    4: 'Orange',
    5: 'Red',
}

# Default threat keywords per severity (from least to worst)
DEFAULT_KEYWORDS = {
    5: ['kill', 'murder', 'attack', 'destroy', 'bomb', 'shoot', 'slaughter', 'massacre'],
    4: ['threat', 'harm', 'violenc', 'injur', 'hostil'],
    3: ['warn', 'caution', 'alert', 'danger'],
    2: ['notice', 'attention', 'careful'],
}

API_BASE = 'https://api.twitter.com/2'


def get_bearer_token():
    token = os.getenv('TWITTER_BEARER_TOKEN')
    if not token:
        sys.exit('Error: Set environment variable TWITTER_BEARER_TOKEN with your Twitter API v2 Bearer Token')
    return token


def request_json(url, headers, params=None):
    resp = requests.get(url, headers=headers, params=params)
    if resp.status_code != 200:
        logging.error(f'API request failed ({resp.status_code}): {resp.text}')
        sys.exit(1)
    return resp.json()


def get_user_id(username, headers):
    url = f'{API_BASE}/users/by/username/{username}'
    data = request_json(url, headers)
    return data['data']['id']


def get_latest_tweet(user_id, headers):
    url = f'{API_BASE}/users/{user_id}/tweets'
    params = {
        'max_results': 5,  # fetch a few in case the first is a retweet
        'exclude': 'retweets,replies',
        'tweet.fields': 'id,text,conversation_id'
    }
    data = request_json(url, headers, params)
    for tweet in data.get('data', []):
        # take the first non-reply
        if tweet.get('conversation_id'):
            return tweet['id'], tweet['conversation_id'], tweet['text']
    logging.error('No original tweets found for this user')
    sys.exit(1)


def get_replies(conversation_id, headers, limit):
    url = f'{API_BASE}/tweets/search/recent'
    params = {
        'query': f'conversation_id:{conversation_id}',
        'max_results': min(limit, 100),
        'expansions': 'author_id',
        'tweet.fields': 'id,text,author_id',
        'user.fields': 'username'
    }
    data = request_json(url, headers, params)
    replies = data.get('data', [])
    users = {u['id']: u['username'] for u in data.get('includes', {}).get('users', [])}
    results = []
    for rep in replies[:limit]:
        uid = rep['author_id']
        results.append({
            'reply_id': rep['id'],
            'user': users.get(uid, uid),
            'content': rep['text'],
        })
    return results


def classify_text(text, keywords):
    tl = text.lower()
    for lvl in sorted(keywords.keys(), reverse=True):
        for kw in keywords[lvl]:
            if kw in tl:
                return lvl
    return 1


def analyze(username, limit, keywords):
    token = get_bearer_token()
    headers = {'Authorization': f'Bearer {token}'}

    user_id = get_user_id(username, headers)
    tweet_id, conv_id, tweet_text = get_latest_tweet(user_id, headers)
    logging.info(f'Analyzing replies to tweet {tweet_id!r}: {tweet_text!r}')

    replies = get_replies(conv_id, headers, limit)
    for r in replies:
        sev = classify_text(r['content'], keywords)
        r['severity'] = sev
        r['color'] = COLOR_LEVELS[sev]
        r['url'] = f'https://x.com/{r["user"]}/status/{r["reply_id"]}'

    return sorted(replies, key=lambda x: x['severity'], reverse=True)


def main():
    parser = argparse.ArgumentParser(description='Analyze X replies by threat level via Twitter API v2')
    parser.add_argument('-u', '--user', default='NSAGov', help='X username (default: NSAGov)')
    parser.add_argument('-n', '--limit', type=int, default=100, help='Max replies (default:100, max per request:100)')
    parser.add_argument('-k', '--keywords-file', help='JSON file mapping severity to keywords')
    parser.add_argument('-o', '--output', help='Write full JSON results to file')
    parser.add_argument('--test', action='store_true', help='Run classification smoke tests and exit')
    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')

    if args.test:
        assert classify_text('I will kill you', DEFAULT_KEYWORDS) == 5
        assert classify_text('Be careful out there', DEFAULT_KEYWORDS) == 2
        assert classify_text('Just saying hi', DEFAULT_KEYWORDS) == 1
        print('All tests passed.')
        sys.exit(0)

    keywords = DEFAULT_KEYWORDS
    if args.keywords_file:
        try:
            with open(args.keywords_file) as f:
                data = json.load(f)
            keywords = {int(k): v for k, v in data.items()}
        except Exception as e:
            logging.warning(f'Failed to load keywords file: {e}; using defaults')

    results = analyze(args.user, args.limit, keywords)

    for r in results:
        print(f"[{r['color']}] @{r['user']}: {r['content'][:80]!r}... ({r['url']})")

    if args.output:
        with open(args.output, 'w') as f:
            json.dump(results, f, indent=2)
        logging.info(f'Wrote results to {args.output}')

if __name__ == '__main__':
    main()