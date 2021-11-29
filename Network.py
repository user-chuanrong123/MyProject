"""
网口串口界面
"""
import PySimpleGUI as sg
import socket
from  settings import *



FORMAT = '%(asctime)s %(threadName)s %(thread)d %(message)s'
logging.basicConfig(format=FORMAT, level=logging.INFO)
host =socket.gethostbyname(socket.gethostname())
#主题
sg.theme('Default1')

#右边上方框架布局
nbool = '状态'
ip_str = ''
port_str = ''
Frame_one = [
    [sg.Text(nbool, key='-CONORDIS-', font=FONT_SIZE_11, size=(20,1)), sg.Text('对方IP地址:', font=FONT_SIZE_11), sg.Text(ip_str, key='-SHOWIP-', font=FONT_SIZE_11, size=(13,1)), sg.Text('对方端口号: ', font=FONT_SIZE_11), sg.Text(port_str, key='-SHOWPORT-', font=FONT_SIZE_11, size=(6,1))],
    [sg.Button('连接',font=FONT_SIZE_11, size=BUTTEN_SIZE_81, key='-CONNECT-'), sg.Button('断开', key='-DISCONNECT-', font=FONT_SIZE_11, size=BUTTEN_SIZE_81),sg.Button('启动',font=FONT_SIZE_11, size=BUTTEN_SIZE_81, key='-STARTPORT-')]
]

#右边中间框架布局
Frame_two = [[sg.Listbox('', key='-MIDBOX-' ,size=(79,9))]]

#右边下方框架布局
Frame_three = [[sg.Listbox('', key='-BELOW-', size=(79,9))]]

#右边整体框架布局
Frame_Right = [
    [sg.Frame('Socket状态', Frame_one)],
    [sg.Frame('数据接收窗口', Frame_two, key='-RINGHTTWO-')],
    [sg.Frame('数据发送窗口', Frame_three)],
    [sg.Radio('显示十六进制', 'R1', key='-HEX-', font=FONT_SIZE_11), sg.Button('发送数据', key='-SEND-', font=FONT_SIZE_11, size=BUTTEN_SIZE_81), sg.Text('', size=BUTTEN_SIZE_131), sg.Button('统计清零', key='-CLEAR-', font=FONT_SIZE_11, size=BUTTEN_SIZE_81)]
]

#左边列表框显示内容
Left_list = ['TCP Server', 'TCP Client', '---127.0.0.1', 'UDP Server', 'UDP Client']

#整体布局
Layout = [
    [sg.Button('创建',key='-CREATE-', font=FONT_SIZE_11, size=BUTTEN_SIZE_81),
     sg.Button('删除',key='-DELETE-', font=FONT_SIZE_11, size=BUTTEN_SIZE_81),
     sg.Button('退出',key='-EXIT-', font=FONT_SIZE_11, size=BUTTEN_SIZE_81)],
    [sg.Listbox(Left_list, key='-LEFTSEC-', size=(25,30)), sg.Frame('', Frame_Right)]
]

#创建按钮弹窗
Layout_create = [
    [sg.Text('对方IP:', font=FONT_SIZE_11, size=BUTTEN_SIZE_81), sg.InputText('', key='-ADDIP-', size=(20,1))],
    [sg.Text('对方端口:', font=FONT_SIZE_11, size=BUTTEN_SIZE_81), sg.InputText('', key='-ADDPORT-', size=(20,1))],
    [sg.Button('增加',key='-ADD-', font=FONT_SIZE_11, size=BUTTEN_SIZE_81), sg.Button('取消',key='-CANCEL-', font=FONT_SIZE_11, size=BUTTEN_SIZE_81)]
]

window = sg.Window('网口信号接收工具', Layout, icon='ahvbr-81ry5-001.ico')


while True:
    event, values = window.read()
    if event == sg.WINDOW_CLOSED or event == 'Exit':
        break
    if event == '-STARTPORT-':
        window['-RINGHTTWO-'].update(raw_buffer)
    elif event == '-CREATE-':
        window2 = sg.Window('创建客户端', Layout_create, icon='ahvbr-81ry5-001.ico', font=FONT_SIZE_11)
        event2, values2 = window2.read()
        if event2 == sg.WINDOW_CLOSED or event2 == 'Exit' or event2 == '-CANCEL-':
            break

        elif event2 == '-ADD-':
            # if Sock.Connect()
            ip_str = ''.join(values2['-ADDIP-'])
            port_str = ''.join(values2['-ADDPORT-'])
            window['-SHOWIP-'].update(ip_str)
            window['-SHOWPORT-'].update(port_str)






        # print(event2)
        # print(values2)

print(event)
print(values)


