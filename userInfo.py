class User:
    def __init__(self, id, chatId, count: int) -> None:
        self.userId = id
        self.chatId = chatId
        self.count = count

    def saveToFile(self):
        with open("userInfo.txt", 'a') as u:
            print(f"new user {self.count}")
            u.write(f"{self.userId}:[{self.chatId}, {self.count}]\n")