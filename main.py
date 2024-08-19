import parse


from key import GOOGLE_API_KEY

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from matplotlib import pyplot as plt

DB_ID = "1yxxx1JTgrFvbgtbzHDziB8qSkgP4eydTFPXYF6YdyHU"
time_pattern = parse.compile("{:d}h {:d}m {:f}s")


def parse_time_result(res):
    res = time_pattern.search(res)
    total_s = res[0] * 3600 + res[1] *60 + res[2]
    return total_s / 60 #minutes

SONIC_NCW_NAMES = ["Nick","Flub","Loke","Liam","Focus","DSS","Ghast","Sharu","Fury","Wike","Tony","BladeViper","Mati","Dax"]

SONIC_NCW_LOADTIMES = []
def main():
    try:
        service = build('sheets', 'v4', developerKey=GOOGLE_API_KEY)
        sheet = service.spreadsheets()
        ranges = 'Sonic_NCW!D70:AD72'
        result = sheet.values().get(spreadsheetId=DB_ID,range=ranges,majorDimension='COLUMNS').execute()
        values = result.get('values', [])
        for col in values:
            if len(col) > 0 and col[-1] == "":
               col.pop(-1)
            elif len(col) == 0:
                continue
            total_loads_s = parse_time_result(col[-2]) - parse_time_result(col[-1])
            SONIC_NCW_LOADTIMES.append(total_loads_s)
    except HttpError as e:
        print(e)
    for name, time_mins in zip(SONIC_NCW_NAMES, SONIC_NCW_LOADTIMES):
        print(f"{name}: {time_mins} minutes")
    plt.hist(SONIC_NCW_LOADTIMES)
    plt.show()

if __name__ == '__main__':
    main()
