run:
	docker build -t nexus-deploy .
	docker build --secret id=client.crt,src=/private/etc/pki/tls/certs/client.crt --secret id=client.key,src=/private/etc/pki/tls/private/client.key -t nexus-local -f Dockerfile.test .
	docker run -p 8081:8081 -v /sys/fs/cgroup:/sys/fs/cgroup:ro --privileged --rm -ti nexus-local
