# Decentrabank

Decentrabank focuses on developing a DeFi app which implements the concept of yield farming based Dai token.

## Introduction

- The aim of this platform is to help the users to get loan at fixed interest rate, this platform has two roles: lender and borrower. A lender can deposit DAI(stablecoin) in pool and earn interest, whereas a borrower can borrow required DAI from the pool by keeping something of same or higher value as collateral as crypto and pay back the borrowed amount with interest in desired amount of time provided to him.

---

## How it works

- Connect an Ethereum wallet like Metamask
- Deposit amount to the pool in DAI with fixed interest rate
- Add collateral as ether before borrowing the amount
- Borrow amount from the pool in DAI with fixed interest rate
- Withdraw the deposited DAI token with interest
- Return the borrowed DAI token with interest

<p align="center">
  <img src="https://raw.githubusercontent.com/itssunny322/TestRepo/main/Decentrabank.png" | width=720>
</p>

---

## Technologies
1. Solidity (Truffle framework)
2. Slither (static code analysis)
3. Node.js (backend API)
4. React.js (frontend)
5. Mocha (test framework)
6. Metamask (web3 wallet)

## Setup
```
git clone projecturl
cd projectname
npm install
truffle compile
truffle migrate
```

## Note
Shared here only a subset of the codebase (2 smart contracts).
