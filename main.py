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
