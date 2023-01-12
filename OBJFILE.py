from SICASM import *

def main():
    # print('파일 이름 입력: ', end = '')
    # NAME = input().upper()
    NAME = 'SRCFILE'
    OBJCode = OBJCODEGen(NAME)
    WriteOBJFILE(OBJCode)
        
    return OBJCode

def OBJCODEGen(NAME, optabPath = 'optab.txt'):
    with open(optabPath, 'r') as f:
        lines = f.readlines()
    OPTAB = OPTABGen(lines) # OPTAB 저장
    
    with open(NAME, 'r') as f: # 파일 읽어와 lines 변수에 텍스트 저장
        lines = f.readlines()
    
    # Pass 1
    INTFILE = INTFILEGen(lines) # 모든 문장 주소 배정
    WriteFILE(INTFILE, 'INTFILE')
    SYMTAB = SYMTABGen(INTFILE) # Pass 2용 레이블 주소 배정
    WriteFILE(SYMTAB, 'SYMTAB')
    
    # Pass 2
    OBJCode = OBJCodeGen(INTFILE, SYMTAB, OPTAB) 
    # 명령어 어셈블, 사용자 정의 데이터 생성, 리스트 출력
    WriteFILE(OBJCode, 'OBJCODE')
    
    return OBJCode

def WriteOBJFILE(OBJCode):
    startAddr = '000000'
    with open('OBJFILE', 'w') as f:
        start = OBJCode[0]['LOC']
        end = OBJCode[-1]['LOC']
        length = format(int(end,16) - int(start,16), 'x') # 프로그램 전체 길이 연산
        code = ''
        CNT = 0
        NUM = 0
        START = 0
        for LINE in OBJCode:
            if not START: # 최초 1회 목적 코드 기입 시작 주소를 받아옴
                Addr = format(int(LINE['LOC'], 16) + (CNT // 2), 'x')
                START = 1
            if LINE['OPCODE'].upper() == 'START': # START
                startAddr = oneWordCounter(LINE["OPERAND"])
                f.write('H' + LINE['LABEL'].upper() + f'  {startAddr}{oneWordCounter(length)}\n')
                
            elif LINE['OPCODE'].upper() == 'END': # END
                f.write('E' + f'{startAddr}')
                
            else: # 위 두 개 이외 연산자
                if LINE['OPCODE'].upper() == 'RESB':
                    CNT += int(LINE['OPERAND']) * 2 # 다음 기입 시작 주소 연산을 위한 칸 계산
                    f.write(f'T{oneWordCounter(Addr)}{oneByteCounter(format(NUM // 2, "x"))}{code.upper()}\n')
                    code = '' # 내용 입력 후 초기화
                    Addr = format(int(Addr, 16) + (CNT // 2), 'x') # 다음 주소 저장
                    CNT = 0
                    NUM = 0
                    
                elif LINE['OPCODE'].upper() == 'RESW':
                    CNT += int(LINE['OPERAND']) * 6 # 다음 기입 시작 주소 연산을 위한 칸 계산
                    f.write(f'T{oneWordCounter(Addr)}{oneByteCounter(format(NUM // 2, "x"))}{code.upper()}\n')
                    code = '' # 내용 입력 후 초기화
                    Addr = format(int(Addr, 16) + (CNT // 2), 'x') # 다음 주소 저장
                    CNT = 0
                    NUM = 0
                    
                else:
                    for byte in LINE['CODE']:
                        if ((CNT + len(LINE['CODE'])) // 2) >= 0x1E: # 최대길이 초과 시
                            f.write(f'T{oneWordCounter(Addr)}{oneByteCounter(format(NUM // 2, "x"))}{code.upper()}\n')
                            code = ''
                            Addr = format(int(Addr, 16) + (CNT // 2), 'x')
                            CNT = 0
                            NUM = 0
                        if CNT < 0x1E * 2:
                            code += byte
                            CNT += 1
                            NUM += 1
                        if CNT // 2 == 0x1E or \
                                int(Addr,16) + (CNT // 2) == int(end, 16): # 라인 최대 or 프로그램 끝
                            f.write(f'T{oneWordCounter(Addr)}{oneByteCounter(format(NUM // 2, "x"))}{code.upper()}\n')
                            code = ''
                            Addr = format(int(Addr, 16) + (CNT // 2), 'x')
                            CNT = 0
                            NUM = 0
    return 0

def oneWordCounter(OPERAND):
    string = ''
    for i in range(6 - len(OPERAND)):
        string += '0'
    string += OPERAND.upper()
    return string
def oneByteCounter(OPERAND):
    string = ''
    for i in range(2 - len(OPERAND)):
        string += '0'
    string += OPERAND.upper()
    return string

if __name__ == '__main__':
    main()