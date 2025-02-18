import fitz

def remove_pdf_watermark(input_pdf_path, output_pdf_path):
    # 打开PDF文件
    doc = fitz.open(input_pdf_path)
    
    for page in doc:
        page.clean_contents()  # 清理页面绘图命令
        
        # 获取页面字节流
        xref = page.get_contents()[0]  # 获取页面字节流，以xref的形式返回        
        cont0 = doc.xref_stream(xref).decode()  # 将流解码为字符串

        # 打开文件并写入字节流
        with open("quanshan.txt", "wb") as file:
            file.write(cont0.encode())  # 将字符串编码为字节后写入文件
            
        print("字节流已保存为 quanshan.txt")
        
        # 尝试多次删除水印
        for _ in range(50):  # 最多尝试50次
            start = 0
            while True:
                # 查找水印的起始位置
                start = cont0.find("/Artifact", start)
                if start == -1:
                    break  # 没有找到更多水印，退出循环

                # 查找水印的结束位置
                end = cont0.find("EMC", start)
                if end != -1:
                    # 删除水印部分
                    cont0 = cont0[:start] + cont0[end+3:]  # end+3是因为"EMC"包含3个字符

                    # 更新字节流
                    doc.update_stream(xref, cont0.encode())  # 更新流
                    print("已删除一个水印")
                start = end + 3  # 继续查找下一个水印位置

        # 更新页面的内容
        page.clean_contents()  # 再次清理页面内容
        
    # 保存修改后的PDF文件        
    doc.save(output_pdf_path, garbage=4)
    doc.close()

# 调用函数去除水印
remove_pdf_watermark('jiagebiao.pdf', '000.pdf')


# ----------------------------------------------------------------

import pdfplumber
import pandas as pd

def extract_pdf_tables(pdf_path, output_format='csv'):
    """
    提取PDF中的表格并保存为指定格式
    参数：
        pdf_path: PDF文件路径
        output_format: 输出格式（csv/excel）
    """
    with pdfplumber.open(pdf_path) as pdf:
        all_tables = []
        
        # 遍历每一页
        for page_num, page in enumerate(pdf.pages):
            # 提取当前页表格
            tables = page.extract_tables()
            
            for table_num, table in enumerate(tables):
                # 将表格转换为DataFrame
                df = pd.DataFrame(table[1:], columns=table[0])
                df['source_page'] = page_num + 1
                all_tables.append(df)
                
                print(f"发现表格：第 {page_num+1} 页，表格 {table_num+1}")

    if not all_tables:
        return print("未检测到表格")

    # 合并所有表格
    final_df = pd.concat(all_tables, ignore_index=True)

    # 保存结果
    if output_format == 'csv':
        final_df.to_csv('extracted_tables.csv', index=False)
    elif output_format == 'excel':
        final_df.to_excel('extracted_tables.xlsx', index=False)
    
    print(f"表格已保存为 {output_format} 文件")

# 使用示例
extract_pdf_tables('000.pdf', output_format='excel')
# ----------------------------------------------------------------

