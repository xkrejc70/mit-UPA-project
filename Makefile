all:
	@echo haha :(;

load:
	@cd load_data; python3 load_data.py;

initdb:
	@cd db; python3 init_db.py;