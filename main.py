import json
import sys


CHANNELS_CSV_HEADERS = "No.,Channel Name,Channel Type,RX Frequency[MHz],TX Frequency[MHz],Power,Band Width,Scan List,TX Admit,Emergency System,Squelch Level,APRS Report Type,Forbid TX,APRS Receive,Forbid Talkaround,Auto Scan,Lone Work,Emergency Indicator,Emergency ACK,Analog APRS PTT Mode,Digital APRS PTT Mode,TX Contact,RX Group List,Color Code,Time Slot,Encryption,Encryption ID,APRS Report Channel,Direct Dual Mode,Private Confirm,Short Data Confirm,DMR ID,CTC/DCS Decode,CTC/DCS Encode,Scramble,RX Squelch Mode,Signaling Type,PTT ID,VOX Function,PTT ID Display\n"
ZONES_CSV_HEADERS = "No.,Zone Name,Channel Members\n"  # Channel members will be pipe (|) seperated.
CONTACTS_CSV_HEADERS = "No.,Name,ID,Type\n"  # Type will be one of "Group Call" or "Private Call".
file_path = "codeplug.json"

channels_csv = CHANNELS_CSV_HEADERS
zones_csv = ZONES_CSV_HEADERS
contacts_csv = CONTACTS_CSV_HEADERS


with open(file_path, "r") as f:
    codeplug_json = json.load(f)

def terminate_with_error(error):
    print(f"""Error in JSON codeplug at {file_path}:\n\n\t{error}\n\nThe compiler will now exit and no output files will be written.""", file=sys.stderr)
    exit(1)

def index_group_contacts(group_contacts):
    for group_contact in group_contacts:
        

group_contacts = codeplug_json.get("group_contacts")
if not group_contacts:
    terminate_with_error("Root object has no property 'group_contacts'.")
group_contacts = index_group_contacts(group_contacts)
