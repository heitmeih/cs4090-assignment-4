

Feature: Sort
    Gettings stats for tasks

    Scenario: Test data stats
        Given I am using the test data 

        When I fetch its stats

        Then The result should be 4 total, 2 completed, 2 incomplete, and 2 overdue
    
    Scenario: Empty list stats
        Given I am using an empty list

        When I fetch its stats

        Then The result should be 0 total, 0 completed, 0 incomplete, and 0 overdue