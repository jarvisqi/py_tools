import numpy as np
import matplotlib.pyplot as plt


def main():
    A = [[2, 1, 2], [3, 1, 0], [1, 1, -1]]
    # 转置
    b = np.transpose([-3, 5, -2])
    # 求解未知参数矩阵X
    X = np.linalg.solve(A, b)
    print("方程组的解：\n", X)


def ols():
    # 数据初始化
    A = [[1, pow(-3, 3)],
         [1, pow(-2, 3)],
         [1, pow(-1, 3)],
         [1, pow(2, 3)],
         [1, pow(4, 3)]]
    # A的转置矩阵
    At = np.transpose(A)
    y = np.transpose([14.3, 8.3, 4.7, 8.3, 22.7])
    # step1:求解
    # 令 (a ,b)^T 为 未知参数X
    X = np.dot(np.dot(np.linalg.inv(np.dot(At, A)), At), y)
    print(X)
    print("a:", X[0])
    print("b:", X[1])
    
        # 1. 计算拟合数值 fitValue
    def fitValue(arg_x):
        a = X[0]
        b = X[1]
        return a + b*pow(arg_x, 3)

    x_2 = [-3, -2, -1, 2, 4]
    # 创建长为5的【一维】数组；[1,5]：创建第1行为5个元素的【二维】数组
    fitValues = np.zeros([5])
    for i in range(0, len(fitValues)):
        fitValues[i] = fitValue(x_2[i])
        print(i, ":", "x(i):", x_2[i], "fit Y:", fitValues[i])
        pass

    ## 2. 绘图可视化
    yt = np.transpose(y); # y的转置
    plt.rcParams['figure.dpi'] = 100 #分辨率
    plt.scatter(x_2, yt, marker = '*',color = 'red', s = 10 ,label = 'Actual Dataset') # 真实数据集
    plt.scatter(x_2, fitValues, marker = 'x',color = 'green', s = 10 ,label = 'Fitting Dataset') #[拟合数据集]
    plt.legend(loc = 'best')    # 设置 图例所在的位置 使用推荐位置
    plt.show() 


if __name__ == '__main__':
    # main()
    ols()
