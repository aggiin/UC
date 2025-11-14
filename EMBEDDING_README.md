# Embedding Algorithm - Python Implementation

## 概述 (Overview)

这是 Valiant 通用电路嵌入算法的 Python 实现，从原始的 C++ 代码 (`src/uc/2way/embedding.cpp`) 翻译而来。

This is a Python implementation of Valiant's Universal Circuit embedding algorithm, translated from the original C++ code in `src/uc/2way/embedding.cpp`.

## 文件说明 (File Description)

- **embedding_algorithm.py**: 完整的 Python 实现，包含嵌入算法的所有核心功能

## 核心概念 (Core Concepts)

### 1. 通用电路 (Universal Circuits)

通用电路是一种可以通过编程来模拟任意给定大小电路的电路结构。Valiant 的构造方法使用递归的图结构来实现这一目标。

Universal Circuits are circuit structures that can be programmed to simulate any circuit of a given size. Valiant's construction uses recursive graph structures to achieve this.

### 2. 嵌入算法 (Embedding Algorithm)

嵌入算法的目的是将原始电路的边映射到通用图结构上。这个过程包括：

The embedding algorithm maps edges from the original circuit onto the universal graph structure. This process includes:

- **路径查找 (Pathfinding)**: 在通用图中找到连接两个节点的路径
- **控制位设置 (Control Bit Setting)**: 设置开关节点的控制位来实现所需的连接
- **递归分解 (Recursive Decomposition)**: 将大问题分解为子图中的小问题

## 主要数据结构 (Main Data Structures)

### Node

表示 Valiant DAG 中的基本节点，包含：
- 拓扑顺序信息
- 父节点和子节点指针
- X-switch 和 Y-switch 标记
- 控制位信息

Represents a basic node in the Valiant DAG, containing:
- Topological order information
- Parent and child node pointers
- X-switch and Y-switch markers
- Control bit information

### Gamma1Node

Gamma1 图中的节点，特点：
- 最多一条入边和一条出边
- 用于预定义嵌入路径

Nodes in Gamma1 graphs, characterized by:
- At most one incoming and one outgoing edge
- Used for predefining embedding paths

### Gamma2Node

Gamma2 图中的节点，特点：
- 最多两条入边和两条出边
- 包含布尔函数的四位表示
- 支持边着色

Nodes in Gamma2 graphs, characterized by:
- At most two incoming and two outgoing edges
- Contains 4-bit representation of Boolean functions
- Supports edge coloring

### ValiantDAG

主要的 DAG 结构类，包含：
- pole_array: 输入/输出极点数组
- node_array: 内部节点数组
- 子图指针（左/右递归结构）

Main DAG structure class, containing:
- pole_array: Array of input/output poles
- node_array: Array of internal nodes
- Subgraph pointers (left/right recursive structure)

## 核心函数 (Core Functions)

### 1. pathfinder()

```python
def pathfinder(self, index1: int, index2: int, parent: Optional[Node],
               sides: List[bool], u: int = 0, v: int = 0,
               outest_first: bool = True) -> Optional[Node]
```

**功能 (Function)**: 在通用图中寻找从 index1 到 index2 的路径

**参数 (Parameters)**:
- `index1`: 起始极点索引 (Starting pole index)
- `index2`: 结束极点索引 (Ending pole index)
- `parent`: 父节点 (Parent node)
- `sides`: 预定义嵌入路径的布尔向量 (Boolean vector predefining the embedding path)
- `u`: 输入数量 (Number of inputs)
- `v`: 输出数量 (Number of outputs)
- `outest_first`: 是否在最外层图的第一种情况 (Whether in outest graph first case)

**工作原理 (How it works)**:
1. 处理基本情况（2、3、4 个节点）
2. 对于更大的图，递归分解为子图
3. 根据索引的奇偶性选择路径
4. 设置必要的控制位连接

### 2. node2(), node3(), node4()

基本情况的嵌入函数，处理节点数为 2、3、4 时的特殊情况。

Base case embedding functions for handling special cases with 2, 3, or 4 nodes.

**特点 (Features)**:
- 直接设置节点之间的连接
- 不需要递归
- 覆盖所有可能的索引组合

### 3. embedding_with_supergraph()

```python
def embedding_with_supergraph(g, index1: int, index2: int,
                               sides: List[bool], side: bool)
```

**功能 (Function)**: 基于 Gamma2 超图确定嵌入策略

