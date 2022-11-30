from math import gcd
import random

class CertificateAuthority():

    def lcm(self, p, q):
        """
        最小公倍数を求めるメソッド
        """
        return (p * q) // gcd(p, q)

    def generate_random_prism(self, x, y):
        """
        int型の引数xからyの間でランダムな素数2つを求めて返すメソッド
        """
        prime_list = []
        for n in range(x, y):
            isPrime = True

            for num in range(2, n):
                if n % num == 0:
                    isPrime = False

            if isPrime:
                prime_list.append(n)

        randomPrime1 = random.choice(prime_list)
        prime_list.remove(randomPrime1)
        randomPrime2 = random.choice(prime_list)
        return (randomPrime1, randomPrime2)

    def generate_keys(self):
        """
        公開鍵と秘密鍵を計算するメソッド
        公開鍵及び秘密鍵はCAで管理するため、メンバとして登録する
        送信者には公開鍵のみ返す
        """
        p, q = self.generate_random_prism(
            200, 500)  # 200から500の間でランダムな素数2つを取得する. この200と500という数字は適当だが、送信者側で指定すべきだろうか？
        N = p * q
        L = self.lcm(p - 1, q - 1)

        for i in range(2, L):
            if gcd(i, L) == 1:
                E = i
                break

        for i in range(2, L):
            if (E * i) % L == 1:
                D = i
                break

        self.public_key = E
        self.private_key = D
        self.n = N

        return (E, N)  # 公開鍵のみを返す

    def decrypt(self, board):
        """
        盤面を復号して返すメソッド
        """
        decrypted_board = []
        for board_row in board:
            decrypted_board.append(
                [pow(i, self.private_key, self.n) for i in board_row]
            )
        return decrypted_board
