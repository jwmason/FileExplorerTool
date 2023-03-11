# Mason Wong
# masonjw1@uci.edu
# 48567424

"""THis module is in charge of communicating with the DSP server"""

import socket
import json
import ds_protocol


def true_or_false(resp, post):
    '''Returns True or False based on server response being ok or error.'''
    resp = json.loads(resp)
    send_return = ds_protocol.server_response(resp)
    if post == 'ERROR':
        send_return = False
    return send_return


def join(server, port, username, password, message, bio):
    '''Sends the join protocol to the server and receives json object
      with token from server.'''
    try:
        if server and port and username and password:
            json_msg = ds_protocol.join(username, password)
            return json_msg
    except TypeError:
        print('Not all parameters were given.')


def server_send_and_receive(client, msg):
    '''This sends the json object to the DSP Server.'''
    send = client.makefile('w')
    recv = client.makefile('r')

    msg = json.dumps(msg)

    send.write(msg)
    send.flush()

    resp = recv.readline()[:-1]

    return resp


def post_and_bio(message, bio, resp):
    '''Based on send function, returns user post or bio as json object
    if user token is recognized as previously logged user.'''
    if not (message == '' or message == ' ' or bio == '' or bio == ' '):
        if message and bio is None:
            token = ds_protocol.extract_json(resp)[0]
            json_msg2 = ds_protocol.post(message, token)
        elif bio is not None:
            token = ds_protocol.extract_json(resp)[0]
            json_msg2 = ds_protocol.bio(bio, token)
        else:
            return
        return json_msg2
    else:
        return 'ERROR'


def send(server: str, port: int, username: str, password: str,
         message: str, bio: str = None):
    '''
    The send function joins a ds server and sends a message, bio, or both

    :param server: The ip address for the ICS 32 DS server.
    :param port: The port where the ICS 32 DS server is accepting connections.
    :param username: The user name to be assigned to the message.
    :param password: The password associated with the username.
    :param message: The message to be sent to the server.
    :param bio: Optional, a bio for the user.
    '''
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((server, port))
    msg = join(server, port, username, password, message, bio)
    resp = server_send_and_receive(client, msg)
    print('\nServer Response:', resp)
    post = post_and_bio(message, bio, resp)
    t_or_f = true_or_false(resp, post)
    server_send_and_receive(client, post)
    client.close()
    return t_or_f
