import sqlite3

class DBManager:
    def __init__(self, db_name='reservation.db'):
        self.db_name = db_name

    def connect_db(self):
        """データベース接続を管理する関数"""
        return sqlite3.connect(self.db_name)

    def create_tables(self):
        """usersテーブルとlotsテーブルを作成する関数"""
        conn = self.connect_db()
        cursor = conn.cursor()

        # usersテーブルの作成
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT NOT NULL UNIQUE,
            user_password TEXT NOT NULL,
            park TEXT NOT NULL
        )
        ''')

        # lotsテーブルの作成（予約ステータスを追加）
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS lots (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT,
            date TEXT NOT NULL,
            time_slot TEXT NOT NULL,
            status TEXT DEFAULT '未完了',  -- 予約ステータスのカラム（初期値: "未完了"）
            FOREIGN KEY(user_id) REFERENCES users(user_id) ON DELETE CASCADE
        )
        ''')

        conn.commit()
        conn.close()

    def insert_user(self, user_id, password, park):
        """ユーザーを追加する関数"""
        conn = self.connect_db()
        cursor = conn.cursor()
        cursor.execute('''
        INSERT INTO users (user_id, user_password, park) 
        VALUES (?, ?, ?)
        ''', (user_id, password, park))
        conn.commit()
        conn.close()

    def insert_lot(self, user_id, date, time_slot):
        """予約情報(lots)を追加する関数（ステータスはデフォルトで"未完了"）"""
        conn = self.connect_db()
        cursor = conn.cursor()
        cursor.execute('''
        INSERT INTO lots (user_id, date, time_slot)
        VALUES (?, ?, ?)
        ''', (user_id, date, time_slot))
        conn.commit()
        conn.close()

    def get_lots_id_by_user_id_and_date_and_time_slot(self, user_id, date, time_slot):
        """ユーザーID、日付、時間帯から予約IDを取得する関数"""
        conn = self.connect_db()
        cursor = conn.cursor()
        cursor.execute('''
        SELECT id FROM lots WHERE user_id = ? AND date = ? AND time_slot = ?
        ''', (user_id, date, time_slot))
        lots_id = cursor.fetchone()
        conn.close()
        return lots_id

    def update_lots_status(self, lots_id, new_status):
        """予約のステータスを更新する関数"""
        conn = self.connect_db()
        cursor = conn.cursor()
        cursor.execute('''
        UPDATE lots SET status = ? WHERE id = ?
        ''', (new_status, lots_id))
        conn.commit()
        conn.close()

    def get_all_users(self):
        """すべてのユーザーを取得する関数"""
        conn = self.connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users")
        users = cursor.fetchall()
        conn.close()
        return users

    def get_all_lots(self):
        """すべての予約情報(lots)を取得する関数"""
        conn = self.connect_db()
        cursor = conn.cursor()
        cursor.execute('''
        SELECT lots.id, users.user_id, lots.date, lots.time_slot, lots.status
        FROM lots 
        JOIN users ON lots.user_id = users.user_id
        ''')
        lots = cursor.fetchall()
        conn.close()
        return lots

    def get_lot_by_user_id(self, user_id):
        """ユーザーIDで予約情報(lots)を取得する関数"""
        conn = self.connect_db()
        cursor = conn.cursor()
        cursor.execute('''
        SELECT * FROM lots WHERE user_id = ?
        ''', (user_id,))
        lots = cursor.fetchall()
        conn.close()
        return lots

    def get_lot_by_user_id_and_incomplete(self, user_id):
        """未完了の予約を取得する関数"""
        conn = self.connect_db()
        cursor = conn.cursor()
        cursor.execute('''
        SELECT date, time_slot FROM lots WHERE user_id = ? AND status = "未完了"
        ''', (user_id,))
        lots = cursor.fetchall()
        conn.close()
        return lots

    def get_user_id_list(self):
        """ユーザーIDのリストを取得する関数"""
        conn = self.connect_db()
        cursor = conn.cursor()
        cursor.execute('''
        SELECT user_id FROM users
        ''')
        user_id_list = cursor.fetchall()
        conn.close()
        return user_id_list

    def get_user_password(self, user_id):
        """ユーザーIDからパスワードを取得する関数"""
        conn = self.connect_db()
        cursor = conn.cursor()
        cursor.execute('''
        SELECT user_password FROM users WHERE user_id = ?
        ''', (user_id,))
        user_password = cursor.fetchone()
        conn.close()
        return user_password

    def get_park(self, user_id):
        """ユーザーIDから公園を取得する関数"""
        conn = self.connect_db()
        cursor = conn.cursor()
        cursor.execute('''
        SELECT park FROM users WHERE user_id = ?
        ''', (user_id,))
        park = cursor.fetchone()
        conn.close()
        return park
    
    def delete_user_table(self):
        """usersテーブルを削除する関数"""
        conn = self.connect_db()
        cursor = conn.cursor()
        cursor.execute('''
        DROP TABLE IF EXISTS users
        ''')
        conn.commit()
        conn.close()

    def delete_lots_table(self):
        """lotsテーブルを削除する関数"""
        conn = self.connect_db()
        cursor = conn.cursor()
        cursor.execute('''
        DROP TABLE IF EXISTS lots
        ''')
        conn.commit()
        conn.close()

    def insert_test_data(self):
        """テストデータを挿入する関数"""
        self.insert_user("E00057123", "yutotct34", "宝")
        self.insert_lot("E00057123", "2024年10月20日", "10~12")
        self.insert_lot("E00057123", "2024年10月20日", "0~2")
        self.insert_lot("E00057123", "2024年10月21日", "2~4")
        self.insert_lot("E00057123", "2024年11月3日", "6~9")
        self.insert_user("E00057145", "z7tdgu7x", "岡崎")
        self.insert_lot("E00057145", "2024年10月20日", "10~12")
        self.insert_lot("E00057145", "2024年10月20日", "0~2")
        self.insert_lot("E00057145", "2024年10月21日", "2~4")
        self.insert_lot("E00057145", "2024年11月3日", "6~9")

    def update_lot(self, lot_id, user_id, date, time_slot, status):
        """予約情報を更新する関数"""
        conn = self.connect_db()
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE lots
            SET user_id = ?, date = ?, time_slot = ?, status = ?
            WHERE id = ?
        ''', (user_id, date, time_slot, status, lot_id))
        conn.commit()
        conn.close()

    def delete_lot(self, lot_id):
        """指定された予約IDの予約を削除する"""
        conn = self.connect_db()
        cursor = conn.cursor()

        # 削除する予約に紐づくuser_idを取得
        cursor.execute("SELECT user_id FROM lots WHERE id = ?", (lot_id,))
        user_id = cursor.fetchone()[0]

        # 予約を削除
        cursor.execute("DELETE FROM lots WHERE id = ?", (lot_id,))
        conn.commit()

        # そのユーザーが他の予約を持っていないか確認
        cursor.execute("SELECT COUNT(*) FROM lots WHERE user_id = ?", (user_id,))
        lot_count = cursor.fetchone()[0]

        # 他に予約がない場合はUsersからも削除
        if lot_count == 0:
            cursor.execute("DELETE FROM users WHERE user_id = ?", (user_id,))
            conn.commit()

        conn.close()

# 実行部分
if __name__ == '__main__':
    db_manager = DBManager()

    # テーブルを作成
    db_manager.create_tables()



    # サンプルデータを挿入
    # db_manager.insert_test_data()

    # データを取得して表示
    users = db_manager.get_all_users()
    print("Users:", users)

    lots = db_manager.get_all_lots()
    print("Lots:", lots)

    user_id_list = db_manager.get_user_id_list()
    # 予約のステータスを「完了」に変更する例
    # db_manager.update_lots_status(1, "完了")

    # 更新後の予約情報を取得して表示
    lot_by_user_id_and_incomplete = db_manager.get_lot_by_user_id_and_incomplete("E00057145")
    print("Lots by user_id:", lot_by_user_id_and_incomplete)
    print("value(lot_by_user_id):", lot_by_user_id_and_incomplete)
    print(f"type(lot_by_user_id): {type(lot_by_user_id_and_incomplete)}")
    print(f"user list: {user_id_list}")
    print(f"value(user list): {user_id_list[0][0]}")
    print(f"type(user list): {type(user_id_list[0][0])}")

    # テーブルを削除
    # db_manager.delete_user_table()
    # db_manager.delete_lots_table()