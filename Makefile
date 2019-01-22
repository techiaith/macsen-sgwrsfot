default: build

build:
	docker build --rm -t techiaith/adapt .

	
run:
	docker run --name techiaith-adapt -it --rm \
		-v ${PWD}/online-api/cy/:/usr/local/src/adapt-cy \
		techiaith/adapt bash

clean:
	docker rmi techiaith/adapt


# --- Runtime with Python REST API  ----------------------------------------------------
build-online-api: 
	docker build --rm -t techiaith/adapt-online-api -f Dockerfile.online-api .

run-online-api: 
	docker run --name adapt-online-api --restart=always \
        -d -p 5450:8008  \
        techiaith/adapt-online-api

stop-online-api:
	docker stop adapt-online-api
	docker rm adapt-online-api

clean-online-api:
	docker rmi techiaith/adapt-online-api

