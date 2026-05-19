import pymysql


def create_connection():
    try:
        connection = pymysql.connect(
            host="rm-xxx.mysql.rds.aliyuncs.com",  # 数据库主机地址
            user="rxxx_u",  # 数据库用户名
            password="xxx@xxxx",  # 数据库密码
            db="xxxxx",  # 数据库名
        )
        return connection
    except pymysql.MySQLError as e:
        print(f"Error connecting to MySQL Platform: {e}")
        return None


def execute_query(connection, query):
    try:
        with connection.cursor() as cursor:
            cursor.execute(query)
        connection.commit()
        print("Update was successful.")
    except pymysql.MySQLError as e:
        print(f"Error executing query: {e}")


def main():
    query = "UPDATE meteorological_risk_results SET assessed_value=0.00,loss_rate=0,payout_ratio=0,risk_level_code='RISK_LEVEL_04' \
            WHERE evaluation_type_code='RISK_ASSESSMENT_TYPE_04' AND evaluation_time > '2025-03-01' AND assessed_value >= 0.25; "
    connection = create_connection()
    if connection:
        execute_query(connection, query)
        connection.close()

    update = "UPDATE meteorological_disaster_risk_results SET risk_level_code='METEOROLOGICAL_RISK_LEVEL_01_01' ,assessed_value=0.00 \
            WHERE evaluation_type_code='METEOROLOGICAL_HAZARD_INDEX_01' AND evaluation_time > '2025-03-01' ; "
    connection = create_connection()
    if connection:
        execute_query(connection, update)
        connection.close()


if __name__ == "__main__":
    main()
