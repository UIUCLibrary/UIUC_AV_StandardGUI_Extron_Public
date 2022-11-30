##==============================================================================
## These are per system configuration variables, modify these as required

roomName = 'Test Room'     # Room Name - update for each project
activityMode = 3           # Activity mode popup to display
startupTimer = 10          # Max startup timer duration
switchTimer = 20           # Max switch timer duration
shutdownTimer = 30,        # Max shutdown timer duration
shutdownConfTimer = 30     # Shutdown confirmation duration
defaultSource = "PC001"    # Default source on activity switch

# Icon Map
#     0 - no source
#     1 - HDMI
#     2 - PC
#     3 - Wireless
#     4 - Camera
#     5 - Document Camera
#     6 - BluRay
sources = [
            {"id": "PC001",
             "name": "Room PC",
             "icon": 2},
            {"id": "WPD001",
             "name": "Wireless Pres.",
             "icon": 3},
            {"id": "PL001",
             "name": "HDMI",
             "icon": 1}
          ]

techPIN = "1867"           # PIN Code to access tech pages, must be a string
                           # fewer than 10 characters of 0-9

##==============================================================================
##
##++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
## DO NOT MODIFY - System Variables

activity = "off"
source = "none"
sourceOffset = 0
activityDict = {
                "share": "Sharing", 
                "adv_share": "Adv. Sharing",
                "group_work": "Group Work"
                }

##++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++