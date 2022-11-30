from sender import Sender
from ca import CertificateAuthority
from verifier import Verifier

import copy

ca_ins = CertificateAuthority()	# 認証局のインスタンス
sendr_ins = Sender(6, 6)	# 送信者のインスタンス
verifier_ins = Verifier()	# 検証者のインスタンス


# STEP 1 : 公開鍵と秘密鍵の作成
public_key = ca_ins.generate_keys()
print("【認証局】公開鍵と秘密鍵の作成 DONE")
print("")

print("【送信者】解答となる盤面:")
for i in sendr_ins.black_board:
	print(i)
print("")

print("【送信者】問題となる盤面:")
for i in sendr_ins.problem_board:
	print(i)
print("")

# STEP 2 : 盤面を共通の最大素因数の合成数に変換
board = sendr_ins.convert_board()
print("【送信者】各数字を, 共通の最大素因数の合成数に変換した盤面:")
for i in board:
	print(i)
print("")

# STEP 3 : 盤面の暗号化
encrypt_board = sendr_ins.encrypt_problem_board(public_key)
print("【送信者】暗号化した盤面:")
for i in encrypt_board:
	print(i)
print("")

# STEP 4 : 認証局による盤面の復号化
decrypted_board = ca_ins.decrypt(encrypt_board)
print("【認証局】復号化した盤面:")
for i in decrypted_board:
	print(i)
print("")

# STEP 5 : 検証者による盤面の各数字を共通最大素因数に変換
undo_board = verifier_ins.put_the_board_back(decrypted_board)
print("【検証者】盤面の各数字を共通最大素因数に変換した盤面:")
for i in undo_board:
	print(i)
print("")

# STEP 6 : 最初に送られた盤面に対して, 解答となる盤面が成立しているか検証
is_ok = verifier_ins.verification(sendr_ins.black_board)
print("【検証者】最初に送られた盤面に対して, 解答となる盤面が成立しているか検証")
print("")

print("############################################")
if is_ok:
	print("認証結果 : OK")
else:
	print("認証結果 : NG")
print("############################################")
print("")

# テスト : 不正な解答を検証者に送った場合
print("【テスト】不正な解答を検証者に送った場合")
bad_board = copy.copy(sendr_ins.black_board)
bad_board[0][0] = 1
print("検証者に送る不正な盤面:")
for i in bad_board:
	print(i)
print("")
is_ok = verifier_ins.verification(bad_board)
print("############################################")
if is_ok:
	print("認証結果 : OK")
else:
	print("認証結果 : NG")
print("############################################")
