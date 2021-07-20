default: build

build-local:
	docker build --rm -t techiaith/padatious -f Dockerfile.local .

	
run-local:
	docker run --name techiaith-padatious \
		-it --rm \
		--link skills-online-mysql:mysql \
		-v ${PWD}/server/assistant/:/opt/padatious/src \
		-v ${PWD}/recordings/:/recordings \
		-v ${PWD}/data/:/data \
		techiaith/padatious bash

clean-local:
	docker rmi techiaith/padatious



# --- Runtime with Python REST API  ----------------------------------------------------
VERSION := 20.10
PORT := 5456

build: 
	docker build --rm -t techiaith/skills-server-${VERSION} .

run: 
	sudo rm -rf ${PWD}/log-${VERSION}
	docker run --name skills-server-${VERSION} --restart=always \
		--link skills-online-mysql:mysql \
		-v ${PWD}/recordings/data/:/recordings \
		-v ${PWD}/log-${VERSION}/:/var/log/skills-server \
		-d -p ${PORT}:8008  \
		techiaith/skills-server-${VERSION} 

stop:
	-docker stop skills-server-${VERSION}
	-docker rm skills-server-${VERSION}

clean:
	sudo rm -rf ${PWD}/log-${VERSION}
	-docker rmi techiaith/skills-server-${VERSION}



# --- MySQL for managing recorded prompts -----------------------------------------------
mysql:
	docker run --name skills-online-mysql --restart=always \
	 -e MYSQL_ROOT_PASSWORD=Mac53n \
	 -v ${PWD}/mysql:/var/lib/mysql \
	 -d mysql --character-set-server=utf8mb4 --collation-server=utf8mb4_unicode_ci

clean-mysql:
	-docker stop skills-online-mysql
	-docker rm skills-online-mysql
	sudo rm -rf ${PWD}/mysql

