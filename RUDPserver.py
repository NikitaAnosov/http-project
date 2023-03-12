import socket
import requests
import mimetypes
from urllib.parse import urlparse
from pathlib import Path

# Define additional file types
mimetypes.types_map['.pdf'] = 'application/pdf'
mimetypes.types_map['.zip'] = 'application/zip'
mimetypes.types_map['.docx'] = 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'


def download_file(url):
    parsed_url = urlparse(url)

    if not all([parsed_url.scheme, parsed_url.netloc]):
        return 'Please enter a valid URL'

    try:
        response = requests.get(url, stream=True)
        content_type = response.headers.get('Content-Type')

        extension = mimetypes.guess_extension(content_type)
        filename = 'file' + extension if extension else 'file'

        with open(filename, 'wb') as f:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)
                    f.flush()

        return f'Download complete. File saved as {filename}.'
    except Exception as e:
        return str(e)


# create a socket object
serversocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
print("Server listening... ")

# get local machine name
host = socket.gethostname()

port = 7878

# bind the socket to a public host, and a port
serversocket.bind((host, port))

while True:
    # receive URL from client
    url, client_address = serversocket.recvfrom(1024)
    print("Got a connection from %s" % str(client_address))

    # check if file already exists
    filename = 'file' + mimetypes.guess_extension(requests.head(url.decode('utf-8')).headers.get('Content-Type'))
    if Path(filename).exists():
        response = f'File {filename} already exists on the server.'
    else:
        # download file
        response = download_file(url.decode('utf-8'))

    # send response to client
    serversocket.sendto(response.encode('utf-8'), client_address)


