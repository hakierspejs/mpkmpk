FROM python
ADD ./requirements.txt .
RUN pip install -r requirements.txt
EXPOSE 5000
ADD ./main.py .
ADD ./templates templates
CMD ./main.py
