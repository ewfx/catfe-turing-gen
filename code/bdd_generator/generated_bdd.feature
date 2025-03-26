 Feature: Financial Transaction System

   As a user, I want to be able to deposit and withdraw money from my account safely and accurately.

   Background:
      Given I have a unique account ID and an initial balance

   Scenario 1: Deposit money successfully
      Given I have an initial balance of <amount>
      When I deposit <additional_amount>
      Then my new balance should be <calculated_new_balance>
      And the transaction should be logged

   Scenario 2: Withdraw money successfully
      Given I have a balance of <initial_balance>
      And I have sufficient funds for the withdrawal amount
      When I withdraw <withdrawal_amount>
      Then my new balance should be <calculated_new_balance>
      And the transaction should be logged

   Scenario 3: Attempt to withdraw more than the available balance
      Given I have a balance of <initial_balance>
      When I attempt to withdraw an amount greater than my current balance
      Then I should receive an "Insufficient funds" error message
      And the transaction should not be processed and should not be logged