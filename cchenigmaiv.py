from sys import stdout

# Disk configurations

disks = {
    '50': ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm',
           'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z'],

    '51': ['a', 'd', 'c', 'b', 'e', 'h', 'f', 'g', 'i', 'l', 'j', 'k', 'm',
           'p', 'n', 'o', 'q', 't', 'r', 's', 'u', 'x', 'v', 'w', 'z', 'y'],

    '52': ['a', 'y', 'z', 'w', 'v', 'x', 'u', 's', 'r', 't', 'q', 'o', 'n',
           'p', 'm', 'k', 'j', 'l', 'i', 'g', 'f', 'h', 'e', 'b', 'c', 'd'],

    '53': ['a', 'd', 'c', 'b', 'e', 'h', 'g', 'f', 'i', 'l', 'k', 'j', 'm',
           'p', 'o', 'n', 'q', 't', 's', 'r', 'u', 'x', 'w', 'v', 'z', 'y'],

    '60': ['a', 'c', 'e', 'd', 'f', 'h', 'g', 'i', 'k', 'j', 'l', 'n', 'm',
           'o', 'q', 'p', 'r', 't', 's', 'u', 'w', 'v', 'x', 'z', 'y', 'b'],

    '61': ['a', 'z', 'x', 'v', 't', 'r', 'p', 'n', 'd', 'j', 'h', 'f', 'l',
           'b', 'y', 'w', 'u', 's', 'q', 'o', 'm', 'k', 'i', 'g', 'e', 'c'],

    '62': ['a', 'c', 'e', 'g', 'i', 'k', 'm', 'o', 'q', 's', 'u', 'w', 'y',
           'b', 'l', 'f', 'h', 'j', 'd', 'n', 'p', 'r', 't', 'v', 'x', 'z'],

    '63': ['a', 'd', 'e', 'c', 'f', 'i', 'g', 'h', 'k', 'n', 'l', 'j', 'm',
           'p', 'q', 'o', 'r', 'u', 's', 't', 'w', 'z', 'x', 'v', 'b', 'y'],

    '70': ['a', 'z', 'y', 'x', 'w', 'v', 'u', 't', 's', 'r', 'q', 'p', 'o',
           'n', 'm', 'l', 'k', 'j', 'i', 'h', 'g', 'f', 'e', 'd', 'c', 'b'],

    '71': ['a', 'e', 'b', 'c', 'd', 'f', 'j', 'g', 'h', 'i', 'k', 'o', 'l',
           'm', 'n', 'p', 't', 'q', 'r', 's', 'u', 'y', 'v', 'w', 'x', 'z'],

    '72': ['a', 'z', 'x', 'w', 'v', 'y', 'u', 's', 'r', 'q', 't', 'p', 'n',
           'm', 'l', 'o', 'k', 'i', 'h', 'g', 'j', 'f', 'd', 'c', 'b', 'e'],

    '73': ['a', 'x', 'y', 'z', 'w', 't', 'u', 'v', 's', 'p', 'q', 'r', 'o',
           'l', 'm', 'n', 'k', 'h', 'i', 'j', 'g', 'd', 'e', 'f', 'b', 'c'],
}

# Key components: The disks and their order + the initial state of the disks, or the "keyword"

def beautify(text):
    return ' '.join(text[i:i+4] for i in range(0, len(text), 4))

def uglify(text):
    return text.replace(' ', '').lower()

def encrypt(plaintext, key):
    keywordPosOnDisks = [disks[key['disks'][0]].index(key['keyword'][0]),
                    disks[key['disks'][1]].index(key['keyword'][1]),
                    disks[key['disks'][2]].index(key['keyword'][2])]
    ciphertext = ''
    j = 0
    for i, char in enumerate(plaintext):
        if not char.isalpha():
            continue
        posOnDisk2 = disks[key['disks'][2]].index(char)
        movement = (posOnDisk2 - keywordPosOnDisks[2]) % 26
        if j % 2 != 0:
            ciphertext += disks[key['disks'][1]][(keywordPosOnDisks[1] - movement) % 26]
        else:
            ciphertext += disks[key['disks'][0]][(keywordPosOnDisks[0] + movement) % 26]
        j += 1
    return ciphertext

def decrypt(ciphertext, key):
    keywordPosOnDisks = [disks[key['disks'][0]].index(key['keyword'][0]),
                    disks[key['disks'][1]].index(key['keyword'][1]),
                    disks[key['disks'][2]].index(key['keyword'][2])]
    plaintext = ''
    for i in range(0, len(ciphertext), 2):
        posOnDisk0 = disks[key['disks'][0]].index(ciphertext[i])
        posOnDisk1 = disks[key['disks'][1]].index(ciphertext[i + 1])
        movement0 = (posOnDisk0 - keywordPosOnDisks[0]) % 26
        movement1 = (posOnDisk1 - keywordPosOnDisks[1]) % 26
        plaintext += disks[key['disks'][2]][(keywordPosOnDisks[2] + movement0) % 26]
        plaintext += disks[key['disks'][2]][(keywordPosOnDisks[2] - movement1) % 26]
    return plaintext

dictionary = set(open('dict.txt','r').read().lower().split())
max_len = max(map(len, dictionary))

def findEnglishWords(text):
    words_found = set()
    for i in range(len(text)):
        chunk = text[i:i+max_len+1]
        for j in range(4,len(chunk)+1):
            word = chunk[:j]
            if word in dictionary:
                words_found.add(word)

    return words_found

def genCombRange(selected = []):
    diskComb = ['50', '51', '52', '53', '60', '61', '62', '63', '70', '71', '72', '73']
    resultComb = ['50', '51', '52', '53', '60', '61', '62', '63', '70', '71', '72', '73']
    if not selected:
        return resultComb
    for x in diskComb:
        if x in selected:
            resultComb.remove(x)
            if int(x) % 2 == 0:
                resultComb.remove(str(int(x) + 1))
            else:
                resultComb.remove(str(int(x) - 1))
    return resultComb

def verify(possiblePlaintext, ciphertext, key):
    encrypted = encrypt(possiblePlaintext, key)
    return encrypted == ciphertext



def bruteForce(ciphertext, minimumEnglishWords):
    ciphertext = ciphertext.replace(' ', '').lower()
    key = {
        'disks': ['51', '52', '53'],
        'keyword': ['h', 's', 'e']
    }
    i = 0;
    for a in range(0, 26):
        for b in range(0, 26):
            for c in range(0, 26):
                key['keyword'][0] = disks['50'][a]
                key['keyword'][1] = disks['50'][b]
                key['keyword'][2] = disks['50'][c]

                for x in genCombRange():
                    for y in genCombRange([x]):
                        for z in genCombRange([x, y]):
                            key['disks'][0] = x
                            key['disks'][1] = y
                            key['disks'][2] = z
                            possiblePlain = decrypt(ciphertext, key)
                            i += 1
                            stdout.write("\r%d" % i)
                            stdout.flush()
                            engwords = findEnglishWords(possiblePlain)
                            if len(engwords) > minimumEnglishWords:
                                stdout.write("\n")
                                print('Plaintext: ', possiblePlain)
                                print('Found english words: ', engwords)
                                print('Key: ', key)
                                if verify(possiblePlain, ciphertext, key):
                                    print('Good enough!')
                                    return


# Test
key = {
    'disks': ['52', '61', '62'],
    'keyword': ['a', 'b', 'c']
}
print(beautify(encrypt('some string for testing', key)))
print(decrypt(uglify('rnxl rqfh ifmn fqyr hhif'), key))
bruteForce(uglify('rnxl rqfh ifmn fqyr hhif'), 6)
