class DevConfig :
    value = dict()
    file_content = ""
    def __init__(self, filename, create_dict = True) :
        file = open(filename, "r")
        while True:
            content=file.readline()
            if not content:
                break
            if (not create_dict) :
                self.file_content = self.file_content + content
                continue
            content = content.strip()
            if len(content) == 0 or  content[0] == '#' :
                continue
            colPos = content.find(':')
            if colPos == -1 :
                # error
                continue;
            key = content[:colPos].strip()
            val = content[colPos + 1 :].strip()
            self.value[key] = val
        file.close()