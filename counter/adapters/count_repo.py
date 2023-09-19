from typing import List

from pymongo import MongoClient
import psycopg2
from psycopg2 import Error

from counter.domain.models import ObjectCount
from counter.domain.ports import ObjectCountRepo


class CountInMemoryRepo(ObjectCountRepo):

    def __init__(self):
        self.store = dict()

    def read_values(self, object_classes: List[str] = None) -> List[ObjectCount]:
        if object_classes is None:
            return list(self.store.values())

        return [self.store.get(object_class) for object_class in object_classes]

    def update_values(self, new_values: List[ObjectCount]):
        for new_object_count in new_values:
            key = new_object_count.object_class
            try:
                stored_object_count = self.store[key]
                self.store[key] = ObjectCount(key, stored_object_count.count + new_object_count.count)
            except KeyError:
                self.store[key] = ObjectCount(key, new_object_count.count)


class CountMongoDBRepo(ObjectCountRepo):

    def __init__(self, host, port, database):
        self.__host = host
        self.__port = port
        self.__database = database

    def __get_counter_col(self):
        client = MongoClient(self.__host, self.__port)
        db = client[self.__database]
        counter_col = db.counter
        return counter_col

    def read_values(self, object_classes: List[str] = None) -> List[ObjectCount]:
        counter_col = self.__get_counter_col()
        query = {"object_class": {"$in": object_classes}} if object_classes else None
        counters = counter_col.find(query)
        object_counts = []
        for counter in counters:
            object_counts.append(ObjectCount(counter['object_class'], counter['count']))
        return object_counts

    def update_values(self, new_values: List[ObjectCount]):
        counter_col = self.__get_counter_col()
        for value in new_values:
            counter_col.update_one({'object_class': value.object_class}, {'$inc': {'count': value.count}}, upsert=True)


class CountPostgresDBRepo(ObjectCountRepo):
    def __init__(self, database, user, password, host, port):
        self._database = database
        self._user = user
        self._password = password
        self._host = host
        self._port = port
        self._connection = None

    def connect(self):
        try:
            self._connection = psycopg2.connect(
                database=self._database,
                user=self._user,
                password=self._password,
                host=self._host,
                port=self._port
            )
            print("Connected to the PostgreSQL database successfully")
        except (Exception, Error) as error:
            print("Error while connecting to PostgreSQL", error)

    def disconnect(self):
        if self._connection:
            self._connection.close()
            print("Disconnected from the PostgreSQL database")

    def update_values(self, new_values: List[ObjectCount]):
        try:
            self.connect()
            cursor = self._connection.cursor()
            create_query = """create table if not exists counter(
            object_class TEXT UNIQUE,
            count INT
            );"""
            cursor.execute(create_query)
            requested_cls = [rec.object_class for rec in new_values]
            req_cls_str = "','".join(requested_cls)
            check_query = f"""
                select object_class from counter where object_class in ('{req_cls_str}');
            """
            cursor.execute(check_query)

            rows = cursor.fetchall()
            print(rows)
            already_exists = []
            
            for row in rows:
                if row[0] in requested_cls:
                    already_exists.append(row[0])

            already_exists_str = "','".join(already_exists)

            data = ""
            update_data = ""
            for rec in new_values:
                if rec.object_class in already_exists:
                    update_data += f"WHEN '{rec.object_class}' THEN count+{rec.count} "
                else:
                    data += f"('{rec.object_class}',{rec.count}),"
            

            if data:
                data = data[:-1]
                create_query = f"""insert into counter (object_class,count) values {data}"""
                print(create_query)
                cursor.execute(create_query)
            
            if update_data:
                update_query = f"""
                UPDATE counter
                SET count 
                = CASE object_class
                {update_data}
                END
                WHERE object_class IN('{already_exists_str}');
                """
                cursor.execute(update_query)
                
            
            self._connection.commit()
            print("Query executed successfully")
            self.disconnect()
        except (Exception, Error) as error:
            print("Error executing query:", error)

    def read_values(self, object_classes: List[str] = None) -> List[ObjectCount]:
        try:
            self.connect()
            cursor = self._connection.cursor()
            if object_classes:
                object_cls_str = "','".join(object_classes)
                query = f"select * from counter where object_class in ('{object_cls_str}')"
                cursor.execute(query)
            else:
                query = "select * from counter"
                cursor.execute(query)
            
            rows = cursor.fetchall()
            print(rows)
            result = []
            column_names = [desc[0] for desc in cursor.description]
            for row in rows:
                result.append(dict(zip(column_names, row)))
            self.disconnect()
            return result
        except (Exception, Error) as error:
            print("Error fetching data:", error)


# Usage example
if __name__ == "__main__":
    # Replace these with your actual database credentials
    dbname = "your_db_name"
    user = "your_db_user"
    password = "your_db_password"
    host = "your_db_host"
    port = "your_db_port"

    db_handler = DatabaseHandler(dbname, user, password, host, port)
    db_handler.connect()

    # Example query execution
    query = "INSERT INTO table_name (column1, column2) VALUES (%s, %s)"
    params = ('value1', 'value2')
    db_handler.execute_query(query, params)

    # Example data fetching
    select_query = "SELECT * FROM table_name"
    rows = db_handler.fetch_data(select_query)
    print("Fetched Data:", rows)

    db_handler.disconnect()
