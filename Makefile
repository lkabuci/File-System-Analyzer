
all:
	./.env/bin/python3 main.py .

clean:
	$$(find . -type d -name __pycache__ -exec rm -rf {} \;)