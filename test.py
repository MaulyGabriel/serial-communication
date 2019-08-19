from bsutils.board import Wifi
from bsutils.board import Serial


def wifi_protocol():
    w = Wifi()
    connection, client = w.open_connection(port=5000, host='')

    while True:

        print('Client: ', client)

        message = connection.recv(1024)

        print('Message: ', message.decode())

        if message.decode() == 'exit':
            connection.send('Bye')
            connection.close()
            break


def send_command():
    s = Serial()

    connection = s.open_connection('/dev/ttyUSB0')

    while True:

        v = raw_input('Digit your command:')
        v = str(v)

        if v == 'a':
            s.send_message(connection, '$PNEUD,G,1,123456782')
        elif v == 'b':
            s.send_message(connection, '$PNEUD,G,1,123456782,1')
        elif v == 'c':
            s.send_message(connection, '$PNEUD,G,1,123456782,')
        elif v == 'd':
            s.send_message(connection, '$PNEUDOK')


def serial_protocol():
    s = Serial()

    connection = s.open_connection(port='/dev/ttyUSB0')

    s.send_message(connection, '$PNEUL,G,3')

    connection.close()


def example():
    s = Serial()

    connection = s.open_connection(port='/dev/ttyUSB0')

    while True:

        if connection is None:
            connection = s.open_connection(port='/dev/ttyUSB0')

        try:

            if connection.inWaiting() > 0:
                message = connection.readline().decode('utf-8', 'replace')
                print(message)

        except UnicodeError:
            print('Invalid character')


if __name__ == '__main__':
    send_command()
