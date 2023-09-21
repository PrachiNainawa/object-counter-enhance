import os

from counter.adapters.count_repo import CountMongoDBRepo, CountInMemoryRepo, CountPostgresDBRepo
from counter.adapters.object_detector import TFSObjectDetector, FakeObjectDetector
from counter.domain.actions import CountDetectedObjects


def dev_mongo_count_action() -> CountDetectedObjects:
    return CountDetectedObjects(FakeObjectDetector(), CountInMemoryRepo())


def dev_postgres_count_action() -> CountDetectedObjects:
    return CountDetectedObjects(FakeObjectDetector(), CountInMemoryRepo())


def prod_mongo_count_action() -> CountDetectedObjects:
    tfs_host = os.environ.get('TFS_HOST', 'localhost')
    tfs_port = os.environ.get('TFS_PORT', 8501)
    mongo_host = os.environ.get('MONGO_HOST', 'localhost')
    mongo_port = os.environ.get('MONGO_PORT', 27017)
    mongo_db = os.environ.get('MONGO_DB', 'prod_counter')
    return CountDetectedObjects(TFSObjectDetector(tfs_host, tfs_port, os.environ.get('MODEL_NAME','rfcn')),
                                CountMongoDBRepo(host=mongo_host, port=mongo_port, database=mongo_db))


def prod_postgres_count_action() -> CountDetectedObjects:
    tfs_host = os.environ.get('TFS_HOST', 'localhost')
    tfs_port = os.environ.get('TFS_PORT', 8501)
    postgres_host = os.environ.get('POSTGRES_HOST', 'localhost')
    postgres_port = os.environ.get('POSTGRES_PORT', 5432)
    postgres_db = os.environ.get('POSTGRES_DB', 'prod_counter')
    postgres_pswd = os.environ.get('POSTGRES_PASSWORD', 'mypassword')
    postgres_user = os.environ.get('POSTGRES_USER', 'myuser')

    return CountDetectedObjects(TFSObjectDetector(tfs_host, tfs_port, os.environ.get('MODEL_NAME','rfcn')),
                                CountPostgresDBRepo(host=postgres_host, port=postgres_port, database=postgres_db, password=postgres_pswd, user=postgres_user))


def get_count_action() -> CountDetectedObjects:
    env = os.environ.get('ENV', 'dev')
    db = os.environ.get('DB','mongo')
    count_action_fn = f"{env}_{db}_count_action"
    print("count_action_fn",count_action_fn)
    return globals()[count_action_fn]()
