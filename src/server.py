from tools import nmap, service

from mcp.server.fastmcp import FastMCP


mcp = FastMCP("Prompt 2 CVE")


@mcp.tool()
def network_scan(ip_address: str, ports: str = None, scripts: list = None, arguments: str = None) -> dict:
  """
  Perform a network scan using Nmap.

  Args:
      ip_address (str): The target IP address or hostname.
      ports (str, optional): Comma-separated list of ports to scan (e.g., "80,443").
      scripts (list, optional): List of NSE scripts to run.
      arguments (str, optional): Additional Nmap arguments.

  Returns:
      dict: A dictionary containing the scan results.
  """
  return nmap.run_scan(ip_address, ports, scripts, arguments)

@mcp.tool()
def service_scan(server: str, port: int, target_file: str) -> str:
  """
  Lookup the target file on the server.

  Args:
      server (str): The server address.
      port (int): The server port.
      target_file (str): The target file to look up.

  Returns:
      str: The response from the server.
  """
  return service.lookup(server, port, target_file)


def main():
  mcp.run(transport="stdio")


if __name__ == "__main__":
  mcp.run(transport="stdio")
