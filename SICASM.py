from OPTAB import OPTABCheck, OPTABGen
from SYMTAB import SYMTABGen

def main():
    with open('optab.txt', 'r') as f:
        lines = f.readlines()
    OPTAB = OPTABGen(lines) # OPTAB 저장
    
    with open('SRCFILE', 'r') as f: # 파일 읽어와 lines 변수에 텍스트 저장
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

def OBJCodeGen(INTFILE, SYMTAB, OPTAB):
    OBJCode = []
    for LINE in INTFILE:
        Error = None
        Code = ''
        if LINE['OPCODE'] == 'word': # WORD 명령어 처리
            num = int(LINE['OPERAND'], 16)
            strnum = format(num, 'x')
            for i in range(6 - len(strnum)): # 1 word 만큼 작성
                Code += '0'
            Code += strnum
            
        elif LINE['OPCODE'] == 'byte': # BYTE 명령어 처리 
            start = False
            for ch in LINE['OPERAND']: # string 파트만 변수에 저장
                if ch == '\'' and start == True:
                    break
                if start:
                    Code += format(ord(ch), 'x') # 16진수 문자열로 저장
                if ch == '\'':
                    start = True
        
        # RESW, RESB는 Pass 1에서 공간 할당
        elif LINE['OPCODE'] == 'resw':
            pass
        elif LINE['OPCODE'] == 'resb':
            pass
        
        # START, END는 OPTAB에 포함되지 않는 정상 명령어
        elif LINE['OPCODE'] == 'start' or LINE['OPCODE'] == 'end':
            pass
        
        # 다른 명령어는 OPTAB과 SYMTAB을 확인해 처리
        else:
            # 각 Check 함수는 테이블에 대응하는 값이 있으면 코드를 반환, 
            # 그렇지 않으면 None을 반환
            OPCODE = OPTABCheck(OPTAB, LINE['OPCODE'].upper())
            OPERAND = SYMTABCheck(SYMTAB, LINE['OPERAND'])
            if OPCODE == None:
                Error = '**** unrecognized operation code'
            elif OPERAND == None:
                # 인덱스 주소 피연산자(str1,x)는 SYMTAB에 없음
                temp = LINE['OPERAND'].split(',')
                try:
                    if temp[1] == 'x':
                        OPERAND = SYMTABCheck(SYMTAB, temp[0])
                        OPERAND = int(OPERAND, 16) + 0x1000
                        # 16진수 명령어를 인덱스 주소 지정 방식에 맞게 조정
                        OPERAND = format(OPERAND, 'x')
                        Code = OPCODE + OPERAND
                        # 코드 작성
                    else:
                        pass
                except:    
                    Error = '**** undefined symbol in operand'
            else:
                Code = OPCODE + OPERAND
                # 코드 작성
        temp = {'LOC': LINE['LOC'], 'CODE': Code, 'LABEL': LINE['LABEL'], 
                'OPCODE': LINE['OPCODE'], 'OPERAND': LINE['OPERAND']}
        # LOC CODE LABEL OPCODE OPERAND 순으로 OBJCode에 삽입
        OBJCode.append(temp)
        if Error:
            OBJCode.append({'error': Error})
    return OBJCode
    
def INTFILEGen(lines):
    INTFILE = []
    LOCCTR = 0x1000 # LOCCTR 초기화
    for line in lines:
        line = line.split() # 문장을 띄어쓰기 단위로 쪼갬
        if len(line) == 2: # 라벨이 없는 경우
            LINE = {'LOC': format(LOCCTR, 'x'), 'LABEL': '', 'OPCODE': line[0], 'OPERAND': line[1]}
            
        elif len(line) == 3:
            LINE = {'LOC': format(LOCCTR, 'x'), 'LABEL': line[0], 'OPCODE': line[1], 'OPERAND': line[2]}
        else:
            LINE = {line: '\n*** not a appropriate form ***'}
            
        LEN = 0x3 # word
        if LINE['OPCODE'].upper() == 'START':
            LEN = 0x0 # START 라벨은 LOCCTR 증가 안 함
        elif LINE['OPCODE'].upper() == 'RESW':
            LEN = int(LINE['OPERAND'], 16) * 0x3
        elif LINE['OPCODE'].upper() == 'RESB':
            LEN = int(LINE['OPERAND'], 16) * 0x1
        elif LINE['OPCODE'].upper() == 'BYTE':
            temp = LINE['OPERAND'].split('\'')
            chlen = len(temp[1])
            LEN = chlen * 0x1
            
        INTFILE.append(LINE)
        
        LOCCTR += LEN # 문장마다 LOCCTR 증가(SIC 명령문은 3 Byte)
        # RESW, BESB의 경우 LEN 조정
    return INTFILE 

def SYMTABCheck(SYMTAB, label):
    for SYMBOL in SYMTAB:
        if SYMBOL['LABEL'] == label:
            return SYMBOL['LOC']
    return None

def PrintINTFILE(INTFILE): # 출력 함수
    for LINE in INTFILE:
        for key, value in LINE.items():
            if key == 'LOC':
                print(f'{value:6}', end = '')
            elif key == 'LABEL':
                print(f'{value:9}', end = '')
            elif key == 'OPCODE':
                print(f'{value:8}', end = '')
            elif key == 'OPERAND':
                print(f'{value:18}', end = '')
        print()
        
def WriteFILE(FILE, name):
    with open(name, 'w') as f:
        for LINE in FILE:
            for key, value in LINE.items():
                if key == 'LOC':
                    f.write(f'{value:6}')
                elif key == 'LABEL':
                    f.write(f'{value:9}')
                elif key == 'OPCODE':
                    f.write(f'{value:8}')
                elif key == 'OPERAND':
                    f.write(f'{value:18}')
                elif key == 'CODE':
                    f.write(f'{value:15}')
                elif key == 'FLAG':
                    f.write(f'{value:3}')
                elif key == 'error':
                    f.write(f'{value}')
            f.write('\n')
        
if __name__ == '__main__':
    main()