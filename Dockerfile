FROM 536795411033.dkr.ecr.eu-west-1.amazonaws.com/fpm:centos8

RUN mkdir -p /target
WORKDIR /target

RUN yum install -y wget
RUN wget https://download.sonatype.com/nexus/3/latest-unix.tar.gz

RUN mkdir opt
RUN cd opt && tar xzvf ../latest-unix.tar.gz

RUN echo opt/nexus-* | cut -f 2 -d - | sed 's/.*/--version &/g' >.fpm
RUN echo opt/nexus-* | cut -f 3 -d - | sed 's/.*/--iteration &/g' >>.fpm

RUN mv opt/nexus-* opt/nexus
RUN fpm -s dir -t rpm --name nexus --depends nginx-crl --depends nfs-utils \
      --depends cosmos-ca-bundle-devs --depends cosmos-ca-bundle-staff \
      --depends cosmos-ca-bundle-services opt=/
