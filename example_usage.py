#!/usr/bin/env python3
"""
Example Usage of the Embedding Algorithm

This script demonstrates how to use the embedding algorithm module.
It shows basic usage patterns and explains the key concepts.

示例：嵌入算法的使用方法
这个脚本演示如何使用嵌入算法模块，展示基本的使用模式并解释关键概念。
"""

from embedding_algorithm import (
    Node, Gamma1Node, Gamma2Node, ValiantDAG,
    embedding_with_supergraph, embed_side,
    embedding_merged, neighbouring_index
)


def example_1_basic_nodes():
    """
    Example 1: Creating basic node structures
    示例 1: 创建基本的节点结构
    """
    print("=" * 60)
    print("Example 1: Creating Basic Node Structures")
    print("示例 1: 创建基本的节点结构")
    print("=" * 60)
    
    # Create a simple node in Valiant DAG
    node1 = Node(number=0)
    node2 = Node(number=1)
    
    print(f"Created node1: number={node1.number}, top_order={node1.top_order}")
    print(f"Created node2: number={node2.number}, is_x={node2.is_x}")
    
    # Create Gamma1 nodes (at most one edge in/out)
    gamma1_node1 = Gamma1Node(number=1)
    gamma1_node2 = Gamma1Node(number=2)
    gamma1_node1.child = gamma1_node2
    gamma1_node2.parent = gamma1_node1
    
    print(f"\nGamma1 node chain: {gamma1_node1.number} -> {gamma1_node1.child.number}")
    
    # Create Gamma2 nodes (at most two edges in/out)
    gamma2_node = Gamma2Node(number=1)
    gamma2_node.set_function_bits(0, 1, 1, 0)
    
    print(f"Gamma2 node: number={gamma2_node.number}, function_bits={gamma2_node.function_bits}")
    print()


