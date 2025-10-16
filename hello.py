from dagster import op, job

@op
def hello_world():
    print("Hello, world!")

@job
def hello_job():
    hello_world()
