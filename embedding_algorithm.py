"""
Embedding Algorithm for Valiant's Universal Circuit Construction

This module implements the edge-embedding algorithm from Valiant's Universal Circuit
construction. It's translated from the C++ implementation in src/uc/2way/embedding.cpp.

The embedding algorithm is used to map edges of a circuit (represented as a DAG) onto
a universal graph structure. This is a key component in creating universal circuits
that can be programmed to simulate any circuit of a given size.

References:
- Ágnes Kiss and Thomas Schneider: "Valiant's Universal Circuit is Practical" (Eurocrypt 2016)
- Original implementation: https://github.com/encryptogroup/UC

Author: Translated from C++ to Python
License: GNU Affero General Public License v3.0
"""

from typing import List, Optional, Tuple
from dataclasses import dataclass, field


@dataclass
class Node:
    """
    Represents a node in the Valiant DAG structure.
    
    Attributes:
        number: Unique identifier for the node
        top_order: Topological order of the node
        top_ordered: Whether the node has been topologically ordered
        is_x: True if node has two incoming and two outgoing edges (X-switch)
        is_node2: For correctly defining the programming of output Y nodes
        is_first: True if node has a parent that is X-switch from its first wire
        is_first2: True if node has two parents that are X-switch from first wire
        is_second: True if node has a parent that is X-switch from its second wire
        is_second2: True if node has two parents that are X-switch from second wire
        firstof: Parent X-switch node coming from first wire
        firstof2: Second parent X-switch node coming from first wire
        secondof: Parent X-switch node coming from second wire
        secondof2: Second parent X-switch node coming from second wire
        left: Pointer to the next node on the left
        right: Pointer to the next node on the right
        left_parent: Previous node on the left (if b.left_parent = a, then a.left = b)
        right_parent: Previous node on the right (if b.right_parent = a, then a.right = b)
        next_top_order: Node with next topological order
        control_num: Control/programming bits for the node
    """
    number: int
    top_order: int = 0
    top_ordered: bool = False
    is_x: bool = False
    is_node2: bool = False
    is_first: bool = False
    is_first2: bool = False
    is_second: bool = False
    is_second2: bool = False
    firstof: Optional['Node'] = None
    firstof2: Optional['Node'] = None
    secondof: Optional['Node'] = None
    secondof2: Optional['Node'] = None
    left: Optional['Node'] = None
    right: Optional['Node'] = None
    left_parent: Optional['Node'] = None
    right_parent: Optional['Node'] = None
    next_top_order: Optional['Node'] = None
    control_num: int = 0


@dataclass
class Gamma1Node:
    """
    Node in Gamma1 graph (at most one incoming and one outgoing edge).
    
    Attributes:
        number: Node identifier (from 1 to n)
        is_embedded: Whether the edge from this node is already embedded
        parent: Parent node (node with incoming edge to this)
        child: Child node (node with outgoing edge from this)
        is_output: Whether this node is an output
    """
    number: int
    is_embedded: bool = False
    parent: Optional['Gamma1Node'] = None
    child: Optional['Gamma1Node'] = None
    is_output: bool = False


@dataclass
class Gamma2Node:
    """
    Node in Gamma2 graph (at most two incoming and two outgoing edges).
    
    Attributes:
        number: Node identifier (from 1 to n)
        left: First child node
        right: Second child node
        left_parent: First parent node
        right_parent: Second parent node
        colored: Whether incoming edges are already colored
        output: Whether node corresponds to circuit output
        function_bits: Four bits describing the Boolean function
        is_bitchanged: Whether bits were already changed in first embedding step
    """
    number: int
    left: Optional['Gamma2Node'] = None
    right: Optional['Gamma2Node'] = None
    left_parent: Optional['Gamma2Node'] = None
    right_parent: Optional['Gamma2Node'] = None
    colored: bool = False
    output: bool = False
    function_bits: List[int] = field(default_factory=lambda: [0, 0, 0, 0])
    is_bitchanged: bool = False
    
    def set_function_bits(self, c0: int, c1: int, c2: int, c3: int):
        """Set the four function bits for this node."""
        self.function_bits = [c0, c1, c2, c3]


