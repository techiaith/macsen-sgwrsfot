default: build


build:
	docker build --rm -t techiaith/adapt .

	
run:
	docker run --name techiaith-adapt -it --rm \
		-v ${PWD}/local/:/usr/local/src/adapt-cy \
		techiaith/adapt bash

