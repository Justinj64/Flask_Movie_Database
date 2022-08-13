build:
	sudo touch src/worker.log
	sudo docker build -t db-worker .;
run:
	sudo docker run --restart always -v ${PWD}/src/worker.log:/home/src/worker.log --name db-worker -d db-worker;
remove:
	sudo docker rm -f db-worker;
rebuild:
	sudo touch src/worker.log
	sudo docker build -t db-worker .;
	sudo docker rm -f db-worker ;
	sudo docker run --network host --restart always -v ${PWD}/src/Movies.db:/home/src/Movies.db -v ${PWD}/src/worker.log:/home/src/worker.log --name db-worker -d db-worker;
