#!/usr/bin/env python3
"""
OtterStax CLI Client - универсальный клиент для работы с OtterStax
Поддерживает: MySQL и PostgreSQL протоколы, локальный сервер, Docker, Kubernetes
"""

import argparse
import json
import os
import subprocess
import sys
from contextlib import contextmanager
from typing import Any, Dict, List, Optional, Tuple

# MySQL drivers
try:
    import pymysql
except ImportError:
    pymysql = None

try:
    import mysql.connector
except ImportError:
    mysql = None

# PostgreSQL driver
try:
    import psycopg2
except ImportError:
    psycopg2 = None


class OtterStaxConfig:
    """Конфигурация подключения к OtterStax"""

    DEFAULT_CONFIG_PATH = os.path.expanduser("~/.otterstax/config.json")

    def __init__(self):
        self.config = self._load_config()

    def _load_config(self) -> Dict[str, Any]:
        """Загрузка конфигурации из файла"""
        if os.path.exists(self.DEFAULT_CONFIG_PATH):
            with open(self.DEFAULT_CONFIG_PATH, "r") as f:
                return json.load(f)
        return self._default_config()

    def _default_config(self) -> Dict[str, Any]:
        return {
            "environments": {
                "local": {
                    "host": "0.0.0.0",
                    "mysql_port": 8816,
                    "postgres_port": 5432,
                    "http_port": 8085,
                    "user": "testuser",
                    "password": "testpass",
                },
                "docker": {
                    "host": "localhost",
                    "mysql_port": 8816,
                    "postgres_port": 5432,
                    "http_port": 8085,
                    "user": "testuser",
                    "password": "testpass",
                    "container": "otterstax",
                },
                "k8s": {
                    "namespace": "otterstax",
                    "service": "otterstax-server",
                    "mysql_port": 8816,
                    "postgres_port": 5432,
                    "http_port": 8085,
                    "user": "testuser",
                    "password": "testpass",
                },
            },
            "current_environment": "local",
            "protocol": "mysql",
            "data_sources": [],
        }

    def save(self):
        """Сохранение конфигурации"""
        os.makedirs(os.path.dirname(self.DEFAULT_CONFIG_PATH), exist_ok=True)
        with open(self.DEFAULT_CONFIG_PATH, "w") as f:
            json.dump(self.config, f, indent=2)

    def get_current_env(self) -> Dict[str, Any]:
        """Получить текущее окружение"""
        env_name = self.config.get("current_environment", "local")
        return self.config["environments"].get(
            env_name, self.config["environments"]["local"]
        )

    def set_environment(self, env: str):
        """Установить текущее окружение"""
        if env in self.config["environments"]:
            self.config["current_environment"] = env
            self.save()
        else:
            raise ValueError(f"Unknown environment: {env}")

    def get_protocol(self) -> str:
        """Получить текущий протокол"""
        return self.config.get("protocol", "mysql")

    def set_protocol(self, protocol: str):
        """Установить протокол (mysql или postgres)"""
        if protocol in ["mysql", "postgres", "postgresql"]:
            self.config["protocol"] = (
                "postgres" if protocol == "postgresql" else protocol
            )
            self.save()
        else:
            raise ValueError(f"Unknown protocol: {protocol}. Use 'mysql' or 'postgres'")


