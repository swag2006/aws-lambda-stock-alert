FROM public.ecr.aws/lambda/python:3.11

# Install dependencies as root
COPY requirements.txt ./
RUN pip install -r requirements.txt

# Copy your code and make it world‑readable
COPY lambda_function.py ./
RUN chmod 644 lambda_function.py


# (no USER directive needed—defaults will apply) test
CMD ["lambda_function.lambda_handler"]