def example_2_valiant_dag():
    """
    Example 2: Creating a Valiant DAG structure
    示例 2: 创建 Valiant DAG 结构
    """
    print("=" * 60)
    print("Example 2: Creating Valiant DAG Structure")
    print("示例 2: 创建 Valiant DAG 结构")
    print("=" * 60)
    
    # Create a Valiant DAG with 4 poles
    dag = ValiantDAG(pole_number=4)
    
    print(f"Created Valiant DAG with {dag.pole_number} poles")
    
    # Initialize pole array
    dag.pole_array = [Node(number=i) for i in range(dag.pole_number)]
    print(f"Initialized {len(dag.pole_array)} poles")
    
    # Initialize node array (3 nodes per pair of poles for routing)
    num_nodes = 3 * (dag.pole_number // 2)
    dag.node_array = [Node(number=i) for i in range(num_nodes)]
    print(f"Initialized {len(dag.node_array)} internal nodes")
    
    print()


def example_3_neighbouring_index():
    """
    Example 3: Using the neighbouring_index function
    示例 3: 使用 neighbouring_index 函数
    """
    print("=" * 60)
    print("Example 3: Neighbouring Index Function")
    print("示例 3: neighbouring_index 函数")
    print("=" * 60)
    
    # Demonstrate neighbouring index calculation
    # Even indices pair with the next odd index
    # Odd indices pair with the previous even index
    
    test_indices = [0, 1, 2, 3, 4, 5]
    print("Index -> Neighbouring Index")
    print("索引 -> 相邻索引")
    for idx in test_indices:
        neighbour = neighbouring_index(idx)
        print(f"  {idx} -> {neighbour}")
    
    print()


def example_4_base_cases():
    """
    Example 4: Demonstrating base case embeddings
    示例 4: 演示基本情况的嵌入
    """
    print("=" * 60)
    print("Example 4: Base Case Embeddings")
    print("示例 4: 基本情况的嵌入")
    print("=" * 60)
    
    # Example with 2 poles
    dag2 = ValiantDAG(pole_number=2)
    dag2.pole_array = [Node(number=i) for i in range(2)]
    
    print("Testing node2 embedding (2 poles):")
    print("测试 node2 嵌入（2个极点）:")
    result = dag2.node2(0, 1, None)
    if result:
        print(f"  Successfully embedded path from pole 0 to pole 1")
        print(f"  成功嵌入从极点 0 到极点 1 的路径")
    
    # Example with 3 poles
    dag3 = ValiantDAG(pole_number=3)
    dag3.pole_array = [Node(number=i) for i in range(3)]
    
    print("\nTesting node3 embedding (3 poles):")
    print("测试 node3 嵌入（3个极点）:")
    result = dag3.node3(0, 2, None)
    if result:
        print(f"  Successfully embedded path from pole 0 to pole 2")
        print(f"  成功嵌入从极点 0 到极点 2 的路径")
    
    # Example with 4 poles
    dag4 = ValiantDAG(pole_number=4)
    dag4.pole_array = [Node(number=i) for i in range(4)]
    dag4.node_array = [Node(number=i) for i in range(6)]  # 3 nodes per pair
    
    print("\nTesting node4 embedding (4 poles):")
    print("测试 node4 嵌入（4个极点）:")
    result = dag4.node4(1, 3, None)
    if result:
        print(f"  Successfully embedded path from pole 1 to pole 3")
        print(f"  成功嵌入从极点 1 到极点 3 的路径")
    
    print()


def example_5_algorithm_explanation():
    """
    Example 5: High-level explanation of the algorithm
    示例 5: 算法的高层次解释
    """
    print("=" * 60)
    print("Example 5: Algorithm Explanation")
    print("示例 5: 算法解释")
    print("=" * 60)
    
    explanation = """
    The embedding algorithm works as follows:
    嵌入算法的工作原理如下：
    
    1. PATHFINDING (路径查找):
       - Find a path from source pole to destination pole
       - 从源极点找到目标极点的路径
       
    2. BASE CASES (基本情况):
       - For 2, 3, or 4 poles, use direct embeddings
       - 对于 2、3 或 4 个极点，使用直接嵌入
       
    3. RECURSIVE CASE (递归情况):
       - Divide graph into left and right subgraphs
       - 将图分为左右子图
       - Recursively embed in subgraphs
       - 在子图中递归嵌入
       - Pole 2k goes to left subgraph position k
       - 极点 2k 进入左子图的第 k 个位置
       - Pole 2k+1 goes to right subgraph position k
       - 极点 2k+1 进入右子图的第 k 个位置
       
    4. CONTROL BITS (控制位):
       - X-switch: 1 bit (swap or pass-through)
       - X开关：1位（交换或直通）
       - Y-switch: 1 bit (select left or right input)
       - Y开关：1位（选择左或右输入）
       - U-gate: 4 bits (full truth table)
       - U门：4位（完整真值表）
       
    5. COMPLEXITY (复杂度):
       - Time: O(n log n) where n is circuit size
       - 时间：O(n log n)，其中 n 是电路大小
       - Space: O(n) for nodes and edges
       - 空间：O(n) 用于节点和边
    """
    
    print(explanation)


def main():
    """
    Main function to run all examples
    主函数，运行所有示例
    """
    print("\n")
    print("╔" + "=" * 58 + "╗")
    print("║  Valiant's Universal Circuit Embedding Algorithm Demo  ║")
    print("║  Valiant 通用电路嵌入算法演示                          ║")
    print("╚" + "=" * 58 + "╝")
    print("\n")
    
    # Run all examples
    example_1_basic_nodes()
    example_2_valiant_dag()
    example_3_neighbouring_index()
    example_4_base_cases()
    example_5_algorithm_explanation()
    
    print("=" * 60)
    print("All examples completed successfully!")
    print("所有示例成功完成！")
    print("=" * 60)
    print()
    print("For more details, see:")
    print("更多详情，请参阅：")
    print("  - EMBEDDING_README.md (documentation)")
    print("  - embedding_algorithm.py (source code)")
    print("  - src/uc/2way/embedding.cpp (original C++ implementation)")
    print()


if __name__ == "__main__":
    main()
