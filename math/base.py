class Num:
    list = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
            'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j',
            'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't',
            'u', 'v', 'w', 'x', 'y', 'z', '!', '@', '#', '$',
            '%', '^', '&', '*', '(', ')', '`', '~', '|', ':',
            ';', "'", '"', '<', '>', ',', '.', '/', '?', ' ',
            '_', '-', '+', '=', ' ', 'A', 'B', 'C', 'D', 'E',
            'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O',
            'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y',
            'Z'
            ]

    def __init__(self, num: str, base: int):
        self.num = num
        self.base = base
        self.check_validity()

    def check_validity(self):
        for each in self.num:
            if Num.list.index(each) >= self.base:
                raise ValueError(f"INVALID NUMBER -> {self.num}")
        if len(Num.list) < self.base:
            raise ValueError(f"INVALID BASE -> {self.base}, MAX IS {len(Num.list)}")

    def convert_to_decimal(self) -> float:
        total = 0
        for power, each in enumerate(self.num[::-1]):
            total += Num.list.index(each) * self.base ** power
        return total

    def convert_to_base(self, base) -> str:
        res = ""
        dec_num = self.convert_to_decimal()

        while dec_num != 0:
            dev = dec_num // base
            rem = dec_num % base
            res += Num.list[rem]
            dec_num = dev
        if base < 10:
            res = res[::-1]

        res = Num.remove_leading_zeros(res)

        return res

    @staticmethod
    def remove_leading_zeros(num) -> str:
        while num[0] == "0":
            num = num[1:]
        return num


new = Num("Abdulrahman Abusharbain", len(Num.list))
print(new.convert_to_base(10))