**工作流程 (Workflow)**:
1. 检查左右子图中是否存在有效路径
2. 根据可用性和奇偶性选择子图
3. 递归处理子图
4. 将选择记录在 `sides` 向量中

### 4. embed_side()

```python
def embed_side(valiant_dag: ValiantDAG, gamma1, gamma2,
               u: int, v: int, side: bool)
```

**功能 (Function)**: 对左侧或右侧进行嵌入

**步骤 (Steps)**:
1. 遍历 Gamma1 图中的所有节点
2. 为每条边找到嵌入路径
3. 调用 pathfinder 执行实际嵌入
4. 处理输出节点的特殊情况
5. 根据路径方向交换函数位

### 5. embedding_merged()

```python
def embedding_merged(g, u: int, v: int) -> ValiantDAG
```

**功能 (Function)**: 混合通用电路构造的主嵌入函数

**完整流程 (Complete Workflow)**:
1. 创建嵌入所需的子图
2. 初始化 Valiant DAG 结构
3. 嵌入右侧
4. 嵌入左侧
5. 拓扑排序
6. 设置控制位和编程位

## 算法复杂度 (Algorithm Complexity)

- **时间复杂度 (Time Complexity)**: O(n log n)，其中 n 是电路大小
- **空间复杂度 (Space Complexity)**: O(n)，用于存储节点和边

## 使用示例 (Usage Example)

```python
from embedding_algorithm import ValiantDAG, embedding_merged, Node

# 创建 Valiant DAG 结构
# Create Valiant DAG structure
valiant_dag = ValiantDAG(pole_number=10)

# 执行嵌入（假设已有 gamma2 图）
# Perform embedding (assuming gamma2 graph exists)
# result = embedding_merged(gamma2_graph, u=5, v=3)

# 访问嵌入结果
# Access embedding results
# for pole in result.pole_array:
#     print(f"Pole {pole.number}: control_num = {pole.control_num}")
```

## 与原始 C++ 实现的差异 (Differences from Original C++ Implementation)

1. **内存管理 (Memory Management)**: Python 使用自动垃圾回收，不需要手动内存管理
2. **类型系统 (Type System)**: 使用 Python 的类型提示而不是 C++ 的强类型
3. **数据结构 (Data Structures)**: 使用 Python 的 List 代替 C++ 的数组和向量
4. **调试输出 (Debug Output)**: 简化了调试宏，使用简单的 print 语句

## 技术细节 (Technical Details)

### 极点索引 (Pole Indexing)

极点按顺序编号，索引从 0 开始：
- 偶数索引：2k → 进入左子图的第 k 个极点
- 奇数索引：2k+1 → 进入右子图的第 k 个极点

Poles are numbered sequentially, starting from index 0:
- Even indices: 2k → kth pole entering left subgraph
- Odd indices: 2k+1 → kth pole entering right subgraph

### 节点数组 (Node Array)

对于每对极点，有 3 个中间节点：
- n_index = 3 * (pole_index // 2)
- 节点 n_index, n_index+1, n_index+2 用于路由

For each pair of poles, there are 3 intermediate nodes:
- n_index = 3 * (pole_index // 2)
- Nodes n_index, n_index+1, n_index+2 used for routing

### 控制位 (Control Bits)

- **X-switch**: 1 个控制位（交换/不交换）
- **Y-switch**: 1 个控制位（选择左/右输入）
- **U-gate**: 4 个控制位（完整的真值表）

### 递归结构 (Recursive Structure)

通用图递归地分为左右子图：
- 极点数从 n 减少到约 n/2
- 递归深度：O(log n)
- 基本情况：2、3 或 4 个极点

The universal graph is recursively divided into left and right subgraphs:
- Pole count reduces from n to approximately n/2
- Recursion depth: O(log n)
- Base cases: 2, 3, or 4 poles

## 参考文献 (References)

1. Leslie G. Valiant, "Universal circuits (Preliminary Report)", STOC 1976
2. Ágnes Kiss and Thomas Schneider, "Valiant's Universal Circuit is Practical", Eurocrypt 2016
3. Daniel Günther, Ágnes Kiss and Thomas Schneider, "More Efficient Universal Circuit Constructions", Asiacrypt 2017

## 许可证 (License)

GNU Affero General Public License v3.0

Original implementation copyright (C) 2016 Engineering Cryptographic Protocols Group, TU Darmstadt

## 联系方式 (Contact)

For questions about the original C++ implementation, see: https://github.com/encryptogroup/UC

This Python translation is provided for educational and research purposes.
