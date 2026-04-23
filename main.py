import json

CHANNELS_CSV_HEADERS = "No.,Channel Name,Channel Type,RX Frequency[MHz],TX Frequency[MHz],Power,Band Width,Scan List,TX Admit,Emergency System,Squelch Level,APRS Report Type,Forbid TX,APRS Receive,Forbid Talkaround,Auto Scan,Lone Work,Emergency Indicator,Emergency ACK,Analog APRS PTT Mode,Digital APRS PTT Mode,TX Contact,RX Group List,Color Code,Time Slot,Encryption,Encryption ID,APRS Report Channel,Direct Dual Mode,Private Confirm,Short Data Confirm,DMR ID,CTC/DCS Decode,CTC/DCS Encode,Scramble,RX Squelch Mode,Signaling Type,PTT ID,VOX Function,PTT ID Display\n"
ZONES_CSV_HEADERS = "No.,Zone Name,Channel Members\n"  # Channel members will be pipe (|) seperated.
CONTACTS_CSV_HEADERS = "No.,Name,ID,Type\n"  # Type will be one of "Group Call" or "Private Call".
DMR_IDS_CSV_HEADERS = "No.,Radio ID,Radio Name\n"
file_path = "codeplug.json"

channels_rows = []
zones_rows = []
contacts_rows = []
dmr_ids_rows = []

with open(file_path, "r") as f:
    codeplug_json = json.load(f)


def load_digital_channel(digital_channel):
    ts1_contacts = digital_channel.get("ts1_contacts", [])
    ts2_contacts = digital_channel.get("ts2_contacts", [])
    channel_names = []
    for ts, contacts in ((1, ts1_contacts), (2, ts2_contacts)):
        for contact in contacts:
            channel_name = digital_channel["name"] + "-" + contact
            channel_names.append(channel_name)
            channels_rows.append(
                [channel_name, "Digital", digital_channel["uplink"], digital_channel["downlink"], "High", "12.5KHz",
                 "None", "Allow TX",
                 "None", 3, "Off", 0, 0, 0, 0, 0, 0, 0, 0, 0, contact, "None", 0, "Slot 1" if ts == 1 else "Slot 2", 0,
                 "None", 1, 0, 0, 0, digital_channel.get("dmr_id", default_dmr_id),
                 digital_channel.get("uplink_cs", "None"),
                 digital_channel.get("downlink_cs", "None"), "None", "None", "Carrier/CTC", "None", "OFF", "0", "0"])
    return channel_names


def load_analog_channel(analog_channel):
    channel_name = analog_channel["name"]
    channels_rows.append(
        [channel_name, "Analog", analog_channel["uplink"], analog_channel["downlink"], "High", "12.5KHz",
         "None", "Allow TX", "None", 3, "Off", 0, 0, 0, 0, 0, 0, 0, 0, 0, "None", "None", 0, "None", 0, "None", 1, 0, 0,
         0, "None", analog_channel.get("uplink_cs", "None"), analog_channel.get("downlink_cs", "None"), "None",
         "Carrier/CTC", "None", "OFF", 0, 0])
    return channel_name


contacts_rows.extend([[contact["name"], contact["id"], "Group Call"] for contact in codeplug_json.get("group_contacts", [])])
contacts_rows.extend([[contact["name"], contact["id"], "Private Call"] for contact in codeplug_json.get("private_contacts", [])])
dmr_ids_rows.extend([[dmr_id["name"], dmr_id["id"]] for dmr_id in codeplug_json["dmr_ids"]])
default_dmr_id = codeplug_json["default_dmr_id"]
zones = codeplug_json["channels"]
for zone in zones:
    name = zone["names"]
    zone_channel_names = []
    for channel in zone["channels"]:
        if channel["type"] == "Digital":
            zone_channel_names.extend(load_digital_channel(channel))
        else:
            assert channel["type"] == "Analog"
            zone_channel_names.extend(load_analog_channel(channel))
    zones_rows.append([name, "|".join(zone_channel_names)])
