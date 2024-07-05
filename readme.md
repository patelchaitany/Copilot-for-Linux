# 📄 Copilot for Linux

## 💡 Project Idea

This project provides a solution to search across all PDF files on a system using word embeddings for summarization. By leveraging the power of Word2Vec, the project can find and return relevant documents based on user queries, even if the exact keywords are not present in the documents.

## 🚀 How to Run the Project

### Prerequisites

Ensure you have the following installed:

- Python 3.7 or higher
- Required Python packages (listed below)

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/patelchaitany/Copilot-for-Linux
   cd Copilot-for-Linux
   ```

2. **Install the required packages:**
   ```bash
   pip install -r requirements.txt
   ```
3. **Install Chromadb:**
    ```bash
    Run Chromadb On localhost and port 8000
    ```
### Usage

1. **Run the script:**
   ```bash
   python main.py --size <max-file-size-in-MB>
   ```
   Replace `<max-file-size-in-MB>` with the maximum size of PDF files you want to process.

2. **Input your query:**
   When prompted, enter the word or phrase you want to search for in the PDF documents.

3. **View the results:**
   The script will display the list of PDFs containing the relevant information.

### Example

```bash
python main.py --size 10
Word need to search in document: machine learning
```

This command processes all PDF files under the user's home directory that are less than 10 MB in size and searches for the term "machine learning".

### Project Structure

```
.
├── directory.py          # Handles directory structure and file comparisons
├── embedding.py          # Manages document embeddings and queries
├── main.py               # Main script to execute the project
├── requirements.txt      # List of dependencies
└── README.md             # Project documentation
```

### 🔧 Troubleshooting

- Ensure all dependencies are installed.
- Make sure your PDF files are accessible and not corrupted.

### 🤝 Contributing

Feel free to fork this repository, make your changes, and submit a pull request. Contributions are welcome!


