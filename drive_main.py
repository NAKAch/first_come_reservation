from src.backend.drive_site import DriveSite
from src.database.db import DBManager

class DriveManager:
    def __init__(self):
        """DBManagerインスタンスを初期化"""
        self.db = DBManager()
        self.db.create_tables()  # テーブルを作成

    def get_user_id_list_info(self):
        """ユーザー情報を取得"""
        user_id_list = self.db.get_user_id_list()
        return user_id_list

    def drive(self, user_id_list):
        """ユーザーごとの予約を処理"""
        for user_id_tuple in user_id_list:
            user_id = user_id_tuple[0]
            url = "https://g-kyoto.pref.kyoto.lg.jp/reserve_j/core_i/init.asp?SBT=1"
            user_password = self.db.get_user_password(user_id)[0]
            park = self.db.get_park(user_id)[0]
            lots = self.db.get_lot_by_user_id_and_incomplete(user_id)

            # DriveSiteのインスタンスを生成して処理
            drive_site = DriveSite(url=url, user_id=user_id, user_password=user_password, park=park, lots=lots)
            results = drive_site.drive()

            # 結果をデータベースに反映
            for result in results:
                result_user_id = result[0]
                result_date = result[1]
                result_time_slot = result[2]
                result_status = result[3]
                lots_id = self.db.get_lots_id_by_user_id_and_date_and_time_slot(result_user_id, result_date, result_time_slot)[0]
                self.db.update_lots_status(lots_id=lots_id, new_status=result_status)

if __name__ == '__main__':
    # DriveManagerのインスタンスを生成
    drive_manager = DriveManager()

    # ユーザー情報を取得して処理を実行
    user_id_list = drive_manager.get_user_id_list_info()
    drive_manager.drive(user_id_list)