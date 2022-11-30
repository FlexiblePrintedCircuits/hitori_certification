class Verifier():
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

		self.undo_board = []
		for row in board:
			self.undo_board.append(
				[self.max_prime_factor(num) for num in row]
			)
		return self.undo_board

	def verification(self, board):
		"""
		送られてきた解答となる盤面が解答として成立しているかチェック
		"""
		is_ok = True
		for row in board:	# 横列で0(黒マス)以外に重複がないかチェック
			dup = [x for i, x in enumerate(row) if i != row.index(x)]	# リストの中で重複した要素を取り出す
			if len(dup) != 0:
				for i in dup:
					if i != 0:
						is_ok = False

		# 縦列の2次元リストを作る
		column_list = []
		board_len = len(board)
		for i in range(board_len):
			column_list.append(
				[r[i] for r in board]
			)

		for column in column_list:	# 縦列で0(黒マス)以外に重複がないかチェック
			dup = [x for i, x in enumerate(column) if i != column.index(x)]
			if len(dup) != 0:
				for i in dup:
					if i != 0:
						is_ok = False

		for row in board:	# 横列で同じ値が, 黒マス含め連続していないかチェック
			for index, value in enumerate(row):
				try:
					if (row[index] == row[index + 1]):
						is_ok = False
				except:
					pass

		for column in column_list:	# 縦列で同じ値が, 黒マス含め連続していないかチェック
			for index, value in enumerate(column):
				try:
					if (column[index] == column[index + 1]):
						is_ok = False
				except:
					pass

		for index1, value1 in enumerate(self.undo_board):	# 送られてきた解答の盤面が、認証フローの最初から使われてきた盤面のものなのかチェック
			for index2, value2, in enumerate(self.undo_board[index1]):
				if (board[index1][index2] != 0):
					if (board[index1][index2] != self.undo_board[index1][index2]):
						is_ok = False

		return is_ok