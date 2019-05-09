import socket

class Connect:
    def __init__(self, website, port=80, path="/"):
            self.website = website
            self.port = port
            self.path = path

            self.encoding = None
            self.content_length = None
            self.content = None
    
    # get http response
    # https://docs.python.org/3/library/socket.html#socket.AF_UNIX
    def get_response(self):
        # Connect to a remote socket at address
        # socket.conect(address), address
        self.sample = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
        self.sample.connect((self.website, self.port))

        # send three strings
        get_command = f"GET {self.path} HTTP/1.1\r\n"
        Host_string = f"Host: {self.website}:{self.port} \r\n"
        try:
            self.sample.send(get_command.encode("ascii"))
            self.sample.send(Host_string.encode("ascii"))
            self.sample.send(b"\r\n")
            # print('Sending server request successful ')
        except Exception as e:
            raise e

    # read http response header, get 'encoding' and 'Content-Length'
    def read_header(self):

        headbytes = []
        while True:
            chunk = self.sample.recv(1)
            headbytes.append( chunk )
            if b''.join( headbytes[-4:] ) == b'\r\n\r\n':
                break
        head = b''.join(headbytes)
        # print(head.encode("ascii"))
        lines = head.split(b'\r\n')
        # print(lines.encode("ascii"))

        # response
        status_line = lines[0]
        # header
        header_lines = lines[1:]

        headers = []
        # headers_dict = {}
        for line in header_lines:
            if len(line)==0:
                continue
            colon_index = line.index(b":")
            key = line[:colon_index]
            val = line[colon_index+2:]
            headers.append( (key,val) )
            # headers_dict[key] = val
        # print(headers_dict.encode("ascii"))
        
        # get 'encoding' and 'Content-Length'
        # headers_dict = {}
        for key, val in headers:
            if key==b"Content-Type":
                charset_subkey = b"charset="
                # charset_index = val.index( charset_subkey )
                # self.encoding = val[charset_index+len(charset_subkey):].decode("ascii")
                try:
                    charset_index = val.index( charset_subkey )
                    self.encoding = val[charset_index+len(charset_subkey):].decode("ascii")
                except Exception:
                    self.encoding = "ascii"
            elif key==b"Content-Length":
                content_length = int(val.decode("ascii"))
                self.content_length = content_length
            # headers_dict[key] = val

    def read_body(self):
        content_bytes = self.sample.recv(self.content_length)
        self.content = content_bytes.decode(self.encoding)
        # print(self.content)

    def title(self):
        self.get_response()
        self.read_header()
        self.read_body()

        start_title_position = self.content.index("<title>") # "<title>" len = 7
        end_title_position = self.content.index("</title>")

        extraction = self.content[(start_title_position + 7):end_title_position]
        # start_tag = "<title>"
        # end_tag = "</title>"
        # start_pos = content.index(start_tag)+len(start_tag)
        # end_pos = content.index(end_tag)
        # title = content[start_pos:end_pos]

        return extraction

# test case
test_0 = Connect("www.example.org")
print(test_0.title())

test_1 = Connect("www.columbia.edu", 80, "/~fdc/sample.html")
print(test_1.title())
