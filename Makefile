default: build

build:
	docker build --rm -t techiaith/padatious .

	
run:
	docker run --name techiaith-padatious -it --rm \
		-v ${PWD}/online-api/assistant/:/opt/padatious/src \
		techiaith/padatious bash

clean:
	docker rmi techiaith/padatious



# --- Runtime with Python REST API  ----------------------------------------------------
build-online-api: 
	docker build --rm -t techiaith/skills-online-api -f Dockerfile.online-api .

run-online-api: 
	docker run --name skills-online-api --restart=always \
        -d -p 5455:8008  \
        techiaith/skills-online-api

stop-online-api:
	docker stop skills-online-api
	docker rm skills-online-api

clean-online-api:
	docker rmi techiaith/skills-online-api

