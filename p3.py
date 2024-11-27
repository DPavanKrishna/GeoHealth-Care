# Trie Node class for searching by name/address with partial matches
class TrieNode:
    def __init__(self):
        # Initialize each node with a dictionary of children and a list of hospitals.
        # 'children' stores references to child nodes based on characters.
        # 'hospitals' stores the list of hospitals that end at this node.
        self.children = {}
        self.hospitals = []

class Trie:
    def __init__(self):
        # Initialize the Trie with a root node, which is an empty TrieNode.
        self.root = TrieNode()

    def insert(self, key, hospital):
        """Insert a hospital into the Trie based on the key (name or address)."""
        # Start from the root node for each insertion.
        node = self.root
        # Traverse through each character in the key (converted to lowercase for case insensitivity).
        for char in key.lower():
            # If the character is not already a child of the current node, add a new TrieNode.
            if char not in node.children:
                node.children[char] = TrieNode()
            # Move to the child node corresponding to the character.
            node = node.children[char]
        # After traversing all characters, add the hospital to the node's hospital list.
        node.hospitals.append(hospital)

    def search(self, partial_key):
        """Search for hospitals based on a partial key (name or address)."""
        # Start from the root node for each search.
        node = self.root
        # Traverse through each character in the partial key (converted to lowercase for case insensitivity).
        for char in partial_key.lower():
            # If the character is not found among the current node's children, return an empty list (no matches).
            if char not in node.children:
                return []  # No matches found
            # Move to the child node corresponding to the character.
            node = node.children[char]
        # Collect all hospitals from the last matched node and its descendants.
        return self._collect_all_hospitals(node)

    def _collect_all_hospitals(self, node):
        """Collect all hospitals from the current node and its children."""
        # Start with the hospitals at the current node.
        hospitals = list(node.hospitals)
        # Recursively collect hospitals from each child node.
        for child_node in node.children.values():
            hospitals.extend(self._collect_all_hospitals(child_node))
        # Return the aggregated list of hospitals.
    def starts_with(self, prefix):
        """Checks if there is any word in the Trie that starts with the given prefix."""
        node = self.root
        for char in prefix.lower():
            if char not in node.children:
                return False  # No matches found
            node = node.children[char]
        return True  # Prefix found

    def autocomplete(self, prefix):
        """Returns all hospitals in the Trie that start with the given prefix."""
        node = self.root
        for char in prefix.lower():
            if char not in node.children:
                return []  # No matches found
            node = node.children[char]
        return self._collect_all_hospitals(node)
    
    def delete(self, key):
        # Recursive helper function to delete a key
        def delete_recursive(node, key, depth):
            if depth == len(key):
                if '$' in node:
                    del node['$']  # Remove the end-of-word marker
                    return len(node) == 0  # If the node is empty, return True to indicate that it should be removed
                return False

            char = key[depth]
            if char in node:
                can_delete = delete_recursive(node[char], key, depth + 1)
                if can_delete:
                    del node[char]
                    return len(node) == 0
            return False

    def _collect_all_hospitals(self, node):
        """Collect all hospitals from the current node and its children."""
        hospitals = list(node.hospitals)
        for child_node in node.children.values():
            hospitals.extend(self._collect_all_hospitals(child_node))
        return hospitals
