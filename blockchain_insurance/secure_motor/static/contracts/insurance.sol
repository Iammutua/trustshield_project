// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract MotorInsurance {
    address public owner;
    
    enum ClaimStatus { Pending, Approved, Rejected }
    
    struct Policy {
        uint256 policyId;
        address policyholder;
        uint256 coverageAmount;
        uint256 premiumAmount;
        uint256 startDate;
        uint256 endDate;
        bool isActive;
    }
    
    struct Claim {
        uint256 claimId;
        uint256 policyId;
        address claimant;
        uint256 claimAmount;
        ClaimStatus status;
        string reason;
        uint256 submissionDate;
        uint256 approvalDate;
    }
    
    mapping(uint256 => Policy) public policies;
    mapping(uint256 => Claim) public claims;
    
    event PolicyCreated(uint256 indexed policyId, address indexed policyholder);
    event ClaimSubmitted(uint256 indexed claimId, address indexed claimant);
    event ClaimProcessed(uint256 indexed claimId, ClaimStatus status);

    modifier onlyOwner() {
        require(msg.sender == owner, "Not the contract owner");
        _;
    }

    modifier onlyPolicyholder(uint256 _policyId) {
        require(msg.sender == policies[_policyId].policyholder, "Not the policyholder");
        _;
    }

    modifier onlyActivePolicy(uint256 _policyId) {
        require(policies[_policyId].isActive, "Policy is not active");
        _;
    }

    constructor() {
        owner = msg.sender;
    }

    function createPolicy(
        uint256 _policyId,
        uint256 _coverageAmount,
        uint256 _premiumAmount,
        uint256 _startDate,
        uint256 _endDate
    ) external {
        require(policies[_policyId].policyholder == address(0), "Policy ID already exists");
        require(_endDate > _startDate, "Invalid policy dates");
        
        Policy memory newPolicy = Policy({
            policyId: _policyId,
            policyholder: msg.sender,
            coverageAmount: _coverageAmount,
            premiumAmount: _premiumAmount,
            startDate: _startDate,
            endDate: _endDate,
            isActive: true
        });

        policies[_policyId] = newPolicy;
        emit PolicyCreated(_policyId, msg.sender);
    }

    function submitClaim(uint256 _policyId, uint256 _claimAmount, string memory _reason) 
        external 
        onlyPolicyholder(_policyId) 
        onlyActivePolicy(_policyId) 
    {
        require(_claimAmount > 0, "Invalid claim amount");
        
        uint256 claimId = uint256(keccak256(abi.encodePacked(block.timestamp, msg.sender, _policyId)));

        Claim memory newClaim = Claim({
            claimId: claimId,
            policyId: _policyId,
            claimant: msg.sender,
            claimAmount: _claimAmount,
            status: ClaimStatus.Pending,
            reason: _reason,
            submissionDate: block.timestamp,
            approvalDate: 0
        });

        claims[claimId] = newClaim;
        emit ClaimSubmitted(claimId, msg.sender);
    }

    function processClaim(uint256 _claimId, bool _isApproved) external onlyOwner {
        Claim storage claim = claims[_claimId];
        require(claim.status == ClaimStatus.Pending, "Claim is not pending");

        if (_isApproved) {
            // Process claim approval logic
            claim.status = ClaimStatus.Approved;
            claim.approvalDate = block.timestamp;
        } else {
            // Process claim rejection logic
            claim.status = ClaimStatus.Rejected;
        }

        emit ClaimProcessed(_claimId, claim.status);
    }

    function cancelPolicy(uint256 _policyId) external onlyPolicyholder(_policyId) {
        policies[_policyId].isActive = false;
    }
}