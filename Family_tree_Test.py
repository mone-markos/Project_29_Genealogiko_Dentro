import sys
import json
import networkx as nx
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import (
    QApplication, QWidget, QPushButton, QVBoxLayout,
    QLabel, QLineEdit, QComboBox, QTextEdit, QListWidget,
    QFileDialog, QMessageBox
)

class GenealogyApp(QWidget):
    def __init__(self):
        super().__init__()
        self.data = {}  # Store people and relationships
        self.initUI()
    
    def initUI(self):
        layout = QVBoxLayout()
        
        self.name_input = QLineEdit(self)
        self.name_input.setPlaceholderText("Enter Name")
        layout.addWidget(QLabel("Name:"))
        layout.addWidget(self.name_input)
        
        self.birth_input = QLineEdit(self)
        self.birth_input.setPlaceholderText("Enter Birthdate")
        layout.addWidget(QLabel("Birthdate:"))
        layout.addWidget(self.birth_input)
        
        self.relation_input = QComboBox(self)
        self.relation_input.addItems(["Parent", "Spouse", "Child"])
        layout.addWidget(QLabel("Relation Type:"))
        layout.addWidget(self.relation_input)
        
        self.related_person = QLineEdit(self)
        self.related_person.setPlaceholderText("Related Person Name")
        layout.addWidget(QLabel("Related To:"))
        layout.addWidget(self.related_person)
        
        self.add_btn = QPushButton("Add Person", self)
        self.add_btn.clicked.connect(self.add_person)
        layout.addWidget(self.add_btn)
        
        self.save_btn = QPushButton("Save Data", self)
        self.save_btn.clicked.connect(self.save_data)
        layout.addWidget(self.save_btn)
        
        self.load_btn = QPushButton("Load Data", self)
        self.load_btn.clicked.connect(self.load_data)
        layout.addWidget(self.load_btn)
        
        self.view_tree_btn = QPushButton("View Family Tree", self)
        self.view_tree_btn.clicked.connect(self.view_tree)
        layout.addWidget(self.view_tree_btn)
        
        self.setLayout(layout)
        self.setWindowTitle("Genealogy Tree")
        self.setGeometry(100, 100, 400, 300)
    
    def add_person(self):
        name = self.name_input.text()
        birthdate = self.birth_input.text()
        relation = self.relation_input.currentText()
        related_to = self.related_person.text()
        
        if not name:
            QMessageBox.warning(self, "Input Error", "Name is required!")
            return
        
        if name not in self.data:
            self.data[name] = {"birthdate": birthdate, "relations": {}}
        
        if related_to and related_to in self.data:
            self.data[name]["relations"][related_to] = relation
            self.data[related_to]["relations"][name] = relation
        
        QMessageBox.information(self, "Success", f"{name} added successfully!")
    
    def save_data(self):
        file_name, _ = QFileDialog.getSaveFileName(self, "Save File", "", "JSON Files (*.json)")
        if file_name:
            with open(file_name, 'w') as file:
                json.dump(self.data, file)
            QMessageBox.information(self, "Success", "Data saved successfully!")
    
    def load_data(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Load File", "", "JSON Files (*.json)")
        if file_name:
            with open(file_name, 'r') as file:
                self.data = json.load(file)
            QMessageBox.information(self, "Success", "Data loaded successfully!")
    
    def view_tree(self):
        if not self.data:
            QMessageBox.warning(self, "Error", "No data available!")
            return
        
        G = nx.DiGraph()
        for person, details in self.data.items():
            G.add_node(person)
            for related, relation in details["relations"].items():
                G.add_edge(person, related, label=relation)
        
        plt.figure(figsize=(10, 6))
        pos = nx.spring_layout(G)
        nx.draw(G, pos, with_labels=True, node_color='lightblue', edge_color='gray')
        edge_labels = nx.get_edge_attributes(G, 'label')
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
        plt.title("Family Tree")
        plt.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = GenealogyApp()
    window.show()
    sys.exit(app.exec_())