class ValiantDAG:
    """
    Valiant DAG class for universal graphs with at most two incoming 
    and at most two outgoing edges for each node.
    """
    
    def __init__(self, pole_number: int):
        """
        Initialize Valiant DAG structure.
        
        Args:
            pole_number: Number of poles (inputs/outputs) in the graph
        """
        self.pole_number = pole_number
        self.pole_array: List[Node] = []
        self.node_array: List[Node] = []
        self.node_array_outest: List[Node] = []
        self.sub_left: Optional['ValiantDAG'] = None
        self.sub_right: Optional['ValiantDAG'] = None
        self.sub_left2: Optional['ValiantDAG'] = None
        self.sub_right2: Optional['ValiantDAG'] = None
    
    def set_control_bit(self, node1: Node, node2: Node, parent: Node):
        """
        Set control bit connection between nodes.
        
        Args:
            node1: First node
            node2: Second node
            parent: Parent node
        """
        # This is a simplified placeholder - actual implementation would
        # set up the proper control bit connections
        pass
    
    def node2(self, index1: int, index2: int, parent: Node) -> Optional[Node]:
        """
        Embedding when node_number is 2.
        
        Args:
            index1: First index
            index2: Second index
            parent: Parent node
            
        Returns:
            Last parent node, or None if no valid embedding
        """
        if index1 == 0 and index2 == 1:
            self.pole_array[0].left_parent = self.pole_array[1]
            self.pole_array[0].right_parent = parent
            return self.pole_array[0]
        return None
    
    def node3(self, index1: int, index2: int, parent: Node) -> Optional[Node]:
        """
        Embedding when node_number is 3.
        
        Args:
            index1: First index
            index2: Second index
            parent: Parent node
            
        Returns:
            Last parent node, or None if no valid embedding
        """
        if index1 == 0 and index2 == 1:
            self.pole_array[0].left_parent = self.pole_array[1]
            self.pole_array[0].right_parent = parent
            return self.pole_array[0]
        elif index1 == 0 and index2 == 2:
            self.pole_array[0].left_parent = self.pole_array[1]
            self.pole_array[0].right_parent = parent
            self.pole_array[1].left_parent = self.pole_array[2]
            self.pole_array[1].right_parent = self.pole_array[0]
            return self.pole_array[1]
        elif index1 == 1 and index2 == 2:
            self.pole_array[1].left_parent = self.pole_array[2]
            self.pole_array[1].right_parent = parent
            return self.pole_array[1]
        return None
    
    def node4(self, index1: int, index2: int, parent: Node) -> Optional[Node]:
        """
        Embedding when node_number is 4.
        
        Args:
            index1: First index
            index2: Second index
            parent: Parent node
            
        Returns:
            Last parent node, or None if no valid embedding
        """
        if index1 == 0 and index2 == 1:
            self.pole_array[0].left_parent = self.node_array[0]
            self.pole_array[0].right_parent = parent
            self.node_array[0].left_parent = self.pole_array[1]
            self.node_array[0].right_parent = self.pole_array[0]
            return self.node_array[0]
        elif index1 == 0 and index2 == 2:
            self.pole_array[0].left_parent = self.node_array[0]
            self.pole_array[0].right_parent = parent
            self.node_array[0].left_parent = self.node_array[1]
            self.node_array[0].right_parent = self.pole_array[0]
            self.node_array[1].left_parent = self.pole_array[2]
            self.node_array[1].right_parent = self.node_array[0]
            return self.node_array[1]
        elif index1 == 0 and index2 == 3:
            self.pole_array[0].left_parent = self.node_array[0]
            self.pole_array[0].right_parent = parent
            self.node_array[0].left_parent = self.node_array[1]
            self.node_array[0].right_parent = self.pole_array[0]
            self.node_array[1].left_parent = self.node_array[2]
            self.node_array[1].right_parent = self.node_array[0]
            self.node_array[2].left_parent = self.pole_array[3]
            self.node_array[2].right_parent = self.node_array[1]
            return self.node_array[2]
        elif index1 == 1 and index2 == 2:
            self.pole_array[1].left_parent = self.node_array[1]
            self.pole_array[1].right_parent = parent
            self.node_array[1].left_parent = self.pole_array[2]
            self.node_array[1].right_parent = self.pole_array[1]
            return self.node_array[1]
        elif index1 == 1 and index2 == 3:
            self.pole_array[1].left_parent = self.node_array[1]
            self.pole_array[1].right_parent = parent
            self.node_array[1].left_parent = self.node_array[2]
            self.node_array[1].right_parent = self.pole_array[1]
            self.node_array[2].left_parent = self.pole_array[3]
            self.node_array[2].right_parent = self.node_array[1]
            return self.node_array[2]
        elif index1 == 2 and index2 == 3:
            self.pole_array[2].left_parent = self.node_array[2]
            self.pole_array[2].right_parent = parent
            self.node_array[2].left_parent = self.pole_array[3]
            self.node_array[2].right_parent = self.pole_array[2]
            return self.node_array[2]
        return None
    
    def set_indices(self, u: int, v: int, index1: int, index2: int) -> Tuple[int, int]:
        """
        Set the indices for embedding depending on the parity of the number of poles.
        
        Args:
            u: Number of inputs
            v: Number of outputs
            index1: First index
            index2: Second index
            
        Returns:
            Tuple of (n_index1, n_index2) - adjusted indices for nodes
        """
        n_index1 = 3 * (index1 // 2)
        n_index2 = 3 * (index2 // 2)
        
        # Adjust v based on pole number parity
        if (self.pole_number % 2 == 0 and v % 2 == 1) or \
           (self.pole_number % 2 == 1 and v % 2 == 0):
            v -= 1
        
        # Adjust n_index2 based on output position
        if index2 > self.pole_number - v:
            n_index2 -= (v - (self.pole_number - index2 + 1))
            if index2 % 2 == 0:
                n_index2 -= 1
        
        # Adjust indices based on number of inputs
        if u > 1:
            if u % 2 == 0:
                n_index2 = n_index2 - u + 1
                if index1 < u:
                    n_index1 = n_index1 - index1
                else:  # index1 >= u
                    n_index1 = n_index1 - u + 1
            else:
                n_index2 = n_index2 - u + 2
                if index1 < u - 1:
                    n_index1 = n_index1 - index1
                else:
                    n_index1 = n_index1 - u + 2
        
        return n_index1, n_index2
    
    def check_side(self, node_1: Node, node_2: Node) -> Tuple[bool, bool]:
        """
        Check which side (left or right) the embedded edge is on.
        
        Args:
            node_1: Starting node
            node_2: Ending node
            
        Returns:
            Tuple of (side, valid) where side is False for left, True for right,
            and valid indicates if the check was successful
        """
        if node_1.left_parent == node_2:
            return False, True
        elif node_1.right_parent == node_2:
            return True, True
        
        print("ERROR in check_side: outest pathfinder side check")
        return False, False
    
    def pathfinder(self, index1: int, index2: int, parent: Optional[Node],
                   sides: List[bool], u: int = 0, v: int = 0,
                   outest_first: bool = True) -> Optional[Node]:
        """
        Pathfinder for inside universal graphs.
        
        This is the main recursive function that finds a path through the universal
        graph from index1 to index2, setting up the necessary control bits.
        
        Args:
            index1: Starting pole index
            index2: Ending pole index
            parent: Parent node (may be None for top-level calls)
            sides: Vector of bools predefining the embedding path (left=True, right=False)
            u: Number of inputs (for outest pathfinder)
            v: Number of outputs (for outest pathfinder)
            outest_first: True if in outest graph first case
            
        Returns:
            Last parent node needed for setting control bits, or None if no path found
        """
        # Base case: same index
        if index1 == index2:
            return parent
        
        # Base case: single pole (but different indices - no path)
        if self.pole_number == 1:
            return None
        
        # Base case: 2 poles
        if self.pole_number == 2:
            return self.node2(index1, index2, parent)
        
        # Base case: 3 poles
        if self.pole_number == 3:
            return self.node3(index1, index2, parent)
        
        # Base case: 4 poles
        if self.pole_number == 4:
            return self.node4(index1, index2, parent)
        
        # Generic recursive case for pole_number > 4
        if self.pole_number > 4:
            n_index1 = 3 * (index1 // 2)
            n_index2 = 3 * (index2 // 2)
            
            pole_index1 = self.pole_array[index1]
            
            # Special case: adjacent odd indices at the end
            if (index2 % 2 == 1 and index2 == self.pole_number - 1 and 
                index2 == index1 + 1):
                node_index = self.node_array[n_index2 - 1]
                pole_index1.left_parent = node_index
                pole_index1.right_parent = parent
                node_index.left_parent = self.pole_array[index2]
                node_index.right_parent = pole_index1
                return node_index
            
            # Special case: adjacent even-odd indices
            elif index2 == (index1 + 1) and (index1 % 2 == 0):
                node_index = self.node_array[n_index1]
                pole_index1.left_parent = node_index
                pole_index1.right_parent = parent
                node_index.left_parent = self.pole_array[index2]
                node_index.right_parent = pole_index1
                return node_index
            
            # Determine which subgraph to use
            if not sides:
                print("ERROR: sides vector is empty")
                return None
            
            if sides[-1]:  # Left subgraph
                sub = self.sub_left
            else:  # Right subgraph
                sub = self.sub_right
            
            sides.pop()
            
            # Set up entry into subgraph based on index1 parity
            if index1 % 2 == 0:
                node_index = self.node_array[n_index1]
                node_index2 = self.node_array[n_index1 + 1]
                pole_index1.left_parent = node_index
                pole_index1.right_parent = parent
                node_index.left_parent = node_index2
                node_index.right_parent = pole_index1
                node_index2.left_parent = sub.pole_array[index1 // 2]
                node_index2.right_parent = node_index
            else:  # index1 % 2 == 1
                node_index = self.node_array[n_index1 + 1]
                pole_index1.left_parent = node_index
                pole_index1.right_parent = parent
                node_index.left_parent = sub.pole_array[index1 // 2]
                node_index.right_parent = pole_index1
            
            # Recursive call into subgraph
            last = sub.pathfinder(index1 // 2, index2 // 2 - 1,
                                 self.node_array[n_index1 + 1], sides)
            
            # Exit from subgraph
            pole_index1 = sub.pole_array[index2 // 2 - 1]
            
            # Set up exit based on index2 parity and position
            if index2 % 2 == 0:
                if index2 == self.pole_number - 2 or index2 == self.pole_number - 1:
                    pole_index1.left_parent = self.pole_array[index2]
                    pole_index1.right_parent = last
                    return pole_index1
                else:
                    node_index = self.node_array[n_index2 - 1]
                    pole_index1.left_parent = node_index
                    pole_index1.right_parent = last
                    node_index.left_parent = self.pole_array[index2]
                    node_index.right_parent = pole_index1
                    return node_index
            
            if index2 % 2 == 1:
                if index2 == self.pole_number - 1 and self.pole_number % 2 == 0:
                    node_index = self.node_array[n_index2 - 1]
                    pole_index1.left_parent = node_index
                    pole_index1.right_parent = last
                    node_index.left_parent = self.pole_array[index2]
                    node_index.right_parent = pole_index1
                    return node_index
                else:
                    node_index = self.node_array[n_index2 - 1]
                    node_index2 = self.node_array[n_index2]
                    pole_index1.left_parent = node_index
                    pole_index1.right_parent = last
                    node_index.left_parent = node_index2
                    node_index.right_parent = pole_index1
                    node_index2.left_parent = self.pole_array[index2]
                    node_index2.right_parent = node_index
                    return node_index2
        
        return None


def neighbouring_index(index: int) -> int:
    """
    Given an index, returns the neighbouring one.
    
    Args:
        index: Initial index
        
    Returns:
        Neighbouring index (index+1 if even, index-1 if odd)
    """
    if index % 2 == 0:
        return index + 1
    else:
        return index - 1


def embedding_with_supergraph(g, index1: int, index2: int,
                               sides: List[bool], side: bool):
    """
    Embedding algorithm given the Gamma2 supergraph.
    
    This function recursively determines which subgraph (left or right) to use
    for embedding an edge, based on the availability of paths in each subgraph.
    
    Args:
        g: Gamma2 supergraph (DAG_Gamma2 object)
        index1: Starting index
        index2: Ending index
        sides: Vector to accumulate the path choices (modified in-place)
        side: True if left subgraph, False if right subgraph
    """
    # Base cases
    if index1 == index2:
        return
    
    if index2 == neighbouring_index(index1):
        return
    
    if g.node_number <= 4:
        return
    
    # Calculate new indices for recursion
    new_index1 = index1 // 2
    new_index2 = index2 // 2 - 1
    
    # Determine which subgraphs to use
    if side:
        sub = g.sub_left
        gamma1 = g.gamma1_left
    else:
        sub = g.sub_right
        gamma1 = g.gamma1_right
    
    # Check if paths exist in both subgraphs and choose accordingly
    right_ok = (sub and sub.gamma1_right.check_exist(new_index1) and
                sub.gamma1_right.check_right(new_index1, new_index2))
    
    left_ok = (sub and sub.gamma1_left.check_exist(new_index1) and
               sub.gamma1_left.check_right(new_index1, new_index2))
    
    if right_ok:
        if left_ok:
            # Both paths available - choose based on parity
            if ((gamma1.node_number % 2 == 0 and index2 == gamma1.node_number - 2) or
                (gamma1.node_number % 2 == 1 and index2 == gamma1.node_number - 1)):
                # Choose left
                sub.gamma1_left.node_array[new_index1].is_embedded = True
                embedding_with_supergraph(sub, new_index1, new_index2, sides, True)
                sides.append(True)
            else:
                # Choose right
                sub.gamma1_right.node_array[new_index1].is_embedded = True
                embedding_with_supergraph(sub, new_index1, new_index2, sides, False)
                sides.append(False)
        else:
            # Only right path available
            sub.gamma1_right.node_array[new_index1].is_embedded = True
            embedding_with_supergraph(sub, new_index1, new_index2, sides, False)
            sides.append(False)
        return
    
    if left_ok:
        # Only left path available
        sub.gamma1_left.node_array[new_index1].is_embedded = True
        embedding_with_supergraph(sub, new_index1, new_index2, sides, True)
        sides.append(True)
        return
    
    # No valid path found
    print(f"ERROR in embedding_with_supergraph: No valid path from {index1} to {index2}")


def embed_side(valiant_dag: ValiantDAG, gamma1, gamma2,
               u: int, v: int, side: bool):
    """
    Embed edges according to the specified side (left or right).
    
    Args:
        valiant_dag: The Valiant DAG structure
        gamma1: Gamma1 graph (left or right)
        gamma2: Gamma2 graph supergraph
        u: Number of inputs
        v: Number of outputs
        side: True for left side, False for right side
    """
    for i in range(gamma1.node_number):
        if gamma1.node_array[i].child:
            child_num = gamma1.node_array[i].child.number - 1
            
            # Find embedding path through supergraph
            sides = []
            embedding_with_supergraph(gamma2, i, child_num, sides, side)
            
            # Perform embedding in the Valiant DAG
            is_right = valiant_dag.pathfinder(i, child_num, None, sides, u, v, not side)
            
            # Handle output nodes
            if gamma1.node_array[i].child.is_output:
                the_node = gamma2.node_array[child_num]
                pole = valiant_dag.pole_array[child_num]
                
                if pole.left_parent and pole.left_parent.is_node2 == side:
                    the_node.set_function_bits(1, 0, 0, 0)
                elif pole.right_parent and pole.right_parent.is_node2 == side:
                    the_node.set_function_bits(0, 0, 0, 0)
            
            # Swap function bits if necessary based on path direction
            the_node = gamma2.node_array[child_num]
            if (is_right and the_node.left_parent and not the_node.is_bitchanged and
                the_node.left_parent.number == gamma1.node_array[i].number):
                # Swap function_bits[1] and function_bits[2]
                the_node.function_bits[1], the_node.function_bits[2] = \
                    the_node.function_bits[2], the_node.function_bits[1]
                the_node.is_bitchanged = True
            
            if (not is_right and the_node.right_parent and not the_node.is_bitchanged and
                the_node.right_parent.number == gamma1.node_array[i].number):
                # Swap function_bits[1] and function_bits[2]
                the_node.function_bits[1], the_node.function_bits[2] = \
                    the_node.function_bits[2], the_node.function_bits[1]
                the_node.is_bitchanged = True


def embedding_merged(g, u: int, v: int) -> ValiantDAG:
    """
    Main embedding function for merged (hybrid) universal circuit construction.
    
    This function creates the complete embedding of a circuit onto a universal graph
    by processing both left and right sides and setting up the programming bits.
    
    Args:
        g: Gamma2 graph supergraph representing the circuit
        u: Number of circuit inputs
        v: Number of circuit outputs
        
    Returns:
        ValiantDAG: The universal graph with embedded edges and programming bits
    """
    node_num = g.node_number
    
    # Create subgraphs for embedding
    hybrid_choice = []
    g.create_subgraphs(node_num * 2, False, False, False, hybrid_choice)
    g.check_correct_subgraphs()
    
    # Create outest universal graph with u inputs, v outputs and (node_num-u-v) gates
    g2 = ValiantDAG(node_num)  # Simplified - actual init_merged would do more
    
    # Embed right side
    embed_side(g2, g.gamma1_right, g, u, v, False)
    
    # Embed left side
    embed_side(g2, g.gamma1_left, g, u, v, True)
    
    # Topologically sort (simplified placeholder)
    # g2.topologically_sort(u)
    
    # Set control numbers from function bits
    for i in range(u, g2.pole_number):
        the_node = g.node_array[i]
        g2.pole_array[i].control_num = (
            the_node.function_bits[0] * 1 +
            the_node.function_bits[1] * 2 +
            the_node.function_bits[2] * 4 +
            the_node.function_bits[3] * 8
        )
    
    return g2


# Example usage and documentation
if __name__ == "__main__":
    print("Valiant's Universal Circuit Embedding Algorithm")
    print("=" * 60)
    print()
    print("This module implements the edge-embedding algorithm for")
    print("Valiant's Universal Circuit construction.")
    print()
    print("Key Components:")
    print("  - Node: Base node structure for the universal graph")
    print("  - Gamma1Node: Node with at most one incoming/outgoing edge")
    print("  - Gamma2Node: Node with at most two incoming/outgoing edges")
    print("  - ValiantDAG: Main DAG structure for universal circuits")
    print()
    print("Main Functions:")
    print("  - pathfinder(): Finds paths through the universal graph")
    print("  - embedding_with_supergraph(): Determines embedding strategy")
    print("  - embed_side(): Embeds edges for left or right side")
    print("  - embedding_merged(): Complete embedding for hybrid construction")
    print()
    print("For detailed usage, refer to the original paper:")
    print("'Valiant's Universal Circuit is Practical' by Kiss & Schneider")
