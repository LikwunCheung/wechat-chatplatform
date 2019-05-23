FROM python:3.7.3

RUN mkdir /code
WORKDIR /code
ADD . /code

RUN pip install -r requirement.txt

EXPOSE 8080
EXPOSE 8081

# dev
# CMD ["python","manage.py","runserver","--settings=wechat_chatplatform.settings.dev","0.0.0.0:8080"]

# prod
CMD ["python","manage.py","runserver","--settings=wechat_chatplatform.settings.product","0.0.0.0:8080"]
