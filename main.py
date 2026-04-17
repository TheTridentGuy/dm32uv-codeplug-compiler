import json


CHANNELS_CSV_HEADERS = "No.,Channel Name,Channel Type,RX Frequency[MHz],TX Frequency[MHz],Power,Band Width,Scan List,TX Admit,Emergency System,Squelch Level,APRS Report Type,Forbid TX,APRS Receive,Forbid Talkaround,Auto Scan,Lone Work,Emergency Indicator,Emergency ACK,Analog APRS PTT Mode,Digital APRS PTT Mode,TX Contact,RX Group List,Color Code,Time Slot,Encryption,Encryption ID,APRS Report Channel,Direct Dual Mode,Private Confirm,Short Data Confirm,DMR ID,CTC/DCS Decode,CTC/DCS Encode,Scramble,RX Squelch Mode,Signaling Type,PTT ID,VOX Function,PTT ID Display\n"
ZONES_CSV_HEADERS = "No.,Zone Name,Channel Members\n"  # Channel members will be pipe (|) seperated.
CONTACTS_CSV_HEADERS = "No.,Name,ID,Type\n"  # Type will be one of "Group Call" or "Private Call".
file_path = "codeplug.json"

channels_rows = []
zones_rows = []
contacts_rows = []


with open(file_path, "r") as f:
    codeplug_json = json.load(f)


def index_contacts(contacts):
    return {contact["name"]: contact["id"] for contact in contacts}


def index_dmr_ids(dmr_ids):
    return {dmr_id["name"]: dmr_id["id"] for dmr_id in dmr_ids}


def digital_channel_row():
    pass


group_contacts_index = index_contacts(codeplug_json["group_contacts"])
private_contacts_index = index_contacts(codeplug_json["private_contacts"])
dmr_ids_index = index_dmr_ids(codeplug_json["dmr_ids"])
default_dmr_id = codeplug_json["default_dmr_id"]
zones = codeplug_json["channels"]
for zone in zones:
    name = zone["names"]
    for channel in zone["channels"]:
        pass
