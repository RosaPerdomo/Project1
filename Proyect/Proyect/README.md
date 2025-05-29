# Graph Application

This project is a graph application that allows users to visualize and interact with graphs. It includes functionalities for adding and deleting nodes and segments, loading and saving graphs, and refreshing the plot. The application also supports zooming with the mouse wheel and dragging the graph with the right mouse button.

## Project Structure

- **interface.py**: Main application logic for the graph interface.
- **node.py**: Defines the Node class, representing a node in the graph.
- **segment.py**: Defines the Segment class, representing a connection between two nodes.
- **graph.py**: Manages a collection of nodes and segments.
- **path.py**: Contains functions or classes related to pathfinding within the graph.
- **airSpace.py**: Manages airspace data for aviation-related graphs.
- **KML.py**: Exports graph data to KML format for geographic representation.
- **sonidos/**: Contains sound files for sound effects and background music.
- **Cat_nav.txt, Cat_seg.txt, Cat_aer.txt**: Data files for the airspace of Catalonia.
- **ECAC_nav.txt, ECAC_seg.txt, ECAC_aer.txt**: Data files for the airspace of Europe.
- **Spain_nav.txt, Spain_seg.txt, Spain_aer.txt**: Data files for the airspace of Spain.
- **clippy.png**: Image file used as a mascot or helper character.
- **Grup 10.png**: Project logo image file.

## Installation

1. Clone the repository:
   ```
   git clone <repository-url>
   ```
2. Navigate to the project directory:
   ```
   cd Proyect
   ```
3. Install the required dependencies (if any).

## Usage

- Run the application by executing `interface.py`.
- Use the interface to load graphs, add or delete nodes and segments, and explore the graph visually.
- Utilize the mouse wheel to zoom in and out, and drag the graph using the right mouse button.

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue for any suggestions or improvements.

## License

This project is licensed under the MIT License. See the LICENSE file for details.