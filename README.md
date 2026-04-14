# Task Manager API
A client can create, list, and complete tasks. 

This is a Test-Driven Development portfolio project using `venv`, `pytest`, `pytest-cov`, `pytest-mock`, `pre-commits` and `FastAPI`. 

![tdd_fastapi_workflow](https://github.com/user-attachments/assets/4bb4420d-2b63-4f48-915d-85f117dabbd4)

## Why TDD
In TDD, you write tests first. The tests describe what your API should do. Then you write the code to make them pass.
The reason: if you write code first, you tend to write tests that fit your code. 
If you write tests first, you write code that fits your requirements. 
It also means every line of your app exists because a test demanded it.

## Pytest + Pre-commits bomb
Pre-commit intercepts the commit, runs ruff, then runs pytest with coverage. If all 6 tests pass and coverage is above 80%, the commit goes through. If anything fails, you see exactly what broke and the commit is blocked.
This is the whole point: you can never accidentally commit broken code. The toolchain enforces correctness at the moment it matters most.

## To Recreate Virtual Environment with

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```


