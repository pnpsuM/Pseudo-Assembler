def main():
    with open('SRCFILE', 'r') as f: # 파일 읽어와 lines 변수에 텍스트 저장
        lines = f.readlines()
        
    LISFILE = LISFILEGen(lines) # LISFILE 자료구조에 저장
    PrintLISFILE(LISFILE) # LISFILE 출력
    
    print()
    SYMTAB = SYMTABGen(LISFILE) # SYMTAB 작성
    PrintSYMTAB(SYMTAB)
    
    finish = input()
           
def LISFILEGen(lines):
    LISFILE = []
    for line in lines:
        line = line.split() # 문장을 띄어쓰기 단위로 쪼갬
        if len(line) == 2: # 라벨이 없는 경우
            LINE = {'LABEL': '-', 'OPCODE': line[0], 'OPERAND': line[1]}
        elif len(line) == 3: # 라벨이 있는 경우
            LINE = {'LABEL': line[0], 'OPCODE': line[1], 'OPERAND': line[2]}
        LISFILE.append(LINE)
    return LISFILE
        
def SYMTABGen(LISFILE):
    SYMTAB = []
    LABELS = []
    LOCCTR = 0x1000 # LOCCTR 초기화
    for LINE in LISFILE:
        LEN = 0x3 # word
        if LINE['LABEL'] != '-':
            if LINE['OPCODE'].upper() == 'START':
                SYMBOL = {'LABEL': LINE['LABEL'], 'LOC': format(LOCCTR, 'x'), 'FLAG' : '0'}
                LEN = 0 # START 라벨은 LOCCTR 증가 안 함
            elif LINE['OPCODE'].upper() == 'RESW':
                SYMBOL = {'LABEL': LINE['LABEL'], 'LOC': format(LOCCTR, 'x'), 'FLAG' : '0'}
                LEN = int(LINE['OPERAND'], 16) * 0x3
            elif LINE['OPCODE'].upper() == 'RESB':
                SYMBOL = {'LABEL': LINE['LABEL'], 'LOC': format(LOCCTR, 'x'), 'FLAG' : '0'}
                LEN = int(LINE['OPERAND'], 16) * 0x1                
            elif LINE['OPCODE'] == 'byte':
                SYMBOL = {'LABEL': LINE['LABEL'], 'LOC': format(LOCCTR, 'x'), 'FLAG' : '0'}
                LEN = 0x0
                start = False
                for ch in LINE['OPERAND']:
                    if ch == '\'' and start == True:
                        break
                    if start:
                        LEN += 1
                    if ch == '\'':
                        start = True
            else:
                SYMBOL = {'LABEL': LINE['LABEL'], 'LOC': format(LOCCTR, 'x'), 'FLAG' : '0'}
            if LINE['LABEL'] in LABELS:
                SYMBOL['FLAG'] = '1'
            LABELS.append(LINE['LABEL'])
            SYMTAB.append(SYMBOL)
        LOCCTR += LEN # 문장마다 LOCCTR 증가(SIC 명령문은 3 Byte)
    return SYMTAB

def PrintLISFILE(LISFILE): # 출력 함수
    for LINE in LISFILE:
        for key, value in LINE.items():
            if key == 'LABEL':
                print(f'{value.upper():9}', end = '')
            elif key == 'OPCODE':
                print(f'{value.upper():8}', end = '')
            elif key == 'OPERAND':
                print(f'{value.upper():18}', end = '')
        print()
            
def PrintSYMTAB(SYMTAB): # 출력 함수
    for LINE in SYMTAB:
        for key, value in LINE.items():
            print(f'{value}\t', end = '')
        print()
        
if __name__ == '__main__':
    main()