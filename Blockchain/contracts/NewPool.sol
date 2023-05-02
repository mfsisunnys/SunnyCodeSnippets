// SPDX-License-Identifier: GPL-3.0
pragma solidity ^0.8.0;

import "../node_modules/@openzeppelin/contracts/utils/math/SafeMath.sol";
import "../node_modules/@openzeppelin/contracts/access/Ownable.sol";

import "./Weth.sol";
import "./GovernanceToken.sol";

contract NewPool is Ownable {
    /**
     * @notice Safe guarding contract from integer
     * overflow and underflow vulnerabilities.
     */
    using SafeMath for uint256;

    /**
     * @notice Enum to specify the current state of loan repayment
     */
    enum Status {
        Pending,
        PartiallyPaid,
        Paid
    }

    /**
     * @notice struct to define the characteristics of a loan
     */
    struct LoanInfo {
        uint256 loanId;
        uint256 loanedAmount;
        uint256 repayAmount;
        address tokenAddress;
        address collateralAddress;
        uint256 blockNumber;
        Status status;
    }

    /**
     * @notice struct to define the characteristics of a Deposit
     */
    struct DepositInfo {
        uint256 amount;
        uint256 blockNumber;
        uint256 totalInterestEarned;
    }

    /**
     * @notice struct for creating a new pool
     */
    struct Pool {
        address tokenAddress;
        uint256 tokensAvailable;
        uint256 tokensBorrowed;
        uint256 depositInterestRate;
        uint256 borrowInterestRate;
        uint256 depositInterestFactor;
        uint256 borrowInterestFactor;
    }

    /**
     * @notice more structs here
     */

    /**
     * @notice mappings here
     */

    /**
     * @notice Constructor, which is a function that executes
     * once (on deployment) sets block time, WethAddress, dbk token
     */
    constructor(address payable wethContractAddress) {
        blockTime = 14; // 14 seconds for Ethereum main net
        wethAddress = wethContractAddress;
        dbk = new DBK(1000000);
    }

    /**
     * @notice Update block time
     * @param newValue value of block time
     * @return success true if success
     */
    function updateBlocktime(
        uint256 newValue
    ) public onlyOwner returns (bool success) {
        blockTime = newValue;
        return true;
    }

    /**
     * @notice set deposit interestconstant
     * @param tokenAddress address of the token
     * @param depositIntFactor constant value
     */
    function setDepositinterestFactor(
        address tokenAddress,
        uint256 depositIntFactor
    ) public {
        pools[tokenAddress].depositInterestFactor = depositIntFactor;
    }

    /**
     * @notice set borrow interestconstant
     * @param tokenAddress address of the token
     * @param borrowIntFactor constant value
     */
    function setBorrowinterestFactor(
        address tokenAddress,
        uint256 borrowIntFactor
    ) public {
        pools[tokenAddress].borrowInterestFactor = borrowIntFactor;
    }

    /**
     * @notice this function is used for registering a token
     * @param tokenAddress the address of the token
     */
    function registerToken(address tokenAddress) public onlyOwner {
        pools[tokenAddress] = Pool({
            tokenAddress: tokenAddress,
            tokensAvailable: 0,
            tokensBorrowed: 0,
            depositInterestRate: 0,
            borrowInterestRate: 0,
            depositInterestFactor: 2500,
            borrowInterestFactor: 3000
        });
        emit TokenRegistered(tokenAddress);
    }

    /**
     * @notice Get the latest interestrate
     * @param tokenAddress the address of the token
     * @return utilityFactor the interestrate depends on supply and demand
     */
    function checkInterestInfo(
        address tokenAddress
    ) public view returns (uint256) {
        uint256 totalBalance = pools[tokenAddress].tokensAvailable;
        uint256 totalBorrow = pools[tokenAddress].tokensBorrowed;
        uint256 utilityFactor = (totalBorrow.mul(100)).div(
            totalBalance.add(totalBorrow)
        );
        return utilityFactor;
    }

    /**
     * @notice Get the latest interestrate
     * @param tokenAddress the address of the token
     * @return depositInterestRate for depositor
     */
    function getDepositInterestRate(
        address tokenAddress
    ) public returns (uint256) {
        uint256 interestRate = (pools[tokenAddress].depositInterestFactor).add(
            checkInterestInfo(tokenAddress).mul(2)
        );
        return pools[tokenAddress].depositInterestRate = interestRate;
    }

    /**
     * @notice Get the latest interestrate
     * @param tokenAddress the address of the token
     * @return borrowInterestRate for borrower
     */
    function getBorrowerInterestRate(
        address tokenAddress
    ) public returns (uint256) {
        uint256 interestRate = (pools[tokenAddress].borrowInterestFactor).add(
            checkInterestInfo(tokenAddress).mul(2)
        );
        return pools[tokenAddress].borrowInterestRate = interestRate;
    }

    /**
     * @notice calculate and update depositor's interest
     * @param tokenAddress the address of the token
     */
    function calculateDepositorInterest(address tokenAddress) public {
        // duration in seconds from deposit block to this block
        uint256 duration = block
            .number
            .sub(userTokenBal[msg.sender][tokenAddress].blockNumber)
            .mul(blockTime);

        // calculating interestby (principle * APR/100 * duration in seconds) / seconds in a year
        uint256 secondsInYear = uint256(36525).mul(86400).div(100);
        uint256 interest = (userTokenBal[msg.sender][tokenAddress].amount)
            .mul(duration)
            .mul(getDepositInterestRate(tokenAddress))
            .div(100)
            .div(secondsInYear);
        userTokenBal[msg.sender][tokenAddress].amount = userTokenBal[
            msg.sender
        ][tokenAddress].amount.add(interest);
        userTokenBal[msg.sender][tokenAddress]
            .totalInterestEarned = userTokenBal[msg.sender][tokenAddress]
            .totalInterestEarned
            .add(interest);

        userTokenBal[msg.sender][tokenAddress].blockNumber = block.number;
    }

    /**
     * @notice calculate and update a specific loan interestand borrowers's repay amount
     * @param loanId the Loan Id of the Loan
     * @param tokenAddress the address of the token
     */
    function calculateLoanInterest(
        uint256 loanId,
        address tokenAddress
    ) external {
        // duration in seconds from loan block to this block
        uint256 duration = block
            .number
            .sub(userLoanData[msg.sender][loanId - 1].blockNumber)
            .mul(blockTime);

        // calculating interestby (principle * APR/100 * duration in seconds) / seconds in a year
        uint256 secondsInYear = uint256(36525).mul(86400).div(100);
        uint256 principle = userLoanData[msg.sender][loanId - 1].loanedAmount -
            userLoanData[msg.sender][loanId - 1].repayAmount;
        uint256 interest = (principle)
            .mul(duration)
            .mul(getBorrowerInterestRate(tokenAddress))
            .div(100)
            .div(secondsInYear);
        userLoanData[msg.sender][loanId - 1].loanedAmount = userLoanData[
            msg.sender
        ][loanId - 1].loanedAmount.add(interest);
        userLoanData[msg.sender][loanId - 1].blockNumber = block.number;
        emit LoanInterest(principle, interest);
    }

    /**
     * @notice deposit ERC20 token to the pool
     * @param tokenAddress ERC20 token address
     * @param amount token deposited amount
     * @return success true if success
     */
    function deposit(
        address tokenAddress,
        uint256 amount
    ) public returns (bool success) {
        uint256 balance = userTokenBal[msg.sender][tokenAddress].amount.add(
            amount
        );
        pools[tokenAddress].tokensAvailable = pools[tokenAddress]
            .tokensAvailable
            .add(amount);
        getDepositInterestRate(tokenAddress);
        getBorrowerInterestRate(tokenAddress);
        DepositInfo memory newDeposit = DepositInfo(balance, block.number, 0);
        userTokenBal[msg.sender][tokenAddress] = newDeposit;
        uint256 governanceTokenAmount = amount.mul(10).div(100);
        success = dbk.transfer(msg.sender, governanceTokenAmount);

        if (success) {
            emit Deposited(msg.sender, tokenAddress, amount);
            success = ERC20(tokenAddress).transferFrom(
                msg.sender,
                address(this),
                amount
            );
        }

        return success;
    }
}
