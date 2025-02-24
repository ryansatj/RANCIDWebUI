# RANCIDWebUI
## SET UP
1. Make sure youre rancid is working properly with CVS
2. Use group on your routers, edit your routers group in /etc/rancid/rancid.conf in this case the name of routers group is LIST_OF_GROUPS="newRouters"
3. or if you already used another group name, you can replace all "newRouters" in rancid_http_request.py with your group name
4. rancid_http_request.py works on /var/lib/rancid/[groupname]/configs, /var/lib/rancid/logs you can freely change this on the http server code
5. Run the http server using "python3 rancid_http_request.py"
6. Web UI is using React Vite with Tailwind CSS
7. Done

## API Endpoints Overview
| Endpoint                | Method | Description                         |
|-------------------------|--------|-------------------------------------|
| `/getconfigs`          | GET    | Fetch all router configurations   |
| `/rlog/{logname}`      | GET    | Get details of a specific log     |
| `/diff/{router_name}`  | POST   | Show `cvs diff` output, r1 and r2 is the request body, r1 specifies first revision parameter and r2 specifies second revision parameter            |
| `/getrouter`           | GET    | Get all routers name              |
| `/get/{router_name}`   | GET    | Get specific router configurations|
| `/checklogs`           | GET    | Get all rancid-run logs           |
| `/log/{logname}`       | GET    | Get details of a specific log     |


License & Copyright
© 2025 ryansatj. All rights reserved.  
 
