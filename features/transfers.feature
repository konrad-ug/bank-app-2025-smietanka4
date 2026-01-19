Feature: Transfer operations

  Scenario: Incoming transfer increases balance
    Given Account registry is empty
    And I create an account using name: "john", last name: "doe", pesel: "85092909246"
    When I perform "incoming" transfer of "500" to account "85092909246"
    Then Account "85092909246" has balance equal to "500"

  Scenario: Outgoing transfer decreases balance
    Given Account registry is empty
    And I create an account using name: "john", last name: "doe", pesel: "85092909246"
    And I perform "incoming" transfer of "1000" to account "85092909246"
    When I perform "outgoing" transfer of "300" to account "85092909246"
    Then Account "85092909246" has balance equal to "700"

  Scenario: Cannot perform outgoing transfer with insufficient funds
    Given Account registry is empty
    And I create an account using name: "john", last name: "doe", pesel: "85092909246"
    When I perform "outgoing" transfer of "1000" to account "85092909246"
    Then Transfer should fail

  Scenario: Express transfer deducts fee
    Given Account registry is empty
    And I create an account using name: "john", last name: "doe", pesel: "85092909246"
    And I perform "incoming" transfer of "1000" to account "85092909246"
    When I perform "express" transfer of "100" to account "85092909246"
    Then Account "85092909246" has balance less than "900"

  Scenario: Transfer to non-existent account fails
    When I perform "incoming" transfer of "100" to account "99999999999"
    Then Transfer should fail

  Scenario: Invalid transfer type fails
    Given Account registry is empty
    And I create an account using name: "john", last name: "doe", pesel: "85092909246"
    When I perform invalid type "wrong" transfer of "100" to account "85092909246"
    Then Transfer should fail
