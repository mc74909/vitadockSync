import re
import requests
import argparse
import sys

parser = argparse.ArgumentParser(description='Load VitaDock exports into Runalyze.com')
parser.add_argument('-k', '--key', required=True, help='The personal API for Runalyze.com')
parser.add_argument('-t', '--type', required=True, help='The type of data set to load.', choices=['bloodPressure', 'bodyComposition'])
parser.add_argument('-f', '--file', type=argparse.FileType('r'), default=sys.stdin, help='The input file to read from. This is an export file from VitaDock online. Default is to read from stdin.')
parser.add_argument('-v', '--version', action='version', version='loadVitaDock v1.0')

RUNALYZE_API_ENDPOINT = 'https://runalyze.com/api/v1/'

args = parser.parse_args()

headers = { "token": args.key } 

def loadData(content):
    r = requests.post(RUNALYZE_API_ENDPOINT + 'metrics/' + args.type, json=content, headers=headers)
    print(r.content)

if args.type == 'bloodPressure':
    PATTERN = '"(.*)/(.*)/(.*) - (.*)";"(.*) mmHg";"(.*) mmHg";"(.*) bpm";"(.*)";"(.*)";"  "'

    for reading in args.file:
        if match := re.search(PATTERN, reading):
            jsoncontent = { "date_time": match.group(3) + "-" + match.group(1) + "-" + match.group(2) + "T" + match.group(4) + ":00Z", "systolic": int(match.group(5)), "diastolic": int(match.group(6)), "heart_rate": int(match.group(7)) }
            loadData(jsoncontent)
elif args.type == 'bodyComposition':
    PATTERN = '(.*)/(.*)/(.*) - (.*);(.*);(.*);(.*);(.*);(.*);(.*);.*;.*;.*'
    for reading in args.file:
        if match := re.search(PATTERN, reading):
            jsoncontent = { "date_time": match.group(3) + "-" + match.group(1) + "-" + match.group(2) + "T" + match.group(4) + ":00Z", "weight": float(match.group(5)), "fat_percentage": float(match.group(7)), "water_percentage": float(match.group(8)), "muscle_percentage": float(match.group(9)), "bone_percentage": float(match.group(6)) }
            loadData(jsoncontent)
