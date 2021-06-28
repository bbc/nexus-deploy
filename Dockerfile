FROM 536795411033.dkr.ecr.eu-west-1.amazonaws.com/fpm:centos8

RUN mkdir -p /target
WORKDIR /target

RUN yum install -y wget
RUN wget https://download.sonatype.com/nexus/3/latest-unix.tar.gz

RUN mkdir opt
RUN cd opt && tar xzvf ../latest-unix.tar.gz

RUN echo opt/nexus-* | cut -f 2 -d - | sed 's/.*/--version &/g' >.fpm
RUN echo opt/nexus-* | cut -f 3 -d - | sed "s/.*/--iteration &.$(date +%s)/g" >>.fpm

RUN mv opt/nexus-* opt/nexus
COPY nexus.vmoptions /target/opt/nexus/bin/nexus.vmoptions
RUN fpm -s dir -t rpm --name nexus --depends nginx-crl --depends nfs-utils \
      --depends cosmos-ca-bundle-devs --depends cosmos-ca-bundle-staff \
      --depends cosmos-ca-bundle-services opt=/


FROM 536795411033.dkr.ecr.eu-west-1.amazonaws.com/cosmos:centos8
# This tests the RPM is installable and allows for running locally via makefile
COPY --from=0 /target /target
RUN repo yum-config cosmos-el8/revisions/stable >/etc/yum.repos.d/cosmos.repo
RUN --mount=type=secret,id=client.crt,dst=/etc/pki/tls/certs/client.crt \
    --mount=type=secret,id=client.key,dst=/etc/pki/tls/private/client.key \
    yum localinstall -y /target/*.rpm

RUN yum install -y java
RUN java -version
ADD nexus.vmoptions /opt/nexus/bin/nexus.vmoptions
ADD etc/systemd/system/nexus.service /etc/systemd/system/nexus.service
RUN systemctl enable nexus

#CMD /opt/nexus/bin/nexus run
