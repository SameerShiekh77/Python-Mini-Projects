#!/usr/bin/env python3
"""
MySQL Connection Test Script
Tests connection to MySQL server and diagnoses common issues
"""

import socket
import time
import sys

# Configuration - Update these with your actual settings
DB_HOST = '' #update the host
DB_PORT = 3 #update the port
DB_USER = ''  # Update this
DB_PASSWORD = ''  # Update this
DB_NAME = ''  # Update this

def print_header(text):
    """Print a formatted header"""
    print(f"\n{'='*60}")
    print(f"  {text}")
    print('='*60)

def test_network_connectivity():
    """Test basic network connectivity to the MySQL server"""
    print_header("Test 1: Network Connectivity")
    
    try:
        print(f"Testing connection to {DB_HOST}:{DB_PORT}...")
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(10)
        
        start_time = time.time()
        result = sock.connect_ex((DB_HOST, DB_PORT))
        elapsed_time = time.time() - start_time
        
        sock.close()
        
        if result == 0:
            print(f"✓ SUCCESS: Port {DB_PORT} is open and accessible")
            print(f"  Connection time: {elapsed_time:.3f} seconds")
            return True
        else:
            print(f"✗ FAILED: Cannot connect to port {DB_PORT}")
            print(f"  Error code: {result}")
            print(f"\nPossible causes:")
            print(f"  - MySQL server is not running")
            print(f"  - Firewall blocking port {DB_PORT}")
            print(f"  - Wrong IP address or port")
            print(f"  - Network connectivity issues")
            return False
            
    except socket.timeout:
        print(f"✗ FAILED: Connection timeout after 10 seconds")
        print(f"\nPossible causes:")
        print(f"  - Firewall blocking the connection")
        print(f"  - Network routing issues")
        return False
    except socket.gaierror as e:
        print(f"✗ FAILED: Cannot resolve hostname")
        print(f"  Error: {e}")
        return False
    except Exception as e:
        print(f"✗ FAILED: Unexpected error: {e}")
        return False

def test_mysql_connection():
    """Test MySQL connection using MySQLdb"""
    print_header("Test 2: MySQL Connection")
    
    try:
        import MySQLdb
        print("✓ MySQLdb module is installed")
    except ImportError:
        print("✗ MySQLdb module not found")
        print("  Install it with: pip install mysqlclient")
        return False
    
    print(f"\nAttempting to connect to MySQL...")
    print(f"  Host: {DB_HOST}")
    print(f"  Port: {DB_PORT}")
    print(f"  User: {DB_USER}")
    print(f"  Database: {DB_NAME}")
    
    try:
        connection = MySQLdb.connect(
            host=DB_HOST,
            port=DB_PORT,
            user=DB_USER,
            passwd=DB_PASSWORD,
            db=DB_NAME,
            connect_timeout=10
        )
        
        cursor = connection.cursor()
        cursor.execute("SELECT VERSION()")
        version = cursor.fetchone()
        
        print(f"\n✓ SUCCESS: Connected to MySQL!")
        print(f"  MySQL Version: {version[0]}")
        
        cursor.close()
        connection.close()
        return True
        
    except MySQLdb.OperationalError as e:
        error_code, error_message = e.args
        print(f"\n✗ FAILED: MySQL Operational Error")
        print(f"  Error Code: {error_code}")
        print(f"  Error Message: {error_message}")
        
        if error_code == 2003:
            print(f"\n  This is the same error you're seeing in Django!")
            print(f"  Error 2003 means: Cannot connect to MySQL server")
        elif error_code == 1045:
            print(f"\n  Error 1045 means: Access denied (wrong credentials)")
        elif error_code == 2002:
            print(f"\n  Error 2002 means: Cannot connect via socket")
            
        return False
    except Exception as e:
        print(f"\n✗ FAILED: Unexpected error: {e}")
        return False

def test_dns_resolution():
    """Test DNS resolution if hostname is used"""
    print_header("Test 3: DNS Resolution")
    
    try:
        ip_address = socket.gethostbyname(DB_HOST)
        print(f"✓ Hostname resolves to: {ip_address}")
        return True
    except socket.gaierror:
        print(f"  {DB_HOST} is already an IP address (no DNS needed)")
        return True

def test_ping():
    """Test ICMP ping to the server"""
    print_header("Test 4: ICMP Ping Test")
    
    import subprocess
    import platform
    
    # Determine ping command based on OS
    param = '-n' if platform.system().lower() == 'windows' else '-c'
    command = ['ping', param, '4', DB_HOST]
    
    try:
        print(f"Pinging {DB_HOST}...")
        result = subprocess.run(command, capture_output=True, text=True, timeout=15)
        
        if result.returncode == 0:
            print("✓ Host is reachable via ICMP")
            # Show some output
            for line in result.stdout.split('\n')[:5]:
                if line.strip():
                    print(f"  {line}")
            return True
        else:
            print("✗ Host is not reachable via ICMP")
            print("  Note: Some servers block ICMP, this doesn't mean they're down")
            return False
    except subprocess.TimeoutExpired:
        print("✗ Ping timeout")
        return False
    except Exception as e:
        print(f"✗ Ping test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("\n" + "="*60)
    print("  MySQL Connection Diagnostic Script")
    print("="*60)
    print(f"\nTarget: {DB_HOST}:{DB_PORT}")
    print(f"Time: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Run tests
    dns_ok = test_dns_resolution()
    ping_ok = test_ping()
    network_ok = test_network_connectivity()
    mysql_ok = test_mysql_connection()
    
    # Summary
    print_header("Summary")
    print(f"DNS Resolution:       {'✓ PASS' if dns_ok else '✗ FAIL'}")
    print(f"ICMP Ping:            {'✓ PASS' if ping_ok else '✗ FAIL (may be blocked)'}")
    print(f"Network Connectivity: {'✓ PASS' if network_ok else '✗ FAIL'}")
    print(f"MySQL Connection:     {'✓ PASS' if mysql_ok else '✗ FAIL'}")
    
    if mysql_ok:
        print("\n✓ All tests passed! Your Django app should be able to connect.")
    elif network_ok and not mysql_ok:
        print("\n⚠ Network is OK but MySQL connection failed.")
        print("  Check your MySQL credentials and permissions.")
    else:
        print("\n✗ Cannot reach the MySQL server.")
        print("\nTroubleshooting steps:")
        print("  1. Verify the IP address is correct: 82.180.152.1")
        print("  2. Check if MySQL is running on the remote server")
        print("  3. Verify firewall rules allow port 3306")
        print("  4. Check if your IP is whitelisted on the MySQL server")
        print("  5. Verify network connectivity between servers")
    
    print("\n" + "="*60 + "\n")

if __name__ == "__main__":
    main()
