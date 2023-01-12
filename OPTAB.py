def main():
    with open('optab.txt', 'r') as f:
        lines = f.readlines()
    OPTAB = OPTABGen(lines)
    
    while(1):
        print('\nInput a query instruction (0 to quit): ',end = '')
        query = input().upper()
        if query == '0':
            break
        else:
            OPTABCheck(OPTAB, query)

def OPTABGen(lines):
    OPTAB = {}
    for line in lines:
        # 읽어온 파일을 나눠 딕셔너리에 저장
        inst, code = line.split(' ')
        OPTAB[inst] = code.strip()
    return OPTAB

def OPTABCheck(OPTAB, query):
        try:
            # print(f'\nCode for the query instruction ({query}): {OPTAB[query]}')
            return OPTAB[query]
        except KeyError as e:
            print(f'\nCouldn\'t find a matching instruction {query}')
            return None
      
if __name__ == '__main__':
    main()