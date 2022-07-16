import threading
import PySimpleGUI as sg
from tqsdk import TqApi, TqAuth, TargetPosTask

api = TqApi(auth= TqAuth("15221624883", "15221shuai"))
quote_a = api.get_quote("SHFE.ni2207")
quote_b = api.get_quote("SHFE.ni2206")


class WorkingThread(threading.Thread):
    def run(self):
        while True:
            api.wait_update()


# 创建新线程
wt = WorkingThread()
wt.start()

layout = [[sg.Text('ni2207'), sg.Text("99999", key="ni2207.last")],
          [sg.Text('ni2206'), sg.Text("99999", key="ni2206.last")],
          [sg.Text('spread'), sg.Text("99999", key="spread")],
          ]

window = sg.Window('价差显示', layout)

while True:  # Event Loop
    event, values = window.Read(timeout=1)
    if event is None or event == 'Exit':
        break
    window.Element('ni2207.last').Update(quote_a.last_price)
    window.Element('ni2206.last').Update(quote_b.last_price)
    window.Element('spread').Update(quote_b.last_price - quote_a.last_price)

window.Close()