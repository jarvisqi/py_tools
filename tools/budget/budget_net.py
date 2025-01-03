import torch
import torch.nn as nn
from budget_data import BudgetData


# 定义模型
class BudgetModel(nn.Module):
    def __init__(self, input_size, hidden_size, output_size):
        super(BudgetModel, self).__init__()
        self.fc1 = nn.Linear(input_size, hidden_size)
        self.relu = nn.ReLU()
        self.fc2 = nn.Linear(hidden_size, output_size)
        # Softmax 激活函数，将输出转换为概率分布。
        self.softmax = nn.Softmax(dim=1)

    def forward(self, x):
        out = self.fc1(x)
        out = self.relu(out)
        out = self.fc2(out)
        out = self.softmax(out)
        return out


def traning_model():
  
    budgetData= BudgetData("")
    train_data, _, _, _= budgetData.load_data()
    train_loader, val_loader, _=budgetData.load_dataset()
    output_len=len(budgetData.data['预算科目'].unique())

    input_len=len(train_data.columns) - 1
    # 初始化模型、损失函数和优化器
    model = BudgetModel(input_size=input_len, hidden_size=128, output_size=output_len)
    # CrossEntropyLoss 分类任务中常用的损失函数。
    criterion = nn.CrossEntropyLoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=0.001)

    num_epochs = 50
    for epoch in range(num_epochs):
        model.train()
        running_loss = 0.0
        for inputs, labels in train_loader:
            optimizer.zero_grad()
            outputs = model(inputs)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()
            running_loss += loss.item()
        epoch_loss = running_loss / len(train_loader)

        # 在验证集上评估模型
        model.eval()
        val_loss = 0.0,correct = 0,total = 0
        with torch.no_grad():
            for inputs, labels in val_loader:
                outputs = model(inputs)
                loss = criterion(outputs, labels)
                val_loss += loss.item()
                _, predicted = torch.max(outputs.data, 1)
                total += labels.size(0)
                correct += (predicted == labels).sum().item()
        val_accuracy = correct / total
        val_loss = val_loss / len(val_loader)

        print(f'Epoch {epoch + 1}/{num_epochs} - Train Loss: {epoch_loss:.4f} 
              - Val Loss: {val_loss:.4f} - Val Accuracy: {val_accuracy:.4f}')

    traced_script_module = torch.jit.trace(model, torch.randn(1, input_len))
    traced_script_module.save('budget_model.pt')
    print("Budget mode has been saved !")