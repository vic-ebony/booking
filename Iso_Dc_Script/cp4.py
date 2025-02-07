error_files = []
def batch_process_folder(folder_path, replacements, new_revision_date, target_height, target_width, tolerance=0.15, new_date=None):
    global error_files
    for root, _, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            if file.endswith(".docx") or file.endswith(".doc"):
                print(f"正在處理 Word 文件: {file_path}")
                try:
                    word_app = win32.gencache.EnsureDispatch("Word.Application")
                    doc = word_app.Documents.Open(file_path)

                    # 替換修訂日期
                    replace_revision_date(doc, new_revision_date)

                    # 更新頒佈日期
                    if new_date:
                        update_word_table(file_path, new_date)

                    doc.Save()
                    print(f"已成功處理 Word 文件: {file_path}")
                except Exception as e:
                    error_files.append(file_path)
                    print(f"處理 Word 文件時發生錯誤: {file_path}, 錯誤訊息: {e}")
                finally:
                    try:
                        if doc:
                            doc.Close(False)
                    except:
                        pass
                    try:
                        if word_app:
                            word_app.Quit()
                    except:
                        pass
    if error_files:
        print("處理失敗的文件列表：")
        for error_file in error_files:
            print(error_file)
