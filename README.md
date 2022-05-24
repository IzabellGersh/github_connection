# github_connection
Implemented application that will detect and notify suspicious behavior in an integrated GitHub organization using webhooks.

Working with webhooks locally - I used the ngrok tool (https://ngrok.com/).
1. Create github organization.
2. Register webhook used by ngrok:
    (1) Payload URL: '/github' added to end path (e.g: https://9c96-2a0d-6fc0-e94-6110-8882-ec2-2d-69fd.eu.ngrok.io/github)
    (2) Content type: change to application/json
    (3) Select relevant triggers for webhook (teams, pushes, repositories)
3. run the main.py code.
4. test manually by following the assigment you will get the relevant output printed.
