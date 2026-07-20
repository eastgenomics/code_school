## Codeschool presentation - Good with Unit testing: Principles, Python and TDD

Here you will find the scripts that I have used to present some examples for unit testing. Feel free to use this to see how unit testing works, or feel free to use these scripts as a template to your unit testing.

To run pytest, simply run `pytest` in terminal, inside the `example_code` folder. To run pytest-cov, run the following line instead from your terminal:

**Prerequisites:** Install dependencies with `pip install pytest pytest-cov pytest-mock` before running the tests.

```bash
pytest --cov=bin --cov-report=html
```