class OtterStaxClient:
    """Клиент для работы с OtterStax"""

    def __init__(
        self, config: Optional[OtterStaxConfig] = None, protocol: Optional[str] = None
    ):
        self.config = config or OtterStaxConfig()
        self.protocol = protocol or self.config.get_protocol()
        self.connection = None

    def _get_connection_params(self) -> Dict[str, Any]:
        """Получить параметры подключения в зависимости от окружения и протокола"""
        env = self.config.get_current_env()
        env_name = self.config.config.get("current_environment", "local")

        if env_name == "k8s":
            host = "127.0.0.1"
        else:
            host = env.get("host", "0.0.0.0")

        if self.protocol == "postgres":
            return {
                "host": host,
                "port": env.get("postgres_port", 5432),
                "user": env.get("user", "testuser"),
                "password": env.get("password", "testpass"),
                "dbname": env.get("database", "postgres"),
            }
        else:
            return {
                "host": host,
                "port": env.get("mysql_port", 8816),
                "user": env.get("user", "testuser"),
                "password": env.get("password", "testpass"),
            }

    @contextmanager
    def connect(self):
        """Контекстный менеджер для подключения"""
        params = self._get_connection_params()
        conn = None

        try:
            if self.protocol == "postgres":
                if psycopg2:
                    conn = psycopg2.connect(**params)
                else:
                    raise ImportError(
                        "PostgreSQL driver not found. Install psycopg2-binary"
                    )
            else:
                if pymysql:
                    conn = pymysql.connect(**params)
                elif mysql:
                    conn = mysql.connector.connect(**params)
                else:
                    raise ImportError(
                        "MySQL driver not found. Install pymysql or mysql-connector-python"
                    )

            yield conn
        finally:
            if conn:
                conn.close()

    def execute_query(
        self, query: str, params: tuple = None
    ) -> Tuple[List[Dict], List[str]]:
        """Выполнить SQL запрос и вернуть результаты"""
        with self.connect() as conn:
            cursor = conn.cursor()

            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)

            query_upper = query.strip().upper()

            if (
                query_upper.startswith("SELECT")
                or query_upper.startswith("SHOW")
                or query_upper.startswith("DESCRIBE")
                or query_upper.startswith("\\D")
            ):
                columns = (
                    [desc[0] for desc in cursor.description]
                    if cursor.description
                    else []
                )
                rows = cursor.fetchall()

                results = []
                for row in rows:
                    results.append(dict(zip(columns, row)))

                return results, columns
            else:
                affected = cursor.rowcount
                conn.commit()
                return [{"affected_rows": affected}], ["affected_rows"]

    def test_connection(self) -> bool:
        """Проверить подключение"""
        try:
            with self.connect() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT 1")
                return True
        except Exception as e:
            print(f"Connection failed: {e}", file=sys.stderr)
            return False

    def add_data_source(
        self,
        alias: str,
        host: str,
        port: int,
        username: str,
        password: str,
        database: str,
    ) -> bool:
        """Добавить источник данных через HTTP API"""
        import urllib.error
        import urllib.request

        env = self.config.get_current_env()
        http_port = env.get("http_port", 8085)
        http_host = env.get("host", "0.0.0.0")

        url = f"http://{http_host}:{http_port}/add_connection"

        data = {
            "alias": alias,
            "host": host,
            "port": str(port),
            "username": username,
            "password": password,
            "database": database,
            "table": "",
        }

        try:
            req = urllib.request.Request(
                url,
                data=json.dumps(data).encode("utf-8"),
                headers={"Content-Type": "application/json"},
            )
            with urllib.request.urlopen(req, timeout=10) as response:
                return response.status == 200
        except urllib.error.URLError as e:
            print(f"Failed to add data source: {e}", file=sys.stderr)
            return False

    def get_schema(self, database: str = None, table: str = None) -> List[Dict]:
        """Получить схему БД/таблицы"""
        if self.protocol == "postgres":
            if table and database:
                query = f"SELECT column_name, data_type, is_nullable FROM information_schema.columns WHERE table_schema || '.' || table_name = '{database}.{table}'"
            elif database:
                query = f"SELECT table_name FROM information_schema.tables WHERE table_schema = '{database}'"
            else:
                query = "SELECT schema_name FROM information_schema.schemata"
        else:
            if table and database:
                query = f"DESCRIBE {database}.{table}"
            elif database:
                query = f"SHOW TABLES FROM {database}"
            else:
                query = "SHOW DATABASES"

        results, _ = self.execute_query(query)
        return results


class K8sPortForward:
    """Менеджер port-forward для Kubernetes"""

    def __init__(self, namespace: str, service: str, local_port: int, remote_port: int):
        self.namespace = namespace
        self.service = service
        self.local_port = local_port
        self.remote_port = remote_port
        self.process = None

    def start(self):
        """Запустить port-forward"""
        cmd = [
            "kubectl",
            "port-forward",
            "-n",
            self.namespace,
            f"svc/{self.service}",
            f"{self.local_port}:{self.remote_port}",
        ]

        self.process = subprocess.Popen(
            cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )

        import time

        time.sleep(2)

        if self.process.poll() is not None:
            _, stderr = self.process.communicate()
            raise RuntimeError(f"Failed to start port-forward: {stderr.decode()}")

    def stop(self):
        """Остановить port-forward"""
        if self.process:
            self.process.terminate()
            self.process.wait()


