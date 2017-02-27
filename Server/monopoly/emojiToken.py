import os
import binascii
import random

shortHex = [b'3',b'4',b'5']
longHex = [b'0',b'1',b'2',b'3',b'4',b'5',b'6',b'7',b'8',b'9',b'A',b'B',b'C',b'D',b'E',b'F']
unsupported = [b'1F321', b'1F322', b'1F323', b'1F324', b'1F325', b'1F326', b'1F327', b'1F328', b'1F329', b'1F32A', b'1F32B', b'1F32C', b'1F32D', b'1F32E', b'1F32F', b'1F336', b'1F37D', b'1F37E', b'1F37F', b'1F394', b'1F395', b'1F396', b'1F397', b'1F398', b'1F399', b'1F39A', b'1F39B', b'1F39C', b'1F39D', b'1F39E', b'1F39F', b'1F3C5', b'1F3CB', b'1F3CC', b'1F3CD', b'1F3CE', b'1F3CF', b'1F3D0', b'1F3D1', b'1F3D2', b'1F3D3', b'1F3D4', b'1F3D5', b'1F3D6', b'1F3D7', b'1F3D8', b'1F3D9', b'1F3DA', b'1F3DB', b'1F3DC', b'1F3DD', b'1F3DE', b'1F3DF', b'1F3F1', b'1F3F2', b'1F3F3', b'1F3F4', b'1F3F5', b'1F3F6', b'1F3F7', b'1F3F8', b'1F3F9', b'1F3FA', b'1F3FB', b'1F3FC', b'1F3FD', b'1F3FE', b'1F3FF', b'1F43F', b'1F441', b'1F4F8', b'1F4FD', b'1F4FE', b'1F4FF', b'1F53E', b'1F53F', b'1F540', b'1F541', b'1F542', b'1F543', b'1F544', b'1F545', b'1F546', b'1F547', b'1F548', b'1F549', b'1F54A', b'1F54B', b'1F54C', b'1F54D', b'1F54E', b'1F54F', b'1F568', b'1F569', b'1F56A', b'1F56B', b'1F56C', b'1F56D', b'1F56E', b'1F56F', b'1F570', b'1F571', b'1F572', b'1F573', b'1F574', b'1F575', b'1F576', b'1F577', b'1F578', b'1F579', b'1F57A', b'1F57B', b'1F57C', b'1F57D', b'1F57E', b'1F57F', b'1F580', b'1F581', b'1F582', b'1F583', b'1F584', b'1F585', b'1F586', b'1F587', b'1F588', b'1F589', b'1F58A', b'1F58B', b'1F58C', b'1F58D', b'1F58E', b'1F58F', b'1F590', b'1F591', b'1F592', b'1F593', b'1F594', b'1F595', b'1F596', b'1F597', b'1F598', b'1F599', b'1F59A', b'1F59B', b'1F59C', b'1F59D', b'1F59E', b'1F59F', b'1F5A0', b'1F5A1', b'1F5A2', b'1F5A3', b'1F5A4', b'1F5A5', b'1F5A6', b'1F5A7', b'1F5A8', b'1F5A9', b'1F5AA', b'1F5AB', b'1F5AC', b'1F5AD', b'1F5AE', b'1F5AF', b'1F5B0', b'1F5B1', b'1F5B2', b'1F5B3', b'1F5B4', b'1F5B5', b'1F5B6', b'1F5B7', b'1F5B8', b'1F5B9', b'1F5BA', b'1F5BB', b'1F5BC', b'1F5BD', b'1F5BE', b'1F5BF', b'1F5C0', b'1F5C1', b'1F5C2', b'1F5C3', b'1F5C4', b'1F5C5', b'1F5C6', b'1F5C7', b'1F5C8', b'1F5C9', b'1F5CA', b'1F5CB', b'1F5CC', b'1F5CD', b'1F5CE', b'1F5CF', b'1F5D0', b'1F5D1', b'1F5D2', b'1F5D3', b'1F5D4', b'1F5D5', b'1F5D6', b'1F5D7', b'1F5D8', b'1F5D9', b'1F5DA', b'1F5DB', b'1F5DC', b'1F5DD', b'1F5DE', b'1F5DF', b'1F5E0', b'1F5E1', b'1F5E2', b'1F5E3', b'1F5E4', b'1F5E5', b'1F5E6', b'1F5E7', b'1F5E8', b'1F5E9', b'1F5EA', b'1F5EB', b'1F5EC', b'1F5ED', b'1F5EE', b'1F5EF', b'1F5F0', b'1F5F1', b'1F5F2', b'1F5F3', b'1F5F4', b'1F5F5', b'1F5F6', b'1F5F7', b'1F5F8', b'1F5F9', b'1F5FA']

def generateEmoji():
    emoji = b'\\U0001F'+random.choice(shortHex)+random.choice(longHex)+random.choice(longHex)
    if bytes(emoji[5:]) in unsupported:
        emoji = generateEmoji()
    
    return emoji

def getEmojiToken(n):
    
    token = ''
    for i in range(0,n):
        emoji = generateEmoji()
        token += emoji.decode('unicode_escape')
    
    return token
    
def test():
    token = getEmojiToken(8)
    print('http://'+token)
