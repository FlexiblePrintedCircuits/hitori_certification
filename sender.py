import numpy as np

class Sender():
	def __init__(self, s1, s2):
		"""
		s1 とs2 はセキュリティパラメータ
		s1が盤面の大きさで, s2が盤面で使用する数字の種類の数である.
		"""
		self.s1 = s1
		self.s2 = s2
		self.problem_board = [
			[1, 1, 2, 4, 3, 5],
			[1, 1, 5, 4, 4, 6],
			[4, 6, 6, 2, 1, 1],
			[6, 3, 3, 3, 5, 4],
			[2, 3, 4, 1, 6, 5],
			[2, 5, 4, 6, 2, 5]
		]
		self.black_board = [
			[0, 1, 2, 4, 3, 0],
			[1, 0, 5, 0, 4, 6],
			[4, 6, 0, 2, 1, 0],
			[6, 0, 3, 0, 5, 4],
			[2, 3, 4, 1, 6, 5],
			[0, 5, 0, 6, 2, 0]
		]

	def create_board(self):	# 未完成
		"""
		解答となる盤面を作成するメソッド
		"""

		board = [[0] * self.s1 for i in range(self.s1)]	# s1 の大きさで, 0で初期化された2次元リストを作成する

		for row in board:
			"""
			縦列は考慮せずに, 横列だけで数字の被りがないように盤面を作成する.
			盤面の2次元リストは0で初期化しているので, 黒マスは0にする.
			"""

			use_number_list = list(range(1, self.s2 + 1))	# 盤面で使用する数字のリストを作成する. s2が6なら, 1から6までの数字が列挙されたリストを生成.

			for index, value in enumerate(row):
				is_black = np.random.choice([True, False], p=[0.3, 0.7])	# 30% の確率で盤面を黒にする. 30% という数字は適当に決めた.
				if not is_black:	# もし盤面を黒マスにしないのなら, use_number_list からランダムな数字をマスに入れる.
					try:
						number = np.random.choice(use_number_list)
						row[index] = number
						use_number_list.remove(number)	# 同じ横列に同じ数字が並んでいたら解答となる盤面にならないので、1度使用した数字は消す.
					except:
						break
			# 【issue】上の処理では, 確率的に適当に黒マスにするか白マスにするか決めているため, 黒マスが連続する可能性がある.

		"""
		上の処理だけだと, 同じ数字が入ってないかどうかについて横列しか考慮してないので, この処理で縦列についての処理をしたかった.
		for index, value in enumerate(board):
			#row = board[index]
			column = [r[index] for r in board]
			dup = [x for x in set(column) if column.count(x) > 1]
		"""

	def create_prism(self):
		"""
		盤面を共通の最大素因数の合成数に変換するための、素数リストを作成するメソッド
		"""
		tmp = self.s2 * 10000
		prime_list = []
		for i in range(1000, tmp):
			isPrism = True
			for num in range(2, i):
				if (i % num == 0):
					isPrism = False
			if isPrism:
				prime_list.append(i)
			if (len(prime_list) == self.s2):
				break
		return prime_list

	def max_prime_factor(self, num):
		"""
		引数num の最大素因数を計算するメソッド
		"""

		prisms = []
		for i in range(2, num + 1):
			while num % i == 0:
				prisms.append(i)
				num = num / i
		return max(prisms)

	def put_the_board_back(self, board):
		"""
		盤面の合成数を, 共通の最大素因数に変換するメソッド
		"""

		self.before_calculation_board = []	# 合成数を計算する前の, 素因数のみの盤面
		for row in board:
			self.before_calculation_board.append(
				[self.max_prime_factor(num) for num in row]
			)

	def match_the_board(self):
		"""
		解答となる盤面の, 黒マス以外の各数字を素因数のものに変換するメソッド
		"""
		for index1, value1 in enumerate(self.before_calculation_board):
			for index2, value2 in enumerate(self.before_calculation_board[index1]):
				if (self.black_board[index1][index2] != 0):
					self.black_board[index1][index2] = self.before_calculation_board[index1][index2]

	def convert_board(self):
		"""
		盤面のそれぞれの数字に対して、共通の最大素因数の合成数に変換するメソッド
		"""
		prime_list = self.create_prism()
		for target_number_of_conversion in range(1, self.s2 + 1):	# この3重ループ計算量おおくね？？直す気力があったら直したい.
			counter = 1
			for row in self.problem_board:
				for index, value in enumerate(row):
					if value == target_number_of_conversion:
						row[index] = prime_list[0] * counter
						counter += 1
			prime_list.remove(prime_list[0])

		self.put_the_board_back(self.problem_board)
		self.match_the_board()
		return self.problem_board

	def encrypt_problem_board(self, public_key):
		"""
		盤面を暗号化するメソッド
		"""
		E, N = public_key
		encrypt_board = []
		for board_row in self.problem_board:
			encrypt_board.append(
				[pow(i, E, N) for i in board_row]
			)
		return encrypt_board
