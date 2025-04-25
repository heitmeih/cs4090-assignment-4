# Assignment 4: To-Do App Testing Assignment

## 1. Unit Testing

Code location: `tests/test_basic.py`

### Approach

Create a single unit test per function in tasks.py, which provides functionality to the app.

### Proof of Code Coverage

![code coverage](./attachments/code-coverage.png)

Note: Given that `app.py` is graphical interface code, there's not really an easy way of automatically testing it (unless there's a tool I don't know about). Hence, I interpretted the 90% coverage estimate as applying only to `tasks.py`.

## 2. Bug Reporting And Fixing

### Bug 1

#### Description

The reading/writing of the `tasks.json` file is dependent on the working directory from which the app is run.

#### Before

![proof of bug 1](./attachments/bug1-before.jpg)

The bottom arrow shows the `tasks.json` made when running the app from the root directory of the repository; the top arrow points to the `tasks.json` it should actually pull from.

#### After

![proof of bug 1](./attachments/bug1-after.jpg)

After the fix is implemented, you can see that the original `tasks.json` file was modified instead of a new file being created.
