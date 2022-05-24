from flask import Flask, request, json
from datetime import datetime
import dateutil.parser

app = Flask(__name__)


def handle_repo_event(info, req_timestamp):
    mess = 0
    data = json.loads(info)
    action_type = data['action']
    if action_type == 'deleted':
        repo_data = data['repository']
        # created_timestamp = dateutil.parser.parse(repo_data['created_at'])
        created_timestamp = dateutil.parser.parse(repo_data['created_at'])
        end_timestamp = dateutil.parser.parse(req_timestamp)
        if datetime.date(end_timestamp) == datetime.date(created_timestamp):
            delta = end_timestamp - created_timestamp
            hours = delta.seconds // 3600
            minutes = (delta.seconds // 60) % 60
            if hours == 0 and minutes < 10:
                print('Suspicious behavior: repository was deleted after existing less than 10 minutes.')


def handle_push_event(info):
    data = json.loads(info)
    head_commit = data['head_commit']
    push_timestamp = head_commit['timestamp']
    push_time = dateutil.parser.parse(push_timestamp)
    quit_start_time = dateutil.parser.parse('14:00:00')
    quit_end_time = dateutil.parser.parse('18:00:00')
    if quit_start_time.time() <= push_time.time() <= quit_end_time.time():
        print("Suspicious behavior: Someone pushed code.")


def handle_team_event(info):
    data = json.loads(info)
    if data['action'] == 'created':
        team = data['team']
        team_name = team['name']
        if team_name.find('hacker') != -1:
            print("Suspicious behavior: Team with prefix 'hacker' created.")


@app.route('/github', methods=['POST'])
def github_webhook():
    if request.headers['Content-Type'] == 'application/json':
        info = json.dumps(request.json)
        # data = json.loads(info)
        event = request.headers['X-Github-Event']
        if event == 'repository':
            timestamp = datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')
            handle_repo_event(info, timestamp)
        elif event == 'push':
            handle_push_event(info)
        elif event == 'team':
            handle_team_event(info)

    return info
    # print('issue is opened')


if __name__ == '__main__':
    app.run(debug=True)
