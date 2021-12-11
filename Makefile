all:
	@echo haha;

run: load initdb
	@echo "\n\n\n";
	@echo "Data downloaded";
	@echo "Data saved into database";

load:
	@cd load_data; python3 load_data.py;

extract:
	@cd load_data; python3 extract_data.py;

visualize:
	@cd load_data; python3 visualize_data.py;

initdb:
	@cd load_data; python3 create_db.py;

start_db_wsl:
	@sudo service mongodb start;
