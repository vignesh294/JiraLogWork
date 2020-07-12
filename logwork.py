import sys
from jira import JIRA
from datetime import datetime
import concurrent.futures
import json

config = None

class WorklogRequest:
    issueId = None
    work = None
    comment = None
    date = None

    def __init__(self, issueId, work):
        self.issueId = issueId
        self.work = work

    def __str__(self):
        return 'WorklogRequest (%s, %s, %s, %s)' % (self.issueId, self.work, self.comment, self.date)

def prepareConfig():
    print("=====Reading configs=====")
    global config
    with open('config.json') as config_json:
        config = json.load(config_json)
    pass
    # todo - validate configs

def prepareJira():
    print("=====Preparing jira=====")
    jira_options = {}
    jira_options['server'] = config['server']
    jira_options['verify'] = config['set_verify']
    jira = JIRA(options=jira_options, basic_auth=(config['username'], config['password']))
    return jira

def prepareWorklogRequest(worklog_request_string):
    worklog_request_params = worklog_request_string.split(',')
    if(len(worklog_request_params) != 4):
        print("=====" + worklog_request_string + " does not have all the 4 params in the comma separated format=====")
        print("=====Exiting without logging work for any of the issues=====")
        sys.exit()
    issueId = worklog_request_params[0]
    if issueId is None or len(issueId) == 0:
        print("=====" + worklog_request_string + " does not have valid issueId=====")
        print("=====Exiting without logging work for any of the issues=====")
        sys.exit()
    work = worklog_request_params[1]
    if work is None or len(work) == 0:
        print("=====" + worklog_request_string + " does not have valid work to log=====")
        print("=====Exiting without logging work for any of the issues=====")
        sys.exit()
    worklog_request = WorklogRequest(issueId, work)
    comment = worklog_request_params[2]
    if comment is not None and len(comment) > 0:
        setattr(worklog_request, 'comment', comment)
    date = worklog_request_params[3]
    date = date if len(date) > 0 else None
    if date is not None:
        # if only date is sent, need to append some time 
        if 'T' not in date and config['default_work_start_time'] is not None and len(config['default_work_start_time']) > 0:
            date += 'T' + config['default_work_start_time']
        date = datetime.strptime(date, '%Y-%m-%dT%H:%M:%S') 
        setattr(worklog_request, 'date', date)
    return worklog_request

def prepareWorklogRequests(no_of_worklogs):
    worklog_requests = []
    for i in range(1, no_of_worklogs):
        worklog_request_string = sys.argv[i]
        worklog_requests.append(prepareWorklogRequest(worklog_request_string))
    return worklog_requests

def addWorklog(jira, worklog_request):
    issueId = getattr(worklog_request, 'issueId')
    work = getattr(worklog_request, 'work')
    comment = getattr(worklog_request, 'comment')
    date = getattr(worklog_request, 'date')
    print("=====Processing: " + str(worklog_request) + "=====")
    worklog_response = jira.add_worklog(issue = issueId, timeSpent = work, comment=comment, started = date)
    print("=====Processed: " + str(worklog_request) + "=====")

def addWorklogs(jira, worklog_requests):
    # use the network call time to jira to concurrently process other worklogs
    # using one thread per worklog request
    with concurrent.futures.ThreadPoolExecutor(max_workers=len(worklog_requests)) as executor:
        for worklog_request in worklog_requests:
            executor.submit(addWorklog, jira, worklog_request)

def main():
    prepareConfig()
    jira = prepareJira()
    no_of_worklogs = len(sys.argv) 
    worklog_requests = prepareWorklogRequests(no_of_worklogs)
    addWorklogs(jira, worklog_requests)

main()

