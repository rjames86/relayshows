PYTHON=${HOME}/Desktop/relay/venv/bin/python
GIT=/opt/homebrew/bin/git

run:
	${PYTHON} main.py

upload: run
	${GIT} commit -am "Updates - $(time)"
	${GIT} push 
	