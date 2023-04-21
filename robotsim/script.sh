gz topic -t "/model/printerArm/joint_trajectory" -m gz.msgs.JointTrajectory -p '
    joint_names: "joint1"
    joint_names: "joint2"
    joint_names: "joint3"
    points {
      positions: -0.7854
      positions: 1.5708
      positions: 0
      time_from_start {
        sec: 1
        nsec: 0000000
      }
    }
    points {
      positions: -1.5708
      positions: 0
      positions: 1.5708
      time_from_start {
        sec: 2
        nsec: 000000
      }
    }
    points {
      positions: -1.5708
      positions: -1.5708
      positions: 0
      time_from_start {
        sec: 3
        nsec: 0000000
      }
    }
    points {
      positions: 0
      positions: 0
      positions: 0
      time_from_start {
        sec: 4
        nsec: 0
      }
    }'
