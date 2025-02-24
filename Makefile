install:
	#install commands
	pip install --upgrade pip &&\
	pip install -r requirements.txt
format:
    #format code
	black monorepo/ travelai/ healthai/
	isort monorepo/ travelai/ healthai/
lint:
	pylint --disable=R,C monorepo/
test:
    #test
	python3 -m pytest --cov=tests -v tests/*.py