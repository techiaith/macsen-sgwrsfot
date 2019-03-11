default: build

build:
	docker build --rm -t techiaith/padatious .

	
run:
	docker run --name techiaith-padatious -it --rm \
		--link skills-online-mysql:mysql \
		-v ${PWD}/online-api/assistant/:/opt/padatious/src \
		techiaith/padatious bash

clean:
	docker rmi techiaith/padatious



# --- Runtime with Python REST API  ----------------------------------------------------
build-online-api: 
	docker build --rm -t techiaith/skills-online-api -f Dockerfile.online-api .

run-online-api: 
	docker run --name skills-online-api --restart=always \
		--link skills-online-mysql:mysql \
		-v ${PWD}/recordings/:/recordings \
		-d -p 5455:8008  \
		techiaith/skills-online-api 

stop-online-api:
	docker stop skills-online-api
	docker rm skills-online-api

clean-online-api:
	docker rmi techiaith/skills-online-api



# --- MySQL for managing recorded prompts -----------------------------------------------
mysql:
	docker run --name skills-online-mysql --restart=always \
	 -e MYSQL_ROOT_PASSWORD=Mac53n \
	 -v ${PWD}/mysql:/var/lib/mysql \
	 -d mysql --character-set-server=utf8mb4 --collation-server=utf8mb4_unicode_ci

mysql-clean:
	docker stop skills-online-mysql
	docker rm skills-online-mysql


