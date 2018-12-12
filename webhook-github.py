import os
import sys
import hmac
import logging

from flask import Flask, jsonify
from git import Repo

app = Flask(__name__)

secret = os.getenv('GITHUB_WEBHOOK_SECRET')
repo_path = os.getenv('GITHUB_REPO_LOCAL_PATH')

logging.basicConfig(stream=sys.stderr, level=logging.INFO)

if not secret:
    logging.error('Environment variable GITHUB_WEBHOOK_SECRET is empty')
    exit(1)

if not repo_path:
    logging.error('Environment variable GITHUB_REPO_LOCAL_PATH is empty')
    exit(1)

logging.info('secret key is %s', secret)
logging.info('repo local path %s', repo_path)

@app.route('/webhook-github', methods=['POST'])
def handle_github_hook():
    """Entry point for github webhook."""

    global secret, repo_path

    signature = request.headers.get('X-Hub-Signature')
    _, signature = signature.split('=')

    hashhex = hmac.new(secret, request.data, digestmod='sha1').hexdigest()

    if hmac.compare_digest(hashhex, signature):
        repo = Repo(repo_path)
        repo.remotes.origin.pull('--rebase')

        commit = request.json['after'][0:6]
        logging.info('Repository updated with commit {}'.format(commit))
        return jsonify({'code': 0, 'msg': 'git pull success'}, 200)

    return jsonify({'code': 1, 'msg': 'git repo doesn\'t change'}, 200)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)
