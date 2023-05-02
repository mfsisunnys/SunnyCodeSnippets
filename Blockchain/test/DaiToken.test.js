const { accounts, contract } = require('@openzeppelin/test-environment');

const { expect } = require('chai');

const DaiToken = contract.fromArtifact('DaiToken');

describe('DaiToken', function () {
  const [owner] = accounts;

  beforeEach(async function () {
    this.daiContract = await DaiToken.new(1000, { from: owner });
  });

  it('the deployer is the owner', async function () {
    expect(await this.daiContract.owner()).to.equal(owner);
  });
});
