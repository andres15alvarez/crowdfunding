// SPDX-License-Identifier: GPL-3.0

pragma solidity >=0.7.0 <0.9.0;

/**
 * @title Crowdfunding
 * @dev Receive funding for a project.
 */
contract Crowdfunding{
    address payable owner;
    uint goal;
    uint amount;
    bool isClosed;

    event SetCrowdfunding(address indexed owner, uint goal);

    event FundingAlert(address indexed contributor, uint amount);

    event FundingFinished(uint amount);

    modifier isOwner(){
        require(
            msg.sender != owner,
            "The owner cannot funds its project."
        );
        _;
    }

    modifier hasFinished(){
        require(
            amount < goal,
            "The project has finished"
        );
        _;
    }

    constructor(uint ownerGoal){
        owner = payable(msg.sender);
        require(
            ownerGoal > 0,
            "Goal must be greater than 0."
        );
        goal = ownerGoal;
        amount = 0;
        isClosed = false;
        emit SetCrowdfunding(owner, goal);
    }

    function getAmount() public view returns (uint){
        return amount;
    }

    function fundProject() public payable isOwner hasFinished{
        amount += msg.value;
        emit FundingAlert(msg.sender, msg.value);
        if(amount >= goal){
            isClosed = true;
            owner.transfer(amount);
            emit FundingFinished(amount);
        }
    }
}