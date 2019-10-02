import socket
from threading import Thread
import glob

clients = []


# Thread to listen one particular client
class ClientListener(Thread):
    def __init__(self, name: str, sock: socket.socket):
        super().__init__(daemon=True)
        self.sock = sock
        self.name = name
        self.file = ''

    # clean up
    def _close(self):
        clients.remove(self.sock)
        self.sock.close()
        print(self.name + ' disconnected')

    def get_file_name(self, byte):
        self.file = byte.decode("utf-16-le")
        print('Receiving file ' + self.file)

    def check_file(self):
        file_name = self.file.split('.')[0].split('_copy')[0]
        files = glob.glob('./' + file_name + '*' + self.file.split('.')[1])
        if len(files):
            extension = str(self.file).split('.')[1]
            self.file = file_name + '_copy' + str(len(files)) + '.' + extension

    def run(self):
        file = None
        byte = self.sock.recv(256)

        # receiving file name
        if not self.file:
            self.get_file_name(byte)

        # check if file with the same name is already in the folder
        if not file:
            self.check_file()
            file = open(self.file, 'wb')

        while True:
            byte = self.sock.recv(256)
            # receiving file content
            if byte:
                file.write(bytes(byte))

            else:
                print("File has been received!")
                self._close()
                return


def main():
    next_name = 1

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    sock.bind(('', 8000))
    sock.listen()

    while True:
        con, addr = sock.accept()
        clients.append(con)
        name = 'u' + str(next_name)
        next_name += 1
        print(str(addr) + ' connected as ' + name)
        ClientListener(name, con).run()


if __name__ == "__main__":
    main()
