import sys
import argparse
import datetime

# Constants
version = "0.1"
band_dict = {"1.9": "160m", "3.5": "80m", "5": "60m", "7": "40m", "10":"30m", 
             "14": "20m", "18": "17m", "21": "15m", "24": "12m", "28": "10m", 
             "50": "6m", "144": "2m", "430": "70cm", "1200": "23cm"}

# Args
parser = argparse.ArgumentParser()
parser.add_argument("--callsign", help="OP CALLSIGN")
parser.add_argument("--ref", help="Park reference e.g. JP-0005")
parser.add_argument("--state", help="State code / prefecture e.g. Shizuoka")
args = parser.parse_args()

my_call = args.callsign
ref = args.ref
state = args.state

""" Render tag and value
"""
def tag(tagname, value=None):
    if value:
        return f"<{tagname}:{len(value)}>{value}"
    return f"<{tagname}>"

# Headers
print(tag("PROGRAMID", "github.com:qpSHiNqp/adif-tools"))
print(tag("PROGRAMVERSION", version))
print(tag("CREATED_TIMESTAMP", datetime.datetime.now().strftime("%Y%m%d%H%M")))
print(tag("EOH"))

# Body
for line in sys.stdin:
    if line[0].isdigit():
        pass
    else:
        # assume as a header line
        continue

    date        = line[0:11].strip()
    time        = line[11:17].strip()
    freq        = line[17:23].strip()
    mode        = line[23:29].strip()
    callsign    = line[29:43].strip()
    sent        = line[43:47].strip()
    sent_no     = line[47:55].strip()
    rcvd        = line[55:59].strip()
    rcvd_no     = line[59:67].strip()
    mlt         = line[67:74].strip()
    pts         = line[74:].strip()

    dt = f"{date} {time}"
    dt = datetime.datetime.strptime(dt, "%Y-%m-%d %H:%M")
    dt = dt.astimezone(datetime.timezone.utc).strftime("%Y%m%d%H%M")

    band = band_dict[freq]

    data = [
            tag("STATION_CALLSIGN", my_call),
            tag("CALL", callsign),
            tag("QSO_DATE", dt[:-4]),
            tag("TIME_ON", dt[-4:]),
            tag("BAND", band),
            tag("MODE", mode),
            tag("MY_SIG", "POTA"),
            tag("MY_SIG_INFO", ref),
            tag("RST_SENT", sent),
            tag("RST_RCVD", rcvd)
            ]

    if state:
        data.append(tag("STATE", state))

    data.append(tag("EOR"))

    print(" ".join(data))
