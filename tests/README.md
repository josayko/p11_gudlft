## QA branch

A development environment has been set up in `config.py` and `.env.development`.

### Run the application in development mode

```bash
$ python server
```

### Unit testing

- Run all tests

```bash
$ pytest
```

- Run a specific test, by its class name or function name

```bash
$ pytest -k "<test_name>"
```

### Tests coverage report

- Make a report

```bash
$ coverage run -m pytest
```

- Show report

```bash
$ coverage report -m
```

- Write report to `html` file

```bash
# Results are in "./htmlcov/index.html"
$ coverage html
```

### Performance test
