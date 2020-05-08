run:
	python3 prober.py

doctest:
	python3 -m doctest -o FAIL_FAST prober.py

demo:
	python3 -m pytest -vvss  --pdb moduleloader.py

test:
	python3 -m pytest -vs --cov=. --cov-report=term-missing moduleloader.py