def format_table(results: List[Dict], columns: List[str]) -> str:
    """Форматирование результатов в таблицу"""
    if not results:
        return "No results"

    widths = {col: len(col) for col in columns}
    for row in results:
        for col in columns:
            val = str(row.get(col, ""))
            widths[col] = max(widths[col], len(val))

    lines = []

    header = " | ".join(col.ljust(widths[col]) for col in columns)
    separator = "-+-".join("-" * widths[col] for col in columns)

    lines.append(header)
    lines.append(separator)

    for row in results:
        line = " | ".join(str(row.get(col, "")).ljust(widths[col]) for col in columns)
        lines.append(line)

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="OtterStax CLI Client")
    parser.add_argument(
        "--protocol",
        "-p",
        choices=["mysql", "postgres"],
        help="Protocol to use (mysql or postgres)",
    )
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # connect
    connect_parser = subparsers.add_parser(
        "connect", help="Test connection to OtterStax"
    )
    connect_parser.add_argument(
        "--env", choices=["local", "docker", "k8s"], help="Environment to use"
    )

    # query
    query_parser = subparsers.add_parser("query", help="Execute SQL query")
    query_parser.add_argument("sql", help="SQL query to execute")
    query_parser.add_argument(
        "--format",
        choices=["table", "json", "csv"],
        default="table",
        help="Output format",
    )

    # schema
    schema_parser = subparsers.add_parser("schema", help="Show database schema")
    schema_parser.add_argument("--database", "-d", help="Database name")
    schema_parser.add_argument("--table", "-t", help="Table name")

    # add-source
    source_parser = subparsers.add_parser("add-source", help="Add data source")
    source_parser.add_argument(
        "--alias", required=True, help="Alias for the data source"
    )
    source_parser.add_argument("--host", required=True, help="Host address")
    source_parser.add_argument("--port", type=int, required=True, help="Port number")
    source_parser.add_argument("--user", required=True, help="Username")
    source_parser.add_argument("--password", required=True, help="Password")
    source_parser.add_argument("--database", required=True, help="Database name")

    # env
    env_parser = subparsers.add_parser("env", help="Manage environments")
    env_parser.add_argument("action", choices=["list", "set", "show"])
    env_parser.add_argument("name", nargs="?", help="Environment name for 'set' action")

    # protocol
    protocol_parser = subparsers.add_parser("protocol", help="Manage protocol")
    protocol_parser.add_argument("action", choices=["show", "set"])
    protocol_parser.add_argument(
        "name",
        nargs="?",
        choices=["mysql", "postgres"],
        help="Protocol name for 'set' action",
    )

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return 1

    config = OtterStaxConfig()
    protocol = args.protocol if hasattr(args, "protocol") and args.protocol else None
    client = OtterStaxClient(config, protocol=protocol)

    if args.command == "connect":
        if args.env:
            config.set_environment(args.env)

        protocol_name = client.protocol.upper()
        if client.test_connection():
            print(
                f"Successfully connected to OtterStax via {protocol_name} ({config.config['current_environment']})"
            )
            return 0
        else:
            print(f"Connection failed via {protocol_name}", file=sys.stderr)
            return 1

    elif args.command == "query":
        try:
            results, columns = client.execute_query(args.sql)

            if args.format == "json":
                print(json.dumps(results, indent=2, default=str))
            elif args.format == "csv":
                if columns:
                    print(",".join(columns))
                    for row in results:
                        print(",".join(str(row.get(col, "")) for col in columns))
            else:
                print(format_table(results, columns))

            return 0
        except Exception as e:
            print(f"Query failed: {e}", file=sys.stderr)
            return 1

    elif args.command == "schema":
        try:
            results = client.get_schema(args.database, args.table)
            print(json.dumps(results, indent=2, default=str))
            return 0
        except Exception as e:
            print(f"Failed to get schema: {e}", file=sys.stderr)
            return 1

    elif args.command == "add-source":
        if client.add_data_source(
            args.alias, args.host, args.port, args.user, args.password, args.database
        ):
            print(f"Data source '{args.alias}' added successfully")
            return 0
        else:
            print("Failed to add data source", file=sys.stderr)
            return 1

    elif args.command == "env":
        if args.action == "list":
            for env_name in config.config["environments"]:
                marker = (
                    "*" if env_name == config.config["current_environment"] else " "
                )
                print(f"{marker} {env_name}")
        elif args.action == "set":
            if not args.name:
                print("Environment name required", file=sys.stderr)
                return 1
            config.set_environment(args.name)
            print(f"Environment set to: {args.name}")
        elif args.action == "show":
            env = config.get_current_env()
            print(json.dumps(env, indent=2))
        return 0

    elif args.command == "protocol":
        if args.action == "show":
            print(f"Current protocol: {config.get_protocol()}")
        elif args.action == "set":
            if not args.name:
                print("Protocol name required (mysql or postgres)", file=sys.stderr)
                return 1
            config.set_protocol(args.name)
            print(f"Protocol set to: {args.name}")
        return 0

    return 0


if __name__ == "__main__":
    sys.exit(main())
