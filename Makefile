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
	-docker rmi techiaith/padatious



# --- Runtime with Python REST API  ----------------------------------------------------
VERSION := 22.02
PORT := 5457

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

test:
	curl "http://localhost:${PORT}/perform_skill?text=beth+fydd+y+tywydd"
	echo
	curl "http://localhost:${PORT}/perform_skill?text=faint+o'r+gloch+ydy+hi"
	echo
	curl "http://localhost:${PORT}/perform_skill?text=chwaraea+fiwsig+gan+alffa"
	echo
	curl "http://localhost:${PORT}/perform_skill?text=beth+yw'r+newyddion"
	echo
	curl "http://localhost:${PORT}/perform_skill?text=gosoda+larwm+am+chwech+o'r+gloch+yn+y+nos"
	echo
	curl "http://localhost:${PORT}/perform_skill?text=gofynna+wicipedia+pwy+oedd+owain+glyndŵr"
	echo
	curl "http://localhost:${PORT}/perform_skill?text=dangosa+raglen+heno+ar+clic"
	echo
	curl "http://localhost:${PORT}/perform_skill?text=amsera+chwarter+awr+i+mi"
	echo
	curl "http://localhost:${PORT}/perform_skill?text=rho+golau'r+gegin+i+ffwrdd"
	echo

sentences:
	curl "http://localhost:${PORT}/get_all_sentences"

skills:
	curl "http://localhost:${PORT}/get_all_skills_intents_sentences"


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

