import SimpleQIWI

TOKEN = "b55d3014f1219106e3daf146f4b81243"

PHONE = "+79851609109"


class QiwiChecker:

    TOKEN = "b55d3014f1219106e3daf146f4b81243"

    PHONE = "+79851609109"

    def __init__(self, ID, SUM) -> None:

        self.id = ID

        self.sum = SUM

    def check(self):

        for CUR in SimpleQIWI.QApi(token=TOKEN, phone=PHONE).payments["data"]:

            try:

                if int(CUR["comment"]) == self.id and int(CUR["sum"]["amount"]) == self.sum:

                    return True, CUR["txnId"]

            except (KeyError, TypeError, ValueError):

                continue

        return False






