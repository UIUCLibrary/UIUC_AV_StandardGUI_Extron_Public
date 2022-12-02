##==============================================================================
## These are per system configuration variables, modify these as required

roomName = 'Test Room'        # Room Name - update for each project
activityMode = 3              # Activity mode popup to display
startupTimer = 10             # Max startup timer duration
switchTimer = 20              # Max switch timer duration
shutdownTimer = 30,           # Max shutdown timer duration
shutdownConfTimer = 30        # Shutdown confirmation duration
activitySplash = 15           # Duration to show activity splash pages for
defaultSource = "PC001"       # Default source id on activity switch
primaryDestination = "PRJ001" # Primary destination
micCtl = 1                    # Microphone control: 0 - no mic control, 1 - mic control

# Icon Map
#     0 - no source
#     1 - HDMI
#     2 - PC
#     3 - Wireless
#     4 - Camera
#     5 - Document Camera
#     6 - BluRay
sources = \
   [
      {
         "id": "PC001",
         "name": "Room PC",
         "icon": 2,
         "input": 3,
         "src-ctl": "PC",
         "adv-src-ctl": None
      },
      {
         "id": "PL001-1",
         "name": "HDMI 1",
         "icon": 1,
         "input": 1,
         "src-ctl": "HDMI",
         "adv-src-ctl": None
      },
      {
         "id": "PL001-2",
         "name": "HDMI 2",
         "icon": 1,
         "input": 2,
         "src-ctl": "HDMI",
         "adv-src-ctl": None
      },
      {
         "id": "WPD001",
         "name": "Inst. Wireless",
         "icon": 3,
         "input": 4,
         "src-ctl": "WPD",
         "adv-src-ctl": "WPD"
      },
      {
         "id": "WPD002",
         "name": "North Wireless",
         "icon": 3,
         "input": 5,
         "src-ctl": "WPD",
         "adv-src-ctl": "WPD"
      },
      {
         "id": "WPD003",
         "name": "South Wireless",
         "icon": 3,
         "input": 6,
         "src-ctl": "WPD",
         "adv-src-ctl": "WPD"
      }
   ]

# Destination Types
#  proj     - Projector with uncontrolled screen
#  proj+scn - Projector with controlled screen
#  mon      - Large format monitor
#  conf     - Instructor confidence monitor
destinations = \
   [
      {
         "id": "PRJ001",
         "name": "Projector",
         "output": 3,
         "type": "proj+scn",
         "rly": [1, 2],
         "group-work-src": "WPD001",
         "adv-layout": {
            "row": 0,
            "pos": 0
         }
      },
      {
         "id": "MON001",
         "name": "North Monitor",
         "output": 2,
         "type": "mon",
         "group-work-src": "WPD002",
         "adv-layout": {
            "row": 1,
            "pos": 0
         }
      },
      {
         "id": "MON002",
         "name": "South Monitor",
         "output": 4,
         "type": "mon",
         "group-work-src": "WPD003",
         "adv-layout": {
            "row": 1,
            "pos": 1
         }
      }
   ]
   
cameras = \
   [
      {
         "id": "CAM001",
         "name": "North Camera"
      },
      {
         "id": "CAM002",
         "name": "South Camera"
      }
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
activityDict = \
   {
      "share": "Sharing", 
      "adv_share": "Adv. Sharing",
      "group_work": "Group Work"
   }
adv_share_layout = None

CtlProc_Main = None
TP_Main = None
TransitionDict = {}
SourceButtons = {}
PinButtons = {}

##++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++