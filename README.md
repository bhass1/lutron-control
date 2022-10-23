# Lutron-Control

For controlling the Lutron devices in my house.

## Lutron Caseta Bridge (Model: BDG-1)

### Default Telnet Credentials

- Username: `lutron`
- Password: `integration`

### Select Command Reference

- Check light status for light ID 2: `?OUTPUT,2,1`
- Set light 100% for light ID 2: `#OUTPUT,2,1,100.00`
- Set light 0% for light ID 2: `#OUTPUT,2,1,0`

## Resources
- [Kolby Graham's "Lutron Integration Protocol" Blog](docs/Lutron%20Integration%20Protocol%20–%20Kolby%20Graham.net.htm)
- [Lutron Integration Protocol (Local Copy)](docs/Lutron-040249.pdf)
- [Integration Protocol (Online Copy)](https://www.lutron.com/TechnicalDocumentLibrary/040249.pdf)

## Copyright Notice

Copyright (c) 2022 Bill Hass

This work is licensed under the Creative Commons Attribution 4.0 International License.
To view a copy of this license, visit http://creativecommons.org/licenses/by/4.0/ or
send a letter to Creative Commons, PO Box 1866, Mountain View, CA 94042, USA.
