

Feature: Sort
    Sorting tasks

    Scenario: Sorting by id, ascending
        Given I am using the test data 
        And I sort by id
        And I sort in ascending order

        When I sort the data

        Then The result should be the same as the test data
    
    Scenario: Sorting by due date, descending
        Given I am using the test data 
        And I sort by due date
        And I sort in descending order

        When I sort the data

        Then The result should be organized from highest due date to lowest 
    
    Scenario: Sorting empty list
        Given I am using an empty list
        And I sort by anything
        And I sort in any order

        When I sort the data

        Then The result should be an empty list