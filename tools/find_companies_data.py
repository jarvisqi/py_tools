import pandas as pd

# 需要显示的列名
required_columns = ['企业名称', '现有人数', '正式编制人数', '需求总人数', '需求人数差', '项目部数量']
# 需要查询的企业
parent_company_names = ['']
# 文件路径
file_path = '/Desktop/财务人员信息统计-7041400.xlsx'


# 查询子企业包括本身
def get_child_companies_data_including_parent(df, parent_company_names):
    # 初始化父级企业字典
    companies_data = {company: pd.DataFrame() for company in parent_company_names}
    for parent_company_name in parent_company_names:
        # 查找当前父公司的所有子公司，包括自身
        child_companies_data = find_child_companies(df, parent_company_name)
        parent_data = df[df['企业名称'] == parent_company_name]
        if not parent_data.empty:
            child_companies_data = pd.concat([parent_data, child_companies_data], ignore_index=True)
        
        if not child_companies_data.empty:
            companies_data[parent_company_name] = child_companies_data[required_columns[:-1]] 
    
    return companies_data

# 查找所以子企业
def find_child_companies(df, parent_company_name):
    child_companies = df[df['父级企业名称'] == parent_company_name]
    if child_companies.empty:
        return pd.DataFrame()
    child_data = pd.DataFrame()
    for _, child_company in child_companies.iterrows():
        child_company_name = child_company['企业名称']
        child_company_data = find_child_companies(df, child_company_name)
        child_data = pd.concat([child_data, child_company_data], ignore_index=True)
    # 将子公司的数据与当前子公司的数据合并
    child_data = pd.concat([child_companies, child_data], ignore_index=True)
    return child_data


def main():
    df = pd.read_excel(file_path)
    child_companies_data_including_parent = get_child_companies_data_including_parent(df, parent_company_names)

    # 保存数据
    output_file_path = '../shudao_child_companies_data.xlsx'
    with pd.ExcelWriter(output_file_path) as writer:
        for company, data in child_companies_data_including_parent.items():
            data.to_excel(writer, sheet_name=company, index=False)

# 执行main函数
if __name__ == "__main__":
    main()

