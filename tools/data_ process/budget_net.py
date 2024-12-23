import torch
import torch.nn as nn
from budget_data import BudgetData


class BudgetModel(nn.Module):
    def __init__(self, input_size, hidden_size, output_size):
        super(BudgetModel, self).__init__()
        self.fc1 = nn.Linear(input_size, hidden_size)
        self.relu = nn.ReLU()
        self.fc2 = nn.Linear(hidden_size, output_size)

    def forward(self, x):
        out = self.fc1(x)
        out = self.relu(out)
        out = self.fc2(out)
        return out


def traning_mode():
  
    budgetData= BudgetData("")
    train_data, _, _, _= budgetData.load_data()
    train_loader, val_loader, _=budgetData.load_dataset()

    output_len=len(budgetData.data['预算科目'].unique())
    model = BudgetModel(input_size=len(train_data.columns) - 1, hidden_size=128, output_size=output_len)
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
