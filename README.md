# SMA Energy Meter simulator

This home assistant add-on can emulate the existence of one or more SMA Energy Meters on the local network. This makes it possible to use the data from other meter types and integrate them in your SMA inverter. 

The add-on will subscribe to the following mqtt topic: `sma/emeter/<METER_ID>/state`. When receiving the first message the emulator wil start the emulation of the energy meter with the provided <METER_ID>. The emulator wil send a udp packet every 1000ms. The content of the packet wil stay the same until it gets updated by the next mqtt message.

```json
{
    "powerIn": 1200, // power consumption in W
    "powerOut": 800, // power production in W
    "energyIn": 500000, // consumed energy in Wh
    "energyOut": 200000, // produced energy in Wh
    "destinationAddresses": [ // optional ip-addresses to send the packets to. Default behaviour uses multicast.
    ]
}
```

## Installation

- Add the repository to the add-on repository:

[![Open your Home Assistant instance and show the add add-on repository dialog with a specific repository URL pre-filled.](https://my.home-assistant.io/badges/supervisor_add_addon_repository.svg)](https://my.home-assistant.io/redirect/supervisor_add_addon_repository/?repository_url=https%3A%2F%2Fgithub.com%2Froeland54%2FSMA-Energy-Meter-emulator)

- Install the addon from the add-on store.

# Configuration
If you have a mqtt broker configured in home assistant you do not need to configure anything. Otherwise fill in the mqtt configuration in the configuration tab.

### [SMA Energy Meter simulator](./example)

![Supports aarch64 Architecture][aarch64-shield]
![Supports amd64 Architecture][amd64-shield]
![Supports armhf Architecture][armhf-shield]
![Supports armv7 Architecture][armv7-shield]
![Supports i386 Architecture][i386-shield]

<!--

Notes to developers after forking or using the github template feature:
- While developing comment out the 'image' key from 'example/config.yaml' to make the supervisor build the addon
  - Remember to put this back when pushing up your changes.
- When you merge to the 'main' branch of your repository a new build will be triggered.
  - Make sure you adjust the 'version' key in 'example/config.yaml' when you do that.
  - Make sure you update 'example/CHANGELOG.md' when you do that.
  - The first time this runs you might need to adjust the image configuration on github container registry to make it public
  - You may also need to adjust the github Actions configuration (Settings > Actions > General > Workflow > Read & Write)
- Adjust the 'image' key in 'example/config.yaml' so it points to your username instead of 'home-assistant'.
  - This is where the build images will be published to.
- Rename the example directory.
  - The 'slug' key in 'example/config.yaml' should match the directory name.
- Adjust all keys/url's that points to 'home-assistant' to now point to your user/fork.
- Share your repository on the forums https://community.home-assistant.io/c/projects/9
- Do awesome stuff!
 -->

[aarch64-shield]: https://img.shields.io/badge/aarch64-yes-green.svg
[amd64-shield]: https://img.shields.io/badge/amd64-yes-green.svg
[armhf-shield]: https://img.shields.io/badge/armhf-yes-green.svg
[armv7-shield]: https://img.shields.io/badge/armv7-yes-green.svg
[i386-shield]: https://img.shields.io/badge/i386-yes-green.svg
