import sys
import socket
import os
import math

SIZE = 256


def file_sending(file, socket):
    size_of_file = os.path.getsize(file)
    number_of_iterations = math.floor(size_of_file/SIZE)

    with open(file, 'rb') as f:
        byte = f.read(SIZE)
        i = 0
        while byte:
            socket.send(byte)
            byte = f.read(SIZE)
            print_progress_bar(i, number_of_iterations)
            i += 1
        socket.close()
        print("File has been sent!")


# Source: https://stackoverflow.com/questions/3173320/text-progress-bar-in-the-console
def print_progress_bar(iteration, total, prefix='', suffix='', decimals=1, length=100, fill='█'):
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filled_length = int(length * iteration // total)
    bar = fill * filled_length + '-' * (length - filled_length)
    print('\r%s |%s| %s%% %s' % (prefix, bar, percent, suffix), end='\r')
    # Print New Line on Complete
    if iteration == total:
        print()


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Wrong number of arguments. Please, provide in this format: \"file domain-name|ip-address port-number\"")
        sys.exit()
    else:
        file_name = sys.argv[1]
        address = sys.argv[2]
        port = int(sys.argv[3])

        socket = socket.socket()
        socket.connect((address, port))

        # sending name of the file
        socket.send(bytes(file_name, encoding="utf-16-le"))

        # sending file itself
        file_sending(file_name, socket)
