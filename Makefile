all:
	@echo haha;

run: load initdb extract visualize
	@echo "\n\n\n";
	@echo "Data downloaded";
	@echo "Data saved into database";
	@echo "Data extracted";
	@echo "Data visualized";

load:
	@cd src; python3 load_data.py;

extract:
	@cd src; python3 extract_data.py;

visualize:
	@cd src; python3 visualize_data.py;

initdb:
	@cd src; python3 create_db.py;

start_db_wsl:
	@sudo service mongodb start;
