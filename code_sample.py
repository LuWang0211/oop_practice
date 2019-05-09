
# Result should be : Example Domain

import socket

# open up a streaming byte connection to the host
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("www.example.org", 80))

# send three strings
s.send(b"GET / HTTP/1.1\r\n")
s.send(b"Host: www.example.com\r\n")
s.send(b"\r\n")

headbytes = []
while True:
    chunk = s.recv(1)
    headbytes.append( chunk )
    if b''.join( headbytes[-4:] ) == b'\r\n\r\n':
        break
head = b''.join(headbytes)

lines = head.split(b'\r\n')

status_line = lines[0]
header_lines = lines[1:]

headers = []
for line in header_lines:
    if len(line)==0:
        continue
    colon_index = line.index(b":")
    key = line[:colon_index]
    val = line[colon_index+2:]
    headers.append( (key,val) )
  
encoding = None
for key, val in headers:
    if key==b"Content-Type":
        charset_subkey = b"charset="
        charset_index = val.index( charset_subkey )
        encoding = val[charset_index+len(charset_subkey):].decode("ascii")
    elif key==b"Content-Length":
        content_length = int(val.decode("ascii"))
    
content_bytes = s.recv(content_length)
content = content_bytes.decode(encoding)

start_tag = "<title>"
end_tag = "</title>"
start_pos = content.index(start_tag)+len(start_tag)
end_pos = content.index(end_tag)

title = content[start_pos:end_pos]

print( title )
