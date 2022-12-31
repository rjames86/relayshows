PYTHON=${HOME}/Desktop/relay/venv/bin/python
GIT=/opt/homebrew/bin/git

run:
	${PYTHON} main.py

upload: run
	NOW=$(date)
	${GIT} commit -am "Updates - $(NOW)"
	${GIT} push 
	