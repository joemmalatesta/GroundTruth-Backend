import chromadb
from chromadb.utils import embedding_functions
import os

# Initialize OpenAI embedding function
openai_ef = embedding_functions.OpenAIEmbeddingFunction(
    api_key=os.environ.get("OPENAI_API_KEY"),
    model_name="text-embedding-ada-002"
)

# Initialize Chroma client with persistence
client = chromadb.PersistentClient(path="./chroma_db")

# Get the existing collection
collection = client.get_collection(name="sentry_docs", embedding_function=openai_ef)

# Query the collection
query = """File Path: packages/feedback/src/screenshot/components/ScreenshotEditor.tsx

Broader Context:
The file ScreenshotEditor.tsx is likely part of a larger feedback or annotation tool, allowing users to take and edit screenshots, particularly focusing on cropping functionality. The code touches several critical areas related to user interaction with screenshots, primarily:

Canvas Element and Ref Management:

The cropping functionality is managed using an HTML canvas element (croppingRef). The cropping area is controlled with the croppingRect state, which tracks the boundaries of the cropping box (i.e., start and end positions of the crop on the X and Y axes).
State Management:

Several new states were added to control dragging (isDragging), resizing (isResizing), and cropping confirmation (confirmCrop). These states are essential for handling user actions when they interact with the screenshot editor.
Event Handlers:

The main handlers, onDragStart, handleMouseMove, and handleMouseUp, control how a user drags the cropping box. The code changes focus on setting up the initial drag position, then using mouse move events to adjust the crop area dynamically while dragging.
These handlers could tie into documentation on how user interactions are managed in components (mouse events, state updates, etc.).
UI Behavior:

The cursor style is dynamically updated to provide feedback to users when they confirm a crop (confirmCrop), switching the cursor to a move pointer, which is typically a good practice for visual feedback in UI interactions.
Potential Documentation Areas:
Screenshot Editing Components: If there's a section or file in your documentation that discusses cropping, dragging, or resizing screenshot elements, this is likely where you'd find corresponding documentation. Look for any docs related to user interactions in screenshot tools.

Canvas and Refs: Documentation around the use of HTML5 Canvas elements for drawing, cropping, or other screenshot modifications might also be relevant. Refs like croppingRef are pivotal to this code.

State Management and Hooks: The use of React state and hooks (like useState and useRef) for managing the editor's cropping and dragging functionality could be documented under a section dealing with interactive components or UI state management in the project.

Given that the file path is tied to feedback/screenshot functionality, the most relevant documentation would likely be under sections related to screenshot handling, feedback UI components, or event-driven interactions in your app's codebase."""
results = collection.query(
    query_texts=[query],
    n_results=1,
    include=["metadatas", "documents"]
)

if results['metadatas']:
    closest_match = results['metadatas'][0][0]
    document_content = results['documents'][0][0]
    print(f"The closest match to '{query}' is:")
    print(f"Title: {closest_match['title']}")
    print(f"Type: {closest_match['type']}")
    print(f"URL: {closest_match['url']}")
else:
    print(f"No results found for '{query}'.")
