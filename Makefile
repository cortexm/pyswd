.PHONY: test install uninstall

all: install

test:
	@echo TESTNG ..
	@python3 -m unittest discover

install: test
	@echo INSTALLING ..
	@pip3 install --upgrade .

uninstall:
	@echo UNINSTALLING ..
	@pip3 uninstall pyswd
