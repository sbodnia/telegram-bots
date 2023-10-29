FROM python:3.9.18-slim
# set work directory
WORKDIR /usr/src/app/
# copy project
COPY . /usr/src/app/
# install dependencies
RUN pip install telebot
# run app
CMD ["python", "main.py"]