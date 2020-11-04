# BE-on-JE-Realms

should let BE players connect to JE realms. this will get the IP and port for the realm, and generate a config so Geyser can do the rest of the work

#### To use:

1. run `setup.sh` as root (on Linux), or `setup.bat` on Windows.

2. run `generate_yaml.py` and input the info it needs. Anything you input will only ever be sent to Mojang and stored in the config file.

3. copy `config.yml` to wherever Geyser reads it from. Overwrite the file Geyser made.

4. run Geyser and join with your BE device.

If it breaks then you can ask for help through Discord.
