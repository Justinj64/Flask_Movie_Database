build:
	sudo touch flask_app/info.log
	sudo docker build -t flask-movie-database .;
run:
	sudo docker run --restart always -v ${PWD}/flask_app/info.log:/home/flask_app/info.log --name flask-movie-database -p 5000:5000 -d flask-movie-database;
remove:
	sudo docker rm -f flask-movie-database;
rebuild:
	sudo touch flask_app/info.log
	sudo docker build -t flask-movie-database .;
	sudo docker rm -f flask-movie-database ;
	sudo docker run --network host --restart always -v ${PWD}/celery_app/src/Movies.db:/home/flask_app/Movies.db -v ${PWD}/flask_app/info.log:/home/flask_app/info.log --name flask-movie-database -d flask-movie-database;
