
"""
# Euclidean distance formula to calculate the distance between two latittude and longitude points
def calculate_distance(coord1, coord2):
    #tuple unpacking of coordinates 
    lat1, lon1 = coord1
    lat2, lon2 = coord2
    
    # Calculate the differences
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    
    # Convert the differences from degrees to kilometers
    km_per_degree_latitude = 111
    km_per_degree_longitude = 111 * math.cos(math.radians(lat1))

    # Euclidean formula
    distance = math.sqrt((dlat * km_per_degree_latitude) ** 2 + (dlon * km_per_degree_longitude) ** 2)
    return distance
"""

import math

def calculate_distance(coord1, coord2):
    """
    Calculate the Haversine distance between two points on the Earth.
    
    Parameters:
    coord1: tuple of (latitude, longitude) for the first point in degrees.
    coord2: tuple of (latitude, longitude) for the second point in degrees.
    
    Returns:
    Distance between the two points in kilometers.
    """
    # Convert latitude and longitude from degrees to radians.
    lat1, lon1 = math.radians(coord1[0]), math.radians(coord1[1])
    lat2, lon2 = math.radians(coord2[0]), math.radians(coord2[1])
    
    # Differences between the coordinates.
    dlat = lat2 - lat1
    dlon = lon2 - lon1

    # Haversine formula.
    a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    R = 6371  # Earth's radius in kilometers.
    distance = R * c

    return distance


# R-Tree Node class
class RTreeNode:
    # Initializes a node, which can be either an internal node or a leaf node.
    # - `is_leaf`: Determines if the node is a leaf (holds data points) or an internal node (holds child nodes).
    # - `children`: Stores either other RTreeNodes (if internal) or actual hospital data points (if leaf).
    # - `bounding_box`: A rectangular area defined by min and max latitude/longitude values that encloses all its children.
    def __init__(self, is_leaf=False):
        self.is_leaf = is_leaf
        self.children = []
        self.bounding_box = None  # Min and max lat/long for the node

    # Inserts a hospital into the R-Tree and adjusts the bounding box.
    # If the node is a leaf and exceeds capacity, it will split.
    def insert(self, hospital):
        if self.is_leaf:
            # If it's a leaf, add the hospital data to the children.
            self.children.append(hospital)
            # Adjust the bounding box to include the new data point.
            self.adjust_bounding_box()
            if len(self.children) > 4:  # Max capacity reached, split the node
                return self.split()  # Splits the node into two if it has too many children.
        else:
            # If it's an internal node, find the best child to insert the hospital into.
            best_child = self.choose_best_child(hospital)
            # Recursively insert the hospital into the selected child node.
            new_node = best_child.insert(hospital)
            # If the child node split, add the new node to the current node.
            if new_node:
                self.children.append(new_node)
                # Adjust the bounding box after adding the new child.
                self.adjust_bounding_box()
        return None

    # Adjusts the bounding box to fit all children within this node.
    def adjust_bounding_box(self):
        if not self.children:
            return

        # If the node is a leaf, adjust the bounding box to fit all hospital locations.
        if self.is_leaf:
            min_lat = min(child["latitude"] for child in self.children)
            max_lat = max(child["latitude"] for child in self.children)
            min_lon = min(child["longitude"] for child in self.children)
            max_lon = max(child["longitude"] for child in self.children)
        else:
            # If it's an internal node, adjust the bounding box to fit all child bounding boxes.
            min_lat = min(child.bounding_box[0][0] for child in self.children)
            max_lat = max(child.bounding_box[1][0] for child in self.children)
            min_lon = min(child.bounding_box[0][1] for child in self.children)
            max_lon = max(child.bounding_box[1][1] for child in self.children)

        self.bounding_box = ((min_lat, min_lon), (max_lat, max_lon))

    # Splits the node into two, creating a new node with half of the current node's children.
    def split(self):
        mid_index = len(self.children) // 2
        new_node = RTreeNode(is_leaf=self.is_leaf)
        new_node.children = self.children[mid_index:]  # Move the second half to the new node.
        self.children = self.children[:mid_index]  # Keep the first half in the current node.
        self.adjust_bounding_box()  # Adjust bounding boxes for both nodes.
        new_node.adjust_bounding_box()
        return new_node

    # Chooses the best child node to insert a new hospital into, based on distance.
    def choose_best_child(self, hospital):
        best_child = None
        min_distance = float('inf')  # Initialize with infinity to find the minimum distance.

        # Get the hospital's latitude and longitude.
        hospital_lat = hospital["latitude"]
        hospital_lon = hospital["longitude"]

        # Iterate through each child and calculate the distance to find the best one.
        for child in self.children:
            # Get the child's bounding box coordinates (assuming lower-left corner for comparison).
            child_lat = child.bounding_box[0][0]
            child_lon = child.bounding_box[0][1]

            # Calculate the distance between the hospital and the child's bounding box corner.
            distance = calculate_distance((child_lat, child_lon), (hospital_lat, hospital_lon))

            # Find the child with the minimum distance.
            if distance < min_distance:
                min_distance = distance
                best_child = child

        return best_child
    
    def delete(self, hospital):
        if self.is_leaf:
            # If it's a leaf node, try to remove the hospital directly.
            if hospital in self.children:
                self.children.remove(hospital)
                self.adjust_bounding_box()
                return True  # Hospital removed successfully
            return False  # Hospital not found

        # If it's an internal node, recursively try to delete from child nodes.
        for child in self.children:
            # Check if the hospital's coordinates fall within the child's bounding box.
            if self.is_within_bounding_box(hospital, child.bounding_box):
                if child.delete(hospital):
                    # If the child has fewer than the minimum allowed children after deletion,
                    # it may need to be merged or adjusted.
                    if len(child.children) < 2:  # Example threshold, may vary based on your implementation.
                        self.children.remove(child)  # Remove the child node.
                        self.adjust_bounding_box()
                    return True  # Hospital deleted successfully

        return False  # Hospital not found

