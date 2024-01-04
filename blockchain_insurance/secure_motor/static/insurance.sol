// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract MotorInsurance {
    enum PolicyType {comprehensive, thirdparty, ttf}
    enum VehicleUse {commercial, psv, personal}
    enum PolicyStatus {active, inactive, expired, canceled}
    struct Policy{
        uint policyNo;
        string holder;
        PolicyType pType;
        VehicleUse use;
        PolicyStatus status;
        uint claimsFiled;
        uint256 value;
        string registration;
        uint date_created;
        uint expiry_date;
        uint next_premium;
        bool exist;
    }
    Policy[] public policies;
    mapping(string => Policy) public policyByRegistration;
    uint policyCount = 0;
    function policySize() public view returns(uint) {
        return policies.length;
    }

    function exists(string memory _registration) public view returns(bool) {
        if(policyByRegistration[_registration].exist == true){
            return true;
        }
        else{return false;}
    }

    function createPolicy(
        string memory _holder,
        string memory _pTypeString,
        string memory _useString,
        uint256 _value,
        string memory _registration
    ) internal {
        uint PolicyId = uint(keccak256(abi.encodePacked(_holder, block.timestamp)));
        uint _date_created = block.timestamp;
        uint _expiry_date = block.timestamp + 365 days;
        uint _next_premium = block.timestamp + 4 weeks;

        VehicleUse _use;
        PolicyType _pType;
        policyCount += 1;

        if(keccak256(abi.encodePacked(_useString)) == keccak256(abi.encodePacked("commercial"))){
            _use = VehicleUse.commercial;
        }
        else if(keccak256(abi.encodePacked(_useString)) == keccak256(abi.encodePacked("personal"))){
            _use = VehicleUse.personal;
        }
        else if(keccak256(abi.encodePacked(_useString)) == keccak256(abi.encodePacked("psv"))){
            _use = VehicleUse.psv;
        }
        if(keccak256(abi.encodePacked(_pTypeString)) == keccak256(abi.encodePacked("Comprehensive"))){
            _pType = PolicyType.comprehensive;
        }
        else if(keccak256(abi.encodePacked(_pTypeString)) == keccak256(abi.encodePacked("ThirdParty"))){
            _pType = PolicyType.thirdparty;
        }
        else if(keccak256(abi.encodePacked(_pTypeString)) == keccak256(abi.encodePacked("ttf"))){
            _pType = PolicyType.ttf;
        }
        Policy memory newPolicy = Policy({
            policyNo: PolicyId,
            holder: _holder,
            pType: _pType,
            use: _use,
            status: PolicyStatus.active,
            claimsFiled: 0,
            value: _value,
            registration: _registration,
            date_created: _date_created,
            expiry_date: _expiry_date,
            next_premium: _next_premium,
            exist: true
        });
        policies.push(newPolicy);
        policyByRegistration[_registration] = newPolicy;
    }
    function policyValidity(string memory _holder, string memory _pTypeString, string memory _useString, uint256 _value, string memory _registration) public {
        if(exists(_registration)){
            if(policyByRegistration[_registration].status == PolicyStatus.expired){
                createPolicy(_holder, _pTypeString, _useString, _value, _registration);
            }
            else{
                revert(string.concat("A policy currently exists for ", _registration));
            }
        }
        else{
            createPolicy(_holder, _pTypeString, _useString, _value, _registration);
        }
    } 
}