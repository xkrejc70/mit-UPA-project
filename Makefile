all:
	@echo haha;

run:
	cd load_data; python3 load_data.py; cd ../db; python3 db.py;

load:
	@cd load_data; python3 load_data.py;

initdb:
	@cd db; python3 db.py;