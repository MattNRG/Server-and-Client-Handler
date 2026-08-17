# Server & Client Handler
Updated version of NRG RoboCup Wi-Fi Handler and Game Controller. Focused on making the program more reliable and efficient. 
⚠️ Since the repository was moved under TalTech, this instance will no longer be updated ⚠️


<img width="2500" height="500" alt="Banner (2500 x 500 px)" src="https://github.com/user-attachments/assets/28f648a0-d93e-4b2f-8866-cc844aa6deb1" />


## What changed?

Got rid of _Tie 'n' Pair_ replacing it with a new system. Using a static IP, the robots send connection requests themselves, avoiding the problem of looking for robots only at the start of the program. Likewise, using STREAM, not DGRAM, we can leave the connections open for easier messaging. 

Everything is threaded, making sure everything gets through and processed.

And finally, we no longer use JSON to save the IP's (Since the robots can connect at any time), and it's now replaced with classes.

## Testing Equipment

- TP-Link TL-WR844N

- Raspberry Pi 4

## Software Requirements
The following dependencies are required to run the program:
- Colorama
- PyGame


## Roadmap
- [x] Store robot data using classes
- [x] Implement Server-Client communication
- [x] Add struct support to communications
- [x] Implement a heartbeat system to monitor robot connectivity
- [x] Improve console readability and transparency
- [x] Vision
  - [x] Update vision to be closer to sslclient Python Library
  - [x] Automatically update the robot class data (Position, onField, etc) 
- [x] Rework the file structure, split the code into modules
- [x] Add a settings system
- [x] Add server console commands
- [x] Transfer the repository to the TalTech RoboCup SSL Team 🎉

END OF PUBLIC REPOSITORY (for now)
