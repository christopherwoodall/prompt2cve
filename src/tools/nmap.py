import subprocess
import shlex
from typing import List, Optional, Dict


def run_scan(
    target: str,
    ports: Optional[str] = None,
    scripts: Optional[List[str]] = None,
    arguments: Optional[str] = None,
    timeout: int = 60
) -> Dict[str, str]:
    """
    Runs an Nmap scan on the specified target with optional ports, NSE scripts, and arguments.

    Parameters:
        target (str): The IP address or hostname of the target system.
        ports (str, optional): Comma-separated list of ports or port ranges to scan (e.g., "80,443" or "1-1000").
        scripts (List[str], optional): A list of NSE scripts to include in the scan (e.g., ["http-title", "ssh-auth-methods"]).
        arguments (str, optional): Additional raw arguments to pass to Nmap (e.g., "-sV -Pn").
        timeout (int): Time in seconds before the scan is forcefully terminated.

    Returns:
        Dict[str, str]: A dictionary with two keys:
            - "stdout": The standard output from the Nmap scan.
            - "stderr": The standard error output, if any.

    Raises:
        ValueError: If the target is not provided or is empty.
        subprocess.TimeoutExpired: If the Nmap scan exceeds the timeout duration.
        subprocess.CalledProcessError: If Nmap exits with a non-zero status.
    """

    if not target.strip():
        raise ValueError("Target must be a non-empty string.")

    # Construct the base Nmap command
    cmd_parts = ["nmap", target]

    # Append port range if specified
    if ports:
        cmd_parts.extend(["-p", ports])

    # Append NSE scripts if provided
    if scripts:
        script_str = ",".join(scripts)
        cmd_parts.extend(["--script", script_str])

    # Append any additional arguments (e.g., -sV, -A)
    if arguments:
        cmd_parts.extend(shlex.split(arguments))

    # Run the command using subprocess and capture output
    try:
        result = subprocess.run(
            cmd_parts,
            capture_output=True,
            text=True,
            timeout=timeout,
            check=True
        )
        return {
            "stdout": result.stdout,
            "stderr": result.stderr
        }

    except subprocess.TimeoutExpired as e:
        raise subprocess.TimeoutExpired(cmd=e.cmd, timeout=e.timeout) from e

    except subprocess.CalledProcessError as e:
        raise subprocess.CalledProcessError(
            returncode=e.returncode,
            cmd=e.cmd,
            output=e.output,
            stderr=e.stderr
        ) from e
