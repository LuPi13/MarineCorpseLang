import sys
from enum import Enum, auto


class KeyWordType(Enum):
    BLANK = auto()
    VAR_DECLARE = auto()
    INPUT = auto()
    OUTPUT = auto()
    GOTO = auto()
    IF = auto()


class MarineLang:
    def __init__(self):
        self.index = 0
        self.int_data = dict()
        self.string_data = dict()


    # [해병연산] . -> 1 감소, ! -> 1 증가, ? -> 앞뒤 곱연산
    def get_int(self, code):
        plus = code.count("!")
        minus = code.count(".")

        code.replace("!", "")
        code.replace(".", "")

        if (not code.empty()):
            raise SyntaxError(f"아뿔싸! 컴 파일러 해병님과 {self.index + 2}초간의 마라톤회의 진행중에 숫자를 오도짜세해병식으로 입력하지 않아 해병수육이 되고 말았다!")

        return plus - minus


    # [해병변수입력] 새끼... ~~(숫자 or @) (~~ 뒤에 오는 해병연산이나 변수값 저장 또는 @로 입력받아 저장, 변수명이 '해병'으로 시작하면 아스키 변수로 저장)
    def get_number(self, code):
        output = 0
        now_add = True

        while (len(code) != 0):
                if (code.startswith("@")):
                    given = input()
                    if (now_add):
                        if (given.isdigit()):
                            output += int(given)
                        elif (len(given) == 1):
                            output += ord(given)
                        else:
                            raise SyntaxError("아쎄이! 잘못된 입력방식이다!")
                    else:
                        if (given.isdigit()):
                            output += int(given)
                        elif (len(given) == 1):
                            output += ord(given)
                        else:
                            raise SyntaxError("아쎄이! 잘못된 입력방식이다!")
                        now_add = True

                    code = code[1:]

                elif (code.startswith("!") or code.startswith(".")):
                    now_char = code[0]
                    now_num = 0

                    while (now_char == "!" or now_char == "."):
                        if (not code):
                            break

                        now_char = code[0]

                        if (now_char == "!"):
                            now_num += 1
                        elif (now_char == "."):
                            now_num -= 1
                        else:
                            break

                        code = code[1:]

                    if (now_add):
                        output += now_num
                    else:
                        output *= now_num
                        now_add = True

                elif (code.startswith("?")):
                    now_add = False
                    code = code[1:]

                else:
                    is_var_name = False
                    if (code.startswith("긴빠이 친 ")):
                        code = code.removeprefix("긴빠이 친 ")
                        for key in self.int_data.keys():
                            if (code.startswith(key)):
                                if (now_add):
                                    output += self.int_data[key]
                                else:
                                    output *= self.int_data[key]
                                    now_add = True

                                code = code[len(key):]
                                is_var_name = True
                                break

                        for key in self.string_data.keys():
                            if (code.startswith(key)):
                                if (now_add):
                                    output += ord(self.string_data[key])
                                else:
                                    output *= ord(self.string_data[key])
                                    now_add = True

                                code = code[len(key):]
                                is_var_name = True
                                break
                    else:
                        raise SyntaxError(f"아뿔싸! 컴 파일러 해병님과 {self.index + 2}초간의 마라톤회의 진행중에 모범적인 해병대의 오도짜세해병체를 사용하지 않아 해병수육이 되고 말았다!")

                    if (not is_var_name):
                        raise ValueError(f"아뿔싸! 컴 파일러 해병님과 {self.index + 2}초간의 마라톤회의 진행중에 없는 변수를 참조하는 기열민간인 짓을 하여 해병돈까스가 되고 말았다!")

        return output


    def get_output(self, code):
        for key in self.int_data.keys():
            if (code.startswith(key)):
                if (code == key):
                    return self.int_data[key]
                else:
                    raise ValueError(f"아뿔싸! 컴 파일러 해병님과 {self.index + 2}초간의 마라톤회의 진행중에 없는 변수를 참조하는 기열민간인 짓을 하여 해병돈까스가 되고 말았다!")

        for key in self.string_data.keys():
            if (code.startswith(key)):
                if (code == key):
                    return self.string_data[key]
                else:
                    raise ValueError(f"아뿔싸! 컴 파일러 해병님과 {self.index + 2}초간의 마라톤회의 진행중에 없는 변수를 참조하는 기열민간인 짓을 하여 해병돈까스가 되고 말았다!")



    @staticmethod
    def get_type(self, code):
        if (not code):
            return KeyWordType.BLANK
        elif code.startswith("새끼... "):
            return KeyWordType.VAR_DECLARE
        elif code.startswith("@"):
            return KeyWordType.INPUT
        elif code.startswith("오도짜세"):
            return KeyWordType.OUTPUT
        elif code.startswith("기합"):
            return KeyWordType.GOTO
        elif code.startswith("악! "):
            return KeyWordType.IF
        else:
            raise SyntaxError(f"아뿔싸! 컴 파일러 해병님과 {self.index + 2}초간의 마라톤회의 진행중에 모범적인 해병대의 오도짜세해병체를 사용하지 않아 해병수육이 되고 말았다!")


    def compileLine(self, code):
        if (code == ""):
            return None

        TYPE = self.get_type(self, code)

        if (TYPE == KeyWordType.BLANK):
            return

        if (TYPE == KeyWordType.VAR_DECLARE):
            comps = []

            code = code.removeprefix('새끼... ')
            for i in range(0, len(code)):
                if ((code[i] == ".") or (code[i] == "!") or (code[i] == "?") or (code[i] == "@")):
                    comps.append(code[:i])
                    comps.append(code[i:])
                    break
                if (code[i] == " "):
                    comps.append(code[:i])
                    comps.append(code[i+1:])
                    break

            val = 0
            varname = comps[0]

            if ((len(comps) != 1) and (len(comps) != 2)):
                raise SyntaxError(f"아뿔싸! 컴 파일러 해병님과 {self.index + 2}초간의 마라톤회의 진행중에 오도짜세해병체를 기열찐빠같이 사용하여 해병삼겹살이 되고 말았다!")

            if (len(comps) == 2):
                if ((not varname.startswith("해병")) and (not varname in self.int_data)):
                    self.int_data[varname] = 0
                elif ((varname.startswith("해병") and (not varname in self.string_data))):
                    self.string_data[varname] = chr(0)
                try:
                    val = self.get_number(comps[1])
                except Exception:
                    raise SyntaxError(f"아뿔싸! 컴 파일러 해병님과 {self.index + 2}초간의 마라톤회의 진행중에 유효한 숫자를 입력하지 않아 해병족발이 되고 말았다!")

            if (varname.startswith("해병")):
                self.string_data[varname] = chr(ord(self.string_data[varname]) + val)
            else:
                self.int_data[varname] += val

        if (TYPE == KeyWordType.INPUT):
            input()

        if (TYPE == KeyWordType.OUTPUT):
            code = code.removeprefix("오도짜세")
            if (code.endswith("!")):
                code = code.removesuffix("!")
                try:
                    val = self.get_output(code)
                    print(val, end = "")
                except UnicodeEncodeError:
                    raise UnicodeEncodeError(f"아뿔싸! 컴 파일러 해병님과 {self.index + 2}초간의 마라톤회의 진행중에 못읽는 글자를 해병님께 읽게 하여 해병육회가 되고 말았다!")
                except Exception:
                    raise ValueError(f"아뿔싸! 컴 파일러 해병님과 {self.index + 2}초간의 마라톤회의 진행중에 없는 변수를 참조하는 기열민간인 짓을 하여 해병돈까스가 되고 말았다!")
            else:
                raise SyntaxError(f"아뿔싸! 컴 파일러 해병님과 {self.index + 2}초간의 마라톤회의 진행중에 오도짜세해병체를 기열찐빠같이 사용하여 해병삼겹살이 되고 말았다!")

        if (TYPE == KeyWordType.GOTO):
            number = code[2:]
            number_int = self.get_number(number)

            return number_int - 2

        if (TYPE == KeyWordType.IF):
            code = code.removeprefix("악! ")
            comps = code.split('을 해도 되는 지에 대한 조건으로 ')

            if (len(comps) != 2):
                raise SyntaxError(f"아뿔싸! 컴 파일러 해병님과 {self.index + 2}초간의 마라톤회의 진행중에 오도짜세해병체를 기열찐빠같이 사용하여 해병삼겹살이 되고 말았다!")

            if (comps[1].endswith("에 대해 여쭈어봐도 되겠습니까!")):
                comps[1] = comps[1].removesuffix("에 대해 여쭈어봐도 되겠습니까!")
                if (comps[1].startswith("개씹썅똥꾸릉내 나는 ")):
                    comps[1] = comps[1].removeprefix("개씹썅똥꾸릉내 나는 ")
                    num = self.get_number(comps[1])
                    if (num != 0):
                        states = self.compileLine(comps[0])

                        if (type(states) == int):
                            self.index = states - 1

                else:
                    num = self.get_number(comps[1])
                    if (num == 0):
                        states = self.compileLine(comps[0])

                        if (type(states) == int):
                            self.index = states - 1

            else:
                raise SyntaxError(f"아뿔싸! 컴 파일러 해병님과 {self.index + 2}초간의 마라톤회의 진행중에 모범적인 해병대의 오도짜세해병체를 사용하지 않아 해병수육이 되고 말았다!")


    def compile(self, code):
        self.index = 0

        if (code.pop(0) != "라이라이라이라이 차차차!"):
            raise SyntaxError("아쎄이! 오도짜세해병체를 처음부터 틀렸다!")
        if (code.pop() != "부라보! 부라보! 해병대!"):
            raise SyntaxError("아쎄이! 오도짜세해병체의 마무리가 마음에 안든다!")

        while (self.index < len(code)):
            states = self.compileLine(code[self.index])
            self.index += 1

            if (type(states) == int):
                self.index = states


    def compile_file(self, path):
        try:
            with open(path, encoding="utf-8-sig") as mcl_file:
                code = mcl_file.read().splitlines()
                self.compile(code)

        except FileNotFoundError:
            raise FileNotFoundError("아뿔싸! 존재하지도 않는 파일을 컴 파일러 해병님께 들이밀었다가 격노하셔 나에게 해병오함마(두개골에 직접투여)를 직접 처방하여 주셨다!")
        except UnicodeDecodeError:
            raise UnicodeDecodeError("아뿔싸! 컴 파일러 해병님이 읽지 못하시는 파일을 들이밀어서 격노하신 해병님이 나에게 해병야구방망이(갈비뼈에 직접투여)를 직접 처방하여 주셨다!")


if __name__ == "__main__":
    compiler = MarineLang()
    if (len(sys.argv) == 2):
        compiler.compile_file(sys.argv[2])
    else:
        compiler.compile_file("main.mcl")
