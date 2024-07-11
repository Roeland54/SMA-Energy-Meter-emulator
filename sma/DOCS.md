# SMA Energy Meter simulator

This home assistant add-on can emulate the existence of one or more SMA Energy Meters on the local network. This makes it possible to use the data from other meter types and integrate them in your SMA inverter.

# Configuration

If you have a mqtt broker configured in home assistant you do not need to configure anything. Otherwise fill in the mqtt configuration in the configuration tab.

## How to use

The add-on will subscribe to the following mqtt topic: `sma/emeter/<NUMERIC_METER_ID>/state`. When receiving the first message the emulator wil start the emulation of the energy meter with the provided <NUMERIC_METER_ID>. The emulator wil send a udp packet every 1000ms. The content of the packet wil stay the same until it gets updated by the next mqtt message.

```json
{
  "powerIn": 1200, // power consumption in W
  "powerOut": 800, // power production in W
  "energyIn": 500000, // consumed energy in Wh
  "energyOut": 200000, // produced energy in Wh
  "destinationAddresses": [
    // optional ip-addresses to send the packets to. Default behaviour uses multicast.
  ]
}
```

# Home Assistant

example of a service call to publish the mqtt message:

```yaml
service: mqtt.publish
metadata: {}
data:
  topic: sma/emeter/1234/state
  payload_template: |-
    {{
    {
      "powerIn": 0,
      "powerOut": states('sensor.solax_inverter_power'),
      "energyIn": 0,
      "energyOut": states('sensor.solax_inverter_energy'),
      "destinationAddresses": [
        ]
    }
    }}
```