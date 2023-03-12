import tkinter as tk
from tkinter import filedialog
import socket
import requests

# define function to initiate connection
def connect():
    # get inputs from GUI
    url = url_input.get()
    protocol = protocol_input.get()

    # get local machine name
    host = socket.gethostname()

    # define port numbers for TCP and RUDP
    tcp_port = 9898
    rudp_port = 7878

    # create a socket object for the chosen protocol
    if protocol.upper() == 'TCP':
        sock_type = socket.SOCK_STREAM
        port = tcp_port
    elif protocol.upper() == 'RUDP':
        sock_type = socket.SOCK_DGRAM
        port = rudp_port
    else:
        response_label.config(text='Invalid protocol choice')
        return

    clientsocket = socket.socket(socket.AF_INET, sock_type)

    # connect to the server
    clientsocket.connect((host, port))

    # send URL to server
    clientsocket.send(url.encode('utf-8'))

    # receive response from server
    response = clientsocket.recv(1024).decode('utf-8')

    # update GUI with response
    response_label.config(text=response)

    # close the socket
    clientsocket.close()

# create GUI
root = tk.Tk()
root.title('HTTP Downloader')

# set window size
root.geometry('400x200')

# create URL input field and label
url_label = tk.Label(root, text='URL:')
url_label.grid(row=0, column=0)
url_input = tk.Entry(root)
url_input.grid(row=0, column=1)

# create protocol input field and label
protocol_label = tk.Label(root, text='Protocol:')
protocol_label.grid(row=1, column=0)
protocol_input = tk.Entry(root)
protocol_input.grid(row=1, column=1)

# create button to initiate connection
connect_button = tk.Button(root, text='Connect', command=connect)
connect_button.grid(row=2, column=0, columnspan=2)

# create label for response
response_label = tk.Label(root, text='')
response_label.grid(row=3, column=0, columnspan=2)

root.mainloop()
