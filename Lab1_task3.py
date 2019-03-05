# This macro shows an example of running a program on the robot using the Python API (online programming)
# More information about the RoboDK API appears here:
# https://robodk.com/doc/en/RoboDK-API.html
from robolink import *    # API to communicate with RoboDK
from robodk import *      # robodk robotics toolbox
# Any interaction with RoboDK must be done through RDK:
RDK = Robolink()
# Select a robot (a popup is displayed if more than one robot is available)
robot = RDK.ItemUserPick('Select a robot', ITEM_TYPE_ROBOT)
if not robot.Valid():
    raise Exception('No robot selected or available')
RUN_ON_ROBOT = False
# Important: by default, the run mode is RUNMODE_SIMULATE
# If the program is generated offline manually the runmode will be RUNMODE_MAKE_ROBOTPROG,
# Therefore, we should not run the program on the robot
if RDK.RunMode() != RUNMODE_SIMULATE:
    RUN_ON_ROBOT = False
if RUN_ON_ROBOT:

    # Connect to the robot using default IP
    success = robot.Connect() # Try to connect once
    status, status_msg = robot.ConnectedState()
    if status != ROBOTCOM_READY:
        # Stop if the connection did not succeed
        print(status_msg)
        raise Exception("Failed to connect: " + status_msg)
    # This will set to run the API programs on the robot and the simulator (online programming)
    RDK.setRunMode(RUNMODE_RUN_ROBOT)

# Get the current joint position of the robot
# (updates the position on the robot simulator)
joints_ref = robot.Joints()
# get the current position of the TCP with respect to the reference frame:
# (4x4 matrix representing position and orientation)
target_ref = robot.Pose()
pos_ref = target_ref.Pos()
# It is important to provide the reference frame and the tool frames when generating programs offline
# It is important to update the TCP on the robot mostly when using the driver
robot.setPoseFrame(robot.PoseFrame())
robot.setPoseTool(robot.PoseTool())
#robot.setZoneData(10) # Set the rounding parameter (Also known as: CNT, APO/C_DIS, ZoneData, Blending radius, cornering, ...)
robot.setSpeed(200) # Set linear speed in mm/s

# Setting Pose 1, Pose 2, and Pose 3 from the Lab Manual
# We enter our xyzrpw (X, Y, Z, RX, RY, RZ) into the function xyzrpw_2_pose()
# to convert out position and euler angles to a 4x4 pose matrix
pose_1 = xyzrpw_2_pose([-575, -350, 300, 131.441, -5.933 , 58.398]) 
pose_2 = xyzrpw_2_pose([-240, -445, 650, 107.452, 23.626, -107.452])
pose_3 = xyzrpw_2_pose([400, -400, 200, 160.148, -1.116, -6.369])
# Move the robot in joint space using MoveJ
robot.MoveJ(pose_1)
robot.MoveJ(pose_2)
robot.MoveJ(pose_3)
# Wait 10 seconds to run in cartesian space using MoveL
pause(10)
robot.MoveL(pose_1)
robot.MoveL(pose_2)
robot.MoveL(pose_3)

print('Done')
