gz topic -t "/model/printerArm/joint_trajectory" -m gz.msgs.JointTrajectory -p '
    joint_names: "joint1"
    joint_names: "joint2"
    points {
      positions: -0.7854
      positions: 1.5708
      time_from_start {
        sec: 0
        nsec: 250000000
      }
    }
    points {
      positions: -1.5708
      positions: 0
      time_from_start {
        sec: 0
        nsec: 500000000
      }
    }
    points {
      positions: -1.5708
      positions: -1.5708
      time_from_start {
        sec: 0
        nsec: 750000000
      }
    }
    points {
      positions: 0
      positions: 0
      time_from_start {
        sec: 1
        nsec: 0
      }
    }'
