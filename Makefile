PYTHON=${HOME}/Desktop/relay/venv/bin/python
GIT=/opt/homebrew/bin/git

NOW=`/bin/date`

run:
	${PYTHON} main.py

run/action:
	python main.py

upload: run
	${GIT} commit -am "Updates - ${NOW}"
	${GIT} push 
	