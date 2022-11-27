from datetime import datetime


class Write:
    @staticmethod
    def toUniversalFile(text):
        with open(file='logs/at_log.txt', mode='a', encoding='ASCII') as f:
            text = text.replace('\r\n', '\r')
            f.write(text)

    @staticmethod
    def toSeparateFile(text):
        with open(file=f'logs/at_log_{datetime.now().strftime("d_%m_%Y_%Hh%Mm%Ss")}.txt', mode='w',
                  encoding='ASCII') as f:
            text = text.replace('\r\n', '\r')
            f.write(text)
