import socket
class Connect:
    def __init__(self, website):
        self.website = website
    
    def title(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((self.website, 80))  

        # send three strings
        Host_string = "Host:" + self.website + "\r\n"
        print(Host_string)
        try:
            s.send(b"GET / HTTP/1.1\r\n")
            s.send(b'Host_string')
            s.send(b"\r\n")
            print('did it ')
        except:
            print('error')
        
        headbytes = []
        while True:
            chunk = s.recv(1)
            headbytes.append( chunk )
            if b''.join( headbytes[-4:] ) == b'\r\n\r\n':
                break
        head = b''.join(headbytes)

        print(head)
        lines = head.split(b'\r\n')
        # print(lines)
        status_line = lines[0]
        header_lines = lines[1:]headers = []
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
        print(headers)


a = Connect("www.example.org")
a.title()