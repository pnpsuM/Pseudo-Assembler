import OBJFILE as o
WORD = 6
BYTE = 2

def main():
    with open('optab.txt', 'r') as f:
        lines = f.readlines()
    OPTAB = o.OPTABGen(lines) # OPTAB 저장
    
    with open('SRCFILE', 'r') as f: # 파일 읽어와 lines 변수에 텍스트 저장
        lines = f.readlines()
    
    OBJCODE = o.main()
    with open('OBJFILE', 'r') as f:
        record = f.readlines()
        
    print('한 번에 실행할 명령어 개수:')
    try:
        iter = int(input())
    except:
        print('올바른 정수를 입력해 주세요. 엔터를 누르면 종료합니다...')
        input()
        exit()
    cnt = iter
    print('실행: r, 종료: q')
    ch = '1'
    while(ch != 'q'):
        for line in record[1:-1]:
            i = 0
            if line[i] == 'T':
                i += WORD + 1
                num = 1
                A = 0xFFFFFF
            else: break
            LEN = int(line[i:i+BYTE], 16)
            i += BYTE
            # 레지스터와 인덱스 초기화 후 문장 길이 저장
            
            for word in range(LEN // 3):
                # 문장을 3바이트 단위로 읽어서 번역
                if cnt >= iter:
                    ch = input()
                    cnt = 0
                if ch == 'r':
                    inst = line[i:i+6]
                    i += WORD
                    if OBJCODE[num]['CODE'].upper() == inst:
                        OPCODE, OPERAND = CodeCheck(inst, OBJCODE, OPTAB)
                        if OPCODE and OPERAND:
                            print(inst, OPCODE, OPERAND)
                            A = Calculate(OPCODE, OPERAND, A)
                            print(f"REGISTER A: {A}", end = '\n\n')
                    num += 1
                    cnt += 1

def CodeCheck(inst, OBJCODE, OPTAB):
    operandAddr = inst[-4:]
    opcode = None
    operand = None
    
    for line in OBJCODE:
        if line['LOC'].upper() == operandAddr:
            operand = line['CODE']
    for name, code in OPTAB.items():
        if inst[:2] == code:
            opcode = name
    
    return opcode, operand

def Calculate(opcode, operand, A):
    opcode = opcode.upper()
    operand = operand.upper()
    if opcode == 'LDA':
        A = int(operand, 16)
    elif opcode == 'ADD':
        A += int(operand, 16)
    elif opcode == 'SUB':
        A -= int(operand, 16)
    elif opcode == 'MUL':
        A *= int(operand, 16)
    
    return A
    
if __name__ == "__main__":
    main()