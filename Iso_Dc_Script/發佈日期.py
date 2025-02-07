import os
import win32com.client as win32
import openpyxl

def is_within_tolerance(value, target, tolerance):
    """
    判斷數值是否在目標值的允許範圍內。
    """
    return target * (1 - tolerance) <= value <= target * (1 + tolerance)

def replace_text_in_word(doc_path, replacements):
    """
    使用 Word 的內建功能替換正文、頁首與頁尾的文字，並保持字體格式不變。
    """
    word_app = win32.gencache.EnsureDispatch("Word.Application")
    word_app.Visible = False

    try:
        doc = word_app.Documents.Open(doc_path)
        for old_text, new_text in replacements.items():
            # 替換正文
            word_app.Selection.Find.ClearFormatting()
            word_app.Selection.Find.Execute(
                FindText=old_text,
                ReplaceWith=new_text,
                Replace=win32.constants.wdReplaceAll,
                Format=False
            )
            for section in doc.Sections:
                # 替換頁首
                header_range = section.Headers(win32.constants.wdHeaderFooterPrimary).Range
                header_range.Find.ClearFormatting()
                header_range.Find.Execute(
                    FindText=old_text,
                    ReplaceWith=new_text,
                    Replace=win32.constants.wdReplaceAll,
                    Format=False
                )
                # 替換頁尾
                footer_range = section.Footers(win32.constants.wdHeaderFooterPrimary).Range
                footer_range.Find.ClearFormatting()
                footer_range.Find.Execute(
                    FindText=old_text,
                    ReplaceWith=new_text,
                    Replace=win32.constants.wdReplaceAll,
                    Format=False
                )
        doc.Save()
        print(f"已成功處理 Word 文件: {doc_path}")
    except Exception as e:
        print(f"處理 Word 文件時發生錯誤: {doc_path}, 錯誤訊息: {e}")
    finally:
        doc.Close(False)
        word_app.Quit()

def remove_images_by_size_in_word(doc_path, target_height, target_width, tolerance=0.15):
    """
    在 Word 文件中移除符合指定大小的圖片，包括正文和頁首。
    """
    word_app = win32.gencache.EnsureDispatch("Word.Application")
    word_app.Visible = False

    try:
        doc = word_app.Documents.Open(doc_path)
        for shape in doc.Shapes:
            if shape.Type == 3:  # 圖片類型
                height_cm = shape.Height / 28.3465
                width_cm = shape.Width / 28.3465
                if (is_within_tolerance(height_cm, target_height, tolerance) and
                        is_within_tolerance(width_cm, target_width, tolerance)):
                    shape.Delete()
        for inline_shape in doc.InlineShapes:
            if inline_shape.Type == 3:  # 圖片類型
                height_cm = inline_shape.Height / 28.3465
                width_cm = inline_shape.Width / 28.3465
                if (is_within_tolerance(height_cm, target_height, tolerance) and
                        is_within_tolerance(width_cm, target_width, tolerance)):
                    inline_shape.Delete()
        for section in doc.Sections:
            header_range = section.Headers(win32.constants.wdHeaderFooterPrimary).Range
            for shape in header_range.ShapeRange:
                if shape.Type == 3:
                    height_cm = shape.Height / 28.3465
                    width_cm = shape.Width / 28.3465
                    if (is_within_tolerance(height_cm, target_height, tolerance) and
                            is_within_tolerance(width_cm, target_width, tolerance)):
                        shape.Delete()
            for inline_shape in header_range.InlineShapes:
                if inline_shape.Type == 3:
                    height_cm = inline_shape.Height / 28.3465
                    width_cm = inline_shape.Width / 28.3465
                    if (is_within_tolerance(height_cm, target_height, tolerance) and
                            is_within_tolerance(width_cm, target_width, tolerance)):
                        inline_shape.Delete()
        doc.Save()
        print(f"已成功移除 Word 文件中的指定大小圖片：{doc_path}")
    except Exception as e:
        print(f"處理 Word 文件時發生錯誤：{doc_path}, 錯誤訊息：{e}")
    finally:
        doc.Close(False)
        word_app.Quit()

def replace_text_in_excel(file_path, replacements):
    """
    在 Excel 文件中進行文字替換。
    """
    wb = openpyxl.load_workbook(file_path)
    for sheet in wb.worksheets:
        for row in sheet.iter_rows():
            for cell in row:
                if cell.value and isinstance(cell.value, str):
                    for old_text, new_text in replacements.items():
                        cell.value = cell.value.replace(old_text, new_text)
    wb.save(file_path)
    print(f"已成功處理 Excel 文件: {file_path}")

def update_word_table(doc_path, new_date):
    """
    更新 Word 文件中第一頁表格中包含 "頒佈日期" 的欄位的日期。
    """
    word_app = win32.gencache.EnsureDispatch("Word.Application")
    word_app.Visible = False

    try:
        doc = word_app.Documents.Open(doc_path)
        table = doc.Tables(1)  # 獲取第一個表格
        for row in table.Rows:
            cell_text = row.Cells(1).Range.Text.strip()
            if "頒佈日期" in cell_text:
                row.Cells(2).Range.Text = new_date
                break
        doc.Save()
        print(f"已成功更新 Word 文件中的表格日期: {doc_path}")
    except Exception as e:
        print(f"更新 Word 文件中的表格日期時發生錯誤: {doc_path}, 錯誤訊息: {e}")
    finally:
        doc.Close(False)
        word_app.Quit()

def batch_process_folder(folder_path, replacements, target_height, target_width, tolerance=0.15, new_date=None):
    """
    批次處理資料夾中的 Word 和 Excel 文件，進行文字替換及移除指定大小的圖片。
    """
    for root, _, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            if file.endswith(".docx") or file.endswith(".doc"):
                print(f"正在處理 Word 文件: {file_path}")
                replace_text_in_word(file_path, replacements)
                remove_images_by_size_in_word(file_path, target_height, target_width, tolerance)
                if new_date:
                    update_word_table(file_path, new_date)
            elif file.endswith(".xlsx") or file.endswith(".xls"):
                print(f"正在處理 Excel 文件: {file_path}")
                replace_text_in_excel(file_path, replacements)

# 使用範例
if __name__ == "__main__":
    folder_path = r"C:\Users\31628\Desktop\新增資料夾"
    replacements = {
        "昇恆昌": "金坊國際",
        "ER": "KF",
        "2.01": "1.01",
        "2.02": "1.01",
        "版本：2.01": "版本：1.01",
        "版本：2.02": "版本：1.01",
    }
    target_height = 0.9  # 目標高度（公分）
    target_width = 3.23  # 目標寬度（公分）
    tolerance = 0.15  # 容差範圍（15%）
    new_date = "2029.12.12"  # 新的頒佈日期

    if os.path.exists(folder_path):
        batch_process_folder(folder_path, replacements, target_height, target_width, tolerance, new_date)
    else:
        print("路徑無效，請檢查後重新執行程式。")