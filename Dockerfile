FROM alpine

COPY jams_finder /jams_finder
COPY requirements.txt /jams_finder
WORKDIR /jams_finder

RUN ls / &&\
    sed -i 's/dl-cdn.alpinelinux.org/mirrors.tuna.tsinghua.edu.cn/g' /etc/apk/repositories &&\
    apk update &&\
    apk add python3 &&\
    apk add py3-pip &&\
    pip3 install -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt

ENTRYPOINT ["python3", "main.py"]