const { accounts, contract } = require('@openzeppelin/test-environment');

const { expect } = require('chai');

const DaiToken = contract.fromArtifact('DaiToken');
const Pool = contract.fromArtifact('Pool');

describe('Pool', function () {
  const [owner, other] = accounts;

  before(async function () {
    this.daiContract = await DaiToken.new(1000, { from: owner });
    this.poolContract = await Pool.new(this.daiContract.address, {
      from: owner,
    });
  });

  it('the deployer is the owner', async function () {
    expect(await this.poolContract.owner()).to.equal(owner);
  });

  it('deposits 100 dai to the pool', async function () {
    await this.daiContract.approve(this.poolContract.address, 100, {
      from: owner,
    });
    await this.poolContract.deposit(100, 0, { from: owner });
    var poolBalance = await this.poolContract.poolBalance();
    expect(poolBalance.toString()).to.equal('100');
  });

  it('transfers 1 eth as collateral to the pool', async function () {
    await this.poolContract.send(1e18, { from: other });
    var balance = await this.poolContract.getTotalCollateralDeposited({
      from: owner,
    });
    expect(balance.toString()).to.equal('1000000000000000000');
  });

  it('borrows 100 dai from the pool', async function () {
    await this.poolContract.borrow(100, 0, { from: other });
    var balance = await this.daiContract.balanceOf(other);
    expect(balance.toString()).to.equal('100');
  });

  it('repays 100 dai to the pool', async function () {
    await this.daiContract.approve(this.poolContract.address, 100, {
      from: other,
    });
    await this.poolContract.repay(1, { from: other });
    var poolBalance = await this.poolContract.poolBalance();
    expect(poolBalance.toString()).to.equal('100');
  });

  it('withdraws 100 dai from the pool', async function () {
    await this.poolContract.withdraw(1, { from: owner });
    var balance = await this.daiContract.balanceOf(owner);
    expect(balance.toString()).to.equal('1000');
  });
});
