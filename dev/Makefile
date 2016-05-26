clean:
	-docker-compose rm -f
	-docker rmi dev_v8cffi

build: clean
	docker-compose up -d
	docker cp v8cffi_master:/code/v8 ../v8cffi/src

.PHONY: clean build
