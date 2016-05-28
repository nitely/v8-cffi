clean_all:
	-bash -c "docker ps -q -f status=exited | xargs docker rm"
	-bash -c "docker images -q -f dangling=true | xargs docker rmi"

clean:
	-docker-compose rm -f -a
	-docker rmi dev_v8cffi

build: clean
	docker-compose up -d
	docker cp v8cffi_master:/code/v8 ../v8cffi/src

.PHONY: clean clean_all build
