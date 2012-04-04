config = { 
  'Toyota EPC' : { 
    'path': "D:/TMCEPCW3/APLI/TMAIN.EXE",
    #'area': ('Europe', 'General', 'USA, Canada', 'Japan')
    'present': True
  }, 
  'Tecdoc': { 
    'path': "D:/TECDOC_CD/1_2012/pb/tof.exe",
    'present': False
  },
  'Mitsubishi ASA' : {
    'GENERAL EXPORT': {
      'present': True,
      'path': 'C:\MMC\ASA\M80\PROG\ASA.exe'
    },
    'NORTH AMERICA': {
      'present': True,
      'path': 'C:\MMC\ASA\M50\PROG\ASA.exe'
    },
    'JAPAN': {
      'present': True,
      'path': 'C:\MMC\ASA\M00\PROG\ASA.exe'
    },
    'EUROPE': {
      'present': True,
      'path': 'C:\MMC\ASA\M60\PROG\ASA.exe'
    }
  },
  'Redis': '192.168.2.6'
}