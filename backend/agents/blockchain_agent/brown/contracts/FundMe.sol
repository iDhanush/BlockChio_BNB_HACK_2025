// SPDX-License-Identifier: MIT
pragma solidity ^0.6.0;

import "@chainlink/contracts/src/v0.6/interfaces/AggregatorV3Interface.sol";
import "@chainlink/contracts/src/v0.6/vendor/SafeMathChainlink.sol";

contract FundMe {
    using SafeMathChainlink for uint256;

    mapping(address => uint256) public addressToFund;
    address public owner;
    address[] public funders;

    constructor() public {
        owner = msg.sender;
    }

    function fund() public payable {
        uint256 minimumETH = 1e14; // 0.0001 ETH
        require(msg.value >= minimumETH, "Minimum ETH not met");
        addressToFund[msg.sender] += msg.value;
        funders.push(msg.sender);
    }

    function getPrice(uint256 ethAmt) public view returns (uint256) {
        AggregatorV3Interface priceFeed = AggregatorV3Interface(
            0x694AA1769357215DE4FAC081bf1f309aDC325306
        );
        (, int256 answer, , , ) = priceFeed.latestRoundData();
        uint256 price = uint256(answer * 10000000000);
        return (price * ethAmt) / 1e18;
    }

    /// @notice Transfer funds from this contract to another address
    /// @param from The address initiating the transfer (must match msg.sender)
    /// @param to The recipient address
    /// @param amount The amount to send (in wei)
    function transferFunds(address from, address payable to, uint256 amount) public {
        require(from == msg.sender, "Only sender can initiate transfer");
        require(address(this).balance >= amount, "Insufficient contract balance");
        require(addressToFund[from] >= amount, "Insufficient deposited balance");

        addressToFund[from] = addressToFund[from].sub(amount);
        to.transfer(amount);
    }

    /// @notice Allow contract owner to withdraw all funds
    function withdrawAll() public {
        require(msg.sender == owner, "Only owner can withdraw");
        msg.sender.transfer(address(this).balance);
    }

    /// @notice Get the amount funded by a specific address
    function getUserBalance(address user) public view returns (uint256) {
        return addressToFund[user];
    }
}
