# Network-infra-kafka

카프카 도커에 메인 잡고

도커 컴포즈 올림

해당하는 포트 다 개방해주고

server.properties.sh 수정해서 advtise쪽에 브로커 아이피 박기

---

토픽생성
sudo bin/kafka-topics.sh --create --bootstrap-server <NUC IP>:9092 --replication-factor 1 --partitions 1 --topic {topic_name}
토픽목록
kafka-topics.sh --list --bootstrap-server 10.32.103.147:9092

---

라즈베리파이 세팅법

미러서버 - (http|rsync)://ftp.jaist.ac.jp/pub/Linux/raspbian-archive/raspbian
sudo nano /etc/apt/sources.list

라이브러리

sudo apt install -y vim

sudo apt install -y python3-pip

sudo apt install -y default-jdk # 카프카 사용을 위한 것

sudo pip3 install kafka-python

wget http://archive.apache. org/dist/kafka/2.8.0/kafka_2.12-2.8.0.tgz
