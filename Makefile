run:
	python3 prober.py

doctest:
	python3 -m doctest -o FAIL_FAST prober.py
