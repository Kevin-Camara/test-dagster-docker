from dagster import job, op

@op
def hello_dagster():
    print("Hello, Dagster!")

@job
def hello_world_pipeline():
    hello_dagster()
