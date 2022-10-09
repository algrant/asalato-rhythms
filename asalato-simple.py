# Generate lists of "interesting" asalato two handed rhythms

moves = {
    # heli
    "h": [0, 0],
    # den den
    "dd": [1, 0, 1, 0],
    # air turn
    "at": [1, 0, 0, 0],
    # flip flop
    "ffg": [1, 0, 0, 1, 0, 0],
}

moves_with_reverse_helis = {
    # flip flop with reverse heli
    "frfg": [1, 0, 0, 0, 0, 1, 0, 0],
    # den den with reverse heli
    "drd": [1, 0, 0, 0, 1, 0],
}


class AsalatoRhythm:
    def __init__(self, move_list):
        self.move_list = move_list

    def splits(self):
        i = 0
        splits = []
        for move in self.move_list[:-1]:
            i += len(move)
            splits.append(i)
        return set(splits)

    def length(self):
        return sum([len(move) for move in self.move_list])

    def clicks(self):
        return [beat for move in self.move_list for beat in moves[move]]

    def __repr__(self):
        x = "".join(self.move_list)
        return f"<{x}>"

    @staticmethod
    def rhythms_of_length(n):
        def helper(n):
            out = []

            for move in moves.keys():
                if len(move) == n:
                    out.append([move])
                elif len(move) < n:
                    for move_list in helper(n - len(move)):
                        out.append([move] + move_list)

            return out

        return [AsalatoRhythm(move_list) for move_list in helper(n)]


class AsalatoTwoHand:
    def __init__(self, left: AsalatoRhythm, right: AsalatoRhythm):
        self.left = left
        self.right = right

    def is_unique(self):
        return len(self.left.splits().intersection(self.right.splits())) == 0

    def click_string(self, chars="X/\\ "):
        left = self.left.clicks()
        right = self.right.clicks()

        clicks = ""

        for i in range(len(left)):
            if left[i] and right[i]:
                clicks += chars[0]
            elif left[i]:
                clicks += chars[1]
            elif right[i]:
                clicks += chars[2]
            else:
                clicks += chars[3]

        return clicks

    def hashed_string(self):
        reg = self.click_string("abbc")
        reg2 = reg + reg
        best = reg
        for i in range(len(reg)):
            n = reg2[i: i + len(reg)]
            if n < best:
                best = n

        return best

    def __repr__(self):
        left_moves = " ".join(list("".join(self.left.move_list)))

        right_moves = " ".join(list("".join(self.right.move_list)))

        return f"  {left_moves}\n  { self.click_string() } \n  {right_moves}\n"

    @staticmethod
    def unique_rhythms_of_length(n):
        rhythms = AsalatoRhythm.rhythms_of_length(n)
        rhythm_hash = {}

        for e, left in enumerate(rhythms):
            for right in rhythms[e:]:
                new_rhythm = AsalatoTwoHand(left, right)

                if new_rhythm.is_unique():
                    new_hash = new_rhythm.hashed_string()
                    if new_hash not in rhythm_hash:
                        rhythm_hash[new_hash] = []
                    rhythm_hash[new_hash].append(new_rhythm)

        return rhythm_hash


if __name__ == "__main__":
    rhythm_hash = AsalatoTwoHand.unique_rhythms_of_length(4)

    for n, vals in enumerate(rhythm_hash.values()):
        print(f"{n + 1}.")
        for v in vals:
            print(v)
