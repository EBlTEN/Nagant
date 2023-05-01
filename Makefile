start:
	python3 main.py 2>/dev/null &

kill:
	pgrep python3 | xargs kill

pull:
	pgrep python3 | xargs kill
	git pull
	python3 main.py 2>/dev/null &
	