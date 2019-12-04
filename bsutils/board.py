from loguru import logger
import serial
import sys
import os


class BoardSerial(object):

    def __init__(self):

        self.rate = 9600
        self.time = 1

    def open_connection(self, port):

        try:

            if sys.platform == 'linux':
                os.system('sudo chmod -R 777 ' + port)

            connection = serial.Serial(port, baudrate=self.rate, timeout=self.time)
            logger.success('Successfully connected')
            return connection

        except serial.SerialException:
            logger.error('Check your parameters and your permission.')
            return None

    def send_message(self, connection, message):

        if connection is None:
            logger.error('Error in connection')

            return False
        else:
            message = str(message)

            message = self.create_digit(message)

            connection.write(message.encode())

            return True

    @staticmethod
    def create_digit(information):

        information = information.upper()

        information += ','

        verify_digit = 0

        for digit in str(information):
            verify_digit ^= ord(digit)

        validated_information = ''
        hexadecimal = hex(verify_digit)
        len_hexadecimal = len(hexadecimal)

        if len_hexadecimal == 3:
            validated_information = '0' + hexadecimal[2]
        elif len_hexadecimal == 4:
            validated_information = hexadecimal[2:4]
        else:
            logger.error('Unable to generate validation')

        validated_information = '{}*{}\r\n'.format(information, validated_information.upper())

        return validated_information.upper()

    def verify_digit(self, information):

        position = information.find('*')

        result = self.create_digit(information[:position - 1])

        if information[position + 1:] == result[position + 1:]:
            return True
        else:
            return False
