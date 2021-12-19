class Earley:
    def __init__(self):
        self.D = []
        self.E = []
        self.N = ['S1']
        self.P = dict()
        self.from_net_symb_to_int = dict()
        self.start_symb = ''

    class State:
        neterminal_from = 0
        left = []  # before dot pairs (N, j),(N, k),(E, t),...
        right = []  # after dot pairs (N, j),(N, k),(E, t),...
        i = 0

        def __init__(self):
            self.neterminal_from = 0
            self.left = []
            self.right = []
            self.i = 0

    def fit(self, G):
        n = G['kol_neterms']
        e = G['kol_terms']
        p = G['kol_rules']
        self.from_net_symb_to_int['S1'] = 0
        for i in range(n):
            symb = G['neterms'][i]
            if symb in self.N:
                continue
            self.from_net_symb_to_int[symb] = i + 1
            self.N.append(symb)
            self.P[symb] = []
        alphabet = G['alphabet']
        for elem in alphabet:
            self.E.append(elem)
        for i in range(p):
            rule = G['rules'][i]
            arr = rule.split('->')
            arr_right_part = []
            for elem in arr[1]:
                if elem in self.N:
                    arr_right_part.append(['N', self.N.index(elem)])
                else:
                    arr_right_part.append(['E', self.E.index(elem)])
            self.P[arr[0]].append(arr_right_part)
        self.start_symb = G['start_symbol']

        return

    def scan(self, j, w):
        for a in self.E:
            if a not in self.D[j]:
                continue
            for st in self.D[j][a]:
                if a == w[j]:
                    new_st = self.State()
                    new_st.right = st.right.copy()
                    new_st.left = st.left.copy()
                    new_st.i = st.i
                    new_st.neterminal_from = st.neterminal_from
                    if not new_st.right:
                        if new_st not in self.D[j + 1]['$']:
                            self.D[j + 1]['$'].append(new_st)
                        continue
                    new_st.left.append(new_st.right[0])
                    new_st.right.pop(0)
                    if not new_st.right:
                        if new_st not in self.D[j + 1]['$']:
                            self.D[j + 1]['$'].append(new_st)
                        continue
                    beta = new_st.right[0].copy()
                    if beta[0] == 'N':
                        beta = self.N[beta[1]]
                    else:
                        beta = self.E[beta[1]]
                    if st in self.D[j + 1][beta]:
                        continue
                    self.D[j + 1][beta].append(new_st)

    def complete(self, j, w):
        for st in self.D[j]['$']:
            i = st.i
            neterm = st.neterminal_from
            for rul in self.D[i][self.N[neterm]]:
                new_st = self.State()
                new_st.right = rul.right.copy()
                new_st.left = rul.left.copy()
                new_st.i = rul.i
                new_st.neterminal_from = rul.neterminal_from
                if not new_st.right:
                    if new_st not in self.D[j]['$']:
                        self.D[j]['$'].append(new_st)
                    continue
                new_st.left.append(new_st.right[0])
                new_st.right.pop(0)
                first_symb_after_dot = ''
                if not new_st.right:
                    if new_st not in self.D[j]['$']:
                        self.D[j]['$'].append(new_st)
                    continue
                if new_st.right[0][0] == 'N':
                    first_symb_after_dot = self.N[new_st.right[0][1]]
                else:
                    first_symb_after_dot = self.E[new_st.right[0][1]]
                if new_st in self.D[j][first_symb_after_dot]:
                    continue
                self.D[j][first_symb_after_dot].append(new_st)

    def predict(self, j, w):
        for neterm in self.N:
            if neterm not in self.D[j]:
                continue
            for st in self.D[j][neterm]:
                for rule in self.P[neterm]:
                    new_st = self.State()
                    new_st.neterminal_from = self.from_net_symb_to_int[neterm]
                    new_st.i = j
                    new_st.left = []
                    new_st.right = rule.copy()
                    first_symb_after_dot = ''
                    if not new_st.right:
                        if new_st not in self.D[j]['$']:
                            self.D[j]['$'].append(new_st)
                        continue
                    if new_st.right[0][0] == 'N':
                        first_symb_after_dot = self.N[new_st.right[0][1]]
                    else:
                        first_symb_after_dot = self.E[new_st.right[0][1]]
                    if first_symb_after_dot not in self.D[j]:
                        self.D[j][first_symb_after_dot] = []
                    fl = 0
                    for elem in self.D[j][first_symb_after_dot]:
                        if new_st.i == elem.i and new_st.right == elem.right and new_st.left == elem.left and new_st.neterminal_from == elem.neterminal_from:
                            fl = 1
                            break
                    if fl:
                        continue
                    self.D[j][first_symb_after_dot].append(new_st)

    def predict_result(self, word):
        for symb in word:
            if symb not in self.E:
                return False
        self.D = [None] * (len(word) + 1)
        for i in range(len(word) + 1):
            self.D[i] = dict()
        first = self.State()
        first.neterminal_from = 0
        first.i = 0
        first.left = []
        first.right = [['N', self.from_net_symb_to_int[self.start_symb]]]
        self.D[0][self.start_symb] = [first]
        self.D[0]['S1'] = []
        # D[0][S] = {[S′→⋅ S,0]}
        for i in range(1, len(word) + 1):
            for a in self.E:
                self.D[i][a] = []
            for A in self.N:
                self.D[i][A] = []
            self.D[i]['$'] = []
        self.D[0]['$'] = []

        while 1:
            tmp = self.D[0].copy()
            self.predict(0, word)
            self.complete(0, word)
            if tmp == self.D[0]:
                break
        for j in range(1, len(word) + 1):
            self.scan(j - 1, word)
            while 1:
                tmp = self.D[j].copy()
                self.predict(j, word)
                self.complete(j, word)
                if self.D[j] == tmp:
                    break
        last_st = self.State()
        last_st.right = []
        last_st.left = [['N', self.from_net_symb_to_int[self.start_symb]]]
        last_st.neterminal_from = 0
        last_st.i = 0
        for elem in self.D[len(word)]['$']:
            if last_st.i == elem.i and last_st.right == elem.right and last_st.left == elem.left and last_st.neterminal_from == elem.neterminal_from:
                return True
        return False


'''def input_data(G):
    G['kol_neterms'], G['kol_terms'], G['kol_rules'] = map(int, input().split())
    G['neterms'] = input()
    G['alphabet'] = input()
    G['rules'] = []
    for i in range(G['kol_rules']):
        G['rules'].append(input())
    G['start_symbol'] = input()


def main():
    t = Earley()
    G = dict()
    input_data(G)
    t.fit(G)
    m = int(input())
    for i in range(m):
        w = input()

        if t.predict_result(w):
            print("YES")
        else:
            print("NO")


main()'''
