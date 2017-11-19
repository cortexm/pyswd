.PHONY: test install uninstall

all: test install

test:
	@echo TESTING
	@python3 -m unittest discover

install:
	@echo INSTALLING
	@pip3 install --upgrade .

editable:
	@echo INSTALLING editable
	@pip3 install --editable .

uninstall:
	@echo UNINSTALLING
	@pip3 uninstall pyswd
