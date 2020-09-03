import subprocess
import json
import time
import os
from argparse import ArgumentParser


playerId = ''
clientRef = ''
gamePlayId = ''
trackingId = ''
timeoffset = 0
reportdata=''

parser = ArgumentParser()
parser.add_argument("-p", "--playerID", dest="playerId",
                    help="playerId", required=True)
parser.add_argument("-g", "--game", dest="game",
                    help="gameId", required=True)
parser.add_argument("-d", "--date", dest="date",
                    help="date in format year-month-day", required=True)
parser.add_argument("-t", "--time", dest="time",
                    help="time in 24hr format hr:min:sec", required=True)
parser.add_argument("-i", "--gamePlayId", dest="gamePlayId",
                    help="gamePlayId", required=False)
parser.add_argument("-s", "--daylight-saving", dest="timeoffset",
                    help="daylight saving", required=False)
parser.add_argument("-c", "--clusterID", dest="clusterID",
                    help="clusterID", required=True)

args = parser.parse_args()

#Cluster selection
clusterID=args.clusterID

if 'jp' in clusterID:
        reportdata='gs://roxor-japan-prod-rgp-event-report-data/'

if 'as' in clusterID:
        reportdata='gs://roxor-asia-prod-rgp-event-report-data/'

if 'eu' in clusterID:
		reportdata='gs://gamesys-eu-live-rgp-event-report-data/'
#endof Cluster selection

playerId = args.playerId

if 'play-' in args.game:
    game = args.game + "*"
else:
    game = "*" + args.game + "*"

date = args.date
target = args.time.split(":")
target[0] = int(target[0])
target[1] = int(target[1])
target[2] = int(target[2])

if args.gamePlayId:
    gamePlayId = args.gamePlayId

if args.timeoffset:
    timeoffset = int(args.timeoffset)


trackingIds = []

transaction = []

output = subprocess.check_output(['gsutil', 'ls', reportdata + date + '/' + game])


fileList = output.split(b'\n')

targetSeconds = int(((target[0] - timeoffset) * 60) + target[1])


times = []


for i in range(0, len(fileList) - 1):
    name = fileList[i].split(b'.')


    if len(name) == 5:
        index = 1
    elif len(name) == 6 or len(name) == 8 or len(name) == 10:
        index = 2

    else:
        index = 1

    info = {}

    info['time'] = name[index].split(b'_')
    info['file'] = i

    times.append(info)

    #print(info['time'])

targetFiles = []

for i in range(0, len(times) - 2):
    currentSeconds = (int(times[i]['time'][1]) * 60) + int(times[i]['time'][2])
    nextSeconds = (int(times[i + 1]['time'][1]) * 60) + int(times[i + 1]['time'][2])

    if targetSeconds > currentSeconds and targetSeconds <= nextSeconds and nextSeconds - currentSeconds < 120:
        targetFiles.append(times[i + 1]['file'])

logs = []


def getFile(file):
    filename = fileList[file].split(b'/')

    print(filename[4])

    if os.path.exists(filename[4].decode('UTF-8')):
        print('exists')
    else:
        subprocess.run(['gsutil', 'cp', fileList[file], '.'])


    with open(filename[4].rstrip()) as fin:
        for line in fin:
            log = json.loads(line)
            log['filename'] = filename[4].decode('UTF-8')
            logs.append(log)


for file in targetFiles:
    #getFile(file - 1)
    getFile(file)
    getFile(file + 1)
    #getFile(file + 2)
    #getFile(file + 3)
    #getFile(file + 4)
    #getFile(file + 5)




logs = sorted(logs, key=lambda k: k['header'].get('timestamp', 0))


startIndex = 0
playerSessionId = ''


results= []


for i in range(0, len(logs) - 1):
    log = logs[i]


    if gamePlayId != '' and gamePlayId in json.dumps(logs[i]):
        print('found game play id')
        trackingId = log['header']['trackingId']
        #print(json.dumps(logs[i]))
        break


    if clientRef == '' and gamePlayId == '':
        if 'playerId' in log['metadata'] and log['metadata']['playerId'] == playerId:
            timestamp = log['header']['timestamp']

            logtime = time.strftime('%H:%M:%S', time.gmtime(timestamp / 1000))

            logtime = logtime.split(':')


            results.append(log)
            #print(logtime)



            if int(logtime[0]) == int(target[0]) - 1 and int(logtime[1]) == int(target[1]) and int(logtime[2]) == int(
                    target[2]):
                trackingId = log['header']['trackingId']
                #print(log['filename'])
                #break

    if clientRef != '' and clientRef in json.dumps(logs[i]):
        #print("found")
        #print(json.dumps(log))

        if log['header']['eventType'] == 'IGSRequest':
            gamePlayId = log['data']['body']['clientGameplayRef']
            playerSessionId = log['metadata']['playerSessionId']
            trackingId = log['header']['trackingId']
            playerId = log['metadata']['playerId']
            #print(log['header']['timestamp'])
            break

        if log['header']['eventType'] == 'savePlayRequest':
            trackingId = log['header']['trackingId']
            playerId = log['metadata']['playerId']
            break

for i in range(0, len(logs) - 1):
    log = logs[i]

    if 'trackingId' in log['header'] and log['header']['trackingId'] == trackingId:
        startIndex = i
        break

finish = False
current = {}

current['event'] = 'test'


#print(startIndex)

#startIndex = 0


for i in range(startIndex, len(logs) - 1):
    log = logs[i]

    if 'playerId' in log['metadata'] and log['metadata']['playerId'] == playerId:
        results.append(log)

        #print(json.dumps(log))
        #print(log['header']['trackingId'])
        if log['header']['eventType'] == 'gameEvent':



            if 'event' in log['data']['body']:
                current['event'] = log['data']['body']['event']
                #print(json.dumps(log))
                #results.append(log)


            if 'responseText' in log['data']['body']:
                current['response'] = log['data']['body']['responseText']
                transaction.append(current)
                current = {}

            if 'responseText' in log['data']['body'] and finish == True:
                break

        if "FINISH_GAME_PLAY" in json.dumps(logs[i]):
            #print("finish")
            finish = True


result = {}
result['result'] = transaction
result['status'] = 'success'

print(json.dumps(result))


#print(json.dumps(results))
