# DM32UV Codeplug Compiler

Baofeng's CPS software UX is pretty bad, so I made this tool to compile a simple JSON format into CSV files that can easily be imported into the software.

https://github.com/user-attachments/assets/d830122c-d048-4992-8b2a-572fb2b098af

## Usage:

### As a Python script:
Assuming your codeplug is contained in `codeplug.json`:
```shell
python3 main.py codeplug.json
```

### As a compiled executable:
Again, assuming your codeplug is contained in `codeplug.json`:
```shell
dm32uv codeplug.json
```

### However you choose to run it:
It will output 4 files, `channels.csv`, `zones.csv`, `contacts.csv` and `dmr_ids.csv`. If they already exist, it will prompt you to overwrite them individually.
Once it's written the files, import them into their respective parts of the Baofeng CPS software, and upload to your radio.

## Building:

### With pyinstaller:
If you haven't already, run `pip3 install pyinstaller`:
```shell
pyinstaller dm32uv.spec
```

## Codeplug Format:
> ### Why JSON?
> Cause I'm a dumbass. Yes. There were way better formats, for example YAML.

### The format is pretty self-explanatory. Check out `example_codeplug.json` for a reference.
