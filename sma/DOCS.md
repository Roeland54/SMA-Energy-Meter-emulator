# SMA Energy Meter emulator

This home assistant add-on can emulate the existence of one or more SMA Energy Meters on the local network. This makes it possible to use the data from other meter types and integrate them in your SMA inverter.

# Configuration

If you have a mqtt broker configured in home assistant you do not need to configure anything. Otherwise fill in the mqtt configuration in the configuration tab.

## How to use

The add-on will subscribe to the following mqtt topic: `sma/emeter/<NUMERIC_METER_ID>/state`. When receiving the first message the emulator wil start the emulation of the energy meter with the provided <NUMERIC_METER_ID>. The emulator wil send a udp packet every 1000ms. The content of the packet wil stay the same until it gets updated by the next mqtt message.

```json
{
  "powerIn": 125.5, // power consumption in W
  "powerOut": 80.3, // power production in W
  "energyIn": 5000.603, // consumed energy in kWh
  "energyOut": 2000.707, // produced energy in Kwh
  "destinationAddresses": [
    "192.168.1.34" // ip-address(es) to send the packets to. This should be the ip of the inverter. If you leave this emtpy then multicast will be used. (multicast is not confirmed to work yet)
  ]
}
```

# Home Assistant

example of a service call to publish the mqtt message:

```yaml
service: mqtt.publish
data:
  payload_template: |-
    {
      "powerIn": {{states('sensor.power_consumed_from_grid')}},
      "powerOut": {{states('sensor.power_returned_to_grid')}},
      "energyIn": {{states('sensor.energy_grid_consumed_helper')}},
      "energyOut": {{states('sensor.energy_grid_returned_helper')}},
      "destinationAddresses": [
          "192.168.1.34"
        ]
    }
  topic: sma/emeter/1/state
```