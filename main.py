import sys
import json
import pathlib
import argparse


parser = argparse.ArgumentParser()
parser.add_argument("file", help="path to JSON codeplug file")
args = parser.parse_args()


CHANNELS_CSV_HEADERS = "No.,Channel Name,Channel Type,RX Frequency[MHz],TX Frequency[MHz],Power,Band Width,Scan List,TX Admit,Emergency System,Squelch Level,APRS Report Type,Forbid TX,APRS Receive,Forbid Talkaround,Auto Scan,Lone Work,Emergency Indicator,Emergency ACK,Analog APRS PTT Mode,Digital APRS PTT Mode,TX Contact,RX Group List,Color Code,Time Slot,Encryption,Encryption ID,APRS Report Channel,Direct Dual Mode,Private Confirm,Short Data Confirm,DMR ID,CTC/DCS Decode,CTC/DCS Encode,Scramble,RX Squelch Mode,Signaling Type,PTT ID,VOX Function,PTT ID Display"
ZONES_CSV_HEADERS = "No.,Zone Name,Channel Members"  # Channel members will be pipe (|) seperated.
CONTACTS_CSV_HEADERS = "No.,Name,ID,Type"  # Type will be one of "Group Call" or "Private Call".
DMR_IDS_CSV_HEADERS = "No.,Radio ID,Radio Name"

channels_rows = []
zones_rows = []
contacts_rows = []
dmr_ids_rows = []


def info(msg):
    print(f"[INFO] {msg}")


def warn(msg):
    print(f"[WARN] {msg}")


def err_and_exit(msg):
    print(f"[ERR] {msg}", file=sys.stderr)
    sys.exit(-1)


with open(args.file, "r") as f:
    codeplug_json = json.load(f)
info(f"Loaded JSON from {args.file}...")


def load_channel(channel):
    if channel["type"] == "digital":
        ts1_contacts = channel.get("ts1_contacts", [])
        ts2_contacts = channel.get("ts2_contacts", [])
        channel_names = []
        for ts, contacts in ((1, ts1_contacts), (2, ts2_contacts)):
            for contact in contacts:
                if not contact in contacts_set:
                    err_and_exit(f"Contact {contact} not found in contacts.")
                channel_name = channel["name"] + " " + contact
                channel_names.append(channel_name)
                channels_rows.append(
                    [channel_name, "Digital", channel["uplink"], channel["downlink"], "High", "12.5KHz",
                     None, "Allow TX",
                     None, 3, "Off", 0, 0, 0, 0, 0, 0, 0, 0, 0, contact, None, 0, "Slot 1" if ts == 1 else "Slot 2", 0,
                     None, 1, 0, 0, 0, channel.get("dmr_id", default_dmr_id), None, None, None, None, "Carrier/CTC", None, "OFF", "0", "0"])
        return channel_names
    else:
        assert channel["type"] == "analog"
        channel_name = channel["name"]
        channels_rows.append(
            [channel_name, "Analog", channel["uplink"], channel["downlink"], "High", "12.5KHz",
             None, "Allow TX", None, 3, "Off", 0, 0, 0, 0, 0, 0, 0, 0, 0, None, None, 0, None, 0, None, 1, 0, 0,
             0, None, channel.get("uplink_cs"), channel.get("downlink_cs"), None,
             "Carrier/CTC", None, "OFF", 0, 0])
        return [channel_name]


contacts_rows.extend([[contact["name"], contact["id"], "Group Call"] for contact in codeplug_json.get("group_contacts", [])])
contacts_rows.extend([[contact["name"], contact["id"], "Private Call"] for contact in codeplug_json.get("private_contacts", [])])
dmr_ids_rows.extend([[dmr_id["id"], dmr_id["name"]] for dmr_id in codeplug_json["dmr_ids"]])
default_dmr_id = codeplug_json["default_dmr_id"]
zones = codeplug_json["zones"]


contacts_set = set(contact_row[0] for contact_row in contacts_rows)
dmr_ids_set = set(dmr_ids_row[1] for dmr_ids_row in dmr_ids_rows)


if not default_dmr_id in dmr_ids_set:
    err_and_exit(f"Default DMR ID '{default_dmr_id}' not found in DMR IDs.")


for zone in zones:
    name = zone["name"]
    zone_channel_names = []
    for channel in zone["channels"]:
        zone_channel_names.extend(load_channel(channel))
    zones_rows.append([name, "|".join(zone_channel_names)])


def write_csv(headers, rows, path):
    if path.exists():
        if input(f"[CONF] Overwrite existing file '{path}'? [Y/n] ").lower().startswith("n"):
            warn(f"Skipped writing {path}")
            return
    with open(path, "w") as f:
        f.write("\n".join(
            [headers, *[",".join([str(n), *[str(item) for item in row]]) for n, row in enumerate(rows, start=1)]]))
    info(f"Wrote {path}...")


write_csv(CHANNELS_CSV_HEADERS, channels_rows, pathlib.Path("channels.csv"))
write_csv(ZONES_CSV_HEADERS, zones_rows, pathlib.Path("zones.csv"))
write_csv(CONTACTS_CSV_HEADERS, contacts_rows, pathlib.Path("contacts.csv"))
write_csv(DMR_IDS_CSV_HEADERS, dmr_ids_rows, pathlib.Path("dmr_ids.csv"))
