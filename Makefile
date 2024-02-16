
all:
	./.env/bin/python3 main.py .

venv:
	python3 -m venv .env
	source .env/bin/activate
	pip install -r --upgrade requirements.txt

test:
	docker compose up --build

clean:
	$$(find . -type d -name __pycache__ -exec rm -rf {} \;)
