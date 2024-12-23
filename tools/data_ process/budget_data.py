import pandas as pd
import torch
from torch.utils.data import Dataset, DataLoader
from sklearn.preprocessing import LabelEncoder, StandardScaler


class BudgetData(Dataset):

    def __init__(self, path):
        self.data = pd.read_csv(path)

    def load_data(self):
        """
        读取并预处理数据，划分训练集、验证集和测试集
        """
        data = self.data
        label_encoders = {}
        categorical_cols = ["企业名称", "资金用途", "资金科目"]
        for col in categorical_cols:
            le = LabelEncoder()
            data[col] = le.fit_transform(data[col])
            label_encoders[col] = le

        # 归一化数值
        scaler = StandardScaler()
        data["金额"] = scaler.fit_transform(data[["金额"]])

        train_data = data.sample(frac=0.7, random_state=42)
        remaining_data = data.drop(train_data.index)
        val_data = remaining_data.sample(frac=0.5, random_state=42)
        test_data = remaining_data.drop(val_data.index)

        return train_data, remaining_data, val_data, test_data

    def create_dataset(self, input_data):
        """
        根据输入的数据创建Dataset对象实例
        """
        self.data = input_data
        self.x = torch.tensor(
            self.data.drop("预算科目", axis=1).values, dtype=torch.float32
        )
        self.y = torch.tensor(self.data["预算科目"].values, dtype=torch.long)
        return self

    def target_data(self):
        return self.data["预算科目"]

    def __len__(self):
        return len(self.data) if hasattr(self, "data") else 0

    def __getitem__(self, idx):
        return self.x[idx], (
            self.y[idx] if hasattr(self, "x") and hasattr(self, "y") else (None, None)
        )

    def load_dataset(self):
        """
        整体加载数据集，返回对应的数据加载器
        """
        train_data, _, val_data, test_data = self.load_data()

        train_dataset = self.create_dataset(train_data)
        val_dataset = self.create_dataset(val_data)
        test_dataset = self.create_dataset(test_data)

        train_loader = DataLoader(train_dataset, batch_size=32, shuffle=True)
        val_loader = DataLoader(val_dataset, batch_size=32)
        test_loader = DataLoader(test_dataset, batch_size=32)

        return train_loader, val_loader, test_loader
