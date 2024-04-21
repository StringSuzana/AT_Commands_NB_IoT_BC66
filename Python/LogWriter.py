from datetime import datetime


class Write:
    @staticmethod
    def toUniversalFile(text):
        with open(file='logs/at_log.txt', mode='a', encoding='utf-8') as f:
            f.write(text)

    @staticmethod
    def toSeparateFile(text):
        with open(
                file=f'logs/at_log_{datetime.now().strftime("Y_%m_%d_%Hh%Mm%Ss")}.txt', mode='w',
                encoding='ASCII') as f:
            # text = text.replace('\r\n', '\r')
            f.write(text)
