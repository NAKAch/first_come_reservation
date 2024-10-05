import tkinter as tk
from tkinter import messagebox, ttk
from tkcalendar import Calendar
from src.database.db import DBManager  # DBManager のインポート

class Application:
    def __init__(self, root):
        self.root = root
        self.db_manager = DBManager()

        self.root.title("Reservation Management")
        self.root.geometry("600x600")

        # 最初の画面を表示
        self.show_main_menu()

    def show_main_menu(self):
        """最初の画面を表示"""
        self.clear_frame()

        # ラベル
        self.label = tk.Label(self.root, text="Reservation Management System", font=("Arial", 16))
        self.label.pack(pady=20)

        # 選択肢ボタン
        self.option1_button = tk.Button(self.root, text="① ユーザー追加と予約の追加", command=self.show_add_user)
        self.option1_button.pack(pady=10)

        self.option2_button = tk.Button(self.root, text="② データベース確認・編集・削除", command=self.show_edit_database)
        self.option2_button.pack(pady=10)

    def show_add_user(self):
        """ユーザー情報の追加画面を表示"""
        self.clear_frame()

        self.label = tk.Label(self.root, text="ユーザー追加", font=("Arial", 14))
        self.label.pack(pady=10)

        # ユーザーID入力
        self.user_id_label = tk.Label(self.root, text="User ID:")
        self.user_id_label.pack(pady=5)
        self.user_id_entry = tk.Entry(self.root)
        self.user_id_entry.pack(pady=5)

        # パスワード入力（隠さない）
        self.password_label = tk.Label(self.root, text="Password:")
        self.password_label.pack(pady=5)
        self.password_entry = tk.Entry(self.root)  # パスワードを隠さない
        self.password_entry.pack(pady=5)

        # 公園選択
        self.park_label = tk.Label(self.root, text="Park:")
        self.park_label.pack(pady=5)
        self.park_combobox = ttk.Combobox(self.root, values=["岡崎", "宝"], state="readonly")
        self.park_combobox.pack(pady=5)

        # OKボタンと戻るボタン
        self.ok_button = tk.Button(self.root, text="OK", command=self.store_user_info)
        self.ok_button.pack(pady=10)

        self.back_button = tk.Button(self.root, text="戻る", command=self.show_main_menu)
        self.back_button.pack(pady=10)

    def store_user_info(self):
        """ユーザー情報を一時的に保存し、次の予約情報画面に移行"""
        self.user_id = self.user_id_entry.get()
        self.password = self.password_entry.get()
        self.park = self.park_combobox.get()

        if self.user_id and self.password and self.park:
            # ユーザー情報が正しく入力されたら、予約情報の入力画面へ
            self.show_add_lot()
        else:
            messagebox.showerror("Error", "すべての項目を入力してください。")

    def show_add_lot(self):
        """予約情報の追加画面を表示"""
        self.clear_frame()

        self.label = tk.Label(self.root, text="予約情報の追加", font=("Arial", 14))
        self.label.pack(pady=10)

        # カレンダーウィジェットで日付選択
        self.date_label = tk.Label(self.root, text="Date:")
        self.date_label.pack(pady=5)
        self.calendar = Calendar(self.root, selectmode='day', date_pattern='yyyy-mm-dd')
        self.calendar.pack(pady=5)

        # 時間帯選択
        self.timeslot_label = tk.Label(self.root, text="Time Slot:")
        self.timeslot_label.pack(pady=5)
        self.timeslot_combobox = ttk.Combobox(self.root, values=["8~10", "10~12", "0~2", "2~4", "4~6", "6~9"], state="readonly")
        self.timeslot_combobox.pack(pady=5)

        # 予約のリストを表示するリストボックス
        self.listbox_label = tk.Label(self.root, text="Selected Dates and Time Slots:")
        self.listbox_label.pack(pady=5)
        self.listbox = tk.Listbox(self.root, height=5)
        self.listbox.pack(pady=5)

        # 日付と時間帯の追加ボタン
        self.add_button = tk.Button(self.root, text="Add Date & Time Slot", command=self.add_date_and_timeslot)
        self.add_button.pack(pady=5)

        # OKボタンと戻るボタン
        self.ok_button = tk.Button(self.root, text="Save All", command=self.add_user_and_lots)
        self.ok_button.pack(pady=10)

        self.back_button = tk.Button(self.root, text="戻る", command=self.show_main_menu)
        self.back_button.pack(pady=10)

    def add_date_and_timeslot(self):
        """選択された日付と時間帯をリストに追加"""
        date = self.calendar.get_date()
        formatted_date = self.format_date_to_japanese(date)  # 日付をフォーマット

        timeslot = self.timeslot_combobox.get()

        if formatted_date and timeslot:
            # 日付と時間帯をリストに追加
            self.listbox.insert(tk.END, f"Date: {formatted_date}, Time Slot: {timeslot}")
            self.timeslot_combobox.set("")  # 時間帯選択をクリア
        else:
            messagebox.showerror("Error", "日付と時間帯を選択してください。")

    def format_date_to_japanese(self, date):
        """日付を yyyy-mm-dd から yyyy年mm月dd日 形式に変換"""
        year, month, day = date.split('-')
        return f"{year}年{month}月{day}日"

    def add_user_and_lots(self):
        """ユーザーと複数の予約情報をデータベースに追加する"""
        if self.listbox.size() > 0:
            # ユーザー情報をデータベースに保存
            self.db_manager.insert_user(self.user_id, self.password, self.park)

            # 追加された複数の予約情報を保存
            for item in self.listbox.get(0, tk.END):
                date, timeslot = item.replace("Date: ", "").replace("Time Slot: ", "").split(", ")
                self.db_manager.insert_lot(self.user_id, date, timeslot)

            messagebox.showinfo("Success", "ユーザーと予約情報が追加されました。")
            self.show_main_menu()  # メインメニューに戻る
        else:
            messagebox.showerror("Error", "少なくとも1つの予約情報を追加してください。")

    def show_edit_database(self):
        """データベース編集・削除画面を表示"""
        self.clear_frame()

        self.label = tk.Label(self.root, text="データベース確認・編集・削除", font=("Arial", 14))
        self.label.pack(pady=10)

        # データベースから予約情報を取得
        lots = self.db_manager.get_all_lots()

        # Treeviewを作成して表示
        self.tree = ttk.Treeview(self.root, columns=("ID", "User ID", "Date", "Time Slot", "Status"), show="headings")
        self.tree.heading("ID", text="ID")
        self.tree.heading("User ID", text="User ID")
        self.tree.heading("Date", text="Date")
        self.tree.heading("Time Slot", text="Time Slot")
        self.tree.heading("Status", text="Status")

        for lot in lots:
            self.tree.insert("", "end", values=lot)

        self.tree.pack(pady=10, fill=tk.BOTH, expand=True)

        # 編集ボタン
        self.edit_button = tk.Button(self.root, text="編集", command=self.edit_selected_row)
        self.edit_button.pack(pady=5)

        # 削除ボタン
        self.delete_button = tk.Button(self.root, text="削除", command=self.delete_selected_row)
        self.delete_button.pack(pady=5)

        # データベース全削除ボタン
        self.delete_all_button = tk.Button(self.root, text="全データ削除", command=self.confirm_delete_all_data)
        self.delete_all_button.pack(pady=5)

        # OKボタンと戻るボタン
        self.ok_button = tk.Button(self.root, text="OK", command=self.show_main_menu)
        self.ok_button.pack(pady=10)

    def confirm_delete_all_data(self):
        """全データ削除の確認ウィンドウを表示"""
        self.confirm_window = tk.Toplevel(self.root)
        self.confirm_window.title("確認")

        label = tk.Label(self.confirm_window, text="本当に全データを削除してもよいですか？")
        label.pack(pady=10)

        # 「削除する」ボタン
        delete_button = tk.Button(self.confirm_window, text="削除する", command=self.delete_all_data)
        delete_button.pack(pady=5)

        # 「キャンセル」ボタン
        cancel_button = tk.Button(self.confirm_window, text="キャンセル", command=self.confirm_window.destroy)
        cancel_button.pack(pady=5)

    def delete_all_data(self):
        """全データを削除する処理"""
        self.db_manager.delete_user_table()
        self.db_manager.delete_lots_table()
        self.db_manager.create_tables()  # 空のテーブルを再作成
        messagebox.showinfo("Success", "すべてのデータが削除されました。")
        self.confirm_window.destroy()  # 確認ウィンドウを閉じる
        self.show_main_menu()  # メインメニューに戻る

    def edit_selected_row(self):
        """選択された行を編集"""
        selected_item = self.tree.selection()

        if selected_item:
            # 選択された行のデータを取得
            values = self.tree.item(selected_item, "values")

            # ダイアログで編集を行う
            self.edit_window = tk.Toplevel(self.root)
            self.edit_window.title("編集")

            # User ID
            tk.Label(self.edit_window, text="User ID").grid(row=0, column=0)
            self.edit_user_id = tk.Entry(self.edit_window)
            self.edit_user_id.grid(row=0, column=1)
            self.edit_user_id.insert(0, values[1])

            # Date
            tk.Label(self.edit_window, text="Date").grid(row=1, column=0)
            self.edit_date = tk.Entry(self.edit_window)
            self.edit_date.grid(row=1, column=1)
            self.edit_date.insert(0, values[2])

            # Time Slot
            tk.Label(self.edit_window, text="Time Slot").grid(row=2, column=0)
            self.edit_time_slot = tk.Entry(self.edit_window)
            self.edit_time_slot.grid(row=2, column=1)
            self.edit_time_slot.insert(0, values[3])

            # Status
            tk.Label(self.edit_window, text="Status").grid(row=3, column=0)
            self.edit_status = tk.Entry(self.edit_window)
            self.edit_status.grid(row=3, column=1)
            self.edit_status.insert(0, values[4])

            # 保存ボタン
            tk.Button(self.edit_window, text="保存", command=lambda: self.save_edited_row(selected_item)).grid(row=4, column=0, columnspan=2)

    def save_edited_row(self, item):
        """編集されたデータを保存"""
        new_user_id = self.edit_user_id.get()
        new_date = self.edit_date.get()
        new_time_slot = self.edit_time_slot.get()
        new_status = self.edit_status.get()

        # データベースの更新
        lot_id = self.tree.item(item, "values")[0]
        self.db_manager.update_lot(lot_id, new_user_id, new_date, new_time_slot, new_status)

        # Treeviewの表示を更新
        self.tree.item(item, values=(lot_id, new_user_id, new_date, new_time_slot, new_status))

        self.edit_window.destroy()

    def delete_selected_row(self):
        """選択された行を削除する際に確認する"""
        selected_item = self.tree.selection()

        if selected_item:
            # 選択された行のIDを取得
            lot_id = self.tree.item(selected_item, "values")[0]

            # 確認ダイアログを表示
            confirm = messagebox.askyesno("削除の確認", "本当に削除しますか？")
            
            if confirm:
                # ユーザーが削除を承認した場合のみ削除を実行
                self.db_manager.delete_lot(lot_id)

                # Treeviewから削除
                self.tree.delete(selected_item)
                messagebox.showinfo("削除完了", "選択した予約が削除されました。")
            else:
                messagebox.showinfo("キャンセル", "削除がキャンセルされました。")


    def clear_frame(self):
        """ウィジェットをすべてクリアする"""
        for widget in self.root.winfo_children():
            widget.destroy()

if __name__ == '__main__':
    root = tk.Tk()
    app = Application(root)
    root.mainloop()
