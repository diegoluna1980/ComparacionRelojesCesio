# -*- coding: utf-8 -*-
"""
Editor de Spyder

Este es un archivo temporal.
"""
import serial, time, schedule, pyvisa
import dateutil.parser, astropy.time
from datetime import date
from ftplib import FTP


# ACORDARSE DE CAMBIAR EL NIVEL DE DISPARO A 1V

# Configura el puerto para el multiplexor
ser = serial.Serial()
ser.port = 'COM6'
ser.baudrate = 9600
ser.open()

# Configura el contador
rm = pyvisa.ResourceManager()
SR620 = rm.open_resource('GPIB0::16::INSTR')
SR620.write("*rst; status:preset; *cls")
SR620.write("MODE0;SRCE0;ARMM1;SIZE1;AUTM0;CLCK1")
SR620.write("TERM1,0;TERM2,0;LEVL1,1;LEVL2,1")

def subUTCr(MJD):
    MJD_str = str(MJD)
    filename = 'CDIN__' + MJD_str[:2] + '.' + MJD_str[2:]
    ftp = FTP('5.144.141.242', timeout=10)
    print('ftp definido')
    time.sleep(10)
    ftp.login(user='INTI', passwd = 'PONERPASSWORDDEINTI')
    print('adentro del BIPM')
    time.sleep(10)
    ftp.cwd('/data/UTCr/INTI/CLOCK')
    ftp.storbinary('STOR '+ filename, open( './archivosBIPM/UTCr/' + filename, 'rb'))    
    print( filename + ': SUBIDO')      
    ftp.quit()

def MJD_today():
    today = date.today()
    hoy = today.strftime("%Y.%m.%d")
    dt = dateutil.parser.parse(hoy)
    time = astropy.time.Time(dt)
    MJD = int(time.mjd)
    return MJD

def mideTD(relo):
    ser.write(relo)
    time.sleep(10)
    TD = float(SR620.query("STRT;*WAI;XAVG?")) - 34e-9 # 34 ns por offsets de cables
    if TD > 0.5:
        SR620.write("SRCE1")
        time.sleep(3)
        TD = float(SR620.query("STRT;*WAI;XAVG?"))
        print(str(TD))
        time.sleep(5)
        SR620.write("SRCE0")

    TD = '{0:.1f}'.format((-1)*TD*1E9)
    time.sleep(10)
    return TD

def generaCDIN(MJD, TD12, TD13):
    MJD_str = str(MJD)
    linea = MJD_str + ' 10015'
    linea = linea + ' 1362377       0.0'
    linea = linea + ' 1363270 ' + TD12.rjust(9)
    linea = linea + ' 1363511 ' + TD13.rjust(9)

    filename1 = './archivosBIPM/UTCr/CDIN__' + MJD_str[0:2] + '.' + MJD_str[2:5]
    f = open(filename1, 'w+')
    f.write(linea + '\n')
    f.close()
    
def appendRNT(MJD,hora,T12,T13):
    filename = './archivosRNT/TDI1-I2_' + str(MJD) + '.txt'
    f = open(filename, 'a+')
    f.write(hora + '\t' + T12 + '\n')
    f.close()
    
    filename = './archivosRNT/TDI1-I3_' + str(MJD) + '.txt'
    f = open(filename, 'a+')
    f.write(hora + '\t' + T13 + '\n')
    f.close()
    
def jobRNT():
    print('comienza jobRNT a las ' + time.strftime("%H%M%S"))
    hora = time.strftime("%H%M%S")
    TD12 = mideTD(b'CLOCK1')
    TD13 = mideTD(b'CLOCK2')
    MJD = MJD_today()
    appendRNT(MJD,hora,TD12,TD13)
    time.sleep(60)

def jobUTCr():
    print('comienza jobUTCr a las ' + time.strftime("%H%M%S"))
    TD12 = mideTD(b'CLOCK1')
    TD13 = mideTD(b'CLOCK2')
    MJD = MJD_today()
    generaCDIN(MJD, TD12, TD13)
#    subUTCr(MJD)
    time.sleep(60)


print('Medición inicial de prueba a las ' + time.strftime("%H%M%S"))
TD12 = mideTD(b'CLOCK1')
TD13 = mideTD(b'CLOCK2')


schedule.every().hour.at(":00").do(jobRNT)
schedule.every().day.at("00:10").do(jobUTCr)


while True:
    schedule.run_pending()
    time.sleep(1)
