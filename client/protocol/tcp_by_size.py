__author__ = 'Yossi'

# from  tcp_by_size import send_with_size ,recv_by_size

SIZE_HEADER_FORMAT = "00000000~" # n digits for data size + one delimiter
size_header_size = len(SIZE_HEADER_FORMAT)
TCP_DEBUG = True
LEN_TO_PRINT = 100

VER = 'Python3'

# function to convert a string to bytes or vice versa, depending on the direction argument
def str_byte(_s, direction):
    """
    Convert a string to bytes or vice versa, depending on the direction argument.

    Args:
        _s (str or bytes): The input string or bytes object.
        direction (str): The direction of the conversion. Should be either 'encode' or 'decode'.

    Returns:
        bytes or str: The converted bytes or string object.
    """
    if VER == 'Python3':
        if direction == 'encode':
            return _s.encode()
        else:
            return _s.decode('utf8')
    else:
        return _s


# function to receive data from a socket, where the size of the data is indicated by a header
def recv_by_size(sock):
    """
    Receive data from a socket, where the size of the data is indicated by a header.

    Args:
        sock (socket.socket): The socket to receive data from.

    Returns:
        bytes: The received data.
    """
    size_header = b''
    data_len = 0
    # receive the size header
    while len(size_header) < size_header_size:
        _s = sock.recv(size_header_size - len(size_header))
        if _s == b'':
            size_header = b''
            break
        size_header += _s
    data  = b''
    # receive the data
    if size_header != b'':
        data_len = int(size_header[:size_header_size - 1])
        while len(data) < data_len:
            _d = sock.recv(data_len - len(data))
            if _d == b'':
                data  = b''
                break
            data += _d

    # if the length of the received data doesn't match the expected length, treat it as if no data was received
    if data_len != len(data):
        data=b'' # Partial data is like no data !

    # print debug message
    if  TCP_DEBUG and  data_len > 0:
        print ("\nRecv(%s)>>>" % (data_len,), end='')
        print ("%s"%(data[:min(len(data),LEN_TO_PRINT)],))

    return data


# function to send data over a socket, where the size of the data is indicated by a header
def send_with_size(sock, bdata):
    """
    Send data over a socket, where the size of the data is indicated by a header.

    Args:
        sock (socket.socket): The socket to send data over.
        bdata (bytes): The data to send, as a bytes object.

    Returns:
        None
    """
    len_data = len(bdata)
    header_data = str(len(bdata)).zfill(size_header_size - 1) + "~"

    # combine the header and data into a single bytearray and send it
    bytea = bytearray(header_data, encoding='utf8') + bdata
    sock.send(bytea)

    # print debug message
    if  TCP_DEBUG and  len_data > 0:
        print ("\nSent(%s)>>>" % (len_data,), end='')
        print ("%s"%(bytea[:min(len(bytea),LEN_TO_PRINT)],))