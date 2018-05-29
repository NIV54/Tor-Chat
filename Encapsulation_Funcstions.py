from Classes import *
import json


def encapsulate_message(msg_txt, keys, path, end_address, num_of_layers, cur_layer=1):
    """Handles the creation of an encapsulated message, each layer is being encrypted individually
    from the last layer to the last. This function is recursive.
    :param keys = type list of strings, the key of each node in the way, first node first.
    :param path = type list of tuples, each place is an address of a node, in order of the chosen path by the dir server
    :param end_address = type tuple, the ip and port of communication with the end user
    :param cur_layer = type int, lets the function to know when the last layer is being handled (different from the others)
    """
    encoder = AESCipher(keys[0])
    if cur_layer == num_of_layers:
        next_layer = None
        next_address = end_address
        next_msg = msg_txt
    else:
        next_layer = encapsulate_message(msg_txt, keys[1:], path[1:], end_address, num_of_layers, cur_layer + 1)
        next_address = path[1]
        next_msg = ""

    layer = json.dumps(DataLayer(next_layer, next_address, next_msg).__dict__)
    return encoder.encrypt(layer)


def decapsulate(key, encoded_data):
    """Handles the decapsulation of one layer with a given key to decapsulate
    :return decapsulated data after json load"""
    decoder = AESCipher(key)
    decoded_data = decoder.decrypt(encoded_data)
    json_loaded_data = json.loads(decoded_data)
    return json_loaded_data
