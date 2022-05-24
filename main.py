from typing import Tuple

from flask import Flask, request, json
from datetime import datetime
import dateutil.parser

app = Flask(__name__)


def handle_repo_event(info: json) -> bool:
    req_timestamp = datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')
    data = json.loads(info)
    if isinstance(data, dict) and data.get('action') == 'deleted':
        repo_data = data.get('repository')
        if isinstance(repo_data, dict):
            created_timestamp = dateutil.parser.parse(repo_data.get('created_at'))
            end_timestamp = dateutil.parser.parse(req_timestamp)
            if datetime.date(end_timestamp) == datetime.date(created_timestamp):
                delta = end_timestamp - created_timestamp
                hours = delta.seconds // 3600
                minutes = (delta.seconds // 60) % 60
                if hours == 0 and minutes < 10:
                    return True
    return False


def handle_push_event(info: json) -> bool:
    data = json.loads(info)
    if isinstance(data, dict):
        head_commit = data.get('head_commit')
        if isinstance(head_commit, dict):
            push_timestamp = head_commit.get('timestamp')
            push_time = dateutil.parser.parse(push_timestamp)
            quit_start_time = dateutil.parser.parse('14:00:00')
            quit_end_time = dateutil.parser.parse('16:00:00')
            if quit_start_time.time() <= push_time.time() <= quit_end_time.time():
                return True
    return False


def handle_team_event(info: json) -> bool:
    data = json.loads(info)
    if isinstance(data, dict) and data.get('action') == 'created':
        team = data.get('team')
        if isinstance(team, dict):
            team_name = team.get('name')
            if isinstance(team_name, str) and team_name.find('hacker') != -1:
                return True
    return False


events_dict = {
    "repository": handle_repo_event,
    "push": handle_push_event,
    "team": handle_team_event
}


@app.route('/github', methods=['POST'])
def github_webhook():
    if request.headers['Content-Type'] == 'application/json':
        info = json.dumps(request.json)
        event = request.headers['X-Github-Event']
        try:
            handler = events_dict.get(event)
            if handler is None:
                print(f'please implement handler for the {event}')
                return
            is_suspicious = handler(info)
            if is_suspicious:
                print(f'Suspicious behavior caused by: {event} event')
        except Exception:
            print(f'event:{event} handler crashed')


if __name__ == '__main__':
    app.run()