# Helper function to determine if a hospital's coordinates are within a given bounding box.
    def is_within_bounding_box(self, hospital, bounding_box):
        lat, lon = hospital["latitude"], hospital["longitude"]
        min_lat, min_lon = bounding_box[0]
        max_lat, max_lon = bounding_box[1]
        return min_lat <= lat <= max_lat and min_lon <= lon <= max_lon




# R-Tree class, manages the overall structure and operations of the R-Tree.
class RTree:
    # Initializes the R-Tree with a root node.
    def __init__(self):
        self.root = RTreeNode(is_leaf=True)  # Start with a leaf node as the root.

    # Inserts a hospital into the R-Tree.
    def insert_hospital(self, hospital):
        new_node = self.root.insert(hospital)  # Inserts the hospital into the root.
        if new_node:  # If the root split, create a new root.
            new_root = RTreeNode(is_leaf=False)
            new_root.children = [self.root, new_node]  # The old root and new node become children of the new root.
            new_root.adjust_bounding_box()  # Adjust the bounding box for the new root.
            self.root = new_root
    
    # Searches for the nearest hospitals within a given distance range.
    def search_nearest(self, user_location, max_results=3, distance_range=None):
        nearest_hospitals = []
        # Start the search from the root node.
        self._nearest_search(self.root, user_location, nearest_hospitals, max_results, distance_range)
        # Sort the hospitals by distance and return the nearest ones.
        return sorted(nearest_hospitals, key=lambda h: calculate_distance(user_location, (h['latitude'], h['longitude'])))

    # Recursively searches for hospitals in the tree that are within the distance range.
    def _nearest_search(self, node, user_location, nearest_hospitals, max_results, distance_range):
        # If the node is a leaf, check distances of all hospitals directly.
        if node.is_leaf:
            for hospital in node.children:
                dist = calculate_distance(user_location, (hospital['latitude'], hospital['longitude']))
                # If within the specified distance, add the hospital to the results.
                if distance_range is None or dist <= distance_range:
                    nearest_hospitals.append(hospital)
        else:
            # If it's an internal node, recursively search each child node.
            for child in node.children:
                self._nearest_search(child, user_location, nearest_hospitals, max_results, distance_range)
    def delete_hospital(self, hospital):
        """ Delete a hospital from the R-Tree. """
        if self.root.delete(hospital):
            if not self.root.children and not self.root.is_leaf:
                # If the root becomes empty, reset to a new leaf node.
                self.root = RTreeNode(is_leaf=True)
            return True  # Hospital deleted successfully
        return False  # Hospital not found