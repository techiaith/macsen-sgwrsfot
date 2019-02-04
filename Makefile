default: build

build:
	docker build --rm -t techiaith/adapt .

	
run:
	docker run --name techiaith-adapt -it --rm \
		-v ${PWD}/online-api/cy/:/usr/local/src/adapt-cy \
		-v ${PWD}/padatious/:/opt/padatious/src \
		techiaith/adapt bash

clean:
	docker rmi techiaith/adapt



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

