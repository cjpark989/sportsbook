.SILENT:clean

install: requirements.txt
	@python -m pip install --upgrade pip ||:
	@pip install -r requirements.txt ||:

format:
	@autoflake --in-place --remove-unused-variables --recursive sd/ ||:
	@isort sd/ ||:
	@black sd/ ||: