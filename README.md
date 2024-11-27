GeoHealth-Care

GeoHealth-Care is a Python-based project designed to revolutionize healthcare accessibility. By leveraging advanced data structures such as R-trees, heaps, tries, and stacks, GeoHealth provides a highly efficient platform for finding, ranking, and accessing information about healthcare facilities.

Features

Efficient Hospital Search

Utilizes R-trees for rapid nearest-hospital searches based on user location.

Offers highly optimized spatial indexing for large geographic datasets.

Top-Rated Hospital Discovery

Employs a max-heap to dynamically rank hospitals based on ratings and reviews.

Ensures efficient retrieval and updates for accurate rankings.

Comprehensive Hospital Information

Provides detailed data on hospital services, contact information, and availability.

Uses tries for quick searches by hospital name or city.

Search History Management

Tracks user queries with stacks for easy access to previously searched facilities.

Note:The Hospitals,rating,user_location are taken input as dictionary in the file itself

Setup Instructions

Prerequisites

Python 3.6 or above installed on your system.

Installation Steps

Clone the repository:

git clone https://github.com/yourusername/GeoHealth-Care.git
cd GeoHealth-Care

Run the main script to test the functionalities:

python p4.py

Project Structure



How to Use

Nearest Hospital Search:

change user_location

The system uses R-tree to find the nearest hospital.

Discover Top-Rated Hospitals:

View a ranked list of hospitals using the max-heap feature.

Search by Name or City:

Use partial or full search queries to find hospitals with tries.

Search History:

Access your recent searches stored in the stack.

Showcase Presentation

The project overview is available in the PowerPoint file located in the Documentation folder:

GeoHealth: Revolutionizing Healthcare Accessibility

Contributions

Contributions are welcome! Feel free to fork the repository, make changes, and submit a pull request.

License

This project is licensed under the MIT License. See the LICENSE file for details.

